from src.models import SolvingGrid
from src.models import AnchorTable
from src.models import AnchorVariantsResolver


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
        pass
        # rects = self.solve()
        # solve_grid = [[0 for x in range(self.size)] for y in range(self.size)]
        # n = 1
        # for rect in rects:
        #     for i in range(rect.y, rect.width):
        #         for j in range(rect.x, rect.height):
        #             solve_grid[i][j] = n
        #     n += 1
        # print(solve_grid)
