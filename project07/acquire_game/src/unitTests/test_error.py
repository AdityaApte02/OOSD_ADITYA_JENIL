import sys
sys.path.append(r'C:\Users\Aditya\OOSD_Pair1\project07\acquire_game\src')
import unittest
from  acquire.error import Error

class TestError(unittest.TestCase):
    def test_error_message(self):
        error_message = "This is an error message"
        error = Error(error_message)
        self.assertEqual(error.message, error_message)

    def test_error_to_dict(self):
        error_message = "This is an error message"
        error = Error(error_message)
        error_dict = error.to_dict()
        self.assertEqual(error_dict, {"error": error_message})

if __name__ == "__main__":
    unittest.main()