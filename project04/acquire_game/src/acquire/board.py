from tile import Tile
from hotel import Hotel

class Board:
    def __init__(self, board):
        self.tiles = board['tiles']
        self.hotels = board['hotels']

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
                if (row-1 >=0 and (board[row-1][col] != hotel_label and board[row-1][col] != '0' and board[row-1][col] != '1')) :
                    raise Exception("Invalid hotel placement")
                elif (row+1 < 9 and (board[row+1][col] != hotel_label and board[row+1][col] != '0' and board[row+1][col] != '1')) :
                    raise Exception("Invalid hotel placement")
                elif  (col-1 >=0 and (board[row][col-1] != hotel_label and board[row][col-1] != '0' and board[row][col-1] != '1')) :
                    raise Exception("Invalid hotel placement")
                elif (col+1 < 12 and (board[row][col+1] != hotel_label and board[row][col+1] != '0' and board[row][col+1] != '1')):
                    raise Exception("Invalid hotel placement")
                else:
                    board[row][col] = hotel_label
            
        return board
    
    def place_tile(self, row, column):
        pass

    def print_board(self):
        pass
