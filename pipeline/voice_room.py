#!/usr/bin/env python3
"""Put the voice in the room the picture shows (adopted 2026-09-29 from the realism test; tape hiss dropped).
ElevenLabs voices come out as a dry, full-band booth recording; over a 1990s picture that reads as dubbed. This:
  band-limits to 120 Hz - 7 kHz (gentle 12 dB/oct slopes), adds a touch of tape saturation, and a small office room
  (RT60 ~0.35 s, early reflections 7-34 ms, the reverb ~13 dB under the direct sound). Loudness is kept.
Timing is unchanged (the direct sound is not delayed), so lip sync is unaffected.
assemble.py applies it to every part with sound unless the part says "room": false (music, stings, montage, a
caller already treated as a phone line, or a mix whose dialogue was treated in its own build).
Usage: voice_room.py IN OUT   (wav or video; video is copied, audio treated)"""
import os, subprocess, sys, tempfile, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
WET_DB = -13.0; RT60 = 0.35


def _bp(x, lo, hi):
    x = sosfilt(butter(2, lo, "highpass", fs=SR, output="sos"), x, axis=0)
    return sosfilt(butter(2, hi, "lowpass", fs=SR, output="sos"), x, axis=0)


def room_ir(seed=3):
    rng = np.random.default_rng(seed)
    n = int(0.45 * SR); t = np.arange(n) / SR
    tail = _bp(rng.standard_normal(n) * np.exp(-6.91 * t / RT60), 200, 4500)
    ir = np.zeros(n); ir[0] = 1.0
    for d, g in ((0.007, 0.35), (0.013, 0.28), (0.019, 0.22), (0.027, 0.18), (0.034, 0.12)):
        ir[int(d * SR)] += g * (1 if rng.random() > 0.5 else -1)
    ir[int(0.009 * SR):] += (tail / np.sqrt(np.sum(tail ** 2)) * 10 ** (WET_DB / 20))[: n - int(0.009 * SR)]
    return ir


def treat(x):
    """x: float array (n,) or (n, ch) at 48 kHz -> same shape, same RMS"""
    x = np.asarray(x, np.float64)
    rms0 = np.sqrt(np.mean(x ** 2)) + 1e-12
    y = _bp(x, 120, 7000)
    y = np.tanh(y * 2.2) / np.tanh(2.2)
    ir = room_ir()
    y = np.stack([fftconvolve(y[:, c], ir)[: len(y)] for c in range(y.shape[1])], 1) if y.ndim == 2 else fftconvolve(y, ir)[: len(y)]
    return (y * rms0 / (np.sqrt(np.mean(y ** 2)) + 1e-12)).astype(np.float32)


def treat_file(src, out):
    """treat the sound of src (audio or video) into out; video stream copied"""
    from common import FFMPEG
    tmp = tempfile.mkdtemp(); a = os.path.join(tmp, "a.wav"); b = os.path.join(tmp, "b.wav")
    subprocess.run([FFMPEG, "-y", "-v", "error", "-i", src, "-vn", "-ac", "2", "-ar", str(SR), "-c:a", "pcm_s16le", a], check=True)
    w = wave.open(a); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32) / 32768
    y = treat(x)
    w = wave.open(b, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    if os.path.splitext(out)[1].lower() == ".wav":
        os.replace(b, out)
    else:
        subprocess.run([FFMPEG, "-y", "-v", "error", "-i", src, "-i", b, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                        "-c:a", "pcm_s16le", out], check=True)
    return out


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    print(treat_file(sys.argv[1], sys.argv[2]))
