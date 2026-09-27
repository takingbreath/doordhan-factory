#!/usr/bin/env python3
"""The edit's sound-effect kit, synthesised locally (no credits, no licences), written to assets/audio/sfx_*.wav.
whoosh (whip pans), pop (a word popping on), ding (a number landing), thud (a slam), scratch (record scratch),
riser (tension before a reveal), stamp (rubber stamp / verdict), room (office fan hum, loopable).
  sfx.py [--out assets/audio]"""
import argparse, os, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(7)


def t(d):
    return np.arange(int(SR * d)) / SR


def bandnoise(d, lo, hi):
    """White noise band-limited in the frequency domain; lo/hi may be arrays over time (a sweep)."""
    n = int(SR * d)
    N, hop = 2048, 512  # STFT overlap-add with a Hann window: no clicks at block edges
    x = rng.standard_normal(n + N)
    out = np.zeros(n + N); norm = np.zeros(n + N); w = np.hanning(N)
    f = np.fft.rfftfreq(N, 1 / SR)
    for s in range(0, n, hop):
        i = min(s, n - 1)
        l = lo[i] if np.ndim(lo) else lo; h = hi[i] if np.ndim(hi) else hi
        X = np.fft.rfft(x[s:s + N] * w)
        X[(f < l) | (f > h)] = 0
        out[s:s + N] += np.fft.irfft(X) * w; norm[s:s + N] += w * w
    out = out[:n] / np.maximum(norm[:n], 1e-3)
    return out / (np.abs(out).max() + 1e-9)


def env(x, a, r):
    n = len(x); tt = np.arange(n) / SR
    e = np.minimum(1, tt / max(a, 1e-4)) * np.exp(-np.maximum(0, tt - a) / max(r, 1e-4))
    return x * e


def whoosh():
    d = 0.38; n = int(SR * d); tt = t(d)
    lo = np.linspace(300, 1800, n); hi = lo * 3
    x = bandnoise(d, lo, hi)
    shape = np.sin(np.pi * np.minimum(1, tt / d)) ** 2
    return 0.8 * x * shape


def pop():
    d = 0.09; tt = t(d)
    f = 900 * np.exp(-tt * 30) + 250
    x = np.sin(2 * np.pi * np.cumsum(f) / SR)
    return 0.9 * env(x, 0.002, 0.03)


def ding():
    d = 1.1; tt = t(d)
    x = sum(a * np.sin(2 * np.pi * f * tt) for f, a in [(1318, 1), (2637, 0.35), (3951, 0.15), (1976, 0.2)])
    return 0.5 * env(x, 0.003, 0.35)


def thud():
    d = 0.6; tt = t(d)
    f = 110 * np.exp(-tt * 9) + 45
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.25 * env(bandnoise(d, 80, 2500), 0.001, 0.02)
    return 0.95 * env(x, 0.002, 0.16)


def scratch():
    d = 0.42; n = int(SR * d); tt = t(d)
    c = 900 + 700 * np.sin(2 * np.pi * 7 * tt)
    x = bandnoise(d, c * 0.6, c * 1.6)
    return 0.8 * x * np.minimum(1, tt / 0.01) * np.minimum(1, (d - tt) / 0.06)


def riser():
    d = 1.4; n = int(SR * d); tt = t(d)
    lo = np.linspace(200, 2500, n)
    x = bandnoise(d, lo, lo * 2.5) * 0.6
    f = np.linspace(180, 720, n)
    x += 0.35 * np.sin(2 * np.pi * np.cumsum(f) / SR)
    return 0.75 * x * (tt / d) ** 2


def stamp():
    d = 0.35; tt = t(d)
    x = 0.7 * np.sin(2 * np.pi * (180 * np.exp(-tt * 20) + 70) * tt) + 0.6 * env(bandnoise(d, 300, 5000), 0.001, 0.015)
    return 0.95 * env(x, 0.001, 0.07)


def room():
    """10 s loop: brown-ish noise, the fan's 50 Hz motor hum and a slow blade swish."""
    d = 10.0; tt = t(d)
    b = np.cumsum(rng.standard_normal(len(tt))); b -= np.convolve(b, np.ones(4800) / 4800, "same"); b /= np.abs(b).max()
    hum = 0.25 * np.sin(2 * np.pi * 100 * tt) + 0.12 * np.sin(2 * np.pi * 150 * tt)
    swish = 1 + 0.25 * np.sin(2 * np.pi * 4.5 * tt)
    x = (0.8 * b * swish + hum)
    fade = int(SR * 0.5)  # crossfade the ends so it loops
    x[:fade] = x[:fade] * np.linspace(0, 1, fade) + x[-fade:] * np.linspace(1, 0, fade)
    return 0.3 * x[: len(x) - fade] / np.abs(x).max()


def save(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                  "assets", "audio"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    for name, fn in [("whoosh", whoosh), ("pop", pop), ("ding", ding), ("thud", thud), ("scratch", scratch),
                     ("riser", riser), ("stamp", stamp), ("room", room)]:
        p = os.path.join(a.out, f"sfx_{name}.wav"); save(p, fn()); print("wrote", p)
