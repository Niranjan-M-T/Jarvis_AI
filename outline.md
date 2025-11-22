# WhisperLite Project Outline

This document provides a detailed overview of the files in the WhisperLite voice assistant project and their specific functionalities.

## Root Directory

### `main.py`
- **Purpose**: The entry point of the application.
- **Functionality**:
  - Initializes all components (Wake Word, Recorder, STT, LLM, Executor, TTS).
  - Implements the main event loop:
    1. Listens for the wake word ("Jarvis").
    2. Records audio upon detection.
    3. Transcribes audio to text.
    4. Processes text into a structured command via LLM.
    5. Executes the command.
    6. Provides voice feedback.
  - Handles resource management (opening/closing audio streams).

### `requirements.txt`
- **Purpose**: Lists Python dependencies.
- **Content**: `pvporcupine`, `sounddevice`, `numpy`, `pyttsx3`, `psutil`, `pyyaml`, `openai-whisper`, `requests`, `llama-cpp-python`.

### `README.md`
- **Purpose**: Product Requirements Document (PRD) and project overview.
- **Content**: Problem statement, architecture, technical stack, and installation goals.

### `.gitignore`
- **Purpose**: Specifies intentionally untracked files to ignore.
- **Content**: `__pycache__`, compiled files, models, and environment variables.

---

## Configuration (`config/`)

### `config/config.yaml`
- **Purpose**: Centralized configuration file.
- **Functionality**:
  - Defines wake word settings (engine, keyword "jarvis").
  - Configures model paths for STT and LLM.
  - Sets recording parameters (sample rate, duration).
  - Defines TTS settings (rate, volume).
  - Lists allowed commands for the executor.

---

## Source Code (`src/`)

### `src/wakeword.py`
- **Purpose**: Wake word detection engine.
- **Functionality**:
  - Wraps `pvporcupine` library.
  - Initializes with the access key and keyword.
  - Processes audio frames (PCM data) to detect the keyword "Jarvis".

### `src/recorder.py`
- **Purpose**: Audio handling.
- **Functionality**:
  - Wraps `sounddevice`.
  - Records audio for a fixed duration or until silence (simple duration based currently).
  - Saves recorded audio to WAV files (`command.wav`).
  - Provides an audio stream for the wake word engine.

### `src/stt.py`
- **Purpose**: Speech-to-Text (ASR).
- **Functionality**:
  - Wraps `openai-whisper` (or `whisper.cpp`).
  - Loads the specified Whisper model (e.g., "tiny").
  - Transcribes WAV files into text strings.

### `src/llm.py`
- **Purpose**: Language Model integration (Intent Parsing).
- **Functionality**:
  - Wraps `llama-cpp-python` for local inference.
  - Loads GGUF models (e.g., Phi-3 Mini).
  - Constructs a prompt to instruct the LLM to output JSON.
  - Parses the LLM's output to extract structured intents (e.g., `{"intent": "open_application", ...}`).

### `src/executor.py`
- **Purpose**: Command Execution Layer.
- **Functionality**:
  - Receives structured commands from the LLM.
  - **System Stats**: Returns CPU and RAM usage using `psutil`.
  - **System Control**: Performs shutdown and restart operations (Windows optimized).
  - **File Operations**: Creates folders and safely deletes files in user directories.
  - **Web Search**: Opens Google searches in the default browser.
  - **App Launching**: Opens applications via `os.startfile`.

### `src/tts.py`
- **Purpose**: Text-to-Speech response.
- **Functionality**:
  - Wraps `pyttsx3`.
  - Converts text responses from the executor into audible speech.
  - Configurable rate and volume.

---

## Tests (`tests/`)

### `tests/test_components.py`
- **Purpose**: Unit tests for initialization and basic flow.
- **Functionality**:
  - Mocks external dependencies (`pvporcupine`, `sounddevice`, `whisper`, etc.).
  - Verifies that components initialize correctly with the given config.
  - Tests fallback logic when models are missing.

### `tests/test_executor.py`
- **Purpose**: Dedicated tests for the Command Executor.
- **Functionality**:
  - Mocks `psutil`, `webbrowser`, and `os` functions.
  - Verifies that `system_stats` returns the expected format.
  - Verifies that `file_operations` call the correct path creation/deletion methods.
  - Checks security logic (e.g., preventing deletion outside safe directories).
