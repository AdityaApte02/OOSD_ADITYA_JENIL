# test file to test the board representation
# import required libraries
import os
import json
from unittest import TestCase, main

# import acquire class from acquire module
from acquire import Acquire

class TestBoard(TestCase):
    def _set_up(self, file):
        request = self.get_file_content(file)
        self.acquire = Acquire(request)
        self.board_instance = self.acquire.get_board()
    
    def get_file_content(self, file):
        script_dir = os.getcwd()
        absolute_path = os.path.join(script_dir, file)
        with open(absolute_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)

    def test_validate_board(self):
        file = os.path.join(os.getcwd(), 'acquire_game/tests/part1-tests/in0.json')
        self._set_up(file)
        _, message = self.acquire.validate_board(self.board_instance)
        output_file = os.path.join(os.getcwd(), 'acquire_game/tests/part1-tests/out0.json')
        expected = self.get_file_content(output_file)
        self.assertEqual(message, expected)
    
    def test_valid_placement(self):
        file = os.path.join(os.getcwd(), 'acquire_game/tests/part1-tests/in1.json')
        self._set_up(file)
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
        file = os.path.join(os.getcwd(), 'acquire_game/tests/part1-tests/in2.json')
        self._set_up(file)
        _, message = self.acquire.validate_board(self.board_instance)
        output_file = os.path.join(os.getcwd(), 'acquire_game/tests/part1-tests/out2.json')
        expected = self.get_file_content(output_file)
        self.assertEqual(message, expected)

    def test_duplicate_tiles(self):
        file = os.path.join(os.getcwd(), 'acquire_game/tests/part1-tests/in3.json')
        self._set_up(file)
        _, message = self.acquire.validate_board(self.board_instance)
        output_file = os.path.join(os.getcwd(), 'acquire_game/tests/part1-tests/out3.json')
        expected = self.get_file_content(output_file)
        self.assertEqual(message, expected)

    def test_duplicate_hotel_tiles(self):
        file = os.path.join(os.getcwd(), 'acquire_game/tests/part1-tests/in4.json')
        self._set_up(file)
        _, message = self.acquire.validate_board(self.board_instance)
        output_file = os.path.join(os.getcwd(), 'acquire_game/tests/part1-tests/out4.json')
        expected = self.get_file_content(output_file)
        self.assertEqual(message, expected)

    def test_tiles_within_board(self):
        file = os.path.join(os.getcwd(), 'acquire_game/tests/part1-tests/in5.json')
        self._set_up(file)
        _, message = self.acquire.validate_board(self.board_instance)
        output_file = os.path.join(os.getcwd(), 'acquire_game/tests/part1-tests/out5.json')
        expected = self.get_file_content(output_file)
        self.assertEqual(message, expected)

    def test_hotel_tiles_within_board(self):
        file = os.path.join(os.getcwd(), 'acquire_game/tests/part1-tests/in6.json')
        self._set_up(file)
        _, message = self.acquire.validate_board(self.board_instance)
        output_file = os.path.join(os.getcwd(), 'acquire_game/tests/part1-tests/out6.json')
        expected = self.get_file_content(output_file)
        self.assertEqual(message, expected)

    def test_hotel_chain_size(self):
        file = os.path.join(os.getcwd(), 'acquire_game/tests/part1-tests/in7.json')
        self._set_up(file)
        _, message = self.acquire.validate_board(self.board_instance)
        output_file = os.path.join(os.getcwd(), 'acquire_game/tests/part1-tests/out7.json')
        expected = self.get_file_content(output_file)
        self.assertEqual(message, expected)

    def test_hotel_tiles_are_in_board_tiles(self):
        file = os.path.join(os.getcwd(), 'acquire_game/tests/part1-tests/in8.json')
        self._set_up(file)
        _, message = self.acquire.validate_board(self.board_instance)
        output_file = os.path.join(os.getcwd(), 'acquire_game/tests/part1-tests/out8.json')
        expected = self.get_file_content(output_file)
        self.assertEqual(message, expected)

    def test_hotel_tiles_are_connected(self):
        file = os.path.join(os.getcwd(), 'acquire_game/tests/part1-tests/in9.json')
        self._set_up(file)
        _, message = self.acquire.validate_board(self.board_instance)
        output_file = os.path.join(os.getcwd(), 'acquire_game/tests/part1-tests/out9.json')
        expected = self.get_file_content(output_file)
        self.assertEqual(message, expected)





if __name__ == "__main__":
    main()