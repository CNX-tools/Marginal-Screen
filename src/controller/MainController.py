import os
import sys
sys.path.append(os.getcwd())  # NOQA

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from src.gui.MainGui import MainGui


class MainController(MainGui):
    def __init__(self, app: QApplication, parent=None):
        super(MainController, self).__init__(app=app, parent=parent)

        self.add_table_row(1, "red", "hor", (0, 0))
        self.add_table_row(2, "green", "ver", (142, 435))

    def add_table_row(self, order: int, color: str, line_type: str, postion: tuple):
        # Create a new row
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        # Add the order
        self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(str(order)))
        self.tableWidget.item(rowPosition, 0).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        # Add the color
        self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(color))
        self.tableWidget.item(rowPosition, 1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        # Add the line type
        self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(line_type))
        self.tableWidget.item(rowPosition, 2).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        # Add the position
        self.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(str(postion)))

    def add_line_event(self, color: str):
        pass
