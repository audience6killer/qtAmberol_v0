import colorsys

from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QWidget

from Common import resources


def determine_color_degradation(current_color: tuple):
    [red, green, blue] = [n_color / 255 for n_color in current_color]

    [h, s, v] = colorsys.rgb_to_hsv(red, green, blue)

    bg_color = current_color
    border_color = [int(ch * 255) for ch in colorsys.hsv_to_rgb(h, s, v * 0.80)]
    hover_color = [int(ch * 255) for ch in colorsys.hsv_to_rgb(h, s, v * 1.30)]

    return [bg_color, border_color, hover_color]


def generate_css(object_name: str, current_color: tuple):
    file = QFile(f":/qss/{object_name}.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stylesheet = QTextStream(file).readAll()
    file.close()

    if len(current_color) > 3:
        current_color = current_color[:3]

    [bg_color, border_color, hover_color] = determine_color_degradation(current_color)
    [alpha_bg, alpha_border, alpha_bg_hover] = [0.3, 0.3, 0.3]

    print(f"{bg_color} {border_color} {hover_color}")

    stylesheet = stylesheet.replace('$red_bg', str(bg_color[0]))
    stylesheet = stylesheet.replace('$blue_bg', str(bg_color[2]))
    stylesheet = stylesheet.replace('$green_bg', str(bg_color[1]))
    stylesheet = stylesheet.replace('$red_hover', str(hover_color[0]))
    stylesheet = stylesheet.replace('$blue_hover', str(hover_color[2]))
    stylesheet = stylesheet.replace('$green_hover', str(hover_color[1]))
    stylesheet = stylesheet.replace('$red_border', str(border_color[0]))
    stylesheet = stylesheet.replace('$blue_border', str(border_color[2]))
    stylesheet = stylesheet.replace('$green_border', str(border_color[1]))
    stylesheet = stylesheet.replace('$alpha_bg_normal', str(alpha_bg))
    stylesheet = stylesheet.replace('$alpha_border', str(alpha_border))
    stylesheet = stylesheet.replace('$alpha_bg_hover', str(alpha_bg_hover))

    return stylesheet


def setStyleSheet(widget: QWidget, primary_color: tuple) -> None:
    stylesheet = generate_css(widget.objectName(), primary_color)
    widget.setStyleSheet(stylesheet)
