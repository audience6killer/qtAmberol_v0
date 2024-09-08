from PyQt5.QtCore import QAbstractListModel, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtMultimedia import QMediaPlaylist
from PyQt5.QtWidgets import QListWidget, QStyledItemDelegate, QStyle, QListWidgetItem, QAbstractItemView, QWidget

from Common import signal_bus, setStyleSheet
from Components.media_player.song_info import SongInfo
from Components.playlist_scrollbar import PlaylistScrollBar
from .song_in_playlilst_widget import SongInPlaylistWidget


class NoSelectionDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Remove all selection-related states
        option.state &= ~QStyle.State_Selected
        option.state &= ~QStyle.State_HasFocus
        super().paint(painter, option, index)


class TrackListWidget(QListWidget):

    def __init__(self, parent=None):
        super(TrackListWidget, self).__init__(parent)

        self._is_window_visible = False
        self._current_index = 0

        self.v_scrollbar = PlaylistScrollBar(Qt.Vertical)
        self.setupUI()

        self.__connectSignalsToSlots()

    def setupUI(self):
        self.setObjectName("tracklist_widget")
        self.setItemDelegate(NoSelectionDelegate())
        self.setContentsMargins(0, 20, 0, 0)

        self.setVerticalScrollBar(self.v_scrollbar)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def __connectSignalsToSlots(self):
        self.itemClicked.connect(self.trackClicked)
        signal_bus.track_added_to_playlist_signal.connect(self.addTrack)
        signal_bus.playlist_current_track_index_signal.connect(self.trackChanged)
        signal_bus.state_colors_updated_signal.connect(self.setQss)
        signal_bus.playlist_view_is_visible.connect(self.isWindowVisible)

    def isWindowVisible(self, value):
        self._is_window_visible = value
        if self._is_window_visible:
            self.startTrackScroll()
        else:
            self.stopTrackScroll()

    def startTrackScroll(self):
        item = self.item(self._current_index)
        self.itemWidget(item).isScrolling = True

    def stopTrackScroll(self):
        if self.count():
            item = self.item(self._current_index)
            self.itemWidget(item).isScrolling = False

    def trackClicked(self, track: QListWidgetItem):
        track_index = self.row(track)
        signal_bus.playlist_track_clicked_index_signal.emit(track_index)

    def trackChanged(self, new_track: int):
        """"Track changed"""
        # Remove the playing symbol from all the tracks
        for index in range(self.count()):
            item = self.item(index)
            self.itemWidget(item).isPlaying = False

        item = self.item(new_track)
        self.itemWidget(item).isPlaying = True
        self._current_index = new_track

    def addTracks(self, playlist: list[SongInfo]):
        """Add entire playlist"""
        self.clear()
        for track_info in playlist:
            track = QListWidgetItem()
            track_widget = SongInPlaylistWidget(metadata=track_info)
            track.setSizeHint(track_widget.sizeHint())
            self.addItem(track)
            self.setItemWidget(track, track_widget)

    def addTrack(self, track_info: SongInfo):
        """Add a track"""
        track = QListWidgetItem()
        track_widget = SongInPlaylistWidget(metadata=track_info)
        track.setSizeHint(track_widget.sizeHint())
        self.addItem(track)
        self.setItemWidget(track, track_widget)

    def enterEvent(self, event):
        self.v_scrollbar.show_scrollbar()  # Show scrollbar when entering the widget
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.v_scrollbar.hide_timer.start(1000)  # Hide scrollbar after delay when leaving the widget
        super().leaveEvent(event)

    def setQss(self, state_colors):
        setStyleSheet(self, state_colors)
