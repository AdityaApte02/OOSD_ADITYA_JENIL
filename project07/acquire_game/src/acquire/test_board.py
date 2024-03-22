# test file to test the board representation
# import required libraries
from unittest import TestCase, main

# import acquire class from acquire module
from acquire import Acquire
from board import Board

class TestBoard(TestCase):
    def _set_up(self, request):
        self.acquire = Acquire()
        self.board_instance = Board()
        self.board_instance.tiles = request['board']['tiles']
        self.board_instance.hotels = request['board']['hotels']

    def test_validate_board(self):
        req = { 
                "board" :  {
                    "tiles": [
                        {"row": "A", "column": "1"},
                        {"row": "A", "column": "2"},
                        {"row": "C", "column": "3"},
                        {"row": "C", "column": "4"}
                    ],
                    "hotels": [
                        {
                            "hotel": "American",
                            "tiles": [{"row": "C", "column": "3"}, {"row": "C", "column": "4"}]
                        }
                    ]
                }
            }
        self._set_up(req)
        _, message = self.acquire.validate_board(self.board_instance)
        expected = "Board is valid"
        self.assertEqual(message, expected)
    
    def test_valid_placement(self):
        req = {
            "board": {
                "tiles": [
                {
                    "row": "A",
                    "column": "1"
                },
                {
                    "row": "A",
                    "column": "3"
                },
                {
                    "row": "A",
                    "column": "4"
                },
                {
                    "row": "B",
                    "column": "1"
                },
                {
                    "row": "C",
                    "column": "3"
                },
                {
                    "row": "C",
                    "column": "4"
                }
                ],
                "hotels": [
                {
                    "hotel": "Imperial",
                    "tiles": [
                    {
                        "row": "A",
                        "column": "1"
                    },
                    {
                        "row": "B",
                        "column": "1"
                    }
                    ]
                },
                {
                    "hotel": "Continental",
                    "tiles": [
                    {
                        "row": "A",
                        "column": "3"
                    },
                    {
                        "row": "A",
                        "column": "4"
                    }
                    ]
                },
                {
                    "hotel": "Festival",
                    "tiles": [
                    {
                        "row": "C",
                        "column": "3"
                    },
                    {
                        "row": "C",
                        "column": "4"
                    }
                    ]
                }
                ]
            }
        }
        self._set_up(req)
        created_board = self.board_instance.create_board()
        expected_board = [
            ['Imperial', '0', 'Continental', 'Continental', '0', '0', '0', '0', '0', '0', '0', '0'], 
            ['Imperial', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
            ['0', '0', 'Festival', 'Festival', '0', '0', '0', '0', '0', '0', '0', '0'], 
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
            ]
        self.assertEqual(created_board, expected_board)

    def test_invalid_tiles_list(self):
        req = { 
                "board" :  {
                    "tiles": [
                        {"row": "A", "column": "1"},
                        {"row": "A", "column": "2"},
                        {"row": "C", "column": "3"},
                        {"row": "C", "column": "4"}
                    ],
                    "hotels": [
                        {
                            "hotel": "American",
                            "tiles": [
                                {"row": "C", "column": "3"}, 
                                {"row": "C", "column": "4"},
                                {"row": "C", "column": "5"},
                                {"row": "C", "column": "6"},
                                {"row": "C", "column": "7"}
                            ]
                        }
                    ]
                }
            }
        self._set_up(req)
        _, message = self.acquire.validate_board(self.board_instance)
        expected = {
                        "error": "Hotel tiles are greater than total tiles"
                    }
        self.assertEqual(message, expected)

    def test_duplicate_tiles(self):
        req = { 
                "board" :  {
                    "tiles": [
                        {"row": "A", "column": "1"},
                        {"row": "A", "column": "2"},
                        {"row": "C", "column": "3"},
                        {"row": "C", "column": "3"},
                        {"row": "C", "column": "4"}
                    ],
                    "hotels": [
                        {
                            "hotel": "American",
                            "tiles": [
                                {"row": "C", "column": "3"}, 
                                {"row": "C", "column": "4"}
                            ]
                        }
                    ]
                }
            }
        self._set_up(req)
        _, message = self.acquire.validate_board(self.board_instance)
        expected = {
                    "error": "Tile {'row': 'C', 'column': '3'} is not unique"
                }
        self.assertEqual(message, expected)

    def test_duplicate_hotel_tiles(self):
        req = { 
                "board" :  {
                    "tiles": [
                        {"row": "A", "column": "1"},
                        {"row": "A", "column": "2"},
                        {"row": "C", "column": "3"},
                        {"row": "C", "column": "4"}
                    ],
                    "hotels": [
                        {
                            "hotel": "American",
                            "tiles": [
                                {"row": "C", "column": "3"}, 
                                {"row": "C", "column": "3"}, 
                                {"row": "C", "column": "4"}
                            ]
                        }
                    ]
                }
            }
        self._set_up(req)
        _, message = self.acquire.validate_board(self.board_instance)
        expected = {
                    "error": "Tile {'row': 'C', 'column': '3'} is not unique"
                }
        self.assertEqual(message, expected)

    def test_tiles_within_board(self):
        req = { 
                "board" :  {
                    "tiles": [
                        {"row": "A", "column": "20"},
                        {"row": "A", "column": "2"},
                        {"row": "C", "column": "3"},
                        {"row": "C", "column": "4"}
                    ],
                    "hotels": [
                        {
                            "hotel": "American",
                            "tiles": [
                                {"row": "C", "column": "3"}, 
                                {"row": "C", "column": "3"}, 
                                {"row": "C", "column": "4"}
                            ]
                        }
                    ]
                }
            }
        self._set_up(req)
        _, message = self.acquire.validate_board(self.board_instance)
        expected = {
                    "error": "Tile {'row': 'A', 'column': '20'} is not within the board"
                }
        self.assertEqual(message, expected)

    def test_hotel_tiles_within_board(self):
        req = { 
                "board" :  {
                    "tiles": [
                        {"row": "A", "column": "2"},
                        {"row": "A", "column": "2"},
                        {"row": "C", "column": "3"},
                        {"row": "C", "column": "4"}
                    ],
                    "hotels": [
                        {
                            "hotel": "American",
                            "tiles": [
                                {"row": "C", "column": "33"}, 
                                {"row": "C", "column": "3"}, 
                                {"row": "C", "column": "4"}
                            ]
                        }
                    ]
                }
            }
        self._set_up(req)
        _, message = self.acquire.validate_board(self.board_instance)
        expected = {
                    "error": "Tile {'row': 'C', 'column': '33'} is not within the board"
                }
        self.assertEqual(message, expected)

    def test_hotel_chain_size(self):
        req = { 
                "board" :  {
                    "tiles": [
                        {"row": "A", "column": "2"},
                        {"row": "A", "column": "2"},
                        {"row": "C", "column": "3"},
                        {"row": "C", "column": "4"}
                    ],
                    "hotels": [
                        {
                            "hotel": "American",
                            "tiles": [
                                {"row": "C", "column": "4"}
                            ]
                        }
                    ]
                }
            }
        self._set_up(req)
        _, message = self.acquire.validate_board(self.board_instance)
        expected = {
                    "error": "Hotel {'hotel': 'American', 'tiles': [{'row': 'C', 'column': '4'}]} chain size is less than 2"
                }
        self.assertEqual(message, expected)

    def test_hotel_tiles_are_in_board_tiles(self):
        req = { 
                "board" :  {
                    "tiles": [
                        {"row": "A", "column": "2"},
                        {"row": "A", "column": "2"},
                        {"row": "C", "column": "3"},
                        {"row": "C", "column": "4"}
                    ],
                    "hotels": [
                        {
                            "hotel": "American",
                            "tiles": [
                                {"row": "C", "column": "11"},
                                {"row": "C", "column": "3"}
                            ]
                        }
                    ]
                }
            }
        self._set_up(req)
        _, message = self.acquire.validate_board(self.board_instance)
        expected = {
                "error": "Tile {'row': 'C', 'column': '11'} is not present in board tiles"
            }
        self.assertEqual(message, expected)

    def test_hotel_tiles_are_connected(self):
        req = { 
                "board" :  {
                    "tiles": [
                        {"row": "A", "column": "2"},
                        {"row": "A", "column": "2"},
                        {"row": "C", "column": "3"},
                        {"row": "C", "column": "5"}
                    ],
                    "hotels": [
                        {
                            "hotel": "American",
                            "tiles": [
                                {"row": "C", "column": "3"},
                                {"row": "C", "column": "5"}
                            ]
                        }
                    ]
                }
            }
        self._set_up(req)
        _, message = self.acquire.validate_board(self.board_instance)
        expected = {
                    "error": "Hotel American chain's tiles are not connected"
                }
        self.assertEqual(message, expected)


if __name__ == "__main__":
    main()