#!/usr/bin/env python3
"""Is this still the same character? Cosine similarity between AuraFace-v1 identity embeddings (pipeline/face.py) of
the character's reference (a character sheet: every face on it is used, best match counts) and a keyframe or a clip
(frames sampled every --every seconds; the worst frame counts, so a face that drifts mid-clip is caught).
Thresholds calibrated 2026-09-28 on our own episodes (work/lag/face_calibration.txt):
  same character (Pandey, Sarika, Gupta: sheet vs keyframes vs clips, 45 pairs)   0.66 - 0.93
  different characters (75 pairs)                                             0.10 - 0.34
  -> PASS >= 0.55, WARN 0.45-0.55 (look at it), FAIL < 0.45.
  No mid-clip identity drift exists in our material yet, so the FAIL side is calibrated on other characters.
Usage: face_consistency.py REF.png TARGET(.png|.mp4) [TARGET ...] [--every 1.0] [--start S --end E] [--json OUT]
  --start/--end: only that time range of a video (one talking segment of a finished reel; qc_gate.py uses it)."""
import argparse, json, os, sys
import numpy as np

here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from face import load_rgb, analyse, embed  # noqa: E402
from common import duration  # noqa: E402

PASS, WARN = 0.55, 0.45


def ref_embeddings(path):
    rgb = load_rgb(path, width=1440)            # sheets hold several small faces: analyse at higher resolution
    return [embed(rgb, f) for f in analyse(rgb)]


def target_embeddings(path, every, start=0.0, end=None):
    if os.path.splitext(path)[1].lower() in (".png", ".jpg", ".jpeg", ".webp"):
        rgb = load_rgb(path); f = analyse(rgb)
        return [(0.0, embed(rgb, f[0]))] if f else []
    out = []
    end = min(end if end is not None else 1e9, duration(path) - 0.1)
    for t in np.arange(start + 0.2, end, every):
        rgb = load_rgb(path, t=float(t)); f = analyse(rgb)
        if f:
            out.append((float(t), embed(rgb, f[0])))
    return out


def score(refs, emb):
    return max(float(np.dot(r, emb)) for r in refs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ref"); ap.add_argument("targets", nargs="+")
    ap.add_argument("--every", type=float, default=1.0); ap.add_argument("--json")
    ap.add_argument("--start", type=float, default=0.0); ap.add_argument("--end", type=float)
    a = ap.parse_args()
    refs = ref_embeddings(a.ref)
    if not refs:
        sys.exit(f"no face found in the reference {a.ref}")
    results = []
    for tg in a.targets:
        embs = target_embeddings(tg, a.every, a.start, a.end)
        if not embs:
            results.append({"target": tg, "verdict": "UNSURE", "detail": "no face found"}); continue
        sims = [(t, round(score(refs, e), 3)) for t, e in embs]
        worst = min(s for _, s in sims)
        v = "PASS" if worst >= PASS else ("WARN" if worst >= WARN else "FAIL")
        results.append({"target": tg, "verdict": v, "min": worst, "mean": round(float(np.mean([s for _, s in sims])), 3),
                        "per_frame": sims})
    for r in results:
        extra = f"min {r['min']}  mean {r['mean']}" if "min" in r else r["detail"]
        print(f"{os.path.basename(r['target'])}: {r['verdict']}  vs {os.path.basename(a.ref)}  {extra}")
    if a.json:
        json.dump(results, open(a.json, "w"), indent=1)


if __name__ == "__main__":
    main()
