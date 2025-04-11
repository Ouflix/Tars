import whisper
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile

model = whisper.load_model("base")  # You can also try "tiny" for faster results
samplerate = 16000
duration = 5  # seconds per chunk
channels = 1

print("Listening. Press Ctrl+C to stop.")

def record_and_transcribe():
    while True:
        print("\n[Listening...]")
        audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=channels, dtype="int16")
        sd.wait()
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as f:
            scipy.io.wavfile.write(f.name, samplerate, audio)
            result = model.transcribe(f.name)
            print("[You said]:", result["text"])

try:
    record_and_transcribe()
except KeyboardInterrupt:
    print("\nStopped.")
