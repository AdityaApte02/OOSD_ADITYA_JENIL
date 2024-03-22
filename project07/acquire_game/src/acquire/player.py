from abc import ABC, abstractmethod
class Player(ABC):
    def __init__(self, name, cash=6000, tiles=[], shares=[]):
        self.name = name
        self.cash = cash
        self.tiles = tiles
        self.shares = shares
        

class HumanPlayer(Player):
    def __init__(self, name, cash, tiles, shares):
        super().__init__(name, cash, tiles, shares)


class AIPlayer(Player):
    def __init__(self, name, cash, tiles, shares):
        super().__init__(name,  cash, tiles, shares)

