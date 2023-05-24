import dataclasses

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
        """Возвращает набор точек, входящих в указанный прямоугольник"""
        for y in range(self.height):
            for x in range(self.width):
                yield self.x + x, self.y + y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and \
            self.height == other.height and self.width == other.width


class AnchorsFileReader:
    def __init__(self, data: str):
        self.grid = []
        self.size = len(data.splitlines())
        self.anchors = AnchorsFileReader.create_anchors(self, data)

    def create_anchors(self, content: str):
        """Парсит строку с целью выделения множества якорей"""
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
        self.matrix: list[Cell] = [Cell(False) for _ in
                                   range(self.size * self.size)]
        for i in anchors:
            self.mark_occupied(i.x, i.y)

    def is_cell_occupied(self, x, y) -> bool:
        """Определяет, занята ли указанная точка"""
        return self.matrix[y * self.size + x].is_occupied

    def get_anchors_that_reach_cell(self, x, y):
        """Возвращает список якорей, которые потенциально дотягиваются
        до точки"""
        return self.matrix[y * self.size + x].reachable_by

    def mark_occupied(self, x, y) -> None:
        """Помечает указанную точку как занятую, что в дальнейшем запрещает
        размещать здесь другие прямоугольники"""
        self.matrix[y * self.size + x].is_occupied = True

    def mark_reachable_by(self, x, y, anchor: Anchor):
        """Помечает указанную точку как потенциально достижимую указанным
        якорем"""
        self.matrix[y * self.size + x].reachable_by.append(anchor)

    def clear_all_reachable(self):
        """Убирает пометки Reachable во всех клетках, подготавливает поле к
        следующей итерации отсеивания решений"""
        for i in self.matrix:
            i.clear_reachable()

    def collide(self, rect: Rectangle) -> [tuple[int, int]]:
        """Возвращает все точки прямоугольника, помеченные как занятые"""
        ans = []
        a = [i for i in rect.get_inner_points()]
        for x, y in a:
            if self.is_cell_occupied(x, y):
                ans.append((x, y))
        return ans

    @staticmethod
    def collideAll(rect: Rectangle) -> [tuple[int, int]]:
        """Возвращает все точки, содержащиеся в указанном прямоугольнике"""
        return [i for i in rect.get_inner_points()]

    def is_rect_valid(self, rect: Rectangle) -> bool:
        """Проверяет, может ли указанный прямоугольник существовать на поле"""
        return 0 <= rect.x < self.size and 0 <= rect.y < self.size and \
            0 <= rect.x + rect.width - 1 < self.size and \
            0 <= rect.y + rect.height - 1 < self.size

    def print(self):
        """Отладочная функция для вывода состояния матрицы на консоль"""
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
        """Путем полного перебора определяет все потенциальное множество
        решений для текущего якоря"""
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

    def search_responsible_points(self, rect: Rectangle) -> [Rectangle]:
        """Проверяет, не является ли решение(прямоугольник) единственным,
        кто достигает некоторой точки"""
        k = self.grid.collideAll(rect)
        for x, y in k:
            ancss = self.grid.get_anchors_that_reach_cell(x, y)
            if len(ancss) == 1 and (x, y) != (self.anchor.x, self.anchor.y):
                return [rect]
        return []

    def filter_existing_variants(self) -> [Rectangle]:
        """Выделяет из текущего множества решений лишь те, которые остаются
        валидными на текущей итерации"""
        for rect in self.variants:
            collide_entries: tuple[int, int] = self.grid.collide(rect)
            if len(collide_entries) > 1:
                self.variants.remove(rect)
            responsible_rect = self.search_responsible_points(rect)
            if responsible_rect:
                self.variants = responsible_rect
                break
        if len(self.variants) == 1:
            for x, y, in self.grid.collideAll(self.variants[0]):
                self.grid.mark_occupied(x, y)
        return self.variants

    def mark_reachable(self) -> None:
        """Функция помечает все клетки всех решений(прямоугольников) как
        достижимые данным якорем"""
        for rect in self.variants:
            for x, y in rect.get_inner_points():
                self.grid.mark_reachable_by(x, y, self.anchor)


class SolutionChecker:
    def __init__(self, ancs: list[Anchor], rects: list[Rectangle], size: int):
        self.ancs = ancs
        self.rects = rects
        self.size = size
        self.grid = SolvingGrid(size, self.ancs)

    def get_anchor_from_coord(self, x:int, y:int) -> Anchor | None:
        """ищет якорь с соответствующей координатой"""
        for i in self.ancs:
            if i.x == x and i.y == y:
                return i
        return None

    def check(self) -> bool:
        """Проверяет решение на валидность"""
        for i in self.rects:
            collide = self.grid.collide(i)
            if len(collide) != 1:
                return False
            anc = self.get_anchor_from_coord(collide[0][0], collide[0][1])
            if anc.size != i.height * i.width:
                return False
            for x, y in i.get_inner_points():
                self.grid.mark_occupied(x, y)
        return all([k.is_occupied for k in self.grid.matrix])
