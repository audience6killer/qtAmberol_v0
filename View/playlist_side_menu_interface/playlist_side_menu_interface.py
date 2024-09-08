from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QStyledItemDelegate, QStyle, QListView, \
    QPushButton, QStyleOption, QListWidget, QListWidgetItem, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter, QIcon, QColor, QLinearGradient
from PyQt5.QtCore import QSize, Qt, QRect, QAbstractListModel, QModelIndex

from .song_in_playlilst_widget import SongInPlaylistWidget
from .playlist_header import PlaylistHeader
from .tracklist_widget import TrackListWidget

from Common.signal_bus import signal_bus

from Common import resources, setStyleSheet


class PlaylistSideMenuInterface(QWidget):

    def __init__(self, parent=None):
        super(PlaylistSideMenuInterface, self).__init__(parent)
        # Layouts
        self._parent = parent

        self.setStyleSheet("background: transparent;")
        self.colors = None
        self.main_layout = QVBoxLayout()

        self.playlist_header = PlaylistHeader()
        #self.playlist_list_view = QListWidget(self)
        self.tracklist_widget = TrackListWidget()

        self.setupUI()

        self.__connectSignalsToSlots()

    def setupUI(self):
        """Setup UI"""
        self.setObjectName("playlist_widget")
        #self.playlist_list_view.setItemDelegate(NoSelectionDelegate())
        self.main_layout.setContentsMargins(5, 15, 12, 5)
        self.main_layout.addWidget(self.playlist_header)
        self.main_layout.addWidget(self.tracklist_widget)
        #self.playlist_list_view.setSpacing(10)
        #self.playlist_list_view.setContentsMargins(0, 20, 0, 0)

        ##### TESTING ONLY
        #for i in range(4):
        #    track = QListWidgetItem()
        #    track_widget = SongInPlaylistWidget()
        #    track.setSizeHint(track_widget.sizeHint())
        #    self.playlist_list_view.addItem(track)
        #    self.playlist_list_view.setItemWidget(track, track_widget)
        #####

        self.setLayout(self.main_layout)

    def __connectSignalsToSlots(self):
        signal_bus.state_colors_updated_signal.connect(self.setQss)

    def setQss(self, state_colors):
        setStyleSheet(self, state_colors)
