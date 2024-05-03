"""
Timestamp widget
"""

from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QSizePolicy


class TimestampWidget(QWidget):

    timestamp_chaged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Main widget layout
        self.main_layout = QHBoxLayout()

        self.time_left_label = QLabel()

        self.time_current_label = QLabel()

        self.setup_ui()

    def setup_ui(self):

        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.time_left_label.setObjectName("left-timestamp")
        self.time_current_label.setObjectName("current-timestamp")

        # Default text initialization
        self.time_left_label.setText("00:00")
        self.time_current_label.setText("00:00")

        self.time_left_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.time_current_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.time_left_label.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed
        )
        self.time_current_label.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed
        )
        #self.setFixedSize(QSize(230, 30))
        self.main_layout.addWidget(self.time_current_label)
        self.main_layout.addWidget(self.time_left_label)

        self.setLayout(self.main_layout)

    def update_timestamps(self, values: list):
        """Update timestamps"""
        self.time_current_label.setText(values[0])
        self.time_left_label.setText(values[1])
