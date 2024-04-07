import unittest
from admin import Admin
from acquire import Acquire
from error import Error
from board import Board
from driver import TestDriver
import json
import os

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
        self.folder_path = '../player-tests/Input/'
        self.output_path = '../player-tests/Output/'
        if os.path.exists(self.folder_path):
            print('folder_path',self.folder_path)
            self.file_list = [f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))]
            self.file_list.sort()
            self.responses = []
            for file in self.file_list:
                request = readJsonRequest(os.path.join(self.folder_path, file))
                if type(request) != Error:
                    testDriver = TestDriver(request)
                    response = testDriver.handleRequest()
                    self.responses.append(response)


    def test_responses(self):
        self.maxDiff = None
        for i in range(len(self.responses)):
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