from PyQt5.QtGui import QPixmap, QColor, QPainter, QBrush
from PyQt5.QtCore import Qt
from colorthief import ColorThief


def get_rounded_pixmap(pixmap: QPixmap, radius=25) -> QPixmap:
    """
    A function to get a pixmap with rounded corners
    :param pixmap: Pixmap to round
    :param radius: Corner radius
    :return: Pixmap rounded
    """
    rounded = QPixmap(pixmap.size())
    rounded.fill(QColor("transparent"))

    # draw rounded rect on new pixmap using original pixmap as brush
    painter = QPainter(rounded)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QBrush(pixmap))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(pixmap.rect(), radius, radius)

    return rounded


def get_image_color_palette(img_path: str) -> list:
    color_thief = ColorThief(img_path)
    palette = color_thief.get_palette(color_count=2, quality=5)

    return palette


def get_image_primary_color(img_path: str) -> tuple:
    colorthief = ColorThief(img_path)
    primary_color = colorthief.get_color(quality=5)
    return primary_color
