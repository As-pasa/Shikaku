import unittest
from src.models import AnchorVariantsResolver, Rectangle, SolvingGrid
from src.solution import BoardSolution
from src.models import AnchorsFileReader


# from ..models import Anchor, AnchorVariantsResolver, Rectangle, SolvingGrid


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.table = AnchorsFileReader(
            '2 0 4 0 0\n'
            '4 3 0 2 2\n'
            '0 0 0 2 0\n'
            '0 0 0 2 0\n'
            '0 4 0 0 0'
        )
        self.ancs = self.table.anchors
        self.grid = SolvingGrid(self.table.size, self.ancs)

    def test_something(self):
        singles = []
        for i in self.ancs:
            solver = AnchorVariantsResolver(i, self.grid)
            solver.variants = solver.get_rectangle_variants()
            if len(solver.variants) == 1:
                singles.append(solver.anchor)

        self.assertEqual(singles, [self.ancs[0], self.ancs[2]])  # add assertion here

    def test_collide(self):
        rect = Rectangle(3, 0, 1, 3)

        for x, y in self.grid.collideAll(rect):
            self.grid.mark_occupied(x, y)
        self.assertEqual(
            [self.grid.is_cell_occupied(3, 0), self.grid.is_cell_occupied(3, 1), self.grid.is_cell_occupied(3, 2)],
            [1, 1, 1])

    def test_rect_resolving(self):

        ans = BoardSolution(self.table).solve()
        b = BoardSolution(self.table).print_solution()

        z=sorted([Rectangle(x=3, y=3, width=2, height=1),
                                    Rectangle(x=0, y=0, width=2, height=1),
                                    Rectangle(x=1, y=1, width=1, height=3),
                                    Rectangle(x=0, y=1, width=1, height=4),
                                    Rectangle(x=1, y=4, width=4, height=1),
                                    Rectangle(x=2, y=0, width=1, height=4),
                                    Rectangle(x=4, y=0, width=1, height=2),
                                    Rectangle(x=3, y=0, width=1, height=2),
                                    Rectangle(x=3, y=2, width=2, height=1)], key=lambda rect: (rect.x,rect.y,rect.width,rect.height))

        self.assertEqual(ans, z)


if __name__ == '__main__':

    unittest.main()
