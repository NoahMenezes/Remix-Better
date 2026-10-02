"""Generate a synthetic test sample with stdlib only (no pip deps).

Creates samples/test_synth.wav: 8s stereo 44.1kHz with a 120 BPM click
(drums), a 55 Hz pulse (bass-ish), and a 440/554 Hz melody (other) so
separation output can be sanity-checked by ear once Demucs runs.

Run: ./venv/bin/python scripts/make_sample.py
"""
import math
import os
import struct
import wave

SR = 44100
DURATION = 8.0
BPM = 120.0
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "samples", "test_synth.wav")


def _sample(t: float) -> tuple[float, float]:
    beat = 60.0 / BPM
    # Click on each beat (drums stand-in): short decaying noise burst.
    phase = t % beat
    click = math.exp(-phase * 120.0) * math.sin(2 * math.pi * 2000.0 * phase)
    # Bass pulse on beats 1 & 3.
    bar = t % (beat * 4)
    bass = 0.5 * math.sin(2 * math.pi * 55.0 * t) if bar < beat * 2 else 0.0
    # Simple two-note melody alternating each bar.
    freq = 440.0 if (t % (beat * 8)) < beat * 4 else 554.37
    melody = 0.25 * math.sin(2 * math.pi * freq * t)
    mono = click * 0.6 + bass * 0.5 + melody
    mono = max(-0.95, min(0.95, mono))
    return mono, mono * 0.9


def main() -> str:
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    n = int(SR * DURATION)
    with wave.open(OUT, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        for i in range(n):
            l, r = _sample(i / SR)
            w.writeframes(struct.pack("<hh", int(l * 32767), int(r * 32767)))
    print(f"Wrote {OUT} ({DURATION}s @ {BPM:.0f} BPM synthetic)")
    return OUT


if __name__ == "__main__":
    main()
