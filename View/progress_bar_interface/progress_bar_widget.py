"""
Progress bar widget
"""
import random

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QSizePolicy, QHBoxLayout, QWidget
from PyQt5.QtGui import QColor

from Components.segmented_slider.waveform_slider import WaveformSlider


class ProgressBarWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.steps = 60
        self.orientation = Qt.Orientation.Horizontal

        self.progress_bar = WaveformSlider(self.steps, self.orientation, self)

        self.main_layout = QHBoxLayout()

        self.setup_ui()

    def setup_ui(self):
        self.progress_bar.setAddPagetyle(WaveformSlider.AddPageStyle.Fill)
        self.progress_bar.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )
        self.progress_bar.setFixedSize(QSize(250, 50))
        self.progress_bar.setWaveformStyle(
            WaveformSlider.WaveformStyle.Symmetrical
        )
        self.progress_bar.setSolidPercent(0.5)

        values = [round(random.random(), 2) for _ in range(self.steps)]
        self.progress_bar.setWaveformFunction(values)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.progress_bar)

        self.setLayout(self.main_layout)

    def setSliderColor(self, color: QColor):
        self.progress_bar.setColor(color)

