#!/usr/bin/env python3
"""Build the padded audio track for one generated shot: lead-in, lines with gaps, end hold, rounded up to whole seconds.
Usage: make_track.py OUT.mp3 line1.wav [line2.wav ...] [--lead 0.12] [--gap 0.3] [--hold 0.4] [--min 2]"""
import argparse, math, os, tempfile
from common import FFMPEG, run, duration, silence

p = argparse.ArgumentParser()
p.add_argument("out"); p.add_argument("lines", nargs="+")
p.add_argument("--lead", type=float, default=0.12)
p.add_argument("--gap", type=float, default=0.3)
p.add_argument("--hold", type=float, default=0.4, help="silence after the last word (reaction / smile)")
p.add_argument("--min", type=int, default=2, help="minimum clip length: 2 for Wan 2.7, 4 for Seedance")
a = p.parse_args()

os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
tmp = tempfile.mkdtemp()
lead, gap = os.path.join(tmp, "lead.wav"), os.path.join(tmp, "gap.wav")
silence(lead, a.lead); silence(gap, a.gap)
lst = os.path.join(tmp, "list.txt")
with open(lst, "w") as f:
    f.write(f"file '{lead}'\n")
    for i, ln in enumerate(a.lines):
        if i:
            f.write(f"file '{gap}'\n")
        f.write(f"file '{os.path.abspath(ln)}'\n")
joined = os.path.join(tmp, "joined.wav")
run([FFMPEG, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, joined])
speech_end = duration(joined)
clip = max(a.min, math.ceil(speech_end + a.hold))
run([FFMPEG, "-y", "-v", "error", "-i", joined, "-af", f"apad=whole_dur={clip}", "-t", str(clip),
     "-c:a", "libmp3lame", "-b:a", "256k", "-ar", "48000", a.out])
print(f"{a.out}: clip duration {clip}s (speech ends at {speech_end:.2f}s)")
# Video models bill per whole second, so a hold that spills past a boundary buys a second of silence.
tight = max(a.min, math.ceil(speech_end + 0.2))
if tight < clip:
    print(f"  note: --hold {max(0.2, round(tight - speech_end - 0.01, 2))} would make it {tight}s "
          f"(saves {clip - tight}s of video, about {1.5 * (clip - tight):.1f} credits on Wan 720p)")
