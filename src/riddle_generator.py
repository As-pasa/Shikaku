from models import Rectangle
from random import randint, choices, choice


class DivideRiddleGenerator:
    ANCHOR_COUNT = {5: 9, 10: 19, 15: 31}

    def __init__(self, deck_size: int, preferred_anchor_count: int):
        self.dec_size: int = deck_size
        self.anchorCount: int = preferred_anchor_count
        self.rectangles: list[Rectangle] = [
            Rectangle(0, 0, deck_size, deck_size)]
        self.finalized: list[Rectangle] = []
        self.max_scatter = 3

    @staticmethod
    def subdivide(rect: Rectangle, subdivision_axis: int,
                  subdivision_index: int) -> list[Rectangle]:
        """Принимая все заранее сгенерированные параметры проводит разбиение прямоугольника.
         В случае невалидных аргументов возвращает исходный прямоугольник"""
        if subdivision_axis == 0:
            if subdivision_index >= rect.width:
                return [rect]
            rect1 = Rectangle(rect.x, rect.y, subdivision_index, rect.height)
            rect2 = Rectangle(rect.x + subdivision_index, rect.y,
                              rect.width - subdivision_index, rect.height)
            return [rect1, rect2]
        if subdivision_axis == 1:
            if subdivision_index >= rect.height:
                return [rect]
            rect1 = Rectangle(rect.x, rect.y, rect.width, subdivision_index)
            rect2 = Rectangle(rect.x, rect.y + subdivision_index, rect.width,
                              rect.height - subdivision_index)
            return [rect1, rect2]

    def select_rectangle_to_divide(self) -> int:
        """Выбирает из списка один из прямоугольников.
        В большинстве случаев выбирается самый круный, но с небольшим шансом могут быть выбраны и другие"""
        self.rectangles = sorted(self.rectangles,
                                 key=lambda x: x.width * x.height, reverse=True)

        real_scatter = min(len(self.rectangles) - 1, self.max_scatter - 1)
        if real_scatter > 0:
            selected = choices([i for i in range(0, real_scatter)],
                               [0.4, 0.3, 0.2][:real_scatter])[0]
            return selected
        return 0

    def subdivide_from_index(self, index: int, slice_axis: int,
                             slice_index: int) -> None:
        """Обертка над основной статической функцией, выполняет доп. проверки и модифицирует текущее состояние"""
        rect = self.rectangles[index]
        self.rectangles.remove(rect)
        kk = self.subdivide(rect, slice_axis, slice_index)
        for i in kk:
            if i.height * i.width == 1:
                self.rectangles.append(rect)
                return
        self.rectangles += kk

    @staticmethod
    def select_axis(rect: Rectangle) -> int:
        """Выбирает ось деления прямоугольника"""
        if rect.height * rect.width <= 4:
            return 2

        return choices([max([0, 1], key=lambda x: [rect.width, rect.height][x]),
                        min([0, 1],
                            key=lambda x:
                            [rect.width, rect.height][x])],
                       [0.7, 0.3])[0]

    @staticmethod
    def select_index(size: int) -> int:
        """Выбирает, по какому измерению проводить разбиение"""
        if size <= 2:
            return 1
        return randint(1, size - 1)

    def compute(self) -> None:
        """Формирует финальное разбиение"""
        while self.rectangles and len(
                self.finalized + self.rectangles) < self.anchorCount:
            ind = self.select_rectangle_to_divide()
            axis = self.select_axis(self.rectangles[ind])
            if axis == 2:
                self.finalized.append(self.rectangles[ind])
                self.rectangles.remove(self.rectangles[ind])
                continue
            sp = 0
            if axis == 1:
                sp = self.select_index(self.rectangles[ind].height)
            if axis == 0:
                sp = self.select_index(self.rectangles[ind].width)
            self.subdivide_from_index(ind, axis, sp)

    def convert_to_string(self):
        """Подготавливает строковое представление"""
        matr = [[0 for j in range(self.dec_size)] for i in range(self.dec_size)]
        for i in self.rectangles + self.finalized:
            x, y = choice([i for i in i.get_inner_points()])
            sz = i.height * i.width
            matr[y][x] = sz
        st = ""
        for i in matr:
            kk = " ".join([str(p) for p in i])
            st += kk + "\n"
        return st