import unittest
from unittest.mock import patch
import sys
sys.path.append(r'C:\Users\Aditya\OOSD_Pair1\project07\acquire_game\src')
from acquire.acquire import Acquire
from acquire.error import Error
from acquire.board import Board
from acquire.player import HumanPlayer

def create_test_boardMatrix(boardObj):
    board = Board()
    board.tiles = boardObj['tiles']
    board.hotels = boardObj['hotels']
    boardMatrix = board.create_board()

    return boardMatrix
        

class AcquireTest(unittest.TestCase):
    def setUp(self):
        self.acquire = Acquire()

    def test_EmptyBoard_setState_request(self):
        state = {"board":{}, "playersList":[]}
        expected_output = {
            "error": "Board is Empty"
        }
        result, output = self.acquire.set_state(state)
        self.assertFalse(result)
        self.assertEqual(output, expected_output)


    def test_wrongAttributeName_setState_request(self):
        state = {"board":{"tiles":[], "hotels":[]}}
        expected_output = {
            "error": "Invalid key found in the request state"
        }
        result, output = self.acquire.set_state(state)
        self.assertFalse(result)
        self.assertEqual(output, expected_output)


    def test_validate_state(self):
        board = {
                    "tiles": [
                    ],
                    "hotels": [
                    ],
                }
        self.acquire.state['board'].tiles = board['tiles']
        self.acquire.state['board'].hotels = board['hotels']
        state1 = {
            "board": self.acquire.state['board'],
            "players": [HumanPlayer("Aditya")]
        }
        state1['players'][0].cash = -5000
        state1['players'][0].tiles = [
            {"row": "A", "column": "3"},
            {"row": "F", "column": "3"},
            {"row": "D", "column": "3"},
            {"row": "D", "column": "4"}
        ]
        state1['players'][0].shares = [
            {"share": "American", "count": 3}
        ]
        
    
        expected_output = {'error':'The current player has negative cash'}
        result, output = self.acquire.validate_state(state1)
        self.assertEqual(output, expected_output)
        
        
        state2 = {
            "board": self.acquire.state['board'],
                "players": [
                ],
        }
        expected_output = {'error':'The players list is empty'}
        result, output = self.acquire.validate_state(state2)
        self.assertEqual(output, expected_output)
        state3 = {
            "board": self.acquire.state['board'],
            "players": [HumanPlayer("Aditya")]
        }
        state3['players'][0].cash = 5000
        state3['players'][0].tiles = [
            {"row": "A", "column": "3"},
            {"row": "F", "column": "3"},
            {"row": "D", "column": "3"},
            {"row": "D", "column": "4"},
            {"row": "G", "column": "8"},
            {"row": "H", "column": "2"},
            {"row": "F", "column": "10"},
        ]
        state3['players'][0].shares = [
            {"share": "American", "count": 3}
        ]

        expected_output = {'error':'Player ' + state3['players'][0].name+' has more than 6 tiles'}
        result, output = self.acquire.validate_state(state3)
        self.assertEqual(output, expected_output)
        
        state4 = {
            "board": self.acquire.state['board'],
            "players": [HumanPlayer("Aditya"), HumanPlayer("Aditya")]
        }
        expected_output = {'error':'The players name are not unique'}
        result, output = self.acquire.validate_state(state4)
        self.assertEqual(output, expected_output)

        state5 = {
            "board": self.acquire.state['board'],
            "players": [HumanPlayer("Aditya")]
        }
        state5['players'][0].cash = 5000
        state5['players'][0].tiles = [
            {"row": "A", "column": "3"},
            {"row": "F", "column": "3"},
            {"row": "D", "column": "3"},
            {"row": "D", "column": "4"},
            {"row": "G", "column": "8"},
            {"row": "H", "column": "2"},
        ]
        state5['players'][0].shares = [
            {"share": "American", "count": 33}
        ]
        
        
        expected_output = {'error':'The current player already has 25 shares of American'}
        result, output = self.acquire.validate_state(state5)
        self.assertEqual(output, expected_output)
        
        
        state6 = {
            "board": self.acquire.state['board'],
            "players": [HumanPlayer("Aditya")]
        }
        state6['players'][0].cash = 5000
        state6['players'][0].tiles = [
            {"row": "A", "column": "3"},
            {"row": "F", "column": "3"},
            {"row": "D", "column": "3"},
            {"row": "D", "column": "4"},
            {"row": "G", "column": "8"},
            {"row": "H", "column": "2"},
        ]
        state6['players'][0].shares = [
            {"share": "Davis", "count": 3}
        ]
        expected_output = {'error':'The current player shares label Davis is not valid'}
        result, output = self.acquire.validate_state(state6)
        self.assertEqual(output, expected_output)
        
        
        state7 = {
            "board": self.acquire.state['board'],
            "players": [HumanPlayer("Aditya")]
        }
        state7['players'][0].cash = 5000
        state7['players'][0].tiles = [
            {"row": "A", "column": "3"},
            {"row": "F", "column": "3"},
            {"row": "G", "column": "8"},
            {"row": "G", "column": "8"},
            {"row": "H", "column": "2"},
            {"row": "F", "column": "10"},
        ]
        state7['players'][0].shares = [
            {"share": "American", "count": 3}
        ]
        expected_output = {'error':"Tile {'row': 'G', 'column': '8'} is not unique for current player"}
        result, output = self.acquire.validate_state(state7)
        self.assertEqual(output, expected_output)
        
        
        board = {
                    "tiles": [
                        {"row":"G", "column":"8"}
                    ],
                    "hotels": [
                    ],
                }
        self.acquire.state['board'].tiles = board['tiles']
        self.acquire.state['board'].hotels = board['hotels']

        state8 = {
            "board": self.acquire.state['board'],
            "players": [HumanPlayer("Aditya")]
        }
        state8['players'][0].cash = 5000
        state8['players'][0].tiles = [
            {"row": "A", "column": "3"},
            {"row": "F", "column": "3"},
            {"row": "G", "column": "8"},
            {"row": "H", "column": "2"},
            {"row": "F", "column": "10"},
        ]
        state8['players'][0].shares = [
            {"share": "American", "count": 3}
        ]
        expected_output = {'error':'The player already has a tile in the board'}
        result, output = self.acquire.validate_state(state8)
        self.assertEqual(output, expected_output)
        

    def test_handle_query(self):
        request = {
            "request":"query",
            "row":"A",
            "column":"1",
            "board":
                {
                    "tiles": [
                        { "row": "A", "column": "1" },
                        { "row": "A", "column": "2" },
                        { "row": "C", "column": "3" },
                        { "row": "C", "column": "4" },
                        { "row": "D", "column": "7" }
                    ],
                    "hotels": [
                        {
                        "hotel": "American",
                        "tiles": [
                            { "row": "C", "column": "3" },
                            { "row": "C", "column": "4" }
                        ]
                        }
                    ]
                    }
        }
        expected_output = {
            'error' : 'A tile already exists at the desired location'
        }
        boardMatrix = create_test_boardMatrix(request['board'])
        result, output = self.acquire.handle_query(request, boardMatrix)
        self.assertFalse(result)
        self.assertEqual(output, expected_output)


    def test_singleton(self):
        board1 = {
                "tiles":[
                    {
                        "row":"B",
                        "column":"2"
                    },
                    {
                        "row":"B",
                        "column":"3"
                    },
                    {
                        "row":"B",
                        "column":"4"
                    }
                ],
                "hotels":[]
            }
        
        self.acquire.state['board'].tiles = board1['tiles']
        self.acquire.state['board'].hotels = board1['hotels']
        boardMatrix = create_test_boardMatrix(board1)
        request = {
            "request":"singleton",
            "row":"C",
            "column":"3",
            "board":self.acquire.state['board']
        }
        expected_output = Error('Other Operation').message
        output = self.acquire.handle_singleton(request, boardMatrix)
        self.assertEqual(output.message, expected_output)


        board2 = {
        "tiles":[
            {
                "row":"A",
                "column":"1"
            },
            {
                "row":"A",
                "column":"2"
            },
            {
                "row":"C",
                "column":"1"
            },
            {
                "row":"C",
                "column":"2"
            },
            {
                "row":"C",
                "column":"12"
            },
            {
                "row":"E",
                "column":"1"
            },
            {
                "row":"E",
                "column":"2"
            },
            {
                "row":"G",
                "column":"1"
            },
            {
                "row":"G",
                "column":"2"
            },
            {
                "row":"A",
                "column":"5"
            },
            {
                "row":"B",
                "column":"5"
            },
            {
                "row":"D",
                "column":"5"
            },
            {
                "row":"E",
                "column":"5"
            },
            {
                "row":"H",
                "column":"10"
            },
            {
                "row":"I",
                "column":"10"
            }
        ],
        "hotels":[
            {
            "hotel":"Festival",
            "tiles":[
                {
                    "row":"A",
                    "column":"1"
                },
                {
                    "row":"A",
                    "column":"2"
                }
            ]
        },

        {
            "hotel":"Worldwide",
            "tiles":[
                {
                    "row":"C",
                    "column":"1"
                },
                {
                    "row":"C",
                    "column":"2"
                }
            ]
        },

        {
            "hotel":"Tower",
            "tiles":[
                {
                    "row":"E",
                    "column":"1"
                },
                {
                    "row":"E",
                    "column":"2"
                }
            ]
        },

        {
            "hotel":"Imperial",
            "tiles":[
                {
                    "row":"G",
                    "column":"1"
                },
                {
                    "row":"G",
                    "column":"2"
                }
            ]
        },

        {
            "hotel":"Continental",
            "tiles":[
                {
                    "row":"A",
                    "column":"5"
                },
                {
                    "row":"B",
                    "column":"5"
                }
            ]
        },

        {
            "hotel":"Sackson",
            "tiles":[
                {
                    "row":"D",
                    "column":"5"
                },
                {
                    "row":"E",
                    "column":"5"
                }
            ]
        },

        {
            "hotel":"American",
            "tiles":[
                {
                    "row":"H",
                    "column":"10"
                },
                {
                    "row":"I",
                    "column":"10"
                }
            ]
        }
        ]
}
        
        self.acquire.state['board'].tiles = board2['tiles']
        self.acquire.state['board'].hotels = board2['hotels']
        boardMatrix = create_test_boardMatrix(board2)
        request = {
            "request":"singleton",
            "row":"C",
            "column":"11",
            "board":self.acquire.state['board']
        }
        expected_output = {'singleton':None}
        output = self.acquire.handle_singleton(request, boardMatrix)
        self.assertEqual(output, expected_output)


    def test_founding(self):
        board1 = {
                "tiles":[
                    {
                        "row":"A",
                        "column":"2"
                    },
                    {
                        "row":"C",
                        "column":"2"
                    }
                ],
                "hotels": [
                    {
                    "hotel":'American',
                    "tiles":[
                        {
                            "row":"A",
                            "column":"4"
                        },
                        {
                            "row":"B",
                            "column":"4"
                        },
                        {
                            "row":"C",
                            "column":"4"
                        }
                    ]
                    }

                ]
            }
        
        self.acquire.state['board'].tiles = board1['tiles']
        self.acquire.state['board'].hotels = board1['hotels']
        boardMatrix = create_test_boardMatrix(board1)
        request = {
            "request":"founding",
            "row":"B",
            "column":"2",
            "hotel":"American",
            "board":self.acquire.state['board']
        }
        expected_output = Error('A hotel with that label already exists').message
        output = self.acquire.handle_founding(request, boardMatrix)
        self.assertEqual(output.message, expected_output)

        board2 = {
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
        "column": "2"
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
      }
    ]
  }
        
        self.acquire.state['board'].tiles = board2['tiles']
        self.acquire.state['board'].hotels = board2['hotels']
        boardMatrix = create_test_boardMatrix(board2)
        request = {
            "request":"founding",
            "row":"B",
            "column":"4",
            "hotel":"American",
            "board":self.acquire.state['board']
        }
        expected_output = {'founding':'American'}
        output = self.acquire.handle_founding(request, boardMatrix)
        self.assertEqual(output, expected_output)


    def test_growing(self):
        board1 = {
                "tiles":[
                    {
                        "row":"A",
                        "column":"2"
                    },
                    {
                        "row":"A",
                        "column":"1"
                    },
                     {
                        "row":"B",
                        "column":"3"
                    },
                    {
                        "row":"C",
                        "column":"3"
                    }
                ],
                "hotels": [
                    {
                    "hotel":'American',
                    "tiles":[
                        {
                            "row":"A",
                            "column":"2"
                        },
                        {
                            "row":"A",
                            "column":"1"
                        }
                    ]
                    },

                    {
                        "hotel":"Sackson",
                        "tiles":[
                            {
                            "row":"B",
                            "column":"3"
                        },
                        {
                            "row":"C",
                            "column":"3"
                        }
                        ]
                    }

                ]
            }
        
        self.acquire.state['board'].tiles = board1['tiles']
        self.acquire.state['board'].hotels = board1['hotels']
        boardMatrix = create_test_boardMatrix(board1)
        request = {
            "request":"growing",
            "row":"B",
            "column":"2",
            "board":self.acquire.state['board']
        }
        expected_output = Error('A merger would take place').message
        output = self.acquire.handle_growing(request, boardMatrix)
        self.assertEqual(output.message, expected_output)


        board2 = {
            "tiles":[
                    {
                        "row":"A",
                        "column":"2"
                    },
                     {
                        "row":"B",
                        "column":"3"
                    },
                    {
                        "row":"D",
                        "column":"2"
                    }
                ],
                "hotels":[]
        }

        self.acquire.state['board'].tiles = board2['tiles']
        self.acquire.state['board'].hotels = board2['hotels']
        boardMatrix = create_test_boardMatrix(board2)
        request = {
            "request":"growing",
            "row":"B",
            "column":"2",
            "board":self.acquire.state['board']
        }
        expected_output = Error('No hotel found').message
        output = self.acquire.handle_growing(request, boardMatrix)
        self.assertEqual(output.message, expected_output)


    def test_merging(self):
        board1 = {
    "tiles": [
      {
        "row": "B",
        "column": "2"
      },
      {
        "row": "C",
        "column": "1"
      },
      {
        "row": "D",
        "column": "6"
      },
      {
        "row": "D",
        "column": "5"
      },
      {
        "row": "C",
        "column": "6"
      },
      {
        "row": "C",
        "column": "5"
      },
      {
        "row": "C",
        "column": "4"
      },
      {
        "row": "B",
        "column": "6"
      },
      {
        "row": "B",
        "column": "5"
      },
      {
        "row": "B",
        "column": "4"
      },
      {
        "row": "A",
        "column": "4"
      },
      {
        "row": "A",
        "column": "5"
      },
      {
        "row": "A",
        "column": "6"
      },
      {
        "row": "D",
        "column": "2"
      },
      {
        "row": "D",
        "column": "3"
      },
      {
        "row": "E",
        "column": "4"
      },
      {
        "row": "E",
        "column": "5"
      },
      {
        "row": "E",
        "column": "6"
      },
      {
        "row": "F",
        "column": "2"
      },
      {
        "row": "F",
        "column": "3"
      },
      {
        "row": "F",
        "column": "4"
      },
      {
        "row": "F",
        "column": "5"
      },
      {
        "row": "F",
        "column": "6"
      },
      {
        "row": "G",
        "column": "2"
      },
      {
        "row": "G",
        "column": "3"
      },
      {
        "row": "G",
        "column": "4"
      },
      {
        "row": "G",
        "column": "5"
      },
      {
        "row": "G",
        "column": "6"
      }
    ],
    "hotels": [
      {
        "hotel": "American",
        "tiles": [
          {
            "row": "D",
            "column": "2"
          },
          {
            "row": "D",
            "column": "3"
          }
        ]
      },
      {
        "hotel": "Continental",
        "tiles": [
          {
            "row": "E",
            "column": "4"
          },
          {
            "row": "E",
            "column": "5"
          },
          {
            "row": "E",
            "column": "6"
          },
          {
            "row": "F",
            "column": "2"
          },
          {
            "row": "F",
            "column": "3"
          },
          {
            "row": "F",
            "column": "4"
          },
          {
            "row": "F",
            "column": "5"
          },
          {
            "row": "F",
            "column": "6"
          },
          {
            "row": "G",
            "column": "2"
          },
          {
            "row": "G",
            "column": "3"
          },
          {
            "row": "G",
            "column": "4"
          },
          {
            "row": "G",
            "column": "5"
          },
          {
            "row": "G",
            "column": "6"
          }
        ]
      },
      {
        "hotel": "Festival",
        "tiles": [
          {
            "row": "C",
            "column": "6"
          },
          {
            "row": "C",
            "column": "5"
          },
          {
            "row": "C",
            "column": "4"
          },
          {
            "row": "B",
            "column": "6"
          },
          {
            "row": "B",
            "column": "5"
          },
          {
            "row": "B",
            "column": "4"
          },
          {
            "row": "A",
            "column": "4"
          },
          {
            "row": "A",
            "column": "5"
          },
          {
            "row": "A",
            "column": "6"
          }
        ]
      }
    ]
  }
        self.acquire.state['board'].tiles = board1['tiles']
        self.acquire.state['board'].hotels = board1['hotels']
        boardMatrix = create_test_boardMatrix(board1)
        request = {
            "request":"merging",
            "row":"D",
            "column":"4",
            "hotel":"Continental",
            "board":self.acquire.state['board']
        }
        expected_output = Error('Hotel has chain length of atleast 11').message
        output = self.acquire.handle_merging(request, boardMatrix)
        self.assertEqual(output.message, expected_output)
        
        
        
        board2 = {
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
        
        self.acquire.state['board'].tiles = board2['tiles']
        self.acquire.state['board'].hotels = board2['hotels']
        boardMatrix = create_test_boardMatrix(board2)
        request = {
            "request":"merging",
            "row":"D",
            "column":"4",
            "hotel":"Continental",
            "board":self.acquire.state['board']
        }
        expected_output = Error('Only one hotel to merge').message
        output = self.acquire.handle_merging(request, boardMatrix)
        self.assertEqual(output.message, expected_output)

if __name__ == "__main__":
    unittest.main()
