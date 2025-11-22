# 📄 Product Requirements Document (PRD)

## Project Name: **WhisperLite Voice Assistant**

**Version**: 1.0
**Target Environment**: Windows 10/11
**Primary Goal**: Fully local, voice-activated, command-executing assistant that operates via CLI, triggered only by a wake word, optimized for **8GB RAM systems with RTX 3050 GPU**.

---

## 🔹1. Problem Statement

Users want a **lightweight, private, local AI assistant** that can be activated by voice, understand natural language, and perform system actions on Windows—without requiring cloud services or heavy RAM usage.

---

## 🔹2. Product Vision

Create a **fully offline, resource-efficient, wake-word-based voice assistant** that:

✔ Runs locally — no internet required
✔ Works only after detecting a wake word
✔ Supports voice commands for Windows automation
✔ Uses lightweight ASR + LLM models
✔ Works in a simple CLI environment

---

## 🔹3. Core Objectives

| Feature                   | Requirement                                     |
| ------------------------- | ----------------------------------------------- |
| Wake-Word Detection       | Ultra-low CPU usage, always listening           |
| Speech-to-Text            | Whisper.cpp (Tiny/Base) — Runs within 800MB RAM |
| Lightweight LLM           | Runs locally under 1GB RAM                      |
| Executes Windows commands | Via Python subprocess, psutil, os               |
| Pure CLI interface        | No GUI, text only                               |
| Optional Voice Output     | Piper TTS or Windows SAPI                       |
| Zero Cloud Dependency     | All models local, no API calls                  |

---

## 🔹4. Use Case Examples

| Voice Command                                     | Example System Action               |
| ------------------------------------------------- | ----------------------------------- |
| "Nova, open Chrome"                               | Launches Chrome                     |
| "Nova, start OBS"                                 | Launches OBS Studio                 |
| "Nova, create a folder named Projects on desktop" | Makes directory                     |
| "Nova, shutdown the system"                       | System shutdown (with confirmation) |
| "Nova, what's my CPU usage?"                      | Reads and reports system stats      |
| "Nova, launch my trading bot"                     | Executes a Python script            |

---

## 🔹5. System Architecture

```
 ┌────────────────────────┐
 │ Wake Word Engine       │   (Porcupine / OpenWakeWord)
 └─────────┬──────────────┘
           │
   Wake word detected
           │
 ┌─────────▼──────────────┐
 │ Audio Recorder (WAV)   │  (sounddevice / pyaudio)
 └─────────┬──────────────┘
           │
 ┌─────────▼──────────────┐
 │ Whisper.cpp STT        │  (Tiny/Base models)
 └─────────┬──────────────┘
           │
 ┌─────────▼──────────────┐
 │ Lightweight LLM        │  (Local inference)
 │ Gemma 2B / Phi-3 Mini  │
 └─────────┬──────────────┘
           │
 ┌─────────▼──────────────┐
 │ Intent Parser & Router │ (JSON command mapping)
 └─────────┬──────────────┘
           │
 ┌─────────▼──────────────┐
 │ Windows Command Layer  │ (Python subprocess/psutil/os)
 └─────────┬──────────────┘
           │
 ┌─────────▼──────────────┐
 │ CLI Output / TTS       │
 └────────────────────────┘
```

---

## 🔹6. Technical Stack

### 📌 **Wake Word Detection – Lightweight Options**

| Module                | RAM Usage | Notes                                       |
| --------------------- | --------- | ------------------------------------------- |
| Picovoice Porcupine   | <50MB     | Most reliable, commercial license available |
| OpenWakeWord          | ~90MB     | Open-source, CPU-only, free                 |
| Vosk Keyword Spotting | ~140MB    | Less accurate, fallback option              |

**Best Choice**: **Picovoice Porcupine** (.ppn custom wake file)

---

### 📌 **Speech-to-Text (ASR) – Whisper.cpp Models**

| Model     | Size  | RAM Usage | Accuracy | Ideal Use      |
| --------- | ----- | --------- | -------- | -------------- |
| ggml-tiny | 77MB  | ~350MB    | Basic    | Quick commands |
| ggml-base | 142MB | ~550MB    | Better   | Natural speech |

**Recommended**: ggml-tiny.en → faster, fits low-RAM system easily.

---

### 📌 **Lightweight LLM Model Options (Fit Below 1GB RAM)**

| Model              | RAM (Q4 quantized) | Type       | Best For                        |
| ------------------ | ------------------ | ---------- | ------------------------------- |
| Gemma 2B Q4        | ~500MB             | General    | Good accuracy + speed           |
| Phi-3 Mini 3.8B Q4 | ~950MB             | Reasoning  | Great system task understanding |
| LLaMA 3.2 1B Q4    | ~350MB             | Very small | Basic automation only           |

**Best Pick for Balance:** 🏆 **Phi-3 Mini (Q4_K_M)**
Good language understanding | Fits in RAM | Good for command classification

---

### 📌 **Command Execution Layer (Windows)**

| Feature                 | Library                            |
| ----------------------- | ---------------------------------- |
| Launch apps             | `os.startfile`, `subprocess.Popen` |
| System commands         | `PowerShell`, `subprocess`         |
| Monitor CPU/RAM         | `psutil`                           |
| Automate mouse/keyboard | `pyautogui`                        |
| Web search              | `webbrowser`                       |
| File handling           | `shutil`, `os`, `pathlib`          |

---

### 📌 **Voice Output (Optional)**

| Engine    | RAM Usage | Notes                          |
| --------- | --------- | ------------------------------ |
| Piper TTS | ~120MB    | Local, natural sounding        |
| pyttsx3   | <50MB     | Uses Windows native SAPI voice |
| Coqui TTS | ~350MB    | Highest voice quality, heavy   |

**Recommendation:** Use **pyttsx3 (Windows SAPI)** → lowest footprint, no GPU needed.

---

## 🔹7. Main System Flow

### 🔁 Loop-based state machine

1️⃣ **Idle Listening**
→ Low-power wake-word detection

2️⃣ **Wake Activation**
→ Print “Listening…”

3️⃣ **Audio Recording (5–10 sec max)**
→ Save as `command.wav`

4️⃣ **STT Processing (Whisper.cpp)**
→ Convert audio to text

5️⃣ **Send text into LLM**
→ Interpret into structured command
→ JSON Output Example:

```json
{
  "intent": "open_application",
  "application": "Google Chrome"
}
```

6️⃣ **Execute Command**
→ Use Python automation
→ Validate with security filter
→ Run system action

7️⃣ **Respond (Text/TTS)**
→ Speak/print result

8️⃣ Return to **Idle Mode**

---

## 🔹8. Security Design

| Command Type | Security Level       | Example                        |
| ------------ | -------------------- | ------------------------------ |
| Low-Risk     | Auto-execute         | open chrome, play songs        |
| Medium       | Ask for confirmation | run scripts, delete files      |
| High-Risk    | Disabled by default  | format drive, disable firewall |

**Prevention methods:**
✔ Allowed commands whitelist
✔ Path restrictions (only C:\Users\Scripts)
✔ JSON-structured LLM output to avoid arbitrary code

---

## 🔹9. Performance Targets

| Metric                 | Goal      |
| ---------------------- | --------- |
| Idle RAM               | <200MB    |
| Active RAM (STT + LLM) | <1.5GB    |
| Wake Word Latency      | <200ms    |
| Transcription Time     | <1.5s     |
| Command Execution      | Immediate |
| Voice Response         | <1s       |

---

## 🔹10. Deliverables Required for Final Product

✔ CLI-based voice assistant (Python executable)
✔ Wake-word listener active in background
✔ Whisper ASR integration
✔ Local LLM with intent classification
✔ Command execution framework
✔ Config file (YAML/JSON) for:

* Wake word path
* Model paths
* Allowed commands
* Logging settings

✔ Documentation:

* Installation
* Setup
* Add custom commands
* Extend with plugins

✔ Optionally packaged via PyInstaller → one executable

---

## 🔹11. Future Expansion (Not Required Now)

🚀 GUI version (Electron/Tkinter)
🚀 Offline chatbot mode
🚀 Custom voice wake word generator
🚀 Browser automation (control Chrome tabs)
🚀 Plugin system for AI tools

---

## 🏁 Final Recommendation Summary

| Component           | Best Choice                |
| ------------------- | -------------------------- |
| Wake Word           | Porcupine                  |
| STT                 | Whisper.cpp Tiny           |
| LLM (RAM-optimized) | Phi-3 Mini (Q4)            |
| Command Execution   | Python subprocess / psutil |
| Voice Output (Opt.) | Windows SAPI (pyttsx3)     |
| Packaging           | PyInstaller                |



Let me know 🚀
