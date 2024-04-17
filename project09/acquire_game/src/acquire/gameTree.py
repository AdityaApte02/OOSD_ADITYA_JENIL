from tile import Tile
from error import Error
from collections import defaultdict
from tqdm import tqdm
class GameTree():
    def __init__(self) -> None:
        self.tree = None

    def canBuy(self,avlShares,curShare,curShareQty):
        if curShareQty <= avlShares[curShare]:
            return True
        return False

    def groupBy(self,data):
        countDict = defaultdict(int)
        for share in data:
            countDict[share]+=1
        return countDict
    
    # Computes possiblities of the next state
    def generateTree(self,admin):
        currentPlayer = admin.acquire.state["players"][0]
        playerTiles = currentPlayer.tiles
        avlHotels = admin.banker.remaining_hotels
        avlShares = admin.banker.remaining_shares
        avlReplacementTiles = admin.banker.remaining_tiles
        hotelsOnBoard = []
        for hotel in admin.acquire.state["board"].hotels:
            hotelsOnBoard.append(hotel["hotel"])
        level0  = []
        for tile in playerTiles:
            result = admin.place(tile["row"],tile["column"],False)
            print("result",result)
            if result[0] == False:
                meta = {"tile":tile,"place":"NP","hotelsOnBoard":hotelsOnBoard,"hotelsPossible":[],"hotelsRemoved":[]}
            else:
                result = result[1]["response"]
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

            
    def traverse(self,admin,playerReq)->bool:
        if "playerTile" not in playerReq:
            
            return True,"Success"
        # print("playerReq",playerReq)
        playerTile = playerReq["playerTile"]
        playerHotel = playerReq["hotel"]
        playerShareReq = self.groupBy(playerReq["requestedShares"])
        if sum(playerShareReq.values()) > 3:
            return False,Error("Cannot buy more than 3 shares at a time!")
        if playerReq["requestedNewTile"] is not None:
            playerNewTileReq = playerReq["requestedNewTile"]

        flg = False
        for item in self.tree[0]:
            if item["tile"]["row"] == playerTile.row and item["tile"]["column"] == playerTile.column:
                if item["place"] == "founding":
                    if playerHotel in item["hotelsPossible"]:
                        item["hotelsOnBoard"]+=playerHotel
                    else:
                        return False,Error("Hotel invalid!")
                count = 3
                for share in playerShareReq:
                    if not self.canBuy(admin.banker.remaining_shares,share,playerShareReq[share]):
                        return False, Error(f"Cannot buy {playerShareReq[share]} no of shares for {share}")
                if self.tree[1] != []:
                    if playerNewTileReq not in self.tree[1]:
                        return False,Error(f"Cannot replace tile with {playerNewTileReq}")
                flg = True
                break
        
        if flg:
            return True,"Success"
        else:
            return False,Error("tile not found in player tiles")
                

                
                

            
        
