"""
Volume widget interface
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtGui import QColor

from .volume_control_widget import VolumeControlWidget


class VolumeControlInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.steps = 20
        self.orientation = Qt.Orientation.Horizontal

        self.volume_control = VolumeControlWidget(self.steps, self.orientation)

        self.main_layout = QVBoxLayout()

        self.setup_ui()

    def setup_ui(self):
        """Setup ui"""

        self.main_layout.addWidget(self.volume_control)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.main_layout)

    def setSliderColor(self, color: QColor):
        self.volume_control.setSliderColor(color)
