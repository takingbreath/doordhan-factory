#!/usr/bin/env python3
"""Toolchain self-test. Spends no credits. Run from the repo root: python3 pipeline/self_test.py
Builds synthetic audio/video and runs every tool. Prints PASS/FAIL per step."""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from common import FFMPEG, W, H, run, duration, loudness, speech_map

py = sys.executable
T = tempfile.mkdtemp(prefix="df_selftest_")
results = []


def step(name, fn):
    try:
        msg = fn(); results.append(("PASS", name, msg if isinstance(msg, str) else ""))
    except Exception as e:
        results.append(("FAIL", name, str(e)[-400:]))


def tool(*args):
    r = subprocess.run([py, os.path.join(here, args[0]), *args[1:]], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr or r.stdout)
    return r.stdout.strip()


voice = lambda d: f"aevalsrc='0.4*sin(2*PI*180*t)*(0.55+0.45*sin(2*PI*4*t))':s=48000:d={d}"
raw = os.path.join(T, "raw.wav")
def make_raw():
    a, b, s = [os.path.join(T, n) for n in ("a.wav", "b.wav", "s.wav")]
    run([FFMPEG, "-y", "-v", "error", "-f", "lavfi", "-i", voice(2.0), a])
    run([FFMPEG, "-y", "-v", "error", "-f", "lavfi", "-i", voice(1.5), b])
    run([FFMPEG, "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", "0.9", s])
    open(os.path.join(T, "l.txt"), "w").write(f"file '{s}'\nfile '{a}'\nfile '{s}'\nfile '{b}'\nfile '{s}'\n")
    run([FFMPEG, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(T, "l.txt"), raw])
step("synthetic voice line", make_raw)
line = os.path.join(T, "line.wav")
step("prep_line (trim, tighten pauses, level, tempo)", lambda: tool("prep_line.py", raw, line, "--tempo", "1.15"))
def lvl():
    I, _ = loudness(line); assert abs(I + 16) < 1.0, f"loudness {I}"; return f"{I} LUFS"
step("line levelled to -16 LUFS", lvl)
# A real TTS line (Sarika, 3 s). Synthetic tones hid a bug: before 2026-09-25 this line landed at -17.3 LUFS.
real = os.path.join(T, "real.wav")
def real_line():
    tool("prep_line.py", os.path.join(here, "fixtures", "sarika_line_raw.mp3"), real, "--tempo", "1.15")
    I, _ = loudness(real); assert abs(I + 16) < 0.5, f"real line landed at {I} LUFS"; return f"{I} LUFS"
step("prep_line hits -16 LUFS on a real voice line", real_line)
track = os.path.join(T, "track.mp3")
step("make_track (padded, whole seconds)", lambda: tool("make_track.py", track, line, "--min", "4"))
clip = os.path.join(T, "clip.mp4")
step("fake talking clip", lambda: run([FFMPEG, "-y", "-v", "error", "-f", "lavfi", "-i",
     f"testsrc2=s={W}x{H}:r=24:d={duration(track)}", "-i", track, "-shortest", "-c:v", "libx264", "-c:a", "aac", clip]))
step("speech_map", lambda: tool("speech_map.py", clip))
def match():
    out = tool("check_match.py", clip, track); assert out.startswith("PASS"), out; return out
step("check_match", match)
def mismatch():
    rev = os.path.join(T, "rev.mp3")
    run([FFMPEG, "-y", "-v", "error", "-i", track, "-af", "areverse", rev])
    out = tool("check_match.py", clip, rev); assert out.startswith("FAIL"), out; return "reversed track rejected"
step("check_match rejects different audio", mismatch)
step("lipcheck runs", lambda: tool("lipcheck.py", clip, "--box", "190", "350", "100", "80"))
step("headcheck runs", lambda: tool("headcheck.py", clip, "--mouth", "190", "350", "100", "80"))
title, logo = os.path.join(T, "title.png"), os.path.join(T, "logo.png")
def imgs():
    im = Image.new("RGB", (752, 1344), (20, 40, 160)); ImageDraw.Draw(im).ellipse([226, 400, 526, 700], fill=(230, 180, 40)); im.save(title)
    lg = Image.new("RGBA", (400, 136), (0, 0, 0, 0)); ImageDraw.Draw(lg).rectangle([0, 0, 130, 136], fill=(220, 60, 40, 255)); lg.save(logo)
step("test images", imgs)
sting = os.path.join(T, "sting.mp3")
step("test sting", lambda: run([FFMPEG, "-y", "-v", "error", "-f", "lavfi", "-i", "sine=f=440:d=5.7", "-c:a", "libmp3lame", sting]))
mont = os.path.join(T, "montage.mkv")
step("montage (tail of sting kept)", lambda: tool("montage.py", title, sting, mont, "--seconds", "2.5"))
card = os.path.join(T, "card.png")
step("inset card", lambda: tool("inset_card.py", "card", logo, card, "--label", "IPO"))
carded = os.path.join(T, "carded.mp4")
step("inset overlay (explicit position)", lambda: tool("inset_card.py", "overlay", clip, card, carded, "--at", "300", "40"))
edit = os.path.join(T, "edit.json"); final = os.path.join(T, "final.mp4")
def assemble():
    json.dump({"out": final, "parts": [{"file": carded, "start": 0, "end": 3.0}, {"file": mont},
               {"file": clip, "start": 0.0}], "target_lufs": -14}, open(edit, "w"))
    out = tool("assemble.py", edit); I, _ = loudness(final); assert abs(I + 14) < 1.0, f"final loudness {I}"; return out.splitlines()[0]
step("assemble (finish, 1080x1920, -14 LUFS, joins sheet)", assemble)
def assemble_one():
    e1, f1 = os.path.join(T, "edit1.json"), os.path.join(T, "final1.mp4")
    json.dump({"out": f1, "parts": [{"file": clip}]}, open(e1, "w"))
    tool("assemble.py", e1); return f"{duration(f1):.1f}s"
step("assemble a one-part edit (no joins)", assemble_one)
def looks():
    got = []
    for preset in ("broadcast", "vhs", "clean"):
        o = os.path.join(T, f"look_{preset}.mp4")
        tool("look.py", clip, o, "--preset", preset, "--at", "1.0"); got.append(f"{preset} {duration(o):.1f}s")
    return ", ".join(got)
step("look presets render (broadcast, vhs, clean)", looks)
for r in results:
    print(f"{r[0]}  {r[1]}  {r[2][:160]}")
print("\nALL PASS" if all(r[0] == "PASS" for r in results) else "\nSOME STEPS FAILED")
