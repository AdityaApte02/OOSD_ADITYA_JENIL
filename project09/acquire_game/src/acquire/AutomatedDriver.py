import sys
from automatedAdmin import Admin
from automatedPlayer import AutomatedPlayer
from tile import Tile
import random
from gameTree import GameTree
import time
from tabulate import tabulate
class AutomatedDriver():
    def __init__(self, playersList):
        self.admin = Admin()
        playerNames = [player.name for player in playersList]
        self.admin.setUp({"request":"setup", "players":playerNames})
        self.players = playersList
        
        
    def getPlayer(self, name):
        for player in self.players:
            if player.name == name:
                return player
            
        return None
        
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
        

    def place(self,perform=True):
        player = self.admin.acquire.state["players"][0]
        automatedPlayer = self.getPlayer(player.name)
        return automatedPlayer.playTile(self.admin, perform)
        
    
    def buy(self,perform):
        player = self.admin.acquire.state["players"][0]
        automatedPlayer = self.getPlayer(player.name)
        return automatedPlayer.buyShares(self.admin, perform)
        
    def treePlay(self,gameTree:GameTree):
        res1 = self.place(False)
        shares = self.buy(False)
        if len(self.admin.banker.remaining_tiles) > 0:
            val = self.admin.banker.remaining_tiles[0] 
        else:
            val = None
        res = {"requestedShares":shares,"requestedNewTile":val}
        if type(res1) != bool:
            res["playerTile"] = res1["Tile"]
            res["hotel"] = res1["hotel"]
        status,_ = gameTree.traverse(self.admin,res)
        if status:
            self.place(True)
            self.buy(True)
    
        
        
    def getHotel(self, hotels, name):
        for hotel in hotels:
            if hotel["hotel"] == name:
                return hotel
        return None
    
    
    def computeWinner(self):
        maxCash = -1
        winner = ''
        for player in self.admin.acquire.state["players"]:
            for share in player.shares:
                hotel_name = share["share"]
                count= share["count"]
                hotel = self.getHotel(self.admin.acquire.state["board"].hotels, hotel_name)
                if hotel == None:
                    continue
                num_of_tiles = len(hotel["tiles"])
                share_price = -1
                for lower_range, higher_range, price in self.admin.banker.stock_prices[hotel_name]:
                    if num_of_tiles >= lower_range and num_of_tiles <= higher_range:
                        share_price = price
                player.cash = player.cash + (share_price * count)
            if player.cash >= maxCash:
                winner = player
                maxCash = player.cash
        return winner
                    
  
    
if __name__ =="__main__":
    for i in range(100):
        player1 = AutomatedPlayer("Jenil", "ordered")
        player2 = AutomatedPlayer("Aditya", "random")
        player3 = AutomatedPlayer("Pranav", "smallest-anti")
        player4 = AutomatedPlayer("Krishna", "largest-alpha")
        
        
        playerList = [player1, player2, player3, player4]
        
        driver = AutomatedDriver(playerList)
        flag = True
        while flag:
            response = driver.gameOver()
            if response[0]:
                flag = False
            else:
                driver.admin.play()
                driver.treePlay(driver.admin.gameTree)

        print(f'{driver.computeWinner().name} won the Game')
        print("Game Over!!!")
        break