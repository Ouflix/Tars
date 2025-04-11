import subprocess
import tempfile
import sounddevice as sd
import numpy as np
import scipy.io.wavfile
import os

WAV_FILENAME = "temp.wav"
WHISPER_CPP_PATH = "/home/pi/whisper.cpp"  # Change to your actual path

def record_audio(duration=4, samplerate=16000):
    print("[Listening...]")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    scipy.io.wavfile.write(WAV_FILENAME, samplerate, audio)

def transcribe_with_whisper_cpp(wav_file):
    result = subprocess.run([
        f"{WHISPER_CPP_PATH}/main",
        "-m", f"{WHISPER_CPP_PATH}/ggml-tiny.bin",
        "-l", "ro",
        "-f", wav_file,
        "-otxt"
    ], capture_output=True, text=True)

    output_txt_file = wav_file.replace(".wav", ".txt")
    if os.path.exists(output_txt_file):
        with open(output_txt_file, "r") as f:
            text = f.read().strip()
        return text
    else:
        return "[Error] Transcription failed."

# Main loop
while True:
    record_audio(duration=4)
    result = transcribe_with_whisper_cpp(WAV_FILENAME)
    print("[You said]:", result)
