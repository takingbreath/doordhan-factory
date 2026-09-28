#!/usr/bin/env python3
"""Check a keyframe before it becomes a talking shot (free; run on every talking keyframe).
  face size   face height / frame height and mouth width (px at 720 wide). Floors, not goals: every E3-E6 talking
              clip had 16-33% and 62-130 px; the E5 master wide (13%, 44 px) was never used for talking.
  head pose   yaw / pitch / roll. The E5 clips that drifted past the lip-sync limit started tilted (the Billu
              two-shot: pitch 28, roll -15) or turned (T4v2: yaw -17 with a head turn in the prompt); straight-on
              frames and E5 v1's 3/4 frames (yaw -29, level head) synced fine.
  mouth       jawOpen blendshape: a talking shot should start with the mouth closed (a still start).
  eyes        --profile pandey: heavy-lidded, not wide-eyed. Lid closure (eyeBlink) was 0.00-0.02 on the frozen
              "lifeless" keyframes and 0.09-0.19 on the approved ones (Akhilesh, 2026-09-27).
  text        --ocr X Y W H --expect "TEXT": OCR (tesseract eng+hin) on a region in the 720-wide frame, fuzzy-matched.
              Catches a board or logo the image model misspelled.
Verdict: FAIL on any hard limit, WARN on a soft one.
Usage: preflight_keyframe.py IMAGE [--profile pandey|sarika|generic] [--role talking|cutaway]
       [--ocr X Y W H --expect "DOORDHAN SAHAYATA KENDRA"] [--json OUT]"""
import argparse, difflib, json, os, re, sys
import numpy as np

here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from face import load_rgb, analyse  # noqa: E402

# (warn, fail) thresholds; see the docstring for the data behind them
FACE_H = (0.16, 0.12)       # below warn -> WARN, below fail -> FAIL
MOUTH_PX = (60, 45)
YAW = (20, 32)              # |deg| above warn -> WARN, above fail -> FAIL
PITCH = (18, 26)
ROLL = (10, 16)
JAW_OPEN = (0.12, 0.25)
PROFILES = {"pandey": {"lid_min": 0.06}, "sarika": {}, "gupta": {}, "generic": {}}


def grade(value, warn, fail, higher_is_worse=True):
    v = abs(value) if higher_is_worse else value
    if higher_is_worse:
        return "FAIL" if v > fail else ("WARN" if v > warn else "ok")
    return "FAIL" if v < fail else ("WARN" if v < warn else "ok")


def ocr(rgb, box):
    import pytesseract
    from PIL import Image, ImageOps
    x, y, w, h = box
    im = Image.fromarray(rgb[y:y + h, x:x + w])
    im = ImageOps.autocontrast(ImageOps.grayscale(im.resize((w * 3, h * 3), Image.LANCZOS)))
    best = ""
    for img in (im, ImageOps.invert(im)):
        t = pytesseract.image_to_string(img, lang="eng+hin", config="--psm 6")
        t = re.sub(r"\s+", " ", t).strip()
        if len(re.sub(r"[^A-Za-zऀ-ॿ]", "", t)) > len(re.sub(r"[^A-Za-zऀ-ॿ]", "", best)):
            best = t
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image"); ap.add_argument("--profile", default="generic", choices=PROFILES)
    ap.add_argument("--role", default="talking", choices=["talking", "cutaway"])
    ap.add_argument("--ocr", nargs=4, type=int); ap.add_argument("--expect")
    ap.add_argument("--json"); ap.add_argument("--label", default="")
    a = ap.parse_args()
    rgb = load_rgb(a.image)
    H = rgb.shape[0]
    faces = analyse(rgb)
    C = {}
    if a.role == "talking":
        if not faces:
            C["face"] = ("FAIL", "no face found")
        else:
            f = faces[0]; p = f["points"]; x0, y0, x1, y1 = f["box"]
            fh = (y1 - y0) / H; mw = float(np.linalg.norm(p[61] - p[291]))
            C["face_size"] = (grade(fh, *FACE_H, higher_is_worse=False), f"face {fh:.0%} of frame height")
            C["mouth_size"] = (grade(mw, *MOUTH_PX, higher_is_worse=False), f"mouth {mw:.0f} px wide")
            ps = f["pose"]
            C["yaw"] = (grade(ps["yaw"], *YAW), f"{ps['yaw']:+.0f} deg")
            C["pitch"] = (grade(ps["pitch"], *PITCH), f"{ps['pitch']:+.0f} deg")
            C["roll"] = (grade(ps["roll"], *ROLL), f"{ps['roll']:+.0f} deg")
            jaw = f["blend"].get("jawOpen", 0)
            C["mouth_closed"] = (grade(jaw, *JAW_OPEN), f"jawOpen {jaw:.2f} (a still start needs a closed mouth)")
            lid = (f["blend"].get("eyeBlinkLeft", 0) + f["blend"].get("eyeBlinkRight", 0)) / 2
            prof = PROFILES[a.profile]
            if "lid_min" in prof:
                C["heavy_lids"] = ("ok" if lid >= prof["lid_min"] else "FAIL",
                                   f"lid closure {lid:.2f} (>= {prof['lid_min']} for {a.profile}: wide-eyed reads lifeless)")
            if len(faces) > 1 and faces[1]["area"] > 0.25 * f["area"]:
                C["one_face"] = ("WARN", f"{len(faces)} faces; the lip-sync model may animate the wrong one")
    if a.ocr:
        txt = ocr(rgb, a.ocr)
        if a.expect:
            norm = lambda s: re.sub(r"[^a-z0-9ऀ-ॿ]", "", s.lower())
            r = difflib.SequenceMatcher(None, norm(a.expect), norm(txt)).ratio()
            C["text"] = ("ok" if r >= 0.8 else ("WARN" if r >= 0.6 else "FAIL"),
                         f"read '{txt}' vs expected '{a.expect}' (match {r:.2f})")
        else:
            C["text"] = ("ok", f"read '{txt}'")
    verdict = "FAIL" if any(v[0] == "FAIL" for v in C.values()) else ("WARN" if any(v[0] == "WARN" for v in C.values()) else "PASS")
    if a.json:
        json.dump({"image": a.image, "verdict": verdict, "checks": {k: {"grade": g, "detail": d} for k, (g, d) in C.items()}},
                  open(a.json, "w"), indent=1, ensure_ascii=False)
    print(f"{a.label or os.path.basename(a.image)}: {verdict}")
    for k, (g, d) in C.items():
        print(f"  {g:4s} {k}: {d}")


if __name__ == "__main__":
    main()
