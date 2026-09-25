#!/usr/bin/env python3
"""Does the mouth move more while speaking than while silent? Crude but caught the dead-lips desk shot.
Usage: lipcheck.py CLIP.mp4 --box X Y W H     (box around the mouth, in a 480x854 frame)
       lipcheck.py CLIP.mp4 --face-crop 3.0 OUT.png   (save a frame to find the mouth box)"""
import argparse, subprocess
import numpy as np
from common import FFMPEG, W, H, run

p = argparse.ArgumentParser()
p.add_argument("clip")
p.add_argument("--box", nargs=4, type=int)
p.add_argument("--face-crop", nargs=2)
a = p.parse_args()
if a.face_crop:
    t, out = a.face_crop
    run([FFMPEG, "-y", "-v", "error", "-ss", t, "-i", a.clip, "-frames:v", "1", "-vf", f"scale={W}:{H}", out])
    print(f"saved {out} ({W}x{H}); pick the mouth box in these coordinates"); raise SystemExit
x0, y0, w, h = a.box
raw = subprocess.run([FFMPEG, "-v", "error", "-i", a.clip, "-vf",
                      f"scale={W}:{H},fps=24,crop={w}:{h}:{x0}:{y0},gblur=sigma=3,format=gray",
                      "-f", "rawvideo", "-"], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(float)
mot = np.convolve(np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2)), np.ones(3) / 3, "same")
aud = subprocess.run([FFMPEG, "-v", "error", "-i", a.clip, "-ac", "1", "-ar", "24000", "-f", "s16le", "-"],
                     capture_output=True).stdout
x = np.frombuffer(aud, np.int16).astype(float)
spf = 1000
db = np.array([20 * np.log10(np.sqrt((x[i * spf:(i + 1) * spf] ** 2).mean() + 1e-9)) - 90.3
               for i in range(len(x) // spf)])
n = min(len(mot), len(db) - 1)
mot, speaking = mot[:n], (db[1:n + 1] > -38)
if speaking.all() or (~speaking).all():
    print("INCONCLUSIVE  no silent (or no speaking) frames to compare"); raise SystemExit
ratio = mot[speaking].mean() / max(mot[~speaking].mean(), 1e-6)
print(f"{'PASS' if ratio >= 1.15 else 'CHECK'}  mouth-motion ratio speaking/silent = {ratio:.2f}")
