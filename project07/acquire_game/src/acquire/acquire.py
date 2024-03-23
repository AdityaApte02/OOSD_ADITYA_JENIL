from acquire.board import Board
from acquire.tile import Tile
from acquire.error import Error
from acquire.player import HumanPlayer

def printBoard(board):
    print("================================")
    for r in board:
        print(r)


class Acquire:
    def __init__(self):
        self.state = {"board": Board(), "players": []}

    def set_state(self, state, flag=False):
        if state['board'] == {}:
            return False, Error('Board is Empty').to_dict()
        if 'tiles' not in state['board'].keys() or 'hotels' not in state['board'].keys() or 'players' not in state.keys():
            return False, Error('Invalid key found in the request state').to_dict()
        self.state["board"].tiles = state["board"]["tiles"]
        self.state["board"].hotels = state["board"]["hotels"]
        if flag:
            self.state["players"] = []
            players = state["players"]
            for player in players:
                current_player = HumanPlayer(player["player"])
                current_player.cash = player["cash"]
                current_player.shares = player["shares"]
                current_player.tiles = player["tiles"]
                self.state["players"].append(current_player)

    def validate_board(self, board):
        # check if hotel tiles are less than or equal to total tiles
        hotel_tiles = 0
        total_tiles = len(board.tiles)
        valid_hotels = [
            "Imperial",
            "Continental",
            "Tower",
            "Sackson",
            "American",
            "Festival",
            "Worldwide",
        ]
        for hotel in board.hotels:
            for tile in hotel["tiles"]:
                hotel_tiles += 1
        if hotel_tiles > total_tiles:
            return False, Error("Hotel tiles are greater than total tiles").to_dict()

        # check if tiles column is string
        for tile in board.tiles:
            if not isinstance(tile["row"], str):
                return False, Error(f"Tile {tile} row is not a string").to_dict()

        # check if hotel tiles column is string
        for hotel in board.hotels:
            for tile in hotel["tiles"]:
                if not isinstance(tile["row"], str):
                    return False, Error(f"Tile {tile} row is not a string").to_dict()

        # check if tiles are within the board
        for tile in board.tiles:
            if tile["row"] not in "ABCDEFGHI" or int(tile["column"]) not in range(
                1, 13
            ):
                return False, Error(f"Tile {tile} is not within the board").to_dict()

        # check if hotel tiles are within the board
        for hotel in board.hotels:
            for tile in hotel["tiles"]:
                if tile["row"] not in "ABCDEFGHI" or int(tile["column"]) not in range(
                    1, 13
                ):
                    return (
                        False,
                        Error(f"Tile {tile} is not within the board").to_dict(),
                    )

        # check if hotel chain size is greater than or equal to 2
        for hotel in board.hotels:
            if len(hotel["tiles"]) < 2:
                return (
                    False,
                    Error(f"Hotel {hotel} chain size is less than 2").to_dict(),
                )
            # check if hotel label is valid
            if hotel["hotel"] not in valid_hotels:
                return (
                    False,
                    Error(f"Hotel {hotel['hotel']} label is not valid").to_dict(),
                )

        # check if hotel chain size is less than or equal to 41
        for hotel in board.hotels:
            if len(hotel["tiles"]) >= 41:
                return (
                    False,
                    Error(
                        f"Game over! Hotel {hotel} chain size is greater than or equal to 41"
                    ).to_dict(),
                )

        # check if hotel tiles are present in board tiles
        for hotel in board.hotels:
            for tile in hotel["tiles"]:
                if tile not in board.tiles:
                    return (
                        False,
                        Error(f"Tile {tile} is not present in board tiles").to_dict(),
                    )

        # check if hotel chain's tiles are connected
        for hotel in board.hotels:
            # create matrix for hotel tiles, with 1 for hotel tiles and 0 for empty tiles
            hotel_tiles = [[0 for _ in range(12)] for _ in range(9)]
            for tile in hotel["tiles"]:
                row = ord(tile["row"]) - 65
                col = int(tile["column"]) - 1
                hotel_tiles[row][col] = 1

            if not self._are_ones_connected(hotel_tiles):
                return (
                    False,
                    Error(
                        f"Hotel {hotel['hotel']} chain's tiles are not connected"
                    ).to_dict(),
                )

        # check if tiles are unique
        for i in range(len(board.tiles)):
            for j in range(i + 1, len(board.tiles)):
                if board.tiles[i] == board.tiles[j]:
                    return (
                        False,
                        Error(f"Tile {board.tiles[i]} is not unique").to_dict(),
                    )

        # check if hotel tiles are unique
        for hotel in board.hotels:
            for i in range(len(hotel["tiles"])):
                for j in range(i + 1, len(hotel["tiles"])):
                    if hotel["tiles"][i] == hotel["tiles"][j]:
                        return (
                            False,
                            Error(f"Tile {hotel['tiles'][i]} is not unique").to_dict(),
                        )

        return True, "Board is valid"

    def validate_state(self, state):
        board_instance = state["board"]
        is_valid, message = self.validate_board(board_instance)
        if is_valid:
             # Check players list should not be empty
            players = state["players"]
            if len(players) == 0:
                return False, Error("The players list is empty").to_dict()

            # Check players list should not be more than 6
            if len(players) > 6:
                return False, Error("The players list is more than 6").to_dict()
            
            curr_player_cash = state["players"][0].cash
            # Check cash should be integer
            if not isinstance(curr_player_cash, int):
                return (
                    False,
                    Error("The current player cash is not an integer").to_dict(),
                )

            # Check cash should not be negative
            if curr_player_cash < 0:
                return False, Error("The current player has negative cash").to_dict()
            
            # Check each player should have 6 tiles
            for player in players:
                if len(player.tiles) > 6:
                    return False, Error(f"Player {player.name} has more than 6 tiles").to_dict()

            # Check players name should be string and unique
            players_name = []
            for player in players:
                if not isinstance(player.name, str):
                    return False, Error("The player name is not a string").to_dict()
                players_name.append(player.name)
            if len(players_name) != len(set(players_name)):
                return False, Error("The players name are not unique").to_dict()

            curr_player_shares = players[0].shares
            for shares in curr_player_shares:
                # Check if shares count is integer
                if not isinstance(shares["count"], int):
                    return (
                        False,
                        Error(
                            "The current player shares count is not an integer"
                        ).to_dict(),
                    )
                # Curr_player_shares should be less than 26
                if shares["count"] >= 26:
                    return (
                        False,
                        Error(f'The current player already has 25 shares of {shares["share"]}').to_dict(),
                    )
                # Check if shares label is valid
                if shares["share"] not in [
                    "Imperial",
                    "Continental",
                    "Tower",
                    "Luxor",
                    "American",
                    "Festival",
                    "Worldwide",
                ]:
                    return (
                        False,
                        Error(
                            f"The current player shares label {shares['share']} is not valid"
                        ).to_dict(),
                    )

            # Check if players tiles are all unique
            curr_player_tiles = state["players"][0].tiles
            for i in range(len(curr_player_tiles)):
                for j in range(i + 1, len(curr_player_tiles)):
                    if curr_player_tiles[i] == curr_player_tiles[j]:
                        return (
                            False,
                            Error(
                                f"Tile {curr_player_tiles[i]} is not unique for current player"
                            ).to_dict(),
                        )

            # Check if players tiles already in the board tiles or boards hotel tiles
            players_tiles_dict = state["players"][0].tiles
            players_tiles = []
            for tile in players_tiles_dict:
                players_tiles.append(tile["row"] + str(tile["column"]))

            board_tiles = board_instance.tiles
            board_hotel = board_instance.hotels

            for tile in players_tiles_dict:
                if tile in board_tiles:
                    return (
                        False,
                        Error("The player already has a tile in the board").to_dict(),
                    )
                for hotel in board_hotel:
                    if tile in hotel["tiles"]:
                        return (
                            False,
                            Error(
                                "The player already has a tile in the hotel"
                            ).to_dict(),
                        )

            return True, "State is valid"

        else:
            return False, message

    def _count_connected_ones(self, matrix, i, j, visited):
        if (
            i < 0
            or i >= len(matrix)
            or j < 0
            or j >= len(matrix[0])
            or matrix[i][j] == 0
            or visited[i][j]
        ):
            return 0

        visited[i][j] = True
        return (
            1
            + self._count_connected_ones(matrix, i + 1, j, visited)
            + self._count_connected_ones(matrix, i - 1, j, visited)
            + self._count_connected_ones(matrix, i, j + 1, visited)
            + self._count_connected_ones(matrix, i, j - 1, visited)
        )

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

    def handle_query(self, request, boardMatrix):
        if boardMatrix[ord(request["row"]) - 65][int(request["column"]) - 1] != "0":
            return False, Error("A tile already exists at the desired location").to_dict()
        res = self.handle_singleton(request, boardMatrix)
        if type(res) == dict and "singleton" in res:
            return res
        else:
            merging_res = self.handle_merging(request, boardMatrix)
            if type(merging_res) == dict and "acquirer" in merging_res:      
                return merging_res
            else:
                growing_resonse = self.handle_growing(request, boardMatrix)
                if type(growing_resonse) == dict and "growing" in growing_resonse: 
                    return growing_resonse
                else:
                    if "hotel" in request.keys():
                        founding_response = self.handle_founding(request, boardMatrix)
                        if type(founding_response) and "founding" in founding_response:
                            return founding_response
        return Error("Invalid Board!")

    def handle_singleton(self, request, boardMatrix):
        printBoard(boardMatrix)
        row = ord(request["row"]) - 65
        col = int(request["column"]) - 1
        singleTonFlag = True
        if boardMatrix[row][col] != "0":
            singleTonFlag = False
            return Error("A Tile cannot be placed at the desired location")
        
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        if len(request["board"].hotels) < 7:
            for r, c in offsets:
                if (
                    row + r >= 0
                    and row + r < len(boardMatrix)
                    and col + c >= 0
                    and col + c < len(boardMatrix[0])
                ):
                    if boardMatrix[row + r][col + c] != "0":
                        singleTonFlag = False
                        break
        else:
            for r, c in offsets:
                if (
                    row + r >= 0
                    and row + r < len(boardMatrix)
                    and col + c >= 0
                    and col + c < len(boardMatrix[0])
                ):
                    if len(boardMatrix[row + r][col + c]) > 1:
                        singleTonFlag = False
                        break
        if singleTonFlag:
            boardMatrix[row][col] = "1"
            return {"singleton": None}
        else:
            return Error("Other Operation")

    def handle_growing(self, request, boardMatrix):
        row = ord(request["row"]) - 65
        col = int(request["column"]) - 1
        if boardMatrix[row][col] != "0":
            return Error("A Tile cannot be placed at the desired location")
        visited = set()
        growing_tiles = []
        hotel = ""
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for r, c in offsets:
            if (
                row + r >= 0
                and row + r < len(boardMatrix)
                and col + c >= 0
                and col + c < len(boardMatrix[0])
            ):
                if len(boardMatrix[row + r][col + c]) > 1:
                    if boardMatrix[row + r][col + c] != hotel and hotel != "":
                        return Error("A merger would take place")
                    hotel = boardMatrix[row + r][col + c]
        def dfs(x, y):
            visited.add((x, y))
            growing_tiles.append(Tile(x, y))
            for r, c in offsets:
                if (
                    x + r >= 0
                    and x + r < len(boardMatrix)
                    and y + c >= 0
                    and y + c < len(boardMatrix[0])
                    and boardMatrix[x + r][y + c] == "1"
                    and (x + r, y + c) not in visited
                ):
                    dfs(x + r, y + c)

        dfs(row, col)
        for tile in growing_tiles:
            if hotel != "":
                boardMatrix[int(tile.row)][int(tile.column)] = hotel
            else:
                return Error("No hotel found")
        return {"growing": hotel}

    def handle_founding(self, request, boardMatrix):
        row = ord(request["row"]) - 65
        col = int(request["column"]) - 1
        num_of_hotels_placed = len(request["board"].hotels)
        if num_of_hotels_placed >= 7:
            return Error("No Hotel chains remaining!")
        if boardMatrix[row][col] != "0":
            return Error("A Tile cannot be placed at the desired location")

        founding_tiles = []
        first_other_hotel_found = ""
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        hotel_label = request["hotel"]
        for hotel in request["board"].hotels:
            if hotel["hotel"] == hotel_label:
                return Error("A hotel with that label already exists")
        for r, c in offsets:
            if (
                row + r >= 0
                and row + r < len(boardMatrix)
                and col + c >= 0
                and col + c < len(boardMatrix[0])
            ):
                if (
                    len(boardMatrix[row + r][col + c]) > 1
                    and boardMatrix[row + r][col + c] != first_other_hotel_found
                    and first_other_hotel_found != ""
                ):
                    return Error("There should be a merger here!!")
                elif (
                    boardMatrix[row + r][col + c] != hotel_label
                    and len(boardMatrix[row + r][col + c]) > 1
                ):
                    first_other_hotel_found = boardMatrix[row + r][col + c]
        visited = set()

        def dfs(x, y):
            visited.add((x, y))
            founding_tiles.append(Tile(x, y))
            for r, c in offsets:
                if (
                    x + r >= 0
                    and x + r < len(boardMatrix)
                    and y + c >= 0
                    and y + c < len(boardMatrix[0])
                    and boardMatrix[x + r][y + c] == "1"
                    and (x + r, y + c) not in visited
                ):
                    dfs(x + r, y + c)

        dfs(row, col)
        if founding_tiles == []:
            return Error("A chain cannot be formed here")
        founding_tiles.append(Tile(row, col))
        for tile in founding_tiles:
            boardMatrix[int(tile.row)][int(tile.column)] = hotel_label

        # Call the update handler and convert to board object form
        return {"founding": hotel_label}

    def handle_merging(self, request, boardMatrix):
        row = ord(request["row"]) - 65
        col = int(request["column"]) - 1
        merging_flag = True
        if boardMatrix[row][col] != "0":
            merging_flag = False
            return Error("A Tile cannot be placed at the desired location")
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        hotels = request["board"].hotels

        max_length = 0
        acquirer = ""
        acquired_hotels = {}
        acquired = []
        for r, c in offsets:
            new_row = row + r
            new_col = col + c
            if (
                new_row >= 0
                and new_row < len(boardMatrix)
                and new_col >= 0
                and new_col < len(boardMatrix[0])
            ):
                if (
                    boardMatrix[new_row][new_col] != "0"
                    and boardMatrix[new_row][new_col] != "1"
                ):
                    label = boardMatrix[new_row][new_col]
                    for hotel in hotels:
                        if hotel["hotel"] == label and label not in acquired_hotels:
                            len_of_hotel = len(hotel["tiles"])
                            acquired_hotels[label] = len_of_hotel
                            if len_of_hotel > max_length:
                                max_length = len_of_hotel
                                acquirer = label
        if acquirer == "":
            merging_flag = False
            return Error("No hotels to merge")
        elif len(acquired_hotels) == 1:
            merging_flag = False
            return Error("Only one hotel to merge")
        else:
            len_of_acquirer = acquired_hotels[acquirer]
            if len_of_acquirer >= 11:
                return Error("Hotel has chain length of atleast 11")
            del acquired_hotels[acquirer]

            for hotel_name, len_of_hotel in acquired_hotels.items():
                if len_of_hotel >= 11:
                    return Error("Hotel has chain length of atleast 11")
                else:
                    if len_of_acquirer + len_of_hotel <= 41:
                        acquired.append(hotel_name)
            if len(acquired) == 0:
                merging_flag = False
                return Error("Only one hotel to merge")
            tiles_acquired = []
            for hotel in hotels:
                if hotel["hotel"] in acquired:
                    tiles_acquired.extend(hotel["tiles"])
                elif hotel["hotel"] == acquirer:
                    tiles_acquired.extend(hotel["tiles"])
            for tile in tiles_acquired:
                row_index = ord(tile["row"]) - 65
                col_index = int(tile["column"]) - 1
                boardMatrix[row_index][col_index] = acquirer

            boardMatrix[row][col] = acquirer
            
        if merging_flag:
            return {"acquirer": acquirer, "acquired": acquired, "acquired_hotels_dict" : acquired_hotels}
        else:
            return Error("Other Operation")
