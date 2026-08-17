def generate_instrument_tone(frequency, duration, style):

    t = np.linspace(
        0,
        duration,
        int(SAMPLE_RATE * duration),
        endpoint=False
    )

    # Envelope: attack + decay + sustain + release
    attack = min(int(0.03 * SAMPLE_RATE), len(t) // 4)
    release = min(int(0.08 * SAMPLE_RATE), len(t) // 4)

    envelope = np.ones(len(t))

    if attack > 0:
        envelope[:attack] = np.linspace(0, 1, attack)

    if release > 0:
        envelope[-release:] = np.linspace(1, 0, release)

    # ---------------- PIANO ----------------

    if style == "🎹 Piano":

        tone = (
            1.00 * np.sin(2 * np.pi * frequency * t)
            + 0.35 * np.sin(2 * np.pi * frequency * 2 * t)
            + 0.18 * np.sin(2 * np.pi * frequency * 3 * t)
            + 0.08 * np.sin(2 * np.pi * frequency * 4 * t)
        )

        # Piano-like decay
        envelope *= np.exp(-2.5 * t)

    # ---------------- THEATER ----------------

    elif style == "🎭 Theater":

        vibrato = 4 * np.sin(
            2 * np.pi * 5 * t
        )

        tone = (
            0.8 * np.sin(
                2 * np.pi * (frequency + vibrato) * t
            )
            + 0.35 * np.sin(2 * np.pi * frequency * 2 * t)
            + 0.15 * np.sin(2 * np.pi * frequency * 3 * t)
        )

    # ---------------- JAZZ ----------------

    elif style == "🎷 Jazz":

        vibrato = 2.5 * np.sin(
            2 * np.pi * 4.5 * t
        )

        tone = (
            0.75 * np.sin(
                2 * np.pi * (frequency + vibrato) * t
            )
            + 0.45 * np.sin(2 * np.pi * frequency * 2 * t)
            + 0.30 * np.sin(2 * np.pi * frequency * 3 * t)
            + 0.15 * np.sin(2 * np.pi * frequency * 4 * t)
        )

    # ---------------- CELEBRATION ----------------

    elif style == "🎺 Celebration":

        tone = (
            0.8 * np.sin(2 * np.pi * frequency * t)
            + 0.5 * np.sin(2 * np.pi * frequency * 2 * t)
            + 0.3 * np.sin(2 * np.pi * frequency * 3 * t)
            + 0.2 * np.sin(2 * np.pi * frequency * 4 * t)
        )

    # ---------------- CLASSIC ----------------

    else:

        tone = (
            0.9 * np.sin(2 * np.pi * frequency * t)
            + 0.25 * np.sin(2 * np.pi * frequency * 2 * t)
            + 0.12 * np.sin(2 * np.pi * frequency * 3 * t)
        )

    return tone * envelope
