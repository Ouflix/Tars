import whisper
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile
import time

# Load model (use "tiny" for speed)
model = whisper.load_model("tiny")

samplerate = 16000
channels = 1
threshold = 300  # Silence threshold (lower = more sensitive)
silence_limit = 1.0  # seconds of silence before stop
chunk_duration = 0.2  # duration of each read in seconds

print("Speak to start recording...")

def rms(audio):
    return np.sqrt(np.mean(np.square(audio)))

def record_until_silence():
    audio_data = []
    silence_start = None

    stream = sd.InputStream(samplerate=samplerate, channels=channels, dtype='int16')
    stream.start()

    try:
        while True:
            chunk, _ = stream.read(int(samplerate * chunk_duration))
            audio_data.append(chunk)

            level = rms(chunk)
            if level < threshold:
                if silence_start is None:
                    silence_start = time.time()
                elif time.time() - silence_start > silence_limit:
                    break
            else:
                silence_start = None
    finally:
        stream.stop()

    return np.concatenate(audio_data, axis=0)

while True:
    print("\n[Listening for voice...]")
    audio = record_until_silence()
    print("[Transcribing...]")

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as f:
        scipy.io.wavfile.write(f.name, samplerate, audio)
        result = model.transcribe(f.name, language="en")
        print("[You said]:", result["text"])
