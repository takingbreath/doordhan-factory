#!/usr/bin/env python3
"""Talking-shot specs with our defaults applied, and the accept / retry-once / ask decision after generation.

build: one voice line -> one or more Wan 2.7 shot specs (JSON with the generate_video params, the track to upload and
       the QC to run). Defaults, each from something that went wrong:
         - trim the line at its last word when verify_line finds a sound after it (E5 "Ghatao": a breath read as a
           half-open mouth before the cut)
         - lead-in 0.5 s of silence before the first word (Wan's first second barely moves the lips; E5 "Ghar hai")
         - still start: the prompt opens with the mouth closed and still until the voice begins
         - duration headroom: >= 0.3 s after the last word, rounded up to whole seconds (billing)
         - 6 s cap: longer lines are split at the pause nearest the middle, because Wan drifts about -8 ms/s
           (median over 29 clips, E3-E6; E5 T4v2, 11 s, crossed -125 ms at 9 s). --allow-long when lipsync_lag has passed
           on longer shots of this character and framing.
continuity (2026-09-29):
         - chaining: consecutive shots of the same character in the same set and framing (--chain-from the previous
           shot's spec) start from the previous clip's last clean frame (mouth closed, eyes open, preflight pose and
           size limits, identity vs the sheet) instead of the set keyframe. No clean frame -> the keyframe. judge runs
           face_consistency on every chained shot; a FAIL resets the shot to the keyframe (RESET_TO_KEYFRAME).
         - looks and reaches (--look-at / --reach-for TARGET --target-side left|right|down): the target must be in the
           frame (--target-in-frame), or the builder refuses: a look at something off-frame is a cut (he looks
           off-camera, then a cutaway of the object). In frame -> the spec carries an end-image request (the start
           frame with his eyes or hand on the target, target visible), and the Wan params get it as end_image.
         - a change of position (--end-pose "...") needs both a start and an end image.
         After an end image is made: shot_spec.py endcheck SPEC END.png (identity, mouth, gaze toward the target).
judge: after the clip is downloaded: runs lipsync_lag on it (own audio) and decides
         PASS                  -> accept
         constant offset        -> accept, with the audio_shift_ms for assembly (no regeneration)
         drift / weak lips / other FAIL -> one automatic retry (a split for drift on a long line, a stronger
                                   articulation prompt otherwise); after that -> ASK (a summary for Akhilesh)
Usage:
  shot_spec.py build --line P2.wav --id P2 --keyframe 93b0322a-... --character pandey \
       --acting "small nod on each 'gino'..." [--prompt-base "..."] [--out work/<slug>/specs] [--allow-long]
  shot_spec.py build ... --set kendra --framing two_shot --chain-from specs/P5.json      (chain when it applies)
  shot_spec.py build ... --look-at "the ginger cat" --target-side left --target-in-frame
  shot_spec.py endcheck SPEC.json END.png
  shot_spec.py judge SPEC.json CLIP.mp4"""
import argparse, json, math, os, subprocess, sys

here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from common import FFMPEG, duration, speech_map  # noqa: E402

LEAD = 0.5; HEADROOM = 0.3; MAX_TALK = 6.0
DECLINED_PRESET = "24bae836-2c4a-48e0-89b6-49fcc0b21612"
STILL_START = ("The person begins completely still and silent with the mouth closed, and starts speaking only when "
               "the voice begins.")
ARTICULATE = ("The jaw and lower lip move clearly with every syllable in exact sync with the provided audio, from the "
              "very first word.")
BASES = {
    "pandey": ("The man from the start image, a dry, tired government helpline clerk, speaks in Hindi. Deadpan but "
               "alive and human: heavy-lidded bored eyes, a faint dry smirk under his moustache."),
    "sarika": ("The news anchor from the start image reads the news in Hindi. She is a poised professional newsreader: "
               "head steady and level, shoulders still, only a small natural nod on a stressed word, expression carried "
               "by her eyes, a faint knowing smile at the end. No head tilting, no bobbing, no hair movement."),
    "gupta": ("The field news correspondent from the start image reports to camera in Hindi, head steady, "
              "a small natural nod on a stressed word."),
}
# eyeline rule (2026-09-29): talking shots are straight to camera or eyes down, with exactly one blink and one small
# eye shift, and no objects handled; a look at something is either a cut or the thing is in frame with an end image
EYES_TALK = ("Eyes straight to the camera, or down; exactly one blink and one small eye shift during the line, nothing "
             "more. No objects are handled.")
EYES_LOOK = "His eyes stay on {t}, which is in the frame; exactly one blink, nothing more. No objects are handled."
TAIL = "Small, subtle, natural movements only. Locked-off camera. Keep the exact analog look of the start image; no new text, no subtitles."
SHEETS = {"pandey": "assets/characters/pandey_sheet_v2.jpg"}   # identity reference per character (repo-relative, tracked)
END_IMAGE_MODEL = {"sarika": "seedream_v4_5"}                 # GPT Image blocks her wardrobe; everyone else gpt_image_2_5
ROOT = os.path.dirname(here)


def clean_frame(clip, character, out_png, search=3.0, step=0.08):
    """the last frame of clip (searching back `search` s) with the mouth closed, eyes open, pose and size inside the
    preflight limits and identity >= PASS vs the character sheet. Returns (path, info) or (None, why)."""
    from face import load_rgb, analyse, mouth_open, embed
    from preflight_keyframe import FACE_H, YAW, PITCH, ROLL, JAW_OPEN
    D = duration(clip); why = []
    ref = None
    sheet = os.path.join(ROOT, SHEETS[character]) if character in SHEETS else None
    if sheet and os.path.exists(sheet):
        from face_consistency import ref_embeddings, score, PASS
        ref = ref_embeddings(sheet)
    t = D - 0.12
    while t > max(0.0, D - search):
        rgb = load_rgb(clip, t=t, width=None); f = analyse(rgb)
        if f:
            f = f[0]; H = rgb.shape[0]; ps = f["pose"]; b = f["blend"]
            lid = (b.get("eyeBlinkLeft", 0) + b.get("eyeBlinkRight", 0)) / 2
            checks = {"mouth": mouth_open(f) < 0.03 and b.get("jawOpen", 0) < JAW_OPEN[0],
                      "eyes": lid < 0.45, "size": (f["box"][3] - f["box"][1]) / H >= FACE_H[1],
                      "pose": abs(ps["yaw"]) <= YAW[0] + 10 and abs(ps["pitch"]) <= PITCH[0] and abs(ps["roll"]) <= ROLL[0]}
            if ref is not None and all(checks.values()):
                checks["identity"] = score(ref, embed(rgb, f)) >= PASS
            if all(checks.values()):
                from PIL import Image
                Image.fromarray(rgb).save(out_png)
                return out_png, {"t": round(t, 2), "mouth_open": round(mouth_open(f), 3), "lid": round(lid, 2),
                                 "pose": {k: round(v, 1) for k, v in ps.items()}}
            why.append(f"{t:.2f}s: " + ",".join(k for k, v in checks.items() if not v))
        t -= step
    return None, "no clean frame in the last %.1f s (%s)" % (search, "; ".join(why[:4]))


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr[-800:])
    return r.stdout


def split_points(path, max_len):
    """cut times at pauses so every part is <= max_len of speech (pause nearest each ideal cut)"""
    sm = speech_map(path)
    start, end = sm["start"] or 0, sm["end"] or duration(path)
    if end - start <= max_len:
        return [(0.0, duration(path))]
    n = math.ceil((end - start) / max_len)
    mids = [(a + b) / 2 for a, b in sm["pauses"]]
    cuts = []
    for k in range(1, n):
        ideal = start + k * (end - start) / n
        cand = [m for m in mids if all(abs(m - c) > 1.0 for c in cuts)]
        if not cand:
            break
        cuts.append(min(cand, key=lambda m: abs(m - ideal)))
    cuts = sorted(cuts)
    edges = [0.0] + cuts + [duration(path)]
    return list(zip(edges[:-1], edges[1:]))


def build(a):
    os.makedirs(a.out, exist_ok=True)
    if not a.line and not a.silent:
        sys.exit("give --line (a talking shot) or --silent SECONDS (a cutaway, reaction or insert without dialogue)")
    if a.line and a.reach_for:
        sys.exit("refused: no object handling in talking shots. Put the reach in a no-dialogue insert "
                 "(--silent SECONDS --reach-for ...), then cut back to him talking.")
    line = a.line
    # 1. trim a tail sound after the last word
    tail_fix = None
    try:
        if a.silent:
            raise StopIteration
        from verify_line import audio_checks
        au = audio_checks(line)
        if au["tail_sound"]:
            trimmed = os.path.join(a.out, f"{a.id}_trimmed.wav")
            end = au["speech_end"] + 0.05
            run([FFMPEG, "-y", "-v", "error", "-i", line, "-t", f"{end:.3f}", "-af",
                 f"afade=t=out:st={max(0, end - 0.05):.3f}:d=0.05", trimmed])
            tail_fix = f"trimmed a sound after the last word ({au['tail_sound']['at']} s)"
            line = trimmed
    except StopIteration:
        pass
    except Exception as ex:
        tail_fix = f"tail check skipped: {ex}"
    # 2. the 6 s cap
    # continuity: chain from the previous shot, and end images for looks, reaches and moves
    target = a.look_at or a.reach_for
    if target and not a.target_in_frame:
        sys.exit(f"refused: '{target}' is not in the frame. A look at something off-frame is a cut: shoot him looking "
                 "off-camera (or eyes down), then a cutaway of the object. Put the object in the frame and pass "
                 "--target-in-frame to make it a look within the shot.")
    start = {"kind": "keyframe", "value": a.keyframe}
    chain = None
    if a.chain_from:
        prev = json.load(open(a.chain_from))
        clip = next((h["clip"] for h in reversed(prev.get("history", [])) if h.get("accepted")), prev.get("clip"))
        same = (prev.get("character") == a.character and prev.get("set") == a.set and prev.get("framing") == a.framing)
        if not same:
            chain = {"used": False, "why": f"previous shot is {prev.get('character')}/{prev.get('set')}/{prev.get('framing')}: "
                                           "a different character, set or framing starts from its keyframe"}
        elif not clip or not os.path.exists(clip):
            chain = {"used": False, "why": "previous shot has no accepted clip on disk"}
        else:
            png, info = clean_frame(clip, a.character, os.path.join(a.out, f"{a.id}_chain_start.png"))
            if png:
                start = {"kind": "previous_last_clean_frame", "file": png, "from": clip, "value": "<media_id of the uploaded frame>"}
                chain = {"used": True, "from_spec": a.chain_from, **info}
            else:
                chain = {"used": False, "why": info}
    end_request = None
    if target or a.end_pose:
        what = (f"his eyes on {target}" if a.look_at else f"his hand on {target}") if target else a.end_pose
        side = {"left": "to the left of the frame", "right": "to the right of the frame", "down": "down"}.get(a.target_side, "")
        end_request = {
            "model": END_IMAGE_MODEL.get(a.character, "gpt_image_2_5"), "aspect_ratio": "9:16",
            "medias": [{"role": "image_references", "value": start["value"]}],
            "prompt": ("Exactly the same photograph: same person, face, hair, clothes, room, framing, lighting and analog "
                       f"look. The only change: {what}" + (f" ({side})" if side else "") + ". "
                       + (f"{target[0].upper() + target[1:]} is clearly visible in the frame. " if target else "")
                       + "Mouth closed, eyes open. No new text."),
            "check": f"shot_spec.py endcheck <spec> <end image>  (identity, mouth closed, gaze {a.target_side or 'n/a'})"}
    if a.end_pose and start["kind"] == "keyframe" and not a.keyframe:
        sys.exit("a change of position needs a start image too (--keyframe or --chain-from)")
    if a.silent:
        return build_silent(a, start, chain, end_request)
    parts = [(0.0, duration(line))] if a.allow_long else split_points(line, MAX_TALK)
    specs = []
    for i, (t0, t1) in enumerate(parts):
        pid = a.id if len(parts) == 1 else f"{a.id}{chr(97 + i)}"
        seg = os.path.join(a.out, f"{pid}_line.wav")
        run([FFMPEG, "-y", "-v", "error", "-i", line, "-ss", f"{t0:.3f}", "-to", f"{t1:.3f}", seg])
        sm = speech_map(seg)
        speech = (sm["end"] or 0) - (sm["start"] or 0)
        # 3. lead-in, headroom, whole seconds
        track = os.path.join(a.out, f"{pid}_track.mp3")
        out = run([sys.executable, os.path.join(here, "make_track.py"), track, seg, "--lead", str(LEAD),
                   "--hold", str(HEADROOM), "--min", "2"])
        dur = int(out.split("clip duration ")[1].split("s")[0])
        base = a.prompt_base or BASES.get(a.character, BASES["pandey"])
        eyes = EYES_LOOK.format(t=a.look_at) if a.look_at else EYES_TALK
        prompt = " ".join(x for x in [STILL_START, base, ARTICULATE, eyes, a.acting or "", TAIL] if x)
        medias = [{"role": "start_image", "value": start["value"]}]
        if end_request:
            medias.append({"role": "end_image", "value": "<job id of the checked end image>"})
        medias.append({"role": "audio_references", "value": "<media_id of the uploaded track>"})
        spec = {"id": pid, "line": a.id, "part": i + 1, "parts": len(parts), "source_line": a.line,
                "set": a.set, "framing": a.framing, "target_side": a.target_side, "start": start, "chain": chain, "end_image_request": end_request,
                "sheet": SHEETS.get(a.character), "keyframe": a.keyframe,
                "source_span_s": [round(t0, 2), round(t1, 2)], "speech_s": round(speech, 2), "track": track,
                "character": a.character, "tail_fix": tail_fix, "attempt": 0, "max_auto_retries": 1,
                "edit_src_in_s": round(LEAD - 0.12, 2),
                "params": {"model": "wan2_7", "resolution": "720p", "aspect_ratio": "9:16", "duration": dur,
                           "declined_preset_id": DECLINED_PRESET,
                           "medias": medias,
                           "prompt": prompt},
                "qc": [f"python3 pipeline/lipsync_lag.py <clip> --json <clip>_lag.json",
                       f"python3 pipeline/check_match.py <clip> {track}",
                       f"python3 pipeline/face_consistency.py {SHEETS.get(a.character, '<character sheet>')} <clip>"]}
        path = os.path.join(a.out, f"{pid}.json")
        json.dump(spec, open(path, "w"), indent=1, ensure_ascii=False)
        specs.append(path)
        print(f"{pid}: {dur} s shot ({spec['speech_s']} s of speech) -> {path}")
    if len(parts) > 1:
        print(f"  line longer than {MAX_TALK:.0f} s: split into {len(parts)} shots at pauses; cut between them in the edit")
    if tail_fix:
        print(f"  {tail_fix}")
    if chain:
        print("  chain: " + (f"starts from the previous shot's clean frame at {chain['t']} s -> {start['file']}"
                             if chain["used"] else f"keyframe ({chain['why']})"))
    if end_request:
        print(f"  end image needed ({end_request['model']}): {end_request['prompt'][:140]}...")


def build_silent(a, start, chain, end_request):
    """a cutaway, reaction or insert without dialogue: no track, business and reaches allowed, same continuity rules"""
    dur = max(2, math.ceil(a.silent))
    base = a.prompt_base or ""
    prompt = " ".join(x for x in [base, a.acting or "", "No one speaks; the mouth stays closed.", TAIL] if x)
    medias = [{"role": "start_image", "value": start["value"]}]
    if end_request:
        medias.append({"role": "end_image", "value": "<job id of the checked end image>"})
    spec = {"id": a.id, "kind": "silent", "character": a.character, "set": a.set, "framing": a.framing,
            "target_side": a.target_side, "start": start, "chain": chain, "end_image_request": end_request,
            "sheet": SHEETS.get(a.character), "keyframe": a.keyframe, "attempt": 0, "max_auto_retries": 1,
            "params": {"model": "wan2_7", "resolution": "720p", "aspect_ratio": "9:16", "duration": dur,
                       "declined_preset_id": DECLINED_PRESET, "medias": medias, "prompt": prompt},
            "qc": [f"python3 pipeline/face_consistency.py {SHEETS.get(a.character, '<character sheet>')} <clip>"]}
    path = os.path.join(a.out, f"{a.id}.json")
    json.dump(spec, open(path, "w"), indent=1, ensure_ascii=False)
    print(f"{a.id}: {dur} s silent shot -> {path}  ({dur * 1.5:.1f} credits at 720p)")
    if chain:
        print("  chain: " + (f"starts from the previous shot's clean frame at {chain['t']} s" if chain["used"]
                             else f"keyframe ({chain['why']})"))
    if end_request:
        print(f"  end image needed ({end_request['model']})")


def judge(a):
    spec = json.load(open(a.spec))
    lag = os.path.splitext(a.clip)[0] + "_lag.json"
    if spec.get("kind") == "silent":           # no dialogue: nothing to sync; identity decides below
        L = {"verdict": "PASS (no dialogue)"}
    else:
        run([sys.executable, os.path.join(here, "lipsync_lag.py"), a.clip, "--json", lag])
        L = json.load(open(lag))
    spec.setdefault("history", []).append({"attempt": spec["attempt"], "clip": a.clip, "verdict": L["verdict"],
                                          "pattern": L.get("pattern"), "drift": L.get("drift_ms_per_s"),
                                          "failing_windows": L.get("failing_windows")})
    decision = {}
    face = None
    if spec.get("sheet") and os.path.exists(os.path.join(ROOT, spec["sheet"])):
        fj = os.path.splitext(a.clip)[0] + "_face.json"
        run([sys.executable, os.path.join(here, "face_consistency.py"), os.path.join(ROOT, spec["sheet"]), a.clip,
             "--every", "0.5", "--json", fj])
        face = json.load(open(fj))[0]
        spec["history"][-1]["face"] = {k: face.get(k) for k in ("verdict", "min", "mean")}
    if (spec.get("chain") or {}).get("used") and face and face.get("verdict") in ("FAIL", "UNSURE"):
        spec["start"] = {"kind": "keyframe", "value": spec["keyframe"]}
        spec["params"]["medias"][0]["value"] = spec["keyframe"]
        spec["chain"]["reset"] = True
        decision = {"action": "RESET_TO_KEYFRAME", "why": f"chained shot drifted from the character (face {face.get('verdict')}, "
                    f"worst {face.get('min')})", "do": "regenerate from the set keyframe instead of the previous frame"}
    elif spec.get("kind") == "silent" and face and face.get("verdict") == "FAIL":
        decision = {"action": "ASK", "why": f"identity drifted (worst {face.get('min')})"}
    elif L["verdict"].startswith("PASS"):
        decision = {"action": "ACCEPT"}
    elif L.get("pattern") == "constant" and "audio_shift_ms" in L and abs(L["audio_shift_ms"]) <= 250:
        decision = {"action": "ACCEPT_WITH_SHIFT", "audio_shift_ms": L["audio_shift_ms"], "why": L.get("repair")}
    elif spec["attempt"] < spec["max_auto_retries"]:
        spec["attempt"] += 1
        if L.get("pattern") == "drift" and spec["speech_s"] > 3.5:
            decision = {"action": "RETRY_SPLIT", "why": "drift within the line",
                        "do": f"shot_spec.py build --line {spec['source_line']} --id {spec['line']} with a lower cap "
                              f"(split this part at its pause) and regenerate both halves"}
        else:
            p = spec["params"]
            p["prompt"] = p["prompt"].replace(ARTICULATE, ARTICULATE + " Clear, visible mouth shapes on every "
                                              "vowel; the mouth closes fully on m, p and b.")
            decision = {"action": "RETRY", "why": f"{L['verdict'][:4]} ({L.get('pattern')})",
                        "do": "regenerate with the updated params in this spec (stronger articulation wording)"}
    else:
        decision = {"action": "ASK", "why": "failed again after the automatic retry",
                    "summary": f"{spec['id']}: {L['verdict'][:4]}, pattern {L.get('pattern')}, drift "
                               f"{L.get('drift_ms_per_s')} ms/s, failing windows at {L.get('failing_windows')} s. "
                               "Options: accept as is, regenerate from a tighter/straighter keyframe, or split the line."}
    if decision["action"].startswith("ACCEPT"):
        spec["history"][-1]["accepted"] = True
        spec["clip"] = a.clip
    spec["decision"] = decision
    json.dump(spec, open(a.spec, "w"), indent=1, ensure_ascii=False)
    print(f"{spec['id']} attempt {spec['attempt']}: {decision['action']}  " +
          "  ".join(f"{k}: {v}" for k, v in decision.items() if k != "action"))


def endcheck(a):
    """is the generated end image usable: same person, mouth closed, eyes toward the target side"""
    from face import load_rgb, analyse, gaze, mouth_open, embed
    spec = json.load(open(a.spec)); req = spec.get("end_image_request") or {}
    rgb = load_rgb(a.image, width=None); f = analyse(rgb)
    if not f:
        print("END IMAGE: FAIL  no face"); return
    f = f[0]; g = gaze(f); C = {}
    if spec.get("sheet"):
        from face_consistency import ref_embeddings, score, PASS
        sim = score(ref_embeddings(os.path.join(ROOT, spec["sheet"])), embed(rgb, f))
        C["identity"] = (sim >= PASS, f"{sim:.2f} vs sheet (>= {PASS})")
    C["mouth_closed"] = (mouth_open(f) < 0.06, f"inner-lip/width {mouth_open(f):.3f}")
    side = next((s for s in ("left", "right", "down") if s in (req.get("prompt") or "")), None)
    side = spec.get("target_side") or side
    if side:
        other = {"left": "right", "right": "left", "down": "up"}[side]
        ok = g[side] > 0.25 and g[side] > g[other] + 0.1
        C["gaze"] = (ok, f"eyes {side} {g[side]:.2f} vs {other} {g[other]:.2f} (want {side} > 0.25 and clearly more)")
    v = "PASS" if all(ok for ok, _ in C.values()) else "FAIL"
    spec["end_image_check"] = {"image": a.image, "verdict": v, **{k: d for k, (ok, d) in C.items()}}
    json.dump(spec, open(a.spec, "w"), indent=1, ensure_ascii=False)
    print(f"END IMAGE: {v}"); [print(f"  {'ok ' if ok else 'BAD'} {k}: {d}") for k, (ok, d) in C.items()]


def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("--line"); b.add_argument("--id", required=True)
    b.add_argument("--silent", type=float, help="a no-dialogue shot of this many seconds (instead of --line)")
    b.add_argument("--keyframe", required=True); b.add_argument("--character", default="pandey")
    b.add_argument("--acting", default=""); b.add_argument("--prompt-base"); b.add_argument("--out", default="specs")
    b.add_argument("--allow-long", action="store_true")
    b.add_argument("--set", default="", help="the set (kendra, studio, field...)")
    b.add_argument("--framing", default="", help="camera setup (front, three_quarter_left, two_shot, low...)")
    b.add_argument("--chain-from", help="the previous shot's spec: chain when character, set and framing match")
    b.add_argument("--look-at"); b.add_argument("--reach-for"); b.add_argument("--end-pose")
    b.add_argument("--target-side", choices=["left", "right", "down"])
    b.add_argument("--target-in-frame", action="store_true")
    e = sub.add_parser("endcheck"); e.add_argument("spec"); e.add_argument("image")
    j = sub.add_parser("judge"); j.add_argument("spec"); j.add_argument("clip")
    a = ap.parse_args()
    {"build": build, "judge": judge, "endcheck": endcheck}[a.cmd](a)


if __name__ == "__main__":
    main()
