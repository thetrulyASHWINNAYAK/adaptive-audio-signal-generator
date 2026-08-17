import io
import wave
import numpy as np

SAMPLE_RATE = 44100

duration = 2
frequency = 440

t = np.linspace(
    0,
    duration,
    int(SAMPLE_RATE * duration),
    endpoint=False
)

audio = 0.5 * np.sin(
    2 * np.pi * frequency * t
)

audio = (audio * 32767).astype(np.int16)

buffer = io.BytesIO()

with wave.open(buffer, "wb") as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(SAMPLE_RATE)
    wav.writeframes(audio.tobytes())

buffer.seek(0)

st.subheader("🔊 Audio Test — 440 Hz")

st.audio(
    buffer,
    format="audio/wav"
)
