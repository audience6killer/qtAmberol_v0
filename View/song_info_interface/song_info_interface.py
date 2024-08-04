"""
Song info interface
"""

from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal

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

    def update_song_info(self, info: dict):
        self.info_widget.update_info(info)

    def __connectSignalsToSlots(self):
        """Connect signals to slots"""
        signal_bus.metadata_song_signal.connect(self.trackMetadataChanged)

    def trackMetadataChanged(self, values: dict):
        """Track metadata changed"""
        song_metadata = {}
        if 'AlbumArtist' in values:
            song_metadata['Artist'] = values['AlbumArtist']
        elif 'Artist' in values:
            song_metadata['Artist'] = values['Artist']
        elif 'ContributingArtist' in values:
            song_metadata['Artist'] = values['ContributingArtist']
        else:
            song_metadata['Artist'] = 'Unknown Artist'

        if 'Title' not in values:
            song_metadata['Title'] = 'Unknown Title'
        else:
            song_metadata['Title'] = values['Title']

        if 'AlbumTitle' not in values:
            song_metadata['AlbumTitle'] = 'Unknown Album'
        else:
            song_metadata['AlbumTitle'] = values['AlbumTitle']

        self.update_song_info(song_metadata)
