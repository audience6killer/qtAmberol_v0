import os

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl

from Common.metasingleton import Singleton
from Common.signal_bus import signal_bus

class MediaPlayer(QMediaPlayer):
    """Media player class"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.__connectSignalsToSlots()

    def loadTrack(self, file_path: str):
        """Load new track to player"""
        #print("Setting new track")
        self.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        pass

    def togglePlayState(self):
        """Toggle Play State"""
        #print(f"Playing State: {self.state()}")
        if self.state() == QMediaPlayer.PlayingState:
            self.pause()
        elif self.state() in (QMediaPlayer.PausedState, QMediaPlayer.StoppedState):
            self.play()
        else:
            pass

    def __connectSignalsToSlots(self):
        """Connect signals to slots"""
        self.mediaStatusChanged.connect(self.trackMetadataChanged)
        self.positionChanged.connect(self.trackPositionChangedEvent)

        self.error.connect(self.handleErrorSlot)

    def trackMetadataChanged(self, status):
        if self.isMetaDataAvailable() and status == QMediaPlayer.LoadedMedia:
            metadata_keys = self.availableMetaData()
            metadata = {key: self.metaData(key) for key in metadata_keys}
            print("Metadata:", metadata)
            signal_bus.metadata_song_signal.emit(metadata)

        else:
            print("There's no metadata to show!!!")

    def handleErrorSlot(self, error):
        print("Error occurred:", error, self.errorString())

    def playerStatusChanged(self, status):
        if status == QMediaPlayer.LoadingMedia:
            print("MediaStatus.LoadingMedia")
        elif status == QMediaPlayer.StalledMedia:
            print("MediaStatus.StalledMedia")
        elif status == QMediaPlayer.InvalidMedia:
            print("MediaStatus.InvalidMedia")
        elif status == QMediaPlayer.UnknownMediaStatus:
            print("MediaStatus.UnknownMediaStatus")
        elif status == QMediaPlayer.NoMedia:
            print("MediaStatus.NoMedia")
        elif status == QMediaPlayer.LoadedMedia:
            print("MediaStatus.LoadedMedia")
        elif status == QMediaPlayer.BufferingMedia:
            print("MediaStatus.BufferingMedia")
        elif status == QMediaPlayer.BufferedMedia:
            print("MediaStatus.BufferedMedia")
        elif status == QMediaPlayer.EndOfMedia:
            print("MediaStatus.EndOfMedia")
        elif status == QMediaPlayer.NetworkError:
            print("MediaStatus.NetworkError")
        elif status == QMediaPlayer.FormatError:
            print("MediaStatus.FormatError")
        elif status == QMediaPlayer.AccessDeniedError:
            print("MediaStatus.AccessDeniedError")
        elif status == QMediaPlayer.ServiceMissingError:
            print("MediaStatus.ServiceMissingError")
        else:
            print("Other Status")

    def trackPositionChangedEvent(self, value):
        c_time = value
        l_time = self.duration() - c_time



#player = MediaPlayer()