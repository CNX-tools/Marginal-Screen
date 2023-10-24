import os
import sys
from PyQt6 import QtGui
sys.path.append(os.getcwd())  # NOQA

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class QComboBoxDelegateForColumn(QStyledItemDelegate):
    """
        This class is used to create a combobox in a specific column of the table
    Args:
        options (list): The list of options for the combobox
    """

    def __init__(self, options: list, parent):
        super().__init__(parent)
        self.options = options

    def createEditor(self, parent, option, index) -> QWidget:
        editor = QComboBox(parent)
        editor.addItems(self.options)
        return editor

    def setEditorData(self, editor, index) -> None:
        current_text = index.model().data(index, Qt.ItemDataRole.EditRole)
        # If the editor is a QComboBox, this will select the current text
        if isinstance(editor, QComboBox):
            editor.setCurrentText(current_text)
        else:
            super().setEditorData(editor, index)

    def setModelData(self, editor, model, index) -> None:
        if isinstance(editor, QComboBox):
            model.setData(index, editor.currentText(), Qt.ItemDataRole.EditRole)
        else:
            super().setModelData(editor, model, index)


class MainGui(QWidget):

    base_colors: list = ["black", "red", "green", "blue", "white", "gray"]
    closed = pyqtSignal()

    def __init__(self, app: QApplication, parent=None):
        super(MainGui, self).__init__(parent)
        self.app = app

        self.setupFont()
        self.setupUI()

    def setupFont(self):
        self.font = QFont()
        self.font.setFamily(u"Segoe UI")
        self.font.setPointSize(10)

        self.font1 = QFont()
        self.font1.setFamily(u"Segoe UI")
        self.font1.setPointSize(10)
        self.font1.setBold(True)

        self.font2 = QFont()
        self.font2.setFamily(u"Segoe UI")
        self.font2.setPointSize(10)
        self.font2.setBold(True)
        self.font2.setItalic(True)

    def __setupLabel(self):
        self.label = QLabel(self)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(73, 20, 121, 31))
        self.label.setFont(self.font1)
        self.label.setText("Marginal Monitor")

    def __setupButton(self):
        self.add_line_button = QPushButton(self)
        self.add_line_button.setObjectName(u"pushButton")
        self.add_line_button.setGeometry(QRect(32, 85, 81, 31))
        self.add_line_button.setFont(self.font)
        self.add_line_button.setStyleSheet(
            u"QPushButton {background-color: rgb(19, 132, 2); color: white; border-radius: 5px}  QPushButton:hover {border: 2px solid pink}")
        self.add_line_button.setText("Add Line")
        self.add_line_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.delete_line_button = QPushButton(self)
        self.delete_line_button.setObjectName(u"delete_line_button")
        self.delete_line_button.setGeometry(QRect(32, 165, 81, 31))
        self.delete_line_button.setFont(self.font)
        self.delete_line_button.setStyleSheet(
            u"QPushButton {background-color: rgb(44, 125, 202); color: white; border-radius: 5px}  QPushButton:hover {border: 2px solid pink}")
        self.delete_line_button.setText("Delete Line")
        self.delete_line_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.show_hide_button = QPushButton(self)
        self.show_hide_button.setObjectName(u"show_hide_button")
        self.show_hide_button.setGeometry(QRect(72, 230, 111, 31))
        self.show_hide_button.setFont(self.font)
        self.show_hide_button.setStyleSheet(
            u"QPushButton {background-color: rgb(0, 0, 0); color: white; border-radius: 5px}  QPushButton:hover {border: 2px solid pink}")
        self.show_hide_button.setText("Show/Hide Lines")
        self.show_hide_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def __setupComboBox(self):
        # Choose line color combobox
        self.comboBox = QComboBox(self)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(140, 87, 81, 25))
        self.comboBox.setFont(self.font)
        self.comboBox.setStyleSheet(
            u"background-color:rgb(214, 214, 214); border: 1px solid white; border-radius: 2px; color: rgb(0, 0, 0)")
        self.comboBox.addItems(self.base_colors)

        # Choose line to delete combobox
        self.comboBox_2 = QComboBox(self)
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setGeometry(QRect(140, 168, 81, 25))
        self.comboBox_2.setFont(self.font)
        self.comboBox_2.setStyleSheet(
            u"background-color:rgb(214, 214, 214); border: 1px solid white; border-radius: 2px; color: rgb(0, 0, 0)")

    def __setupTable(self):
        self.tableWidget = QTableWidget(self)
        if (self.tableWidget.columnCount() < 4):
            self.tableWidget.setColumnCount(4)

        __no_line = QTableWidgetItem()
        __no_line.setFont(self.font2)
        __no_line.setText("#No")
        self.tableWidget.setHorizontalHeaderItem(0, __no_line)

        __line_color = QTableWidgetItem()
        __line_color.setFont(self.font2)
        __line_color.setText("Color")
        self.tableWidget.setHorizontalHeaderItem(1, __line_color)

        __line_type = QTableWidgetItem()  # horizontal or vertical
        __line_type.setFont(self.font2)
        __line_type.setText("Type")
        self.tableWidget.setHorizontalHeaderItem(2, __line_type)

        __line_position = QTableWidgetItem()
        __line_position.setFont(self.font2)
        __line_position.setText("Position (From Top / Left side)")
        self.tableWidget.setHorizontalHeaderItem(3, __line_position)

        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(290, 30, 381, 241))
        self.tableWidget.horizontalHeader().setDefaultSectionSize(50)

        # Change the width of the columns 4
        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 50)
        self.tableWidget.setColumnWidth(2, 50)
        self.tableWidget.setColumnWidth(3, 380 - 1 - 150)

        # We cannot resize the columns
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

        # Turn off the vertical header
        self.tableWidget.verticalHeader().setVisible(False)

        # Set the delegate for the combobox at column 1, 2
        self.tableWidget.setItemDelegateForColumn(1, QComboBoxDelegateForColumn(self.base_colors, self))
        self.tableWidget.setItemDelegateForColumn(2, QComboBoxDelegateForColumn(["hor", "ver"], self))

    def setupUI(self):
        self.resize(700, 300)
        self.setMinimumSize(QSize(700, 300))
        self.setMaximumSize(QSize(700, 300))
        self.setStyleSheet("background-color: white;")

        # Set up the label
        self.__setupLabel()
        # Set up the button
        self.__setupButton()
        # Set up the combobox
        self.__setupComboBox()
        # Set up the table
        self.__setupTable()

    def warning_box(self, message: str):
        box = QMessageBox()
        box.setIcon(QMessageBox.Icon.Warning)
        box.setWindowTitle("Warning")
        box.setText(message)
        box.setStandardButtons(QMessageBox.StandardButton.Ok)
        box.exec()
