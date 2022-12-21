#!python3

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QMainWindow, \
    QListWidget, QFileDialog
from PyQt6.QtGui import QIcon, QFont, QAction
from pygame import mixer
from pathlib import Path
from stylesheets import *
import glob
import os
import sys
import DLL


class Window(QMainWindow):
    def __init__(self):
        super().__init__()  # calls parent class' constructor
        self.setWindowTitle(f"Audio player - Playing: ")  # TODO set variable current_track {current_track}
        self.setWindowIcon(QIcon("qt.png"))

        self.setGeometry(500, 300, 550, 400)
        self.create_menu()  # calls this method to create the top menu
        self.track = None

        mixer.init()

    def create_menu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")

        importTracks = QAction("Import tracks", self)  # TODO add icon(s) here
        importTracks.setShortcut("Ctrl+N")
        importTracks.triggered.connect(self.discover_Tracks)

        exitAction = QAction("Exit", self)
        exitAction.setShortcut("Alt+F4")
        exitAction.triggered.connect(self.close_window)

        fileMenu.addAction(importTracks)
        fileMenu.addAction(exitAction)

    def close_window(self):
        self.close()

    def create_ui(self, MainWindow):
        self.main_v_layout = QVBoxLayout()
        self.buttons_h_layout = QHBoxLayout()  # create the h. layout for the buttons
        self.centralwidget = QWidget(MainWindow)  # creates the central widget and sets the parent to MainWindow
        self.centralwidget.setObjectName("centralwidget")

        """
        This part of the code is dedicated to creating the buttons for playing media.
        Three buttons are defined: one for returning to the previous track, one for playing/pausing
        the current track and one for getting to the next track.
        All the widgets in the main window must inherit from centralwidget.
        """

        self.trackList = QListWidget(self.centralwidget)
        self.trackList.setGeometry(25, 250, 500, 70)
        self.trackList.setStyleSheet(u"background-image:url('./listback.png')")
        self.trackList.clicked.connect(self.track_selected)

        self.playButton = QPushButton(self.centralwidget)
        self.playButton.setObjectName("playButton")  # sets obj name
        self.playButton.setCheckable(True)
        self.playButton.setGeometry(240, 170, 70, 50)  # sets position and dimensions: x,y,width, height

        self.backButton = QPushButton(self.centralwidget)
        self.backButton.setObjectName("backButton")
        self.backButton.setGeometry(150, 170, 70, 50)

        self.forwardButton = QPushButton(self.centralwidget)
        self.forwardButton.setObjectName("backButton")
        self.forwardButton.setGeometry(330, 170, 70, 50)

        self.playButton.setStyleSheet(playbuttonStyle)
        self.backButton.setStyleSheet(backbuttonstyle)
        self.forwardButton.setStyleSheet(nextbuttonstyle)

        self.playButton.setIcon(QIcon("./icons/play.png"))
        self.backButton.setIcon(QIcon("./icons/rewind.png"))
        self.forwardButton.setIcon(QIcon("./icons/forward.png"))

        self.playButton.clicked.connect(self.play_pause)
        self.backButton.clicked.connect(self.previous)
        self.forwardButton.clicked.connect(self.next)

        self.buttons_h_layout.addWidget(self.backButton)
        self.buttons_h_layout.addWidget(self.playButton)
        self.buttons_h_layout.addWidget(self.forwardButton)

        MainWindow.setCentralWidget(self.centralwidget)  # sets the window's main widget

        self.main_v_layout.addLayout(self.buttons_h_layout)
        self.main_v_layout.addWidget(self.trackList)
        self.centralwidget.setStyleSheet(u"background-image:url('./wallpaper.jpg')")

    def play_pause(self):
        if self.playButton.isChecked():
            self.playButton.setIcon(QIcon("./icons/play.png"))
            mixer.music.pause()
        else:
            self.playButton.setIcon(QIcon("./icons/pause.png"))
            mixer.music.unpause()

    def previous(self):
        if self.track is None:
            return
        tracks = DLL.DLL()  # creates a doubly linked list

        for key in self.tracksD.keys():
            if key == self.track:
                tracks.InsertToEnd(key)  # DLL
                tracks.TraverseDLL(True, False, self.track)
                continue
            tracks.InsertToEnd(key)  # DLL
            print(f"[DICT KEY] {key}")

        tName = str(tracks.changeTrack(True, True, False, self.track).data)
        self.track = tName
        previousPath = self.tracksD[tName]
        mixer.music.load(previousPath)
        mixer.music.play()
        self.setWindowTitle(f"Audio player - Playing: {self.track}")

    def next(self):
        if self.track is None:
            return
        tracks = DLL.DLL()  # creates a doubly linked list

        for key in self.tracksD.keys():
            if key == self.track:
                tracks.InsertToEnd(key)  # DLL
                tracks.TraverseDLL(True, False, self.track)
                continue
            tracks.InsertToEnd(key)  # DLL
            print(f"[DICT KEY] {key}")

        tName = str(tracks.changeTrack(True, True, True, self.track).data)
        self.track = tName
        previousPath = self.tracksD[tName]

        mixer.music.load(previousPath)
        mixer.music.play()
        self.setWindowTitle(f"Audio player - Playing: {self.track}")

    def track_selected(self):
        try:
            self.track = self.trackList.currentItem().text()
            self.setWindowTitle(f"Audio player - Playing: {self.track}")
            mixer.music.load(self.tracksD[f"{self.track}"])
            mixer.music.play()
            self.playButton.setIcon(QIcon("./icons/pause.png"))
            print(self.tracksD[f"{self.track}"])
        except Exception as E:
            with open("report.txt", "w") as f:
                f.write("Line 154 " + str(E))

    def discover_Tracks(self):
        self.folderPath = QFileDialog.getExistingDirectory(self, 'Select Tracks Folder')  # type: str
        print(self.folderPath)
        try:
            self.allFiles = glob.glob(f"{self.folderPath}/*.mp3", recursive=False)
            for i in range(len(self.allFiles)):
                print(self.allFiles[i])
        except Exception as E:
            with open("report.txt", "w") as f:
                f.write(str(E))
        self.add_to_list(self.allFiles)

    def add_to_list(self, tracks):
        try:
            self.tracksD = {}
            for i in range(len(tracks)):
                self.trackList.insertItem(0, Path(tracks[i]).name)
                self.tracksD[Path(tracks[i]).name] = tracks[i]
            for key, value in self.tracksD.items():
                print(f"{key} -> {value}")
        except Exception as E:
            with open("report.txt", "w") as f:
                f.write(str(E))


if __name__ == "__main__":
    # mixer.init()
    app = QApplication(sys.argv)
    window = Window()
    window.create_ui(window)

    window.discover_Tracks()
    window.show()
    sys.exit(app.exec())
