#!/usr/bin/env python3
"""How the lips move, not only when (anthropic01, 2026-10-28). lipsync_lag and check_match judge timing, so shots
that passed them still looked wrong to Akhilesh: Rashmi's mouth opened about twice as wide as a real speaker's and
she talked through a grin. This measures, on the largest face, over a span of the clip (30 fps):
  lip gap      inner-lip distance as % of face height: mean and p90 (real creator 3.5-3.8 / 7.0-7.5)
  upper lip    mouthUpperUp blendshape: a grin over the teeth (real 0.12-0.19)
  pucker       mouthPucker + mouthFunnel: exaggerated O shapes (real 0.11-0.13)
  smile        mouthSmile while speaking
  brows        browInnerUp / browOuterUp: raised brows read as excited (real 0.39-0.49 / 0.30-0.32)
  cycles/s     open-close cycles of the lips (timing; real 2.3-2.5)
Reference numbers are from the creator in instagram.com/reel/DeyzsQiBZ3B (three 15 s spans); our results per take are
in docs/lab/2026-10-28-talking-realism.md. Run it on a real creator's clip of the same framing to get your own bar.
Usage: mouth_meter.py CLIP FROM TO [LABEL] [--json OUT]"""
import argparse, json, os, sys
import numpy as np
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from motion_meter import frames  # noqa: E402
from face import analyse  # noqa: E402

FPS = 30


def measure(clip, t0, t1):
    rows = []
    for f in frames(clip, t0, t1, FPS, 540):
        a = analyse(f)
        if not a: continue
        a = a[0]; b = a["blend"]; p = a["points"]; fh = a["box"][3] - a["box"][1]
        rows.append(dict(gap=float(np.linalg.norm(p[13] - p[14]) / fh), jaw=b["jawOpen"],
                         pucker=b["mouthPucker"] + b["mouthFunnel"],
                         smile=(b["mouthSmileLeft"] + b["mouthSmileRight"]) / 2,
                         upper=(b["mouthUpperUpLeft"] + b["mouthUpperUpRight"]) / 2,
                         brow=b["browInnerUp"], browout=(b["browOuterUpLeft"] + b["browOuterUpRight"]) / 2))
    if len(rows) < 10: sys.exit(f"{clip}: face found in only {len(rows)} frames")
    A = {k: np.array([r[k] for r in rows]) for k in rows[0]}
    g = A["gap"]; sm = np.convolve(g, np.ones(3) / 3, mode="same"); d = np.diff(sm)
    peaks = int(((d[:-1] > 0) & (d[1:] <= 0) & (sm[1:-1] > np.percentile(sm, 40) + 0.01)).sum())
    secs = len(rows) / FPS
    return {"frames": len(rows), "lip_gap_mean_pct": round(float(g.mean() * 100), 1),
            "lip_gap_p90_pct": round(float(np.percentile(g, 90) * 100), 1), "lip_gap_max_pct": round(float(g.max() * 100), 1),
            "jaw_mean": round(float(A["jaw"].mean()), 2), "cycles_per_s": round(peaks / secs, 1),
            "pucker": round(float(A["pucker"].mean()), 2), "smile": round(float(A["smile"].mean()), 2),
            "upper_lip": round(float(A["upper"].mean()), 2), "brow_inner": round(float(A["brow"].mean()), 2),
            "brow_outer": round(float(A["browout"].mean()), 2)}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("clip"); ap.add_argument("t0", type=float); ap.add_argument("t1", type=float)
    ap.add_argument("label", nargs="?"); ap.add_argument("--json")
    a = ap.parse_args()
    r = measure(a.clip, a.t0, a.t1)
    print(f"{(a.label or os.path.basename(a.clip)):18s} " + "  ".join(f"{k} {v}" for k, v in r.items()))
    if a.json: json.dump(dict(r, clip=a.clip, span=[a.t0, a.t1]), open(a.json, "w"), indent=1)


if __name__ == "__main__":
    main()
