"""Generate the plugin's default sounds (pure stdlib, no deps).

Usage:  python scripts/generate-sounds.py
Writes: sounds/notify.wav & sounds/complete.wav

Design ("tada" set): notify and complete share ONE melodic line (D->G->C),
question and answer. notify stops hanging on G ("ding-dong?"); complete
quotes the same D->G motif as a fast pickup, then resolves into a C-major
chord bloom ("ding-dong-DAA!"). Same marimba timbre and reverb throughout,
soft attack (no click), exponential decay, peak -7.5 dBFS.

A "complete" sound must resolve onto the tonic (do) — ending on the
dominant (sol) sounds unresolved / still-in-progress.
"""
import math
import os
import struct
import wave

SR = 44100

# Note frequencies (Hz)
C5, D5, E5, G5, C6 = 523.25, 587.33, 659.25, 783.99, 1046.50

TIMBRE = dict(attack=0.008, detune=0.10,
              partials=[(1, 1.00, 1.0), (2, 0.25, 0.6), (3, 0.08, 0.4)])

REVERB_WET = 0.10
PEAK = 0.42

# events = [(start, freq, dur, amp, tau)]
SOUNDS = {
    "notify": [(0.00, D5, 0.35, 0.85, 0.09), (0.16, G5, 0.55, 1.00, 0.16)],
    "complete": [(0.00, D5, 0.18, 0.60, 0.07), (0.10, G5, 0.18, 0.70, 0.07),
                 (0.22, C5, 0.75, 0.60, 0.22), (0.22, E5, 0.75, 0.55, 0.20),
                 (0.22, G5, 0.75, 0.50, 0.20), (0.22, C6, 0.75, 0.85, 0.26)],
}
TOTAL_DUR = 1.10


def tone(freq, dur, amp, tau):
    """One marimba-like note: warm fundamental, overtones that die out faster."""
    attack = TIMBRE["attack"]
    samples = []
    for i in range(int(SR * dur)):
        t = i / SR
        env = math.exp(-t / tau)
        if t < attack:
            env *= t / attack
        s = 0.0
        for mult, pamp, tmult in TIMBRE["partials"]:
            s += pamp * math.sin(2 * math.pi * freq * mult * t) * math.exp(-t / (tau * tmult))
        s += TIMBRE["detune"] * math.sin(2 * math.pi * freq * 1.004 * t)
        samples.append(amp * env * s)
    return samples


def mix(events, total_dur):
    buf = [0.0] * int(SR * total_dur)
    for start, samples in events:
        offset = int(SR * start)
        for i, v in enumerate(samples):
            if offset + i < len(buf):
                buf[offset + i] += v
    return buf


def reverb(buf, wet, decay=0.45):
    """Light comb-filter reverb for a touch of 'air'."""
    if wet <= 0:
        return buf
    n = len(buf)
    out = list(buf)
    for d in (1021, 1279, 1523):  # ~23-35ms combs
        y = [0.0] * n
        for i in range(n):
            y[i] = buf[i] + (decay * y[i - d] if i >= d else 0.0)
        for i in range(n):
            out[i] += (wet / 3) * (y[i] - buf[i])
    return out


def write_wav(path, buf, peak_target):
    peak = max(abs(v) for v in buf) or 1.0
    scale = peak_target / peak
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(
            b"".join(
                struct.pack("<h", int(max(-1.0, min(1.0, v * scale)) * 32767)) for v in buf
            )
        )
    print(f"wrote {path} ({len(buf) / SR:.2f}s)")


def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sounds")
    os.makedirs(out_dir, exist_ok=True)
    for kind, spec in SOUNDS.items():
        events = [(start, tone(f, dur, amp, tau)) for start, f, dur, amp, tau in spec]
        buf = reverb(mix(events, TOTAL_DUR), REVERB_WET)
        write_wav(os.path.join(out_dir, f"{kind}.wav"), buf, PEAK)


if __name__ == "__main__":
    main()
