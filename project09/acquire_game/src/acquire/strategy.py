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
        if tiles == []:
            return []
        smallest_tile = Tile(
            tiles[0]["row"], tiles[0]["column"]
        )
        for tile in tiles:
            tile = Tile(tile["row"], tile["column"])
            if tile < smallest_tile:
                smallest_tile = tile
        return smallest_tile

    def reset(self, admin,initalCash,shares):
        admin.acquire.state["players"][0].cash = initalCash
        print(f"{admin.acquire.state['players'][0].name}:",admin.acquire.state["players"][0].shares)
        for share in shares:
            for s1 in admin.acquire.state["players"][0].shares:
                if s1["share"] == share:
                    s1["count"] -= 1
                    admin.banker.remaining_shares[share] += 1
                    if s1["count"] == 0:
                        admin.acquire.state["players"][0].shares.remove(s1)
                    break
        return True
    
    
    def buy(self, admin, perform):
        cntr = 3
        shares = []
        initialCash = admin.acquire.state["players"][0].cash
        for share in sorted(list(admin.banker.remaining_shares.keys())):
            for i in range(3):
                res, state = admin.buy_shares(share, perform)
                if res:
                    shares.append(share)
                    cntr -= 1
                if cntr == 0:
                    if perform:
                        admin.done()
                    else:
                        self.reset(admin,initialCash,shares)
                    return shares
        if perform:
            admin.done()
        else:
            self.reset(admin,initialCash,shares)
        return shares
    
    def play(self, player, admin, perform):
        smallest_tile = self.find_smallest_tile(player.tiles)
        if smallest_tile == []:
            return False
        row = smallest_tile.row
        column = smallest_tile.column
        status,res = admin.place(row, column, perform)
        if not perform:
            retAns = {"Tile":smallest_tile,"hotel":None}
            if "hotel" in res:
                retAns["hotel"] = res["hotel"]
            print(retAns)
            return retAns
        if status:
            return res
    
    
class RandomStrategy(Strategy):
    def __init__(self, strategy):
        super().__init__(strategy)
        
    def reset(self, admin,initalCash,shares):
        admin.acquire.state["players"][0].cash = initalCash
        print(f"{admin.acquire.state['players'][0].name}:",admin.acquire.state["players"][0].shares)
        for share in shares:
            for s1 in admin.acquire.state["players"][0].shares:
                if s1["share"] == share:
                    s1["count"] -= 1
                    admin.banker.remaining_shares[share] += 1
                    if s1["count"] == 0:
                        admin.acquire.state["players"][0].shares.remove(s1)
                    break
        return True
        
    def buy(self, admin, perform):
        shares = []
        placedHotels = []
        totalShares = 0
        initialCash = admin.acquire.state["players"][0].cash
        for hotelName in list(admin.banker.remaining_shares.keys()):
            if hotelName not in admin.banker.remaining_hotels:
                placedHotels.append(hotelName)
                totalShares += admin.banker.remaining_shares[hotelName]
        cntr = min(3, totalShares)
        while cntr != 0:
            idx = random.randint(0, len(placedHotels) - 1)
            res, state = admin.buy_shares(placedHotels[idx], perform)
            if (
                "error" in state
                and state["error"]
                == "The player does not have enough cash to buy the shares"
            ):
                break
            if res:
                shares.append(placedHotels[idx])
                cntr -= 1
        if perform:
            admin.done()
        else:
            self.reset(admin,initialCash,shares)
        return shares
    
    def play(self, player, admin, perform):
        if len(player.tiles) <= 1:
            index = 0
            if len(player.tiles) == 0:
                return False
        else:
            index = random.randint(0, len(player.tiles)-1)
        tile = Tile(player.tiles[index]["row"], player.tiles[index]["column"])
        row = tile.row
        column = tile.column
        status,res = admin.place(row, column, perform)
        if not perform:
            retAns = {"Tile":tile,"hotel":None}
            if "hotel" in res:
                retAns["hotel"] = res["hotel"]
            print(retAns)
            return retAns
        if status:
            return res
    
    
class LargestAlpha(Strategy):
    def __init__(self, strategy):
        super().__init__(strategy)
        
    def reset(self, admin,initalCash,shares):
        admin.acquire.state["players"][0].cash = initalCash
        print(f"{admin.acquire.state['players'][0].name}:",admin.acquire.state["players"][0].shares)
        for share in shares:
            for s1 in admin.acquire.state["players"][0].shares:
                if s1["share"] == share:
                    s1["count"] -= 1
                    admin.banker.remaining_shares[share] += 1
                    if s1["count"] == 0:
                        admin.acquire.state["players"][0].shares.remove(s1)
                    break
        return True
        
    def find_largest_tile(self, tiles):
        if tiles == []:
            return []
        largest_tile = Tile(
            tiles[0]["row"], tiles[0]["column"]
        )
        for tile in tiles:
            tile = Tile(tile["row"], tile["column"])
            if tile > largest_tile:
                largest_tile = tile
        return largest_tile
        
    def play(self, player, admin, perform):
        largest_tile = self.find_largest_tile(player.tiles)
        if largest_tile == []:  
            return False
        row = largest_tile.row
        column = largest_tile.column
        status,res = admin.place(row, column, perform)
        if not perform:
            retAns = {"Tile":largest_tile,"hotel":None}
            if "hotel" in res:
                retAns["hotel"] = res["hotel"]
            print(retAns)
            return retAns
        if status:
            return res
        
        
    def buy(self, admin, perform):
        cntr = 3
        shares = []
        initialCash = admin.acquire.state["players"][0].cash
        for share in sorted(list(admin.banker.remaining_shares.keys())):
            for i in range(3):
                res, state = admin.buy_shares(share, perform)
                if res:
                    shares.append(share)
                    cntr -= 1
                if cntr == 0:
                    if perform:
                        admin.done()
                    else:
                        self.reset(admin,initialCash,shares)
                    return shares
                
        if perform:
            admin.done()
        else:
            self.reset(admin,initialCash,shares)
        return shares
        
        
        
class SmallestAnti(Strategy):
    def __init__(self, strategy):
        super().__init__(strategy)
        
    def reset(self, admin,initalCash,shares):
        admin.acquire.state["players"][0].cash = initalCash
        print(f"{admin.acquire.state['players'][0].name}:",admin.acquire.state["players"][0].shares)
        for share in shares:
            for s1 in admin.acquire.state["players"][0].shares:
                if s1["share"] == share:
                    s1["count"] -= 1
                    admin.banker.remaining_shares[share] += 1
                    if s1["count"] == 0:
                        admin.acquire.state["players"][0].shares.remove(s1)
                    break
        return True
        
    def find_smallest_tile(self, tiles):
        if tiles == []: 
            return []
        print("tiles"   ,tiles)
        smallest_tile = Tile(
            tiles[0]["row"], tiles[0]["column"]
        )
        for tile in tiles:
            tile = Tile(tile["row"], tile["column"])
            if tile < smallest_tile:
                smallest_tile = tile
        return smallest_tile
        
    def play(self, player, admin, perform):
        smallest_tile = self.find_smallest_tile(player.tiles)
        if smallest_tile == []: 
            return False
        row = smallest_tile.row
        column = smallest_tile.column
        status,res = admin.place(row, column, perform)
        if not perform:
            retAns = {"Tile":smallest_tile,"hotel":None}
            if "hotel" in res:
                retAns["hotel"] = res["hotel"]
            print(retAns)
            return retAns
        if status:
            return res
        
        
    def buy(self, admin, perform):
        cntr = 3
        shares = []
        initialCash = admin.acquire.state["players"][0].cash
        for share in sorted(list(admin.banker.remaining_shares.keys()), reverse=True):
            for i in range(3):
                res, state = admin.buy_shares(share, perform)
                if res:
                    shares.append(share)
                    cntr -= 1
                if cntr == 0:
                    if perform:
                        admin.done()
                    else:
                        self.reset(admin,initialCash,shares)
                    return shares
        if perform:
            admin.done()
        else:
            self.reset(admin,initialCash,shares)
        return shares
        
    