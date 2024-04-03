from board import Board
from tile import Tile
from hotel import Hotel
from error import Error


def printBoard(board):
    print('================================')
    for r in board:
        print(r)

class Acquire:
    def __init__(self, request):
        self.board = Board(request['board'])

    # if request(not inspect) is successful, return res+message
        
    def get_board(self):
        return self.board
    
    def validate_board(self, board):
        # check if hotel tiles are less than or equal to total tiles
        hotel_tiles = 0
        total_tiles = len(board.tiles)
        for hotel in board.hotels:
            for tile in hotel["tiles"]:
                hotel_tiles += 1
        if hotel_tiles > total_tiles:
            return False, Error("Hotel tiles are greater than total tiles").to_dict()
        
        # check if tiles are within the board
        for tile in board.tiles:
            if tile["row"] not in "ABCDEFGHI" or int(tile["column"]) not in range(1, 13):
                return False, Error(f"Tile {tile} is not within the board").to_dict()
            
        # check if hotel tiles are within the board
        for hotel in board.hotels:
            for tile in hotel["tiles"]:
                if tile["row"] not in "ABCDEFGHI" or int(tile["column"]) not in range(1, 13):
                    return False, Error(f"Tile {tile} is not within the board").to_dict()
        
        # check if hotel chain size is greater than or equal to 2
        for hotel in board.hotels:
            if len(hotel["tiles"]) < 2:
                return False, Error(f"Hotel {hotel} chain size is less than 2").to_dict()
                
        # check if hotel chain size is less than or equal to 41
        for hotel in board.hotels:
            if len(hotel["tiles"]) >= 41:
                return False, Error(f"Game over! Hotel {hotel} chain size is greater than or equal to 41").to_dict()
            
        # check if hotel tiles are present in board tiles
        for hotel in board.hotels:
            for tile in hotel["tiles"]:
                if tile not in board.tiles:
                    return False, Error(f"Tile {tile} is not present in board tiles").to_dict()

        # check if hotel chain's tiles are connected
        for hotel in board.hotels:
            # create matrix for hotel tiles, with 1 for hotel tiles and 0 for empty tiles
            hotel_tiles = [[0 for _ in range(12)] for _ in range(9)]
            for tile in hotel["tiles"]:
                row = ord(tile["row"]) - 65
                col = int(tile["column"]) - 1
                hotel_tiles[row][col] = 1
            
            if not self._are_ones_connected(hotel_tiles):
                return False, Error(f"Hotel {hotel['hotel']} chain's tiles are not connected").to_dict()


        # check if tiles are unique
        for i in range(len(board.tiles)):
            for j in range(i+1, len(board.tiles)):
                if board.tiles[i] == board.tiles[j]:
                    return False, Error(f"Tile {board.tiles[i]} is not unique").to_dict()

        # check if hotel tiles are unique
        for hotel in board.hotels:
            for i in range(len(hotel["tiles"])):
                for j in range(i+1, len(hotel["tiles"])):
                    if hotel["tiles"][i] == hotel["tiles"][j]:
                        return False, Error(f"Tile {hotel['tiles'][i]} is not unique").to_dict()
                    
        return True, "Board is valid"

    def _count_connected_ones(self, matrix, i, j, visited):
        if i < 0 or i >= len(matrix) or j < 0 or j >= len(matrix[0]) or matrix[i][j] == 0 or visited[i][j]:
            return 0

        visited[i][j] = True
        return 1 + self._count_connected_ones(matrix, i + 1, j, visited) + self._count_connected_ones(matrix, i - 1, j, visited) + self._count_connected_ones(matrix, i, j + 1, visited) + self._count_connected_ones(matrix, i, j - 1, visited)


    def _are_ones_connected(self, matrix):
        total_ones = sum(row.count(1) for row in matrix)
        visited = [[False for _ in range(len(matrix[0]))] for _ in range(len(matrix))]

        # Find the first "1" to start flood fill
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 1:
                    connected_count = self._count_connected_ones(matrix, i, j, visited)
                    return total_ones == connected_count

        return True

    def handle_request(self, request, boardMatrix):
        if boardMatrix[ord(request["row"])-65][int(request["column"])-1] != '0':
            return Error('Tile already placed at the desired location!').to_dict()
        if request["request"] == "query":
            return self.handle_query(request, boardMatrix)
        elif request["request"] == "singleton":
            return self.handle_singleton(request, boardMatrix)
        elif request["request"] == "growing":
            return self.handle_growing(request, boardMatrix)
        elif request["request"] == "founding":
            return self.handle_founding(request, boardMatrix)
        elif request["request"] == "merging":
            return self.handle_merging(request, boardMatrix)
        else:
            return Error('Invalid request!').to_dict()

    def handle_query(self, request, boardMatrix):
        res = self.handle_singleton(request, boardMatrix)
        if res == 'singleton':
            return res
        
        else:
            res = self.handle_merging(request, boardMatrix)
            if "acquirer" in res.keys():
                return res
            
            else:
                growing_resonse = self.handle_growing(request, boardMatrix)
                if 'growing' in growing_resonse.keys():
                    return growing_resonse
                
                else:
                    founding_response = self.handle_founding(request, boardMatrix)
                    if founding_response == 'founding':
                        return founding_response
                    

        return Error('Invalid Board!').to_dict()   

    def handle_singleton(self, request, boardMatrix):
        row = ord(request['row']) - 65
        col = int(request['column']) - 1
        singleTonFlag  = True
        if boardMatrix[row][col] != '0':
            singleTonFlag = False
            return {
                "impossible": 'A Tile cannot be placed at the desired location'
            }
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        if len(request['board']['hotels']) < 7:
            for r,c in offsets:
                if row+r >= 0 and row+r < len(boardMatrix) and col+c >= 0 and col+c < len(boardMatrix[0]):
                    if boardMatrix[row+r][col+c] != '0':
                        singleTonFlag = False
                        break
        else:
            for r,c in offsets:
                if row+r >= 0 and row+r < len(boardMatrix) and col+c >= 0 and col+c < len(boardMatrix[0]):
                    if len(boardMatrix[row+r][col+c]) > 1:
                        singleTonFlag = False
                        break

        if singleTonFlag:
            boardMatrix[row][col] = '1'
            printBoard(boardMatrix)
            return "singleton"
        
        else:
            return {
                "impossible": 'Other Operation'
            }


    def handle_growing(self, request, boardMatrix):
        row = ord(request['row']) - 65
        col = int(request['column']) - 1
        if boardMatrix[row][col] != '0':
            return {
                "impossible": 'A Tile cannot be placed at the desired location'
            }
        visited = set()
        growing_tiles  =[]
        hotel = ''
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for r,c in offsets:
            if row+r >= 0 and row+r < len(boardMatrix) and col+c >= 0 and col+c < len(boardMatrix[0]):
                if len(boardMatrix[row+r][col+c]) > 1:
                    if boardMatrix[row+r][col+c] != hotel and hotel != '':
                        return {
                            'impossible':'A merger would take place'
                        }
                    hotel = boardMatrix[row+r][col+c]
        def dfs(x, y):
            visited.add((x,y))
            growing_tiles.append(Tile(x,y))
            for r,c in offsets:
                if x+r >= 0 and x+r < len(boardMatrix) and y+c >= 0 and y+c < len(boardMatrix[0]) and boardMatrix[x+r][y+c] == '1' and (x+r, y+c) not in visited:
                    dfs(x+r, y+c)
        dfs(row, col)
        for tile in growing_tiles:
            if hotel != '':
                boardMatrix[int(tile.row)][int(tile.column)] = hotel

            else:
                return Error('No hotel found').to_dict()
        printBoard(boardMatrix)
        return {"growing":hotel}


    def handle_founding(self, request, boardMatrix):
        row = ord(request['row']) - 65
        col = int(request['column']) - 1
        num_of_hotels_placed = len(request['board']['hotels'])
        if num_of_hotels_placed >= 7:
            return Error('No Hotel chains remaining!').to_dict()
        if boardMatrix[row][col] != '0':
            return {
                "impossible": 'A Tile cannot be placed at the desired location'
            }
        founding_tiles = []
        first_other_hotel_found = ''
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        if request["request"] == "founding":
            hotel_label = request['label']
            for hotel in request['board']['hotels']:
                if hotel['hotel'] == hotel_label:
                    return Error('A hotel with that label already exists').to_dict()
            for r,c in offsets:
                if row+r >= 0 and row+r < len(boardMatrix) and col+c >= 0 and col+c < len(boardMatrix[0]):
                    if len(boardMatrix[row+r][col+c]) > 1 and boardMatrix[row+r][col+c] != first_other_hotel_found and first_other_hotel_found != '':
                        return {
                            'impossible':'There should be a merger here!!'
                        }
                    elif boardMatrix[row+r][col+c] != hotel_label and len(boardMatrix[row+r][col+c]) > 1:
                        first_other_hotel_found = boardMatrix[row+r][col+c]
            visited  = set()
            def dfs(x, y):
                visited.add((x,y))
                founding_tiles.append(Tile(x,y))
                for r,c in offsets:
                    if x+r >= 0 and x+r < len(boardMatrix) and y+c >= 0 and y+c < len(boardMatrix[0]) and boardMatrix[x+r][y+c] == '1' and (x+r, y+c) not in visited:
                        dfs(x+r, y+c)
            dfs(row, col)
        else:
            for r,c in offsets:
                if row+r >= 0 and row+r < len(boardMatrix) and col+c >= 0 and col+c < len(boardMatrix[0]):
                    if boardMatrix[row+r][col+c] == '1':
                        founding_tiles.append(Tile(row+r, col+c))
        if founding_tiles == []:
            return {
                "impossible": 'A chain cannot be formed here'
            }
        if request["request"] == "founding":
            founding_tiles.append(Tile(row, col))
            for tile in founding_tiles:
                boardMatrix[int(tile.row)][int(tile.column)] = hotel_label
        printBoard(boardMatrix)
        return "founding"
                    

    def handle_merging(self, request, boardMatrix):
        row = ord(request['row']) - 65
        col = int(request['column']) - 1
        merging_flag  = True
        if request["request"] == "merging" and (request["label"] == "" or request["label"] is None):
            return Error("Hotel label should be provided.").to_dict()
        if boardMatrix[row][col] != '0':
            merging_flag = False
            return {
                "impossible": 'A Tile cannot be placed at the desired location'
            }
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        hotels = request['board']['hotels']
        
        max_length = 0
        acquirer = ""
        acquired_hotels = {}
        acquired = []
        for r,c in offsets:
            new_row = row+r
            new_col = col+c
            if new_row >= 0 and new_row < len(boardMatrix) and new_col >= 0 and new_col < len(boardMatrix[0]):
                if boardMatrix[new_row][new_col] != '0' and boardMatrix[new_row][new_col] != '1':
                    label = boardMatrix[new_row][new_col]
                    for hotel in hotels:
                        if hotel['hotel'] == label and label not in acquired_hotels:
                            len_of_hotel = len(hotel['tiles'])
                            acquired_hotels[label] = len_of_hotel
                            if len_of_hotel > max_length:
                                max_length = len_of_hotel
                                acquirer = label
        
        if acquirer == "":
            merging_flag = False
            return {
                "impossible": 'No hotels to merge'
            }
        elif len(acquired_hotels) == 1:
            merging_flag = False
            return {
                "impossible": 'Only one hotel to merge'
            }
        else:
            len_of_acquirer = acquired_hotels[acquirer]
            if len_of_acquirer >= 11:
                    return {
                    "impossible": 'Hotel have chain length of atleast 11'
                    }
            del acquired_hotels[acquirer]

            for hotel_name, len_of_hotel in acquired_hotels.items():
                if len_of_hotel >= 11:
                    return {
                    "impossible": 'Hotel have chain length of atleast 11'
                    }
                else:
                    if len_of_acquirer + len_of_hotel <= 41:
                        acquired.append(hotel_name)

            if len(acquired) == 0:
                merging_flag = False
                return {
                "impossible": 'Only one hotel to merge'
                }
                    
            if request["request"] == "merging":

                if request["label"] != acquirer:
                    if request["label"] in acquired:
                        len_of_hotel_label = acquired_hotels[request["label"]]
                        if len_of_hotel_label == len_of_acquirer:
                            acquired.append(acquirer)
                            acquired.remove(request["label"])
                            acquirer = request["label"]
                        else:
                            return {
                            "impossible": f'The {request["label"]}  hotel cannot be the acquirer'
                            }
                    else:
                        return {
                        "impossible": f'The {request["label"]}  hotel cannot be the acquirer'
                        }
                
                tiles_acquired = []
                for hotel in hotels:
                    if hotel['hotel'] in acquired:
                        tiles_acquired.extend(hotel['tiles'])  
                    elif hotel['hotel'] == acquirer:
                        tiles_acquired.extend(hotel['tiles'])

                for tile in tiles_acquired:
                    row_index = ord(tile["row"]) - 65
                    col_index = int(tile["column"]) - 1
                    boardMatrix[row_index][col_index] = acquirer
                
                boardMatrix[row][col] = acquirer

                tiles_acquired = []
                for hotel in hotels:
                    if hotel['hotel'] in acquired:
                        tiles_acquired.extend(hotel['tiles'])  

                for hotel in hotels:
                    if hotel['hotel'] == acquirer:            
                        hotel['tiles'].extend(tiles_acquired)
                        break 

                self.board.hotels = [hotel for hotel in self.board.hotels if hotel['hotel'] not in acquired]

                # print(self.board.hotels)
                printBoard(boardMatrix)


        
        if merging_flag:
            return { "acquirer"   : acquirer, "acquired" : acquired }
                    
        else:
            return {
                "impossible": 'Other Operation'
            }

