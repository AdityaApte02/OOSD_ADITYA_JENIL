from tile import Tile
from hotel import Hotel
from tabulate import tabulate
class Board:
    def __init__(self):
        self.tiles = []
        self.hotels = []

    def create_board(self):
        board = [['0' for _ in range(12)] for _ in range(9)]
        # Place tiles and hotels on the board
        for tile in self.tiles:
            row = ord(tile["row"]) - 65
            col = int(tile["column"]) - 1
            board[row][col] = "1"

        for hotel in self.hotels:
            for tile in hotel["tiles"]:
                row = ord(tile["row"]) - 65
                col = int(tile["column"]) - 1
                board[row][col] = hotel['hotel']
        
        for hotel in self.hotels:
            hotel_label = hotel['hotel']
            for tile in hotel['tiles']:
                row = ord(tile["row"]) - 65
                col = int(tile["column"]) - 1
                board[row][col] = hotel_label
            
        # todo: validate adjacent 1s
        return board
    
    def place_tile(self, row, column):
        pass
    
    @staticmethod
    def print_board(board):
        print(tabulate(board,tablefmt="grid"))
