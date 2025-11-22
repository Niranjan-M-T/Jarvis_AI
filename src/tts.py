import pyttsx3

class TTSEngine:
    def __init__(self, config):
        self.config = config
        self.engine = pyttsx3.init()
        self._configure()

    def _configure(self):
        rate = self.config.get("rate", 150)
        volume = self.config.get("volume", 1.0)
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

    def speak(self, text):
        """
        Convert text to speech.
        """
        print(f"Speaking: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
