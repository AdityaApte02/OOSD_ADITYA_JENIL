from adminInterface import AcquireGame
from acquire import Acquire
from banker import Banker
from error import Error
from player import HumanPlayer
import utils as utils
from tile import Tile

class Admin(AcquireGame):
    def __init__(self):
        super().__init__()
        self.banker = Banker()
        self.acquire = Acquire()

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

    def update_banker_records(self, request, response, new_board):
        board = new_board["state"]["board"]

        hotels = board["hotels"]
        self.banker.update_remaining_hotels(hotels)
        # hotels
        print("response", response)

        self.acquire.state["players"][0].tiles.remove(
            {"row": request["row"], "column": request["column"]}
        )

        if "founding" in response.keys():
            self.acquire.state["players"][0].shares.append(
                {"hotel_label": response["founding"], "count": 1}
            )

    def buy_shares(self, label):
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
                if share["share"] == label:
                    share["count"] += 1
                    is_present = True
                    break
            if not is_present:
                player.shares.append({"share": label, "count": 1})
            remaining_shares -= 1
            self.banker.update_remaining_shares(remaining_shares, label)

        print(self.banker.remaining_shares[label])
        print("Player cash: ", player.cash)
        print("Player shares: ", player.shares)
        return True, self.print_state(self.acquire.state)

    def buy(self, request):
        self.acquire.set_state(request["state"], True)
        state_instance = self.acquire.state
        is_valid, message = self.acquire.validate_state(state_instance)
        if is_valid:
            is_buy_valid = True
            for share in request["shares"]:
                if is_buy_valid:
                    is_buy_valid, buy_message = self.buy_shares(share)
                else:
                    return False, buy_message
            return True, buy_message
        else:
            return False, message
    
    def place(self, request, test=True):
        if test:
            self.banker.update_remaining_tiles(request)
            self.banker.update_remaining_hotels(request["state"]["board"]["hotels"])
            self.acquire.set_state(request["state"], test)
            state_instance = self.acquire.state
            board_instance = self.acquire.state["board"]
        else:
            state_instance = self.acquire.state
            board_instance = self.acquire.state["board"]
        # todo: iterate in tile objects
        flag = False
        requested_tile = {"row": request.get("row"), "column": request.get("column")}
        # check if requested tile is within board limits
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

        # Validate the board
        is_valid, message = self.acquire.validate_state(state_instance)
        if is_valid:
            try:
                # create the board matrix here
                boardMatrix = board_instance.create_board()
                requestObj = {
                    "request": "query",
                    "row": request["row"],
                    "column": request["column"],
                    "board": board_instance,
                }
                if "hotel" in request.keys():
                    requestObj["hotel"] = request["hotel"]
                response = self.acquire.handle_query(requestObj, boardMatrix)
                if type(response) != Error:
                    new_board = utils.matrix_to_object(boardMatrix)
                    print("new_board",new_board)
                    self.update_banker_records(request, response, new_board)
                    if type(response) == dict and "acquirer" in response:
                        acquired = response["acquired"]
                        self.banker.add_hotels_from_acquired(acquired)
                        self.banker.distribute_bonuses(self.acquire.state["players"], response.get("acquired_hotels_dict"))
                        print("acquired_hotels", response.get("acquired_hotels_dict"))

                    if test:
                        new_board['state']['players'] = []
                        for pl in self.acquire.state['players']:
                            new_board['state']['players'].append(pl.__dict__)
        
                        return True, new_board["state"]
                    else:
                        self.acquire.state["board"].tiles.append(Tile(request["row"], request["column"]).__dict__)
                        self.acquire.set_state(new_board["state"])
                    # print("tile", request["row"] + str(request["column"]))
                    # print("player", self.acquire.state["players"][0].tiles)
                    # print(self.acquire.state["board"].__dict__)
                    # print(self.print_state(self.acquire.state))

                else:
                    return False, response.to_dict()

            except Exception as e:
                print("Exception", e)
                return False, Error(str(e)).to_dict()
        else:
            return False, message

    def done(self, request=None):
        # todo: rotate the player list and return state
        if request == None:
            self.acquire.state["players"][0].tiles.append(self.banker.give_new_tile())
            player = self.acquire.state["players"].pop(0)
            self.acquire.state["players"].append(player)

        else:
            self.banker.update_remaining_tiles(request)
            self.banker.update_remaining_hotels(request["state"]["board"]["hotels"])
            self.acquire.set_state(request["state"], True)

            # print(len(self.acquire.state["players"][0].tiles))
            # new_tile = self.banker.give_new_tile()
            # print(new_tile)
            # self.acquire.state["players"][0].tiles.append(new_tile)
            # print(len(self.acquire.state["players"][0].tiles))

            player = self.acquire.state["players"].pop(0)
            print("Player", player.__dict__)
            self.acquire.state["players"].append(player)

        
        return True, self.print_state(self.acquire.state)


if __name__ == "__main__":
    admin = Admin()
    res = admin.setUp({"request": "setup", "players": ["mayur", "aditya", "honey"]})
    if type(res) != Error:
        res = admin.place(
            {
                "request": "place",
                "row": "X",
                "column": admin.acquire.state["players"][0].tiles[1]["column"],
            },
            False,
        )

        print(res)

        res = admin.done()
        print(res)

        res = admin.place(
            {
                "request": "place",
                "row": admin.acquire.state["players"][0].tiles[1]["row"],
                "column": admin.acquire.state["players"][0].tiles[1]["column"],
            },
            False,
        )

        res = admin.done()
        print(res)

    # res  = admin.place({"request":"place",
    #     "row":"D",
    #     "column":"4",
    #     "state": {
    #         "board": {
    #             "tiles": [
    #                 {"row": "A", "column": "1"},
    #                 {"row": "A", "column": "2"},
    #                 {"row": "C", "column": "3"},
    #                 {"row": "C", "column": "4"},
    #                 {"row" : "D", "column": "7"}
    #             ],
    #             "hotels": [
    #                 {
    #                     "hotel": "American",
    #                     "tiles": [
    #                         {"row": "C", "column": "3"},
    #                         {"row": "C", "column": "4"},
    #                     ],
    #                 }
    #             ],
    #         },
    #         "players": [
    #             {
    #                 "player": "Aditya",
    #                 "cash": 5000,
    #                 "tiles": [
    #                     {"row": "A", "column": "3"},
    #                     {"row": "F", "column": "3"},
    #                     {"row": "D", "column": "3"},
    #                     {"row": "D", "column": "4"},
    #                 ],
    #                 "shares": [
    #                     {"share": "American", "count": 3},
    #                 ],
    #             },

    #             {
    #                 "player": "Mayur",
    #                 "cash": 5000,
    #                 "tiles": [
    #                     {"row": "C", "column": "7"},
    #                     {"row": "E", "column": "10"},
    #                     {"row": "G", "column": "1"},
    #                     {"row": "I", "column": "11"},
    #                 ],
    #                 "shares": [
    #                     {"share": "American", "count": 2},
    #                 ],
    #             }
    #         ],
    #         }})

    # res = admin.done({
    #     "request":"done",
    #     "state": {
    #         "board": {
    #             "tiles": [
    #                 {"row": "A", "column": "1"},
    #                 {"row": "A", "column": "2"},
    #                 {"row": "C", "column": "3"},
    #                 {"row": "C", "column": "4"},
    #                 {"row" : "D", "column": "7"}
    #             ],
    #             "hotels": [
    #                 {
    #                     "hotel": "American",
    #                     "tiles": [
    #                         {"row": "C", "column": "3"},
    #                         {"row": "C", "column": "4"},
    #                     ],
    #                 }
    #             ],
    #         },
    #         "players": [
    #             {
    #                 "player": "Aditya",
    #                 "cash": 5000,
    #                 "tiles": [
    #                     {"row": "A", "column": "3"},
    #                     {"row": "F", "column": "3"},
    #                     {"row": "D", "column": "3"},
    #                     {"row": "D", "column": "4"},
    #                 ],
    #                 "shares": [
    #                     {"share": "American", "count": 3},
    #                 ],
    #             },

    #             {
    #                 "player": "Mayur",
    #                 "cash": 5000,
    #                 "tiles": [
    #                     {"row": "C", "column": "7"},
    #                     {"row": "E", "column": "10"},
    #                     {"row": "G", "column": "1"},
    #                     {"row": "I", "column": "11"},
    #                 ],
    #                 "shares": [
    #                     {"share": "American", "count": 2},
    #                 ],
    #             }
    #         ],
    #         }

    # })
    # print(res)

    # res  = admin.done({
    #     "request":"done",
    #     "state": {
    #         "board": {
    #             "tiles": [
    #                 {"row": "A", "column": "1"},
    #                 {"row": "A", "column": "2"},
    #                 {"row": "C", "column": "3"},
    #                 {"row": "C", "column": "4"},
    #             ],
    #             "hotels": [
    #                 {
    #                     "hotel": "American",
    #                     "tiles": [
    #                         {"row": "C", "column": "3"},
    #                         {"row": "C", "column": "4"},
    #                     ],
    #                 }
    #             ],
    #         },
    #         "players": [
    #             {
    #                 "player": "Aditya",
    #                 "cash": 5000,
    #                 "tiles": [
    #                     {"row": "A", "column": "3"},
    #                     {"row": "F", "column": "3"},
    #                     {"row": "D", "column": "3"},
    #                     {"row": "D", "column": "4"},
    #                 ],
    #                 "shares": [
    #                     {"share": "American", "count": 3},
    #                 ],
    #             },

    #             {
    #                 "player": "Mayur",
    #                 "cash": 5000,
    #                 "tiles": [
    #                     {"row": "C", "column": "7"},
    #                     {"row": "E", "column": "10"},
    #                     {"row": "G", "column": "1"},
    #                     {"row": "I", "column": "11"},
    #                 ],
    #                 "shares": [
    #                     {"share": "American", "count": 2},
    #                 ],
    #             }
    #         ],
    #         },
    # }
    # res = admin.place(req, True)


# res = admin.buy(
# {
#             "request": "buy",
#             "shares": ["American", "Imperial"],
#             "state": {
#                 "board": {
#                     "tiles": [
#                         {"row": "A", "column": "1"},
#                         {"row": "A", "column": "2"},
#                         {"row": "C", "column": "3"},
#                         {"row": "C", "column": "4"},
#                     ],
#                     "hotels": [
#                         {
#                             "hotel": "American",
#                             "tiles": [
#                                 {"row": "C", "column": "3"},
#                                 {"row": "C", "column": "4"},
#                             ],
#                         }
#                     ],
#                 },
#                 "players": [
#                     {
#                         "player": "Aditya",
#                         "cash": 5000,
#                         "tiles": [
#                             {"row": "A", "column": "3"},
#                             {"row": "F", "column": "3"},
#                             {"row": "D", "column": "3"},
#                             {"row": "D", "column": "4"},
#                         ],
#                         "shares": [
#                             {"share": "American", "count": 3},
#                         ],
#                     }
#                 ],
#             },
# })


# print(res)