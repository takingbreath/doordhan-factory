#!/usr/bin/env python3
"""Tile frames from a clip so you can look at them. Usage:
contact_sheet.py CLIP.mp4 OUT.png --fps 2            (every half second)
contact_sheet.py CLIP.mp4 OUT.png --times 3.9 4.2 ... (specific moments, e.g. either side of each join)"""
import argparse, os, tempfile
from common import FFMPEG, run, duration

p = argparse.ArgumentParser()
p.add_argument("clip"); p.add_argument("out")
p.add_argument("--fps", type=float); p.add_argument("--times", nargs="+", type=float)
p.add_argument("--width", type=int, default=130)
a = p.parse_args()
if a.times:
    tmp = tempfile.mkdtemp(); ins = []
    for i, t in enumerate(a.times):
        f = os.path.join(tmp, f"{i:03d}.png")
        run([FFMPEG, "-y", "-v", "error", "-ss", str(t), "-i", a.clip, "-frames:v", "1", "-vf", f"scale={a.width}:-2", f])
        ins += ["-i", f]
    if len(a.times) == 1:   # hstack needs two or more inputs (a one-part edit has no joins)
        run([FFMPEG, "-y", "-v", "error", *ins, a.out])
    else:
        run([FFMPEG, "-y", "-v", "error", *ins, "-filter_complex", f"hstack=inputs={len(a.times)}", a.out])
else:
    fps = a.fps or 1
    n = max(1, round(duration(a.clip) * fps))
    cols = min(12, n); rows = -(-n // cols)          # grid sized to the clip (was always 12x2)
    run([FFMPEG, "-y", "-v", "error", "-i", a.clip, "-vf", f"fps={fps},scale={a.width}:-2,tile={cols}x{rows}",
         "-frames:v", "1", a.out])
print(a.out)
