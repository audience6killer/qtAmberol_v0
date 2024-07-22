
import numpy as np
from pydub import AudioSegment

from PyQt5.QtCore import QThread, pyqtSignal


class WaveformValuesThread(QThread):

    waveform_finished = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.track_path = ""
        self.n_samples = 0
        self.values = []

    def run(self):
        if not self.track_path:
            return

        audio = AudioSegment.from_file(self.track_path).set_channels(1)
        sample_data = np.array(audio.get_array_of_samples())
        max_value = max(abs(sample_data))
        normalized_samples = sample_data / max_value
        self.values = self.downsample_audio_rms(normalized_samples, self.n_samples)
        self.waveform_finished.emit(self.values)

    def setTrack(self, path: str, n_samples: int = 60):
        """Set track path"""
        self.track_path = path
        self.n_samples = n_samples

    @staticmethod
    def downsample_audio_rms(audio_samples, reduced_sample_count):
        segment_length = len(audio_samples) // reduced_sample_count
        downsampled = np.array([
            np.sqrt(np.mean(audio_samples[i * segment_length:(i + 1) * segment_length] ** 2))
            for i in range(reduced_sample_count)
        ])
        new_max = max(abs(downsampled))
        downsampled = downsampled / new_max
        return downsampled.tolist()










