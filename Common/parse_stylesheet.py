import colorsys

def determine_alpha_channel(current_color: list):
    [red, green, blue] = [n_color / 255 for n_color in current_color]

    [h, s, v] = colorsys.rgb_to_hsv(red, green, blue)

    if v > s:
        [alpha_bg, alpha_border, alpha_bg_hover] = [0.3, 0.7, 0.4]
    else:
        [alpha_bg, alpha_border, alpha_bg_hover] = [0.2, 0.5, 0.3]

    return [alpha_bg, alpha_border, alpha_bg_hover]


def generate_css(current_color: list):
    with open("./resource/qss/main_window.qss", 'r') as f:
        stylesheet = f.read()

    if len(current_color) > 3:
        raise IndexError

    [red, green, blue] = current_color
    [alpha_bg, alpha_border, alpha_bg_hover] = determine_alpha_channel(current_color)

    stylesheet = stylesheet.replace('$red', str(red))
    stylesheet = stylesheet.replace('$blue', str(blue))
    stylesheet = stylesheet.replace('$green', str(green))
    stylesheet = stylesheet.replace('$alpha_bg_normal', str(alpha_bg))
    stylesheet = stylesheet.replace('$alpha_border', str(alpha_border))
    stylesheet = stylesheet.replace('$alpha_bg_hover', str(alpha_bg_hover))

    with open("./resource/qss/main_window.css", 'w') as f:
        f.write(stylesheet)




