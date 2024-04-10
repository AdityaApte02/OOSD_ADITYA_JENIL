import sys
sys.path.append("..")
import unittest
from unittest import TestCase
from unittest.mock import patch
from admin import Admin
from acquire import Acquire
from board import Board
from driver import TestDriver

class TestStates(TestCase):
    def _set_up(self, request):
        self.driver = TestDriver(request)


