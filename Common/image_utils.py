from PyQt5.QtGui import QPixmap, QColor, QPainter, QBrush, QImage
from PyQt5.QtCore import Qt
import fast_colorthief as fct
import numpy as np

import colorsys
import itertools


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


class Color:
    def __init__(self, rgb: tuple, priority: int):
        self.rgb = rgb
        self.priority = priority
        self.color_luminance = 0

        self.calculate_color_luminance()

    def __repr__(self):
        return "#{:02x}{:02x}{:02x}".format(self.rgb[0], self.rgb[1], self.rgb[2])

    def calculate_color_luminance(self):
        """
        Relative luminance
        """
        n_color = self.normalize_color(self.rgb)
        self.color_luminance = 0.2126 * n_color[0] + 0.7152 * n_color[1] + 0.0722 * n_color[2]

    @staticmethod
    def normalize_color(color: tuple) -> tuple:
        return tuple([channel / 255.0 for channel in color])


class ColorPalette:
    def __init__(self, image: QImage, subpalette_size=3):
        if image.width() > 500 or image.height() > 500:
            image = image.scaled(400, 400, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)

        # Ensure the image format is RGBA
        if image.format() != QImage.Format_RGBA8888:
            image = image.convertToFormat(QImage.Format_RGBA8888)

        # Get the size of the image
        width = image.width()
        height = image.height()

        # Get a pointer to the image data
        ptr = image.bits()
        ptr.setsize(image.byteCount())

        # Create a NumPy array from the data buffer
        np_image = np.array(ptr).reshape(height, width, 4)

        self.palette_tuple = fct.get_palette(np_image, color_count=6, quality=9)
        self.palette_list = [Color(rgb=value, priority=index + 1) for index, value in enumerate(self.palette_tuple)]
        self.combinations = self.list_combinations(self.palette_tuple, subpalette_size)
        self.subpalette_combinations = self.list_combinations(self.combinations[0], 2)
        self.subpalette_list = [{'palette': (self.palette_list[c[0]], self.palette_list[c[1]], self.palette_list[c[2]]),
                                 'cr': 0.0} for c in self.combinations]

        self.primary_color = (0, 0, 0)
        self.calculate_sub_palette_cr()

    def calculate_sub_palette_cr(self):
        """ Calculate subpalette contrast ratio"""
        for palette in self.subpalette_list:
            wg_avg = 0.0
            for comb in self.subpalette_combinations:
                palette['cr'] += self.calculate_two_colors_cr(palette['palette'][comb[0]], palette['palette'][comb[1]])
                wg_avg += min(palette['palette'][comb[0]].priority, palette['palette'][comb[1]].priority)

            palette['cr'] /= wg_avg

        self.subpalette_list = sorted(self.subpalette_list, key=lambda x: x['cr'])
        #print(self.subpalette_list)

    def get_min_contrast_palette(self):
        palette = [color.rgb for color in self.subpalette_list[0]['palette']]
        print(f"Chosen palette: Min Contrast - {palette}")
        return palette

    def get_primary_min_contrast_palette(self):
        """ Get palette with the primary color and the minimum contrast ratio"""
        r_palette = None
        for palette in self.subpalette_list:
            if self.palette_tuple[0] in [x.rgb for x in palette['palette']]:
                r_palette = [x.rgb for x in palette['palette']]

        print(f"Chosen palette: Primary relative - {r_palette}")
        return r_palette

    def get_dominant_color(self):
        """
        Estracted from: https://www.cnblogs.com/zhiyiYo/p/15815866.html
        """
        # 调整调色板明度
        palette = self.__adjust_palette_value(self.palette_tuple)
        for rgb in palette[:]:
            h, s, v = colorsys.rgb_to_hsv(*rgb)
            if h < 0.02:
                palette.remove(rgb)
                if len(palette) <= 2:
                    break

        # 挑选主题色
        palette = palette[:5]
        #palette.sort(key=lambda rgb: self.colorfulness(*rgb), reverse=False)

        self.primary_color = [int(channel) for channel in palette[0]]

        #print(f"Primary color: {self.primary_color}")
        return self.primary_color

    @staticmethod
    def calculate_two_colors_cr(p_color: Color, s_color: Color):
        L1 = p_color.color_luminance
        L2 = s_color.color_luminance
        return min(p_color.priority, s_color.priority) * (max(L1, L2) + 0.05) / (min(L1, L2) + 0.05)

    @staticmethod
    def list_combinations(palette, no_groups: int):
        return list(itertools.combinations([index for index, value in enumerate(palette)], no_groups))

    @classmethod
    def __adjust_palette_value(cls, palette: list):
        """ 调整调色板的明度 """
        newPalette = []
        for rgb in palette:
            h, s, v = colorsys.rgb_to_hsv(*rgb)

            if v > 0.9:
                factor = 0.8
            elif 0.8 < v <= 0.9:
                factor = 0.9
            elif 0.7 < v <= 0.8:
                factor = 0.95
            else:
                factor = 1

            v *= factor
            newPalette.append(colorsys.hsv_to_rgb(h, s, v))

        return newPalette

    @staticmethod
    def colorfulness(r: int, g: int, b: int):
        rg = np.absolute(r - g)
        yb = np.absolute(0.5 * (r + g) - b)

        rg_mean, rg_std = np.mean(rg), np.std(rg)
        yb_mean, yb_std = np.mean(yb), np.std(yb)

        std_root = np.sqrt(rg_std ** 2 + yb_std ** 2)
        mean_root = np.sqrt(rg_mean ** 2 + yb_mean ** 2)

        return std_root + 0.3 * mean_root

    def calculate_color_degradation(self):
        current_color = self.primary_color
        [red, green, blue] = [n_color / 255 for n_color in current_color]

        [h, s, v] = colorsys.rgb_to_hsv(red, green, blue)

        bg_color = current_color
        border_color = [int(ch * 255) for ch in colorsys.hsv_to_rgb(h, s, v * 0.75)]
        hover_color = [int(ch * 255) for ch in colorsys.hsv_to_rgb(h, s, v * 1.25)]

        return [bg_color, border_color, hover_color]


