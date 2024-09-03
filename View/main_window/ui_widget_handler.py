from PyQt5.QtCore import Qt, QPropertyAnimation, QSize, QRect, QEvent, QEasingCurve
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QMdiArea

from Common.signal_bus import signal_bus
from View.player_ui_interface import MainPlayerView
from View.playlist_side_menu_interface import PlaylistMenuView


class UIWidgetHandler(QMdiArea):

    def __init__(self, parent=None):
        super(UIWidgetHandler, self).__init__(parent)

        self.parent_size = parent.size()
        self.__is_playlist_visible = False
        self.setBackground(QBrush(Qt.transparent))
        self.setOption(QMdiArea.DontMaximizeSubWindowOnActivation)

        self.player_view = MainPlayerView(self)
        self.playlist_view = PlaylistMenuView(self)

        self.addSubWindow(self.player_view)
        self.addSubWindow(self.playlist_view)

        #self.player_view.showMaximized()
        #self.setActiveSubWindow(self.player_view)

        self.playlist_view.setGeometry(0, 0, 0, self.height())

        self.side_menu_visible = False

        self.__connectSignalsToSlots()

    def __connectSignalsToSlots(self):
        """Connect signals to slots"""
        signal_bus.playlist_view_open_signal.connect(self.showPlaylistView)
        #signal_bus.hide_playlist_view.connect(self.hidePlaylistView)
        self.subWindowActivated.connect(self.__windowActivated)

    def showPlaylistView(self):
        #self.playlist_view.setGeometry(0, 0, 0, self.height())
        self.playlist_view.resize(QSize(0, self.height()))
        self.animation = QPropertyAnimation(self.playlist_view, b"size")
        self.animation.setDuration(200)
        self.animation.setStartValue(QSize(0, self.height()))
        self.animation.setEndValue(QSize(int(self.width() * 0.55), self.height()))
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.animation.start()

        #self.animation.finished.connect(self.__onShowPlaylistViewAnimationFinished)
        self.playlist_view.show()
        self.setActiveSubWindow(self.playlist_view)
        self.player_view.showMaximized()  # Keep the player_view maximized
        self.__is_playlist_visible = True

        # Ensure the playlist_view stays on top
        self.playlist_view.raise_()

    def hidePlaylistView(self):
        self.animation = QPropertyAnimation(self.playlist_view, b"size")
        self.animation.setDuration(200)
        self.animation.setStartValue(self.playlist_view.size())
        self.animation.setEndValue(QSize(0, self.height()))
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.animation.start()

        self.animation.finished.connect(self.__onPlaylistHideAnimationFinished)

    def __onPlaylistHideAnimationFinished(self):
        self.playlist_view.hide()
        self.playlist_view.resize(QSize(0, self.height()))
        self.setActiveSubWindow(self.player_view)
        self.player_view.showMaximized()
        self.__is_playlist_visible = False

    def __windowActivated(self, sub_window):
        if sub_window == self.player_view:
            self.hidePlaylistView()
            signal_bus.playlist_view_is_visible.emit(False)
        elif sub_window == self.playlist_view:
            signal_bus.playlist_view_is_visible.emit(True)
        #print(f"Activated SubWindow: {sub_window.windowTitle()}")
