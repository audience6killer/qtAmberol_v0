import os

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl

from Common.metasingleton import Singleton
from Common.signal_bus import signal_bus

class MediaPlayer(QMediaPlayer):
    """Media player class"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setNotifyInterval(500)
        self._current_playlist_track = 0
        self._last_volume = self.volume()

        self.__connectSignalsToSlots()

    def togglePlayState(self):
        """Toggle Play State"""
        if self.state() == QMediaPlayer.PlayingState:
            self.pause()
        elif self.state() in (QMediaPlayer.PausedState, QMediaPlayer.StoppedState):
            self.play()
        else:
            pass

    def trackSelected(self):
        """If a track was selected from the playlist"""
        if self.state() in (QMediaPlayer.PausedState, QMediaPlayer.StoppedState):
            self.play()
            signal_bus.set_play_state_signal.emit()

    def __connectSignalsToSlots(self):
        """Connect signals to slots"""
        signal_bus.media_player_toggle_play_state_signal.connect(self.trackSelected)
        self.volumeChanged.connect(signal_bus.volume_changed_event)
        self.positionChanged.connect(self.trackPositionChangedEvent)
        self.error.connect(self.handleErrorSlot)

    def handleErrorSlot(self, error):
        print("Error occurred:", error, self.errorString())

    def trackPositionChangedEvent(self, value):
        """Position in the track changed"""
        if self.state() == self.State.PlayingState:
            signal_bus.track_position_changed_signal.emit(value)

    def setNewPosition(self, pos):
        """Set new track position"""
        new_pos = (pos / 100) * self.duration()
        self.setPosition(int(new_pos))

    def setMuteState(self, is_muted: bool):
        if is_muted:
            self._last_volume = self.volume()
            self.setMuted(True)
        else:
            self.setVolume(self._last_volume)

    def increaseVolume(self, increment: int):
        new_value = increment + self.volume()
        if self.isMuted():
            new_value = increment

        if new_value <= 100:
            print(f"Current volume {new_value}")
            self.setVolume(new_value)

    def setVolume(self, volume):
        if self.isMuted():
            self.setMuted(False)
        signal_bus.volume_changed_event.emit(volume)
        super(MediaPlayer, self).setVolume(volume)


