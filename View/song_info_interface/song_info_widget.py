""" Song Info Widget """

from PyQt5.QtWidgets import QLabel, QSizePolicy, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt


class SongInfoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout
        self.info_layout = QVBoxLayout()

        # Info labels
        self.track_title = QLabel()
        self.track_artist = QLabel()
        self.track_album = QLabel()

        self.setup_ui()

    def setup_ui(self):

        self.track_title.setObjectName("track-title")
        self.track_artist.setObjectName("track-artist")
        self.track_album.setObjectName("track-album")

        self.track_title.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        )
        self.track_artist.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        )
        self.track_album.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        )
        self.track_title.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        self.track_album.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        self.track_artist.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )

        self.track_title.setText("Girl Friend")
        self.track_album.setText("Midori")
        self.track_artist.setText("飯島真理")

        self.info_layout.addWidget(self.track_title)
        self.info_layout.addWidget(self.track_artist)
        self.info_layout.addWidget(self.track_album)

        # The layout is set in parent
        self.setLayout(self.info_layout)

    def update_info(self, info: dict):
        """Update song info"""
        self.track_title.setText(info['Title'])
        self.track_artist.setText(info['AlbumArtist'])
        self.track_album.setText(info['AlbumTitle'])
