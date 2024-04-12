"""
Main window layout
"""

import os

from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QSlider,
    QPushButton,
    QSizePolicy,
    QApplication,
    QGraphicsBlurEffect,
    QProgressBar,
)
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QLinearGradient, QColor
from PyQt5.QtCore import Qt, QSize, QPointF
from qframelesswindow import FramelessMainWindow, StandardTitleBar

# from ..utils.utils import (
#    get_rounded_pixmap,
#    get_image_color_palette,
#    get_image_primary_color,
# )

from Common.image_utils import *

RES_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "res")
THEME_PATH = os.path.join(os.path.dirname(__file__), "..", "theme")
ALBUM_COVER = "img/album-cover-test.jpg"


class CustomTitleBar(StandardTitleBar):
    def __init__(self, parent):
        super().__init__(parent)

        self.minBtn.setHoverColor(Qt.white)
        self.minBtn.setHoverBackgroundColor(QColor(0, 100, 182))
        self.minBtn.setPressedColor(Qt.white)
        self.maxBtn.hide()


class CustomProgressSlider(QWidget):
    def __init__(self):
        super().__init__()

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(50)  # Set initial value
        self.progress_bar.setOrientation(
            Qt.Orientation.Horizontal
        )  # Horizontal orientation
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(
            """QProgressBar:horizontal {
                                              border: 2px solid #2196F3;
                                              border-radius: 5px;
                                              background-color: #E0E0E0;
                                              color: black;
                                          }
                                          QProgressBar::chunk:horizontal {
                                              background-color: #2196F3;
                                              width: 5px; 
                                              margin: 1px;
                                          }"""
        )
        self.progress_bar.setFixedSize(QSize(200, 30))

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)  # Set initial value
        self.slider.setHidden(True)
        self.slider.setFixedSize(QSize(200, 30))  # Make it same size as progress bar

        layout = QVBoxLayout()

        layout.addWidget(self.progress_bar)
        layout.addWidget(self.slider)
        self.setLayout(layout)

        self.progress_bar.valueChanged.connect(self.move_slider)
        self.slider.valueChanged.connect(self.progress_bar_moved)

    def progress_bar_moved(self, value):
        print("Progress bar moved to:", value)
        self.progress_bar.setValue(value)

    def move_slider(self, value):
        self.slider.setValue(value)


class Window(FramelessMainWindow):
    def __init__(self, colors: list, parent=None):
        super().__init__(parent=parent)
        self.colors = colors
        self.setTitleBar(CustomTitleBar(self))
        # self.setWindowTitle("PyQt-Frameless-Window")
        self.titleBar.raise_()
        # self.titleBar.layout().insertWidget(0, menuBar, 0, Qt.AlignLeft)
        self.titleBar.layout().insertStretch(1, 1)
        self.setMenuWidget(self.titleBar)

    def paintEvent(self, event):
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


class MainWindowUI(object):
    def __init__(self, main_window, app: QApplication):
        # Window configuration
        self.main_window = main_window
        # self.main_window.setWindowTitle("qtMusicPlayer")
        self.main_window.setFixedSize(QSize(530, 700))
        self.setup_ui()
        # self.set_style_sheet(app)
        with open(os.path.join(THEME_PATH, "styles.css"), "r") as theme:
            app.setStyleSheet(theme.read())

    def set_style_sheet(self, main_window):
        with open(os.path.join(THEME_PATH, "styles.css"), "r") as theme:
            main_window.setStyleSheet(theme.read())

    def setup_ui(self):
        # Main layout configuration
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 20, 10, 20)

        # Song cover and top layout
        self.cover_layout = QHBoxLayout()
        self.cover_layout.setContentsMargins(0, 0, 0, 0)
        self.album_cover_label = QLabel()
        self.album_cover_label.setFixedSize(QSize(300, 300))

        pixmap = QPixmap()
        pixmap.load(os.path.join(RES_PATH, ALBUM_COVER))
        modified_pixmap = get_rounded_pixmap(
            pixmap.scaled(
                300,
                300,
                aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                transformMode=Qt.TransformationMode.SmoothTransformation,
            )
        )
        self.album_cover_label.setPixmap(modified_pixmap)
        self.album_cover_label.setObjectName("albumCover")
        self.cover_layout.addWidget(self.album_cover_label)

        # The album cover layout is added to the main layout
        self.main_layout.addLayout(self.cover_layout)

        # Song information layoout
        self.info_layout = QHBoxLayout()
        self.info_vertical_leyout = QVBoxLayout()

        self.track_title = QLabel()
        self.track_artist = QLabel()
        self.track_album = QLabel()

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

        self.track_title.setText("Song Name")
        self.track_album.setText("Album Name")
        self.track_artist.setText("Artist Name")

        self.info_vertical_leyout.addWidget(self.track_title)
        self.info_vertical_leyout.addWidget(self.track_artist)
        self.info_vertical_leyout.addWidget(self.track_album)

        self.info_layout.addLayout(self.info_vertical_leyout)

        # The song info layout is added to the main
        self.main_layout.addLayout(self.info_layout)

        # Progress slider layout
        self.slider_layout = QVBoxLayout()
        self.timestamp_layout = QHBoxLayout()
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.time_left_label = QLabel()
        self.time_current_label = QLabel()

        self.slider_layout.setContentsMargins(90, 20, 90, 0)

        # self.progress_slider.setContentsMargins(90, 20, 90, 0)
        self.progress_slider.setMaximum(100)
        self.progress_slider.setMinimum(0)

        primary_color = get_image_primary_color(os.path.join(RES_PATH, ALBUM_COVER))
        rgb_primary = (
            f"rgba({primary_color[0]},{primary_color[1]},{primary_color[2]}, {0.5})"
        )
        self.progress_slider.setStyleSheet(
            "QSlider::sub-page:horizontal {background:" + rgb_primary + ";}"
        )

        self.time_left_label.setProperty("class", "timestamp")
        self.time_current_label.setProperty("class", "timestamp")
        self.time_left_label.setText("-00:00")
        self.time_current_label.setText("00:00")
        self.time_left_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.time_current_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.time_left_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.time_current_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )

        self.timestamp_layout.addWidget(self.time_current_label)
        self.timestamp_layout.addWidget(self.time_left_label)

        self.slider_layout.addWidget(self.progress_slider)
        self.slider_layout.addLayout(self.timestamp_layout)

        # The slider layout is added to the main layout
        self.main_layout.addLayout(self.slider_layout)

        # Control layout
        self.control_layout = QHBoxLayout()
        self.play_button = QPushButton()
        self.next_button = QPushButton()
        self.previous_button = QPushButton()

        self.play_button.setIcon(
            QIcon(QPixmap(os.path.join(RES_PATH, "icons/play.svg")))
        )
        self.next_button.setIcon(
            QIcon(QPixmap(os.path.join(RES_PATH, "icons/next.svg")))
        )
        self.previous_button.setIcon(
            QIcon(QPixmap(os.path.join(RES_PATH, "icons/previous.svg")))
        )

        self.play_button.setProperty("class", "player-button")
        self.next_button.setProperty("class", "player-button")
        self.previous_button.setProperty("class", "player-button")

        self.play_button.setFixedSize(QSize(50, 50))
        self.next_button.setFixedSize(QSize(50, 50))
        self.previous_button.setFixedSize(QSize(50, 50))

        self.control_layout.addWidget(self.previous_button)
        self.control_layout.addWidget(self.play_button)
        self.control_layout.addWidget(self.next_button)

        # We add the control layout to the main layout
        self.main_layout.addLayout(self.control_layout)

        # We se the menu and volume control
        self.volume_layout = QHBoxLayout()
        # self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider = CustomProgressSlider()
        self.volume_up_button = QPushButton()
        self.volume_mute_button = QPushButton()

        self.volume_layout.setContentsMargins(110, 0, 110, 0)

        self.volume_mute_button.setObjectName("mute-button")
        self.volume_up_button.setObjectName("volume-up")
        self.volume_slider.setObjectName("volume-slider")

        self.volume_up_button.setProperty("class", "volume-controls")
        self.volume_mute_button.setProperty("class", "volume-controls")

        self.volume_up_button.setIcon(
            QIcon(os.path.join(RES_PATH, "icons/volume-up.svg"))
        )
        self.volume_up_button.setFixedSize(QSize(30, 30))
        self.volume_mute_button.setIcon(
            QIcon(os.path.join(RES_PATH, "icons/volume-mute.svg"))
        )
        self.volume_mute_button.setFixedSize(QSize(30, 30))

        # self.volume_slider.setMaximum(100)
        # self.volume_slider.setMinimum(0)

        # Initial value
        self.progress_slider.setValue(50)

        self.volume_layout.addWidget(self.volume_mute_button)
        self.volume_layout.addWidget(self.volume_slider)
        self.volume_layout.addWidget(self.volume_up_button)
        # self.menu_layout.addLayout(self.volume_layout)

        self.main_layout.addLayout(self.volume_layout)

        ################################
        self.menu_layout = QHBoxLayout()
        self.menu_button = QPushButton()
        self.shuffle_playlist = QPushButton()
        self.enable_repeat = QPushButton()

        self.menu_layout.setContentsMargins(110, 0, 110, 0)

        self.menu_button.setProperty("class", "menu-button")
        self.shuffle_playlist.setProperty("class", "menu-button")
        self.enable_repeat.setProperty("class", "menu-button")

        self.shuffle_playlist.setIcon(
            QIcon(os.path.join(RES_PATH, "icons/shuffle.svg"))
        )
        self.shuffle_playlist.setFixedSize(QSize(30, 30))
        self.enable_repeat.setIcon(QIcon(os.path.join(RES_PATH, "icons/repeat.svg")))
        self.enable_repeat.setFixedSize(QSize(30, 30))
        self.menu_button.setIcon(QIcon(os.path.join(RES_PATH, "icons/menu.svg")))
        self.menu_button.setFixedSize(QSize(30, 30))

        self.menu_layout.addWidget(self.menu_button)
        self.menu_layout.addWidget(self.shuffle_playlist)
        self.menu_layout.addWidget(self.enable_repeat)

        self.main_layout.addLayout(self.menu_layout)
        self.main_widget.setLayout(self.main_layout)

        self.main_window.setCentralWidget(self.main_widget)


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

    colors = get_image_color_palette(os.path.join(RES_PATH, ALBUM_COVER))
    main_window = Window(colors)
    ui = MainWindowUI(main_window, app)
    # ui.setup_ui(main_window)

    main_window.show()

    app.exec()
