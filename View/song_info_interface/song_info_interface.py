"""
Song info interface
"""

from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal

from Components.media_player.song_info import SongInfo
from .song_info_widget import SongInfoWidget

from Common.signal_bus import signal_bus


class SongInfoInterface(QWidget):

    song_info_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.info_widget = SongInfoWidget(parent)

        self.main_layout = QVBoxLayout()

        self.main_layout.addWidget(self.info_widget)

        self.setLayout(self.main_layout)

        self.__connectSignalsToSlots()

    def update_song_info(self, info: SongInfo):
        self.info_widget.update_info(info)

    def __connectSignalsToSlots(self):
        """Connect signals to slots"""
        signal_bus.playlist_track_changed_signal.connect(self.update_song_info)
