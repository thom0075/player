#!python3

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QMainWindow
from PyQt6.QtGui import QIcon, QFont, QAction
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()  # calls parent class' constructor
        self.setWindowTitle(f"Audio player - Playing ")  # TODO set variable current_track {current_track}
        self.setWindowIcon(QIcon("qt.png"))

        self.setGeometry(500, 300, 400, 300)
        self.create_menu()  # calls this method to create the top menu

    def create_menu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")

        importTracks = QAction("Import tracks", self)  # TODO add icon(s) here
        importTracks.setShortcut("Ctrl+N")

        exitAction = QAction("Exit", self)
        exitAction.setShortcut("Alt+F4")

        fileMenu.addAction(importTracks)
        fileMenu.addAction(exitAction)

    def close_window(self):
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
