import os
import sys
from inspect import getsourcefile
from pathlib import Path

from PyQt5.QtWidgets import QApplication

# from PyQt5.Core import Qt

os.chdir(Path(getsourcefile(lambda: 0)).resolve().parent)

from View.main_window import MainWindowUI, Window
from Common.image_utils import get_image_color_palette

ALBUM_COVER = "./resource/images/test-images/album-cover-test.jpg"

# QApplication.setHighDpiScaleFactorRoundingPolicy(
#    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
# )
# QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
# QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

app = QApplication(sys.argv)
# app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

colors = get_image_color_palette(ALBUM_COVER)
main_window = Window(colors)
ui = MainWindowUI(main_window, app)
# ui.setup_ui(main_window)

main_window.show()

app.exec()
