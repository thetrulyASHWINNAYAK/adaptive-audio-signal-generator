import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import wave

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Adaptive Audio Signal & Tune Generator",
    page_icon="🎵",
    layout="wide"
)

# ==========================================================
# TITLE
# ==========================================================

st.title("🎵 Adaptive Audio Signal & Tune Generator")

st.markdown("""
### Generate • Play • Visualize • Analyze

An Electronics & Telecommunication Engineering laboratory
project using Python, NumPy, Matplotlib and Streamlit.
""")

st.divider()

# ==========================================================
# CONSTANTS
# ==========================================================

SAMPLE_RATE = 44100


# ==========================================================
# AUDIO GENERATION FUNCTIONS
# ==========================================================

def generate_tone(frequency, duration=2, amplitude=0.5):

    samples = int(SAMPLE_RATE * duration)

    t = np.arange(samples) / SAMPLE_RATE

    signal = amplitude * np.sin(
        2 * np.pi * frequency * t
    )

    return signal


def generate_siren(
    low_frequency,
    high_frequency,
    duration=5,
    modulation_rate=1.2
):

    samples = int(SAMPLE_RATE * duration)

    t = np.arange(samples) / SAMPLE_RATE

    frequency = (
        (low_frequency + high_frequency) / 2
        +
        (high_frequency - low_frequency) / 2
        * np.sin(
            2 * np.pi * modulation_rate * t
        )
    )

    phase = (
        2 * np.pi
        * np.cumsum(frequency)
        / SAMPLE_RATE
    )

    signal = 0.5 * np.sin(phase)

    return signal


def generate_tune(notes, note_duration=0.35):

    complete_signal = []

    for frequency in notes:

        if frequency == 0:

            tone = np.zeros(
                int(SAMPLE_RATE * note_duration)
            )

        else:

            tone = generate_tone(
                frequency,
                note_duration,
                0.5
            )

        complete_signal.extend(tone)

    return np.array(complete_signal)


# ==========================================================
# MUSICAL NOTES
# ==========================================================

NOTES = {
    "C4": 261.63,
    "D4": 293.66,
    "E4": 329.63,
    "F4": 349.23,
    "G4": 392.00,
    "A4": 440.00,
    "B4": 493.88,
    "C5": 523.25
}


# ==========================================================
# PREDEFINED TUNES
# ==========================================================

happy_birthday = [
    262, 262, 294, 262, 349, 330,
    262, 262, 294, 262, 392, 349,
    262, 262, 523, 440, 349, 330, 294,
    466, 466, 440, 349, 392, 349
]

school_tune = [
    262, 294, 330, 349,
    392, 440, 494, 523,
    494, 440, 392, 349,
    330, 294, 262
]


# ==========================================================
# CONVERT SIGNAL TO WAV
# ==========================================================

def signal_to_wav(signal):

    max_value = np.max(np.abs(signal))

    if max_value > 0:
        signal = signal / max_value

    signal = (
        signal * 32767
    ).astype(np.int16)

    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as wav_file:

        wav_file.setnchannels(1)

        wav_file.setsampwidth(2)

        wav_file.setframerate(
            SAMPLE_RATE
        )

        wav_file.writeframes(
            signal.tobytes()
        )

    buffer.seek(0)

    return buffer


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("🎛️ Audio Control Panel")

audio_type = st.sidebar.selectbox(
    "Select Audio Type",
    [
        "🚑 Ambulance Siren",
        "🚓 Police Siren",
        "🎂 Happy Birthday",
        "🎼 School Tune",
        "🎚️ Custom Frequency",
        "🎶 Custom Tune"
    ]
)

st.sidebar.divider()


# ==========================================================
# SIGNAL GENERATION
# ==========================================================

signal = None


# ==========================================================
# AMBULANCE SIREN
# ==========================================================

if audio_type == "🚑 Ambulance Siren":

    st.header("🚑 Ambulance Siren")

    duration = st.sidebar.slider(
        "Duration (seconds)",
        1,
        10,
        5
    )

    signal = generate_siren(
        700,
        1200,
        duration,
        1.2
    )


# ==========================================================
# POLICE SIREN
# ==========================================================

elif audio_type == "🚓 Police Siren":

    st.header("🚓 Police Siren")

    duration = st.sidebar.slider(
        "Duration (seconds)",
        1,
        10,
        5
    )

    signal = generate_siren(
        500,
        1000,
        duration,
        1.5
    )


# ==========================================================
# HAPPY BIRTHDAY
# ==========================================================

elif audio_type == "🎂 Happy Birthday":

    st.header("🎂 Happy Birthday Tune")

    note_duration = st.sidebar.slider(
        "Note Duration",
        0.1,
        1.0,
        0.35,
        0.05
    )

    signal = generate_tune(
        happy_birthday,
        note_duration
    )


# ==========================================================
# SCHOOL TUNE
# ==========================================================

elif audio_type == "🎼 School Tune":

    st.header("🎼 Musical Scale")

    note_duration = st.sidebar.slider(
        "Note Duration",
        0.1,
        1.0,
        0.30,
        0.05
    )

    signal = generate_tune(
        school_tune,
        note_duration
    )


# ==========================================================
# CUSTOM FREQUENCY
# ==========================================================

elif audio_type == "🎚️ Custom Frequency":

    st.header("🎚️ Custom Frequency Generator")

    frequency = st.sidebar.number_input(
        "Frequency (Hz)",
        min_value=20.0,
        max_value=20000.0,
        value=440.0,
        step=1.0
    )

    duration = st.sidebar.slider(
        "Duration (seconds)",
        1,
        10,
        3
    )

    amplitude = st.sidebar.slider(
        "Amplitude",
        0.1,
        1.0,
        0.5,
        0.1
    )

    st.info(
        f"🎵 Selected Frequency: {frequency:.1f} Hz"
    )

    signal = generate_tone(
        frequency,
        duration,
        amplitude
    )


# ==========================================================
# CUSTOM TUNE
# ==========================================================

elif audio_type == "🎶 Custom Tune":

    st.header("🎶 Custom Tune Generator")

    st.write(
        "Enter frequencies separated by commas."
    )

    note_input = st.text_input(
        "Frequency Sequence",
        "262,294,330,349,392,440,494,523"
    )

    note_duration = st.sidebar.slider(
        "Note Duration",
        0.1,
        1.0,
        0.35,
        0.05
    )

    try:

        notes = [
            float(x.strip())
            for x in note_input.split(",")
            if x.strip()
        ]

        if len(notes) > 0:

            signal = generate_tune(
                notes,
                note_duration
            )

    except ValueError:

        st.error(
            "❌ Please enter valid numbers."
        )


# ==========================================================
# AUDIO ANALYSIS
# ==========================================================

if signal is not None and len(signal) > 0:

    # ------------------------------------------------------
    # CREATE WAV
    # ------------------------------------------------------

    wav_audio = signal_to_wav(signal)

    # ------------------------------------------------------
    # AUDIO PLAYER
    # ------------------------------------------------------

    st.subheader("🔊 Audio Player")

    st.audio(
        wav_audio,
        format="audio/wav"
    )

    # ------------------------------------------------------
    # SIGNAL PARAMETERS
    # ------------------------------------------------------

    duration = len(signal) / SAMPLE_RATE

    peak = np.max(
        np.abs(signal)
    )

    rms = np.sqrt(
        np.mean(signal ** 2)
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Sampling Rate",
        f"{SAMPLE_RATE} Hz"
    )

    col2.metric(
        "Duration",
        f"{duration:.2f} s"
    )

    col3.metric(
        "Peak Amplitude",
        f"{peak:.3f}"
    )

    col4.metric(
        "RMS",
        f"{rms:.3f}"
    )

    # ======================================================
    # WAVEFORM
    # ======================================================

    st.subheader("📈 Time-Domain Waveform")

    display_samples = min(
        len(signal),
        SAMPLE_RATE * 2
    )

    time = (
        np.arange(display_samples)
        / SAMPLE_RATE
    )

    fig1, ax1 = plt.subplots(
        figsize=(12, 4)
    )

    ax1.plot(
        time,
        signal[:display_samples]
    )

    ax1.set_title(
        "Audio Signal Waveform"
    )

    ax1.set_xlabel(
        "Time (seconds)"
    )

    ax1.set_ylabel(
        "Amplitude"
    )

    ax1.grid(True)

    st.pyplot(
        fig1,
        clear_figure=True
    )

    # ======================================================
    # FFT
    # ======================================================

    st.subheader(
        "📊 Frequency-Domain Analysis (FFT)"
    )

    N = len(signal)

    fft_values = np.fft.rfft(
        signal
    )

    frequencies = np.fft.rfftfreq(
        N,
        1 / SAMPLE_RATE
    )

    magnitude = (
        2 * np.abs(fft_values) / N
    )

    max_frequency = min(
        5000,
        SAMPLE_RATE / 2
    )

    mask = frequencies <= max_frequency

    fig2, ax2 = plt.subplots(
        figsize=(12, 4)
    )

    ax2.plot(
        frequencies[mask],
        magnitude[mask]
    )

    ax2.set_title(
        "FFT Frequency Spectrum"
    )

    ax2.set_xlabel(
        "Frequency (Hz)"
    )

    ax2.set_ylabel(
        "Magnitude"
    )

    ax2.grid(True)

    st.pyplot(
        fig2,
        clear_figure=True
    )

    # ======================================================
    # DOMINANT FREQUENCY
    # ======================================================

    if len(magnitude) > 1:

        dominant_index = (
            np.argmax(
                magnitude[1:]
            ) + 1
        )

        dominant_frequency = (
            frequencies[
                dominant_index
            ]
        )

        st.success(
            f"🎯 Dominant Frequency: "
            f"{dominant_frequency:.2f} Hz"
        )

    # ======================================================
    # DOWNLOAD AUDIO
    # ======================================================

    st.download_button(
        label="⬇️ Download WAV Audio",
        data=wav_audio,
        file_name="adaptive_audio.wav",
        mime="audio/wav"
    )


# ==========================================================
# PROJECT INFORMATION
# ==========================================================

st.divider()

st.header("📚 Project Information")

st.markdown("""
### Adaptive Audio Signal & Tune Generator

This project demonstrates the generation and analysis
of audio signals using Python.

#### Technologies Used

- Python
- NumPy
- Matplotlib
- Streamlit
- FFT
- WAV Audio

#### Main Functions

1. Audio signal generation
2. Ambulance siren generation
3. Police siren generation
4. Musical tune generation
5. Custom frequency generation
6. Custom tune generation
7. Waveform visualization
8. FFT frequency analysis
9. Dominant frequency detection
10. Audio playback
11. WAV file download

#### Project Flow

**Python → Streamlit GUI → GitHub → Streamlit Cloud → Android**
""")

st.success(
    "🎓 Electronics & Telecommunication Engineering Laboratory Project"
)
