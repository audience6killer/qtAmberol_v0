import sys
import math

from enum import Enum
from typing import List, Dict, Union

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QEvent, QPoint, QSize, Qt, QPointF, QRectF, QSizeF
from PyQt5.QtGui import QColor

"""
TODO:   Fix colors saturation   
        Fix sizing problem
        
        Add gradient option
"""


class SegmentedSlider(QtWidgets.QWidget):

    clicked_value_signal = QtCore.pyqtSignal(int)

    class AddPageStyle(Enum):
        Empty = 0
        Fill = 1
        Outline = 2

    def __init__(self, steps, orientation: Qt.Orientation, parent=None):
        super().__init__(parent)

        # Default slider values
        self._value = 100
        self._vmin = 0
        self._vmax = 100

        # Events flags
        self._is_clicked = False
        self._is_hovering = False
        self._is_manually_modified = False

        # Widget to expand within its parent
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )

        # Widget styling
        self._step_color = QtGui.QColor(100, 100, 100)
        self._hover_color = self._step_color.darker(100)
        self._inactive_color = self._step_color.lighter(100)
        self._addpage_style = self.AddPageStyle.Empty

        # Widget orientation
        if isinstance(orientation, Qt.Orientation):
            self._orientation = orientation
        else:
            raise TypeError("Orientation must be a Qt.Orientation enum member")

        # Widget canvas attributes
        self._padding = 4
        self.canvas_height = super().size().height() - (self._padding * 2)
        self.canvas_width = super().size().width() - (self._padding * 2)
        self._background_color = QtGui.QColor("transparent")

        # Steps attributes
        self.n_active_steps = 0
        self.setSteps(steps)
        self._steps_data = []  # type: List[Dict[str, any]]
        self._bar_solid_percent = 0.5

        self.__updateStepsAttributes()

        # Hovering attributes
        self._hovering_step = 0
        self.setAttribute(Qt.WidgetAttribute.WA_Hover)
        self.setAttribute(Qt.WidgetAttribute.WA_NoMousePropagation)

        # Event filter
        self.installEventFilter(self)

    def sizeHint(self):
        if self._orientation == Qt.Orientation.Horizontal:
            return QSize(300, 200)
        else:
            return QSize(200, 300)

    def setSteps(self, steps=10):
        """Sets the number of steps and the type"""
        if isinstance(steps, list):
            # list of colors
            self.n_steps = len(steps)
            self.steps = steps

        elif isinstance(steps, int):
            self.n_steps = steps
            self.steps = steps * [1]

        else:
            raise TypeError("Steps must be a list or int")

    def setFixedSize(self, size: QSize):
        """setFixedSize: Sets widget fixed size and updates the step attributes"""
        super().setFixedSize(size)
        self.canvas_height = self.size().height() - (self._padding * 2)
        self.canvas_width = self.size().width() - (self._padding * 2)

        # self.__updateStepsAttributes()
        self.triggerRefresh(update_steps=True)

    def paintEvent(self, e):
        """paintEvent"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        brush = QtGui.QBrush()
        brush.setColor(self._background_color)
        brush.setStyle(Qt.BrushStyle.SolidPattern)

        # The background of the widget is painted
        rect = QtCore.QRect(
            QPoint(0, 0),
            QSize(self.canvas_width, self.canvas_height),
        )

        painter.fillRect(rect, brush)

        ## Draw the bars

        # Calculate the y-stop position, from the value in range.
        if not self._is_manually_modified:
            selected_step = (self._value - self._vmin) / (self._vmax - self._vmin)
            self.n_active_steps = int(selected_step * self.n_steps)
            self.n_active_steps = max(min(self.n_active_steps, self.n_steps), 0)
        else:
            self._is_manually_modified = False

        # Draw active steps

        for n in range(self.n_active_steps):
            active_step_color = self._step_color

            if self._is_hovering and n >= self._hovering_step:
                active_step_color = self._hover_color

            brush.setColor(active_step_color)
            rect = QRectF(
                self._steps_data[n]["pos"],
                self._steps_data[n]["size"],
            )

            painter.fillRect(rect, brush)

        # Draw inactive steps
        if self._addpage_style != self.AddPageStyle.Empty:
            # We start to draw the add page where the active pages ended
            for n in range(self.n_active_steps, self.n_steps):
                # The colors should be according to the last actual page color placed
                inactive_step_color = self._inactive_color

                if self._is_hovering and n < self._hovering_step:
                    inactive_step_color = self._step_color

                rect = QtCore.QRectF(
                    self._steps_data[n]["pos"],
                    self._steps_data[n]["size"],
                )

                if self._addpage_style == self.AddPageStyle.Outline:
                    pen = QtGui.QPen(inactive_step_color)
                    painter.setPen(pen)
                    painter.drawRect(rect)
                elif self._addpage_style == self.AddPageStyle.Fill:
                    brush.setColor(inactive_step_color)
                    painter.fillRect(rect, brush)

        painter.end()

    def __updateStepsAttributes(self) -> None:
        """Updates step attributes: step thickness, total size and position"""
        self._step_size = (
            self.canvas_height / self.n_steps
            if self._orientation == Qt.Orientation.Vertical
            else self.canvas_width / self.n_steps
        )

        self.bar_thickness = self._step_size * self._bar_solid_percent
        if self._orientation == Qt.Orientation.Vertical:
            self._steps_data = [
                {
                    "pos": QPointF(
                        self._padding,
                        self._padding + self.canvas_height - (1 + n) * self._step_size,
                    ),
                    "size": QSizeF(self.canvas_width, self.bar_thickness),
                }
                for n in range(self.n_steps)
            ]

        elif self._orientation == Qt.Orientation.Horizontal:
            self._steps_data = [
                {
                    "pos": QPointF(
                        self._padding + n * self._step_size,
                        self._padding,
                    ),
                    "size": QSizeF(
                        self.bar_thickness,
                        (self.canvas_height - self._padding),
                    ),
                }
                for n in range(self.n_steps)
            ]

    def triggerRefresh(self, update_steps=True):
        if update_steps:
            self.__updateStepsAttributes()
        self.update()

    def __calculateMouseHoveringPosition(self, e):
        """Calculates mouse hovering step"""
        click_pos = 0.0
        active_pct = 0.0

        if self._orientation == Qt.Orientation.Vertical:
            click_pos = e.pos().y() - self._padding - self._step_size
            active_pct = (self.canvas_height - click_pos) / self.canvas_height
        elif self._orientation == Qt.Orientation.Horizontal:
            click_pos = e.pos().x() - self._padding + self._step_size
            active_pct = (self.canvas_width - click_pos) / self.canvas_width

        hover_value = int(self._vmin + active_pct * (self._vmax - self._vmin))
        hover_value = max(min(hover_value, self._vmax), self._vmin)
        hover_value = (
            hover_value
            if self._orientation == Qt.Orientation.Vertical
            else 100 - hover_value
        )
        hover_value = (hover_value - self._vmin) / (self._vmax - self._vmin)
        self._hovering_step = int(hover_value * self.n_steps)
        self.triggerRefresh(update_steps=False)

    def __stopHoverEffect(self, e):
        """Stops mouse hovering effect"""
        self.triggerRefresh(update_steps=False)

    def __calculateClickedValue(self, e):
        """Calculates clicked value within the _vmax and _vmin values"""
        # parent = self.parent()
        click_pos = 0.0
        active_pct = 0.0

        if self._orientation == Qt.Orientation.Vertical:
            # self._step_size = self.canvas_height / self.n_steps
            click_pos = e.pos().y() - self._padding - self._step_size
            active_pct = (self.canvas_height - click_pos) / self.canvas_height

        elif self._orientation == Qt.Orientation.Horizontal:
            # self._step_size = self.canvas_width / self.n_steps
            click_pos = e.pos().x() - self._padding + self._step_size
            active_pct = (self.canvas_width - click_pos) / self.canvas_width
            # active_pct = 1 - active_pct
            # active_pct = (click_pos - self.canvas_width) / self.canvas_width

        value = int(self._vmin + active_pct * (self._vmax - self._vmin))
        self.value = max(min(value, self._vmax), self._vmin)
        self._value = (
            value if self._orientation == Qt.Orientation.Vertical else 100 - value
        )

        if not self._is_clicked:
            self.clicked_value_signal.emit(self._value)

        self.triggerRefresh(update_steps=False)

    def eventFilter(self, obj, e: QEvent):
        """Event filter"""
        # events must be ordered by priority
        if obj is self:
            if e.type() == QEvent.Type.MouseMove:
                self.__calculateClickedValue(e)
            elif e.type() == QEvent.Type.MouseButtonPress:
                self._is_clicked = True
                self.__calculateClickedValue(e)
            elif e.type() == QEvent.Type.MouseButtonRelease:
                self._is_clicked = False
                self.__calculateClickedValue(e)
            elif e.type() == QEvent.Type.HoverLeave:
                self._is_hovering = False
                self.__stopHoverEffect(e)
            elif e.type() == QEvent.Type.HoverEnter:
                self._is_hovering = True
                self.__calculateMouseHoveringPosition(e)
            elif e.type() == QEvent.Type.HoverMove:
                if not self._is_clicked:
                    self.__calculateMouseHoveringPosition(e)

        return super().eventFilter(obj, e)

    def setColor(self, color: Union[QtGui.QColor, list]):
        """Sets a uniform color for all steps"""
        if type(color) is QtGui.QColor:
            self._step_color = color
            self._inactive_color = self._step_color.lighter(200)
            self._hover_color = self._step_color.lighter(180)
        else:
            self._step_color = color[2]
            self._hover_color = color[1]
            self._inactive_color = color[0]
        self.triggerRefresh(update_steps=False)

    def setPadding(self, padding):
        """Set padding"""
        self._padding = int(padding)

        # self.__updateStepsAttributes()
        self.triggerRefresh(update_steps=True)

    def setSolidPercent(self, f):
        """Set step solid percent"""
        self._bar_solid_percent = float(f)

        # self.__updateStepsAttributes()
        self.triggerRefresh(update_steps=True)

    def setBackgroundColor(self, color):
        """Set background color"""
        self._background_color = QtGui.QColor(color)
        self.triggerRefresh(update_steps=False)

    def setAddPagetyle(self, style: AddPageStyle):
        """Set add page style"""
        self._addpage_style = style
        self.triggerRefresh(update_steps=False)

    def setMaxValue(self, max: int) -> None:
        """Set max value"""
        self._vmax = max

        # self.__updateStepsAttributes()
        self.triggerRefresh(update_steps=True)

    def setMinValue(self, min: int) -> None:
        """Set min value"""
        self._vmin = min

        # self.__updateStepsAttributes()
        self.triggerRefresh(update_steps=True)

    def enableAutomaticStepsParamsUpdate(self, enable):
        self.automatic_steps_update = enable

    def getCanvasSize(self) -> QSize:
        return QSize(self.canvas_width, self.canvas_height)

    def increaseSliderValue(self):
        if self.n_active_steps < self.n_steps:
            self.n_active_steps += 1
            self._value = ((self._vmax - self._vmin) / self.n_steps) * self.n_active_steps
            self._is_manually_modified = True
            self.triggerRefresh(update_steps=False)

    def setActiveSteps(self, steps: int):
        if steps <= self.n_steps:
            self.n_active_steps = steps
            self._value = ((self._vmax - self._vmin) / self.n_steps) * self.n_active_steps
            self._is_manually_modified = True
            self.triggerRefresh(update_steps=False)

    def setValue(self, value: int):
        if value in range(self._vmin, self._vmax + 1):
            self._value = value
            self._is_manually_modified = False
            self.triggerRefresh(update_steps=False)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    # slider = SegmentedSlider(
    #    [
    #        "#49006a",
    #        "#7a0177",
    #        "#ae017e",
    #        "#dd3497",
    #        "#f768a1",
    #        "#fa9fb5",
    #        "#fcc5c0",
    #        "#fde0dd",
    #        "#fff7f3",
    #    ],
    #    Qt.Orientation.Horizontal,
    # )
    # Horizontal
    # fixed_size = QSize(500, 100)
    # slider = SegmentedSlider(50, Qt.Orientation.Horizontal)
    # slider.setAddPagetyle(SegmentedSlider.AddPageStyle.Fill)
    # Vertical
    fixed_size = QSize(100, 300)
    slider = SegmentedSlider(50, Qt.Orientation.Vertical)
    slider.setAddPagetyle(SegmentedSlider.AddPageStyle.Fill)

    slider.setFixedSize(fixed_size)
    window.setFixedSize(fixed_size)
    window.setCentralWidget(slider)

    window.show()
    app.exec()
