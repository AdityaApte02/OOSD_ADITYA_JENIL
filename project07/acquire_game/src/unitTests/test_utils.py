import sys
sys.path.append(r'C:\Users\Aditya\OOSD_Pair1\project07\acquire_game\src')
import unittest
from  acquire.utils import matrix_to_object


class TestUtils(unittest.TestCase):
    def test_matrix_to_object_empty_board(self):
        board = [["0"] * 12 for _ in range(9)]
        expected_state = {"state": {"board": {"tiles": [], "hotels": []}}}
        self.assertEqual(matrix_to_object(board), expected_state)

    def test_matrix_to_object_single_tile(self):
        board = [["0"] * 12 for _ in range(9)]
        board[0][0] = "1"
        expected_state = {
            "state": {"board": {"tiles": [{"row": "A", "column": "1"}], "hotels": []}}
        }
        self.assertEqual(matrix_to_object(board), expected_state)

    def test_matrix_to_object_multiple_tiles(self):
        board = [["0"] * 12 for _ in range(9)]
        board[0][0] = "1"
        board[1][1] = "1"
        expected_state = {
            "state": {
                "board": {
                    "tiles": [{"row": "A", "column": "1"}, {"row": "B", "column": "2"}],
                    "hotels": [],
                }
            }
        }
        self.assertEqual(matrix_to_object(board), expected_state)

    def test_matrix_to_object_with_hotels(self):
        board = [["0"] * 12 for _ in range(9)]
        board[0][0] = "American"
        board[0][1] = "American"
        board[1][0] = "Continental"
        expected_state = {
            "state": {
                "board": {
                    "tiles": [
                        {"row": "A", "column": "1"},
                        {"row": "A", "column": "2"},
                        {"row": "B", "column": "1"},
                    ],
                    "hotels": [
                        {
                            "hotel": "American",
                            "tiles": [
                                {"row": "A", "column": "1"},
                                {"row": "A", "column": "2"},
                            ],
                        },
                        {
                            "hotel": "Continental",
                            "tiles": [{"row": "B", "column": "1"}],
                        },
                    ],
                }
            }
        }
        self.assertEqual(matrix_to_object(board), expected_state)


if __name__ == "__main__":
    unittest.main()
