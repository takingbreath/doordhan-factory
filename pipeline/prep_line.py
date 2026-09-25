#!/usr/bin/env python3
"""Clean one raw TTS line: trim edge silence, tighten long pauses, level to -16 LUFS, optional tempo, peak limit.
Usage: prep_line.py RAW.mp3 OUT.wav [--tempo 1.15] [--phone]"""
import argparse, os, shutil, tempfile
from common import FFMPEG, run, loudness, duration, speech_map

p = argparse.ArgumentParser()
p.add_argument("src"); p.add_argument("out")
p.add_argument("--tempo", type=float, default=1.0, help="1.15 for anchors/presenters")
p.add_argument("--target", type=float, default=-16.0, help="LUFS")
p.add_argument("--max-pause", type=float, default=0.3, help="pauses longer than this get shortened")
p.add_argument("--keep-pause", type=float, default=0.24, help="...down to this")
p.add_argument("--phone", action="store_true", help="landline EQ for callers")
a = p.parse_args()

trim = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,"
        "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse")
pause = (f"silenceremove=stop_periods=-1:stop_duration={a.max_pause}:stop_threshold=-40dB:"
         f"stop_silence={a.keep_pause}")
chain = f"aresample=48000,aformat=channel_layouts=mono,{trim},{pause}"
if a.phone:
    chain += (",highpass=f=300,highpass=f=300,lowpass=f=3400,lowpass=f=3400,"
              "acompressor=threshold=0.125:ratio=3:attack=5:release=60:makeup=2")
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
tmp = os.path.join(tempfile.mkdtemp(), "t.wav")
run([FFMPEG, "-y", "-v", "error", "-i", a.src, "-af", chain, tmp])
I, _ = loudness(tmp)
post = f"volume={a.target - I:.2f}dB"
if abs(a.tempo - 1) > 1e-3:
    post += f",atempo={a.tempo}"
post += ",alimiter=limit=0.84:level=false"
run([FFMPEG, "-y", "-v", "error", "-i", tmp, "-af", post, a.out])
# Tempo and the peak limiter pull real speech off target (a TTS line landed at -17.3 instead of -16),
# so measure the finished file and correct the residual.
for _ in range(3):
    I2, _ = loudness(a.out)
    if I2 is None or abs(a.target - I2) < 0.3:
        break
    prev = os.path.join(tempfile.mkdtemp(), "p.wav")
    shutil.move(a.out, prev)
    run([FFMPEG, "-y", "-v", "error", "-i", prev, "-af",
         f"volume={a.target - I2:.2f}dB,alimiter=limit=0.84:level=false", a.out])
sm = speech_map(a.out)
print(f"{a.out}: {duration(a.out):.2f}s  loudness {loudness(a.out)[0]} LUFS  pauses {sm['pauses']}")
