import unittest
from unittest.mock import patch
from admin import Admin
from acquire import Acquire
from board import Board


class TestAdmin(unittest.TestCase):
    def setUp(self):
        self.admin = Admin()

    def _set_up_for_print_state(self, request):
        self.acquire = Acquire()
        self.board_instance = Board()
        self.board_instance.tiles = request["board"]["tiles"]
        self.board_instance.hotels = request["board"]["hotels"]
        self.acquire.set_state(request, True)

    def test_print_state(self):
        request = {
            "board": {
                "tiles": [
                    {"row": "A", "column": "1"},
                    {"row": "A", "column": "2"},
                    {"row": "C", "column": "3"},
                    {"row": "C", "column": "4"},
                    {"row": "D", "column": "7"},
                ],
                "hotels": [
                    {
                        "hotel": "American",
                        "tiles": [
                            {"row": "C", "column": "3"},
                            {"row": "C", "column": "4"},
                        ],
                    }
                ],
            },
            "players": [
                {
                    "player": "Honey",
                    "cash": 5000,
                    "tiles": [
                        {"row": "A", "column": "3"},
                        {"row": "F", "column": "3"},
                        {"row": "D", "column": "3"},
                        {"row": "D", "column": "4"},
                    ],
                    "shares": [{"share": "American", "count": 3}],
                },
            ],
        }
        self._set_up_for_print_state(request)
        output = self.admin.print_state(self.acquire.state)
        expected_output = {
            "board": {
                "tiles": [
                    {"row": "A", "column": "1"},
                    {"row": "A", "column": "2"},
                    {"row": "C", "column": "3"},
                    {"row": "C", "column": "4"},
                    {"row": "D", "column": "7"},
                ],
                "hotels": [
                    {
                        "hotel": "American",
                        "tiles": [
                            {"row": "C", "column": "3"},
                            {"row": "C", "column": "4"},
                        ],
                    }
                ],
            },
            "players": [
                {
                    "name": "Honey",
                    "cash": 5000,
                    "tiles": [
                        {"row": "A", "column": "3"},
                        {"row": "F", "column": "3"},
                        {"row": "D", "column": "3"},
                        {"row": "D", "column": "4"},
                    ],
                    "shares": [{"share": "American", "count": 3}],
                }
            ],
        }
        self.assertEqual(output, expected_output)

    def test_setUp_invalid_request(self):
        request = {
            "request": "setup",
            "players": [
                "player1",
                "player2",
                "player3",
                "player4",
                "player5",
                "player6",
                "player7",
            ],
        }
        expected_output = {"error": "Number of players should be between 1 to 6"}
        result, output = self.admin.setUp(request)
        self.assertFalse(result)
        self.assertEqual(output, expected_output)

    def test_setUp_long_player_name(self):
        request = {"request": "setup", "players": ["areallyloooooongplayername"]}
        expected_output = {"error": "Player name should be less than 20 characters"}
        result, output = self.admin.setUp(request)
        self.assertFalse(result)
        self.assertEqual(output, expected_output)

    def test_setUp_unique_player_name(self):
        request = {"request": "setup", "players": ["player1", "player1"]}
        expected_output = {"error": "Player names should be unique"}
        result, output = self.admin.setUp(request)
        self.assertFalse(result)
        self.assertEqual(output, expected_output)

    def test_valid_place_with_bonus_distribution(self):
        request = {
            "request": "place",
            "row": "D",
            "column": "4",
            "state": {
                "board": {
                    "tiles": [
                        {"row": "B", "column": "2"},
                        {"row": "C", "column": "1"},
                        {"row": "C", "column": "6"},
                        {"row": "C", "column": "5"},
                        {"row": "C", "column": "4"},
                        {"row": "D", "column": "2"},
                        {"row": "D", "column": "1"},
                        {"row": "E", "column": "4"},
                        {"row": "E", "column": "5"},
                        {"row": "E", "column": "6"},
                        {"row": "F", "column": "4"},
                        {"row": "D", "column": "3"},
                    ],
                    "hotels": [
                        {
                            "hotel": "Festival",
                            "tiles": [
                                {"row": "D", "column": "2"},
                                {"row": "D", "column": "1"},
                                {"row": "D", "column": "3"},
                            ],
                        },
                        {
                            "hotel": "Continental",
                            "tiles": [
                                {"row": "E", "column": "4"},
                                {"row": "E", "column": "5"},
                                {"row": "E", "column": "6"},
                                {"row": "F", "column": "4"},
                            ],
                        },
                        {
                            "hotel": "American",
                            "tiles": [
                                {"row": "C", "column": "6"},
                                {"row": "C", "column": "5"},
                                {"row": "C", "column": "4"},
                            ],
                        },
                    ],
                },
                "players": [
                    {
                        "player": "Aditya",
                        "cash": 5000,
                        "tiles": [
                            {"row": "A", "column": "3"},
                            {"row": "F", "column": "3"},
                            {"row": "E", "column": "1"},
                            {"row": "D", "column": "4"},
                        ],
                        "shares": [
                            {"share": "American", "count": 3},
                            {"share": "Festival", "count": 2},
                        ],
                    },
                    {
                        "player": "Honey",
                        "cash": 6500,
                        "tiles": [
                            {"row": "I", "column": "3"},
                            {"row": "I", "column": "4"},
                            {"row": "H", "column": "3"},
                            {"row": "G", "column": "0"},
                        ],
                        "shares": [
                            {"share": "American", "count": 3},
                            {"share": "Festival", "count": 2},
                        ],
                    },
                    {
                        "player": "Mayur",
                        "cash": 4000,
                        "tiles": [
                            {"row": "I", "column": "2"},
                            {"row": "I", "column": "1"},
                            {"row": "H", "column": "2"},
                            {"row": "G", "column": "1"},
                        ],
                        "shares": [
                            {"share": "American", "count": 3},
                            {"share": "Festival", "count": 4},
                        ],
                    },
                ],
            },
        }
        expected_output = {
            "board": {
                "tiles": [
                    {"row": "B", "column": "2"},
                    {"row": "C", "column": "1"},
                    {"row": "C", "column": "4"},
                    {"row": "C", "column": "5"},
                    {"row": "C", "column": "6"},
                    {"row": "D", "column": "1"},
                    {"row": "D", "column": "2"},
                    {"row": "D", "column": "3"},
                    {"row": "D", "column": "4"},
                    {"row": "E", "column": "4"},
                    {"row": "E", "column": "5"},
                    {"row": "E", "column": "6"},
                    {"row": "F", "column": "4"},
                ],
                "hotels": [
                    {
                        "hotel": "Continental",
                        "tiles": [
                            {"row": "C", "column": "4"},
                            {"row": "C", "column": "5"},
                            {"row": "C", "column": "6"},
                            {"row": "D", "column": "1"},
                            {"row": "D", "column": "2"},
                            {"row": "D", "column": "3"},
                            {"row": "D", "column": "4"},
                            {"row": "E", "column": "4"},
                            {"row": "E", "column": "5"},
                            {"row": "E", "column": "6"},
                            {"row": "F", "column": "4"},
                        ],
                    }
                ],
            },
            "players": [
                {
                    "name": "Aditya",
                    "cash": 9000,
                    "tiles": [
                        {"row": "A", "column": "3"},
                        {"row": "F", "column": "3"},
                        {"row": "E", "column": "1"},
                    ],
                    "shares": [
                        {"share": "American", "count": 3},
                        {"share": "Festival", "count": 2},
                    ],
                },
                {
                    "name": "Honey",
                    "cash": 10500,
                    "tiles": [
                        {"row": "I", "column": "3"},
                        {"row": "I", "column": "4"},
                        {"row": "H", "column": "3"},
                        {"row": "G", "column": "0"},
                    ],
                    "shares": [
                        {"share": "American", "count": 3},
                        {"share": "Festival", "count": 2},
                    ],
                },
                {
                    "name": "Mayur",
                    "cash": 8000,
                    "tiles": [
                        {"row": "I", "column": "2"},
                        {"row": "I", "column": "1"},
                        {"row": "H", "column": "2"},
                        {"row": "G", "column": "1"},
                    ],
                    "shares": [
                        {"share": "American", "count": 3},
                        {"share": "Festival", "count": 4},
                    ],
                },
            ],
        }
        result, output = self.admin.place(request)
        self.assertTrue(result)
        print("OUTPUT", output)
        print("EXPECTED", expected_output)
        self.assertEqual(output, expected_output)

    def test_place_invalid_player_tile(self):
        request = {
            "request": "place",
            "row": "H",
            "column": "10",
            "state": {
                "board": {
                    "tiles": [
                        {"row": "A", "column": "1"},
                        {"row": "A", "column": "2"},
                        {"row": "C", "column": "3"},
                        {"row": "C", "column": "4"},
                        {"row": "D", "column": "7"},
                    ],
                    "hotels": [
                        {
                            "hotel": "American",
                            "tiles": [
                                {"row": "C", "column": "3"},
                                {"row": "C", "column": "4"},
                            ],
                        }
                    ],
                },
                "players": [
                    {
                        "player": "Aditya",
                        "cash": 5000,
                        "tiles": [
                            {"row": "A", "column": "3"},
                            {"row": "F", "column": "3"},
                            {"row": "D", "column": "3"},
                            {"row": "D", "column": "4"},
                        ],
                        "shares": [{"share": "American", "count": 3}],
                    },
                    {
                        "player": "Mayur",
                        "cash": 5000,
                        "tiles": [
                            {"row": "C", "column": "7"},
                            {"row": "E", "column": "10"},
                            {"row": "G", "column": "1"},
                            {"row": "I", "column": "11"},
                        ],
                        "shares": [{"share": "American", "count": 2}],
                    },
                ],
            },
        }
        expected_output = {"error": "The player does not have the requested tile"}
        result, output = self.admin.place(request)
        self.assertFalse(result)
        self.assertEqual(output, expected_output)

    def test_place_invalid_hotel_placement(self):
        request = {
            "request": "place",
            "row": "D",
            "column": "10",
            "state": {
                "board": {
                    "tiles": [
                        {"row": "B", "column": "2"},
                        {"row": "C", "column": "1"},
                        {"row": "D", "column": "5"},
                        {"row": "C", "column": "5"},
                        {"row": "C", "column": "4"},
                        {"row": "D", "column": "4"},
                        {"row": "D", "column": "3"},
                        {"row": "E", "column": "4"},
                        {"row": "E", "column": "5"},
                        {"row": "F", "column": "5"},
                        {"row": "C", "column": "3"},
                    ],
                    "hotels": [
                        {
                            "hotel": "American",
                            "tiles": [
                                {"row": "D", "column": "3"},
                                {"row": "D", "column": "4"},
                            ],
                        },
                        {
                            "hotel": "Imperial",
                            "tiles": [
                                {"row": "C", "column": "4"},
                                {"row": "C", "column": "3"},
                            ],
                        },
                        {
                            "hotel": "Continental",
                            "tiles": [
                                {"row": "E", "column": "4"},
                                {"row": "E", "column": "5"},
                                {"row": "F", "column": "5"},
                            ],
                        },
                        {
                            "hotel": "Festival",
                            "tiles": [
                                {"row": "D", "column": "5"},
                                {"row": "C", "column": "5"},
                            ],
                        },
                    ],
                },
                "players": [
                    {
                        "player": "Aditya",
                        "cash": 5000,
                        "tiles": [
                            {"row": "A", "column": "11"},
                            {"row": "F", "column": "12"},
                            {"row": "D", "column": "10"},
                            {"row": "D", "column": "11"},
                        ],
                        "shares": [{"share": "American", "count": 3}],
                    },
                    {
                        "player": "Honey",
                        "cash": 6500,
                        "tiles": [
                            {"row": "B", "column": "3"},
                            {"row": "F", "column": "10"},
                            {"row": "D", "column": "9"},
                            {"row": "E", "column": "12"},
                        ],
                        "shares": [{"share": "American", "count": 3}],
                    },
                ],
            },
        }
        expected_output = {"error": "Invalid hotel placement"}
        result, output = self.admin.place(request)
        self.assertFalse(result)
        self.assertEqual(output, expected_output)

    def test_valid_buy(self):
        request = {
            "request": "buy",
            "shares": ["American", "Imperial"],
            "state": {
                "board": {
                    "tiles": [
                        {"row": "A", "column": "1"},
                        {"row": "A", "column": "3"},
                        {"row": "A", "column": "4"},
                        {"row": "B", "column": "1"},
                        {"row": "C", "column": "3"},
                        {"row": "C", "column": "4"},
                    ],
                    "hotels": [
                        {
                            "hotel": "Imperial",
                            "tiles": [
                                {"row": "A", "column": "1"},
                                {"row": "B", "column": "1"},
                            ],
                        },
                        {
                            "hotel": "Continental",
                            "tiles": [
                                {"row": "A", "column": "3"},
                                {"row": "A", "column": "4"},
                            ],
                        },
                        {
                            "hotel": "American",
                            "tiles": [
                                {"row": "C", "column": "3"},
                                {"row": "C", "column": "4"},
                            ],
                        },
                    ],
                },
                "players": [
                    {
                        "player": "Aditya",
                        "cash": 5000,
                        "tiles": [
                            {"row": "A", "column": "11"},
                            {"row": "F", "column": "12"},
                            {"row": "D", "column": "10"},
                            {"row": "D", "column": "11"},
                        ],
                        "shares": [{"share": "American", "count": 3}],
                    },
                    {
                        "player": "Honey",
                        "cash": 6500,
                        "tiles": [
                            {"row": "B", "column": "3"},
                            {"row": "F", "column": "10"},
                            {"row": "D", "column": "9"},
                            {"row": "E", "column": "12"},
                        ],
                        "shares": [{"share": "American", "count": 3}],
                    },
                ],
            },
        }
        expected_output = {
            "board": {
                "tiles": [
                    {"row": "A", "column": "1"},
                    {"row": "A", "column": "3"},
                    {"row": "A", "column": "4"},
                    {"row": "B", "column": "1"},
                    {"row": "C", "column": "3"},
                    {"row": "C", "column": "4"},
                ],
                "hotels": [
                    {
                        "hotel": "Imperial",
                        "tiles": [
                            {"row": "A", "column": "1"},
                            {"row": "B", "column": "1"},
                        ],
                    },
                    {
                        "hotel": "Continental",
                        "tiles": [
                            {"row": "A", "column": "3"},
                            {"row": "A", "column": "4"},
                        ],
                    },
                    {
                        "hotel": "American",
                        "tiles": [
                            {"row": "C", "column": "3"},
                            {"row": "C", "column": "4"},
                        ],
                    },
                ],
            },
            "players": [
                {
                    "name": "Aditya",
                    "cash": 4400,
                    "tiles": [
                        {"row": "A", "column": "11"},
                        {"row": "F", "column": "12"},
                        {"row": "D", "column": "10"},
                        {"row": "D", "column": "11"},
                    ],
                    "shares": [
                        {"share": "American", "count": 4},
                        {"share": "Imperial", "count": 1},
                    ],
                },
                {
                    "name": "Honey",
                    "cash": 6500,
                    "tiles": [
                        {"row": "B", "column": "3"},
                        {"row": "F", "column": "10"},
                        {"row": "D", "column": "9"},
                        {"row": "E", "column": "12"},
                    ],
                    "shares": [{"share": "American", "count": 3}],
                },
            ],
        }
        result, output = self.admin.buy(request)
        self.assertTrue(result)
        self.assertEqual(output, expected_output)

    def test_buy_not_formed_hotel_shares(self):
        request = {
            "request": "buy",
            "shares": ["American", "Imperial"],
            "state": {
                "board": {
                    "tiles": [
                        {"row": "A", "column": "1"},
                        {"row": "A", "column": "3"},
                        {"row": "A", "column": "4"},
                        {"row": "B", "column": "1"},
                        {"row": "C", "column": "3"},
                        {"row": "C", "column": "4"},
                    ],
                    "hotels": [
                        {
                            "hotel": "Imperial",
                            "tiles": [
                                {"row": "A", "column": "1"},
                                {"row": "B", "column": "1"},
                            ],
                        },
                        {
                            "hotel": "Continental",
                            "tiles": [
                                {"row": "A", "column": "3"},
                                {"row": "A", "column": "4"},
                            ],
                        },
                        {
                            "hotel": "Festival",
                            "tiles": [
                                {"row": "C", "column": "3"},
                                {"row": "C", "column": "4"},
                            ],
                        },
                    ],
                },
                "players": [
                    {
                        "player": "Aditya",
                        "cash": 5000,
                        "tiles": [
                            {"row": "A", "column": "11"},
                            {"row": "F", "column": "10"},
                            {"row": "D", "column": "10"},
                            {"row": "D", "column": "11"},
                        ],
                        "shares": [{"share": "American", "count": 3}],
                    },
                    {
                        "player": "Honey",
                        "cash": 6500,
                        "tiles": [
                            {"row": "B", "column": "3"},
                            {"row": "F", "column": "10"},
                            {"row": "D", "column": "9"},
                            {"row": "E", "column": "12"},
                        ],
                        "shares": [{"share": "American", "count": 3}],
                    },
                ],
            },
        }
        expected_output = {"error": "The hotel American is not yet formed"}
        result, output = self.admin.buy(request)
        self.assertFalse(result)
        self.assertEqual(output, expected_output)

    def test_25_shares_already(self):
        request = {
            "request": "place",
            "row": "A",
            "column": "2",
            "hotel": "American",
            "state": {
                "board": {
                    "tiles": [
                        {"row": "A", "column": "1"},
                        {"row": "A", "column": "3"},
                        {"row": "A", "column": "4"},
                        {"row": "B", "column": "1"},
                        {"row": "C", "column": "2"},
                        {"row": "C", "column": "4"},
                    ],
                    "hotels": [
                        {
                            "hotel": "Imperial",
                            "tiles": [
                                {"row": "A", "column": "1"},
                                {"row": "B", "column": "1"},
                            ],
                        },
                        {
                            "hotel": "Continental",
                            "tiles": [
                                {"row": "A", "column": "3"},
                                {"row": "A", "column": "4"},
                            ],
                        },
                    ],
                },
                "players": [
                    {
                        "player": "Aditya",
                        "cash": 5000,
                        "tiles": [
                            {"row": "B", "column": "4"},
                            {"row": "A", "column": "2"},
                            {"row": "D", "column": "3"},
                            {"row": "D", "column": "4"},
                        ],
                        "shares": [{"share": "American", "count": 26}],
                    },
                    {
                        "player": "Honey",
                        "cash": 6500,
                        "tiles": [
                            {"row": "A", "column": "3"},
                            {"row": "F", "column": "3"},
                            {"row": "D", "column": "3"},
                            {"row": "D", "column": "4"},
                        ],
                        "shares": [{"share": "American", "count": 3}],
                    },
                ],
            },
        }
        expected_output = {
            "error": "The current player already has 25 shares of American"
        }
        result, output = self.admin.buy(request)
        self.assertFalse(result)
        self.assertEqual(output, expected_output)

    def test_valid_done(self):
        request = {
            "request": "done",
            "state": {
                "board": {
                    "tiles": [
                        {"row": "A", "column": "1"},
                        {"row": "A", "column": "2"},
                        {"row": "C", "column": "3"},
                        {"row": "C", "column": "4"},
                        {"row": "D", "column": "7"},
                    ],
                    "hotels": [
                        {
                            "hotel": "American",
                            "tiles": [
                                {"row": "C", "column": "3"},
                                {"row": "C", "column": "4"},
                            ],
                        }
                    ],
                },
                "players": [
                    {
                        "player": "Aditya",
                        "cash": 5000,
                        "tiles": [
                            {"row": "A", "column": "3"},
                            {"row": "F", "column": "3"},
                            {"row": "D", "column": "3"},
                            {"row": "D", "column": "4"},
                        ],
                        "shares": [{"share": "American", "count": 3}],
                    },
                    {
                        "player": "Mayur",
                        "cash": 5000,
                        "tiles": [
                            {"row": "C", "column": "7"},
                            {"row": "E", "column": "10"},
                            {"row": "G", "column": "1"},
                            {"row": "I", "column": "11"},
                        ],
                        "shares": [{"share": "American", "count": 2}],
                    },
                ],
            },
        }

        expected_output = {
            "board": {
                "tiles": [
                    {"row": "A", "column": "1"},
                    {"row": "A", "column": "2"},
                    {"row": "C", "column": "3"},
                    {"row": "C", "column": "4"},
                    {"row": "D", "column": "7"},
                ],
                "hotels": [
                    {
                        "hotel": "American",
                        "tiles": [
                            {"row": "C", "column": "3"},
                            {"row": "C", "column": "4"},
                        ],
                    }
                ],
            },
            "players": [
                {
                    "name": "Mayur",
                    "cash": 5000,
                    "tiles": [
                        {"row": "C", "column": "7"},
                        {"row": "E", "column": "10"},
                        {"row": "G", "column": "1"},
                        {"row": "I", "column": "11"},
                    ],
                    "shares": [{"share": "American", "count": 2}],
                },
                {
                    "name": "Aditya",
                    "cash": 5000,
                    "tiles": [
                        {"row": "A", "column": "3"},
                        {"row": "F", "column": "3"},
                        {"row": "D", "column": "3"},
                        {"row": "D", "column": "4"},
                    ],
                    "shares": [{"share": "American", "count": 3}],
                },
            ],
        }

        result, output = self.admin.done(request)
        self.assertTrue(result)
        self.assertEqual(output, expected_output)


if __name__ == "__main__":
    unittest.main()
