import dataclasses
import math

from utils.mathUtils import get_divider_pairs


@dataclasses.dataclass
class Anchor:
    x: int
    y: int
    id: int
    size: int


@dataclasses.dataclass
class Cell:
    is_occupied: bool
    reachable_by: list[Anchor] = dataclasses.field(default_factory=list)

    def clear_reachable(self):
        self.reachable_by = []


@dataclasses.dataclass
class Rectangle:
    x: int
    y: int
    width: int
    height: int

    def get_inner_points(self) -> [tuple[int, int]]:
        for y in range(self.height):
            for x in range(self.width):
                yield self.x + x, self.y + y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.height == other.height and self.width == other.width


class AnchorsFileReader:
    def __init__(self, data: str):
        self.grid = []
        self.size = len(data.splitlines())
        self.anchors = AnchorsFileReader.create_anchors(self, data)

    def create_anchors(self, content: str):
        anchors = []
        lines = content.splitlines()
        data = [[value for value in map(int, row.split())]
                for row in lines]
        idd: int = 0
        for x in range(self.size):
            for y in range(self.size):
                if data[y][x] != 0:
                    z = Anchor(x, y, idd, data[y][x])
                    idd += 1
                    anchors.append(z)
        return anchors


class SolvingGrid:
    def __init__(self, size: int, anchors: list[Anchor]):
        self.size: int = size
        self.matrix: list[Cell] = [Cell(False) for i in
                                   range(self.size * self.size)]
        for i in anchors:
            self.mark_occupied(i.x, i.y)

    def is_cell_occupied(self, x, y) -> bool:
        return self.matrix[y * self.size + x].is_occupied

    def get_anchors_that_reach_cell(self, x, y):
        return self.matrix[y * self.size + x].reachable_by

    def mark_occupied(self, x, y) -> None:
        self.matrix[y * self.size + x].is_occupied = True

    def mark_reachable_by(self, x, y, anchor: Anchor):
        self.matrix[y * self.size + x].reachable_by.append(anchor)

    def clear_all_reachable(self):
        for i in self.matrix:
            i.clear_reachable()

    def collide(self, rect: Rectangle) -> [tuple[int, int]]:
        ans = []
        a = [i for i in rect.get_inner_points()]
        for x, y in a:
            if self.is_cell_occupied(x, y):
                ans.append((x, y))
        return ans

    def collideAll(self, rect: Rectangle) -> [tuple[int, int]]:
        return [i for i in rect.get_inner_points()]

    def is_rect_valid(self, rect: Rectangle) -> bool:

        return 0 <= rect.x < self.size and \
            0 <= rect.y < self.size and \
            0 <= rect.x + rect.width - 1 < self.size \
            and 0 <= rect.y + rect.height - 1 < self.size

    def print(self):
        ans = ""
        for i in range(len(self.matrix)):
            if i % self.size == 0:
                ans += f"\n"

            ans += f"{int(self.matrix[i].is_occupied)} "
        print(ans)


class AnchorVariantsResolver:
    def __init__(self, anchor: Anchor, grid: SolvingGrid):
        self.anchor = anchor
        self.grid = grid
        self.variants: list[Rectangle] = self.get_rectangle_variants()

    def get_rectangle_variants(self) -> [Rectangle]:
        size: int = self.anchor.size
        ans = []
        for width, height in get_divider_pairs(size):
            for start_x in range(self.anchor.x - width + 1, self.anchor.x + 1):
                for start_y in range(self.anchor.y - height + 1,
                                     self.anchor.y + 1):
                    r = Rectangle(start_x, start_y, width, height)
                    if not self.grid.is_rect_valid(r):
                        continue
                    collide_entries: tuple[int, int] = self.grid.collide(r)
                    if len(collide_entries) == 1:
                        ans.append(r)
        return ans

    def _inner_filter(self) -> [Rectangle]:

        for rect in self.variants:

            collide_entries: tuple[int, int] = self.grid.collide(rect)

            if len(collide_entries) > 1:
                self.variants.remove(rect)
            k=self.grid.collideAll(rect)
            for x, y in k:
                ancss = self.grid.get_anchors_that_reach_cell(x, y)
                if len(ancss) == 1 and (x, y) != (self.anchor.x, self.anchor.y):
                    self.variants = [rect]

                    return self.variants
        return self.variants

    def filter_existing_variants(self) -> [Rectangle]:

        self._inner_filter()

        if len(self.variants) == 1:
            for x, y, in self.grid.collideAll(self.variants[0]):
                self.grid.mark_occupied(x, y)
        return self.variants

    def mark_reachable(self) -> None:
        for rect in self.variants:
            for x, y in rect.get_inner_points():
                self.grid.mark_reachable_by(x, y, self.anchor)
