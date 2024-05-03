import random
import sys
import math

from enum import Enum

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import QSize, Qt, QPointF, QSizeF
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy

from .segmented_slider import SegmentedSlider


class WaveformSlider(SegmentedSlider):
    class WaveformStyle(Enum):
        FromLongitudinalAxis = 0
        Symmetrical = 1
        Normal = 2

    def __init__(self, steps: int, orientation: Qt.Orientation, parent=None):

        super().__init__(steps, orientation, parent)

        # True: this class updates the params; False: super() does it
        self._params_update = False

        self.parent = parent
        self.v_offset = 0  # Vertical center, from which it will draw the steps
        self.waveform_style = self.WaveformStyle.Normal
        self.amplitude = self.n_steps * [1]

        self.__triggerRefresh()

        # self.__updateStepsAttributes()

    def sizeHint(self):
        return super().sizeHint()

    def setWaveformFunction(self, amplitude: list):
        self.amplitude = amplitude[: self.n_steps]
        self.__triggerRefresh()

    def __updateStepsAttributes(self) -> None:

        self.amplitude = [x * (self.canvas_height if self._orientation == Qt.Orientation.Horizontal
                               else self.canvas_width) for x in self.amplitude]
        self._step_size = (
            self.canvas_height / self.n_steps
            if self._orientation == Qt.Orientation.Vertical
            else self.canvas_width / self.n_steps
        )

        self.bar_thickness = self._step_size * self._bar_solid_percent

        if self._orientation == Qt.Orientation.Vertical:
            offset = self.v_offset * self.canvas_width
            self._steps_data = [
                {
                    "pos": QPointF(
                        (
                            (offset + self.amplitude[n])
                            if self.waveform_style == self.WaveformStyle.Symmetrical
                            else offset
                        ),
                        self._padding + self.canvas_height - (1 + n) * self._step_size,
                    ),
                    "size": QSizeF(
                        (
                            self.amplitude[n]
                            if self.waveform_style
                            == self.WaveformStyle.FromLongitudinalAxis
                            else -self.amplitude[n] * 2
                        ),
                        self.bar_thickness,
                    ),
                    # "pos": QPointF(
                    #    self._padding + offset,
                    #    self._padding + self.canvas_height - (1 + n) * self._step_size,
                    # ),
                    # "size": QSizeF(self.canvas_width - offset, self.bar_thickness),
                }
                for n in range(self.n_steps)
            ]

        elif self._orientation == Qt.Orientation.Horizontal:
            offset = self.v_offset * self.canvas_height
            self._steps_data = [
                {
                    "pos": QPointF(
                        self._padding + n * self._step_size,
                        (
                            (self.canvas_height + self.amplitude[n]) / 2
                            if self.waveform_style == self.WaveformStyle.Symmetrical
                            else offset
                        ),
                    ),
                    "size": QSizeF(
                        self.bar_thickness,
                        (
                            self.amplitude[n]
                            if self.waveform_style
                            == self.WaveformStyle.FromLongitudinalAxis
                            else -self.amplitude[n]
                        ),
                    ),
                }
                for n in range(self.n_steps)
            ]

    def __triggerRefresh(self):
        # Who updates the steps params
        if self._params_update:
            self.__updateStepsAttributes()
            super().triggerRefresh(update_steps=False)
        else:
            super().triggerRefresh(update_steps=True)

    def paintEvent(self, e):
        # self.__updateStepsAttributes()
        return super().paintEvent(e)

    def setWaveformStyle(self, style: WaveformStyle, v_offset=0.0):
        self.waveform_style = style
        self.v_offset = v_offset
        if self.waveform_style != self.WaveformStyle.Normal:
            self._params_update = True
        else:
            self._params_update = False

        if self.waveform_style == self.WaveformStyle.Symmetrical:
            self.v_offset = 0.5

    def setFixedSize(self, size: QSize):
        super().setFixedSize(size)
        self.__triggerRefresh()

    def getCanvasSize(self) -> QSize:
        return super().getCanvasSize()

    def setPadding(self, padding):
        """Set padding"""
        self._padding = int(padding)

        self.__triggerRefresh()

    def setSolidPercent(self, f):
        """Set step solid percent"""
        self._bar_solid_percent = float(f)

        self.__triggerRefresh()

    def setMaxValue(self, max: int) -> None:
        """Set max value"""
        self._vmax = max

        self.__triggerRefresh()

    def setMinValue(self, min: int) -> None:
        """Set min value"""
        self._vmin = min

        self.__triggerRefresh()


if __name__ == "__main__":
    from PyQt5.QtWidgets import QVBoxLayout, QPushButton

    app = QApplication(sys.argv)
    window = QMainWindow()

    n_steps = 50
    layout = QVBoxLayout()

    fixed_size = QSize(500, 300)
    main_widget = QtWidgets.QWidget()

    waveform = WaveformSlider(n_steps, Qt.Orientation.Horizontal)
    waveform.setWaveformStyle(WaveformSlider.WaveformStyle.Symmetrical)
    waveform.setAddPagetyle(WaveformSlider.AddPageStyle.Outline)
    waveform.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
    waveform.setFixedSize(fixed_size)

    waveform.setSolidPercent(0.5)

    values = [round(random.random(), 2) for _ in range(n_steps)]
    waveform.setWaveformFunction(values)

    button = QPushButton()
    layout.addWidget(waveform)
    layout.addWidget(button)
    main_widget.setLayout(layout)
    # main_widget.setFixedSize(QSize(600, 400))

    window.setCentralWidget(main_widget)
    window.show()
    app.exec()
