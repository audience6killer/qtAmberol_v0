"""
Main window layout
"""

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication
from PyQt5.QtGui import QPainter, QLinearGradient, QColor
from PyQt5.QtCore import Qt, QSize, QPointF

from qframelesswindow import FramelessMainWindow, StandardTitleBar

from View.album_cover_interface import AlbumCoverInterface
from View.song_info_interface import SongInfoInterface
from View.progress_bar_interface import ProgressBarInterface
from View.playback_control_interface import PlaybackControlInterface
from View.volume_control_interface import VolumeControlInterface
from View.menu_control_interface import MenuControlInterface

from Common.image_utils import get_image_color_palette
from Common.image_utils import get_image_primary_color

from Common.style_sheet import setStyleSheet
from Common.parse_stylesheet import generate_css
from Common import resources


ALBUM_COVER = "resource/images/test-images/album-cover-test-4.jpg"


class CustomTitleBar(StandardTitleBar):
    def __init__(self, parent):
        super().__init__(parent)

        self.closeBtn.setHoverBackgroundColor(QColor(216, 212, 213, 50))
        self.closeBtn.setHoverColor(Qt.black)
        self.minBtn.setHoverColor(Qt.black)
        self.minBtn.setHoverBackgroundColor(QColor(216, 212, 213, 50))
        self.maxBtn.hide()


class MainWindowUI(FramelessMainWindow):
    repaint_flag = True

    def __init__(self, parent=None):
        # Window configuration
        super().__init__(parent=parent)

        ### Provisionalmente
        self.colors = get_image_color_palette(ALBUM_COVER)

        self.primary_color = self.colors[0]
        ## Provisionalmente

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
        color = QColor(self.primary_color[0], self.primary_color[1], self.primary_color[2])
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

        self.show()

    def setQss(self):
        """ Generate qss and apply """
        generate_css(self.primary_color)
        setStyleSheet(self, "main_window")

    def adjustWidgetGeometry(self):
        # Main layout configuration
        self.playerLayout.setContentsMargins(10, 20, 10, 20)

    def paintEvent(self, event):
        """ Paint widget event """
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

