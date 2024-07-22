
from .metasingleton import Singleton
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtMultimedia import QMediaPlayer


class SignalBus(QObject, Singleton):
    """Signalbus"""
    # Menu Options
    open_file_signal = pyqtSignal(str)
    open_folder_signal = pyqtSignal()

    # Playback options
    toggle_play_state_signal = pyqtSignal()

    # Metadata options
    metadata_song_signal = pyqtSignal(dict)

    # Progress bar options
    update_waveform_signal = pyqtSignal(str)
    waveform_is_ready_signal = pyqtSignal()

    # Volume options
    mute_volume_signal = pyqtSignal()
    increase_volume_signal = pyqtSignal()
    volume_scroll_changed_signal = pyqtSignal(int)

    # Main window options
    repaint_main_window_signal = pyqtSignal()


signal_bus = SignalBus()
