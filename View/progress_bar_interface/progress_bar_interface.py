"""
Progress bar interface
"""

from PyQt5.QtCore import QSize, pyqtSignal, Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtGui import QColor

from .progress_bar_widget import ProgressBarWidget
from .timestamp_widget import TimestampWidget


class ProgressBarInterface(QWidget):

    song_position_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Widget Layout
        self.progress_layout = QVBoxLayout()

        # Progress widget
        self.progress_widget = ProgressBarWidget(self)

        # Timestamp widget
        self.timestamp_widget = TimestampWidget(self)

        self.setup_ui()

    def setup_ui(self):
        """Setup ui"""
        self.progress_layout.setContentsMargins(110, 0, 110, 0)

        self.progress_layout.addWidget(self.progress_widget)
        self.progress_layout.addWidget(self.timestamp_widget)

        self.progress_layout.setAlignment(Qt.AlignHCenter)
        #self.progress_layout.setContentsMargins(0, 0, 0, 0)
        self.progress_layout.setSpacing(0)

        self.setLayout(self.progress_layout)

    def setSliderColor(self, color: QColor):
        self.progress_widget.setSliderColor(color)

