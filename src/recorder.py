import sounddevice as sd
import numpy as np
import wave
import time

class AudioRecorder:
    def __init__(self, config):
        self.config = config
        self.sample_rate = config.get("sample_rate", 16000)
        self.channels = config.get("channels", 1)
        self.duration = config.get("duration", 5)

    def record(self, duration=None):
        """
        Record audio for a specific duration.
        """
        record_seconds = duration if duration else self.duration
        print(f"Recording for {record_seconds} seconds...")

        recording = sd.rec(
            int(record_seconds * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype='int16'
        )
        sd.wait()
        print("Recording complete.")
        return recording

    def save_wav(self, audio_data, filename="command.wav"):
        """
        Save the recorded audio to a WAV file.
        """
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2) # 16-bit
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data.tobytes())
        return filename

    def get_stream(self, frame_length, callback):
        """
        Returns an InputStream for real-time processing (e.g., wake word).
        """
        return sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype='int16',
            blocksize=frame_length,
            callback=callback
        )
