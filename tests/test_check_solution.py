import unittest
from src.models import AnchorVariantsResolver, Rectangle, SolvingGrid, Anchor, SolutionChecker


class MyTestCase(unittest.TestCase):
    def test_trivial_true(self):
        k = SolutionChecker([Anchor(0, 0, 0, 4)], [Rectangle(0, 0, 2, 2)], 2)
        self.assertEqual(k.check(), True)

    def test_trivial_multiple_true(self):
        k = SolutionChecker([Anchor(0, 0, 0, 2), Anchor(1, 1, 0, 2)], [Rectangle(0, 0, 1, 2), Rectangle(1, 0, 1, 2)], 2)
        self.assertEqual(k.check(), True)

    def test_trivial_false(self):
        k = SolutionChecker([Anchor(0, 0, 0, 2)], [Rectangle(0, 0, 2, 1)], 2)
        self.assertEqual(k.check(), False)

    def test_overlap(self):
        k = SolutionChecker([Anchor(0, 0, 0, 2)], [Rectangle(0, 0, 2, 1),Rectangle(0, 0, 2, 2)], 2)
        self.assertEqual(k.check(), False)


if __name__ == '__main__':
    unittest.main()
