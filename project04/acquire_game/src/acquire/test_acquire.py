import unittest
import os
import json
from acquire import Acquire
from error import Error


def readJsonRequest(filepath):
    try:
        script_dir = os.getcwd()
        absolute_path = os.path.join(script_dir, filepath)

        with open(absolute_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data
        
    except Exception as e:
        return Error('Error while parsing json data.')

class Test(unittest.TestCase):
    def setUp(self):
        self.folder_path = '../../tests/board-tests/Input/'
        self.output_path = '../../tests/board-tests/Output/'
        if os.path.exists(self.folder_path):
            self.file_list = [f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))]
            self.file_list.sort()
            self.responses = []
            for file in self.file_list:
                request = readJsonRequest(os.path.join(self.folder_path, file))
                if type(request) != Error:
                    acquire = Acquire(request)
                    board_instance = acquire.get_board()
                    is_valid, message = acquire.validate_board(board_instance)
                    if is_valid:
                        try:
                            board = board_instance.create_board()
                            response = acquire.handle_request(request, board)
                            self.responses.append(response)
                        except Exception as e:
                            self.responses.append(Error(str(e)).to_dict())
                    else:
                        self.responses.append(message)


    def test_responses(self):
        for i in range(len(self.responses)):
            print(i, self.responses[i])
            with self.subTest(f'Testing response for file {self.file_list[i]}'):
                if isinstance(self.responses[i], Error):
                    self.fail(f'Error in processing request: {self.responses[i]}')
                else:
                    output_file = os.path.join(self.output_path, f'out{i}.json')
                    print('output_file',output_file)
                    with open(output_file, 'r', encoding='utf-8') as json_file:
                        expected_output = json.load(json_file)
                    self.assertEqual(self.responses[i], expected_output)
                    

if __name__ == '__main__':
    unittest.main()
