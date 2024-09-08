import colorsys

from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QConicalGradient, QColor
from PyQt5.QtWidgets import QWidget

from Common import resources


def determine_color_degradation(current_color: tuple) -> list[QColor]:
    """Returns primary_color, hover_color and emphasis_color, in that order"""
    [red, green, blue] = [n_color / 255 for n_color in current_color]

    [h, l, s] = colorsys.rgb_to_hls(red, green, blue)

    print(f"Color to degrade: {(h, l, s)}")

    if l >= 0.80:
        hover_color = current_color
        bg_color = [int(ch * 255) for ch in colorsys.hls_to_rgb(h, l * 1.8, s)]
        emphasis_color = [int(ch * 255) for ch in colorsys.hls_to_rgb(h, l * 2.2, s)]
    elif l <= 0.25:
        if l <= 0.12:
            bg_pct = 2.0
            hover_oct = 3
        else:
            bg_pct = 2.6
            hover_oct = 1.4

        emphasis_color = current_color  # Darker color
        bg_color = [int(ch * 255) for ch in colorsys.hls_to_rgb(h, l * bg_pct, s)]  # Normal color
        hover_color = [int(ch * 255) for ch in colorsys.hls_to_rgb(h, l * hover_oct, s)]  # Brighter color
    else:
        bg_color = current_color
        hover_color = [int(ch * 255) for ch in colorsys.hls_to_rgb(h, l * 0.7, s)]
        emphasis_color = [int(ch * 255) for ch in colorsys.hls_to_rgb(h, l * 0.5, s)]

    [alpha_bg, alpha_emphasis, alpha_hover] = [0.3, 0.5, 0.3]
    primary_color = QColor(bg_color[0], bg_color[1], bg_color[2], alpha=int(255*alpha_bg))
    hover_color_ = QColor(hover_color[0], hover_color[1], hover_color[2], alpha=int(255*alpha_hover))
    emphasis_color_ = QColor(emphasis_color[0], emphasis_color[1], emphasis_color[2], alpha=int(255*alpha_emphasis))
    return [primary_color, hover_color_, emphasis_color_]


def generate_css(object_name: str, state_colors: list[QColor]):
    file = QFile(f":/qss/{object_name}.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stylesheet = QTextStream(file).readAll()
    file.close()

    if not state_colors:
        bg_color = (125, 125, 125, 0.3)
        hover_color = (125, 125, 125, 0.3)
        emphasis_color = (125, 125, 125, 0.3)
    else:
        bg_color = state_colors[0].getRgb()
        hover_color = state_colors[1].getRgb()
        emphasis_color = state_colors[2].getRgb()

    stylesheet = stylesheet.replace('$red_bg', str(bg_color[0]))
    stylesheet = stylesheet.replace('$green_bg', str(bg_color[1]))
    stylesheet = stylesheet.replace('$blue_bg', str(bg_color[2]))
    stylesheet = stylesheet.replace('$alpha_bg_normal', str(bg_color[3]))

    stylesheet = stylesheet.replace('$red_hover', str(hover_color[0]))
    stylesheet = stylesheet.replace('$green_hover', str(hover_color[1]))
    stylesheet = stylesheet.replace('$blue_hover', str(hover_color[2]))
    stylesheet = stylesheet.replace('$alpha_bg_hover', str(hover_color[3]))

    stylesheet = stylesheet.replace('$red_border', str(emphasis_color[0]))
    stylesheet = stylesheet.replace('$green_border', str(emphasis_color[1]))
    stylesheet = stylesheet.replace('$blue_border', str(emphasis_color[2]))
    stylesheet = stylesheet.replace('$alpha_border', str(emphasis_color[3]))

    return stylesheet


def setStyleSheet(widget: QWidget, state_colors: list[QColor]) -> None:
    stylesheet = generate_css(widget.objectName(), state_colors)
    widget.setStyleSheet(stylesheet)
