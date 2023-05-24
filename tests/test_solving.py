import unittest
from src.models import AnchorVariantsResolver, Rectangle, SolvingGrid, Anchor
from src.solution import BoardSolution
from src.models import AnchorsFileReader


class SolverTest(unittest.TestCase):
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

    def test_collide(self):
        rect = Rectangle(3, 0, 1, 3)

        for x, y in self.grid.collideAll(rect):
            self.grid.mark_occupied(x, y)
        self.assertEqual(
            [self.grid.is_cell_occupied(3, 0),
             self.grid.is_cell_occupied(3, 1),
             self.grid.is_cell_occupied(3, 2)],
            [1, 1, 1])

    def test_rect_resolving(self):
        ans = BoardSolution(self.table).solve()

        z = sorted([Rectangle(x=3, y=3, width=2, height=1),
                    Rectangle(x=0, y=0, width=2, height=1),
                    Rectangle(x=1, y=1, width=1, height=3),
                    Rectangle(x=0, y=1, width=1, height=4),
                    Rectangle(x=1, y=4, width=4, height=1),
                    Rectangle(x=2, y=0, width=1, height=4),
                    Rectangle(x=4, y=0, width=1, height=2),
                    Rectangle(x=3, y=0, width=1, height=2),
                    Rectangle(x=3, y=2, width=2, height=1)],
                   key=lambda rect: (rect.x, rect.y, rect.width, rect.height))

        self.assertEqual(ans, z)

    def test_get_rectangle_variants(self):
        table = AnchorsFileReader(
            '2 0 0 0\n'
            '0 0 0 0\n'
            '0 0 0 0\n'
            '0 0 0 4\n'
        )
        ancs = [
            Anchor(0, 0, 0, 2),
            Anchor(3, 3, 1, 4)
        ]

        grid = SolvingGrid(table.size, ancs)
        grid.mark_occupied(3, 1)
        resolvers = [
            AnchorVariantsResolver(ancs[0], grid),
            AnchorVariantsResolver(ancs[1], grid)
        ]
        for i in resolvers:
            i.get_rectangle_variants()
        self.assertEqual(resolvers[0].variants,
                         [Rectangle(0, 0, 1, 2), Rectangle(0, 0, 2, 1)])
        self.assertEqual(resolvers[1].variants,
                         [Rectangle(2, 2, 2, 2), Rectangle(0, 3, 4, 1)])

    def test_search_responsible_points(self):
        solvers = [AnchorVariantsResolver(i, self.grid) for i in self.ancs]
        for i in solvers:
            i.mark_reachable()
        an = self.grid.get_anchors_that_reach_cell(4, 3)
        self.assertEqual(an, [Anchor(3, 3, 7, 2)])

    def test_filter_existing_variants(self):
        solvers = [AnchorVariantsResolver(i, self.grid) for i in self.ancs]
        for i in solvers:
            i.get_rectangle_variants()
        for i in solvers:
            i.filter_existing_variants()
        self.assertEqual(solvers[4].variants, [Rectangle(2, 0, 1, 4)])


if __name__ == '__main__':
    unittest.main()
