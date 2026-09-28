#!/usr/bin/env python3
"""The QC gate: every assembled final passes through this before Akhilesh sees it. Nothing else presents a final.
Checks, in order (each row ends pass, repaired or failed):
  1 script    the final's Scribe transcript against the frozen approved script (script_diff.py); the frozen file's
              sha256 is re-checked so an edited "approved" script fails too
  2 lip-sync  lipsync_lag.py on every talking segment of the pre-finish edit (the manifest's "prefinish", or
              assemble.py's <final>_prefinish.mkv: same timing, before the VHS pass and the look, which lower SyncNet's
              confidence and faked a +480 ms reading in the realism test), against the reel's own audio; a line fails if
              any measured segment has a confident window outside -125..+45 ms, or if none of its segments could be
              measured (segments shorter than one 2 s window are covered by a longer segment of the same clip)
  3 face      face_consistency against each character's sheet, frames every 0.5 s through each talking segment
  4 mix       verify_line's audio checks on each line as placed in the mix (the build's dialogue stem, same
              placement, trims and fades): no hard-cut end, no sound after the last word, and the cut to the talking
              shot lands 0-0.40 s before the first word
  5 loudness  integrated loudness within 1 LU of the target, true peak <= -1 dBTP
  6 length    duration within the format's bounds and the build's expected length, 1080x1920, 25 fps, audio as
              long as the picture
Known repairs are applied automatically, once: a constant lip-sync offset (the clip's src_in moves, or a part's
audio_shift_ms in edit.json), a hard-cut or truncated line end
(the line re-ends at its last word; if the file itself stops hot but the word is heard, an 80 ms fade) and a
wrong lead (the cut to the talking shot moves, with the clip's src_in, so the lips stay in sync). The gate
writes them to the manifest's repairs file, runs the manifest's rebuild command, and runs every check again. Any
other failure, or a failure after the rebuild, blocks: the summary names the check, the clip to look at and the fix.
Outputs next to the final: <stem>.qc.json (the stamp: verdict, rows, sha256 of the final and its _phone copy),
<stem>_qc.txt and <stem>_qc.png (the one-screen summary sent with the final). Failure clips go to work/<slug>/qc/.
Only a PASS stamp lets a final out (qc_stamp.py: the SendUserFile hook and put_upload.py check it).

Usage:
  qc_gate.py MANIFEST.json [--no-repair]          run the gate (exit 0 PASS, 1 BLOCKED)
  qc_gate.py bind-transcript FINAL TEXT_FILE      record Scribe's transcript of this exact final (the connector
                                                  route; with ELEVENLABS_API_KEY the gate transcribes by itself)
  qc_gate.py waive FINAL CHECK --by "Akhilesh: <his words>"   accept one failed row (e.g. lipsync:P6) for this
                                                  exact file; only on Akhilesh's or Naveen's say-so
MANIFEST (written by the episode's build; work/sk01/build.py is the example):
  {"slug", "format", "final", "script": "registry/scripts/<slug>.json", "characters": {"pandey": "<sheet.png>"},
   "dialogue_stem": "<wav aligned with the final>", "length": {"min", "max", "expected"}, "loudness": {"target"},
   "repairs_file": "work/<slug>/qc_repairs.json", "rebuild": "<shell command that rebuilds the final>",
   "edit_json": "<optional: assemble.py spec; lines with a 'part' index get audio_shift_ms there>",
   "lines": [{"id", "speaker", "start", "end" (voice as placed, reel s), "source" (the line's wav),
              "cut_in" (reel s the talking shot starts), "segments": [[t0, t1], ...], "part": optional}]}"""
import argparse, datetime, hashlib, json, os, shutil, subprocess, sys, tempfile, wave
import numpy as np

here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from common import FFMPEG, FFPROBE, duration, loudness  # noqa: E402
from qc_stamp import sha256  # noqa: E402

ROOT = os.path.dirname(here)
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
LAG_LO, LAG_HI = -125, 45
MIN_SEG = 2.0                   # shorter talking segments can't hold one lipsync_lag window
LEAD_OK = (0.0, 0.40)           # cut to the talking shot -> first word (s)
LEAD_TARGET = 0.12              # where a lead repair puts the cut (the build's LEAD)
LUFS_TOL, MAX_TP = 1.0, -1.0
SIZE, FPS = (1080, 1920), 25
FACE_EVERY = 0.5


def now():
    return datetime.datetime.now(IST).strftime("%Y-%m-%d %H:%M IST")


def P(path):
    return path if os.path.isabs(path) else os.path.join(ROOT, path)


def rel(path):
    return os.path.relpath(path, ROOT)


def stem(final):
    return os.path.splitext(P(final))[0]


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def audio_id(path):
    """fingerprint of the final's sound (decoded), so a transcript is only reused for the audio it was made from"""
    raw = subprocess.run([FFMPEG, "-v", "error", "-i", P(path), "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True).stdout
    return hashlib.md5(raw).hexdigest()


def row(check, id_, ok, detail, fix=None, repair=None, clip=None):
    return {"check": check, "id": id_, "status": "pass" if ok else "failed", "detail": detail, "fix": fix,
            "repair": repair, "clip": clip}


def evidence(M, final, name, t0, t1):
    """cut the failing stretch of the final into work/<slug>/qc/ so it can be sent and looked at"""
    d = os.path.join(ROOT, "work", M.get("slug", "qc"), "qc"); os.makedirs(d, exist_ok=True)
    out = os.path.join(d, f"{os.path.basename(stem(final))}_{name}.mp4")
    sh([FFMPEG, "-y", "-v", "error", "-ss", f"{max(0, t0):.2f}", "-to", f"{t1:.2f}", "-i", P(final), "-vf",
        "scale=540:-2", "-c:v", "libx264", "-crf", "23", "-c:a", "aac", out])
    return rel(out)


# ---------------------------------------------------------------- 1 script
def transcript_for(final):
    """Scribe text bound to this exact audio: <stem>.scribe.json, or transcribe now if an API key is available"""
    aid = audio_id(final)
    bound = stem(final) + ".scribe.json"
    if os.path.exists(bound):
        doc = json.load(open(bound))
        if doc.get("audio_id") == aid:
            return doc["text"], None
    key = not os.environ.get("QC_NO_TRANSCRIBE") and os.environ.get("ELEVENLABS_API_KEY") or (os.path.exists(os.path.join(ROOT, ".env")) and
                                                   "ELEVENLABS_API_KEY" in open(os.path.join(ROOT, ".env")).read())
    if key:
        out = tempfile.mktemp(suffix=".json")
        r = sh([sys.executable, os.path.join(here, "transcribe.py"), P(final), "--json", out])
        if r.returncode == 0 and os.path.exists(out):
            text = json.load(open(out)).get("text", "")
            json.dump({"final": rel(P(final)), "audio_id": aid, "text": text, "bound_at": now(), "by": "transcribe.py"},
                      open(bound, "w"), ensure_ascii=False, indent=1)
            return text, None
    why = "no Scribe transcript of this exact audio" + (" (the bound one is of an earlier cut)" if os.path.exists(bound) else "")
    return None, why


def check_script(M, final):
    from script_freeze import digest
    doc = json.load(open(P(M["script"])))
    if digest(doc["lines"]) != doc["sha256"]:
        return [row("script", "all", False, f"{M['script']} was edited after approval (sha256 no longer matches)",
                    fix="restore the approved lines, or re-freeze with script_freeze.py --reapprove after approval")]
    text, why = transcript_for(final)
    if text is None:
        return [row("script", "all", False, why,
                    fix=f"transcribe the final with Scribe (connector: creative_create_asset_upload -> put_upload.py -> "
                        f"creative_finalize_asset_upload -> creative_transcribe_audio), save the text, then "
                        f"qc_gate.py bind-transcript {rel(P(final))} <text file>, and rerun the gate")]
    tf = tempfile.mktemp(suffix=".txt"); open(tf, "w").write(text)
    jf = tempfile.mktemp(suffix=".json")
    r = sh([sys.executable, os.path.join(here, "script_diff.py"), P(M["script"]), "--transcript-file", tf, "--json", jf])
    if r.returncode or not os.path.exists(jf):
        return [row("script", "all", False, f"script_diff crashed: {r.stderr[-200:]}", fix="fix the tool")]
    res = json.load(open(jf))
    bad = [l for l in res["lines"] if l["status"] != "OK"]
    if not bad and not res["extra"]:
        return [row("script", "all", True, f"{len(res['lines'])}/{len(res['lines'])} lines match the frozen script "
                    f"{doc['sha256'][:8]} (approved by {doc['approved_by']})")]
    rows = []
    for l in bad:
        what = {"DROPPED": "line not heard", "NUMBER": f"number not heard: {' '.join(l['missing_numbers'])}",
                "CHANGED": f"words missing: {' '.join(l['missing_words'][:8])}"}[l["status"]]
        rows.append(row("script", l["id"], False, f"{l['status']}: {what} (coverage {l['coverage']:.2f})",
                        fix="re-voice or re-place the line so the final says the approved words; if the words were "
                            "changed on purpose, that needs a re-approval first"))
    for e in res["extra"]:
        rows.append(row("script", "extra", False, f"heard but not in the approved script: \"{e[:60]}\"",
                        fix="remove the extra audio (a wrong take or ad-lib), or get the change approved"))
    return rows


# ---------------------------------------------------------------- 2 lip-sync
def prefinish_of(M, final):
    for cand in (M.get("prefinish"), stem(final) + "_prefinish.mkv"):
        if cand and os.path.exists(P(cand)):
            return cand
    return None


def check_lipsync(M, final, work):
    rows = []
    src = prefinish_of(M, final)
    if src is None:
        src = final
        print("[qc_gate] no pre-finish edit found: lip-sync measured on the finished reel", flush=True)
    for ln in M["lines"]:
        segs = [s for s in ln.get("segments", [])]
        if not segs:
            continue
        measured, unsure, fails = [], [], []
        for k, (t0, t1) in enumerate(segs):
            if t1 - t0 < MIN_SEG:
                unsure.append((t0, t1, "shorter than one 2 s window")); continue
            jf = os.path.join(work, f"lag_{ln['id']}_{k}.json")
            r = sh([sys.executable, os.path.join(here, "lipsync_lag.py"), P(src), "--start", f"{t0:.3f}",
                    "--end", f"{t1:.3f}", "--json", jf, "--label", f"{ln['id']}#{k}"])
            if r.returncode or not os.path.exists(jf):
                fails.append((t0, t1, {"verdict": "ERROR", "repair": r.stderr[-200:]})); continue
            L = json.load(open(jf))
            if L["verdict"].startswith("PASS"):
                measured.append((t0, t1, L))
            elif L["verdict"].startswith("FAIL"):
                fails.append((t0, t1, L))
            else:
                unsure.append((t0, t1, L["verdict"][:40]))
        rid = ln["id"]
        if fails:
            t0, t1, L = max(fails, key=lambda f: f[1] - f[0])
            consts = [f[2] for f in fails if f[2].get("pattern") == "constant" and "audio_shift_ms" in f[2]]
            repair = None
            if len(consts) == len(fails):
                shift = int(np.median([c["audio_shift_ms"] for c in consts]))
                repair = {"kind": "offset", "line": rid, "audio_shift_ms": shift, "src_shift_s": round(shift / 1000, 3),
                          "part": ln.get("part")}
            windows = ", ".join(sorted({f"{f[0] + w:.0f} s" for f in fails for w in f[2].get("failing_windows", [])}))
            detail = (f"{L.get('pattern', L['verdict'][:5])}: median {L.get('median_offset_ms', L.get('syncnet', {}).get('offset_ms'))} ms, "
                      f"drift {L.get('drift_ms_per_s')} ms/s, failing windows at {windows or '?'} (segment {t0:.1f}-{t1:.1f} s)")
            rows.append(row("lipsync", rid, False, detail, fix=L.get("repair"), repair=repair,
                            clip=evidence(M, final, f"lipsync_{rid}", t0, t1)))
        elif not measured:
            t0, t1 = segs[0]
            rows.append(row("lipsync", rid, False, "could not be measured: " + "; ".join(u[2] for u in unsure),
                            fix="look at the clip: a small or turned face means weak lips (regenerate from a tighter "
                                "keyframe); if it is fine, Akhilesh can waive this row",
                            clip=evidence(M, final, f"lipsync_{rid}", t0, t1)))
        else:
            offs = [L.get("median_offset_ms", L.get("syncnet", {}).get("offset_ms")) for *_, L in measured]
            offs = [o for o in offs if o is not None]
            note = f", {len(unsure)} short segment(s) covered by the same clip" if unsure else ""
            rows.append(row("lipsync", rid, True, f"offset {int(np.median(offs)) if offs else '?'} ms, drift "
                            f"{measured[0][2].get('drift_ms_per_s')} ms/s over {len(measured)} segment(s){note}"
                            + ("" if src != final else " (on the finished reel)")))
    return rows


# ---------------------------------------------------------------- 3 face
def check_face(M, final):
    from face_consistency import ref_embeddings, target_embeddings, score, PASS
    rows, refs = [], {}
    for ln in M["lines"]:
        sheet = M.get("characters", {}).get(ln.get("speaker"))
        if not ln.get("segments") or not sheet:
            continue
        if ln["speaker"] not in refs:
            refs[ln["speaker"]] = ref_embeddings(P(sheet))
        R = refs[ln["speaker"]]
        # identity is judged on the talking clip itself over the span the edit uses: in the final, captions flying
        # over the face, crash zooms and whip pans drop the score of a face that is plainly him (E5 v4: 0.33-0.47)
        sims, src = [], "final"
        if ln.get("clip") and ln.get("clip_spans") and os.path.exists(P(ln["clip"])):
            src = f"clip {os.path.basename(ln['clip'])}"
            for (c0, c1), (t0, t1) in zip(ln["clip_spans"], ln["segments"]):
                sims += [(t0 + (t - c0), score(R, e)) for t, e in target_embeddings(P(ln["clip"]), FACE_EVERY, c0, c1)]
        else:
            for t0, t1 in ln["segments"]:
                sims += [(t, score(R, e)) for t, e in target_embeddings(P(final), FACE_EVERY, t0, t1)]
        if not sims:
            t0, t1 = ln["segments"][0]
            rows.append(row("face", ln["id"], False, "no face found in the talking shot",
                            fix="look at the clip; if the character is off-screen by design, drop the segment from the manifest",
                            clip=evidence(M, final, f"face_{ln['id']}", t0, t1)))
            continue
        t, worst = min(sims, key=lambda x: x[1])
        ok = worst >= PASS
        rows.append(row("face", ln["id"], ok, f"{ln['speaker']}: worst {worst:.2f} at {t:.1f} s, mean "
                        f"{np.mean([s for _, s in sims]):.2f} ({len(sims)} frames of the {src}; same >= {PASS})",
                        fix=None if ok else "the face drifts from the character sheet here: regenerate the shot from "
                                            "the approved keyframe, or check the right face is in frame",
                        clip=None if ok else evidence(M, final, f"face_{ln['id']}", t - 1, t + 1)))
    return rows


# ---------------------------------------------------------------- 4 mix
def read_mono(path):
    raw = subprocess.run([FFMPEG, "-v", "error", "-i", P(path), "-vn", "-ac", "1", "-ar", "48000", "-f", "s16le", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def write_wav(path, x, sr=48000):
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


def check_mix(M, final, work, script_bad=()):
    from verify_line import audio_checks, END_FAIL_DB
    src = M.get("dialogue_stem") if M.get("dialogue_stem") and os.path.exists(P(M["dialogue_stem"])) else final
    where = "dialogue as placed in the mix" if src != final else "final mix"
    x = read_mono(src); sr = 48000
    rows = []
    starts = sorted(l["start"] for l in M["lines"])
    for ln in M["lines"]:
        s, e = ln["start"], ln["end"]
        nxt = [t for t in starts if t > s + 0.01]
        if nxt and nxt[0] < e:            # the next line starts inside this file's trailing silence
            e = nxt[0] - 0.005
        seg = x[int(s * sr): int(e * sr)]
        wf = os.path.join(work, f"mix_{ln['id']}.wav"); write_wav(wf, seg)
        au = audio_checks(wf)
        if au.get("speech_end") is None:
            rows.append(row("mix", ln["id"], False, f"no speech found at {s:.2f}-{e:.2f} s in the {where}",
                            fix="the line is missing from the mix: check the build's placement")); continue
        problems, fixes, repair = [], [], {}
        # hard-cut end: the line is still at speech level when it stops
        if au["end_drop_db"] < END_FAIL_DB:
            problems.append(f"hard-cut end (only {au['end_drop_db']:.0f} dB down at {e:.2f} s)")
            srcau = audio_checks(P(ln["source"])) if ln.get("source") and os.path.exists(P(ln["source"])) else None
            if srcau and srcau["end_drop_db"] >= END_FAIL_DB and srcau["speech_end"] > e - s - 0.03:
                # the placement cut the line short: re-end it at its last word
                repair.update(voice_end_s=round(srcau["speech_end"] + 0.06, 3), fade_s=0.05)
                fixes.append(f"re-end the line at its last word ({srcau['speech_end']:.2f} s into the source) with a fade")
            elif srcau and ln["id"] not in script_bad:
                # the voice file itself stops at speech level, but Scribe heard the line whole: fade the last 80 ms so
                # the final vowel dies away instead of clicking off (E5 P6 "का": 4 dB down at the file's end)
                repair.update(voice_end_s=round(e - s, 3), fade_s=0.08)
                fixes.append("fade the last 80 ms of the line (the last word is heard in full; the file just stops hot)")
            else:
                fixes.append("the source line itself is cut and a word is missing: re-voice the line, then rebuild")
        if au["tail_sound"]:
            t = au["tail_sound"]
            problems.append(f"sound {t['at']:.2f} s into the line after the last word (breath or noise, {t['len']:.2f} s)")
            fixes.append(f"trim the line at {au['speech_end']:.2f} s and cut 0.25 s after the word; if the talking clip "
                         "mouths the breath, regenerate it from a trimmed track (shot_spec.py build)")
        lead = None
        if ln.get("cut_in") is not None:
            lead = s + au["lead"] - ln["cut_in"]
            if not (LEAD_OK[0] <= lead <= LEAD_OK[1]):
                d = round(lead - LEAD_TARGET, 3)
                problems.append(f"lead {lead:.2f} s from the cut to the first word (want {LEAD_OK[0]:.2f}-{LEAD_OK[1]:.2f})")
                repair["cut_in_delay_s"] = d
                fixes.append(f"cut to the talking shot {abs(d):.2f} s {'later' if d > 0 else 'earlier'} (src_in moves with it)")
        ok = not problems
        detail = (f"end {au['end_drop_db']:.0f} dB down, no tail" + (f", lead {lead:.2f} s" if lead is not None else "")
                  if ok else "; ".join(problems))
        auto = bool(repair) and not au["tail_sound"] and not any("itself is cut" in f for f in fixes)
        rows.append(row("mix", ln["id"], ok, detail, fix="; ".join(fixes) or None,
                        repair=dict(kind="mix", line=ln["id"], **repair) if auto else None,
                        clip=None if ok else evidence(M, final, f"mix_{ln['id']}", s - 0.5, e + 0.8)))
    return rows


# ---------------------------------------------------------------- 5 loudness, 6 length
def check_loudness(M, final):
    target = M.get("loudness", {}).get("target", -14)
    I, tp = loudness(P(final))
    ok = abs(I - target) <= LUFS_TOL and tp <= MAX_TP
    return [row("loudness", "final", ok, f"{I:.1f} LUFS (target {target}), true peak {tp:.1f} dBTP (max {MAX_TP})",
                fix=None if ok else "re-run assemble.py (it levels to target_lufs) and check nothing after it re-encodes the sound")]


def probe(path):
    j = json.loads(sh([FFPROBE, "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate,duration",
                       "-of", "json", P(path)]).stdout)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    n, d = map(int, v["r_frame_rate"].split("/"))
    return (int(v["width"]), int(v["height"])), n / d, float(v.get("duration", 0)), float(a["duration"]) if a else None


def check_length(M, final):
    L = M.get("length", {}); D = duration(P(final))
    size, fps, vd, ad = probe(final)
    problems = []
    if L.get("min") is not None and D < L["min"]:
        problems.append(f"{D:.1f} s is under the {L['min']} s minimum")
    if L.get("max") is not None and D > L["max"]:
        problems.append(f"{D:.1f} s is over the {L['max']} s cap")
    if L.get("expected") is not None and abs(D - L["expected"]) > 0.3:
        problems.append(f"{D:.2f} s but the build planned {L['expected']:.2f} s (a truncated render or mux?)")
    if tuple(size) != SIZE:
        problems.append(f"{size[0]}x{size[1]}, want {SIZE[0]}x{SIZE[1]}")
    if abs(fps - FPS) > 0.01:
        problems.append(f"{fps:.2f} fps, want {FPS}")
    if ad is None:
        problems.append("no audio stream")
    elif abs(ad - vd) > 0.15:
        problems.append(f"audio {ad:.2f} s vs picture {vd:.2f} s")
    ok = not problems
    bounds = f"{L.get('min', '-')}-{L.get('max', '-')} s"
    return [row("length", "final", ok, f"{D:.1f} s (bounds {bounds}), {size[0]}x{size[1]}, {fps:.0f} fps" if ok
                else "; ".join(problems), fix=None if ok else "cut the script or fix the render so the final fits")]


# ---------------------------------------------------------------- the gate
def run_checks(M, work):
    final = M["final"]
    if not os.path.exists(P(final)):
        return [row("final", "file", False, f"{final} does not exist", fix="build it first")]
    rows = []
    for name, fn in (("script", lambda: check_script(M, final)), ("lipsync", lambda: check_lipsync(M, final, work)),
                     ("face", lambda: check_face(M, final)), ("mix", lambda: check_mix(M, final, work, [r["id"] for r in rows if r["check"] == "script" and r["status"] == "failed"])),
                     ("loudness", lambda: check_loudness(M, final)), ("length", lambda: check_length(M, final))):
        print(f"[qc_gate] {name} ...", flush=True)
        try:
            rows += fn()
        except Exception as ex:
            rows.append(row(name, "all", False, f"the check crashed: {str(ex)[-200:]}", fix="fix the tool; a crashed check blocks"))
    return rows


def apply_repairs(M, repairs):
    """write repairs where the build reads them (repairs_file) and, for assemble.py parts, into edit.json"""
    rf = P(M["repairs_file"]) if M.get("repairs_file") else None
    R = json.load(open(rf)) if rf and os.path.exists(rf) else {}
    edit = json.load(open(P(M["edit_json"]))) if M.get("edit_json") else None
    done = []
    for rp in repairs:
        ln = rp["line"]; cur = R.setdefault(ln, {})
        if rp["kind"] == "offset":
            if edit is not None and rp.get("part") is not None:
                part = edit["parts"][rp["part"]]
                part["audio_shift_ms"] = int(part.get("audio_shift_ms", 0)) + rp["audio_shift_ms"]
                done.append(f"{ln}: audio_shift_ms {rp['audio_shift_ms']:+d} on part {rp['part']}")
            else:
                cur["src_shift_s"] = round(cur.get("src_shift_s", 0.0) + rp["src_shift_s"], 3)
                done.append(f"{ln}: clip src_in {rp['src_shift_s']:+.3f} s (lip-sync offset)")
        if "voice_end_s" in rp:
            cur["voice_end_s"] = rp["voice_end_s"]; cur["fade_s"] = rp.get("fade_s", 0.05)
            done.append(f"{ln}: line ends at {rp['voice_end_s']:.2f} s with a {cur['fade_s'] * 1000:.0f} ms fade")
        if "cut_in_delay_s" in rp:
            cur["cut_in_delay_s"] = round(cur.get("cut_in_delay_s", 0.0) + rp["cut_in_delay_s"], 3)
            done.append(f"{ln}: cut to the talking shot {rp['cut_in_delay_s']:+.2f} s")
    if rf:
        json.dump(R, open(rf, "w"), indent=1)
    if edit is not None:
        json.dump(edit, open(P(M["edit_json"]), "w"), indent=1)
    return done


def waived(final_sha, final, r):
    wf = stem(final) + ".qc_waivers.json"
    if not os.path.exists(wf):
        return None
    for w in json.load(open(wf)):
        if w["sha256"] == final_sha and w["check"] == f"{r['check']}:{r['id']}":
            return w["by"]
    return None


def covers(final):
    c = {rel(P(final)): sha256(P(final))}
    phone = stem(final) + "_phone.mp4"
    if os.path.exists(phone) and abs(duration(phone) - duration(P(final))) < 0.15 and \
            os.path.getmtime(phone) >= os.path.getmtime(P(final)) - 1:
        c[rel(phone)] = sha256(phone)
    return c


MARK = {"pass": "PASS", "repaired": "REPAIRED", "failed": "FAILED", "waived": "WAIVED"}
LABEL = {"script": "1 script", "lipsync": "2 lip-sync", "face": "3 face", "mix": "4 mix", "loudness": "5 loudness",
         "length": "6 length", "final": "0 final"}


def summary_text(doc):
    L = [f"QC GATE  {os.path.basename(doc['final'])}  ->  {doc['verdict']}",
         f"{doc['at']}  sha256 {doc['sha256'][:12]}  {doc['length_s']:.1f} s  (gate runs: {len(doc['history'])})", ""]
    last = None
    for r in doc["rows"]:
        lab = LABEL.get(r["check"], r["check"]) if r["check"] != last else ""
        last = r["check"]
        L.append(f"{lab:<11} {r['id']:<6} {MARK[r['status']]:<8} {r['detail']}")
    rep = [r for r in doc["rows"] if r["status"] == "repaired"]
    if rep:
        L += ["", "REPAIRED AUTOMATICALLY (rebuilt and re-checked):"] + [f"  {r['check']} {r['id']}: {r['applied']}" for r in rep]
    wv = [r for r in doc["rows"] if r["status"] == "waived"]
    if wv:
        L += ["", "WAIVED:"] + [f"  {r['check']} {r['id']}: {r['waived_by']}" for r in wv]
    bad = [r for r in doc["rows"] if r["status"] == "failed"]
    if bad:
        L += ["", "BLOCKED. Not sent. For each failure:"]
        for r in bad:
            L.append(f"  {r['check']} {r['id']}: {r['detail']}")
            if r.get("clip"):
                L.append(f"    clip: {r['clip']}")
            if r.get("fix"):
                L.append(f"    fix:  {r['fix']}")
    return "\n".join(L)


def summary_png(doc, path):
    from PIL import Image, ImageDraw, ImageFont
    mono = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    bold = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
    f, fb, fh = ImageFont.truetype(mono, 22), ImageFont.truetype(bold, 22), ImageFont.truetype(bold, 34)
    fs = ImageFont.truetype(mono, 18)
    col = {"pass": (70, 200, 110), "repaired": (240, 180, 40), "failed": (235, 70, 60), "waived": (170, 140, 240)}
    W = 1080; wrap = 56

    def lines_of(r):
        txt, out = r["detail"], []
        while len(txt) > wrap:
            k = txt.rfind(" ", 0, wrap); k = k if k > 20 else wrap
            out.append(txt[:k]); txt = txt[k:].lstrip()
        return out + [txt]
    def wrapped(txt, n=88):
        out = []
        while len(txt) > n:
            k = txt.rfind(" ", 0, n); k = k if k > 20 else n
            out.append(txt[:k]); txt = "    " + txt[k:].lstrip()
        return out + [txt]
    notes = []
    for r in doc["rows"]:
        if r["status"] == "repaired":
            notes += [("repaired", x) for x in wrapped(f"{r['check']} {r['id']}: {r['applied']}")]
        if r["status"] == "failed":
            notes += [("failed", x) for x in wrapped(f"{r['check']} {r['id']}: {r['fix'] or r['detail']}")]
            if r.get("clip"):
                notes += [("failed", x) for x in wrapped(f"    clip: {r['clip']}")]
    body = sum(len(lines_of(r)) for r in doc["rows"])
    Hh = 190 + body * 30 + len(doc["rows"]) * 6 + 40 + (len(notes) * 24 + 30 if notes else 0)
    im = Image.new("RGB", (W, max(Hh, 600)), (18, 20, 28)); d = ImageDraw.Draw(im)
    vcol = (70, 200, 110) if doc["verdict"] == "PASS" else (235, 70, 60)
    d.text((40, 30), "DOORDHAN QC GATE", font=fh, fill=(240, 240, 240))
    d.text((W - 40, 30), doc["verdict"], font=fh, fill=vcol, anchor="ra")
    d.text((40, 84), os.path.basename(doc["final"]), font=fb, fill=(230, 230, 230))
    d.text((40, 116), f"{doc['at']}   {doc['length_s']:.1f} s   sha256 {doc['sha256'][:12]}", font=f, fill=(160, 160, 170))
    y, last = 170, None
    for r in doc["rows"]:
        if r["check"] != last:
            d.line((40, y - 6, W - 40, y - 6), fill=(50, 54, 66)); last = r["check"]
            d.text((40, y), LABEL.get(r["check"], r["check"])[2:], font=fb, fill=(200, 200, 210))
        d.text((200, y), r["id"], font=f, fill=(200, 200, 210))
        d.text((290, y), MARK[r["status"]], font=fb, fill=col[r["status"]])
        yy = y
        for t in lines_of(r):
            d.text((420, yy), t, font=fs, fill=(215, 215, 220)); yy += 26
        y = max(y + 30, yy) + 6
    if notes:
        y += 14; d.line((40, y - 8, W - 40, y - 8), fill=(50, 54, 66))
        fn = ImageFont.truetype(mono, 17)
        for kind, t in notes:
            d.text((40, y), t, font=fn, fill=col[kind]); y += 24
    im.save(path)


def gate(a):
    M = json.load(open(a.manifest))
    final = M["final"]
    work = tempfile.mkdtemp(prefix="qcgate_")
    stamp_path = stem(final) + ".qc.json"
    prev = json.load(open(stamp_path)) if os.path.exists(stamp_path) else {}
    history = prev.get("history", [])
    rows = run_checks(M, work)
    history.append({"at": now(), "sha256": sha256(P(final)) if os.path.exists(P(final)) else None,
                    "failed": [f"{r['check']}:{r['id']}" for r in rows if r["status"] == "failed"]})
    failed = [r for r in rows if r["status"] == "failed"]
    repaired_shas = prev.get("repaired_shas", [])
    cur_sha = history[-1]["sha256"]
    can_repair = (not a.no_repair and failed and all(r.get("repair") for r in failed) and M.get("rebuild")
                  and cur_sha not in repaired_shas)
    applied = {}
    if can_repair:
        print("[qc_gate] every failure has a known repair: applying, rebuilding, re-checking once", flush=True)
        backup = os.path.join(ROOT, "work", M.get("slug", "qc"), "qc"); os.makedirs(backup, exist_ok=True)
        shutil.copy(P(final), os.path.join(backup, os.path.basename(stem(final)) + "_pre_repair.mp4"))
        notes = apply_repairs(M, [r["repair"] for r in failed])
        for r in failed:   # a row may carry two changes (mix: end + lead); keep every note for its line
            applied[(r["check"], r["id"])] = "; ".join(n for n in notes if n.startswith(r["id"] + ":"))
        b = subprocess.run(M["rebuild"], shell=True, cwd=ROOT, capture_output=True, text=True)
        if b.returncode:
            rows.append(row("rebuild", "-", False, f"rebuild failed: {b.stderr[-300:]}", fix="fix the build and rerun the gate"))
        else:
            M = json.load(open(a.manifest))          # the build rewrites timings (cut points move with a lead repair)
            rows2 = run_checks(M, work)
            repaired_shas.append(sha256(P(final)))
            history.append({"at": now(), "sha256": repaired_shas[-1], "after_repair": list(applied.values()),
                            "failed": [f"{r['check']}:{r['id']}" for r in rows2 if r["status"] == "failed"]})
            for r in rows2:
                if r["status"] == "pass" and (r["check"], r["id"]) in applied:
                    r["status"] = "repaired"
                    was = next(x["detail"] for x in failed if (x["check"], x["id"]) == (r["check"], r["id"]))
                    r["applied"] = f"{applied[(r['check'], r['id'])]}  (was: {was}; now: {r['detail']})"
            rows = rows2
    final_sha = sha256(P(final)) if os.path.exists(P(final)) else ""
    if not applied and final_sha in repaired_shas:
        # this file came out of the gate's own repair round (rerun after e.g. binding a fresh transcript)
        for r in rows:
            k = f"{r['check']}:{r['id']}"
            if r["status"] == "pass" and k in prev.get("applied", {}):
                r["status"], r["applied"] = "repaired", prev["applied"][k]
    carried = {f"{r['check']}:{r['id']}": r["applied"] for r in rows if r["status"] == "repaired"}
    for r in rows:
        if r["status"] == "failed":
            by = waived(final_sha, final, r)
            if by:
                r["status"], r["waived_by"] = "waived", by
    verdict = "PASS" if all(r["status"] in ("pass", "repaired", "waived") for r in rows) else "BLOCKED"
    doc = {"final": rel(P(final)), "verdict": verdict, "at": now(), "sha256": final_sha,
           "length_s": duration(P(final)) if final_sha else 0.0, "manifest": rel(os.path.abspath(a.manifest)),
           "covers": covers(final) if verdict == "PASS" else {}, "rows": rows, "history": history,
           "repaired_shas": repaired_shas, "applied": carried}
    json.dump(doc, open(stamp_path, "w"), indent=1, ensure_ascii=False)
    txt = summary_text(doc)
    open(stem(final) + "_qc.txt", "w").write(txt + "\n")
    summary_png(doc, stem(final) + "_qc.png")
    print(txt)
    print(f"\nstamp {rel(stamp_path)}; summary {rel(stem(final) + '_qc.png')}")
    return 0 if verdict == "PASS" else 1


def bind_transcript(a):
    text = open(a.text_file, encoding="utf-8").read().strip()
    out = stem(a.final) + ".scribe.json"
    json.dump({"final": rel(P(a.final)), "audio_id": audio_id(a.final), "text": text, "bound_at": now(),
               "by": "connector (bind-transcript)"}, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"bound {len(text.split())} words to the audio of {rel(P(a.final))} -> {rel(out)}")


def waive(a):
    wf = stem(a.final) + ".qc_waivers.json"
    W = json.load(open(wf)) if os.path.exists(wf) else []
    W.append({"sha256": sha256(P(a.final)), "check": a.check, "by": a.by, "at": now()})
    json.dump(W, open(wf, "w"), indent=1, ensure_ascii=False)
    print(f"waived {a.check} for this exact file ({a.by}); rerun the gate to restamp")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "bind-transcript":
        ap = argparse.ArgumentParser(); ap.add_argument("cmd"); ap.add_argument("final"); ap.add_argument("text_file")
        return bind_transcript(ap.parse_args())
    if len(sys.argv) > 1 and sys.argv[1] == "waive":
        ap = argparse.ArgumentParser(); ap.add_argument("cmd"); ap.add_argument("final"); ap.add_argument("check")
        ap.add_argument("--by", required=True)
        return waive(ap.parse_args())
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest"); ap.add_argument("--no-repair", action="store_true")
    sys.exit(gate(ap.parse_args()))


if __name__ == "__main__":
    main()
