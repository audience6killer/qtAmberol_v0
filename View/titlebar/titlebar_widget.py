from PyQt5.QtCore import QSize, QEvent, Qt
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QIcon, QColor

from Common.signal_bus import signal_bus
from Common.style_sheet import setStyleSheet


class TitleBar(QWidget):

    def __init__(self, parent=None):
        super(TitleBar, self).__init__(parent)

        self.main_layout = QHBoxLayout()

        self.close_button = QPushButton()
        self.minimize_button = QPushButton()

        self.setupUI()

        self.__connectSignalsToSlots()

    def setupUI(self):
        """Setup UI"""
        self.setObjectName("titlebar_widget")

        self.close_button.setObjectName("close-button")
        self.minimize_button.setObjectName("minimize-button")

        self.close_button.setFixedSize(QSize(20, 20))
        self.minimize_button.setFixedSize(QSize(20, 20))

        self.close_button.setIcon(QIcon(QPixmap(":/images/titlebar/close.svg")))
        self.minimize_button.setIcon(QIcon(":/images/titlebar/minimize.svg"))

        self.main_layout.setContentsMargins(5, 10, 5, 0)
        self.main_layout.addStretch()

        spacer = QSpacerItem(8, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addWidget(self.minimize_button)
        self.main_layout.addItem(spacer)
        self.main_layout.addWidget(self.close_button)

        self.setLayout(self.main_layout)

    def __connectSignalsToSlots(self):
        """Connect signals to slots"""
        signal_bus.state_colors_updated_signal.connect(self.updateWidgetColor)
        self.close_button.clicked.connect(signal_bus.close_window_signal)
        self.minimize_button.clicked.connect(signal_bus.minimize_window_signal)

    def updateWidgetColor(self, state_colors) -> None:
        """Update widget color"""
        setStyleSheet(self, state_colors)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.initial_pos = event.pos()

        super().mousePressEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        if self.initial_pos is not None:
            delta = event.pos() - self.initial_pos
            self.window().move(
                self.window().x() + delta.x(),
                self.window().y() + delta.y(),
            )
            self.setCursor(Qt.SizeAllCursor)
        super().mouseMoveEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event):
        self.initial_pos = None
        self.setCursor(Qt.ArrowCursor)
        super().mouseReleaseEvent(event)
        event.accept()




