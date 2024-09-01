"""
Album cover interface
"""

from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal

from Components.media_player.song_info import SongInfo
from .album_cover_widget import AlbumCoverWidget

from Common.signal_bus import signal_bus


class AlbumCoverInterface(QWidget):

    songCoverNext = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_layout = QVBoxLayout()

        self.album_cover = AlbumCoverWidget()
        self.setup_ui()

        self.__connectSignalsToSlots()

    def setup_ui(self):
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.album_cover)

        self.setLayout(self.main_layout)

    def updateCoverImage(self, metadata: SongInfo):
        """Update cover image"""
        self.album_cover.updateCoverArt(metadata.album_cover)

    def __connectSignalsToSlots(self):
        """connect signals to slots"""
        signal_bus.playlist_track_changed_signal.connect(self.updateCoverImage)
