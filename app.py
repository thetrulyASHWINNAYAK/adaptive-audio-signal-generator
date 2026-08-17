import streamlit as st
import numpy as np
import io
import wave

# =========================================================
# PAGE SETTINGS
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
# INPUT
# =========================================================

name = st.text_input(
    "🎂 Birthday person's name",
    placeholder="Enter birthday person's name"
)

sender = st.text_input(
    "💌 Your name",
    placeholder="Enter your name"
)


# =========================================================
# SESSION STATE
# =========================================================

if "generated" not in st.session_state:
    st.session_state.generated = False


# =========================================================
# GENERATE BIRTHDAY WISH
# =========================================================

if st.button(
    "🎉 Generate Birthday Wish",
    use_container_width=True
):

    if name.strip() == "":

        st.warning(
            "Please enter the birthday person's name."
        )

    else:

        st.session_state.generated = True

        st.session_state.name = name

        if sender.strip() == "":
            st.session_state.sender = "Your Friend"
        else:
            st.session_state.sender = sender


# =========================================================
# SHOW MESSAGE AFTER GENERATE
# =========================================================

if st.session_state.generated:

    birthday_name = st.session_state.name
    sender_name = st.session_state.sender

    st.balloons()

    st.divider()

    st.header(
        "🎂 Happy Birthday, "
        + birthday_name
        + "! 🎉"
    )

    st.write(
        "🥳 Wishing you a wonderful birthday!"
    )

    st.write(
        "May your special day be filled with "
        "happiness, success, beautiful memories "
        "and lots of smiles. 😊"
    )

    st.write(
        "✨ Have an amazing year ahead!"
    )

    st.write(
        "💌 Best wishes from "
        + sender_name
        + " ❤️"
    )


    # =====================================================
    # BIRTHDAY MUSIC
    # =====================================================

    st.divider()

    st.header("🎵 Birthday Music")

    st.write(
        "Choose a musical style for your birthday tune."
    )


    # =====================================================
    # MUSIC STYLE
    # =====================================================

    music_style = st.selectbox(
        "🎼 Choose Music Style",
        [
            "🎹 Piano",
            "🎭 Theater",
            "🎷 Jazz",
            "🎺 Celebration",
            "🎼 Classic",
            "🎵 Custom Tune"
        ]
    )


    # =====================================================
    # CUSTOM TUNE
    # =====================================================

    custom_tune = ""

    if music_style == "🎵 Custom Tune":

        custom_tune = st.text_input(
            "🎵 Enter frequencies in Hz",
            value="262,294,330,392,440,392,330,294,262",
            help="Enter frequencies separated by commas."
        )

        st.info(
            "Example: 262,294,330,392,440"
        )

        st.write("### 🎼 Common Note Frequencies")

        st.write(
            """
            C4 = 262 Hz  
            D4 = 294 Hz  
            E4 = 330 Hz  
            F4 = 349 Hz  
            G4 = 392 Hz  
            A4 = 440 Hz  
            B4 = 494 Hz  
            C5 = 523 Hz
            """
        )


    # =====================================================
    # SAMPLE RATE
    # =====================================================

    SAMPLE_RATE = 44100


    # =====================================================
    # HAPPY BIRTHDAY NOTES
    # =====================================================

    birthday_notes = [

        262, 262, 294, 262,
        349, 330,

        262, 262, 294, 262,
        392, 349,

        262, 262, 523, 440,
        349, 330, 294,

        466, 466, 440, 349,
        392, 349

    ]


    # =====================================================
    # GENERATE ONE NOTE
    # =====================================================

    def make_note(
        frequency,
        duration,
        style
    ):

        t = np.linspace(
            0,
            duration,
            int(SAMPLE_RATE * duration),
            endpoint=False
        )


        # -------------------------------------------------
        # PIANO
        # -------------------------------------------------

        if style == "🎹 Piano":

            sound = (

                1.00
                * np.sin(
                    2 * np.pi
                    * frequency
                    * t
                )

                + 0.35
                * np.sin(
                    2 * np.pi
                    * frequency
                    * 2
                    * t
                )

                + 0.15
                * np.sin(
                    2 * np.pi
                    * frequency
                    * 3
                    * t
                )

            )

            envelope = np.exp(
                -3.5 * t
            )


        # -------------------------------------------------
        # THEATER
        # -------------------------------------------------

        elif style == "🎭 Theater":

            sound = (

                0.80
                * np.sin(
                    2 * np.pi
                    * frequency
                    * t
                )

                + 0.35
                * np.sin(
                    2 * np.pi
                    * frequency
                    * 2
                    * t
                )

                + 0.20
                * np.sin(
                    2 * np.pi
                    * frequency
                    * 3
                    * t
                )

            )

            vibrato = (
                4
                * np.sin(
                    2 * np.pi
                    * 5
                    * t
                )
            )

            sound += (

                0.15
                * np.sin(
                    2 * np.pi
                    * (
                        frequency
                        + vibrato
                    )
                    * t
                )

            )

            envelope = np.ones(
                len(t)
            )


        # -------------------------------------------------
        # JAZZ
        # -------------------------------------------------

        elif style == "🎷 Jazz":

            vibrato = (

                5
                * np.sin(
                    2 * np.pi
                    * 5
                    * t
                )

            )

            sound = (

                0.75
                * np.sin(
                    2 * np.pi
                    * (
                        frequency
                        + vibrato
                    )
                    * t
                )

                + 0.45
                * np.sin(
                    2 * np.pi
                    * frequency
                    * 2
                    * t
                )

                + 0.30
                * np.sin(
                    2 * np.pi
                    * frequency
                    * 3
                    * t
                )

                + 0.18
                * np.sin(
                    2 * np.pi
                    * frequency
                    * 4
                    * t
                )

            )

            # Jazz attack

            attack = int(
                0.03
                * SAMPLE_RATE
            )

            release = int(
                0.10
                * SAMPLE_RATE
            )

            envelope = np.ones(
                len(t)
            )

            envelope[
                :attack
            ] = np.linspace(
                0,
                1,
                attack
            )

            envelope[
                -release:
            ] = np.linspace(
                1,
                0,
                release
            )


        # -------------------------------------------------
        # CELEBRATION
        # -------------------------------------------------

        elif style == "🎺 Celebration":

            sound = (

                1.00
                * np.sin(
                    2 * np.pi
                    * frequency
                    * t
                )

                + 0.50
                * np.sin(
                    2 * np.pi
                    * frequency
                    * 2
                    * t
                )

                + 0.25
                * np.sin(
                    2 * np.pi
                    * frequency
                    * 3
                    * t
                )

            )

            envelope = np.ones(
                len(t)
            )


        # -------------------------------------------------
        # CLASSIC
        # -------------------------------------------------

        elif style == "🎼 Classic":

            sound = (

                1.00
                * np.sin(
                    2 * np.pi
                    * frequency
                    * t
                )

                + 0.20
                * np.sin(
                    2 * np.pi
                    * frequency
                    * 2
                    * t
                )

                + 0.10
                * np.sin(
                    2 * np.pi
                    * frequency
                    * 3
                    * t
                )

            )

            envelope = np.ones(
                len(t)
            )


        # -------------------------------------------------
        # CUSTOM TUNE
        # -------------------------------------------------

        else:

            sound = (

                1.00
                * np.sin(
                    2 * np.pi
                    * frequency
                    * t
                )

                + 0.25
                * np.sin(
                    2 * np.pi
                    * frequency
                    * 2
                    * t
                )

            )

            envelope = np.ones(
                len(t)
            )


        # =================================================
        # FADE IN / FADE OUT
        # =================================================

        fade_samples = min(
            int(0.02 * SAMPLE_RATE),
            len(sound) // 2
        )

        if fade_samples > 0:

            sound[
                :fade_samples
            ] *= np.linspace(
                0,
                1,
                fade_samples
            )

            sound[
                -fade_samples:
            ] *= np.linspace(
                1,
                0,
                fade_samples
            )


        return sound * envelope


    # =====================================================
    # GENERATE COMPLETE MUSIC
    # =====================================================

    def generate_music(style):

        # -------------------------------------------------
        # CUSTOM FREQUENCIES
        # -------------------------------------------------

        if style == "🎵 Custom Tune":

            try:

                frequencies = [

                    float(
                        value.strip()
                    )

                    for value
                    in custom_tune.split(",")

                    if value.strip()

                ]

            except ValueError:

                st.error(
                    "❌ Please enter only numbers "
                    "separated by commas."
                )

                return np.array(
                    [],
                    dtype=np.float32
                )


        # -------------------------------------------------
        # NORMAL BIRTHDAY TUNE
        # -------------------------------------------------

        else:

            frequencies = birthday_notes


        # -------------------------------------------------
        # CREATE AUDIO
        # -------------------------------------------------

        complete_audio = np.array(
            [],
            dtype=np.float32
        )


        for frequency in frequencies:

            # Ignore invalid frequencies

            if frequency <= 0:

                continue


            # Limit extremely high frequencies

            if frequency > 5000:

                st.warning(
                    "Some frequencies were above "
                    "5000 Hz and were ignored."
                )

                continue


            note = make_note(

                frequency,

                0.35,

                style

            )


            complete_audio = np.concatenate(

                (
                    complete_audio,
                    note
                )

            )


        return complete_audio


    # =====================================================
    # CONVERT TO WAV
    # =====================================================

    def convert_to_wav(audio):

        if len(audio) == 0:

            return None


        maximum = np.max(
            np.abs(audio)
        )


        if maximum > 0:

            audio = (
                audio / maximum
            )


        audio = (

            audio
            * 32767

        ).astype(
            np.int16
        )


        buffer = io.BytesIO()


        with wave.open(
            buffer,
            "wb"
        ) as wav:

            wav.setnchannels(1)

            wav.setsampwidth(2)

            wav.setframerate(
                SAMPLE_RATE
            )

            wav.writeframes(
                audio.tobytes()
            )


        buffer.seek(0)


        return buffer


    # =====================================================
    # PLAY MUSIC
    # =====================================================

    if st.button(
        "▶️ Play Birthday Music",
        use_container_width=True
    ):

        music = generate_music(
            music_style
        )


        wav_file = convert_to_wav(
            music
        )


        if wav_file is not None:

            st.audio(
                wav_file,
                format="audio/wav"
            )


            st.success(
                "🎵 Birthday music generated!"
            )


            st.download_button(

                "⬇️ Download This Tune",

                data=wav_file,

                file_name=(
                    "birthday_"
                    + music_style
                    .replace("🎹 ", "")
                    .replace("🎭 ", "")
                    .replace("🎷 ", "")
                    .replace("🎺 ", "")
                    .replace("🎼 ", "")
                    .replace("🎵 ", "")
                    .replace(" ", "_")
                    + ".wav"
                ),

                mime="audio/wav"

            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🎂 Birthday Wishes App | "
    "Python + Streamlit + NumPy"
)
