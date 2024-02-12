from abc import ABC, abstractmethod

class StockCertificate:
    def __init__(self, hotel_label, quantity):
        self.hotel_label = hotel_label
        self.quantity = quantity

class Share:
    def __init__(self, hotel_label, price):
        self.hotel_label = hotel_label
        self.price = price

class Player(ABC):
    def __init__(self, name):
        self.name = name
        self.portfolio = [] 

    @abstractmethod
    def make_move(self, game):
        pass

    def buy(self, hotel_label, quantity) -> bool:
        # Logic to buy shares and update the stock portfolio
        pass

    def sell(self, hotel_label, quantity) -> bool:
        # Logic to sell shares and update the stock portfolio
        pass

class HumanPlayer(Player):
    def make_move(self, game):
        # Logic to get move input from a human player
        pass

class AIPlayer(Player):
    def make_move(self, game):
        # Logic to make a move for an AI player
        pass


class AcquireGame:
    def __init__(self):
        # Initialize game state variables
        self.board = None
        self.players = []  # List of Player objects
        self.current_player = None
        self.game_over = False
        self.stock_market = {}  # Dictionary to represent the stock market

    def initialize_game(self, num_players):
        # Initialize the game with the specified number of players
        # Setup initial board, player hands, stock market, etc.
        pass

    def start_game(self):
        # Start the game, set initial conditions, and begin the first turn
        pass

    def is_valid_move(self, move:str) -> bool:
        # Check if the move made by current player is valid
        pass

    def switch_to_next_player(self):
        # Logic to switch to the next player's turn
        pass


    def get_game_state(self) -> dict:
        # Get the current state of the game for external use
        pass

  
