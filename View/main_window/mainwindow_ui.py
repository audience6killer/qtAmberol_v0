"""
Main window layout
"""
from dataclasses import dataclass
from enum import Enum

from PyQt5.QtWidgets import QMdiArea
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QImage, QBrush
from PyQt5.QtCore import Qt, QSize, QPointF, QPropertyAnimation

from qframelesswindow import FramelessMainWindow, StandardTitleBar, FramelessWindow

from Components.media_player.media_player import MediaPlayer
from Components.media_player.media_playlist import MediaPlaylist
from Components.media_player.song_info import SongInfo

from .ui_widget_handler import UIWidgetHandler

from Common.image_utils import ColorPalette
from Common.style_sheet import setStyleSheet, determine_color_degradation
from Common.signal_bus import signal_bus

from Common import resources


class MainWindowUI(FramelessMainWindow):
    repaint_flag = False
    BG_STYLES = Enum("BG_Styles", ['PRIMARY', 'LESS_CONTRAST'])

    def __init__(self, parent=None):
        # Window configuration
        super().__init__(parent=parent)

        self.player = MediaPlayer()
        self.playlist = MediaPlaylist()
        self.player.setPlaylist(self.playlist)
        self.size()

        self.__last_volume = 100
        self.colors = None
        self._state_colors = None  # list[QColor]

        self._current_bg_style = self.BG_STYLES.LESS_CONTRAST
        self._min_contrast_palette: list = []
        self._primary_color_palette: list = []

        self.initWindow()

        self.ui_handler = UIWidgetHandler(self)
        self.setCentralWidget(self.ui_handler)

    def initWindow(self):
        """Initialize window"""
        self.titleBar.maxBtn.hide()
        self.titleBar.minBtn.hide()
        self.titleBar.closeBtn.hide()
        self.setWindowTitle("qtAmberol")

        self.setFixedSize(QSize(600, 700))

        # set window stylesheet
        self.setObjectName("main_window")
        self.setQss()

        self.connectSignalsToSlots()

        self.show()

    def setQss(self):
        """ Generate qss and apply """
        setStyleSheet(self, self._state_colors)

    def updateUIColors(self, cover: QImage):
        colors = ColorPalette(cover)
        self._min_contrast_palette = colors.get_min_contrast_palette()
        self._primary_color_palette = colors.get_primary_min_contrast_palette()

        if self._current_bg_style == self.BG_STYLES.LESS_CONTRAST:
            self.colors = self._min_contrast_palette
        else:
            self.colors = self._primary_color_palette

        dominant_color = colors.get_dominant_color()
        self._state_colors = determine_color_degradation(dominant_color)

        signal_bus.gradient_colors_updated_signal.emit(self.colors)
        signal_bus.state_colors_updated_signal.emit(self._state_colors)

    def paintEvent(self, event):
        """ Paint widget event """
        if self.repaint_flag:
            self.gradientPaint(event)
        else:
            super(MainWindowUI, self).paintEvent(event)

    def gradientPaint(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

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

    def connectSignalsToSlots(self):
        """Connect signals to slots"""
        signal_bus.toggle_play_state_signal.connect(self.togglePlayState)
        signal_bus.playlist_track_changed_signal.connect(self.currentTrackChanged)
        signal_bus.toggle_mute_volume_signal.connect(self.player.setMuteState)
        signal_bus.increase_volume_signal.connect(self.increaseVolumeEvent)
        signal_bus.volume_scroll_changed_signal.connect(self.volumeScrollEvent)
        signal_bus.progress_bar_clicked_value_signal.connect(self.setTrackPosition)
        signal_bus.alternate_background_style.connect(self.alternateBackgroundStyle)

        signal_bus.close_window_signal.connect(self.close)

    def setTrackPosition(self, new_pos):
        """Set new track position"""
        self.player.setNewPosition(new_pos)

    def volumeScrollEvent(self, value: int):
        """Volume scroll event"""
        volume_value = 5 * round(value / 5)
        self.player.setVolume(volume_value)

    def increaseVolumeEvent(self):
        """Increases the volume by 10%"""
        self.player.increaseVolume(5)

    def togglePlayState(self):
        """Toggle play state"""
        print("Toggle Play State")
        self.player.togglePlayState()

    def currentTrackChanged(self, metadata: SongInfo):
        """Track Metadata Changed"""
        duration = metadata.duration
        if duration:
            signal_bus.update_track_duration_signal.emit(duration)

        cover = metadata.album_cover
        self.updateUIColors(cover)
        self.repaintWidget()

    def repaintWidget(self):
        """A new track has been loaded, so the widget gradient should be repainted"""
        self.setQss()
        self.repaint_flag = True
        self.update()

    def alternateBackgroundStyle(self):
        if self._current_bg_style == self.BG_STYLES.LESS_CONTRAST:
            self.colors = self._primary_color_palette
            self._current_bg_style = self.BG_STYLES.PRIMARY
        else:
            self.colors = self._min_contrast_palette
            self._current_bg_style = self.BG_STYLES.LESS_CONTRAST

        signal_bus.gradient_colors_updated_signal.emit(self.colors)
        self.repaintWidget()

