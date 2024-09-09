"""
Volume widget interface
"""
from signal import signal
from typing import Union

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtGui import QColor

from .volume_control_widget import VolumeControlWidget

from Common.signal_bus import signal_bus
from Common.style_sheet import setStyleSheet


class VolumeControlInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.steps = 20
        self.orientation = Qt.Orientation.Horizontal

        self.volume_control = VolumeControlWidget(self.steps, self.orientation)

        self.main_layout = QVBoxLayout()

        self.setup_ui()

        self.__connectSignalsToSlots()

    def setup_ui(self):
        """Setup ui"""

        self.setObjectName("volume_control_interface")

        self.main_layout.addWidget(self.volume_control)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.main_layout)

    def updateWidgetColor(self, state_colors):
        setStyleSheet(self, state_colors)
        self.volume_control.setSliderColor(state_colors)

    def playerVolumeChanged(self, volume: int):
        if volume:
            self.volume_control.volume_mute_button.setChecked(False)

        self.volume_control.volume_widget.setValue(volume)

    def __connectSignalsToSlots(self):
        """Connect signals to slots"""
        signal_bus.state_colors_updated_signal.connect(self.updateWidgetColor)
        signal_bus.volume_changed_event.connect(self.playerVolumeChanged)


