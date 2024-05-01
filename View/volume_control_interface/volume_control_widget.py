"""
Volume control widget
"""

from PyQt5.QtWidgets import QHBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt

from Components.segmented_slider.segmented_slider import SegmentedSlider
from Common import resources


class VolumeControlWidget(QWidget):
    def __init__(self, steps: int, orientation: Qt.Orientation, parent=None):

        super().__init__(parent)

        self.volume_widget = SegmentedSlider(steps, orientation, self)

        self.volume_up_button = QPushButton()
        self.volume_mute_button = QPushButton()

        self.main_layout = QHBoxLayout()

        self.setup_ui()

    def setup_ui(self):
        """Setup ui"""

        self.main_layout.setContentsMargins(110, 0, 110, 0)

        self.volume_mute_button.setObjectName("mute-button")
        self.volume_up_button.setObjectName("volume-up")

        self.volume_up_button.setIcon(QIcon(":/images/volume_control/volume-up.svg"))
        self.volume_up_button.setFixedSize(QSize(30, 30))

        self.volume_mute_button.setIcon(
            QIcon(":/images/volume_control/volume-mute.svg")
        )
        self.volume_mute_button.setFixedSize(QSize(30, 30))

        self.volume_widget.setFixedSize(QSize(100, 300))

        self.main_layout.addWidget(self.volume_mute_button)
        self.main_layout.addWidget(self.volume_widget)
        self.main_layout.addWidget(self.volume_up_button)

        self.setLayout(self.main_layout)
