import os
import json
import sys
from acquire import Acquire
from error import Error
from automatedAdmin import Admin
from automatedPlayer import AutomatedPlayer

def readJsonRequest(filepath):
    try:
        script_dir = os.getcwd()
        absolute_path = os.path.join(script_dir, filepath)
        with open(absolute_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data
    except Exception as e:
        return Error('Error while parsing json data.').to_dict()


class ATestHarness:
    def __init__(self,request, admin):
        self.board = request["board"]
        self.player = request["player"]
        self.remaining_tiles = request["tile"]
        self.remaining_hotels = request["xhotel"]
        self.remaining_shares = request["share"]
        self.admin = admin
        
        
    def validateTiles(self,playerTiles,remainingTiles,boardTiles):
        pset = set(frozenset(d.items()) for d in playerTiles)
        rset = set(frozenset(d.items()) for d in remainingTiles)
        bset = set(frozenset(d.items()) for d in boardTiles)
        if len(playerTiles+remainingTiles+boardTiles) == 108 and (pset.isdisjoint(bset) and rset.isdisjoint(bset) and pset.isdisjoint(rset)):
            print("TILETRUE")
            return True
        return False
    
    def getShare(self, shares, sharename):
        for share in shares:
            if share["share"] == sharename:
                return share
        return None
        
    def validateShares(self,shares, player):
        player_shares = player['shares']
        for share in shares:
            sh = self.getShare(player_shares, share["share"])
            if sh is not None:
                if int(share["count"]) + int(sh["count"]) != 25:
                    return False
            else:
                if int(share["count"]) != 25:
                    return False
        print("SHARETRUE")
        return True
            
    def hotelHelper(self,boardHotels):
        bset = []
        for d in boardHotels:
            bset.append(d["hotel"])
        return bset
    def validateHotels(self, boardHotels,remainingHotels):
        print(boardHotels)
        boardSet = set(self.hotelHelper(boardHotels))
        remainingHotelsSet = set(self.hotelHelper(remainingHotels))

        if boardSet.isdisjoint(remainingHotelsSet) and len(boardSet.union(remainingHotelsSet)) == 7:
            print("HOTELTRUE")
            return True
        return False
            
    def validateState(self):
        if self.validateHotels(self.board["hotels"],self.remaining_hotels) and self.validateShares(self.remaining_shares,self.player) and self.validateTiles(self.player["tiles"], self.remaining_tiles, self.board["tiles"]):
            return True
        return False
    

class TestDriver:
    def __init__(self,request):
        self.admin = Admin()
        self.request = request
        self.test_harness = ATestHarness(request,self.admin)
        self.strategies = ["ordered","random","smallest-anti","largest-alpha"]
        self.autoPlayer = AutomatedPlayer(self.test_harness.player,"ordered")
        
    def handleRequest(self):
        if not self.test_harness.validateState():
            return Error("State validations failed").to_dict()
        state = {"board":self.test_harness.board, "player":self.test_harness.player}
        self.admin.acquire.set_state(state, True)
        if self.admin.acquire.validate_board(self.admin.acquire.state["board"])[0]:
                tileRes = self.autoPlayer.playTile(self.admin) 
                shareRes = self.autoPlayer.buyShares(self.admin)
               
                win = False
                res, response = self.gameOver()
                if res:
                    win = True
                    
                response = {
                    "win":win,
                    "hotel":shareRes,
                    "place":tileRes
                }
                return response
                
        else:
            return Error("Invalid board")            
            
    def gameOver(self):
        flag = True
        for player in self.admin.acquire.state["players"]:
            if len(player.tiles) != 0:
                flag = False
                break  
        if flag:
            return True, "No playable Tiles"
        flag = False
        for hotel in self.admin.acquire.state["board"].hotels:
            if len(hotel["tiles"]) >= 41:
                flag = True
                return flag, hotel["hotel"] + " has 41 tiles"
            else:
                if len(self.admin.acquire.state["board"].hotels) == 7:
                    if len(hotel["tiles"]) > 11:
                        flag = True
                    else:
                        flag = False
                        break
                else:
                    flag = False
        if flag:
            return True, "All Hotels are safe"
        return False, "Game Continues"


if __name__ == "__main__":
    filename = sys.argv[1]
    request = readJsonRequest(filename)
    if type(request) != Error:
        testDriver = TestDriver(request)
        print(testDriver.handleRequest())
            
            
        
        