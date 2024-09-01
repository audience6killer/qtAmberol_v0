from PyQt5.QtCore import Qt, QPropertyAnimation, QTimer
from PyQt5.QtWidgets import QScrollBar


class PlaylistScrollBar(QScrollBar):

    def __init__(self, orientation=Qt.Vertical, parent=None):
        super(PlaylistScrollBar, self).__init__(orientation, parent)

        self.setMinimumWidth(0)  # Set minimum width to avoid complete disappearance
        self.setMaximumWidth(15)  # Fixed width for better visibility during the hide/show animation

        # Create a property animation for fading in/out
        self.animation = QPropertyAnimation(self, b"maximumWidth")
        self.animation.setDuration(100)  # Duration of the animation in milliseconds

        # Timer to delay the hiding of the scrollbar
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide_scrollbar)

        # Start hidden
        self.hide_scrollbar()

    def show_scrollbar(self):
        self.hide_timer.stop()  # Stop the hide timer if the user interacts
        self.animation.stop()  # Stop any ongoing animation
        self.animation.setStartValue(self.width())  # Set the current width as the start value
        self.animation.setEndValue(12)  # Set the end value to the full width
        self.animation.start()  # Start the animation

    def hide_scrollbar(self):
        self.animation.stop()  # Stop any ongoing animation
        self.animation.setStartValue(self.width())  # Set the current width as the start value
        self.animation.setEndValue(0)  # Set the end value to a very small width
        self.animation.start()  # Start the animation

    def enterEvent(self, event):
        self.show_scrollbar()  # Show scrollbar on mouse enter
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hide_timer.start(1000)  # Start the hide timer with a 1-second delay
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.show_scrollbar()  # Show scrollbar on mouse press
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.hide_timer.start(1000)  # Start the hide timer with a 1-second delay
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        self.show_scrollbar()  # Show scrollbar on scroll
        self.hide_timer.start(1000)  # Start the hide timer with a 1-second delay
        super().wheelEvent(event)

