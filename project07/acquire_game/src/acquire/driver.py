import os
import json
import sys
from acquire.acquire import Acquire
from acquire.error import Error
from acquire.admin import Admin

def readJsonRequest(filepath):
    try:
        script_dir = os.getcwd()
        absolute_path = os.path.join(script_dir, filepath)
        with open(absolute_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data
    except Exception as e:
        return Error('Error while parsing json data.').to_dict()


if __name__ == "__main__":
    filename = sys.argv[1]
    request = readJsonRequest(filename)
    if type(request) != Error:
        admin = Admin()
        if (request.get("request") == None):
            is_valid = False
            response = Error("Invalid request").to_dict()
        elif(request["request"] == "setup"):
            is_valid, response = admin.setUp(request)
        elif (request["request"] == "place"):
            is_valid, response = admin.place(request, True)
        elif (request["request"] == "buy"):
            is_valid, response = admin.buy(request)
        elif (request["request"] == "done"):
            is_valid, response = admin.done(request)
        else:
            is_valid = False
            response = Error("Invalid request").to_dict()
        if is_valid:
                print(response)
        else:
            print(response)