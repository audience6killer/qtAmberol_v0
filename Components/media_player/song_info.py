from dataclasses import dataclass
from PyQt5.QtGui import QImage


@dataclass
class SongInfo:
    file: str = None
    title: str = None
    artist: str = None
    album: str = None
    album_cover: QImage = None
    duration: int = None
    #year: int = None
    #genre: str = None
    #track: int = None
    #trackTotal: int = None
    #disc: int = None
    #discTotal: int = None
    #createTime: int = None
    #modifiedTime: int = None

