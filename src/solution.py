import time

from models import SolvingGrid
from models import AnchorTable
from models import AnchorVariantsResolver


class BoardSolution:
    def __init__(self, table: AnchorTable):
        self.anchors = table.anchors
        self.size = table.size
        self.grid = SolvingGrid(self.size, self.anchors)
        self.rectangles = []

    def solve(self):
        solvers = []
        finalized = []
        for i in self.anchors:
            solver = AnchorVariantsResolver(i, self.grid)
            solver.variants = solver.get_rectangle_variants()
            solvers.append(solver)

        while solvers:
            self.grid.print()
            for solver in solvers:

                rects = solver.filter_existing_variants()

                solver.variants = rects
                if len(rects) == 1:
                    for x, y, in self.grid.collideAll(rects[0]):
                        self.grid.mark_occupied(x, y)
                    finalized.append(solver)
                    solvers.remove(solver)

        for i in range(len(finalized)):
            self.rectangles += finalized[i].variants
        return sorted(self.rectangles, key=lambda rect: rect.x)

    def print_solution(self):
        rects = self.solve()
        solve_grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        n = 1
        for rect in rects:
            for i in range(rect.x, rect.x + rect.width):
                for j in range(rect.y, rect.y + rect.height):
                    solve_grid[i][j] = n
            n += 1
        res = ''
        for line in solve_grid:
            res += f'{" ".join(map(str, line))}\n'
        return print(res)
