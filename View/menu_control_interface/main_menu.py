
from PyQt5.QtWidgets import QMenu, QAction, QFileDialog, QStyle, QStyleOptionMenuItem
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QRegion, QKeySequence
from PyQt5.QtCore import Qt

from Common.signal_bus import signal_bus


class MainMenu(QMenu):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setupUI()


    def setupUI(self):
        """Setup UI"""
        #self.setStyleSheet("""
        #    QMenu {
        #        background-color: white;
        #        border: 1px solid black;
        #        border-radius: 10px;  /* Rounded corners */
        #        padding: 2px;  /* Add padding for better fit */
        #    }
        #    QMenu::item {
        #        background-color: transparent;
        #        border-radius: 8px; /* Ensure items have rounded corners too */
        #        margin: 1px 2px;  /* Adjust margin for better fit */
        #        padding: 4px 8px;  /* Adjust padding for better fit */
        #    }
        #    QMenu::item:selected {
        #        background-color: lightblue;
        #    }
        #    QMenu::separator {
        #        height: 1px;
        #        background: black;
        #        margin-left: 10px;
        #        margin-right: 10px;
        #    }
        #""")
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setObjectName('main-menu')
        self.add_song_option = QAction("Add Song", self)
        self.add_folder_option = QAction("Add Folder", self)
        self.clear_playlist_option = QAction("Clear", self)

        self.add_song_option.setShortcut(QKeySequence("Ctrl+s"))
        self.add_folder_option.setShortcut(QKeySequence("Ctrl+a"))
        self.clear_playlist_option.setShortcut(QKeySequence("Ctrl+L"))

        self.match_cover_art_option = QAction("Match Cover Art", self)
        self.about_option = QAction("About", self)

        self.addAction(self.add_song_option)
        self.addAction(self.add_folder_option)
        self.addAction(self.clear_playlist_option)
        self.addSeparator()

        self.addAction(self.match_cover_art_option)
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
        #self.add_folder_option.triggered.connect()
        self.add_song_option.triggered.connect(self.handleOpenFile)

    def handleOpenFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "/media/vill4in/DATA/Music",
                                                   "Audio Files (*.mp3 *.wav *.ogg *.flac *.m4a);;All Files (*)",
                                                   options=options)
        if file_name:
            print("Selected file:", file_name)
            signal_bus.open_file_signal.emit(file_name)

    def openMenu(self, pos):
        """Open main menu popup"""
        self.exec_(pos)
        signal_bus.repaint_main_window_signal.emit()



