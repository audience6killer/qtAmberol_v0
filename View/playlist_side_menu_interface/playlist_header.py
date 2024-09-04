from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize, Qt

from Common import resources, signal_bus


class PlaylistHeader(QWidget):

    def __init__(self, parent=None):
        super(PlaylistHeader, self).__init__(parent)

        self._time_remaining = 0.0

        self.info_layout = QVBoxLayout()
        self.main_layout = QHBoxLayout()

        # UI elements
        self.title = QLabel()
        self.time_remaining_label = QLabel()

        self.search_button = QPushButton()
        self.select_items = QPushButton()
        self.hide_sidebar = QPushButton()

        self.setupUI()

        self.setQss()

        self.__connectSignalsToSlots()

    def setupUI(self):
        """ Setup UI"""
        self.main_layout.setContentsMargins(8, 0, 0, 5)

        self.title.setObjectName('sidebar-title')
        self.time_remaining_label.setObjectName('time-remaining-label')
        self.hide_sidebar.setObjectName('hide-sidebar-button')
        self.select_items.setObjectName('select-items-button')
        self.search_button.setObjectName('search-track-button')

        icon_side = 20
        self.select_items.setIcon(QIcon(":/images/sidebar/select.svg"))
        self.search_button.setIcon(QIcon(":/images/sidebar/search.svg"))
        self.hide_sidebar.setIcon(QIcon(":/images/sidebar/chevron-left.svg"))
        self.select_items.setIconSize(QSize(icon_side, icon_side))
        self.search_button.setIconSize(QSize(icon_side, icon_side))
        self.hide_sidebar.setIconSize(QSize(icon_side, icon_side))

        icon_side = 30
        self.select_items.setFixedSize(QSize(icon_side, icon_side))
        self.search_button.setFixedSize(QSize(icon_side, icon_side))
        self.hide_sidebar.setFixedSize(QSize(icon_side, icon_side))

        self.title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.time_remaining_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.info_layout.addWidget(self.title)
        self.info_layout.addWidget(self.time_remaining_label)

        self.title.setText("Playlist")
        self.time_remaining_label.setText("10 minutes remaining")

        self.main_layout.addLayout(self.info_layout)
        # self.main_layout.addWidget(self.info_layout)
        self.main_layout.addWidget(self.search_button)
        self.main_layout.addWidget(self.select_items)
        self.main_layout.addWidget(self.hide_sidebar)

        self.setLayout(self.main_layout)

    def setQss(self):
        self.setStyleSheet("""
            QLabel#sidebar-title {
                font-weight: bold;
            }
            QLabel#time-remaining-label {
                font-size: 12px;
            }
        """)

    def __connectSignalsToSlots(self):
        self.hide_sidebar.clicked.connect(signal_bus.hide_playlist_view)
        signal_bus.playlist_remaining_time.connect(self.setPlaylistRemainingTime)
        signal_bus.track_position_changed_signal.connect(self.updatePlaylistRemainingTime)

    def updatePlaylistRemainingTime(self, pos):
        if pos:
            current_time = pos // 1000
            t_left = self._time_remaining - current_time
            self.time_remaining_label.setText(self.getTrackPositionToMinSec(t_left))


    def setPlaylistRemainingTime(self, time_rem: float):
        self._time_remaining = time_rem
        time = self.getTrackPositionToMinSec(self._time_remaining)
        self.time_remaining_label.setText(time)

    # TODO: Create a module for this
    @staticmethod
    def getTrackPositionToMinSec(pos) -> str:
        """ Convert from track position in seconds to min:sec"""
        t_seconds = pos
        t_minutes = 0
        t_hours = 0
        seconds = 0
        time_str = ""
        if t_seconds:
            t_minutes = int(t_seconds // 60)
            # seconds = int(t_seconds % 60)

        if t_minutes >= 60:
            t_hours = int(t_minutes // 60)
            t_minutes = int(t_minutes % 60)

        if t_hours:
            time_str = f"{t_hours} hours {t_minutes} minutes remaining"
        else:
            time_str = f"{t_minutes} minutes remaining"

        if not t_hours and not t_minutes:
            time_str = "< 1 minute remaining"

        return time_str
