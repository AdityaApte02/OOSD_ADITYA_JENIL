import sys
sys.path.append("..")
import unittest
from error import Error

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