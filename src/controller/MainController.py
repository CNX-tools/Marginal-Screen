import os
import sys
sys.path.append(os.getcwd())  # NOQA

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from src.gui.MainGui import MainGui
from src.gui.TransparentGui import TransparentGui


class MainController(MainGui):

    toggle_line_signal = pyqtSignal(str, str)

    def __init__(self, app: QApplication, parent=None):
        super(MainController, self).__init__(app=app, parent=parent)

        self.add_table_row(1, "red", "hor", (0, 0))
        self.add_table_row(2, "green", "ver", (142, 435))

        # Connect the event to button
        self.add_line_button.clicked.connect(lambda: self.add_line_event(self.comboBox.currentText()))
        self.delete_line_button.clicked.connect(lambda: self.delete_line_event(self.comboBox_2.text()))

        self.transparent_gui = TransparentGui(app=self.app)
        self.closed.connect(self.transparent_gui.close)
        self.transparent_gui.show()  # Show the transparent gui
        self.toggle_line_signal.connect(self.transparent_gui.toggle_line)

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
        print(f'Add line {color}')
        self.toggle_line_signal.emit('add', color)

    def delete_line_event(self, no: str):
        if no == '':
            return

        print(f'Delete line {no}')
        self.toggle_line_signal.emit('delete', no)

    def closeEvent(self, event) -> None:
        self.closed.emit()
        event.accept()
