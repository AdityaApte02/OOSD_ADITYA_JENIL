import sys
from adminInterface import AcquireGame
from acquire import Acquire
from banker import Banker
from error import Error
from player import HumanPlayer
import utils as utils
from tile import Tile
from board import Board
from tabulate import tabulate
import traceback
import random
from gameTree import GameTree

class Admin(AcquireGame):
    def __init__(self):
        super().__init__()
        self.banker = Banker()
        self.acquire = Acquire()
        self.gameTree = GameTree()

    def setUp(self, request):
        playerList = request["players"]
        if len(playerList) < 1 or len(playerList) > 6:
            return False, Error("Number of players should be between 1 to 6").to_dict()

        for player in playerList:
            # player name should be less than 20 characters
            if len(player) > 20:
                return False, Error("Player name should be less than 20 characters").to_dict()
            # player name should be unique
            if playerList.count(player) > 1:
                return False, Error("Player names should be unique").to_dict()

        for i in range(len(playerList)):
            player = HumanPlayer(playerList[i])
            player.cash = 6000
            player.shares= []
            self.acquire.state["players"].append(player)

        self.banker.generate_tiles(self.acquire.state["players"])

        
        return True, self.print_state(self.acquire.state)

    def print_state(self, state):
        output = {}
        players = []
        for key, value in state.items():
            if key == "board":
                output["board"] = state[key].__dict__
            else:
                for pl in state[key]:
                    players.append(pl.__dict__)
                output["players"] = players

        return output
    
    
    def remove_player_tile(self, row, column):
        self.acquire.state["players"][0].tiles.remove(
            {"row":row, "column": column}
        )

    def update_banker_records(self, row, column, response, new_board):
        board = new_board["state"]["board"]
        hotels = board["hotels"]
        self.banker.update_remaining_hotels(hotels)
        self.remove_player_tile(row, column)
        if "founding" in response.keys():
            self.acquire.state["players"][0].shares.append(
                {"share": response["founding"], "count": 1}
            )

    def buy_shares(self, label,buy=True):
        remaining_shares = self.banker.remaining_shares[label]
        stock_prices = self.banker.stock_prices[label]
        if remaining_shares == 0:
            return False, Error("The shares are not available").to_dict()
        else:
            board_hotels = self.acquire.state["board"].hotels
            len_hotel_tiles = 0
            for hotel in board_hotels:
                if hotel["hotel"] == label:
                    len_hotel_tiles = len(hotel["tiles"])

            if len_hotel_tiles == 0:
                return False, Error(f"The hotel {label} is not yet formed").to_dict()

            share_price = 0
            for lower_range, higher_range, price in stock_prices:
                if len_hotel_tiles >= lower_range and len_hotel_tiles <= higher_range:
                    share_price = price
                    break
            
            player = self.acquire.state["players"][0]
            if player.cash < share_price:
                return (
                    False,
                    Error(
                        "The player does not have enough cash to buy the shares"
                    ).to_dict(),
                )
            
            player.cash -= share_price

            # If the player already has the shares, update the count or else add the shares to the player
            is_present = False
            for share in player.shares:
                if "share" in share and share["share"] == label:
                    print(share)
                    share["count"] = int(share["count"])
                    share["count"] += 1
                    is_present = True
                    break
            if not is_present:
                player.shares.append({"share": label, "count": 1})
            
            remaining_shares -= 1
            self.banker.update_remaining_shares(remaining_shares, label)
        return True, "None"


    def getFirstAvailableHotel(self):
        if len(self.banker.remaining_hotels) > 1:
            idx = random.randint(0, 100) % len(self.banker.remaining_hotels)    
        else:
            idx = 0
        if len(self.banker.remaining_hotels) > 0:
            return sorted(self.banker.remaining_hotels)[0]
        return None

    def place(self, row, column,place=True):
        hotel = self.getFirstAvailableHotel()
        board_instance = self.acquire.state["board"]
        flag = False
        requested_tile = {"row": row, "column": column}
        if requested_tile["row"] not in "ABCDEFGHI" or int(
            requested_tile["column"]
        ) not in range(1, 13):
            return (
                False,
                Error(f"The requested tile is not within the board limits").to_dict(),
            )
        for player_tile in self.acquire.state["players"][0].tiles:
            if player_tile == requested_tile:
                flag = True
                break
        if flag == False:
            return False, Error("The player does not have the requested tile").to_dict()
        is_valid = True
        if is_valid:
            try:
                boardMatrix = board_instance.create_board()
                if type(boardMatrix) != Error:
                    requestObj = {
                        "request": "query",
                        "row": row,
                        "column": column,
                        "board": board_instance,
                    }
                    if hotel is not None:
                        requestObj["hotel"] = hotel
                    response = self.acquire.handle_query(requestObj, boardMatrix,place)
                    if type(response) != Error:
                        res = {"row":row,"column":column, "response":response}
                        if "hotel" in response:
                            res["hotel"] = response["hotel"]
                        new_board = utils.matrix_to_object(boardMatrix)
                        if place:
                            self.update_banker_records(row, column, response, new_board)
                        if type(response) == dict and "acquirer" in response:
                            acquired = response["acquired"]
                            if response["acquirer"] in acquired:
                                acquired.remove(response["acquirer"])
                                
                            acquired_hotels_dict = response.get('acquired_hotels_dict')
                            del acquired_hotels_dict[response["acquirer"]]
                            self.banker.add_hotels_from_acquired(acquired)
                            self.banker.distribute_bonuses(self.acquire.state["players"], acquired_hotels_dict)

                        self.acquire.set_state(new_board["state"])
                        return True,res
                    else:
                        self.remove_player_tile(row, column)
                        return False, response.to_dict()
                else:
                    return False, Error("Board error!")
            except Exception as e:
                traceback.print_exception(*sys.exc_info())
                print("Exception::", e)
                return False, Error(str(e)).to_dict()
        else:
            return False, "State is Valid"

    def done(self):
        res, tile = self.banker.give_new_tile()
        if res:
            self.acquire.state["players"][0].tiles.append(tile) 
        player = self.acquire.state["players"].pop(0)
        self.acquire.state["players"].append(player)
        return True, self.print_state(self.acquire.state)

    def play(self):
        self.gameTree.generateTree(self)
  