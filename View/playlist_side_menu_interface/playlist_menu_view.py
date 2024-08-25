from signal import signal

from PyQt5.QtGui import QPainter, QColor, QLinearGradient
from PyQt5.QtWidgets import QMdiSubWindow
from PyQt5.QtCore import Qt, QPointF, QSize, QEvent

from Common.signal_bus import signal_bus

from .playlist_side_menu_interface import PlaylistSideMenuInterface


class PlaylistMenuView(QMdiSubWindow):

    def __init__(self, parent=None):
        super(PlaylistMenuView, self).__init__(parent)

        self.window_size = parent.size()    # QSize
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.colors = None
        self.widget = PlaylistSideMenuInterface(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle("Playlist window")
        self.setWidget(self.widget)
        self.__connectSignalsToSlots()

        self.hide()

    def __connectSignalsToSlots(self):
        """Connect signals to slots"""
        signal_bus.gradient_colors_updated_signal.connect(self.setGradientColors)

    def setGradientColors(self, colors: list):
        """Gradient colors was updated"""
        self.colors = colors
        self.update()

    def paintEvent(self, event):
        """Paint event"""
        if self.colors is not None:
            self.gradientPaint(event)
        else:
            super(PlaylistMenuView, self).paintEvent(event)

    def gradientPaint(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set the background brush to transparent
        painter.setBrush(Qt.NoBrush)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        # Define the background colors
        background_colors = [
            QColor(
                self.colors[0][0], self.colors[0][1], self.colors[0][2], int(255 * 0.7)
            ),  # Sample background color 0
            QColor(
                self.colors[1][0], self.colors[1][1], self.colors[1][2], int(255 * 0.7)
            ),  # Sample background color 0Color(),  # Sample background color 1
            QColor(
                self.colors[2][0], self.colors[2][1], self.colors[2][2], int(255 * 0.7)
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


