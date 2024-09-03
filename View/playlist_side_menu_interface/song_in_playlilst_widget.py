from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QScrollArea

from Components.media_player.song_info import SongInfo
from Components.marquee_label import MarqueeLabel

from Common.image_utils import get_rounded_pixmap
from Common import resources, signal_bus


class SongInPlaylistWidget(QWidget):

    def __init__(self, metadata: SongInfo, parent=None):
        super(SongInPlaylistWidget, self).__init__(parent)

        self._is_playing = False
        self._is_scrolling = False

        self.album_cover_label = QLabel()
        self.track_title_label = MarqueeLabel()
        self.artist_label = MarqueeLabel()

        self.playing_symbol = QLabel()

        self.main_layout = QHBoxLayout()

        self.setupUI()

        self.setQss()

        self.setTrackData(metadata)

    @property
    def isPlaying(self):
        return self._is_playing

    @isPlaying.setter
    def isPlaying(self, value: bool):
        self._is_playing = value
        if self._is_playing:
            self.playing_symbol.show()
            self.startScrolling()
        else:
            self.playing_symbol.hide()
            self.stopScrolling()

    @property
    def isScrolling(self):
        return self._is_scrolling

    @isScrolling.setter
    def isScrolling(self, value: bool):
        self._is_scrolling = value
        if self.isScrolling and self.isPlaying:
            self.startScrolling()
        elif not self._is_scrolling:
            self.stopScrolling()

    def setupUI(self):
        """Setup UI"""
        self.album_cover_label.setObjectName("album-cover")
        self.artist_label.setObjectName("artist-label")
        self.track_title_label.setObjectName("track-title-label")
        self.playing_symbol.setObjectName("playing-svg")

        self.artist_label.setText("Unknown Artist")
        self.track_title_label.setText("Unknown Title")
        default_pixmap = QPixmap(":/images/cover_art/album-cover-small.png")
        modified_pixmap = get_rounded_pixmap(default_pixmap, radius=5)
        self.album_cover_label.setPixmap(modified_pixmap)

        self.album_cover_label.setFixedSize(50, 50)
        self.playing_symbol.setFixedSize(20, 20)
        self.playing_symbol.setPixmap(QPixmap(":/images/sidebar/playing.svg"))

        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(5, 0, 0, 0)
        spacer = QSpacerItem(8, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        info_layout.addSpacerItem(spacer)
        info_layout.addWidget(self.track_title_label)
        info_layout.addWidget(self.artist_label)
        info_layout.addSpacerItem(spacer)

        self.main_layout.addWidget(self.album_cover_label)
        self.main_layout.addLayout(info_layout)
        playing_spacer = QSpacerItem(10, 50, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.main_layout.addSpacerItem(playing_spacer)
        self.main_layout.addWidget(self.playing_symbol)
        self.main_layout.setContentsMargins(8, 3, 8, 3)
        # self.main_layout.setSpacing(1)

        self.playing_symbol.hide()
        self.setLayout(self.main_layout)

    def setQss(self):
        self.setStyleSheet("""
            QLabel#track-title-label {
                font-weight: bold;
                font-size: 13px;
            }
            QLabel#artist-label {
                font-size: 12px;
            }
        """)

    def setTrackData(self, data: SongInfo):
        """Set track data"""
        self.artist_label.setText(data.artist)
        self.track_title_label.setText(data.title)

        modified_pixmap = get_rounded_pixmap(
            data.album_cover.scaled(
                50,
                50,
                aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                transformMode=Qt.TransformationMode.SmoothTransformation,
            ),
            radius=5
        )
        self.album_cover_label.setPixmap(modified_pixmap)

    def startScrolling(self):
        self.track_title_label.is_scrolling = True
        self.artist_label.is_scrolling = True

    def stopScrolling(self):
        self.track_title_label.is_scrolling = False
        self.artist_label.is_scrolling = False

