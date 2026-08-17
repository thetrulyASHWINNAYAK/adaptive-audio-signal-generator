import streamlit as st
import numpy as np
import io
import wave

st.set_page_config(
    page_title="Birthday Wishes",
    page_icon="🎂",
    layout="centered"
)

st.title("🎂 Birthday Wishes")
st.write("Create a personalized birthday wish with a birthday tune! 🎉")

st.divider()

name = st.text_input(
    "Enter the birthday person's name:",
    placeholder="Example: Piyush"
)

sender = st.text_input(
    "Your name:",
    placeholder="Example: Ashwin"
)

if st.button("🎉 Generate Birthday Wish"):

    if name.strip() == "":
        st.warning("Please enter the birthday person's name.")

    else:
        if sender.strip() == "":
            sender = "Your Friend"

        st.balloons()

        st.markdown(
            f"""
            ## 🎂 Happy Birthday, {name}! 🎉

            ### 🥳 Wishing you a wonderful birthday!

            May your day be filled with happiness, laughter,
            success and many beautiful memories.

            🎁 Have an amazing year ahead!

            **Best wishes from {sender} ❤️**
            """
        )

st.divider()

st.subheader("🎵 Birthday Tune")

SAMPLE_RATE = 44100

notes = [
    262, 262, 294, 262, 349, 330,
    262, 262, 294, 262, 392, 349,
    262, 262, 523, 440, 349, 330, 294,
    466, 466, 440, 349, 392, 349
]

def generate_tune(notes, duration=0.35):

    audio = np.array([], dtype=np.float32)

    for frequency in notes:

        t = np.linspace(
            0,
            duration,
            int(SAMPLE_RATE * duration),
            endpoint=False
        )

        tone = 0.5 * np.sin(
            2 * np.pi * frequency * t
        )

        fade = min(len(tone) // 20, 500)

        tone[:fade] *= np.linspace(0, 1, fade)
        tone[-fade:] *= np.linspace(1, 0, fade)

        audio = np.concatenate(
            (audio, tone)
        )

    return audio


def convert_to_wav(audio):

    audio = audio / max(
        1,
        np.max(np.abs(audio))
    )

    audio = (
        audio * 32767
    ).astype(np.int16)

    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as wav:

        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)

        wav.writeframes(
            audio.tobytes()
        )

    buffer.seek(0)

    return buffer


birthday_audio = generate_tune(notes)

wav_file = convert_to_wav(birthday_audio)

st.audio(
    wav_file,
    format="audio/wav"
)

st.download_button(
    "⬇️ Download Birthday Tune",
    data=wav_file,
    file_name="birthday_tune.wav",
    mime="audio/wav"
)

st.divider()

st.caption(
    "🎂 Birthday Wishes App | Developed by Ashwin Nayak"
)
