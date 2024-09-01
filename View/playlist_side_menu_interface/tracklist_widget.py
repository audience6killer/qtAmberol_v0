from PyQt5.QtCore import QAbstractListModel, Qt
from PyQt5.QtMultimedia import QMediaPlaylist
from PyQt5.QtWidgets import QListWidget, QStyledItemDelegate, QStyle, QListWidgetItem, QAbstractItemView, QWidget

from Common import signal_bus
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

        self.v_scrollbar = PlaylistScrollBar(Qt.Vertical)
        self.setupUI()

        self.__connectSignalsToSlots()

    def setupUI(self):
        self.setItemDelegate(NoSelectionDelegate())
        self.setContentsMargins(0, 20, 0, 0)

        self.setVerticalScrollBar(self.v_scrollbar)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setStyleSheet("""
        QScrollBar:vertical {
            background: #F0F0F0;
            width: 12px;
            margin: 0px 0px 0px 0px;
            border: none;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical {
            background: #C0C0C0;
            min-height: 20px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical:hover {
            background: #A0A0A0;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        """)

    def __connectSignalsToSlots(self):
        self.itemClicked.connect(self.trackClicked)
        signal_bus.track_added_to_playlist_signal.connect(self.addTrack)
        signal_bus.playlist_current_track_index_signal.connect(self.trackChanged)

    def trackClicked(self, track: QListWidgetItem):
        track_index = self.row(track)
        signal_bus.playlist_track_clicked_index_signal.emit(track_index)

    def trackChanged(self, new_track: int):
        """"Track changed"""
        # Remove the playing symbol from all the tracks
        for index in range(self.count()):
            item = self.item(index)
            self.itemWidget(item).isNotPlaying()

        item = self.item(new_track)
        self.itemWidget(item).isPlaying()

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
        self.v_scrollbar.hide_timer.start(200)  # Hide scrollbar after delay when leaving the widget
        super().leaveEvent(event)



