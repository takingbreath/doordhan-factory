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
judge: after the clip is downloaded: runs lipsync_lag on it (own audio) and decides
         PASS                  -> accept
         constant offset        -> accept, with the audio_shift_ms for assembly (no regeneration)
         drift / weak lips / other FAIL -> one automatic retry (a split for drift on a long line, a stronger
                                   articulation prompt otherwise); after that -> ASK (a summary for Akhilesh)
Usage:
  shot_spec.py build --line P2.wav --id P2 --keyframe 93b0322a-... --character pandey \
       --acting "small nod on each 'gino'..." [--prompt-base "..."] [--out work/<slug>/specs] [--allow-long]
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
               "alive and human: heavy-lidded bored eyes, natural blinks, a faint dry smirk under his moustache."),
    "sarika": ("The news anchor from the start image reads the news in Hindi. She is a poised professional newsreader: "
               "head steady and level, shoulders still, only a small natural nod on a stressed word, expression carried "
               "by her eyes, a faint knowing smile at the end. No head tilting, no bobbing, no hair movement."),
    "gupta": ("The field news correspondent from the start image reports to camera in Hindi, head steady, "
              "a small natural nod on a stressed word."),
}
TAIL = "Small, subtle, natural movements only. Locked-off camera. Keep the exact analog look of the start image; no new text, no subtitles."


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
    line = a.line
    # 1. trim a tail sound after the last word
    tail_fix = None
    try:
        from verify_line import audio_checks
        au = audio_checks(line)
        if au["tail_sound"]:
            trimmed = os.path.join(a.out, f"{a.id}_trimmed.wav")
            end = au["speech_end"] + 0.05
            run([FFMPEG, "-y", "-v", "error", "-i", line, "-t", f"{end:.3f}", "-af",
                 f"afade=t=out:st={max(0, end - 0.05):.3f}:d=0.05", trimmed])
            tail_fix = f"trimmed a sound after the last word ({au['tail_sound']['at']} s)"
            line = trimmed
    except Exception as ex:
        tail_fix = f"tail check skipped: {ex}"
    # 2. the 6 s cap
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
        prompt = " ".join(x for x in [STILL_START, base, ARTICULATE, a.acting or "", TAIL] if x)
        spec = {"id": pid, "line": a.id, "part": i + 1, "parts": len(parts), "source_line": a.line,
                "source_span_s": [round(t0, 2), round(t1, 2)], "speech_s": round(speech, 2), "track": track,
                "character": a.character, "tail_fix": tail_fix, "attempt": 0, "max_auto_retries": 1,
                "edit_src_in_s": round(LEAD - 0.12, 2),
                "params": {"model": "wan2_7", "resolution": "720p", "aspect_ratio": "9:16", "duration": dur,
                           "declined_preset_id": DECLINED_PRESET,
                           "medias": [{"role": "start_image", "value": a.keyframe},
                                      {"role": "audio_references", "value": "<media_id of the uploaded track>"}],
                           "prompt": prompt},
                "qc": [f"python3 pipeline/lipsync_lag.py <clip> --json <clip>_lag.json",
                       f"python3 pipeline/check_match.py <clip> {track}",
                       f"python3 pipeline/face_consistency.py <character sheet> <clip>"]}
        path = os.path.join(a.out, f"{pid}.json")
        json.dump(spec, open(path, "w"), indent=1, ensure_ascii=False)
        specs.append(path)
        print(f"{pid}: {dur} s shot ({spec['speech_s']} s of speech) -> {path}")
    if len(parts) > 1:
        print(f"  line longer than {MAX_TALK:.0f} s: split into {len(parts)} shots at pauses; cut between them in the edit")
    if tail_fix:
        print(f"  {tail_fix}")


def judge(a):
    spec = json.load(open(a.spec))
    lag = os.path.splitext(a.clip)[0] + "_lag.json"
    run([sys.executable, os.path.join(here, "lipsync_lag.py"), a.clip, "--json", lag])
    L = json.load(open(lag))
    spec.setdefault("history", []).append({"attempt": spec["attempt"], "clip": a.clip, "verdict": L["verdict"],
                                          "pattern": L.get("pattern"), "drift": L.get("drift_ms_per_s"),
                                          "failing_windows": L.get("failing_windows")})
    decision = {}
    if L["verdict"].startswith("PASS"):
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
    spec["decision"] = decision
    json.dump(spec, open(a.spec, "w"), indent=1, ensure_ascii=False)
    print(f"{spec['id']} attempt {spec['attempt']}: {decision['action']}  " +
          "  ".join(f"{k}: {v}" for k, v in decision.items() if k != "action"))


def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("--line", required=True); b.add_argument("--id", required=True)
    b.add_argument("--keyframe", required=True); b.add_argument("--character", default="pandey")
    b.add_argument("--acting", default=""); b.add_argument("--prompt-base"); b.add_argument("--out", default="specs")
    b.add_argument("--allow-long", action="store_true")
    j = sub.add_parser("judge"); j.add_argument("spec"); j.add_argument("clip")
    a = ap.parse_args()
    build(a) if a.cmd == "build" else judge(a)


if __name__ == "__main__":
    main()
