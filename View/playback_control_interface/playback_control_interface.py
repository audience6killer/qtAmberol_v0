"""
Playback control interface
"""
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from .playback_control_widget import PlaybackControlWidget

from Common.signal_bus import signal_bus
from Common.style_sheet import setStyleSheet


class PlaybackControlInterface(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.control_widget = PlaybackControlWidget()

        self.main_layout = QVBoxLayout()

        self.setup_ui()

        self.__connectSignalsToSlots()

    def setup_ui(self):
        """Setup ui"""

        self.setObjectName("playback_control_interface")

        self.main_layout.addWidget(self.control_widget)

        self.setLayout(self.main_layout)

    def __connectSignalsToSlots(self):
        """Connect signals to slots"""
        signal_bus.state_colors_updated_signal.connect(self.setQss)

    def setQss(self, state_colors):
        """Update QSS values"""
        setStyleSheet(self, state_colors)


