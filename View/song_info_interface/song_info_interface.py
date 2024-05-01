"""
Song info interface
"""

from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal

from .song_info_widget import SongInfoWidget


class SongInfoInterface(QWidget):

    song_info_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.info_widget = SongInfoWidget(parent)

        self.main_layout = QVBoxLayout()

        self.main_layout.addWidget(self.info_widget)

        self.setLayout(self.main_layout)

    def update_song_info(self, info: list):
        self.info_widget.update_info(info)
