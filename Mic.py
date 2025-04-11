import sounddevice as sd
import numpy as np
import scipy.io.wavfile
import subprocess
import os

# Full paths (replace 'victor' if your username is different)
WAV_FILENAME = "/home/victor/Desktop/temp.wav"
TXT_FILENAME = WAV_FILENAME + ".txt"

WHISPER_CLI = "/home/victor/Desktop/Tars/modules/whisper[git]/bin/whisper-cli"
MODEL_PATH = "/home/victor/Desktop/Tars/modules/whisper[git]/whisper.cpp/models/ggml-tiny.bin"

# Recording settings
DURATION = 4  # seconds
SAMPLERATE = 16000

def record_audio():
    print("[Listening...]")
    audio = sd.rec(int(DURATION * SAMPLERATE), samplerate=SAMPLERATE, channels=1, dtype='int16')
    sd.wait()
    scipy.io.wavfile.write(WAV_FILENAME, SAMPLERATE, audio)

def transcribe_with_whisper_cpp():
    subprocess.run([
        WHISPER_CLI,
        "-m", MODEL_PATH,
        "-l", "ro",
        "-f", WAV_FILENAME,
        "-otxt"
    ], capture_output=True, text=True)

    if os.path.exists(TXT_FILENAME):
        with open(TXT_FILENAME, "r") as f:
            text = f.read().strip()
        print("[You said]:", text)
        # Optional: clean up files
        os.remove(WAV_FILENAME)
        os.remove(TXT_FILENAME)
    else:
        print("[Error] Transcription failed.")

# Run once
record_audio()
transcribe_with_whisper_cpp()
