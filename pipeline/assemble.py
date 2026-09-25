#!/usr/bin/env python3
"""Assemble the final reel from an edit list, apply the old-TV look (look.py), loudness, and 1080x1920 output.
Usage: assemble.py work/<ep>/edit.json
edit.json:
{ "out": "outputs/<ep>/final.mp4",
  "parts": [ {"file": "work/<ep>/A.mp4", "start": 0, "end": 4.06},
             {"file": "work/<ep>/montage.mkv", "lufs": -17},
             {"file": "work/<ep>/C.mp4", "start": 0.1, "end": 13.0} ],
  "target_lufs": -14, "look": "broadcast", "tv_audio": true }
"look": broadcast (default) | vhs | clean (the Sept 2026 finish) | none. "finish": false still means no look.
"tv_audio": mono, 90 Hz-10 kHz, like a TV speaker (default true; the loudness target is measured after it).
Cut points must come from speech_map.py on each generated clip. Never cut before the last word.
Each part with sound is levelled to its "lufs" (default -16, the line level) before joining: video models change
the level of the track we give them (Wan raised one by 3 dB), which undoes the per-line levelling. "lufs": null skips it."""
import json, os, shutil, subprocess, sys, tempfile
from common import FFMPEG, FFPROBE, W, H, FPS, run, duration, loudness
from look import PRESETS, filtergraph, scanline_mask

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
    run(cmd)
    target = p.get("lufs", -16)
    if has_audio and target is not None:
        I0, _ = loudness(out)
        if I0 is not None and I0 > -60 and abs(target - I0) > 0.3:
            pre = out + ".pre.mkv"; shutil.move(out, pre)
            run([FFMPEG, "-y", "-v", "error", "-i", pre, "-c:v", "copy", "-af",
                 f"volume={target - I0:.2f}dB,alimiter=limit=0.84:level=false", "-c:a", "pcm_s16le", out])
            print(f"part {i}: levelled {I0} -> {target} LUFS")
    parts.append(out); t += duration(out); bounds.append(t)
lst = os.path.join(tmp, "list.txt")
open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
joined = os.path.join(tmp, "joined.mkv")
run([FFMPEG, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-crf", "16",
     "-preset", "veryfast", "-c:a", "pcm_s16le", joined])
# Sound: a TV speaker (mono, no deep bass, no air) unless "tv_audio": false; loudness is measured after it.
audio = os.path.join(tmp, "audio.wav")
tv = "pan=mono|c0=0.5*c0+0.5*c1,highpass=f=90,lowpass=f=10000,pan=stereo|c0=c0|c1=c0" if spec.get("tv_audio", True) \
    else "anull"
run([FFMPEG, "-y", "-v", "error", "-i", joined, "-vn", "-af", tv, "-c:a", "pcm_s16le", audio])
I, _ = loudness(audio)
gain = spec.get("target_lufs", -14) - I
look = spec.get("look", "broadcast") if spec.get("finish", True) else "none"
if look == "none":
    graph = "[0:v]scale=1080:1920:flags=lanczos,format=yuv420p[v]"
else:
    graph = filtergraph(look, mask="[2:v]")
mask = scanline_mask(os.path.join(tmp, "scan.png"), (PRESETS.get(look) or {}).get("scan", 0))
os.makedirs(os.path.dirname(os.path.abspath(spec["out"])), exist_ok=True)
run([FFMPEG, "-y", "-v", "error", "-i", joined, "-i", audio, "-loop", "1", "-i", mask,
     "-filter_complex", graph, "-map", "[v]", "-map", "1:a",
     "-af", f"volume={gain:.2f}dB,alimiter=limit=0.84:level=false", "-shortest",
     "-c:v", "libx264", "-crf", "19", "-preset", "veryfast", "-profile:v", "high", "-pix_fmt", "yuv420p",
     "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", spec["out"]])
L = duration(spec["out"]); I2, P2 = loudness(spec["out"])
print(f"{spec['out']}: {L:.1f}s  loudness {I2} LUFS  peak {P2} dBFS  look {look}")
print("joins at:", [round(b, 2) for b in bounds[:-1]])
times = [x for b in bounds[:-1] for x in (max(0, b - 0.15), b + 0.15)] + [max(0, L - 0.2)]
sheet = os.path.splitext(spec["out"])[0] + "_joins.png"
here = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, os.path.join(here, "contact_sheet.py"), spec["out"], sheet, "--times",
                *[f"{x:.2f}" for x in times]], check=True, capture_output=True)
print("joins sheet:", sheet)
