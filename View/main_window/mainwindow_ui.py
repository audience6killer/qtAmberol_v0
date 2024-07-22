"""
Main window layout
"""

from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QImage
from PyQt5.QtCore import Qt, QSize, QPointF

from qframelesswindow import FramelessMainWindow, StandardTitleBar

from View.album_cover_interface import AlbumCoverInterface
from View.song_info_interface import SongInfoInterface
from View.progress_bar_interface import ProgressBarInterface
from View.playback_control_interface import PlaybackControlInterface
from View.volume_control_interface import VolumeControlInterface
from View.menu_control_interface import MenuControlInterface

from Components.media_player.media_player import MediaPlayer

from Common.image_utils import ColorPalette
from Common.style_sheet import setStyleSheet
from Common.parse_stylesheet import generate_css
from Common.signal_bus import signal_bus

from Common import resources


ALBUM_COVER = "resource/images/test-images/album-cover-test-2.jpg"


class CustomTitleBar(StandardTitleBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.closeBtn.setHoverBackgroundColor(QColor(216, 212, 213, 50))
        self.closeBtn.setHoverColor(Qt.black)
        self.minBtn.setHoverColor(Qt.black)
        self.minBtn.setHoverBackgroundColor(QColor(216, 212, 213, 50))
        self.maxBtn.hide()


class MainWindowUI(FramelessMainWindow):
    repaint_flag = False
    def __init__(self, parent=None):
        # Window configuration
        super().__init__(parent=parent)

        self.player = MediaPlayer()

        self.__last_volume = 100
        self.colors = None
        self.primary_color = (125, 125, 125)

        self.createWidgets()

        self.initWidgets()

    def createWidgets(self):
        """Create widgets"""

        # Player widget
        self.playerWidget = QWidget()

        # PlayerWidget
        self.playerLayout = QVBoxLayout()

        # Album cover widget
        self.album_cover = AlbumCoverInterface(self)

        # Song info widget
        self.song_info = SongInfoInterface(self)

        # Progress bar widget
        self.progress_bar = ProgressBarInterface(self)

        # Playback control
        self.playback_control = PlaybackControlInterface(self)

        # Volume control
        self.volume_control = VolumeControlInterface(self)

        # Menu control
        self.menu_control = MenuControlInterface(self)

        self.initWindow()

    def initWidgets(self):
        """Init widgets"""

        # Set slider colors
        color = QColor(*self.primary_color)
        self.progress_bar.setSliderColor(color)

        self.volume_control.setSliderColor(color)

        # The album cover layout is added to the main layout
        self.playerLayout.addWidget(self.album_cover)

        # The slider layout is added to the main layout
        self.playerLayout.addWidget(self.progress_bar)

        # The song info layout is added to the main
        self.playerLayout.addWidget(self.song_info)

        # We add the control layout to the main layout
        self.playerLayout.addWidget(self.playback_control)

        # We se the menu and volume control
        self.playerLayout.addWidget(self.volume_control)

        self.playerLayout.addWidget(self.menu_control)

        self.playerWidget.setLayout(self.playerLayout)

        self.adjustWidgetGeometry()

        self.setCentralWidget(self.playerWidget)

    def initWindow(self):
        """Initialize window"""
        self.setTitleBar(CustomTitleBar(self))
        self.titleBar.raise_()

        self.titleBar.layout().insertStretch(1, 1)
        self.setMenuWidget(self.titleBar)

        self.setFixedSize(QSize(530, 700))

        # set window stylesheet
        self.setObjectName("main_window")
        self.setQss()

        self.connectSignalsToSlots()

        self.show()

    def setQss(self):
        """ Generate qss and apply """
        #self.primary_color = [255, 255, 255]
        generate_css(self.primary_color)
        setStyleSheet(self, "main_window")

    def adjustWidgetGeometry(self):
        # Main layout configuration
        self.playerLayout.setContentsMargins(10, 20, 10, 20)

    def setCoverColors(self, cover: QImage):
        colors = ColorPalette(cover)
        self.colors = colors.get_min_contrast_palette()
        #self.colors = colors.get_primary_min_contrast_palette()
        self.primary_color = colors.get_dominant_color()

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
        signal_bus.open_file_signal.connect(self.fileOpened)
        signal_bus.open_file_signal.connect(self.updateWaveformEvent)
        signal_bus.metadata_song_signal.connect(self.trackMetadataChanged)
        signal_bus.mute_volume_signal.connect(self.muteVolumeEvent)
        signal_bus.increase_volume_signal.connect(self.increaseVolumeEvent)
        signal_bus.volume_scroll_changed_signal.connect(self.volumeScrollEvent)

        signal_bus.repaint_main_window_signal.connect(self.update)
        #self.player.positionChanged.connect(self.updateTimeStampEvent)

    def updateTimeStampEvent(self, value: int):
        c_time = value
        l_time = self.player.duration() - c_time

        self.progress_bar.updateTimeStamp(c_time=c_time, l_time=l_time)

    def volumeScrollEvent(self, value: int):
        """Volume scroll event"""
        volume_value = 5 * round(value / 5)
        self.player.setVolume(volume_value)

    def increaseVolumeEvent(self):
        """Increases the volume by 10%"""
        current_volume = self.player.volume()
        print(f"Volume: {current_volume}")
        if current_volume < 100:
            self.player.setVolume(current_volume + 5)

    def muteVolumeEvent(self):
        """Mute volume"""
        current_volume = self.player.volume()
        if current_volume == 0:
            self.player.setVolume(self.__last_volume)
        else:
            self.__last_volume = current_volume
            self.player.setVolume(0)

    def togglePlayState(self):
        """Toggle play state"""
        print("Toggle Play State")
        self.player.togglePlayState()

    def fileOpened(self, file_name: str):
        """File opened"""
        self.player.loadTrack(file_name)

    def updateWaveformEvent(self, file: str):
        """Update waveform values"""
        self.progress_bar.setWaveformValues(file)

    def trackMetadataChanged(self, values: dict):
        """Track Metadata Changed"""
        song_metadata = {}
        if 'AlbumArtist' in values:
            song_metadata['Artist'] = values['AlbumArtist']
        elif 'Artist' in values:
            song_metadata['Artist'] = values['Artist']
        elif 'ContributingArtist' in values:
            song_metadata['Artist'] = values['ContributingArtist']
        else:
            song_metadata['Artist'] = 'Unknown Artist'

        if 'Title' not in values:
            song_metadata['Title'] = 'Unknown Title'
        else:
            song_metadata['Title'] = values['Title']

        if 'AlbumTitle' not in values:
            song_metadata['AlbumTitle'] = 'Unknown Album'
        else:
            song_metadata['AlbumTitle'] = values['AlbumTitle']

        #song_metadata = {k: values[k] for k in ('AlbumArtist', 'Title', 'AlbumTitle')}
        self.song_info.update_song_info(song_metadata)

        if 'CoverArtImage' in values:
            cover = values['CoverArtImage']
            self.setCoverColors(cover)

            self.album_cover.updateCoverImage(cover)
            color = QColor(*self.primary_color)
            self.progress_bar.setSliderColor(color)

            self.volume_control.setSliderColor(color)
            self.repaintWidget(cover)

    def repaintWidget(self, cover: QImage):
        """A new track has been loaded, so the widget gradient should be repainted"""
        self.setQss()
        self.repaint_flag = True
        self.update()
