"""
Progress bar interface
"""

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from .progress_bar_widget import ProgressBarWidget
from .timestamp_widget import TimestampWidget


class ProgressBarInterface(QWidget):

    song_position_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.steps = 20
        self.orientation = Qt.Orientation.Horizontal

        # Widget Layout
        self.progress_layout = QVBoxLayout()

        # Progress widget
        self.progress_widget = ProgressBarWidget(self.steps, self.orientation, self)

        # Timestamp widget
        self.timestamp_widget = TimestampWidget(self)

        self.setup_ui()

    def setup_ui(self):
        """Setup ui"""

        self.progress_layout.addWidget(self.progress_widget)
        self.progress_layout.addWidget(self.timestamp_widget)

        self.setLayout(self.progress_layout)
