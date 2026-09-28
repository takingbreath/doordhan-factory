#!/usr/bin/env python3
"""The room under every scene, from real recordings (adopted 2026-09-29; the synthesised bed of the realism test
was replaced with recorded CC0 ambience, and lowered 9 dB). Packs are built from assets/audio/ambience (sources and
licences in SOURCES.md):
  office  an electric fan (low-passed, a room away from the mic) and a distant road through a closed window
assemble.py mixes the pack under the whole reel at "ambience_db" relative to the programme loudness (default -36:
the test bed sat 27 dB under speech, lowered 9 dB), before the TV-speaker filter, with 0.3 s fades.
Usage: ambience.py OUT.wav SECONDS [--pack office]   (writes the bed alone at -30 dB RMS, to listen to)"""
import os, sys, wave
import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000
DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "audio", "ambience")
PACKS = {"office": [("fan_loop.wav", 0.0, 2500), ("road_distant_loop.wav", -3.0, 1200)]}   # file, gain dB, low-pass Hz
DEFAULT_DB = -36.0


def _load(name):
    w = wave.open(os.path.join(DIR, name))
    return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768


def bed(seconds, pack="office", seed=0):
    n = int(seconds * SR); rng = np.random.default_rng(seed); out = np.zeros(n, np.float32)
    for name, gdb, lp in PACKS[pack]:
        x = _load(name)
        x = sosfilt(butter(2, lp, "lowpass", fs=SR, output="sos"), x).astype(np.float32)
        start = int(rng.integers(0, len(x)))
        idx = (np.arange(n) + start) % len(x)
        out += x[idx] * 10 ** (gdb / 20)
    f = min(int(0.3 * SR), n // 4)
    out[:f] *= np.linspace(0, 1, f); out[n - f:] *= np.linspace(1, 0, f)
    return out


def rms_db(x):
    return 20 * np.log10(np.sqrt(np.mean(np.square(x, dtype=np.float64))) + 1e-12)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("seconds", type=float)
    ap.add_argument("--pack", default="office")
    a = ap.parse_args()
    b = bed(a.seconds, a.pack); b *= 10 ** ((-30 - rms_db(b)) / 20)
    w = wave.open(a.out, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(b, -1, 1) * 32767).astype(np.int16).tobytes()); w.close(); print(a.out)
