
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMdiSubWindow, QSizePolicy, QStyleOption, QStyle
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import Qt, QEvent

from View.album_cover_interface import AlbumCoverInterface
from View.song_info_interface import SongInfoInterface
from View.progress_bar_interface import ProgressBarInterface
from View.playback_control_interface import PlaybackControlInterface
from View.volume_control_interface import VolumeControlInterface
from View.menu_control_interface import MenuControlInterface
from View.titlebar import TitleBar

from Common.signal_bus import signal_bus


class PlayerWidget(QWidget):
    def __init__(self, parent=None):
        super(PlayerWidget, self).__init__(parent)

        #self.setAttribute(Qt.WA_TranslucentBackground)

        self.createWidgets()

        self.initWidgets()

        self.installEventFilter(self)

    def createWidgets(self):
        """Create widgets"""

        # PlayerWidget
        self.playerLayout = QVBoxLayout()

        # Titlebar
        self.titlebar = TitleBar(self)

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

    def initWidgets(self):
        """Init widgets"""
        #self.setContentsMargins(0, 0, 0, 0)

        #self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Layout margins
        self.playerLayout.setContentsMargins(10, 5, 10, 20)
        #self.playerLayout.setSpacing(0)

        #self.playerLayout.setContentsMargins(0, 0, 0, 0)
        # Set slider colors
        color = QColor(125, 125, 125)
        self.progress_bar.setSliderColor(color)

        self.volume_control.updateWidgetColor(color)

        self.playerLayout.addWidget(self.titlebar, 0, Qt.AlignTop)

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

        self.setLayout(self.playerLayout)

        #self.adjustWidgetGeometry()


    def eventFilter(self, obj, event):
        return super(PlayerWidget, self).eventFilter(obj, event)


class MainPlayerView(QMdiSubWindow):

    def __init__(self, parent=None):
        super(MainPlayerView, self).__init__(parent)
        #self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Player window")
        self.widget = PlayerWidget()
        self.setContentsMargins(0, 0, 0, 0)
        self.setWidget(self.widget)

        self.showMaximized()
