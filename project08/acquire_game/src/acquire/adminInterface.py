from abc import ABC, abstractmethod

class AcquireGame(ABC):
    @abstractmethod
    def __init__(self):
        # Initialize game state variables
       self.acquire = None   #Instance of the acquire game
       self.banker = None    # Instance of the banker class


    @abstractmethod
    def setUp(self, num_players):
        # Initialize the game with the specified number of players
        # Setup initial board, player hands, stock market, etc.
        pass


    @abstractmethod
    def buy(self, request)-> dict:
        # Buys the share of the requested hotel chain
        pass

    @abstractmethod
    def done(self, request) -> dict:
        # Switch to the next player
        pass


    @abstractmethod
    def place(self, request) -> dict:
        # checks if player can place the tile on requested tileand returns resulting output state
        pass
