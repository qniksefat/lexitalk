import sys
sys.path.append('/Users/qasem/PycharmProjects/lexitalk/')

import unittest
from datetime import time
from core.st_utils import convert_timestamp_str_to_seconds, parse_timestamp


class TestUtils(unittest.TestCase):
    def test_convert_timestamp_str_to_seconds(self):
        self.assertEqual(convert_timestamp_str_to_seconds("0:0:0.000"), 0)
        self.assertEqual(convert_timestamp_str_to_seconds("1:0:0.000"), 3600)
        self.assertEqual(convert_timestamp_str_to_seconds("0:1:0.000"), 60)
        self.assertEqual(convert_timestamp_str_to_seconds("0:0:1.000"), 1)
        self.assertEqual(convert_timestamp_str_to_seconds("2:20:23.560"), 8423)
        self.assertEqual(convert_timestamp_str_to_seconds("0:0:0"), 0)
        self.assertEqual(convert_timestamp_str_to_seconds("1:0:0"), 3600)
        self.assertEqual(convert_timestamp_str_to_seconds("1:03:0"), 3780)
        
    def test_parse_timestamp(self):
        self.assertEqual(parse_timestamp("2:20:23.560"), time(hour=2, minute=20, second=23, microsecond=560000))
        self.assertEqual(parse_timestamp("0:0:0.000"), time(hour=0, minute=0, second=0, microsecond=0))
        self.assertEqual(parse_timestamp("1:0:0"), time(hour=1, minute=0, second=0))
        self.assertEqual(parse_timestamp("0:1:45"), time(hour=0, minute=1, second=45))
        
if __name__ == '__main__':
    unittest.main()
    