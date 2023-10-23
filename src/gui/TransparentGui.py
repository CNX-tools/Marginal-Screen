import os
import sys

from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QWidget
sys.path.append(os.getcwd())  # NOQA

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class TransparentGui(QMainWindow):
    def __init__(self, app: QApplication) -> None:
        super(TransparentGui, self).__init__()
        self.app = app

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(0, 0, 0, 0)

        # PyQt6 syntax
        desktop = QGuiApplication.screens()[0]
        screen_rect = desktop.availableGeometry()

        self.setGeometry(screen_rect)

        self.lines = []  # (no, color, line_type, position)

    def add_lines(self, no: int, color: str, line_type: str, position: tuple):
        self.lines.append((no, color, line_type, position))

    def paintEvent(self, event):
        painter = QPainter(self)

        base_colors: list = ["black", "red", "green", "blue", "white", "gray"]

        # Set up the pen
        red_pen = QPen(Qt.GlobalColor.red, 1, Qt.PenStyle.SolidLine)
        green_pen = QPen(Qt.GlobalColor.green, 1, Qt.PenStyle.SolidLine)
        blue_pen = QPen(Qt.GlobalColor.blue, 1, Qt.PenStyle.SolidLine)
        white_pen = QPen(Qt.GlobalColor.white, 1, Qt.PenStyle.SolidLine)
        gray_pen = QPen(Qt.GlobalColor.gray, 1, Qt.PenStyle.SolidLine)
        black_pen = QPen(Qt.GlobalColor.black, 1, Qt.PenStyle.SolidLine)

        for line in self.lines:
            color: str = line[1]
            line_type: str = line[2]
            position: tuple = line[3]

            painter.setPen(eval(f'{color}_pen'))

            if line_type == "hor":
                # For example, if line_type is "hor" and position is (540, 540), then the line will be the center horizontal line of the full hd screen
                print(line)
                painter.drawLine(0, position[1], self.width(), position[1])
            elif line_type == "ver":
                print(line)
                # For example, if line_type is "ver" and position is (1920/2, 1920/2), then the line will be the center vertical line of the full hd screen
                painter.drawLine(position[0], 0, position[0], self.height())

    def toggle_line(self, status: str, value: str):
        if status == 'add':
            if self.lines == []:
                max_no = 0
            else:
                max_no = max([line[0] for line in self.lines])
            # Default line is horizontal line at the the center of the screen
            self.lines.append((max_no + 1, value, "hor", (0, int(self.height() / 2))))
        elif status == 'delete':
            self.lines = [line for line in self.lines if line[0] != int(value)]

        self.update()
