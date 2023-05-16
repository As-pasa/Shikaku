import unittest
from models import Anchor, AnchorVariantsResolver, Rectangle, SolvingGrid


# from ..models import Anchor, AnchorVariantsResolver, Rectangle, SolvingGrid


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.ancs = [
            Anchor(0, 0, 2),
            Anchor(1, 0, 4),
            Anchor(1, 1, 3),
            Anchor(4, 1, 4),
            Anchor(0, 2, 4),
            Anchor(1, 3, 2),
            Anchor(2, 3, 2),
            Anchor(3, 3, 2),
            Anchor(1, 4, 2)
        ]
        self.grid = SolvingGrid(5, self.ancs)

    def test_something(self):

        singles = []
        for i in self.ancs:
            solver = AnchorVariantsResolver(i, self.grid)
            solver.variants = solver.get_rectangle_variants()
            if len(solver.variants) == 1:
                singles.append(solver.anchor)

        self.assertEqual(singles, [self.ancs[0], self.ancs[1]])  # add assertion here

    def test_collide(self):
        rect = Rectangle(3, 0, 1, 3)

        for x, y in self.grid.collideAll(rect):
            self.grid.mark_occupied(x, y)
        self.assertEqual(
            [self.grid.is_cell_occupied(3, 0), self.grid.is_cell_occupied(3, 1), self.grid.is_cell_occupied(3, 2)],
            [1, 1, 1])


    def test_rect_resolving(self):
        solvers = []
        finalized = []
        for i in self.ancs:
            solver = AnchorVariantsResolver(i, self.grid)
            solver.variants = solver.get_rectangle_variants()

            solvers.append(solver)
        while solvers:
            for solver in solvers:
                rects = solver.filter_existing_variants()
                solver.variants = rects
                if len(rects) == 1:
                    for x, y, in self.grid.collideAll(rects[0]):
                        self.grid.mark_occupied(x, y)
                    finalized.append(solver)
                    solvers.remove(solver)
        ans = []
        for i in range(len(finalized)):
            ans += finalized[i].variants
        self.assertEqual(ans, [Rectangle(x=0, y=0, width=1, height=2), Rectangle(x=1, y=1, width=3, height=1),
                               Rectangle(x=0, y=2, width=4, height=1), Rectangle(x=2, y=3, width=1, height=2),
                               Rectangle(x=0, y=4, width=2, height=1), Rectangle(x=1, y=0, width=4, height=1),
                               Rectangle(x=0, y=3, width=2, height=1), Rectangle(x=4, y=1, width=1, height=4),
                               Rectangle(x=3, y=3, width=1, height=2)])


if __name__ == '__main__':
    unittest.main()
