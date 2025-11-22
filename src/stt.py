import os
try:
    import whisper
except ImportError:
    whisper = None

# Note: The PRD mentions whisper.cpp.
# For this python implementation, we can use the `whisper` python package
# or a wrapper around whisper.cpp like `pywhispercpp`.
# This is a placeholder for the STT engine.

class STTEngine:
    def __init__(self, config):
        self.config = config
        self.model_name = config.get("model", "tiny")
        self.model = None
        self._load_model()

    def _load_model(self):
        if whisper:
            print(f"Loading Whisper model: {self.model_name}...")
            # In a real scenario with whisper.cpp, we would load the ggml model
            try:
                self.model = whisper.load_model(self.model_name)
                print("Whisper model loaded.")
            except Exception as e:
                print(f"Failed to load Whisper model: {e}")
        else:
            print("Whisper module not found. STT will be disabled.")

    def transcribe(self, audio_file):
        """
        Transcribe the given audio file to text.
        """
        if not self.model:
            return ""

        print(f"Transcribing {audio_file}...")
        try:
            result = self.model.transcribe(audio_file)
            text = result.get("text", "").strip()
            print(f"Transcription: {text}")
            return text
        except Exception as e:
            print(f"Error during transcription: {e}")
            return ""
