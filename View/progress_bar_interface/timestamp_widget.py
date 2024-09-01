"""
Timestamp widget
"""

from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QSizePolicy

from Common.signal_bus import signal_bus


class TimestampWidget(QWidget):

    timestamp_chaged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Main widget layout
        self.main_layout = QHBoxLayout()

        self.time_left_label = QLabel()

        self.time_current_label = QLabel()

        self._track_duration = None

        self.current_time = None
        self.time_left = None

        self.setup_ui()

        self.__connectSignalsToSlots()

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

    def updateTimestamps(self, pos: int):
        """Update timestamps"""
        if pos is not None and self._track_duration is not None:
            self.current_time = pos // 1000
            self.time_left = self._track_duration - self.current_time
            print(f"Current time: {self.current_time}, Left Time: {self.time_left}")
            self.time_current_label.setText(self.getTrackPositionToMinSec(self.current_time))
            self.time_left_label.setText("-" + self.getTrackPositionToMinSec(self.time_left))

    def setTrackDuration(self, duration: int):
        """Set track duration"""
        self._track_duration = duration
        self.time_left = duration
        self.current_time = 0

        self.time_left_label.setText("-" + self.getTrackPositionToMinSec(self.time_left))

    def __connectSignalsToSlots(self):
        """Connect signals to slots"""
        signal_bus.update_timestamp_signal.connect(self.updateTimestamps)

    @staticmethod
    def getTrackPositionToMinSec(pos) -> str:
        """ Convert from track position in seconds to min:sec"""
        t_seconds = pos
        t_minutes = 0
        seconds = 0
        if t_seconds:
            t_minutes = int(t_seconds // 60)
            seconds = int(t_seconds % 60)

        if t_minutes < 10:
            minutes_str = f"0{t_minutes}"
        else:
            minutes_str = f"{t_minutes}"

        if seconds < 10:
            seconds_str = f"0{seconds}"
        else:
            seconds_str = f"{seconds}"

        return minutes_str + ":" + seconds_str
