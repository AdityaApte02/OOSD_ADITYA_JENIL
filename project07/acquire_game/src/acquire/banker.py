import random


class Banker:
    def __init__(self):
        self.remaining_tiles = []
        self.remaining_shares = {
            "Worldwide": 25,
            "Sackson": 25,
            "Festival": 25,
            "Imperial": 25,
            "American": 25,
            "Continental": 25,
            "Tower": 25,
        }
        self.remaining_hotels = list(self.remaining_shares.keys())

        self.stock_prices = {
            "Worldwide": [
                (2, 2, 200),
                (3, 3, 300),
                (4, 4, 400),
                (5, 5, 500),
                (6, 10, 600),
                (11, 20, 700),
                (21, 30, 800),
                (31, 40, 900),
                (41, 41, 1000),
            ],
            "Sackson": [
                (2, 2, 200),
                (3, 3, 300),
                (4, 4, 400),
                (5, 5, 500),
                (6, 10, 600),
                (11, 20, 700),
                (21, 30, 800),
                (31, 40, 900),
                (41, 41, 1000),
            ],
            "Festival": [
                (2, 2, 300),
                (3, 3, 400),
                (4, 4, 500),
                (5, 5, 600),
                (6, 10, 700),
                (11, 20, 800),
                (21, 30, 900),
                (31, 40, 1000),
                (41, 41, 1100),
            ],
            "Imperial": [
                (2, 2, 300),
                (3, 3, 400),
                (4, 4, 500),
                (5, 5, 600),
                (6, 10, 700),
                (11, 20, 800),
                (21, 30, 900),
                (31, 40, 1000),
                (41, 41, 1100),
            ],
            "American": [
                (2, 2, 300),
                (3, 3, 400),
                (4, 4, 500),
                (5, 5, 600),
                (6, 10, 700),
                (11, 20, 800),
                (21, 30, 900),
                (31, 40, 1000),
                (41, 41, 1100),
            ],
            "Continental": [
                (2, 2, 400),
                (3, 3, 500),
                (4, 4, 600),
                (5, 5, 700),
                (6, 10, 800),
                (11, 20, 900),
                (21, 30, 1000),
                (31, 40, 1100),
                (41, 41, 1200),
            ],
            "Tower": [
                (2, 2, 400),
                (3, 3, 500),
                (4, 4, 600),
                (5, 5, 700),
                (6, 10, 800),
                (11, 20, 900),
                (21, 30, 1000),
                (31, 40, 1100),
                (41, 41, 1200),
            ],
        }

    def generate_tiles(self, players):
        all_tiles = [
            {"row": row, "column": str(col)} for row in "ABCDEFGHI" for col in range(1, 13)
        ]

        random.shuffle(all_tiles)

        for _ in range(6):
            for player in players:
                player.tiles.append(all_tiles.pop())

        self.remaining_tiles = all_tiles

    # todo: update everything from boardMatrix

    def update_remaining_tiles(self, request):
        all_tiles = [
            {"row": row, "column": str(col)}
            for row in "ABCDEFGHI"
            for col in range(1, 13)
        ]

        board_tiles = request["state"]["board"]["tiles"]
        for tile in board_tiles:
            if tile in all_tiles:
                all_tiles.remove(tile)

        players = request["state"]["players"]
        for player in players:
            for player_tile in player["tiles"]:
                if player_tile in all_tiles:
                    all_tiles.remove(player_tile)

        random.shuffle(all_tiles)
        self.remaining_tiles = all_tiles

    def update_remaining_hotels(self, hotels_on_board):
        for hotel in hotels_on_board:
            hotel_name = hotel["hotel"]
            if hotel_name in self.remaining_hotels:
                self.remaining_hotels.remove(hotel_name)

    def add_hotels_from_acquired(self, acquired_hotels):
        for hotel in acquired_hotels:
            if hotel not in self.remaining_hotels:
                self.remaining_hotels.append(hotel)

    def update_remaining_shares(self, remaining_shares, label):
        self.remaining_shares[label] = remaining_shares
    
    def distribute_bonuses(self, players, acquired_hotels):
        hotel_stock_price = 0
        for hotel, len_hotel_tiles in acquired_hotels.items():
            for lower_range, higher_range, price in self.stock_prices[hotel]:
                if len_hotel_tiles >= lower_range and len_hotel_tiles <= higher_range:
                    hotel_stock_price = price
                    break
            stock_holder = {}
            for player in players:
                for shares in player.shares:
                    if hotel == shares["share"]:
                        stock_holder[player.name] = shares["count"]
                        break

        
            print("Stock_holder: ", stock_holder)
            # stock_holder = {'Aditya': 2, 'Honey': 3}
            sorted_stock_holder = list(sorted(stock_holder.items(), key=lambda item: item[1], reverse=True))

            if len(sorted_stock_holder) == 1:
                for player in players:
                    if player.name == sorted_stock_holder[0][0]:
                        player.cash += ( 10 * hotel_stock_price + 5 * hotel_stock_price)
            elif len(sorted_stock_holder) == 2:
                if sorted_stock_holder[0][1] == sorted_stock_holder[1][1]:
                    for player in players:
                        if player.name == sorted_stock_holder[0][0]:
                            player.cash += (5 * hotel_stock_price + 10 * hotel_stock_price) // 2
                        elif player.name == sorted_stock_holder[1][0]:
                            player.cash += (5 * hotel_stock_price + 10 * hotel_stock_price) // 2
                elif sorted_stock_holder[0][1] > sorted_stock_holder[1][1]:
                    for player in players:
                        if player.name == sorted_stock_holder[0][0]:
                            player.cash += 10 * hotel_stock_price
                        elif player.name == sorted_stock_holder[1][0]:
                            player.cash += 5 * hotel_stock_price
            elif len(sorted_stock_holder) >= 2:
                if sorted_stock_holder[0][1] == sorted_stock_holder[1][1]:
                    for player in players:
                        if player.name == sorted_stock_holder[0][0]:
                            player.cash += (5 * hotel_stock_price + 10 * hotel_stock_price) // 2
                        elif player.name == sorted_stock_holder[1][0]:
                            player.cash += (5 * hotel_stock_price + 10 * hotel_stock_price) // 2
                elif sorted_stock_holder[1][1] == sorted_stock_holder[2][1]:
                    for player in players:
                        if player.name == sorted_stock_holder[0][0]:
                            player.cash += 10 * hotel_stock_price
                        elif player.name == sorted_stock_holder[1][0]:
                            player.cash += (5 * hotel_stock_price) // 2
                        elif player.name == sorted_stock_holder[2][0]:
                            player.cash += (5 * hotel_stock_price) // 2
                elif sorted_stock_holder[0][1] > sorted_stock_holder[1][1]:
                    for player in players:
                        if player.name == sorted_stock_holder[0][0]:
                            player.cash += 10 * hotel_stock_price
                        elif player.name == sorted_stock_holder[1][0]:
                            player.cash += 5 * hotel_stock_price
        
        pass

    def give_new_tile(self):
        # This is to be called separately in done method
        
        tile = self.remaining_tiles.pop(0)
        return tile
