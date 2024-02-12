import os
import json
import sys
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


if __name__ == "__main__":
    filename = sys.argv[1]
    request = readJsonRequest(filename)
    if type(request) != Error:
        acquire = Acquire(request)
        board_instance = acquire.get_board()
        is_valid, message = acquire.validate_board(board_instance)
        if is_valid:
            try:
                board = board_instance.create_board()
                response = acquire.handle_request(request, board)
                print(response)
            except Exception as e:
                print(Error(str(e)).to_dict())
        else:
            print(message.to_dict())