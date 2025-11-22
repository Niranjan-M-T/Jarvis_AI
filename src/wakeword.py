import os
import pvporcupine
import struct

class WakeWordEngine:
    def __init__(self, config):
        self.config = config
        self.access_key = os.getenv("PICOVOICE_ACCESS_KEY", config.get("access_key"))
        self.keywords = config.get("keywords", ["jarvis"])
        self.porcupine = None
        self._initialize()

    def _initialize(self):
        try:
            self.porcupine = pvporcupine.create(
                access_key=self.access_key,
                keywords=self.keywords
            )
        except Exception as e:
            print(f"Error initializing Porcupine: {e}")
            self.porcupine = None

    def process(self, pcm):
        """
        Process audio data (PCM) and return True if wake word is detected.
        pcm: list of integers or similar format expected by Porcupine
        """
        if not self.porcupine:
            return False

        try:
            keyword_index = self.porcupine.process(pcm)
            if keyword_index >= 0:
                return True
        except Exception as e:
            print(f"Error processing audio for wake word: {e}")

        return False

    def get_frame_length(self):
        if self.porcupine:
            return self.porcupine.frame_length
        return 512 # Default fallback

    def close(self):
        if self.porcupine:
            self.porcupine.delete()
