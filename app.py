import streamlit as st
import numpy as np
import io
import wave

# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="Birthday Wishes",
    page_icon="🎂",
    layout="centered"
)

st.title("🎂 Birthday Wishes")
st.write("Create a special birthday wish with personalized music! 🎉")

st.divider()

# =========================================================
# USER INPUT
# =========================================================

name = st.text_input(
    "🎂 Birthday person's name",
    placeholder="Enter name"
)

sender = st.text_input(
    "💌 Your name",
    placeholder="Enter your name"
)

# =========================================================
# GENERATE BUTTON
# =========================================================

if st.button("🎉 Generate Birthday Wish", use_container_width=True):

    if name.strip() == "":
        st.warning("Please enter the birthday person's name.")

    else:

        if sender.strip() == "":
            sender = "Your Friend"

        # Remember that wish was generated
        st.session_state["generated"] = True
        st.session_state["name"] = name
        st.session_state["sender"] = sender


# =========================================================
# SHOW MESSAGE ONLY AFTER GENERATE
# =========================================================

if st.session_state.get("generated", False):

    birthday_name = st.session_state["name"]
    sender_name = st.session_state["sender"]

    st.balloons()

    st.divider()

    st.markdown(
        f"""
        # 🎂 Happy Birthday, {birthday_name}! 🎉

        ### 🥳 Wishing you a wonderful birthday!

        May your special day be filled with:

        ✨ Happiness  
        ❤️ Love  
        🎁 Beautiful memories  
        🌟 Success  
        😊 Lots of smiles  

        **Have an amazing year ahead!**

        ### 💌 Best wishes from {sender_name} ❤️
        """
    )

    # =====================================================
    # BIRTHDAY MUSIC
    # =====================================================

    st.divider()

    st.header("🎵 Birthday Music")

    st.write(
        "Choose a musical style and play your birthday tune."
    )

    music_style = st.selectbox(
        "🎼 Choose Music Style",
        [
            "🎹 Piano",
            "🎭 Theater",
            "🎷 Jazz",
            "🎺 Celebration",
            "🎼 Classic"
        ]
    )

    # =====================================================
    # NOTES
    # =====================================================

    SAMPLE_RATE = 44100

    # Happy Birthday style melody
    base_notes = [
        262, 262, 294, 262, 349, 330,
        262, 262, 294, 262, 392, 349,
        262, 262, 523, 440, 349, 330, 294,
        466, 466, 440, 349, 392, 349
    ]

    # =====================================================
    # MUSIC GENERATOR
    # =====================================================

    def generate_music(style):

        audio = np.array([], dtype=np.float32)

        for i, frequency in enumerate(base_notes):

            duration = 0.35

            t = np.linspace(
                0,
                duration,
                int(SAMPLE_RATE * duration),
                endpoint=False
            )

            # ---------------------------------------------
            # PIANO
            # ---------------------------------------------

            if style == "🎹 Piano":

                tone = (
                    0.50 * np.sin(2 * np.pi * frequency * t)
                    + 0.20 * np.sin(2 * np.pi * frequency * 2 * t)
                    + 0.10 * np.sin(2 * np.pi * frequency * 3 * t)
                )

            # ---------------------------------------------
            # THEATER
            # ---------------------------------------------

            elif style == "🎭 Theater":

                tone = (
                    0.45 * np.sin(2 * np.pi * frequency * t)
                    + 0.25 * np.sin(2 * np.pi * frequency * 2 * t)
                    + 0.15 * np.sin(2 * np.pi * frequency * 4 * t)
                )

                # gentle vibrato
                vibrato = 3 * np.sin(
                    2 * np.pi * 5 * t
                )

                tone += 0.08 * np.sin(
                    2 * np.pi * (frequency + vibrato) * t
                )

            # ---------------------------------------------
            # JAZZ
            # ---------------------------------------------

            elif style == "🎷 Jazz":

                tone = (
                    0.40 * np.sin(2 * np.pi * frequency * t)
                    + 0.25 * np.sin(2 * np.pi * frequency * 3 * t)
                    + 0.15 * np.sin(2 * np.pi * frequency * 5 * t)
                )

                # slight pitch movement
                pitch = frequency * (
                    1 + 0.01 * np.sin(2 * np.pi * 4 * t)
                )

                tone += 0.08 * np.sin(
                    2 * np.pi * pitch * t
                )

            # ---------------------------------------------
            # CELEBRATION
            # ---------------------------------------------

            elif style == "🎺 Celebration":

                tone = (
                    0.55 * np.sin(2 * np.pi * frequency * t)
                    + 0.30 * np.sin(2 * np.pi * frequency * 2 * t)
                    + 0.20 * np.sin(2 * np.pi * frequency * 3 * t)
                )

            # ---------------------------------------------
            # CLASSIC
            # ---------------------------------------------

            else:

                tone = (
                    0.50 * np.sin(2 * np.pi * frequency * t)
                    + 0.15 * np.sin(2 * np.pi * frequency * 2 * t)
                )

            # ---------------------------------------------
            # FADE IN / FADE OUT
            # ---------------------------------------------

            fade = min(
                len(tone) // 20,
                500
            )

            tone[:fade] *= np.linspace(
                0,
                1,
                fade
            )

            tone[-fade:] *= np.linspace(
                1,
                0,
                fade
            )

            audio = np.concatenate(
                (audio, tone)
            )

        return audio

    # =====================================================
    # WAV CONVERSION
    # =====================================================

    def convert_to_wav(audio):

        peak = np.max(
            np.abs(audio)
        )

        if peak > 0:
            audio = audio / peak

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

    # =====================================================
    # PLAY BUTTON
    # =====================================================

    if st.button(
        f"▶️ Play {music_style}",
        use_container_width=True
    ):

        music = generate_music(
            music_style
        )

        wav_file = convert_to_wav(
            music
        )

        st.audio(
            wav_file,
            format="audio/wav"
        )

        st.success(
            f"🎵 Playing Happy Birthday — {music_style}"
        )

        st.download_button(
            "⬇️ Download This Tune",
            data=wav_file,
            file_name="birthday_music.wav",
            mime="audio/wav"
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🎂 Birthday Wishes App | Developed by Ashwin Nayak"
)
