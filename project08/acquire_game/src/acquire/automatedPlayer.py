import sys
from tile import Tile
from strategy import OrderedStrategy
from strategy import RandomStrategy
from strategy import LargestAlpha
from strategy import SmallestAnti
import random


class AutomatedPlayer:
    def __init__(self, name, strategy):
        if strategy == "ordered":
            self.strategy = OrderedStrategy("ordered")
        elif strategy == "random":
            self.strategy = RandomStrategy("random")
        elif strategy =="largest-alpha":
            self.strategy = LargestAlpha("largest-alpha")
        elif strategy == "smallest-anti":
            self.strategy = SmallestAnti("smallest-anti")
        self.name = name


    def getName(self):
        return self.name
    
    def playTile(self, admin):
        player = admin.acquire.state["players"][0]
        return self.strategy.play(player, admin)
        
    def buyShares(self, admin):
        return self.strategy.buy(admin)


if __name__ == "__main__":
    if sys.argv[1] == "1":
        strategy = "ordered"
    else:
        strategy = "random"
    player = AutomatedPlayer(strategy, ["Jenil", "Aditya"])
    
