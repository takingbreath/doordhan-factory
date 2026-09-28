#!/usr/bin/env python3
"""Toolchain self-test. Spends no credits. Run from the repo root: python3 pipeline/self_test.py
Builds synthetic audio/video and runs every tool. Prints PASS/FAIL per step."""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw
import numpy as np
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
# A 44.1 kHz line (ElevenLabs connector output) after the 48 kHz lead: before 2026-09-27 the concat read it 8.8% fast,
# so Wan lip-synced to sped-up speech and the mouth ran ahead of the voice in the edit.
def track_441():
    l441, t441 = os.path.join(T, "l441.wav"), os.path.join(T, "t441.mp3")
    run([FFMPEG, "-y", "-v", "error", "-f", "lavfi", "-i", voice(3.0).replace("s=48000", "s=44100"), l441])
    out = tool("make_track.py", t441, l441, "--lead", "0.6", "--hold", "0.1")
    assert "speech ends at 3.60s" in out, out; return out.splitlines()[0]
step("make_track keeps a 44.1 kHz line at its real speed", track_441)
# verify_line: a clean line passes; a spoken tag, a missing number and a tail sound after the last word each fail
def verify_line_checks():
    import json as _j
    v = os.path.join(T, "v.wav"); vt = os.path.join(T, "vt.wav")
    run([FFMPEG, "-y", "-v", "error", "-f", "lavfi", "-i", voice(2.0), "-af", "afade=t=out:st=1.9:d=0.1", v])
    run([FFMPEG, "-y", "-v", "error", "-i", v, "-f", "lavfi", "-t", "0.4", "-i", "anullsrc=r=48000:cl=mono",
         "-f", "lavfi", "-i", voice(0.15), "-filter_complex", "[2]volume=0.3[b];[0][1][b]concat=n=3:v=0:a=1", vt])
    sc = "[flat, brisk] नब्बे लाख का net worth"
    def res(audio, heard):
        r = subprocess.run([py, os.path.join(here, "verify_line.py"), audio, "--script", sc, "--transcript", heard,
                            "--json", os.path.join(T, "vl.json")], capture_output=True, text=True)
        return _j.load(open(os.path.join(T, "vl.json")))["checks"]
    ok = res(v, "90 लाख का net worth")
    assert ok["must_say"]["ok"] and ok["tags_not_spoken"]["ok"] and ok["tail"]["ok"], ok
    assert not res(v, "ब्रिस्क 90 लाख का net worth")["tags_not_spoken"]["ok"], "spoken tag not caught"
    assert not res(v, "80 लाख का net worth")["must_say"]["ok"], "wrong number not caught"
    assert not res(vt, "90 लाख का net worth")["tail"]["ok"], "tail sound not caught"
    return "clean line passes; spoken tag, wrong number and tail sound fail"
step("verify_line", verify_line_checks)
# script_freeze + script_diff: a frozen script can't be silently overwritten; a dropped line and a changed number fail
def script_gate():
    d = os.path.join(T, "scripts"); lines = os.path.join(T, "lines.json")
    open(lines, "w").write('{"P1": "[flat] घर है? गिनो। Loan है? घटाओ।", "P2": "मोटा-मोटा नब्बे लाख।"}')
    tool("script_freeze.py", "t", "--lines", lines, "--approved-by", "test", "--out-dir", d)
    open(lines, "w").write('{"P1": "घर है? गिनो।", "P2": "मोटा-मोटा अस्सी लाख।"}')
    r = subprocess.run([py, os.path.join(here, "script_freeze.py"), "t", "--lines", lines, "--approved-by", "x",
                        "--out-dir", d], capture_output=True, text=True)
    assert r.returncode != 0, "a frozen script was overwritten without --reapprove"
    js = os.path.join(d, "t.json")
    assert "PASS" in tool("script_diff.py", js, "--transcript", "घर है, गिनो। Loan है, घटाओ। मोटा-मोटा 90 लाख।")
    for bad in ("घर है, गिनो। मोटा-मोटा 90 लाख।", "घर है, गिनो। Loan है, घटाओ। मोटा-मोटा 80 लाख।"):
        r = subprocess.run([py, os.path.join(here, "script_diff.py"), js, "--transcript", bad], capture_output=True, text=True)
        assert "FAIL" in r.stdout, r.stdout
    return "frozen script guarded; dropped line and changed number fail"
step("script_freeze + script_diff", script_gate)
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
def lag_repair_shift():
    """assemble.py audio_shift_ms moves a part's audio by the requested amount (the lipsync_lag repair path)"""
    src = os.path.join(T, "shift_src.mp4"); out = os.path.join(T, "shift_out.mp4")
    run([FFMPEG, "-y", "-v", "error", "-f", "lavfi", "-i", f"testsrc2=s={W}x{H}:r=25:d=3", "-f", "lavfi", "-i",
         "aevalsrc='0.5*sin(2*PI*300*t)*between(t,1,1.2)':s=48000:d=3", "-shortest", "-c:v", "libx264", "-c:a", "aac", src])
    spec = os.path.join(T, "shift.json")
    json.dump({"out": out, "parts": [{"file": src, "audio_shift_ms": -200}], "look": "none", "tv_audio": False,
               "target_lufs": -14}, open(spec, "w"))
    tool("assemble.py", spec)
    db = __import__("common").envelope(out, win=0.02)
    onset = float(np.argmax(db > db.max() - 10) * 0.02)
    assert abs(onset - 0.8) < 0.06, f"burst at {onset:.2f}s, expected 0.80s after a -200 ms shift"
    return f"burst moved from 1.00 s to {onset:.2f} s"
step("assemble audio_shift_ms (lip-sync repair)", lag_repair_shift)


def lipsync_model_check():
    """lipsync_lag on a real 3 s talking clip (E5 Pandey): in sync passes; audio delayed 300 ms fails with a shift fix.
    Needs the QC models (pipeline/fetch_models.sh); skipped, not failed, on a machine without them."""
    models = os.path.join(os.path.dirname(here), "assets", "models", "face_landmarker.task")
    if not os.path.exists(models):
        return "SKIPPED: run pipeline/fetch_models.sh to enable"
    fx = os.path.join(here, "fixtures", "pandey_talk_3s.mp4"); bad = os.path.join(T, "late.mp4")
    run([FFMPEG, "-y", "-v", "error", "-i", fx, "-c:v", "copy", "-af", "adelay=300:all=1", "-c:a", "aac", bad])
    good = tool("lipsync_lag.py", fx)
    assert good.split(": ", 1)[1].startswith("PASS"), good
    late = tool("lipsync_lag.py", bad)
    assert "FAIL" in late and "audio_shift_ms" in late, late
    return "in sync passes; 300 ms late audio fails with a shift repair"
step("lipsync_lag (SyncNet / landmarks)", lipsync_model_check)


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
def scoreboard():
    R = os.path.join(T, "sb"); os.makedirs(os.path.join(R, "registry")); os.makedirs(os.path.join(R, "docs"))
    open(os.path.join(R, "docs", "strategy.md"), "w").write("x\n<!-- scoreboard -->\n<!-- /scoreboard -->\n")
    bet = lambda i, m, t, s, mn, mx: dict(id=i, name=i, status="open", applies="every reel", lever="l", thesis="t",
                                          metric=m, baseline=0, target=t, stop=s, min_reels=mn, max_reels=mx)
    json.dump({"bets": [bet("B1", "skip_rate", 45, 58, 3, 6), bet("B2", "watched_pct", 45, 32, 3, 6),
                        bet("B3", "sends_per_1k", 8, 2, 3, 3), bet("B4", "skip_rate", 45, 58, 3, 6)]},
              open(os.path.join(R, "registry", "bets.json"), "w"))
    sb = lambda *a: tool("scoreboard.py", *a, "--root", R, "--now", "2026-10-10 21:30")
    reels = [("R1", "B1;B2;B3", 40, 20), ("R2", "B1;B2;B3", 42, 25), ("R3", "B1;B2;B3", 44, 28), ("R4", "B4", 50, 40), ("R5", "B4", 50, 40)]
    for rid, bets, *_ in reels:
        sb("add-reel", "--id", rid, "--format", "samachar", "--story", "s", "--bets", bets)
    ig = [dict(shortcode="C" + rid, caption=rid, playCount=1000, likeCount=10, commentCount=1, durationSeconds=25,
               timestamp="2026-10-05T14:00:00Z", shares=5, saves=3, avgWatchTimeMs=8000, avgWatchedPct=w, skipRate=sk)
          for rid, _, sk, w in reels]
    f = os.path.join(T, "ig.json"); json.dump({"followersCount": 40, "summary": {"views": 5000}, "reels": ig}, open(f, "w"))
    sb("ingest-ig", f)
    for rid, *_ in reels:
        sb("link", rid, "C" + rid)
    out = sb("report"); sb("write")
    want = {"B1": "TARGET HIT", "B2": "STOP HIT", "B3": "TIME STOP", "B4": "HOLD"}
    got = {b: next((v for v in ("TARGET HIT", "STOP HIT", "TIME STOP", "HOLD") if f"| {b} {b} |" in l and f"**{v}**" in l), None)
           for b in want for l in out.splitlines() if f"| {b} {b} |" in l}
    assert got == want, got
    assert "B1" in open(os.path.join(R, "docs", "strategy.md")).read() and os.path.exists(os.path.join(R, "registry", "performance.md"))
    try:
        sb("add-reel", "--id", "R9", "--format", "x", "--story", "s", "--bets", "B9"); raise AssertionError("unknown bet accepted")
    except RuntimeError:
        pass
    return "target, stop, time stop and hold verdicts; ingest, link, write"
step("scoreboard verdicts", scoreboard)
for r in results:
    print(f"{r[0]}  {r[1]}  {r[2][:160]}")
print("\nALL PASS" if all(r[0] == "PASS" for r in results) else "\nSOME STEPS FAILED")
