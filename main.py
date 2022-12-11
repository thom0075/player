#!python3

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QMainWindow
from PyQt6.QtGui import QIcon, QFont, QAction
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__(self)
        self.setWindowTitle(f"Audio player - Playing {current_track}")  # TODO set variable current_track
        self.setWindowIcon("qt.png")
        self.setGeometry(500, 300, 600, 200)
        self.create_menu()  #calls this method to create the top menu

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())