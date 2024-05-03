"""
Playback control widget
"""

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon

from Common import resources


class PlaybackControlWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout
        self.main_layout = QHBoxLayout()

        # Control buttons
        self.play_button = QPushButton()
        self.next_button = QPushButton()
        self.previous_button = QPushButton()

        self.setup_ui()

    def setup_ui(self):
        """Setup ui"""
        self.play_button.setIcon(QIcon(QPixmap(":/images/playback_control/play.svg")))
        self.next_button.setIcon(QIcon(QPixmap(":/images/playback_control/next.svg")))
        self.previous_button.setIcon(
            QIcon(QPixmap(":/images/playback_control/previous.svg"))
        )

        self.play_button.setObjectName("play-button")
        self.next_button.setObjectName("next-button")
        self.previous_button.setObjectName("previous_button")

        self.play_button.setFixedSize(QSize(50, 50))
        self.next_button.setFixedSize(QSize(50, 50))
        self.previous_button.setFixedSize(QSize(50, 50))

        self.main_layout.addWidget(self.previous_button)
        self.main_layout.addWidget(self.play_button)
        self.main_layout.addWidget(self.next_button)

        self.setWidgetsTooltip()

        # We add the control layout to the main layout
        self.setLayout(self.main_layout)

    def setWidgetsTooltip(self):
        """ Sets tooltip for all buttons"""
        self.play_button.setToolTip("Play")
        self.next_button.setToolTip("Next")
        self.previous_button.setToolTip("Previous")
