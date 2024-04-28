"""
Album cover interface
"""

from PyQt5.QtCore import pyqtSignal

from album_cover_widget import AlbumCover


class AlbumCoverInterface:

    songCoverNext = pyqtSignal(int)

    def __init__(self, parent=None):
        self.album_cover = AlbumCover()
        self.__initWidget()

    def __initWidget(self):
        pass

    def updateCoverImage(self, arg):
        pass
