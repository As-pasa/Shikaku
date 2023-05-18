import time

from models import SolvingGrid
from models import AnchorsFileReader
from models import AnchorVariantsResolver


class BoardSolution:
    """Класс, решающий доску с головоломкой Shikaku"""
    def __init__(self, table: AnchorsFileReader):
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
            for solver in solvers + finalized:
                solver.mark_reachable()

            for solver in solvers:
                rects = solver.filter_existing_variants()
                solver.variants = rects
                if len(rects) == 1:
                    finalized.append(solver)
                    solvers.remove(solver)
            self.grid.clear_all_reachable()

        for i in range(len(finalized)):
            self.rectangles += finalized[i].variants
        return sorted(self.rectangles, key=lambda rect: (
        rect.x, rect.y, rect.width, rect.height))

    def print_solution(self):
        rects = self.solve()
        solve_grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        n = 1
        for rect in rects:
            for i in range(rect.x, rect.x + rect.width):
                for j in range(rect.y, rect.y + rect.height):
                    solve_grid[j][i] = n
            n += 1
        res = ''
        for line in solve_grid:
            if len(rects) < 10:
                res += f'{" ".join(map(str, line))}\n'
            else:
                for cell in line:
                    res += f'{cell} ' if len(str(cell)) > 1 else f'0{cell} '
                res = res[:-1] + '\n'
        return print(res)
