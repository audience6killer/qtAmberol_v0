import os

from PyQt5.QtWidgets import QMenu, QAction, QFileDialog, QStyle, QStyleOptionMenuItem
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QRegion, QKeySequence
from PyQt5.QtCore import Qt

from Common.signal_bus import signal_bus


class MainMenu(QMenu):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.add_song_option = None
        self.add_folder_option = None
        self.clear_playlist_option = None
        self.match_cover_art_option = None
        self.alternate_background_style = None
        self.about_option = None
        self.setupUI()


    def setupUI(self):
        """Setup UI"""
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setObjectName('main-menu')
        self.add_song_option = QAction("Add Song", self)
        self.add_folder_option = QAction("Add Folder", self)
        self.clear_playlist_option = QAction("Clear", self)

        self.add_song_option.setShortcut(QKeySequence("Ctrl+s"))
        self.add_folder_option.setShortcut(QKeySequence("Ctrl+a"))
        self.clear_playlist_option.setShortcut(QKeySequence("Ctrl+L"))

        self.match_cover_art_option = QAction("Match Cover Art", self)
        self.alternate_background_style = QAction("Alternate Background", self)
        self.about_option = QAction("About", self)

        self.addAction(self.add_song_option)
        self.addAction(self.add_folder_option)
        self.addAction(self.clear_playlist_option)
        self.addSeparator()

        self.addAction(self.match_cover_art_option)
        self.addAction(self.alternate_background_style)
        self.addSeparator()

        self.addAction(self.about_option)

        self.setStyleSheet("""
            QMenu{
                  background-color: white;
                  border-radius: 10px;
                  margin: 10px 10px;
            }
            QMenu::item {
                    background-color: transparent;
                    border-radius: 5px;
                    padding:8px 25px;
                    margin:5px 10px;
            }
            QMenu::item:selected { 
                background-color: #F5F5F5; 
                border-radius: 5px;
            }
             QMenu::separator {
                height: 1px;
                background: lightgrey;
                margin-left: 10px;
                margin-right: 10px;
            }
        """)

        self.__connectSignalsToSlots()

    def __connectSignalsToSlots(self):
        """Connect signals to slots"""
        self.add_song_option.triggered.connect(self.handleOpenFile)
        self.add_folder_option.triggered.connect(self.handleOpenFolder)
        self.alternate_background_style.triggered.connect(signal_bus.alternate_background_style)

    def handleOpenFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "/media/vill4in/DATA/Music",
                                                   "Audio Files (*.mp3 *.wav *.ogg *.flac *.m4a);;All Files (*)",
                                                   options=options)
        if file_name:
            print("Selected file:", file_name)
            signal_bus.open_file_signal.emit(file_name)

    def handleOpenFolder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        directory = QFileDialog.getExistingDirectory(self, "Select a folder", options=options)

        music_extensions = {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'}

        # Get all music file paths of the direct children in the selected directory
        if directory:
            music_files = [
                os.path.join(directory, f)
                for f in os.listdir(directory)
                if os.path.isfile(os.path.join(directory, f)) and os.path.splitext(f)[1].lower() in music_extensions
            ]

            if music_files:
                signal_bus.open_folder_signal.emit(music_files)

                # Print the music file paths
                for file_path in music_files:
                    print(file_path)

    def openMenu(self, pos):
        """Open main menu popup"""
        self.exec_(pos)



