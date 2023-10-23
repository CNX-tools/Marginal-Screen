import traceback
import sys
import os

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QIcon
from src.controller.MainController import MainController as MainGui


def add_path_to_env():
    new_path = os.path.join(
        os.getcwd(), '.venv\Lib\site-packages\PyQt6\Qt6\plugins\platforms')
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = new_path


# Import the UI code from your Qt Designer-generated file
add_path_to_env()

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)

        # Create an instance of the UI class
        ui = MainGui(app=app)

        # Set the title of the main window
        ui.setWindowTitle("Marginal Monitor")

        # Set the main window's icon
        ui.setWindowIcon(QIcon('./assets/quan.ico'))

        # Show the main window
        ui.show()

        # Start the application event loop
        sys.exit(app.exec())
    except Exception as e:
        # Display the error in a message box
        error_message = f"An error occurred:\n{traceback.format_exc()}"
        QMessageBox.critical(None, "Error", error_message)
        sys.exit(1)
