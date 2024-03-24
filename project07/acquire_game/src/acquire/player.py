from abc import ABC, abstractmethod
class Player(ABC):
    def __init__(self, name, cash=6000):
        self.name = name
        self.cash = cash
        self.tiles = []
        self.shares = []
        

class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

class AIPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

