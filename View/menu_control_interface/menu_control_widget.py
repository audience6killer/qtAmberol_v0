"""
Menu control widget
"""

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from Common import resources


class MenuControlWidget(QWidget):
    def __init__(self, parent=None):

        super().__init__(parent)

        self.main_layout = QHBoxLayout()

        self.menu_button = QPushButton()

        self.shuffle_playlist = QPushButton()

        self.enable_repeat = QPushButton()

        self.playlist_button = QPushButton()

        self.setup_ui()

    def setup_ui(self):
        """Setup layout"""

        self.main_layout.setContentsMargins(100, 0, 100, 0)

        self.menu_button.setCheckable(True)
        self.shuffle_playlist.setCheckable(True)
        self.playlist_button.setCheckable(True)
        self.enable_repeat.setCheckable(True)

        self.menu_button.setObjectName("menu-button")
        self.shuffle_playlist.setObjectName("shuffle-button")
        self.enable_repeat.setObjectName("repeat-button")
        self.playlist_button.setObjectName("playlist-button")

        self.shuffle_playlist.setIcon(QIcon(":/images/menu_control/shuffle.svg"))
        self.shuffle_playlist.setFixedSize(QSize(30, 30))

        self.enable_repeat.setIcon(QIcon(":/images/menu_control/repeat.svg"))
        self.enable_repeat.setFixedSize(QSize(30, 30))

        self.menu_button.setIcon(QIcon(":/images/menu_control/menu.svg"))
        self.menu_button.setFixedSize(QSize(30, 30))

        self.playlist_button.setIcon(QIcon(":/images/menu_control/playlist.svg"))
        self.playlist_button.setFixedSize(QSize(30, 30))

        self.main_layout.addWidget(self.playlist_button)
        self.main_layout.addWidget(self.shuffle_playlist)
        self.main_layout.addWidget(self.enable_repeat)
        self.main_layout.addWidget(self.menu_button)

        self.setWidgetsTooltip()

        self.setLayout(self.main_layout)

    def setWidgetsTooltip(self):
        """ Set tooltip for all buttons"""
        self.menu_button.setToolTip("Main menu")
        self.enable_repeat.setToolTip("Enable repeat")
        self.playlist_button.setToolTip("Show playlist")
        self.shuffle_playlist.setToolTip("Shuffle playlist")
