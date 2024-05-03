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

        self.setup_ui()

    def setup_ui(self):
        """Setup layout"""

        self.main_layout.setContentsMargins(110, 0, 110, 0)

        self.menu_button.setObjectName("menu-button")
        self.shuffle_playlist.setObjectName("shuffle-button")
        self.enable_repeat.setObjectName("repeat-button")

        self.shuffle_playlist.setIcon(QIcon(":/images/menu_control/shuffle.svg"))
        self.shuffle_playlist.setFixedSize(QSize(30, 30))

        self.enable_repeat.setIcon(QIcon(":/images/menu_control/repeat.svg"))
        self.enable_repeat.setFixedSize(QSize(30, 30))

        self.menu_button.setIcon(QIcon(":/images/menu_control/menu.svg"))
        self.menu_button.setFixedSize(QSize(30, 30))

        self.main_layout.addWidget(self.menu_button)
        self.main_layout.addWidget(self.shuffle_playlist)
        self.main_layout.addWidget(self.enable_repeat)

        self.setLayout(self.main_layout)
