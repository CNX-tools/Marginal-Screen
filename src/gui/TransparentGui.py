import json
import os
import sys

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QEvent, QObject
from PyQt6.QtWidgets import QWidget
sys.path.append(os.getcwd())  # NOQA

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class TransparentGui(QMainWindow):

    data_dir = os.path.join(os.getcwd(), 'data.json')

    def __init__(self, app: QApplication) -> None:
        super(TransparentGui, self).__init__()
        self.app = app

        self.setWindowTitle('Transparent Screen')

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowDoesNotAcceptFocus | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.WindowTransparentForInput)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(0, 0, 0, 0)

        self.visible = True

        # PyQt6 syntax
        desktop = QGuiApplication.screens()[0]
        screen_rect = desktop.availableGeometry()

        self.setGeometry(screen_rect)

        self.lines = []  # (no, color, line_type, position)

    def add_lines(self, no: int, color: str, line_type: str, position: int):
        self.lines.append((no, color, line_type, position))

    def paintEvent(self, event):
        painter = QPainter(self)

        base_colors: list = ["black", "red", "green", "blue", "white", "gray"]

        # Set up the pen
        red_pen = QPen(Qt.GlobalColor.red, 1.5, Qt.PenStyle.SolidLine)
        green_pen = QPen(Qt.GlobalColor.green, 1.5, Qt.PenStyle.SolidLine)
        blue_pen = QPen(Qt.GlobalColor.blue, 1.5, Qt.PenStyle.SolidLine)
        white_pen = QPen(Qt.GlobalColor.white, 1.5, Qt.PenStyle.SolidLine)
        gray_pen = QPen(Qt.GlobalColor.gray, 1.5, Qt.PenStyle.SolidLine)
        black_pen = QPen(Qt.GlobalColor.black, 1.5, Qt.PenStyle.SolidLine)

        if not self.visible:
            return

        for line in self.lines:
            color: str = line[1]
            line_type: str = line[2]
            position: int = line[3]

            painter.setPen(eval(f'{color}_pen'))

            if line_type == "hor":
                # For example, if line_type is "hor" and position is 525, then the line will be the center horizontal line of the full hd screen
                print(line)
                painter.drawLine(0, position, self.width(), position)
            elif line_type == "ver":
                print(line)
                # For example, if line_type is "ver" and position is (1920/2, 1920/2), then the line will be the center vertical line of the full hd screen
                painter.drawLine(position, 0, position, self.height())

        # Store the current painter state into a json file
        with open(self.data_dir, 'w', encoding='utf8') as f:
            json.dump(self.lines, f, ensure_ascii=False, indent=4)

    def handle_change_line(self, line_change: tuple):
        self.lines = [line_change if line[0] == line_change[0] else line for line in self.lines]
        print(self.lines)
        self.update()

    def toggle_line(self, status: str, value: str):
        if status == 'add':
            if self.lines == []:
                max_no = 0
            else:
                max_no = max([line[0] for line in self.lines])

            self.lines.append((max_no + 1, value, "hor", int(self.height() / 2)))  # Default line is horizontal line at the the center of the screen # NOQA

        elif status == 'delete':
            self.lines = [line for line in self.lines if line[0] != int(value)]

        self.update()

if __name__=='__main__':
    app = QApplication(sys.argv)
    transparent_gui = TransparentGui(app)
    transparent_gui.show()
    sys.exit(app.exec())
