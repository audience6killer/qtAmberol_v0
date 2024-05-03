"""
Album cover widget
"""

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QGraphicsDropShadowEffect

from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt, QSize

from Common.image_utils import get_rounded_pixmap

ALBUM_COVER = "resource/images/test-images/album-cover-test-4.jpg"


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
        self.album_cover_label.setObjectName("album-cover")
        # creating a QGraphicsDropShadowEffect object
        shadow = QGraphicsDropShadowEffect()

        # setting blur radius
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.album_cover_label.setGraphicsEffect(shadow)

        self.cover_layout.addWidget(self.album_cover_label)

        self.setLayout(self.cover_layout)
