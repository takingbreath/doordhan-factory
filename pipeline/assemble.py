#!/usr/bin/env python3
"""Assemble the final reel from an edit list, apply the 90s finish, loudness, and 1080x1920 output.
Usage: assemble.py work/<ep>/edit.json
edit.json:
{ "out": "outputs/<ep>/final.mp4",
  "parts": [ {"file": "work/<ep>/A.mp4", "start": 0, "end": 4.06},
             {"file": "work/<ep>/montage.mkv"},
             {"file": "work/<ep>/C.mp4", "start": 0.1, "end": 13.0} ],
  "target_lufs": -14, "finish": true }
Cut points must come from speech_map.py on each generated clip. Never cut before the last word."""
import json, os, subprocess, sys, tempfile
from common import FFMPEG, FFPROBE, W, H, FPS, run, duration, loudness

spec = json.load(open(sys.argv[1]))
tmp = tempfile.mkdtemp()
parts, bounds, t = [], [], 0.0
for i, p in enumerate(spec["parts"]):
    f = p["file"]
    start = float(p.get("start", 0)); end = float(p.get("end", duration(f)))
    L = end - start
    has_audio = bool(subprocess.run([FFPROBE, "-v", "error", "-select_streams", "a", "-show_entries",
                                     "stream=index", "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip())
    out = os.path.join(tmp, f"p{i:02d}.mkv")
    vf = f"scale={W}:{H}:flags=lanczos,fps={FPS},format=yuv420p,setsar=1"
    af = f"aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.03,afade=t=out:st={max(0, L-0.05):.3f}:d=0.05"
    cmd = [FFMPEG, "-y", "-v", "error", "-ss", f"{start:.3f}", "-i", f]
    if has_audio:
        cmd += ["-t", f"{L:.3f}", "-vf", vf, "-af", af]
    else:
        cmd += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{L:.3f}", "-vf", vf,
                "-map", "0:v", "-map", "1:a"]
    cmd += ["-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-pix_fmt", "yuv420p",
            "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", out]
    run(cmd); parts.append(out); t += duration(out); bounds.append(t)
lst = os.path.join(tmp, "list.txt")
open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
joined = os.path.join(tmp, "joined.mkv")
run([FFMPEG, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-crf", "16",
     "-preset", "veryfast", "-c:a", "pcm_s16le", joined])
I, _ = loudness(joined)
gain = spec.get("target_lufs", -14) - I
vf = "scale=1080:1920:flags=lanczos"
if spec.get("finish", True):
    vf = "noise=alls=7:allf=t,rgbashift=rh=1:bh=-1,gblur=sigma=0.35," + vf
os.makedirs(os.path.dirname(os.path.abspath(spec["out"])), exist_ok=True)
run([FFMPEG, "-y", "-v", "error", "-i", joined, "-vf", vf, "-af", f"volume={gain:.2f}dB,alimiter=limit=0.84:level=false",
     "-c:v", "libx264", "-crf", "19", "-preset", "veryfast", "-profile:v", "high", "-pix_fmt", "yuv420p",
     "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", spec["out"]])
L = duration(spec["out"]); I2, P2 = loudness(spec["out"])
print(f"{spec['out']}: {L:.1f}s  loudness {I2} LUFS  peak {P2} dBFS")
print("joins at:", [round(b, 2) for b in bounds[:-1]])
times = [x for b in bounds[:-1] for x in (max(0, b - 0.15), b + 0.15)] + [max(0, L - 0.2)]
sheet = os.path.splitext(spec["out"])[0] + "_joins.png"
here = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, os.path.join(here, "contact_sheet.py"), spec["out"], sheet, "--times",
                *[f"{x:.2f}" for x in times]], check=True, capture_output=True)
print("joins sheet:", sheet)
