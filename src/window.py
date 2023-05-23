import os

from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox, QPushButton
from PyQt5.QtGui import QPainter, QPixmap

from models import Rectangle


class Window(QMainWindow):
    """Интерактивная доска с головоломкой Shikaku"""

    FILE_NAME = 'game_state.pickle'

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle("Board")
        self.setting = QSettings("QtApp", "App")
        self.set_menuBar()
        self.rectangle = []
        self.rectangles = []
        self.mPixmap = QPixmap()
        self.deleting_rect = []
        self.restored = False
        self.mModified = True
        self.finished = False

    def set_menuBar(self):
        """Устанавливает базовые кнопки для взаимодействия"""
        new_game_action = QAction("Start new game", self)
        new_game_action.setShortcut('Ctrl+N')
        new_game_action.setStatusTip('Start new game with similar size')
        new_game_action.triggered.connect(self.start_new_game)

        check_action = QAction("Check solution", self)
        check_action.setShortcut('Ctrl+S')
        check_action.setStatusTip("Check your solution")
        check_action.triggered.connect(self.parent().check_solution)

        solution_action = QAction("View solution", self)
        solution_action.setShortcut('Ctrl+V')
        solution_action.setStatusTip("View a final solution")
        solution_action.triggered.connect(self.parent().set_solution)

        clean_action = QAction("Clear board", self)
        clean_action.setShortcut('Ctrl+C')
        clean_action.setStatusTip('Clear application')
        clean_action.triggered.connect(self.parent().clear_board)

        exit_action = QAction("Exit", self)
        exit_action.setShortcut('Ctrl+E')
        exit_action.setStatusTip("Exit from game")
        exit_action.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&New game')
        file_menu.addAction(new_game_action)
        file_menu = menubar.addMenu('&Restart')
        file_menu.addAction(clean_action)
        file_menu = menubar.addMenu('&Check')
        file_menu.addAction(check_action)
        file_menu = menubar.addMenu('&Solution')
        file_menu.addAction(solution_action)
        file_menu = menubar.addMenu('&Exit')
        file_menu.addAction(exit_action)

    def start_new_game(self):
        """Создает окно с доской того же размера, что и предыдущая"""
        self.close()
        self.parent().create_window(QPushButton(), 'similar')

    def delete_saving(self):
        """Удаляет данные о сохраненной доске за ненадобностью"""
        if os.path.exists(self.FILE_NAME):
            os.remove(self.FILE_NAME)
            self.parent().resume.disconnect()

    def closeEvent(self, event):
        if not self.finished:
            reply = QMessageBox.question(self, 'Message',
                                         'Do you want to save a game?',
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.setting.setValue('size', self.saveGeometry())
                self.parent().save_game()
            else:
                self.delete_saving()
        self.parent().clean_window()
        event.accept()

    def paintEvent(self, e):
        if len(self.rectangle) != 2 and not self.restored:
            return
        if self.mModified:
            pixmap = QPixmap(self.size())
            pixmap.fill(Qt.white)
            painter = QPainter(pixmap)
            painter.drawPixmap(0, 0, self.mPixmap)
            if self.restored:
                self.parent().repeat_drawing(painter)
            elif not self.deleting_rect:
                x, y, width, height = self.parent().draw_rectangle(painter)
                self.rectangles.append(
                    Rectangle(x, y, width, height)
                )
            else:
                self.parent().delete_rectangle(painter)
                self.mPixmap = QPixmap()
            self.mPixmap = pixmap
            self.mModified = False

        qp = QPainter(self)
        qp.drawPixmap(0, 0, self.mPixmap)
