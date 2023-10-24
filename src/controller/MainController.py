import json
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

    data_dir = os.path.join(os.getcwd(), 'data.json')

    def __init__(self, app: QApplication, parent=None):
        super(MainController, self).__init__(app=app, parent=parent)

        # Connect the event to button
        self.add_line_button.clicked.connect(lambda: self.add_line_event(self.comboBox.currentText()))
        self.delete_line_button.clicked.connect(lambda: self.delete_line_event(self.comboBox_2.currentText()))
        self.show_hide_button.clicked.connect(self.handle_show_hide_button_clicked)

        # Connect the event change of the table
        self.tableWidget.itemChanged.connect(self.table_changed_event)

        # # Create the transparent gui
        # self.transparent_gui = TransparentGui(app=self.app)
        # self.closed.connect(self.transparent_gui.close)
        # self.transparent_gui.show()  # Show the transparent gui
        # self.toggle_line_signal.connect(self.transparent_gui.toggle_line)

        # # Load the saved data
        # self.load_data()

    def load_data(self):
        with open(self.data_dir, 'r') as f:
            data: list = json.load(f)

        # Reload the table
        self.reload_table(data)

        # Reload the combobox
        self.comboBox_2.clear()
        self.comboBox_2.addItems([str(line[0]) for line in data])

        # Add the lines to the transparent gui
        for line in data:
            self.transparent_gui.add_lines(*line)
        self.transparent_gui.update()

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
        self.tableWidget.item(rowPosition, 3).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def reload_table(self, lines: list):
        self.tableWidget.setRowCount(0)
        for line in lines:
            self.add_table_row(line[0], line[1], line[2], line[3])

    def table_changed_event(self):
        # Get the row that has been changed
        row = self.tableWidget.currentRow()

        if row == -1:
            return

        line_change_info = []

        for i in range(4):
            value = self.tableWidget.item(row, i).text()
            if i == 0 or i == 3:
                eval_value = eval(value)
                try:
                    value = int(eval_value)
                    self.tableWidget.item(row, i).setText(str(value))
                except Exception:
                    self.warning_box('The value of position must be an integer')
                    return
            line_change_info.append(value)

        print(f'Line changed has info: {line_change_info}')

        self.transparent_gui.handle_change_line(tuple(line_change_info))

    def add_line_event(self, color: str):
        print(f'Add line {color}')

        # Add the line to the transparent gui
        self.toggle_line_signal.emit('add', color)

        # Add the no of new line to the combobox
        self.comboBox_2.addItem(str(max([line[0] for line in self.transparent_gui.lines])))

        # Reload the table
        self.reload_table(self.transparent_gui.lines)

    def delete_line_event(self, no: str):
        if no == '':
            return

        print(f'Delete line {no}')
        self.toggle_line_signal.emit('delete', no)

        # Reload the table
        self.reload_table(self.transparent_gui.lines)

        # Remove the no of deleted line from the combobox
        self.comboBox_2.removeItem(self.comboBox_2.findText(no))

    def handle_show_hide_button_clicked(self):
        self.transparent_gui.visible = not self.transparent_gui.visible
        self.transparent_gui.update()

    def closeEvent(self, event) -> None:
        self.closed.emit()
        event.accept()
