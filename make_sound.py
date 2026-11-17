#!/usr/bin/env python3
"""
OneFlow sound design — the score is derived from the film itself.

    python3 make_sound.py templates/product-launch.json -o sound.wav
    python3 make_film.py templates/product-launch.json -o film.mp4 --sound

No audio files, no samples, no library music: every sound is
synthesised from the film sheet's own events, so the sound always
fits the action because it IS the action, heard:

- a soft synth pad under the whole film, one chord per beat, chosen
  deterministically from the film's title;
- a whoosh at every carried boundary, its length set by the morph
  time and its strength by how far the camera travelled;
- a short pluck for every element that ENTERS in a beat, pitched from
  a pentatonic scale by the element's id, staggered as they arrive;
- a low hit at the final beat (the landing), and wherever a beat
  sets "sound": "hit". A beat with "sound": "none" gets no events
  (the pad still plays) — use it for rest beats.

Deterministic: the same sheet always scores the same film.
Pure standard library. MIT licensed — free for everyone, forever.
"""

import argparse
import json
import math
import random
import struct
import wave
from pathlib import Path

SR = 44100
# chord roots (Hz): A2, F2, C3, G2 — a calm I–VI–III–VII loop in A minor
ROOTS = [110.00, 87.31, 130.81, 98.00]
# A-minor pentatonic for entrance plucks
SCALE = [220.00, 261.63, 329.63, 392.00, 440.00, 523.25]


def _add(buf, t0, samples):
    i0 = int(t0 * SR)
    for j, s in enumerate(samples):
        i = i0 + j
        if 0 <= i < len(buf):
            buf[i] += s


def _tone(freq, dur, gain, attack=0.01, decay_pow=2.0, slide_to=None):
    n = int(dur * SR)
    out = []
    for i in range(n):
        p = i / max(n - 1, 1)
        f = freq if slide_to is None else freq + (slide_to - freq) * p
        env = min(1.0, i / max(int(attack * SR), 1)) * (1 - p) ** decay_pow
        out.append(gain * env * math.sin(2 * math.pi * f * i / SR))
    return out


def _whoosh(rng, dur, gain):
    """Noise through a sweeping one-pole lowpass — a soft airy sweep."""
    n = int(dur * SR)
    out = []
    y = 0.0
    for i in range(n):
        p = i / max(n - 1, 1)
        cutoff = 0.02 + 0.30 * math.sin(math.pi * p)  # opens, then closes
        y += cutoff * (rng.uniform(-1, 1) - y)
        env = math.sin(math.pi * p) ** 1.5
        out.append(gain * env * y * 2.4)
    return out


def _thump(gain=0.5):
    return _tone(72, 0.32, gain, attack=0.004, decay_pow=2.6, slide_to=44)


def synthesize(sheet, out_path):
    beats = sheet.get("beats", [])
    if not beats:
        raise SystemExit("the film sheet needs a non-empty 'beats' list")
    starts, acc = [], 0.0
    for b in beats:
        starts.append(acc)
        acc += float(b.get("dur", 0))
    total = acc
    morph = float(sheet.get("morph", 0.5))
    rng = random.Random("oneflow:" + str(sheet.get("title", "")))
    buf = [0.0] * int((total + 0.15) * SR)

    def cam(b):
        c = b.get("camera") or {}
        return (float(c.get("x", sheet["width"] / 2)),
                float(c.get("y", sheet["height"] / 2)),
                float(c.get("zoom", 1)))

    for i, beat in enumerate(beats):
        t0, dur = starts[i], float(beat.get("dur", 0))
        mode = beat.get("sound", "auto")
        # --- pad: one chord per beat (root, fifth, octave + a soft third)
        root = ROOTS[i % len(ROOTS)]
        for mult, g in ((1.0, 0.055), (1.5, 0.032), (2.0, 0.026), (1.189, 0.018)):
            _add(buf, t0, _tone(root * mult, dur + 0.25, g,
                                attack=min(0.45, dur / 2), decay_pow=0.55))
        if mode == "none":
            continue
        # --- boundary whoosh (every beat after the first is a carried morph)
        if i > 0:
            x0, y0, z0 = cam(beats[i - 1])
            x1, y1, z1 = cam(beat)
            travel = math.hypot(x1 - x0, y1 - y0) / 900.0 + abs(z1 - z0)
            gain = 0.10 + min(0.14, travel * 0.10)
            _add(buf, max(0.0, t0 - 0.08), _whoosh(rng, morph + 0.22, gain))
        # --- entrance plucks: elements that are new in this beat
        prev_ids = {e.get("id") for e in beats[i - 1].get("elements", [])} if i else set()
        new_els = [e for e in beat.get("elements", []) if e.get("id") not in prev_ids]
        for j, el in enumerate(new_els):
            pitch = SCALE[(sum(map(ord, str(el.get("id", "")))) + j) % len(SCALE)]
            _add(buf, t0 + 0.10 + j * 0.09,
                 _tone(pitch, 0.34, 0.085, attack=0.005, decay_pow=2.4))
        # --- hits: forced, or the final landing
        if mode == "hit" or i == len(beats) - 1:
            _add(buf, t0, _thump(0.42 if i == len(beats) - 1 else 0.3))
            if i == len(beats) - 1:  # a small resolving shimmer on the landing
                for k, mult in enumerate((2.0, 2.5, 3.0)):
                    _add(buf, t0 + 0.05 + k * 0.07,
                         _tone(ROOTS[0] * mult, 0.6, 0.035,
                               attack=0.01, decay_pow=2.2))

    # master: soft-clip, gentle fade out, write 16-bit stereo WAV
    n = len(buf)
    frames = bytearray()
    for i, s in enumerate(buf):
        fade = 1.0 if i < n - int(0.4 * SR) else (n - i) / (0.4 * SR)
        v = math.tanh(s * 1.15) * 0.82 * fade
        iv = int(max(-1.0, min(1.0, v)) * 32767)
        frames += struct.pack("<hh", iv, iv)
    with wave.open(str(out_path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(bytes(frames))
    print(f"sound: {out_path} ({total:.1f}s scored from {len(beats)} beats)")
    return out_path


def main():
    ap = argparse.ArgumentParser(description="OneFlow sound design — score a film sheet.")
    ap.add_argument("sheet", help="film sheet JSON")
    ap.add_argument("-o", "--output", default="sound.wav", help="output WAV")
    args = ap.parse_args()
    from make_film import resolve_sheet
    sheet = resolve_sheet(json.loads(Path(args.sheet).read_text(encoding="utf-8")))
    synthesize(sheet, args.output)


if __name__ == "__main__":
    main()
