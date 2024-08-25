from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize, Qt

from Common import resources


class PlaylistHeader(QWidget):

    def __init__(self, parent=None):
        super(PlaylistHeader, self).__init__(parent)

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
