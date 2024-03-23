import sys
sys.path.append(r'C:\Users\Aditya\OOSD_Pair1\project07\acquire_game\src')
import unittest
from  acquire.banker import Banker
from  acquire.player import HumanPlayer

class TestBanker(unittest.TestCase):
    def setUp(self):
        self.banker = Banker()

    def test_generate_tiles(self):
        players = [HumanPlayer("Player1"), HumanPlayer("Player2"), HumanPlayer("Player3")]
        self.banker.generate_tiles(players)
        self.assertEqual(len(self.banker.remaining_tiles), 90)
        for player in players:
            self.assertEqual(len(player.tiles), 6)

    def test_update_remaining_tiles(self):
        request = {
            "state": {
                "board": {
                    "tiles": [
                        {"row": "A", "column": "1"},
                        {"row": "B", "column": "2"},
                        {"row": "C", "column": "3"}
                    ]
                },
                "players": [
                    {
                        "tiles": [
                            {"row": "D", "column": "4"},
                            {"row": "E", "column": "5"}
                        ]
                    },
                    {
                        "tiles": [
                            {"row": "F", "column": "6"},
                            {"row": "G", "column": "7"}
                        ]
                    }
                ]
            }
        }
        self.banker.update_remaining_tiles(request)
        self.assertEqual(len(self.banker.remaining_tiles), 101)

    def test_update_remaining_hotels(self):
        hotels_on_board = [
            {"hotel": "Worldwide"},
            {"hotel": "Sackson"},
            {"hotel": "Festival"}
        ]
        self.banker.update_remaining_hotels(hotels_on_board)
        self.assertEqual(len(self.banker.remaining_hotels), 4)
        self.assertNotIn("Worldwide", self.banker.remaining_hotels)
        self.assertNotIn("Sackson", self.banker.remaining_hotels)
        self.assertNotIn("Festival", self.banker.remaining_hotels)

    def test_add_hotels_from_acquired(self):
        self.banker.remaining_hotels = ["Worldwide", "Sackson", "Festival", "Tower"]
        acquired_hotels = ["Imperial", "American"]
        self.banker.add_hotels_from_acquired(acquired_hotels)
        self.assertEqual(len(self.banker.remaining_hotels), 6)
        self.assertIn("Imperial", self.banker.remaining_hotels)
        self.assertIn("American", self.banker.remaining_hotels)

    def test_update_remaining_shares(self):
        remaining_shares = 20
        label = "Worldwide"
        self.banker.update_remaining_shares(remaining_shares, label)
        self.assertEqual(self.banker.remaining_shares[label], remaining_shares)

    def test_give_new_tile(self):
        self.banker.remaining_tiles = [
            {"row": "A", "column": "1"},
            {"row": "B", "column": "2"},
            {"row": "C", "column": "3"}
        ]
        tile = self.banker.give_new_tile()
        self.assertEqual(tile, {"row": "A", "column": "1"})
        self.assertEqual(len(self.banker.remaining_tiles), 2)

    def test_distribute_bonuses(self):
        players = [HumanPlayer("Aditya"), HumanPlayer("Honey"), HumanPlayer("Mayur")]
        players[0].shares = [
            {"share": "American", "count": 3},
            {"share": "Festival", "count": 2}
        ]
        players[0].cash = 5000
        players[1].shares = [
            {"share": "American", "count": 3},
            {"share": "Festival", "count": 2}
        ]
        players[1].cash = 6500
        players[2].shares = [
            {"share": "American", "count": 2},
            {"share": "Festival", "count": 4}
        ]
        players[2].cash = 4000
        acquired_hotels = {
            "American": 3,
            "Festival": 3
        }
        self.banker.distribute_bonuses(players, acquired_hotels)
        self.assertEqual(players[0].cash, 5000 + (10 * 400 + 5 * 400) // 2 + (5 * 400) // 2)
        self.assertEqual(players[1].cash, 6500 + (10 * 400 + 5 * 400) // 2 + (5 * 400) // 2)
        self.assertEqual(players[2].cash, 4000 + (10 * 400))

if __name__ == "__main__":
    unittest.main()