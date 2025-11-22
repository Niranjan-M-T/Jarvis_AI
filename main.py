import yaml
import time
import os
import sys

from src.wakeword import WakeWordEngine
from src.recorder import AudioRecorder
from src.stt import STTEngine
from src.llm import LLMEngine
from src.executor import CommandExecutor
from src.tts import TTSEngine

def load_config(path="config/config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def main():
    print("Initializing WhisperLite Voice Assistant...")
    config = load_config()

    # Initialize components
    wakeword_engine = WakeWordEngine(config["wake_word"])
    recorder = AudioRecorder(config["recording"])
    stt_engine = STTEngine(config["stt"])
    llm_engine = LLMEngine(config["llm"])
    executor = CommandExecutor(config["system"])
    tts_engine = TTSEngine(config["tts"])

    print("Components initialized. Waiting for wake word 'Jarvis'...")

    try:
        if wakeword_engine.porcupine is None:
             print("Wake word engine not initialized correctly (likely missing access key).")
             # Fallback for testing: Wait for enter key
             while True:
                input("Press Enter to trigger 'Jarvis' (Simulated Wake Word)...")
                process_cycle(recorder, stt_engine, llm_engine, executor, tts_engine)

        else:
            # Main Loop with Wake Word
            # We open the stream, but when wake word is detected, we must close it (or stop it)
            # before recording the command, because the recorder module uses a separate stream/call.

            while True:
                # Re-open stream for wake word listening
                with recorder.get_stream(wakeword_engine.get_frame_length(), callback=None) as stream:
                     print("Listening for wake word...")
                     while True:
                        data, overflow = stream.read(wakeword_engine.get_frame_length())
                        pcm = data[:, 0]

                        if wakeword_engine.process(pcm):
                            print("Wake word detected!")
                            break # Break inner loop to close stream and proceed to process_cycle

                # Stream is closed here
                process_cycle(recorder, stt_engine, llm_engine, executor, tts_engine)

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        wakeword_engine.close()

def process_cycle(recorder, stt, llm, executor, tts):
    # 1. Record Audio
    audio_data = recorder.record()
    wav_path = recorder.save_wav(audio_data)

    # 2. STT
    text = stt.transcribe(wav_path)
    if not text:
        return

    # 3. LLM
    command_data = llm.process_command(text)

    # 4. Execute
    result = executor.execute(command_data)

    # 5. Respond
    if result:
        tts.speak(str(result))

if __name__ == "__main__":
    main()
