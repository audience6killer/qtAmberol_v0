"""
Playback control interface
"""

from PyQt5.QtWidgets import QVBoxLayout, QWidget

from .playback_control_widget import PlaybackControlWidget


class PlaybackControlInterface(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.control_widget = PlaybackControlWidget()

        self.main_layout = QVBoxLayout()

        self.setup_ui()

    def setup_ui(self):
        """Setup ui"""

        self.main_layout.addWidget(self.control_widget)

        self.setLayout(self.main_layout)
