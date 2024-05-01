"""
Progress bar widget
"""

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QSizePolicy

from Components.segmented_slider.waveform_slider import WaveformSlider


class ProgressBarWidget(WaveformSlider):

    def __init__(self, steps: int, orientation: Qt.Orientation, parent=None):
        super().__init__(steps, orientation, parent)

        self.setup_ui()

    def setup_ui(self):
        """Setup ui"""
        self.setAddPagetyle(self.AddPageStyle.Outline)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.setFixedSize(QSize(200, 100))
        self.setWaveformStyle(self.WaveformStyle.FromLongitudinalAxis, v_offset=0.5)

    def update_waveform(self, values: list):
        self.setWaveformFunction(values)
