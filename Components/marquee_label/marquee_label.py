from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QLabel


class MarqueeLabel(QLabel):
    def __init__(self, text="", pixel_limit=200, parent=None):
        super(MarqueeLabel, self).__init__(parent)

        self._pixel_limit = pixel_limit
        self._is_scrolling = False
        self._original_text = text
        self._shortened_text = text
        self.setText(text)
        self.current_pos = 0
        self.scroll_timer = QTimer(self)

    @property
    def is_scrolling(self):
        return self._is_scrolling

    @is_scrolling.setter
    def is_scrolling(self, value):
        self._is_scrolling = value
        if self._is_scrolling and self.fontMetrics().boundingRect(self._original_text).width() > self._pixel_limit:
            self.scroll_timer.start(50)  # Adjust the speed by changing the interval (ms)
        else:
            # return to its original place
            self.current_pos = 0
            super(MarqueeLabel, self).setText(self._shortened_text)
            self.scroll_timer.stop()
            self.update()

    def scroll_text(self):
        self.current_pos -= 1  # Adjust the speed by changing this value
        print(self.current_pos)
        super().setText(f"{self._original_text}\t")

        if self.current_pos < -self.fontMetrics().boundingRect(self.text()).width():
            self.current_pos = 0

        self.update()

    def setText(self, text):
        if self._original_text != text:
            self._original_text = text

        if self.fontMetrics().boundingRect(text).width() > self._pixel_limit:
            while self.fontMetrics().boundingRect(text).width() > self._pixel_limit:
                text = text[:-1]
            text = text + "..."

        self._shortened_text = text
        super(MarqueeLabel, self).setText(text)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.palette().windowText().color())
        text_width = self.fontMetrics().width(self.text())
        text_height = self.fontMetrics().height()

        painter.drawText(self.current_pos, (self.height() + text_height) // 2, self.text())
        # If the text is outside the widget, redraw it from the other side
        if self.current_pos < 0:
            painter.drawText(self.current_pos + text_width, (self.height() + text_height) // 2, self.text())

        painter.end()
