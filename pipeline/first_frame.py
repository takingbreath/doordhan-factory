#!/usr/bin/env python3
"""The first second of a reel (QC gate row "firstframe"), and a cheap way to try first frames before paying for video.

Why: 52% of viewers skip in the first 3 s against a target of 45% (registry/performance.md). Bet B1 says what the opening
must be: frame 1 already shows the subject and the viewer's stake in 6 big words or fewer, nothing before it, and a cut
or punch-in by 1 s. This checks those from the finished file and the manifest.

The QC manifest declares the opening:
  "hook": {"text": "Anthropic ka God share", "subject": "face"|"logo"|"photo"|"footage"|"number",
           "t0": 0.0 (when the hook text appears), "font_px": 96 (its height on the 1080x1920 frame)}
Rows (blocking when a hook is declared; with no hook the gate says NOT CHECKED and prints what it measured):
  visible  frame 1 is not black, flat or a fade-in (mean luma >= MIN_LUMA, spread >= MIN_SPREAD)
  motion   a cut or punch-in inside the first 1 s: some 0.25 s step differs by >= CUT, or frame 1 vs 1.0 s by >= MOVE
           (mean absolute difference of 72x128 grey frames, 0-255). The two thresholds are first guesses, not calibrated on
           real finals: the row prints the numbers, so tune CUT / MOVE once from a few reels you rate good and bad.
  hook     <= 6 words, on screen from t0 <= 0.1 s, big (font_px >= MIN_FONT_PX when given), and no kind "title",
           "namaskar" or "intro" graphic before 1 s
  subject  "face": a face in frame 1, eyes toward the lens (needs MediaPipe, else NOT CHECKED); any other subject is
           taken from the manifest (declared, not machine-checked)
What this cannot judge: whether the hook is a good one, or readable on the finished frame (no OCR is installed).

  first_frame.py check FINAL [--manifest M.json]    measure a file
  first_frame.py variants --slug S --prompt-file P [--refs ID,ID] [--levers to_camera,split,number]
        writes work/S/first_frame/variants.json: one generate_image request per lever (9:16, the keyframe role's model),
        prints the credits it would cost. It sends nothing; send each through the spend guard, look at them, pick one by eye."""
import argparse, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from common import FFMPEG  # noqa: E402

ROOT = os.path.dirname(HERE)
MIN_LUMA, MIN_SPREAD = 25, 18
CUT, MOVE = 8.0, 5.0
MAX_HOOK_WORDS, MIN_FONT_PX = 6, 90
GAZE_MAX = 0.40
BAD_BEFORE = {"title", "namaskar", "intro"}
W, H, STEP = 72, 128, 0.25


def frames(path, seconds=1.3):
    """grey 72x128 frames every 0.25 s from t=0 (6 frames for 1.3 s)"""
    import numpy as np
    raw = subprocess.run([FFMPEG, "-v", "error", "-i", path, "-t", str(seconds), "-vf",
                          f"fps={1 / STEP:g},scale={W}:{H}:flags=area,format=gray", "-f", "rawvideo", "-"],
                         capture_output=True).stdout
    n = len(raw) // (W * H)
    return [np.frombuffer(raw[i * W * H:(i + 1) * W * H], np.uint8).reshape(H, W).astype(float) for i in range(n)]


def measure(path):
    import numpy as np
    fr = frames(path)
    if len(fr) < 5:
        return None
    steps = [float(np.mean(np.abs(fr[i + 1] - fr[i]))) for i in range(len(fr) - 1)]
    return {"luma": float(fr[0].mean()), "spread": float(fr[0].std()), "max_step": max(steps),
            "step_at_s": steps.index(max(steps)) * STEP + STEP, "move_1s": float(np.mean(np.abs(fr[4] - fr[0])))}


def _face_row(path, subject):
    try:
        import face
        rgb = face.load_rgb(path, t=0.0)
        found = face.analyse(rgb)
    except Exception as ex:
        return None, f"face check unavailable ({str(ex)[-60:]})"
    if not found:
        return False, "no face in frame 1"
    g = face.gaze(found[0])
    off = max(g.values())
    return off <= GAZE_MAX, f"face found, eyes off the lens by {off:.2f} (limit {GAZE_MAX})"


def check(M, final_path, graphics=None):
    """[(id, True|False|None, detail, fix)]; None = not checked"""
    m = measure(final_path)
    if m is None:
        return [("all", False, "the file is shorter than 1.25 s or unreadable", "rebuild the final")]
    seen = (f"luma {m['luma']:.0f}, spread {m['spread']:.0f}, biggest 0.25 s change {m['max_step']:.1f} at "
            f"{m['step_at_s']:.2f} s, frame 1 vs 1.0 s {m['move_1s']:.1f}")
    hook = M.get("hook")
    if not hook:
        return [("all", None, "the manifest declares no hook, so the first second was not judged. Measured: " + seen,
                 'add "hook": {"text","subject","t0","font_px"} to the QC manifest')]
    rows = []
    ok = m["luma"] >= MIN_LUMA and m["spread"] >= MIN_SPREAD
    rows.append(("visible", ok, f"frame 1: luma {m['luma']:.0f}, spread {m['spread']:.0f}" if ok else
                 f"frame 1 is dark or flat (luma {m['luma']:.0f}, spread {m['spread']:.0f}): the cover and the first scroll see nothing",
                 None if ok else "start on the picture, not a fade; the cover is frame 1"))
    ok = m["max_step"] >= CUT or m["move_1s"] >= MOVE
    rows.append(("motion", ok, f"movement in the first second ({seen})" if ok else
                 f"nothing moves in the first second ({seen})", None if ok else "cut or punch in by 1 s (a 1.2x punch-in is enough)"))
    words, problems = len(hook.get("text", "").split()), []
    if words > MAX_HOOK_WORDS:
        problems.append(f"{words} words, limit {MAX_HOOK_WORDS}")
    if float(hook.get("t0", 0)) > 0.1:
        problems.append(f"appears at {hook['t0']:.1f} s, not in frame 1")
    if hook.get("font_px") and hook["font_px"] < MIN_FONT_PX:
        problems.append(f"{hook['font_px']} px tall, under {MIN_FONT_PX} (the old-TV softening eats small text)")
    early = [g for g in (graphics or []) if g.get("kind") in BAD_BEFORE and float(g.get("t0", 0)) < 1.0]
    if early:
        problems.append(f"a {early[0]['kind']} graphic at {early[0]['t0']:.1f} s sits before the hook has landed")
    rows.append(("hook", not problems, f"\"{hook.get('text', '')}\": {words} words, in frame 1" if not problems else
                 f"\"{hook.get('text', '')}\": " + "; ".join(problems),
                 None if not problems else "shorten the hook, show it from frame 1 in big type, and move any title or Namaskar after it"))
    if hook.get("subject") == "face":
        ok, why = _face_row(final_path, "face")
        rows.append(("subject", ok, why, None if ok is not False else "start on a shot of the person looking into the lens"))
    else:
        rows.append(("subject", True, f"declared subject: {hook.get('subject', '?')} (from the manifest, not machine-checked)", None))
    return rows


LEVERS = {
    "to_camera": "The presenter looks straight into the lens, mid-sentence, as if already saying it; the hook is printed in huge bold type across the top third.",
    "split": "Split frame from the first frame: the top half is the story's own picture (the company logo, the person's real photo or the headline), the presenter fills the bottom half looking into the lens; the hook in huge bold type on the seam.",
    "number": "The one number that carries the story fills the frame in huge bold type with its unit, the presenter small in the lower corner looking into the lens.",
}


def variants(a):
    import spend, models
    prices = spend.read_json(spend.PRICES, {})
    model = models.resolve("keyframe")
    base = open(a.prompt_file, encoding="utf-8").read().strip()
    refs = [r for r in (a.refs or "").split(",") if r]
    reqs, total = [], 0.0
    for lv in [x for x in a.levers.split(",") if x]:
        if lv not in LEVERS:
            sys.exit(f"unknown lever {lv}; choose from {', '.join(LEVERS)}")
        params = {"model": model, "aspect_ratio": "9:16", "count": 1, "prompt": f"{base}\n\nFirst frame of a reel. {LEVERS[lv]}"}
        if refs:
            params["medias"] = [{"role": "image_references", "value": r} for r in refs]
        c, desc = spend.price_one(params, prices)
        total += c or 0
        reqs.append({"lever": lv, "cost": c, "params": params})
    out = os.path.join(ROOT, "work", a.slug, "first_frame"); os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "variants.json")
    json.dump({"slug": a.slug, "credits": total, "requests": reqs}, open(path, "w"), indent=1, ensure_ascii=False)
    print(f"{len(reqs)} first-frame variants, {total:g} credits in all ({model}); written to {os.path.relpath(path, ROOT)}. Nothing sent.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check"); c.add_argument("final"); c.add_argument("--manifest")
    v = sub.add_parser("variants"); v.add_argument("--slug", required=True); v.add_argument("--prompt-file", required=True)
    v.add_argument("--refs"); v.add_argument("--levers", default="to_camera,split,number")
    a = ap.parse_args()
    if a.cmd == "variants":
        return variants(a)
    M = json.load(open(a.manifest)) if a.manifest else {}
    bad = 0
    for rid, ok, detail, fix in check(M, a.final, M.get("graphics")):
        print(f"{'NOT CHECKED' if ok is None else 'PASS' if ok else 'FAIL':<11} {rid:<8} {detail}" + (f"\n{'':<20}fix: {fix}" if fix and ok is False else ""))
        bad += ok is False
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
