from abc import ABC, abstractmethod
from tile import Tile
import random

class Strategy(ABC):
    def __init__(self, strategy):
        self.strategy = strategy
    
    @abstractmethod
    def buy():
        '''
        Buy shares according to the strategy
        '''
        
    @abstractmethod
    def play():
        '''
        Place the tile according to the strategy
        '''
        
        
class OrderedStrategy(Strategy):
    def __init__(self, strategy):
        super().__init__(strategy)
        
    def find_smallest_tile(self, tiles):
        smallest_tile = Tile(
            tiles[0]["row"], tiles[0]["column"]
        )
        for tile in tiles:
            tile = Tile(tile["row"], tile["column"])
            if tile < smallest_tile:
                smallest_tile = tile
        return smallest_tile
    
    
    def simBuy(self,admin):
        cntr = 3
        shares = []
        for share in sorted(list(admin.banker.remaining_shares.keys())):
            for i in range(3):
                res, state = admin.buy_shares(share)
                if res:
                    shares.append(share)
                    cntr -= 1
                if cntr == 0:
                    admin.done()
                    return shares
        admin.done()
        return shares

    def buy(self, admin):
        cntr = 3
        shares = []
        for share in sorted(list(admin.banker.remaining_shares.keys())):
            for i in range(3):
                res, state = admin.buy_shares(share)
                if res:
                    shares.append(share)
                    cntr -= 1
                if cntr == 0:
                    admin.done()
                    return shares
        admin.done()
        return shares
    
    def simPlay(self,player,admin):
        smallest_tile = self.find_smallest_tile(player.tiles)
        print("smallest_tile",smallest_tile,player.tiles)
        row = smallest_tile.row
        column = smallest_tile.column
        return smallest_tile
    
    def play(self, player, admin):
        smallest_tile = self.find_smallest_tile(player.tiles)
        print("smallest_tile",smallest_tile,player.tiles)
        row = smallest_tile.row
        column = smallest_tile.column
        status,res = admin.place(row, column)
        if status:
            return res
    
    
class RandomStrategy(Strategy):
    def __init__(self, strategy):
        super().__init__(strategy)
        
    def buy(self, admin):
        shares = []
        placedHotels = []
        totalShares = 0
        for hotelName in list(admin.banker.remaining_shares.keys()):
            if hotelName not in admin.banker.remaining_hotels:
                placedHotels.append(hotelName)
                totalShares += admin.banker.remaining_shares[hotelName]
        cntr = min(3, totalShares)
        while cntr != 0:
            idx = random.randint(0, len(placedHotels) - 1)
            res, state = admin.buy_shares(placedHotels[idx])
            if (
                "error" in state
                and state["error"]
                == "The player does not have enough cash to buy the shares"
            ):
                break
            if res:
                shares.append(placedHotels[idx])
                cntr -= 1
        admin.done()
        return shares
    def play(self, player, admin):
        index = random.randint(0, len(player.tiles) - 1)
        tile = Tile(player.tiles[index]["row"], player.tiles[index]["column"])
        row = tile.row
        column = tile.column
        status,res = admin.place(row, column)
        if status:
            return res
    
    
class LargestAlpha(Strategy):
    def __init__(self, strategy):
        super().__init__(strategy)
        
    def find_largest_tile(self, tiles):
        largest_tile = Tile(
            tiles[0]["row"], tiles[0]["column"]
        )
        for tile in tiles:
            tile = Tile(tile["row"], tile["column"])
            if tile > largest_tile:
                largest_tile = tile
        return largest_tile
        
    def play(self, player, admin):
        largest_tile = self.find_largest_tile(player.tiles)
        row = largest_tile.row
        column = largest_tile.column
        status,res = admin.place(row, column)
        if status:
            return res
        
        
    def buy(self, admin):
        cntr = 3
        shares = []
        for share in sorted(list(admin.banker.remaining_shares.keys())):
            for i in range(3):
                res, state = admin.buy_shares(share)
                if res:
                    shares.append(share)
                    cntr -= 1
                if cntr == 0:
                    admin.done()
                    return shares
        admin.done()
        return shares
        
        
        
class SmallestAnti(Strategy):
    def __init__(self, strategy):
        super().__init__(strategy)
        
    def find_smallest_tile(self, tiles):
        smallest_tile = Tile(
            tiles[0]["row"], tiles[0]["column"]
        )
        for tile in tiles:
            tile = Tile(tile["row"], tile["column"])
            if tile < smallest_tile:
                smallest_tile = tile
        return smallest_tile
        
    def play(self, player, admin):
        smallest_tile = self.find_smallest_tile(player.tiles)
        row = smallest_tile.row
        column = smallest_tile.column
        status,res = admin.place(row, column)
        if status:
            return res
        
        
    def buy(self, admin):
        cntr = 3
        shares = []
        for share in sorted(list(admin.banker.remaining_shares.keys()), reverse=True):
            for i in range(3):
                res, state = admin.buy_shares(share)
                if res:
                    shares.append(share)
                    cntr -= 1
                if cntr == 0:
                    admin.done()
                    return shares
        admin.done()
        return shares
        
    