from tile import Tile
from automatedAdmin import Admin
from error import Error
from collections import defaultdict
class GameTree():
    def __init__(self,admin:Admin) -> None:
        self.admin = admin
        self.tree = None

    def canBuy(self,avlShares,curShare,curShareQty):
        if curShareQty <= avlShares[curShare]:
            return True
        return False
    
    # Computes possiblities of the next state
    def generateTree(self):
        currentPlayer = self.admin.acquire.state["players"][0]

        playerTiles = currentPlayer.tiles
        avlHotels = self.admin.banker.remaining_hotels
        avlShares = self.admin.banker.remaining_shares
        avlReplacementTiles = self.admin.banker.remaining_tiles
        hotelsOnBoard = []
        for hotel in self.admin.acquire.state["board"].hotels:
            hotelsOnBoard.append(hotel["hotel"])
        level0  = []
        for tile in playerTiles:
            result = self.admin.place(tile.row,tile.column,False)
            if type(result) == Error:
                meta = {"tile":tile,"place":"NP","hotelsOnBoard":hotelsOnBoard,"hotelsPossible":[],"hotelsRemoved":[]}
            meta = {"tile":tile,"place":"","hotelsOnBoard":hotelsOnBoard,"hotelsPossible":[],"hotelsRemoved":[]}
            if result["type"] == "founding":
                meta["place"] = "founding"
                meta["hotelsPossible"]  = avlHotels
            elif result["type"] == "merging":
                meta["place"] = "merging"
                meta["hotelsRemoved"] += result["acquired"]
                meta["hotelsOnBoard"] = list(frozenset(meta["hotelsOnBoard"]).difference(frozenset(meta["hotelsRemoved"])))
            else:
                meta["place"] = "G/S" 

            level0.append(meta)
        
        
        level2 = avlReplacementTiles
                    
        self.tree = [level0,level2]
        return True

    def groupBy(self,data):
        countDict = defaultdict(int)
        for share in data:
            countDict[share]+=1
        return countDict
            
    # Used by players to traverse the game tree
    def traverse(self,playerReq)->bool:
        # Player req 
        # {PlayerTile, shareList, newAvltile}
        playerTile = Tile(playerReq["playerTile"])
        playerHotel = playerReq["hotel"]
        playerShareReq = self.groupBy(playerReq["requestedShares"])
        if sum(playerShareReq.values()) > 3:
            return False,Error("Cannot buy more than 3 shares at a time!")
        playerNewTileReq = playerReq["requestedNewTile"]

        flg = False
        for item in self.tree[0]:
            if item["tile"] == playerTile:
                
                if item["place"] == "founding":
                    if playerHotel in item["hotelsPossible"]:
                        item["hotelsOnBoard"]+=playerHotel
                    else:
                        return False,Error("Hotel invalid!")
                count = 3
                for share in playerShareReq:
                    if not self.canBuy(self.admin.banker.remaining_shares,share,playerShareReq[share]):
                        return False, Error(f"Cannot buy {playerShareReq[share]} no of shares for {share}")
                
                if playerNewTileReq not in self.tree[1]:
                    return False,Error(f"Cannot replace tile with {playerNewTileReq}")
                flg = True
                break
        
        if flg:
            return True,"Success"
        else:
            return False,Error("tile not found in player tiles")
                

                
                

            
        
