from PyQt5.QtCore import QFile
from PyQt5.QtWidgets import QWidget

from .parse_stylesheet import generate_css


def getStyleSheet(file: str):
    """get style sheet

    Parameters
    ----------
    file: str
        qss file name, without `.qss` suffix
    """
    f = QFile(f"./resource/qss/{file}.css")
    f.open(QFile.ReadOnly)
    qss = str(f.readAll(), encoding="utf-8")
    f.close()
    return qss


def setStyleSheet(widget: QWidget, primary_color: tuple) -> None:
    obj_name = widget.objectName()
    generate_css(obj_name, primary_color)
    widget.setStyleSheet(getStyleSheet(obj_name))
