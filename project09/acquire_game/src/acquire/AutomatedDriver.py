import sys
from automatedAdmin import Admin
from automatedPlayer import AutomatedPlayer
from tile import Tile
import random
from gameTree import GameTree

class AutomatedDriver():
    def __init__(self, playersList):
        self.admin = Admin()
        playerNames = [player.name for player in playersList]
        self.admin.setUp({"request":"setup", "players":playerNames})
        self.players = playersList
        self.gameTree = GameTree(self.admin)
        
        
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
        
    def play(self):
        player = self.admin.acquire.state["players"][0]
        automatedPlayer = self.getPlayer(player.name)
        automatedPlayer.playTile(self.admin)
        
    
    def buy(self):
        player = self.admin.acquire.state["players"][0]
        automatedPlayer = self.getPlayer(player.name)
        automatedPlayer.buyShares(self.admin)
        
        
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
        player2 = AutomatedPlayer("Aditya", "ordered")
        player3 = AutomatedPlayer("Police", "ordered")
        player4 = AutomatedPlayer("Dab Dab", "ordered")
        
        
        playerList = [player1, player2, player3, player4]
        
        driver = AutomatedDriver(playerList)
        flag = True
        while flag:
            response = driver.gameOver()
            if response[0]:
                flag = False
            else:
                driver.play()
                driver.buy()

        print(f'{driver.computeWinner().name} won the Game')
        print("Game Over!!!")