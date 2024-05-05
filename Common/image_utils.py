from PyQt5.QtGui import QPixmap, QColor, QPainter, QBrush
from PyQt5.QtCore import Qt
from colorthief import ColorThief
import colorsys


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
    #color_thief = ColorThief(img_path)
    #palette = color_thief.get_palette(color_count=2, quality=5)

    palette = ColorPalette.get_image_palette(img_path)

    return palette


def get_image_primary_color(img_path: str) -> tuple:
    colorthief = ColorThief(img_path)
    primary_color = colorthief.get_color(quality=5)
    return primary_color


class ColorPalette:
    @classmethod
    def get_image_palette(cls, img_path: str) -> list:
        """
        Get image color palette with low contrast between colors
        """
        color_thief = ColorThief(img_path)

        if max(color_thief.image.size) > 500:
            color_thief.image = color_thief.image.resize((400, 400))

        palette = color_thief.get_palette(color_count=6, quality=9)

        color_luminance = [cls.get_color_luminance(cls.normalize_color(color)) for color in palette]

        # Sum color contrast ratio between all colors
        color_contrast_r = [cls.get_contrast_ratio(color, color_luminance) / len(color_luminance)
                            for color in color_luminance]

        primary_contrast = [{'contrast': cls.get_single_contrast_ratio(palette[0], palette[i]),
                             'color': palette[i]} for i in range(1, len(palette)-1)]
        primary_contrast = sorted(primary_contrast, key=lambda d: d['contrast'])

        relative_to_primary = [{'color': palette[0], 'contrast': 0.0}, *primary_contrast[:2]]
        relative_to_primary = [color['color'] for color in relative_to_primary]

        color_obj = [{'color': palette[i], 'contrast': color_contrast_r[i]} for i in range(len(palette))]
        color_obj = sorted(color_obj, key=lambda d: d['contrast'])

        # low contrast include the primary color
        low_contrast = color_obj[:3]
        high_contrast = color_obj[3:]

        low_contrast = [color['color'] for color in low_contrast]
        high_contrast = [color['color'] for color in high_contrast]

        hex_colors = ["#{:02x}{:02x}{:02x}".format(c[0], c[1], c[2]) for c in palette]
        low_contrast_hex = ["#{:02x}{:02x}{:02x}".format(c[0], c[1], c[2]) for c in low_contrast]
        high_contrast_hex = ["#{:02x}{:02x}{:02x}".format(c[0], c[1], c[2]) for c in high_contrast]
        primary_contrast_hex = ["#{:02x}{:02x}{:02x}".format(c[0], c[1], c[2]) for c in relative_to_primary]
        print(f"Color luminance: {color_luminance}")
        print(f"Color luminance avg: {sum(color_luminance) / len(color_luminance)}")
        print(f"Color contrast: {color_contrast_r}")
        print(f"Color contrast svg: {sum(color_contrast_r) / len(color_contrast_r)}")
        print(f"Colors: {hex_colors}")
        print(f"Low Contrast: {low_contrast_hex}")
        print(f"High Contrast: {high_contrast_hex}")
        print(f"Primary Contrast: {primary_contrast_hex}\n\n")

        return relative_to_primary

    @classmethod
    def get_contrast_ratio(cls, color: float, comp: list, cr_sum=0.0):
        if len(comp):
            L1 = color
            L2 = comp[-1]
            cr_sum += (max(L1, L2) + 0.05) / (min(L1, L2) + 0.05)
            return cls.get_contrast_ratio(color, comp[:-1], cr_sum=cr_sum)
        else:
            return cr_sum

    @classmethod
    def get_single_contrast_ratio(cls, p_color: tuple, s_color: tuple) -> float:
        L1 = cls.get_color_luminance(p_color)
        L2 = cls.get_color_luminance(s_color)
        return (max(L1, L2) + 0.05) / (min(L1, L2) + 0.05)

    @staticmethod
    def get_color_luminance(color: tuple) -> float:
        """
        Relative luminance
        """
        return 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]

    @staticmethod
    def rgb2hsv(color: tuple) -> tuple:
        norm_color = [channel / 255.0 for channel in color]
        return colorsys.rgb_to_hsv(*norm_color)

    @staticmethod
    def normalize_color(color: tuple) -> tuple:
        return tuple([channel / 255.0 for channel in color])
