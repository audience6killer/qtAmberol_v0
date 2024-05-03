"""
Menu control interface
"""

from PyQt5.QtWidgets import QVBoxLayout, QWidget

from .menu_control_widget import MenuControlWidget


class MenuControlInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.menu_control = MenuControlWidget()

        self.main_layout = QVBoxLayout()

        self.setup_ui()

    def setup_ui(self):
        """Setup ui"""

        self.main_layout.addWidget(self.menu_control)

        self.setLayout(self.main_layout)
