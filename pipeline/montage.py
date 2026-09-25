#!/usr/bin/env python3
"""Opening montage: title-card image with a slow pull-back zoom and CRT flicker, over the LAST N seconds of a sting
(the sting's ending stays intact; it is cut from the beginning).
Usage: montage.py TITLE.png STING.mp3 OUT.mkv [--seconds 2.5] [--lufs -17]"""
import argparse, os, tempfile
from common import FFMPEG, W, H, FPS, run, duration, loudness

p = argparse.ArgumentParser()
p.add_argument("image"); p.add_argument("sting"); p.add_argument("out")
p.add_argument("--seconds", type=float, default=2.5)
p.add_argument("--lufs", type=float, default=-17.0, help="sting level; dialogue sits at about -16")
a = p.parse_args()

os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
start = max(0.0, duration(a.sting) - a.seconds)
tmp = os.path.join(tempfile.mkdtemp(), "s.wav")
run([FFMPEG, "-y", "-v", "error", "-ss", f"{start:.3f}", "-i", a.sting, "-af",
     "aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.15", tmp])
I, _ = loudness(tmp)
frames = int(round(a.seconds * FPS))
vf = (f"scale={W*2}:{H*2},zoompan=z='1.12-0.12*on/{frames}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':"
      f"d={frames}:s={W}x{H}:fps={FPS},eq=brightness='0.015*sin(50*t)',format=yuv420p,setsar=1")
run([FFMPEG, "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS), "-i", a.image, "-i", tmp,
     "-filter_complex", f"[0:v]{vf}[v];[1:a]volume={a.lufs - I:.2f}dB[a]", "-map", "[v]", "-map", "[a]",
     "-t", str(a.seconds), "-c:v", "libx264", "-crf", "16", "-c:a", "pcm_s16le", a.out])
print(f"{a.out}: {duration(a.out):.2f}s (sting from {start:.2f}s to its end)")
