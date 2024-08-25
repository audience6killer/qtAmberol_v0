from PyQt5.QtWidgets import QListWidget, QStyledItemDelegate, QStyle, QListWidgetItem

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

        self.setupUI()

        self.__connectSignalsToSlots()

    def setupUI(self):
        self.setItemDelegate(NoSelectionDelegate())
        self.setContentsMargins(0, 20, 0, 0)

        #### TESTING ONLY
        for i in range(4):
            track = QListWidgetItem()
            track_widget = SongInPlaylistWidget()
            track.setSizeHint(track_widget.sizeHint())
            self.addItem(track)
            self.setItemWidget(track, track_widget)
        ####

    def __connectSignalsToSlots(self):
        self.itemClicked.connect(self.trackChanged)

    def trackChanged(self, item_clicked):
        """"Track changed"""
        # Remove the playing symbol from all the tracks
        for index in range(self.count()):
            item = self.item(index)
            self.itemWidget(item).isNotPlaying()

        widget = self.itemWidget(item_clicked)
        widget.isPlaying()




