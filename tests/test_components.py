import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Mock dependencies that might not be installed or require hardware
sys.modules['pvporcupine'] = MagicMock()
sys.modules['sounddevice'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['pyttsx3'] = MagicMock()
sys.modules['whisper'] = MagicMock()
sys.modules['llama_cpp'] = MagicMock()

from src.wakeword import WakeWordEngine
from src.recorder import AudioRecorder
from src.stt import STTEngine
from src.llm import LLMEngine
from src.executor import CommandExecutor
from src.tts import TTSEngine

class TestComponents(unittest.TestCase):

    def test_wakeword_init(self):
        config = {"keywords": ["jarvis"], "access_key": "test"}
        engine = WakeWordEngine(config)
        self.assertIsNotNone(engine)

    def test_recorder_init(self):
        config = {"sample_rate": 16000}
        recorder = AudioRecorder(config)
        self.assertEqual(recorder.sample_rate, 16000)

    def test_executor_open_app(self):
        config = {}
        executor = CommandExecutor(config)
        # Test command structure
        result = executor.execute({"intent": "open_application", "application": "Notepad"})
        # Since we are on linux (likely) and platform.system() would return Linux, or we can mock it
        # But the code handles non-windows gracefully
        self.assertTrue("Opening" in result or "supported on Windows" in result)

    def test_llm_mock_processing(self):
        config = {"model_path": "dummy"}
        llm = LLMEngine(config)
        # Force llm to be None to test fallback
        llm.llm = None
        result = llm.process_command("Open chrome")
        self.assertEqual(result.get("intent"), "open_application")

if __name__ == '__main__':
    unittest.main()
