import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Mock dependencies
sys.modules['pvporcupine'] = MagicMock()
sys.modules['sounddevice'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['pyttsx3'] = MagicMock()
sys.modules['whisper'] = MagicMock()
sys.modules['llama_cpp'] = MagicMock()

# Mock psutil and webbrowser for executor tests
mock_psutil = MagicMock()
sys.modules['psutil'] = mock_psutil
mock_webbrowser = MagicMock()
sys.modules['webbrowser'] = mock_webbrowser

from src.executor import CommandExecutor
# We need to import after mocking
# But src.executor imports psutil at top level, so the mock above in sys.modules should work.

class TestExecutor(unittest.TestCase):

    def setUp(self):
        self.config = {"allowed_commands": ["system_stats", "system_control", "file_operation", "search_web"]}
        self.executor = CommandExecutor(self.config)

    def test_get_system_stats(self):
        mock_psutil.cpu_percent.return_value = 15.5
        mock_psutil.virtual_memory.return_value.percent = 45.0

        result = self.executor.execute({"intent": "system_stats"})
        self.assertIn("15.5", result)
        self.assertIn("45.0", result)

    def test_search_web(self):
        self.executor.execute({"intent": "search_web", "query": "python"})
        mock_webbrowser.open.assert_called_with("https://www.google.com/search?q=python")

    def test_file_create_folder(self):
        with patch('pathlib.Path.mkdir') as mock_mkdir:
             result = self.executor.execute({
                 "intent": "file_operation",
                 "operation": "create_folder",
                 "name": "TestFolder",
                 "path": "" # Default to desktop
             })
             self.assertIn("Created folder TestFolder", result)
             mock_mkdir.assert_called()

    def test_system_control_shutdown(self):
        # We commented out the actual os.system call in implementation for safety,
        # so we just check the return message.
        with patch('platform.system', return_value="Windows"):
            result = self.executor.execute({"intent": "system_control", "action": "shutdown"})
            self.assertIn("Shutting down", result)

if __name__ == '__main__':
    unittest.main()
