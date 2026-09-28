#!/usr/bin/env python3
"""E5 look/sound lab (2026-09-29): free audio treatments on the in-sync v5 build, for A/B against v5.
Inputs (copies of the v5 build): work/lab/base/{mix,dialogue}.wav. rest = mix - dialogue (SFX, ring, room tone).
  A  ambient bed: ceiling fan (blade swish + motor hum), distant traffic with far horns, faint mains/line noise,
     about 24 dB under the dialogue, under every scene until the closing card
  B  voice to match the picture: Pandey's lines band-limited 120 Hz-7 kHz, a touch of tape saturation, a small
     office room (RT60 ~0.35 s, wet ~13 dB under dry), continuous tape hiss ~40 dB under the voice
Writes work/lab/audio/{A,B,AB}.wav (mono 48 kHz) and bed.wav / hiss.wav for listening on their own."""
import os, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
LAB = os.path.dirname(os.path.abspath(__file__))
CARD = 62.5                 # closing card starts (build.py CARD): the phone hold music has its own sound
C1 = (3.55, 8.65)           # the caller's line is already a landline; leave it alone
rng = np.random.default_rng(7)


def rd(p):
    w = wave.open(p); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return x


def wr(p, x):
    w = wave.open(p, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()


def rms_db(x):
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)


def gain_to(x, db):
    return x * 10 ** ((db - rms_db(x)) / 20)


def bp(x, lo=None, hi=None, order=2):
    if lo:
        x = sosfilt(butter(order, lo, "highpass", fs=SR, output="sos"), x)
    if hi:
        x = sosfilt(butter(order, hi, "lowpass", fs=SR, output="sos"), x)
    return x


def smooth_noise(n, rate_hz):
    """slowly varying 0..1 control signal"""
    k = max(2, int(n * rate_hz / SR) + 2)
    pts = rng.random(k)
    return np.interp(np.arange(n), np.linspace(0, n, k), pts)


def bed(n):
    t = np.arange(n) / SR
    # ceiling fan: broadband air, amplitude-modulated at the blade-pass rate (~4.7 rev/s x 3 blades), plus motor hum
    air = bp(rng.standard_normal(n), 150, 2500)
    blade = 1 + 0.35 * np.sin(2 * np.pi * 14.1 * t) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.13 * t))
    hum = 0.25 * np.sin(2 * np.pi * 100 * t) + 0.12 * np.sin(2 * np.pi * 200 * t + 1) + 0.05 * np.sin(2 * np.pi * 300 * t)
    fan = gain_to(air * blade, -46) + gain_to(hum, -58)
    # distant traffic through a closed window: low rumble with slow swells, a far horn now and then
    rumble = bp(np.cumsum(rng.standard_normal(n)) * 0.01, 60, 450)
    rumble -= np.convolve(rumble, np.ones(SR) / SR, "same")          # remove drift of the random walk
    rumble *= 0.6 + 0.8 * smooth_noise(n, 0.15)
    traffic = gain_to(rumble, -47)
    for at in (5.2, 17.8, 31.5, 44.0, 57.3):
        L = int(rng.uniform(0.25, 0.6) * SR); f0 = rng.choice([392, 440, 466])
        tt = np.arange(L) / SR
        horn = np.sign(np.sin(2 * np.pi * f0 * tt)) * 0.6 + np.sign(np.sin(2 * np.pi * f0 * 1.26 * tt)) * 0.4
        horn = bp(horn * np.minimum(1, np.minimum(tt / 0.03, (L / SR - tt) / 0.08)), 300, 1400)
        horn = fftconvolve(horn, np.exp(-np.arange(int(0.5 * SR)) / (0.12 * SR)) * rng.standard_normal(int(0.5 * SR)))[:L + SR // 2]
        i = int(at * SR); j = min(n, i + len(horn))
        traffic[i:j] += gain_to(horn, -58)[: j - i]
    # faint line noise: mains buzz harmonics and a little hiss from the old wiring
    buzz = sum(np.sin(2 * np.pi * 50 * k * t + k) / k for k in (3, 5, 7, 9))
    line = gain_to(bp(buzz, 120, 2000), -64) + gain_to(bp(rng.standard_normal(n), 2000, 8000), -66)
    b = fan + traffic + line
    fade = int(0.4 * SR)
    b[int(CARD * SR) - fade: int(CARD * SR)] *= np.linspace(1, 0, fade)
    b[int(CARD * SR):] = 0
    b[: int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR))
    return b.astype(np.float32)


def room_ir():
    n = int(0.45 * SR); t = np.arange(n) / SR
    tail = rng.standard_normal(n) * np.exp(-6.91 * t / 0.35)       # RT60 0.35 s
    tail = bp(tail, 200, 4500)
    ir = np.zeros(n); ir[0] = 1.0
    for d, g in ((0.007, 0.35), (0.013, 0.28), (0.019, 0.22), (0.027, 0.18), (0.034, 0.12)):   # desk, walls
        ir[int(d * SR)] += g * rng.choice([-1, 1])
    wet = tail / np.sqrt(np.sum(tail ** 2)) * 10 ** (-13 / 20)       # wet ~13 dB under the direct sound
    ir[int(0.009 * SR):] += wet[: n - int(0.009 * SR)]
    return ir


def voice(dia):
    v = dia.astype(np.float64).copy()
    keep = v.copy()
    v = bp(v, 120, 7000, order=2)                  # tape/TV-studio bandwidth, gentle 12 dB/oct slopes
    v = np.tanh(v * 2.2) / np.tanh(2.2)            # slight tape saturation (soft on peaks)
    v = fftconvolve(v, room_ir())[: len(v)]
    v *= np.sqrt(np.mean(keep ** 2)) / (np.sqrt(np.mean(v ** 2)) + 1e-12)   # same loudness as before
    i0, i1 = int(C1[0] * SR), int(C1[1] * SR)
    v[i0:i1] = keep[i0:i1]                          # the caller stays the landline sound it already is
    # tape hiss: continuous from the first Pandey line to the card, ~40 dB under the voice
    speech_db = 20 * np.log10(np.sqrt(np.mean(keep[np.abs(keep) > 0.01] ** 2)))
    hiss = bp(rng.standard_normal(len(v)), 1500, 10000)
    hiss = gain_to(hiss, speech_db - 40)
    s0, s1 = int(8.9 * SR), int(CARD * SR)
    env = np.zeros(len(v)); env[s0:s1] = 1
    ramp = int(0.2 * SR); env[s0:s0 + ramp] = np.linspace(0, 1, ramp); env[s1 - ramp:s1] = np.linspace(1, 0, ramp)
    return (v + hiss * env).astype(np.float32), (hiss * env).astype(np.float32)


if __name__ == "__main__":
    mix = rd(os.path.join(LAB, "base", "mix.wav")); dia = rd(os.path.join(LAB, "base", "dialogue.wav"))
    rest = mix - dia
    out = os.path.join(LAB, "audio"); os.makedirs(out, exist_ok=True)
    b = bed(len(mix)); vb, hiss = voice(dia)
    wr(os.path.join(out, "bed.wav"), b * 8); wr(os.path.join(out, "hiss.wav"), hiss * 8)   # +18 dB, to hear them
    wr(os.path.join(out, "A.wav"), rest + dia + b)
    wr(os.path.join(out, "B.wav"), rest + vb)
    wr(os.path.join(out, "AB.wav"), rest + vb + b)
    sp = np.abs(dia) > 0.01
    print(f"dialogue {rms_db(dia[sp]):.1f} dB (speech), bed {rms_db(b[: int(CARD * SR)]):.1f} dB, "
          f"old room tone etc. {rms_db(rest[: int(CARD * SR)]):.1f} dB, hiss {rms_db(hiss[int(9 * SR):int(62 * SR)]):.1f} dB")
