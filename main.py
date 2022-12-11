#!python3

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QMainWindow
from PyQt6.QtGui import QIcon, QFont, QAction
from pygame import mixer
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()  # calls parent class' constructor
        self.setWindowTitle(f"Audio player - Playing ")  # TODO set variable current_track {current_track}
        self.setWindowIcon(QIcon("qt.png"))

        self.setGeometry(500, 300, 550, 400)
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

    def create_ui(self, MainWindow):
        buttons_h_layout = QHBoxLayout()  # create the h. layout for the buttons
        self.centralwidget = QWidget(MainWindow)  # creates the central widget and sets the parent to MainWindow
        self.centralwidget.setObjectName("centralwidget")

        """
        This part of the code is dedicated to creating the buttons for playing media.
        Three buttons are defined: one for returning to the previous track, one for playing/pausing
        the current track and one for getting to the next track.
        """

        self.playButton = QPushButton(self.centralwidget)
        self.playButton.setObjectName("playButton")  # sets obj name
        self.playButton.setGeometry(150, 170, 70, 50)  # sets position and dimensions: x,y,width, height
        self.playButton.setText("Play")  # sets the button's text

        self.backButton = QPushButton(self.centralwidget)
        self.backButton.setObjectName("backButton")
        self.backButton.setGeometry(240, 170, 70, 50)
        self.backButton.setText("Previous")

        self.forwardButton = QPushButton(self.centralwidget)
        self.forwardButton.setObjectName("backButton")
        self.forwardButton.setGeometry(330, 170, 70, 50)
        self.forwardButton.setText("Next")

        self.playButton.clicked.connect(self.play_pause)
        self.backButton.clicked.connect(self.previous)
        self.forwardButton.clicked.connect(self.next)

        buttons_h_layout.addWidget(self.backButton)
        buttons_h_layout.addWidget(self.playButton)
        buttons_h_layout.addWidget(self.forwardButton)

        MainWindow.setCentralWidget(self.centralwidget)  # sets the window's main widget

    def play_pause(self):
        pass

    def previous(self):
        pass

    def next(self):
        pass


if __name__ == "__main__":
    mixer.init()
    app = QApplication(sys.argv)
    window = Window()
    window.create_ui(window)
    window.show()
    sys.exit(app.exec())
    pygame.mixer.music.load("example.mp3")
    pygame.mixer.music.play()