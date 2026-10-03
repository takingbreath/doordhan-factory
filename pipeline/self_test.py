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
    try:   # the models can be on disk while this Python lacks the packages (macOS keeps them in a Python 3.11 venv)
        import mediapipe  # noqa: F401
    except Exception:
        return "SKIPPED: this Python has no mediapipe; run the self-test with ~/.venvs/doordhan-qc/bin/python (fetch_models.sh)"
    fx = os.path.join(here, "fixtures", "pandey_talk_3s.mp4"); bad = os.path.join(T, "late.mp4")
    run([FFMPEG, "-y", "-v", "error", "-i", fx, "-c:v", "copy", "-af", "adelay=300:all=1", "-c:a", "aac", bad])
    good = tool("lipsync_lag.py", fx)
    assert good.split(": ", 1)[1].startswith("PASS"), good
    late = tool("lipsync_lag.py", bad)
    assert "FAIL" in late and "audio_shift_ms" in late, late
    return "in sync passes; 300 ms late audio fails with a shift repair"
step("lipsync_lag (SyncNet / landmarks)", lipsync_model_check)


def qc_gate_check():
    """qc_gate.py end to end on a synthetic final (no models, no credits): a line placed with a hard-cut end and a
    late cut is repaired automatically (repairs file, rebuild, re-check); the stamp only covers the passing file;
    the SendUserFile hook and put_upload refuse an unstamped or changed final."""
    root = os.path.dirname(here)
    ep = os.path.join(root, "outputs", "_selftest_qc"); os.makedirs(ep, exist_ok=True)
    try:
        src = os.path.join(T, "qc_line.wav")     # 2 s of "speech" that ends naturally, then 0.3 s of silence
        run([FFMPEG, "-y", "-v", "error", "-f", "lavfi", "-i", voice(2.0), "-af", "afade=t=out:st=1.9:d=0.1,apad=pad_dur=0.3",
             "-ac", "1", src])
        lines = os.path.join(T, "qc_lines.json")
        json.dump([{"id": "L1", "speaker": "anchor", "text": "[calm] yeh ek test line hai"}], open(lines, "w"))
        tool("script_freeze.py", "qctest", "--lines", lines, "--approved-by", "self-test", "--out-dir", T)
        rep, man, fin = os.path.join(T, "qc_repairs.json"), os.path.join(T, "qc_manifest.json"), os.path.join(ep, "qctest.mp4")
        build = os.path.join(T, "qc_build.py")
        open(build, "w").write(f"""
import json, os, subprocess, numpy as np, wave
R = json.load(open({rep!r})).get("L1", {{}}) if os.path.exists({rep!r}) else {{}}
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", {src!r}, "-f", "s16le", "-ac", "1", "-ar", "48000", "-"], capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
end = R.get("voice_end_s", 1.3)                     # the fault: the line is cut mid-speech at 1.3 s (a loud peak)
x = x[: int(end * 48000)].copy()
if "voice_end_s" in R:
    x[-2400:] *= np.linspace(1, 0, 2400)
S = 1.0; cut = 0.3 + R.get("cut_in_delay_s", 0.0)   # the fault: the cut lands 0.7 s before the first word
bus = np.zeros(4 * 48000, np.float32); bus[int(S * 48000): int(S * 48000) + len(x)] = x
for path in ({os.path.join(T, 'qc_dialogue.wav')!r}, {os.path.join(T, 'qc_mix.wav')!r}):
    w = wave.open(path, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(48000)
    w.writeframes((bus * 32767).astype(np.int16).tobytes()); w.close()
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "testsrc2=s=720x1280:r=25:d=4", "-i", {os.path.join(T, 'qc_mix.wav')!r},
                "-shortest", "-c:v", "libx264", "-c:a", "pcm_s16le", {os.path.join(T, 'qc_raw.mkv')!r}], check=True)
json.dump({{"out": {fin!r}, "parts": [{{"file": {os.path.join(T, 'qc_raw.mkv')!r}}}], "look": "none", "tv_audio": False, "target_lufs": -14}},
          open({os.path.join(T, 'qc_edit.json')!r}, "w"))
json.dump({{"slug": "_selftest", "final": {fin!r}, "script": {os.path.join(T, 'qctest.json')!r},
           "dialogue_stem": {os.path.join(T, 'qc_dialogue.wav')!r}, "length": {{"min": 1, "max": 10, "expected": 4.0}},
           "loudness": {{"target": -14}}, "repairs_file": {rep!r},
           "rebuild": "{py} {build} && {py} {os.path.join(here, 'assemble.py')} {os.path.join(T, 'qc_edit.json')}",
           "lines": [{{"id": "L1", "speaker": "anchor", "start": S, "end": round(S + len(x) / 48000, 3),
                      "source": {src!r}, "cut_in": round(cut, 3)}}]}}, open({man!r}, "w"))
""")
        run([py, build]); tool("assemble.py", os.path.join(T, "qc_edit.json"))
        txt = os.path.join(T, "qc_heard.txt"); open(txt, "w").write("yeh ek test line hai")
        tool("qc_gate.py", "bind-transcript", fin, txt)
        env = dict(os.environ, QC_NO_TRANSCRIBE="1")
        gate = lambda: subprocess.run([py, os.path.join(here, "qc_gate.py"), man], capture_output=True, text=True, env=env)
        r1 = gate(); st = json.load(open(os.path.splitext(fin)[0] + ".qc.json"))
        R = json.load(open(rep))["L1"]
        assert "voice_end_s" in R and abs(R["cut_in_delay_s"] - 0.58) < 0.05, f"repairs written: {R}\n{r1.stdout[-800:]}"
        # the repair changed the sound, so the transcript bound to the old cut no longer counts: blocked until re-bound
        bad = [f"{x['check']}:{x['status']}" for x in st["rows"] if x["status"] == "failed"]
        assert r1.returncode == 1 and bad == ["script:failed"], f"after the repair round: {bad}\n{r1.stdout[-1200:]}"
        hook = lambda: subprocess.run([py, os.path.join(here, "hooks", "require_qc_stamp.py")], capture_output=True, text=True,
                                      input=json.dumps({"tool_name": "SendUserFile", "tool_input": {"files": [fin]}}))
        assert hook().returncode == 2, "hook let a blocked final through"
        tool("qc_gate.py", "bind-transcript", fin, txt)
        r2 = gate(); st = json.load(open(os.path.splitext(fin)[0] + ".qc.json"))
        mix = next(x for x in st["rows"] if x["check"] == "mix")
        assert r2.returncode == 0 and st["verdict"] == "PASS" and mix["status"] == "repaired", r2.stdout[-1200:]
        assert hook().returncode == 0, "hook blocked a stamped final: " + hook().stderr
        assert os.path.exists(os.path.splitext(fin)[0] + "_qc.png"), "no summary image"
        open(fin, "ab").write(b"\0")                   # any change after the gate voids the stamp
        assert hook().returncode == 2, "hook accepted a final changed after the gate"
        up = subprocess.run([py, os.path.join(here, "put_upload.py"), fin, "http://127.0.0.1:9/x", "video/mp4"],
                            capture_output=True, text=True)
        assert up.returncode and "QC gate" in up.stderr, "put_upload sent an unstamped final"
        return "hard-cut end + late cut repaired, rebuilt, re-checked; stamp, hook and put_upload enforce it"
    finally:
        import shutil; shutil.rmtree(ep, ignore_errors=True); shutil.rmtree(os.path.join(root, "work", "_selftest"), ignore_errors=True)
step("qc_gate (hard gate, auto-repair once, stamp + hook)", qc_gate_check)


def continuity_rules():
    """shot_spec continuity and eyeline rules (no credits): an off-frame look is refused; a reach in a talking shot is
    refused; an in-frame look asks for an end image and puts end_image in the Wan params; a talking prompt carries the
    one-blink, one-eye-shift rule; a silent insert has no audio"""
    line = os.path.join(T, "cont_line.wav")
    run([FFMPEG, "-y", "-v", "error", "-f", "lavfi", "-i", voice(2.0), "-af", "afade=t=out:st=1.8:d=0.2", "-ac", "1", line])
    out = os.path.join(T, "cont")
    ss = lambda *a: subprocess.run([py, os.path.join(here, "shot_spec.py"), "build", *a, "--out", out], capture_output=True, text=True)
    r = ss("--line", line, "--id", "A", "--keyframe", "k", "--look-at", "the cat", "--target-side", "left")
    assert r.returncode and "is a cut" in (r.stderr + r.stdout), r.stderr[-300:]
    r = ss("--line", line, "--id", "B", "--keyframe", "k", "--reach-for", "the phone", "--target-in-frame")
    assert r.returncode and "no object handling" in (r.stderr + r.stdout), r.stderr[-300:]
    r = ss("--line", line, "--id", "C", "--keyframe", "k", "--look-at", "the cat", "--target-side", "left", "--target-in-frame")
    assert r.returncode == 0, r.stderr[-300:]
    spec = json.load(open(os.path.join(out, "C.json")))
    assert spec["end_image_request"] and any(m["role"] == "end_image" for m in spec["params"]["medias"]), spec
    r = ss("--line", line, "--id", "D", "--keyframe", "k")
    p = json.load(open(os.path.join(out, "D.json")))["params"]["prompt"]
    assert "exactly one blink and one small eye shift" in p and "No objects are handled" in p, p
    r = ss("--silent", "3", "--id", "E", "--keyframe", "k", "--reach-for", "the phone", "--target-in-frame", "--target-side", "right")
    e = json.load(open(os.path.join(out, "E.json")))
    assert r.returncode == 0 and not any(m["role"] == "audio_references" for m in e["params"]["medias"]) and e["end_image_request"], e
    return "off-frame look and talking-shot reach refused; in-frame look gets an end image; eye rule in the prompt; silent insert"
step("shot_spec continuity + eyeline rules", continuity_rules)


def assemble():
    json.dump({"out": final, "parts": [{"file": carded, "start": 0, "end": 3.0}, {"file": mont},
               {"file": clip, "start": 0.0}], "target_lufs": -14}, open(edit, "w"))
    out = tool("assemble.py", edit); I, _ = loudness(final); assert abs(I + 14) < 1.0, f"final loudness {I}"
    assert os.path.exists(os.path.splitext(final)[0] + "_prefinish.mkv"), "no pre-finish edit for the lip-sync gate"
    assert "vhs motion at 0.65" in out and "ambience 'office'" in out, out
    return out.splitlines()[0] + "; vhs motion, voice room, ambience, pre-finish"
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
def voice_reference_rules():
    """voice_reference's line, pause and rhythm rules on made-up Scribe words (no network): a 0.3 s gap is a marked
    pause, a 0.7 s gap and a change of speaker each start a line, words stay as given"""
    import voice_reference as vr
    w = lambda t, s, e, sp: {"text": t, "type": "word", "start": s, "end": e, "speaker_id": sp}
    ws = [w("Haan", 0.0, 0.3, "speaker_0"), w("bhai.", 0.4, 0.7, "speaker_0"), w("Dekho", 1.0, 1.3, "speaker_0"),
          w("ye", 2.0, 2.2, "speaker_0"), w("kya", 2.25, 2.5, "speaker_1"), w("hai?", 2.6, 3.0, "speaker_1")]
    got = vr.full_lines(ws)
    assert got == ["speaker_0: Haan bhai. (0.3 s) Dekho (0.7 s)", "speaker_0: ye", "speaker_1: kya hai?"], got
    sp = {"text": " ", "type": "spacing"}
    got = vr.text_lines({"words": [t for x in ws for t in (x, sp)]})
    assert got == ["Haan bhai.", "Dekho ye kya hai?"], got
    md = vr.rhythm([("clip one.mp3", {"words": ws}, ["speaker_0"])])
    assert md.splitlines()[0] == "Rhythm measured from: clip one.mp3 (only speaker_0).", md
    for want in ("Words per second: 2.67 (4 words over 2 s", "Average words per sentence: 2.0",
                 "Pauses per 10 words: 5.0 (2 pauses)", "Average pause length: 0.50 s", "2 sentences"):
        assert want in md, (want, md)
    assert vr.slug("3 साल, 6 Charts!") == "3-6-charts" and vr.slug("साल") == "clip"
    return "pause marks, line breaks, sentences per line, rhythm numbers, ASCII file names"
step("voice_reference line, pause and rhythm rules", voice_reference_rules)
# script_lint: fixtures are copies of looptest3's r1-script.md, each changed only where its case needs it; they run
# against the live format file and voice cards, in a temp copy so the lint files land there
import shutil
LINT_DIR = os.path.join(T, "script_lint")
shutil.copytree(os.path.join(here, "fixtures", "script_lint"), LINT_DIR)
LINT_FORMAT = os.path.join(os.path.dirname(here), "formats", "sahayata_kendra.md")
def lint(*names, fmt=LINT_FORMAT):
    paths = [os.path.join(LINT_DIR, n) for n in names]
    r = subprocess.run([py, os.path.join(here, "script_lint.py"), fmt, *paths], capture_output=True, text=True)
    stem = os.path.splitext(paths[0])[0]
    read = lambda p: open(p, encoding="utf-8").read() if os.path.exists(p) else ""
    fails_md, report_md = read(stem + "-lint-fails.md"), read(stem + "-lint-report.md")
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in fails_md.splitlines()
            if l.startswith("| ") and not l.startswith("| Check ")]
    return r.returncode, r.stdout + r.stderr, fails_md, report_md, rows
def lint_case(names, code, fail_checks):
    def run_case():
        rc, out, fails_md, report_md, rows = lint(*names)
        assert rc == code, (rc, out)
        assert [row[0] for row in rows] == fail_checks, rows
        assert fails_md.rstrip().splitlines()[-1] == ("VERDICT: FAIL" if fail_checks else "VERDICT: PASS"), fails_md
        return f"exit {rc}, fails: {', '.join(fail_checks) or 'none'}"
    return run_case
def lint_r1():
    rc, out, fails_md, report_md, rows = lint("r1-script.md")
    assert rc == 1 and [r[0] for r in rows] == ["opening_order"] and rows[0][2] == "1", rows
    for want in ("| Words | 75 |", "| Estimated length | 35.8 s |", "| Words in the first spoken line | 20 |",
                 "| Numbers in the reel | 6 |", "| Most numbers in one line | 3 |", "| Silent beats | 0 |"):
        assert want in report_md, (want, report_md)
    return "FAIL on opening_order only; 75 words, 35.8 s at 2.5 w/s, 20 in line 1, 6 numbers, 3 in one line, 0 beats"
step("script_lint a: r1 as written", lint_r1)
for name, files, code, checks in [
        ("b: Pandey first, Billu's beat last", ["b-fixed-opening.md"], 0, []),
        ("c: 'Main' in Pandey's line", ["c-main.md"], 1, ["never"]),
        ("d: 'Main' inside quotes", ["d-main-quoted.md"], 0, []),
        ("e: ', ka?'", ["e-ka-comma.md"], 1, ["ka_comma"]),
        ("f: kaahe twice", ["f-kaahe-twice.md"], 1, ["kaahe"]),
        ("g: 'Comment karo.'", ["g-comment-karo.md"], 1, ["banned_phrases"]),
        ("h: two silent beats", ["h-two-beats.md"], 1, ["silent_beats_max"]),
        ("j: a NARRATOR line", ["j-narrator.md"], 1, ["cast"]),
        ("k: alternate differs only in Pandey's first line", ["b-fixed-opening.md", "k-alt-first-line.md"], 0, [])]:
    step(f"script_lint {name}", lint_case(files, code, checks))
def lint_billu_speaks():
    """since loop v0.3 the silent row only reports: Billu speaking is in the report, never a fail"""
    rc, out, fails_md, report_md, rows = lint("i-billu-speaks.md")
    assert rc == 0 and rows == [], (rc, rows)
    assert "| silent | i-billu-speaks.md | 15 | **BILLU**: Meow |" in report_md, report_md
    return "exit 0, no fails; reported on line 15"
step("script_lint i: Billu speaks (reported)", lint_billu_speaks)
def lint_versions_differ():
    rc, out, fails_md, report_md, rows = lint("b-fixed-opening.md", "k-alt-later-line.md")
    assert rc == 1 and [r[0] for r in rows] == ["versions_match"], rows
    assert rows[0][1] == "k-alt-later-line.md" and rows[0][2] == "13" and "bees hazaar" in rows[0][3], rows
    return "FAIL on versions_match, naming line 13"
step("script_lint k: alternate with a later line changed", lint_versions_differ)
def lint_table_error():
    bad = os.path.join(LINT_DIR, "format-misspelled-row.md")
    text = open(LINT_FORMAT, encoding="utf-8").read()
    assert text.count("| numbers_reel |") == 1
    open(bad, "w", encoding="utf-8").write(text.replace("| numbers_reel |", "| numbers_rell |"))
    lint("b-fixed-opening.md")  # leaves a passing verdict on disk, which the error run must overwrite
    rc, out, fails_md, report_md, rows = lint("b-fixed-opening.md", fmt=bad)
    assert rc == 2, (rc, out)
    assert "numbers_rell" in out and "numbers_reel" in out, out
    for where in (out, fails_md, report_md):
        assert "PASS" not in where, where
    return "exit 2, the bad row and the missing one named, no verdict anywhere"
step("script_lint l: a misspelled format row", lint_table_error)
def voice_cut_matching():
    """voice_cut's take check (no network): a script word and Scribe's other-script spelling of it count as the same
    word, a dropped word is found and named, and the voice step's Bash guard lets voice_cut through and nothing else"""
    import voice_cut as vc
    script = "[flat, brisk] Dollar का rate कोई तय नहीं करता। RBI भी इसी market में एक खिलाड़ी है।"
    assert vc.similarity(script, "डॉलर का रेट कोई तय नहीं करता. RBI भी इसी मार्केट में एक खिलाड़ी है") > 0.95
    dropped = "Dollar का rate कोई तय नहीं करता। RBI भी इसी market में खिलाड़ी है।"
    assert vc.similarity(script, dropped) < 1.0
    assert ("एक", "(nothing)") in vc.differences(script, dropped), vc.differences(script, dropped)
    hook = os.path.join(here, "hooks", "voice_only.py")
    def allowed(cmd):
        r = subprocess.run([py, hook], input=json.dumps({"tool_input": {"command": cmd}}), capture_output=True, text=True)
        return r.returncode == 0
    assert allowed("python3 pipeline/voice_cut.py work/s/loop/audio/w1-1/lines.json work/s/loop/audio/w1-1 --retake P2")
    for cmd in ("python3 pipeline/voice_cut.py work/s/a.json work/s; rm -rf work", "python3 pipeline/tts_elevenlabs.py --check",
                "python3 pipeline/voice_cut.py work/../x.json work/s", "ls"):
        assert not allowed(cmd), cmd
    return "cross-script word match, dropped word named, Bash guard"
step("voice_cut take check and Bash guard", voice_cut_matching)
def reel_script_stubs():
    """the script loop's workflow (.claude/workflows/reel-script.js) end to end with fake agents: every read exists
    when it is read, and the run folder holds the expected files (pipeline/stub_reel_script.mjs)"""
    node = shutil.which("node")
    if not node:
        return "skipped: no node on this machine"
    r = subprocess.run([node, os.path.join(here, "stub_reel_script.mjs"), "--quiet"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    return f"{r.stdout.count('PASS ')} stub runs pass"
step("reel-script workflow stub runs", reel_script_stubs)
for r in results:
    print(f"{r[0]}  {r[1]}  {r[2][:160]}")
print("\nALL PASS" if all(r[0] == "PASS" for r in results) else "\nSOME STEPS FAILED")
