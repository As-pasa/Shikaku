import unittest
from src.check_files import *


class ChecksTest(unittest.TestCase):
    def test_content(self):
        grid = 'a 0 2\n' \
               '0 0 0\n' \
               '3 0 2'
        self.assertEqual(check_file_content(grid), False)

    def test_max(self):
        grid = '10 0 2\n' \
               '0 0 0\n' \
               '3 0 2'
        self.assertEqual(check_max_element(grid), False)


if __name__ == '__main__':
    unittest.main()
