from Components.media_player.song_info import SongInfo
from .metasingleton import Singleton
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QColor
from PyQt5.QtMultimedia import QMediaPlayer


class SignalBus(QObject, Singleton):
    """Signalbus"""
    # Menu Options
    open_file_signal = pyqtSignal(str)
    open_folder_signal = pyqtSignal(list)

    # Playback options
    toggle_play_state_signal = pyqtSignal()
    next_song_signal = pyqtSignal()
    previous_song_signal = pyqtSignal()

    # Metadata options
    metadata_song_signal = pyqtSignal(dict)

    # Progress bar options
    update_waveform_signal = pyqtSignal(str)
    waveform_is_ready_signal = pyqtSignal()
    progress_bar_clicked_value_signal = pyqtSignal(int)
    update_track_duration_signal = pyqtSignal(int)

    update_timestamp_signal = pyqtSignal(int)

    # Volume options
    mute_volume_signal = pyqtSignal()
    increase_volume_signal = pyqtSignal()
    volume_scroll_changed_signal = pyqtSignal(int)

    # Main window options
    repaint_main_window_signal = pyqtSignal()
    playlist_view_open_signal = pyqtSignal()
    close_window_signal = pyqtSignal()
    minimize_window_signal = pyqtSignal()

    # Media player signals
    track_position_changed_signal = pyqtSignal(int)

    # Colors signals
    primary_color_updated_signal = pyqtSignal(QColor)
    gradient_colors_updated_signal = pyqtSignal(list)

    # QMdi signals
    hide_playlist_view = pyqtSignal()

    # Playlist Signals
    track_added_to_playlist_signal = pyqtSignal(SongInfo)
    playlist_changed_signal = pyqtSignal(list)
    playlist_track_changed_signal = pyqtSignal(SongInfo)
    playlist_current_track_index_signal = pyqtSignal(int)
    playlist_track_clicked_index_signal = pyqtSignal(int)



signal_bus = SignalBus()
