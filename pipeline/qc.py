#!/usr/bin/env python3
"""All the checks for one generated talking shot, in one go, written to a notes file you can keep with the shot.
Usage: qc.py CLIP.mp4 --track TRACK.mp3 --box X Y W H [--expect "script line"] [--out qc.md]
  --box: mouth box in the 480x854 analysis frame (lipcheck.py --face-crop helps you find it)
Runs: format probe, speech_map, check_match, lipcheck, transcript vs script (if an ElevenLabs key is set),
loudness, and a 4 fps contact sheet. It does not replace looking at the sheet yourself."""
import argparse, json, os, subprocess, sys
from common import FFPROBE, loudness

here = os.path.dirname(os.path.abspath(__file__))
p = argparse.ArgumentParser()
p.add_argument("clip"); p.add_argument("--track"); p.add_argument("--box", nargs=4, type=int)
p.add_argument("--expect"); p.add_argument("--out")
a = p.parse_args()
out = a.out or os.path.splitext(a.clip)[0] + "_qc.md"
sheet = os.path.splitext(out)[0] + "_sheet.png"


def tool(*args):
    r = subprocess.run([sys.executable, os.path.join(here, args[0]), *args[1:]], capture_output=True, text=True)
    return (r.stdout.strip() or r.stderr.strip().splitlines()[-1] if (r.stdout or r.stderr) else "(no output)")


probe = json.loads(subprocess.run([FFPROBE, "-v", "error", "-show_entries",
                                   "stream=codec_type,width,height,r_frame_rate:format=duration", "-of", "json",
                                   a.clip], capture_output=True, text=True).stdout)
v = next((s for s in probe["streams"] if s["codec_type"] == "video"), {})
has_audio = any(s["codec_type"] == "audio" for s in probe["streams"])
rows = [("format", f"{v.get('width')}x{v.get('height')} @ {v.get('r_frame_rate')} fps, "
                   f"{float(probe['format']['duration']):.2f}s, audio {'yes' if has_audio else 'NO'}"),
        ("speech_map", tool("speech_map.py", a.clip).split(" ", 1)[-1])]
if a.track:
    rows.append(("check_match", tool("check_match.py", a.clip, a.track).split("  (")[0]))
if a.box:
    rows.append(("lipcheck", tool("lipcheck.py", a.clip, "--box", *map(str, a.box))))
if a.expect:
    rows.append(("transcript", tool("transcribe.py", a.clip, "--expect", a.expect).replace("\n", " | ")))
I, P = loudness(a.clip)
rows.append(("loudness", f"{I} LUFS, peak {P} dBFS (assemble.py levels each part to -16 before the mix)"))
tool("contact_sheet.py", a.clip, sheet, "--fps", "4", "--width", "120")
rows.append(("contact sheet", sheet + "  <- look at it: face, hands, text, logo, last frame"))
text = f"# QC: {a.clip}\n\n" + "\n".join(f"- **{k}**: {v}" for k, v in rows) + "\n"
open(out, "w", encoding="utf-8").write(text)
print(text + f"\nwritten to {out}")
