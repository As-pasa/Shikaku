import sys
import pickle
import os

from window import Window
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QFont, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, \
    QPushButton, QMessageBox, QFileDialog, QAction, QInputDialog, QLineEdit, \
    QFormLayout, QDialogButtonBox, QGridLayout, QFrame

from check_files import Checking
from models import AnchorsFileReader, Rectangle
from solution import BoardSolution


class Game(QMainWindow):
    """Основное окно игры с базовыми кнопками выбора формата доски"""

    COLOR = {0: 'white', 1: 'black', 2: '#c4c9cc'}
    FILE_NAME = 'game_state.pickle'

    def __init__(self):
        super().__init__()
        self.data = ""
        self.table = []
        self.size = 0
        self.is_pressed = False
        self.set_menuBar()
        self.window = Window(self)

        self.setWindowTitle("SHIKAKU GAME")
        self.setGeometry(400, 400, 800, 800)
        self.set_centre(self)
        self.name = QLabel("SHIKAKU GAME", self)
        self.name.setGeometry(200, 100, 400, 50)
        self.name.setStyleSheet("border : 3px solid black")
        self.name.setFont(QFont('Terminus', 15))
        self.name.setAlignment(Qt.AlignCenter)

        self.window_components()
        self.show()

    def set_menuBar(self):
        """Устанавливает кнопку выхода из приложения"""
        exit_action = QAction("Exit", self)
        exit_action.setShortcut('Ctrl+E')
        exit_action.setStatusTip("Exit from game")
        exit_action.triggered.connect(self.close)

        menubar = self.menuBar()
        self.statusBar()
        file_menu = menubar.addMenu('&Exit')
        file_menu.addAction(exit_action)

    def save_game(self):
        """Сохраняет состояние игры на момент выхода в файл"""
        collection = []
        for rectangle in self.window.rectangles:
            collection.append((rectangle.x, rectangle.y,
                               rectangle.width, rectangle.height))
        data = {
            'board_data': self.data,
            'table_data': collection
        }
        with open(self.FILE_NAME, 'wb') as file:
            pickle.dump(data, file)
        self.resume.clicked.connect(self.load_game)

    def load_game(self):
        """Загружает доску из файла"""
        win_size = self.window.setting.value('size')
        if win_size:
            self.window.restoreGeometry(win_size)

        msg = QMessageBox.question(self, "Question",
                                   "Wanna you continue game?",
                                   QMessageBox.Yes | QMessageBox.No)
        if msg == QMessageBox.Yes:
            try:
                with open(self.FILE_NAME, 'rb') as file:
                    data = pickle.load(file)
                    self.data = data['board_data']
                    self.size = len(self.data.splitlines())
                    self.window.rectangle = [0, 0]
                    self.window.rectangles = [Rectangle(rect[0], rect[1],
                                                        rect[2], rect[3])
                                              for rect in data['table_data']]
                    material = self.prepare_material(self.data.splitlines())
                    self.restore_board(material, 'restore')
            except FileNotFoundError:
                pass
        else:
            self.window.delete_saving()

    def window_components(self):
        """Устанавливает основные элементы основного окна"""
        self.resume = QPushButton("Resume", self)
        self.resume.setGeometry(125, 300, 175, 40)

        self.generation = QPushButton("Generate", self)
        self.generation.setGeometry(300, 300, 175, 40)
        self.generation.clicked.connect(self.generate_board)

        self.offline = QPushButton("Offline", self)
        self.offline.setGeometry(475, 300, 175, 40)
        self.offline.clicked.connect(self.choose_file)

        if os.path.exists(self.FILE_NAME):
            self.resume.clicked.connect(self.load_game)

    def choose_size(self):
        msg = QMessageBox()
        msg.setWindowTitle("Size choice")
        msg.setText("You should choice a size of board")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        button_y = msg.button(QMessageBox.Yes)
        button_y.setText('5')
        button_n = msg.button(QMessageBox.No)
        button_n.setText('8')
        button_c = msg.button(QMessageBox.Cancel)
        button_c.setText('12')
        msg.buttonClicked.connect(self.generate_board)
        msg.exec_()

    def generate_board(self, button: QMessageBox):
        """Формирует случайную доску для решения"""
        pass

    def choose_file(self):
        """Выводит окно подтверждения загрузки файла с доской"""
        msg = QMessageBox()
        msg.setWindowTitle("File choice")
        msg.setText("You should choose your file")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Open | QMessageBox.Cancel)
        msg.buttonClicked.connect(self.set_file)
        msg.exec_()

    def set_file(self, button: QMessageBox):
        """Загружает файл с данными при решении оффлайн"""
        if button.text() == 'Open':
            file, _ = QFileDialog.getOpenFileName(self,
                                                  'Open File',
                                                  './',
                                                  'Text Files (*.txt)')
            with open(file, 'r') as f:
                file_content = f.read()
            msg = QMessageBox()
            msg.setWindowTitle("WARNING")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Close)
            if not Checking.check_file_content(file_content):
                msg.setText("The file should contain only numbers!")
                msg.exec_()
            elif not Checking.check_max_element(file_content):
                msg.setText(
                    "Each element must be less than square of board")
                msg.exec_()
            else:
                self.data = file_content
                self.help_method()

    def help_method(self):
        """Формирует данные для установки доски"""
        person_data = self.data.splitlines()
        self.size = len(person_data)
        self.set_board(person_data)

    def create_window(self, button: QMessageBox, flag='new'):
        """Загружает данные о доске с сайта при решении онлайн"""
        if flag == 'new':
            self.size = int(button.text())
        # self.data = ParserBoard(self.size).parse_board() #generate a new board
        self.help_method()

    def set_board(self, person_data):
        """Создает новое окно для установки доски"""
        data = self.prepare_material(person_data)
        self.window.setGeometry(0, 0, self.size * 70, self.size * 70)
        self.set_centre(self.window)
        self.restore_board(data)

    def restore_board(self, data, flag='new'):
        """Устанавливает доску для решения пользователем"""
        for i in range(self.size):
            for j in range(self.size):
                if data[i * self.size + j] != '0':
                    button = QPushButton(data[i * self.size + j], self.window)
                else:
                    button = QPushButton(parent=self.window)
                button.setGeometry(50 * (1 + j), 50 * (1 + i), 50, 50)
                button.setFont(QFont('Times', 15))
                position = (50 * (1 + j), 50 * (1 + i))
                # TODO неизменяемый тапл, по идее
                button_status = (button, position)
                button.clicked.connect(
                    lambda checked, btn=button_status: self.set_rectangle(btn))
                self.table.append(button_status)
        self.window.show()
        if flag != "new":
            self.window.mModified = True
            self.window.restored = True

    def clean_board(self):
        """Возвращает доску к значениям по умолчанию"""
        self.window.rectangle = [0, 0]
        self.window.restored = False
        self.window.deleting_rect = self.window.rectangles
        self.window.mModified = True

    def clean_window(self):
        """Удаляет данные окна с доской"""
        self.window = Window(self)
        self.table.clear()
        self.data = ''

    def check_solution(self):
        """Сверяет решение пользователя и правильное решение доски"""
        user_result = self.convert_rectangle(self.window.rectangles)
        program_result = BoardSolution(AnchorsFileReader(self.data)).solve()
        print(f'program: {program_result},\n user: {user_result}')
        msg = QMessageBox()
        msg.setWindowTitle("Results")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if user_result == program_result:
            self.window.finished = True
            msg.setText(
                "Congratulation! You win! Wanna you start a new game?")
            msg.setIcon(QMessageBox.Information)
        else:
            msg.setText(
                "Oh no! You are wrong. Wanna you start a new game?")
            msg.setIcon(QMessageBox.Warning)
        msg.buttonClicked.connect(self.exit_choice)
        msg.exec_()

    def exit_choice(self, button: QMessageBox):
        if button.text() == "&No" and self.window.finished:
            self.window.close()
            self.close()
        if button.text() == "&Yes":
            self.window.close()

    @staticmethod
    def convert_rectangle(rectangles):
        """Приводит решение пользователя к сравнимому формату"""
        rectangles = [Rectangle(rect.x / 50 - 1, rect.y / 50 - 1,
                                rect.width / 50, rect.height / 50)
                      for rect in rectangles]
        return sorted(rectangles, key=lambda rect: (rect.x, rect.y,
                                                    rect.width, rect.height))

    def set_solution(self):
        """Устанавливает доску в положение правильного решения"""
        solution = BoardSolution(AnchorsFileReader(self.data)).solve()
        self.window.rectangles = [Rectangle((rect.x + 1) * 50,
                                            (rect.y + 1) * 50,
                                            rect.width * 50,
                                            rect.height * 50)
                                  for rect in solution]
        self.window.restored = True
        self.window.mModified = True

    def set_rectangle(self, button):
        self.window.restored = False
        if not self.is_point_in_rectangle(button[1]):
            if not self.is_pressed:
                self.window.rectangle.clear()
                self.window.rectangle.append(button[1])
                self.is_pressed = True
            elif button[1] != self.window.rectangle[0]:
                self.window.rectangle.append(button[1])
                self.window.mModified = True
                self.is_pressed = False
        else:
            print(f'for delete: {self.window.deleting_rect}')
            self.window.mModified = True
        print(f'final_rectangles: {self.window.rectangles}')

    def delete_rectangle(self, qp):
        pen = QPen(Qt.white, 3, Qt.SolidLine)
        qp.setPen(pen)
        for delete_rect in self.window.deleting_rect:
            qp.drawRect(delete_rect.x,
                        delete_rect.y,
                        delete_rect.width,
                        delete_rect.height)
            self.window.update()
        if len(self.window.deleting_rect):
            self.window.rectangles.remove(self.window.deleting_rect[0])
        else:
            self.window.rectangles.clear()
        self.window.deleting_rect.clear()
        self.repeat_drawing(qp)

    def repeat_drawing(self, qp):
        for rect in self.window.rectangles:
            pen = QPen(Qt.blue, 3, Qt.SolidLine)
            qp.setPen(pen)
            qp.drawRect(rect.x,
                        rect.y,
                        rect.width,
                        rect.height)
            self.window.update()

    def draw_rectangle(self, qp):
        pen = QPen(Qt.blue, 3, Qt.SolidLine)
        qp.setPen(pen)
        rect = self.window.rectangle
        x = min(rect[0][0], rect[1][0])
        y = min(rect[0][1], rect[1][1])
        qp.drawRect(x, y,
                    abs(rect[0][0] - rect[1][0]) + 50,
                    abs(rect[0][1] - rect[1][1]) + 50)
        self.window.update()
        return x, y, \
               abs(rect[0][0] - rect[1][0]) + 50, \
               abs(rect[0][1] - rect[1][1]) + 50

    def is_point_in_rectangle(self, position):
        if not len(self.window.rectangles):
            return False
        for rect in self.window.rectangles:
            if rect.x <= position[0] <= rect.x + rect.width - 50 and \
                    rect.y <= position[1] <= rect.y + rect.height - 50:
                self.window.deleting_rect.append(rect)
                return True
        return False

    @staticmethod
    def set_centre(child):
        """Устанавливает окно по середине экрана"""
        desktop = QtWidgets.QApplication.desktop()
        x = (desktop.width() - child.width()) // 2
        y = (desktop.height() - child.height()) // 2
        child.move(x, y)

    @staticmethod
    def prepare_material(material):
        data = [line.split(' ') for line in material]
        return [x for line in data for x in line if x]


if __name__ == '__main__':
    App = QApplication([])
    window = Game()
    sys.exit(App.exec())
