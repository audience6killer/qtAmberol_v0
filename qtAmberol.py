import os
import sys
from inspect import getsourcefile
from pathlib import Path

from PyQt5.QtWidgets import QApplication
from Common.style_sheet import getStyleSheet

from PyQt5.QtCore import Qt

os.chdir(Path(getsourcefile(lambda: 0)).resolve().parent)

from View.main_window import MainWindowUI

ALBUM_COVER = "./resource/images/test-images/album-cover-test-3.jpg"

QApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

app = QApplication(sys.argv)

# app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

#colors = get_image_color_palette(ALBUM_COVER)
ui = MainWindowUI()

#app.setStyleSheet(getStyleSheet('main_window'))
# ui.setup_ui(main_window)

ui.show()

app.exec_()
