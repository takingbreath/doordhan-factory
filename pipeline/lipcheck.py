#!/usr/bin/env python3
"""Do the lips move? Two crude numbers, both from a mouth box:
  1. mouth motion while speaking vs while silent (caught the dead-lips desk shot), and
  2. mouth motion vs head motion while speaking (a control box above the mouth), which still works
     on short clips with few silent frames and separates lip-sync from a nodding head.
Usage: lipcheck.py CLIP.mp4 --box X Y W H [--control X Y W H]   (boxes in the 480x854 analysis frame;
                                                                   control defaults to the region above the mouth)
       lipcheck.py CLIP.mp4 --face-crop 3.0 OUT.png                (save a frame to locate the mouth box)
Test shot, 2026-09-25 (Sarika close-up, clearly talking): speaking/silent 1.29, mouth/head 1.70."""
import argparse, subprocess
import numpy as np
from common import FFMPEG, AW, AH, run, envelope

p = argparse.ArgumentParser()
p.add_argument("clip")
p.add_argument("--box", nargs=4, type=int)
p.add_argument("--control", nargs=4, type=int)
p.add_argument("--face-crop", nargs=2)
a = p.parse_args()
if a.face_crop:
    t, out = a.face_crop
    run([FFMPEG, "-y", "-v", "error", "-ss", t, "-i", a.clip, "-frames:v", "1", "-vf", f"scale={AW}:{AH}", out])
    print(f"saved {out} ({AW}x{AH}); pick the mouth box in these coordinates"); raise SystemExit
if not a.box:
    p.error("--box X Y W H is required (use --face-crop first to find it)")


def motion(x0, y0, w, h):
    raw = subprocess.run([FFMPEG, "-v", "error", "-i", a.clip, "-vf",
                          f"scale={AW}:{AH},fps=24,crop={w}:{h}:{x0}:{y0},gblur=sigma=3,format=gray",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(float)
    return np.convolve(np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2)), np.ones(3) / 3, "same")


x0, y0, w, h = a.box
ctrl = a.control or (x0, max(0, y0 - 2 * h), w, h)
mot, head = motion(x0, y0, w, h), motion(*ctrl)
db = envelope(a.clip, win=1 / 24)
n = min(len(mot), len(head), len(db) - 1)
mot, head, speaking = mot[:n], head[:n], (db[1:n + 1] > -38)
if not speaking.any():
    print("INCONCLUSIVE  no speech found in the clip"); raise SystemExit
vs_head = mot[speaking].mean() / max(head[speaking].mean(), 1e-6)
if (~speaking).any():
    ratio = mot[speaking].mean() / max(mot[~speaking].mean(), 1e-6)
    ok = ratio >= 1.15 and vs_head >= 1.3
    print(f"{'PASS' if ok else 'CHECK'}  mouth-motion ratio speaking/silent = {ratio:.2f} (>=1.15), "
          f"mouth/head while speaking = {vs_head:.2f} (>=1.3)")
else:
    print(f"{'PASS' if vs_head >= 1.3 else 'CHECK'}  no silent frames; mouth/head while speaking = {vs_head:.2f} (>=1.3)")
