"""
Album cover widget
"""

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize

from Common.image_utils import get_rounded_pixmap

ALBUM_COVER = "resource/images/test-images/album-cover-test-2.jpg"


class AlbumCoverWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_ui()

    def setup_ui(self):
        self.cover_layout = QHBoxLayout()
        self.cover_layout.setContentsMargins(0, 0, 0, 0)
        self.album_cover_label = QLabel()
        self.album_cover_label.setFixedSize(QSize(210, 210))

        pixmap = QPixmap()
        pixmap.load(ALBUM_COVER)
        modified_pixmap = get_rounded_pixmap(
            pixmap.scaled(
                200,
                200,
                aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                transformMode=Qt.TransformationMode.SmoothTransformation,
            ),
            radius=10,
        )
        self.album_cover_label.setPixmap(modified_pixmap)
        self.album_cover_label.setObjectName("albumCover")
        self.cover_layout.addWidget(self.album_cover_label)

        self.setLayout(self.cover_layout)
