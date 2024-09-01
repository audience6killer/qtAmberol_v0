from pathlib import Path
from typing import Union

from PyQt5.QtCore import QUrl, QByteArray
from PyQt5.QtGui import QImage
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent, QMediaPlayer

from tinytag import TinyTag

from Common import signal_bus
from .song_info import SongInfo


class MediaPlaylist(QMediaPlaylist):

    def __init__(self, parent=None):
        super(MediaPlaylist, self).__init__(parent)

        self.tracklist: list[SongInfo] = []
        self.setPlaybackMode(QMediaPlaylist.Sequential)

        self.__connectSignalsToSlots()

    def __connectSignalsToSlots(self):
        signal_bus.open_file_signal.connect(self.addSong)
        signal_bus.open_folder_signal.connect(self.addFolderTracks)
        signal_bus.next_song_signal.connect(self.next)
        signal_bus.previous_song_signal.connect(self.previous)
        signal_bus.playlist_track_clicked_index_signal.connect(self.changeTrack)
        self.currentIndexChanged.connect(self.trackChanged)

    def addSong(self, filepath: Union[str, Path]):
        """Add song to playlist"""
        if not isinstance(filepath, Path):
            filepath = Path(filepath)

        track_metadata = TinyTag.get(filepath, image=True)
        track_info = SongInfo(
            file=str(filepath),
            title=track_metadata.title or 'Unknown Title',
            artist=track_metadata.artist or track_metadata.albumartist or 'Unknown Artist',
            album=track_metadata.album or 'UnknownAlbum',
            album_cover=QImage.fromData(track_metadata.get_image()) or QImage(":/images/cover_art/album-cover.png"),
            duration=track_metadata.duration or 0
        )
        self.tracklist.append(track_info)
        self.addMedia(QMediaContent(QUrl.fromLocalFile(str(filepath))))
        signal_bus.track_added_to_playlist_signal.emit(track_info)

        if len(self.tracklist) == 1:
            self.setCurrentIndex(0)

    def addFolderTracks(self, tracklist: list):
        """Add tracks in directory"""
        for track in tracklist:
            self.addSong(track)

    def trackChanged(self, index):
        """Track changed"""
        signal_bus.playlist_track_changed_signal.emit(self.tracklist[index])
        signal_bus.playlist_current_track_index_signal.emit(index)

    def changeTrack(self, index: int):
        self.setCurrentIndex(index)





