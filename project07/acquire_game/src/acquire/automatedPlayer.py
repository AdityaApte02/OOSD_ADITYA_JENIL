from automatedAdmin import Admin
from tile import Tile
import random
class AutomatedPlayer():
    def __init__(self, strategy, players):
        self.admin = Admin()
        self.admin.setUp({
            "request":"setup",
            "players":players
        })
        self.strategy = strategy
        
        
    def find_smallest_tile(self, tiles):
        smallest_tile = Tile(tiles[0]["row"],tiles[0]["column"])  # Assume the first tile is the smallest initially
        for tile in tiles:
            tile = Tile(tile["row"],tile["column"])
            if tile < smallest_tile:
                smallest_tile = tile
        return smallest_tile
    
    def gameOver(self):
        flag = False
        for hotel in self.admin.acquire.state["board"].hotels:
            if len(hotel["tiles"]) >= 41:
                flag = True
                return flag, hotel["hotel"]+" has 41 tiles"
            else:
                if len(self.admin.acquire.state["board"].hotels) == 7:
                    if len(hotel["tiles"]) > 11:
                        flag = True
                    else:
                        flag = False
                else:
                    flag = False 
        if flag:
            return True, "All Hotels are safe"
        return False, "Game Continues"
        
                
    def playTile(self):
        player = self.admin.acquire.state["players"][0]
        if self.strategy == "ordered":
            smallest_tile = self.find_smallest_tile(player.tiles)
            row = smallest_tile.row
            column = smallest_tile.column
            self.admin.place(row, column)
           
        if self.strategy == "random":
            index = random.randint(0,len(player.tiles) - 1)
            tile = Tile(player.tiles[index]["row"], player.tiles[index]["column"])
            row = tile.row
            column = tile.column
            self.admin.place(row, column)
            
    
    def buyShares(self):
        player = self.admin.acquire.state["players"][0]
        if self.strategy == "ordered":
            cntr = 3
            for share in sorted(list(self.admin.banker.remaining_shares.keys())):
                for i in range(3):
                    res, state = self.admin.buy_shares(share)
                    if res:
                        cntr -= 1
                    if cntr == 0:
                        self.admin.done()
                        return
            self.admin.done()
            
        if self.strategy == "random":
            placedHotels = []
            totalShares = 0
            for hotelName in list(self.admin.banker.remaining_shares.keys()):
                if hotelName not in self.admin.banker.remaining_hotels:
                    placedHotels.append(hotelName)
                    totalShares+=self.admin.banker.remaining_shares[hotelName]
            cntr = min(3,totalShares)
            while cntr!=0:
                idx = random.randint(0,len(placedHotels)-1)
                res,state = self.admin.buy_shares(placedHotels[idx])
                if "error" in state and state["error"] == "The player does not have enough cash to buy the shares":
                    break
                if res:
                    cntr-=1
                
            self.admin.done()
                    
        
        
if __name__ == '__main__':
    # player = AutomatedPlayer("ordered", ["Aditya", "Jenil"])
    player = AutomatedPlayer("ordered", ["Jenil", "Aditya"])
    flag = True
    while flag:
        print("==============================================================================")
        response = player.gameOver()
        if response[0]:
            print("response",response[1])
            flag = False
        else:
            player.playTile()
            player.buyShares()
        
   
        
        
print('Game Over!!!')
        
    