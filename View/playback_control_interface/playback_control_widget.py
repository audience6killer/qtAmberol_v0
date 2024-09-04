"""
Playback control widget
"""

from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon

from Components.media_player.media_player import MediaPlayer
from Common.signal_bus import signal_bus
from Common import resources


class PlaybackControlWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout
        self.main_layout = QHBoxLayout()

        self.play_pause_icons = [QPixmap(':/images/playback_control/play.svg'),
                                 QPixmap(':/images/playback_control/pause.svg')]
        # Control buttons
        self.play_button = QPushButton()
        self.next_button = QPushButton()
        self.previous_button = QPushButton()

        self.media_player = MediaPlayer()

        self.__is_playing = False
        self.setup_ui()

    def setup_ui(self):
        """Setup ui"""
        self.play_button.setIcon(QIcon(self.play_pause_icons[0]))
        self.next_button.setIcon(QIcon(QPixmap(":/images/playback_control/next.svg")))
        self.previous_button.setIcon(
            QIcon(QPixmap(":/images/playback_control/previous.svg"))
        )

        self.play_button.setObjectName("play-button")
        self.next_button.setObjectName("next-button")
        self.previous_button.setObjectName("previous_button")

        self.play_button.setFixedSize(QSize(50, 50))
        self.next_button.setFixedSize(QSize(50, 50))
        self.previous_button.setFixedSize(QSize(50, 50))

        self.main_layout.addWidget(self.previous_button)
        self.main_layout.addWidget(self.play_button)
        self.main_layout.addWidget(self.next_button)

        self.setWidgetsTooltip()

        # We add the control layout to the main layout
        self.setLayout(self.main_layout)

        self.__connectSignalsToSlots()

    def setWidgetsTooltip(self):
        """ Sets tooltip for all buttons"""
        self.play_button.setToolTip("Play")
        self.next_button.setToolTip("Next")
        self.previous_button.setToolTip("Previous")

    def __connectSignalsToSlots(self):
        """Connect widgets signals to slots"""
        self.play_button.clicked.connect(self.playButtonControl)
        self.next_button.clicked.connect(signal_bus.next_song_signal)
        self.previous_button.clicked.connect(signal_bus.previous_song_signal)
        signal_bus.set_play_state_signal.connect(self.setPlayState)

    def setPlayState(self):
        self.__is_playing = True
        self.play_button.setIcon(QIcon(self.play_pause_icons[1]))

    def playButtonControl(self):
        """Play button control"""
        signal_bus.toggle_play_state_signal.emit()
        self.__is_playing = not self.__is_playing
        if self.__is_playing:
            self.play_button.setIcon(QIcon(self.play_pause_icons[1]))
        else:
            self.play_button.setIcon(QIcon(self.play_pause_icons[0]))

        self.play_button.update()

    def restart_state(self):
        """Restate states"""
        self.play_button.setIcon(QIcon(self.play_pause_icons[0]))
        self.__is_playing = False
