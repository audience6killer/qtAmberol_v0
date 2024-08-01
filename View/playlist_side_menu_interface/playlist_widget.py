
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QStyledItemDelegate, QStyle, QListView, \
    QPushButton
from PyQt5.QtGui import QPixmap, QPainter, QIcon
from PyQt5.QtCore import QSize, Qt, QRect, QAbstractListModel, QModelIndex

from Common import resources


class TrackInPlaylistDelegate(QStyledItemDelegate):

    def __init__(self, height=50, parent=None):
        super().__init__(parent)
        self._height = height

    def paint(self, painter, option, index):
        """Paint event"""
        super(TrackInPlaylistDelegate, self).paint(painter, option, index)

        # Mouse options
        # Hover
        if option.state & QStyle.State_MouseOver:
            painter.fillRect(option.rect, Qt.lightGray)
        else:
            painter.fillRect(option.rect, Qt.transparent)

        # Selected
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, Qt.lightGray)

        # Draw icon
        icon = QPixmap()
        icon.load(index.data()[1])
        left = 24
        icon_pos = QRect(left, ((self._height - icon.height()) / option.rect.y(), icon.width(), icon.height()))
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.drawPixmap(icon_pos, icon)

        # Draw text
        text_pos = QRect((left + 2) + icon.width(), option.rect.y(), option.rect.width(), option.rect.height())
        painter.setPen(Qt.black)
        painter.drawText(text_pos, Qt.AlignVCenter, index.data()[0])

    def sizeHint(self, option, index):
        return QSize(0, self._height)


class PlaylistModel(QAbstractListModel):

    def __init__(self, data=None):
        super(PlaylistModel, self).__init__()

        if data is None:
            data = [("Title", ":/images/cover_art/album-cover-small.png")]

        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            return self._data[index.row()]


class PlaylistView(QListView):

    def __init__(self):
        super(PlaylistView, self).__init__()
        self.setMouseTracking(True)

    def mouseMoveEvent(self, e):
        if self.indexAt(e.pos()).row() >= 0:
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)


class PlaylistWidgetHeader(QWidget):

    def __init__(self, height=None):
        super(PlaylistWidgetHeader, self).__init__()

        if height is None:
            self.setFixedHeight(100)
        else:
            self.setFixedHeight(height)

        # Layouts
        self.info_layout = QVBoxLayout()
        self.main_layout = QHBoxLayout()

        # UI elements
        self.time_remaining_label = QLabel()

        self.search_button = QPushButton()
        self.select_items = QPushButton()
        self.hide_sidebar = QPushButton()

        self.setupUI()

    def setupUI(self):
        """ Setup UI"""
        self.main_layout.setContentsMargins(30, 20, 30, 20)

        title = QLabel()
        title.setObjectName('sidebar-title')
        self.time_remaining_label.setObjectName('time-remaining-label')
        self.hide_sidebar.setObjectName('hide-sidebar-button')
        self.select_items.setObjectName('select-items-button')
        self.search_button.setObjectName('search-track-button')

        self.select_items.setIcon(QIcon(QPixmap(":/images/sidebar/select.svg")))
        self.search_button.setIcon(QIcon(QPixmap(":/images/sidebar/search.svg")))
        self.hide_sidebar.setIcon(QIcon(QPixmap(":/images/sidebar/chevron-left.svg")))

        self.select_items.setFixedSize(QSize(30, 30))
        self.search_button.setFixedSize(QSize(30, 30))
        self.hide_sidebar.setFixedSize(QSize(30, 30))

        title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.time_remaining_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.info_layout.addWidget(title)
        self.info_layout.addWidget(self.time_remaining_label)

        self.main_layout.addWidget(self.info_layout)
        self.main_layout.addWidget(self.search_button)
        self.main_layout.addWidget(self.select_items)
        self.main_layout.addWidget(self.hide_sidebar)


class PlaylistWidget(QWidget):

    def __init__(self):
        super(PlaylistWidget, self).__init__()
        # Layouts
        self.main_layout = QVBoxLayout()

        self.playlist_header = PlaylistWidgetHeader()

        self.playlist_view = PlaylistView()
        self.playlist_view.setModel(PlaylistModel())
        self.playlist_view.setItemDelegate(TrackInPlaylistDelegate())

        self.setupUi()

    def setupUI(self):
        """Setup UI"""

        self.main_layout.addWidget(self.playlist_header)
        self.main_layout.addWidget(self.playlist_view)

        self.setLayout(self.main_layout)


