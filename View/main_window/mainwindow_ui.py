"""
Main window layout
"""

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication
from PyQt5.QtGui import QPainter, QLinearGradient, QColor
from PyQt5.QtCore import Qt, QSize, QPointF

from qframelesswindow import FramelessMainWindow, StandardTitleBar

# from album_cover_interface.album_cover_interface import AlbumCoverInterface
# from song_info_interface.song_info_interface import SongInfoInterface
# from progress_bar_interface.progress_bar_interface import ProgressBarInterface
# from playback_control_interface.playback_control_interface import (
#    PlaybackControlInterface,
# )
# from volume_control_interface.volume_control_interface import VolumeControlInterface
# from menu_control_interface.menu_control_interface import MenuControlInterface

from View.album_cover_interface import AlbumCoverInterface
from View.song_info_interface import SongInfoInterface
from View.progress_bar_interface import ProgressBarInterface
from View.playback_control_interface import PlaybackControlInterface
from View.volume_control_interface import VolumeControlInterface
from View.menu_control_interface import MenuControlInterface

from Common.image_utils import (
    get_rounded_pixmap,
    get_image_primary_color,
    get_image_color_palette,
)
from Common.style_sheet import setStyleSheet
from Common import resources


ALBUM_COVER = "resource/images/test-images/album-cover-test.jpg"


class CustomTitleBar(StandardTitleBar):
    def __init__(self, parent):
        super().__init__(parent)

        self.minBtn.setHoverColor(Qt.white)
        self.minBtn.setHoverBackgroundColor(QColor(0, 100, 182))
        self.minBtn.setPressedColor(Qt.white)
        self.maxBtn.hide()


class MainWindowUI(FramelessMainWindow):
    def __init__(self, parent=None):
        # Window configuration
        super().__init__(parent=parent)

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
        # The album cover layout is added to the main layout
        self.playerLayout.addWidget(self.album_cover)

        # The song info layout is added to the main
        self.playerLayout.addWidget(self.song_info)

        # The slider layout is added to the main layout
        self.playerLayout.addWidget(self.progress_bar)

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
        self.setObjectName("mainWindow")
        self.setQss()

    def setQss(self):
        setStyleSheet(self, "main_window")

    def adjustWidgetGeometry(self):
        # Main layout configuration
        self.playerLayout.setContentsMargins(10, 20, 10, 20)

    def paintEvent(self, event):

        ### Provisionalmente
        self.colors = get_image_color_palette(ALBUM_COVER)
        ###

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


if __name__ == "__main__":
    import sys

    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    # sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    colors = get_image_color_palette(ALBUM_COVER)
    main_window = Window(colors)
    ui = MainWindowUI(main_window, app)
    # ui.initWidget(main_window)

    main_window.show()

    app.exec()
