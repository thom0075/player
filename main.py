#!python3

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QMainWindow, \
    QListWidget, QFileDialog
from PyQt6.QtGui import QIcon, QFont, QAction
from pygame import mixer
from pathlib import Path
import glob
import os
import sys
import DLL


class Window(QMainWindow):
    def __init__(self):
        super().__init__()  # calls parent class' constructor
        self.setWindowTitle(f"Audio player - Playing ")  # TODO set variable current_track {current_track}
        self.setWindowIcon(QIcon("qt.png"))

        self.setGeometry(500, 300, 550, 400)
        self.create_menu()  # calls this method to create the top menu

        mixer.init()

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
        self.main_v_layout = QVBoxLayout()
        self.buttons_h_layout = QHBoxLayout()  # create the h. layout for the buttons
        self.centralwidget = QWidget(MainWindow)  # creates the central widget and sets the parent to MainWindow
        self.centralwidget.setObjectName("centralwidget")

        """
        This part of the code is dedicated to creating the buttons for playing media.
        Three buttons are defined: one for returning to the previous track, one for playing/pausing
        the current track and one for getting to the next track.
        """

        self.trackList = QListWidget(self.centralwidget)
        self.trackList.setGeometry(25, 250, 500, 70)
        self.trackList.clicked.connect(self.track_selected)

        self.playButton = QPushButton(self.centralwidget)
        self.playButton.setObjectName("playButton")  # sets obj name
        self.playButton.setCheckable(True)
        self.playButton.setGeometry(240, 170, 70, 50)  # sets position and dimensions: x,y,width, height
        self.playButton.setText("Play")  # sets the button's text

        self.backButton = QPushButton(self.centralwidget)
        self.backButton.setObjectName("backButton")
        self.backButton.setGeometry(150, 170, 70, 50)
        self.backButton.setText("Previous")

        self.forwardButton = QPushButton(self.centralwidget)
        self.forwardButton.setObjectName("backButton")
        self.forwardButton.setGeometry(330, 170, 70, 50)
        self.forwardButton.setText("Next")

        self.playButton.clicked.connect(self.play_pause)
        self.backButton.clicked.connect(self.previous)
        self.forwardButton.clicked.connect(self.next)

        self.buttons_h_layout.addWidget(self.backButton)
        self.buttons_h_layout.addWidget(self.playButton)
        self.buttons_h_layout.addWidget(self.forwardButton)

        MainWindow.setCentralWidget(self.centralwidget)  # sets the window's main widget

        self.main_v_layout.addLayout(self.buttons_h_layout)
        self.main_v_layout.addWidget(self.trackList)

    def play_pause(self):
        if self.playButton.isChecked():
            self.playButton.setText("Play")
            mixer.music.pause()
        else:
            self.playButton.setText("Pause")
            mixer.music.unpause()

    def previous(self):
        tracks = DLL.DLL()  # creates a doubly linked list

        # tracks = [self.trackList.item(x).text() for x in range(self.trackList.count()-1)]
        for key in self.tracksD.keys():
            if key == self.track:
                tracks.InsertToEnd(key)  # DLL
                playingNode = tracks.TraverseDLL(True, False, False)
                continue
            tracks.InsertToEnd(key)  # DLL
            print(f"[DICT KEY] {key}")

        tName = str(tracks.TraverseDLL(True, False, True))
        previousPath = self.tracksD[tName]
        tracks.TraverseDLL(True, False, True)
        # try:
        #     print(tracks)  # DLL
        #     previous = tracks.index(self.trackList.currentItem().text()) - 1  # LL load the previous element
        #     previousPath = self.tracksD[str(tracks[previous])]  ###             #LL load the element
        #     print(previousPath)
        #     self.playingPrev = True
        #     if str(tracks.index(Path(previousPath).name)) == tracks[previous]:
        #         previous -= 1
        #         # previousPath = self.tracksD[str(tracks[previous])]
        #         # mixer.music.load(previousPath)
        #         # mixer.music.play()
        #     else:
        mixer.music.load(previousPath)
        mixer.music.play()

    # self.playButton.setText("Pause")

    # except Exception as E:
    #     with open("report.txt", "w") as f:
    #         f.write("Line 109 " + str(E))

    def next(self):
        tracks = DLL.DLL()  # creates a doubly linked list

        # tracks = [self.trackList.item(x).text() for x in range(self.trackList.count()-1)]
        for key in self.tracksD.keys():
            if key == self.track:
                node = tracks.InsertToEnd(key)  # DLL
                playingNode = tracks.TraverseDLL(False, True, False)
            tracks.InsertToEnd(key)  # DLL
            print(f"[DICT KEY] {key}")

        tName = str(tracks.TraverseDLL(True, False, False).next.data)
        nextPath = self.tracksD[tName]
        tracks.TraverseDLL(True, False, True, True)
        mixer.music.load(nextPath)
        mixer.music.play()

    def track_selected(self):
        try:
            self.track = self.trackList.currentItem().text()
            # track = track.text()
            self.setWindowTitle(f"Audio player - Playing: {self.track}")
            mixer.music.load(self.tracksD[f"{self.track}"])
            mixer.music.play()
            self.playButton.setText("Pause")
            # self.play_pause(self.tracksD[f"{track}"])
            print(self.tracksD[f"{self.track}"])
        except Exception as E:
            with open("report.txt", "w") as f:
                f.write("Line 105 " + str(E))

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

        """ #OLD
        list(Path.glob(Path(self.folderPath), "*", recursive=False))
                for i in range(len(allFiles)):
            if allFiles[i].suffix == ".mp3" or allFiles[i].suffix == ".wav":
                print(allFiles[i])
            else:
                pass
                # allFiles.pop(i)
        """
        # print(self.folderPath, f"\n {allFiles}")

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
    window.add_to_list(window.allFiles)

    window.show()
    sys.exit(app.exec())
