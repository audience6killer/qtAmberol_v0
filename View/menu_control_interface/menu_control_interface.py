"""
Menu control interface
"""
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from .menu_control_widget import MenuControlWidget

from Common.signal_bus import signal_bus
from Common.style_sheet import setStyleSheet


class MenuControlInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.menu_control = MenuControlWidget()

        self.main_layout = QVBoxLayout()

        self.setup_ui()

        self.__connectSignalsToSlots()

    def setup_ui(self):
        """Setup ui"""
        self.setObjectName("menu_control_interface")

        self.main_layout.addWidget(self.menu_control)

        self.setLayout(self.main_layout)

    def __connectSignalsToSlots(self):
        """Connect signals to slots"""
        signal_bus.state_colors_updated_signal.connect(self.updateWidgetColors)

    def updateWidgetColors(self, state_colors):
        """Update widget colors"""
        setStyleSheet(self, state_colors)

