#!/usr/bin/env python3
"""How much does the head move? Hot and classy means a newsreader's steady head; a wobbling, tilting head reads
cheap (Akhilesh, 2026-09-25: "earlier it was fine... just don't overdo").
Tracks Sarika's bindi (a small dark-red dot: a clean marker) inside the upper-face box. If no bindi is found,
it falls back to phase correlation of the upper face, which works for any character but is noisier.
Usage: headcheck.py CLIP.mp4 --mouth X Y W H   (lipcheck mouth box; the upper-face box is derived from it)
       headcheck.py CLIP.mp4 --box X Y W H     (the upper face itself)        all in the 480x854 analysis frame
Calibrated 2026-09-25 on three Sarika close-ups (head travel with the bindi / with phase correlation):
  setup shot, accepted: 37 / 37 px/s (slow nods: a dip on "namaskar", lowering into the smile).
  black deep-V: 66 / 67 (constant small wobble).  maroon: 83 / 80 (tilts; Akhilesh: "overdoing the head movements").
Speed separates them; the largest offset doesn't (a slow nod travels far but reads as poise). PASS at <= 45 px/s."""
import argparse, subprocess
import numpy as np
from common import FFMPEG, AW, AH

FPS = 25
p = argparse.ArgumentParser()
p.add_argument("clip"); p.add_argument("--box", nargs=4, type=int); p.add_argument("--mouth", nargs=4, type=int)
a = p.parse_args()
if a.box:
    x0, y0, w, h = a.box
elif a.mouth:
    mx, my, mw, mh = a.mouth
    w, h = mw + 100, 120
    x0, y0 = max(0, mx + mw // 2 - w // 2), max(0, my - 170)
else:
    p.error("--mouth or --box is required")
w, h = min(w, AW - x0) // 2 * 2, min(h, AH - y0) // 2 * 2
raw = subprocess.run([FFMPEG, "-v", "error", "-i", a.clip, "-vf", f"scale={AW}:{AH},fps={FPS},crop={w}:{h}:{x0}:{y0}",
                      "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3).astype(float)
secs = len(fr) / FPS

# 1) bindi: centroid of the small dark-red blob
pts = []
for f in fr:
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    ys, xs = np.nonzero((g < 95) & (r > 110) & (r > g + 60) & (b < 115))   # bindi ~(160,65,80); skin has g > 115
    pts.append((xs.mean(), ys.mean()) if 4 <= len(xs) <= 400 else (np.nan, np.nan))
pts = np.array(pts)
found = ~np.isnan(pts[:, 0])
if found.mean() >= 0.9:
    q = pts[found]
    # the dot is a few pixels wide: take a 5-frame running median so detection jitter isn't counted as movement
    q = np.array([np.median(q[max(0, i - 2):i + 3], axis=0) for i in range(len(q))])
    travel = np.linalg.norm(np.diff(q, axis=0), axis=1).sum() / secs
    offset = np.linalg.norm(q - np.median(q, axis=0), axis=1).max()
    ok = travel <= 45
    print(f"{'PASS' if ok else 'CHECK'}  head travel {travel:.0f} px/s (<= 45, bindi), largest offset {offset:.1f} px  "
          f"[upper-face box {x0} {y0} {w} {h}]")
    raise SystemExit

# 2) fallback: phase correlation between consecutive frames of the upper face
gray = (fr @ [0.299, 0.587, 0.114])
win = np.outer(np.hanning(h), np.hanning(w))


def shift(prev, cur):
    A, B = np.fft.fft2((prev - prev.mean()) * win), np.fft.fft2((cur - cur.mean()) * win)
    R = A * np.conj(B); R /= np.abs(R) + 1e-9
    rr = np.fft.fftshift(np.real(np.fft.ifft2(R)))
    py, px = np.unravel_index(np.argmax(rr), rr.shape)
    def sub(c, m, pl):
        d = m - 2 * c + pl
        return 0.0 if abs(d) < 1e-12 else 0.5 * (m - pl) / d
    return (px - w // 2 + sub(rr[py, px], rr[py, (px - 1) % w], rr[py, (px + 1) % w]),
            py - h // 2 + sub(rr[py, px], rr[(py - 1) % h, px], rr[(py + 1) % h, px]))


steps = np.array([shift(gray[i - 1], gray[i]) for i in range(1, len(gray))])
travel = np.linalg.norm(steps, axis=1).sum() / secs
print(f"{'PASS' if travel <= 45 else 'CHECK'}  head travel {travel:.0f} px/s (<= 45, no bindi: phase correlation)  "
      f"[upper-face box {x0} {y0} {w} {h}]")
