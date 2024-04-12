import sys
import math

from enum import Enum

from PyQt6 import QtWidgets
from PyQt6 import QtGui
from PyQt6.QtCore import QSize, Qt, QPointF, QSizeF
from PyQt6.QtGui import QWindow
from PyQt6.QtWidgets import QApplication, QMainWindow, QSizePolicy

from segmented_slider import SegmentedSlider


class WaveformSlider(SegmentedSlider):
    class WaveformStyle(Enum):
        FromLongitudinalAxis = 0
        Symmetrical = 1
        Normal = 2

    def __init__(self, steps, orientation: Qt.Orientation, parent=None):
        super().__init__(steps, orientation, parent)
        # super().enableAutomaticStepsParamsUpdate(False)
        self._params_update = (
            False  # True: this class updates the params; False: super() does it
        )

        self.v_offset = 0  # Vertical center, from which it will draw the steps
        self.waveform_style = self.WaveformStyle.Normal
        self.amplitude = self.n_steps * [1]

        # self.__updateStepsAttributes()

    def sizeHint(self):
        return super().sizeHint()

    def setWaveformFunction(self, f):
        if isinstance(f, list):
            self.amplitude = f[: self.n_steps]
        elif callable(f):
            limit = (
                self.canvas_width
                if self._orientation == Qt.Orientation.Vertical
                else self.canvas_height
            )
            if self.waveform_style == self.WaveformStyle.Symmetrical:
                self.amplitude = [abs(f(x)) for x in range(self.n_steps)]
                self.amplitude = [max(min(x, limit), 0) for x in self.amplitude]
            else:
                self.amplitude = [
                    max(min(f(x), limit), -limit) for x in range(self.n_steps)
                ]
        else:
            raise TypeError("Not a valid waveform function")

        self.__triggerRefresh()

    def __updateStepsAttributes(self) -> None:
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
                            (offset + self.amplitude[n])
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
                            else -self.amplitude[n] * 2
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
    from PyQt6.QtWidgets import QHBoxLayout, QPushButton

    app = QApplication(sys.argv)
    window = QMainWindow()

    n_steps = 50
    layout = QHBoxLayout()

    fixed_size = QSize(500, 300)
    main_widget = QtWidgets.QWidget()

    waveform = WaveformSlider(n_steps, Qt.Orientation.Horizontal)
    waveform.setAddPagetyle(WaveformSlider.AddPageStyle.Outline)
    waveform.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
    waveform.setFixedSize(fixed_size)

    waveform.setWaveformStyle(
        WaveformSlider.WaveformStyle.FromLongitudinalAxis, v_offset=0.5
    )

    def f(x):
        return -(waveform.getCanvasSize().width() / n_steps) * x

    def g(x):
        return (
            -0.5
            * math.sin((2 * math.pi / n_steps) * x)
            * waveform.getCanvasSize().height()
        )

    waveform.setWaveformFunction(g)

    button = QPushButton()
    layout.addWidget(waveform)
    layout.addWidget(button)
    main_widget.setLayout(layout)
    # main_widget.setFixedSize(QSize(600, 400))

    window.setCentralWidget(main_widget)
    window.show()
    app.exec()
