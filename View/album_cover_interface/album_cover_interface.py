"""
Album cover interface
"""

from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal

from .album_cover_widget import AlbumCoverWidget


class AlbumCoverInterface(QWidget):

    songCoverNext = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_layout = QVBoxLayout()

        self.album_cover = AlbumCoverWidget()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout.addWidget(self.album_cover)

        self.setLayout(self.main_layout)

    def updateCoverImage(self, arg):
        pass
