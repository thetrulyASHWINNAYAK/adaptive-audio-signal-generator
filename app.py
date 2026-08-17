import streamlit as st
import numpy as np
import io
import wave

st.set_page_config(
    page_title="Birthday Wishes",
    page_icon="Birthday",
    layout="centered"
)

st.title("Birthday Wishes")
st.write("Create a special birthday wish with music.")

st.divider()

name = st.text_input(
    "Birthday person's name",
    placeholder="Enter name"
)

sender = st.text_input(
    "Your name",
    placeholder="Enter your name"
)

if "generated" not in st.session_state:
    st.session_state.generated = False

if st.button("Generate Birthday Wish", use_container_width=True):

    if name.strip() == "":
        st.warning("Please enter the birthday person's name.")
    else:
        st.session_state.generated = True
        st.session_state.name = name
        st.session_state.sender = sender if sender.strip() else "Your Friend"


if st.session_state.generated:

    birthday_name = st.session_state.name
    sender_name = st.session_state.sender

    st.balloons()

    st.divider()

    st.header("Happy Birthday, " + birthday_name + "!")

    st.write(
        "Wishing you a wonderful birthday filled with "
        "happiness, success and beautiful memories!"
    )

    st.write("Best wishes from " + sender_name)

    st.divider()

    st.header("Birthday Music")

    music_style = st.selectbox(
        "Choose a music style",
        [
            "Piano",
            "Theater",
            "Jazz",
            "Celebration",
            "Classic"
        ]
    )

    st.write("Selected style:", music_style)

    sample_rate = 44100

    notes = [
        262, 262, 294, 262, 349, 330,
        262, 262, 294, 262, 392, 349,
        262, 262, 523, 440, 349, 330,
        294, 466, 466, 440, 349, 392, 349
    ]

    def make_note(frequency, duration, style):

        t = np.linspace(
            0,
            duration,
            int(sample_rate * duration),
            endpoint=False
        )

        if style == "Piano":
            sound = (
                np.sin(2 * np.pi * frequency * t)
                + 0.35 * np.sin(2 * np.pi * frequency * 2 * t)
                + 0.15 * np.sin(2 * np.pi * frequency * 3 * t)
            )

            envelope = np.exp(-3 * t)

        elif style == "Theater":
            sound = (
                np.sin(2 * np.pi * frequency * t)
                + 0.30 * np.sin(2 * np.pi * frequency * 2 * t)
                + 0.20 * np.sin(2 * np.pi * frequency * 3 * t)
            )

            vibrato = 2 * np.sin(2 * np.pi * 5 * t)

            sound += 0.15 * np.sin(
                2 * np.pi * (frequency + vibrato) * t
            )

            envelope = np.ones(len(t))

        elif style == "Jazz":
            vibrato = 3 * np.sin(2 * np.pi * 4 * t)

            sound = (
                np.sin(
                    2 * np.pi * (frequency + vibrato) * t
                )
                + 0.40 * np.sin(2 * np.pi * frequency * 2 * t)
                + 0.20 * np.sin(2 * np.pi * frequency * 3 * t)
            )

            envelope = np.ones(len(t))

        elif style == "Celebration":
            sound = (
                np.sin(2 * np.pi * frequency * t)
                + 0.50 * np.sin(2 * np.pi * frequency * 2 * t)
                + 0.25 * np.sin(2 * np.pi * frequency * 3 * t)
            )

            envelope = np.ones(len(t))

        else:
            sound = (
                np.sin(2 * np.pi * frequency * t)
                + 0.20 * np.sin(2 * np.pi * frequency * 2 * t)
            )

            envelope = np.ones(len(t))

        sound = sound * envelope

        return sound

    def generate_music(style):

        complete_audio = np.array([], dtype=np.float32)

        for frequency in notes:

            note = make_note(
                frequency,
                0.35,
                style
            )

            complete_audio = np.concatenate(
                (complete_audio, note)
            )

        return complete_audio

    def make_wav(audio):

        maximum = np.max(np.abs(audio))

        if maximum > 0:
            audio = audio / maximum

        audio = (
            audio * 32767
        ).astype(np.int16)

        data = io.BytesIO()

        with wave.open(data, "wb") as wav:

            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            wav.writeframes(audio.tobytes())

        data.seek(0)

        return data

    if st.button(
        "Play Birthday Music",
        use_container_width=True
    ):

        music = generate_music(music_style)

        wav_data = make_wav(music)

        st.audio(
            wav_data,
            format="audio/wav"
        )

        st.success(
            "Birthday music generated successfully!"
        )

        st.download_button(
            "Download Birthday Music",
            data=wav_data,
            file_name="birthday_music.wav",
            mime="audio/wav"
        )
