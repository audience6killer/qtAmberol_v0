"""
Custom main widget
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QLinearGradient
from PyQt5.QtCore import Qt, QPointF
from Common.image_utils import get_image_color_palette

ALBUM_COVER = "resource/images/test-images/album-cover-test-3.jpg"

class CustomWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)


    def paintEvent(self, event):
        self.colors = get_image_color_palette(ALBUM_COVER)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Define the background colors
        background_colors = [
            QColor(
                self.colors[0][0], self.colors[0][1], self.colors[0][2]
            ),  # Sample background color 0
            QColor(
                self.colors[2][0], self.colors[2][1], self.colors[2][2]
            ),  # Sample background color 0Color(),  # Sample background color 1
            QColor(
                self.colors[1][0], self.colors[1][1], self.colors[1][2]
            ),  # Sample background color 0QColor(0, 0, 255)  # Sample background color 2
        ]

        # Define the gradient angles
        gradient_angles = [
            (QPointF(0, 0), QPointF(self.width(), self.height())),
            (QPointF(0, self.height()), QPointF(self.width(), 0)),
            (QPointF(self.width(), 0), QPointF(0, self.height())),
        ]

        for i, (start_point, end_point) in enumerate(gradient_angles):
            gradient = QLinearGradient(start_point, end_point)

            # Set the color stops with varying opacity
            gradient.setColorAt(0, background_colors[i].lighter(120))
            gradient.setColorAt(
                0.7071,
                QColor(
                    background_colors[i].red(),
                    background_colors[i].green(),
                    background_colors[i].blue(),
                    0,
                ),
            )

            painter.setBrush(gradient)
            painter.drawRect(self.rect())
