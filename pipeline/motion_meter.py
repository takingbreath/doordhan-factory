#!/usr/bin/env python3
"""How animated is a talking face? (anthropic01, 2026-10-28: Akhilesh found Rashmi's movements unreal next to a real
creator.) Measures, on the largest face, over a span of the clip:
  - head roll and yaw spread (standard deviation, degrees) and head travel (face-centre path, % of face height a second);
  - eye moves a second: frames where the iris shifts by more than 0.6% of the face width against the eye corners;
  - blinks in 10 s: eyeBlink blendshape crossing 0.5;
  - brow lifts in 10 s: browInnerUp crossing 0.35.
Compare a generated clip with a real creator's clip on the same numbers. Usage:
  motion_meter.py CLIP [--from S] [--to S] [--fps 15] [--json OUT]"""
import argparse, json, os, subprocess, sys
import numpy as np
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from common import FFMPEG  # noqa: E402
from face import analyse  # noqa: E402

L_EYE, R_EYE = (33, 133, 468), (362, 263, 473)   # outer corner, inner corner, iris centre


def frames(clip, t0, t1, fps, width=540):
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                            "-of", "csv=p=0", clip], capture_output=True, text=True).stdout.strip().split(",")
    W, H = int(probe[0]), int(probe[1]); h = int(H * width / W) // 2 * 2
    cmd = [FFMPEG, "-v", "error", "-ss", str(t0)] + (["-to", str(t1)] if t1 else []) + \
          ["-i", clip, "-vf", f"fps={fps},scale={width}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    n = len(raw) // (width * h * 3)
    return np.frombuffer(raw[:n * width * h * 3], np.uint8).reshape(n, h, width, 3)


def iris_pos(p, ids):
    a, b, c = p[ids[0]], p[ids[1]], p[ids[2]]
    v = b - a; L = np.linalg.norm(v) + 1e-6
    return np.dot(c - a, v) / L / L, np.cross(v, c - a) / L / L     # along and across the eye, in eye widths


def crossings(x, th):
    up = (x[1:] >= th) & (x[:-1] < th)
    return int(up.sum())


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("clip"); ap.add_argument("--from", dest="t0", type=float, default=0)
    ap.add_argument("--to", dest="t1", type=float); ap.add_argument("--fps", type=float, default=15); ap.add_argument("--json")
    a = ap.parse_args()
    rows = []
    for rgb in frames(a.clip, a.t0, a.t1, a.fps):
        f = analyse(rgb)
        if not f: rows.append(None); continue
        f = f[0]; p = f["points"]; x0, y0, x1, y1 = f["box"]
        g = np.array(iris_pos(p, L_EYE) + iris_pos(p, R_EYE))
        rows.append({"roll": f["pose"]["roll"], "yaw": f["pose"]["yaw"], "pitch": f["pose"]["pitch"],
                     "cx": (x0 + x1) / 2, "cy": (y0 + y1) / 2, "fh": y1 - y0, "gaze": g,
                     "blink": (f["blend"].get("eyeBlinkLeft", 0) + f["blend"].get("eyeBlinkRight", 0)) / 2,
                     "brow": f["blend"].get("browInnerUp", 0)})
    ok = [r for r in rows if r]
    if len(ok) < 10: sys.exit(f"{a.clip}: face found in only {len(ok)} frames")
    secs = len(rows) / a.fps
    arr = lambda k: np.array([r[k] for r in ok])
    fh = np.median(arr("fh"))
    path = np.hypot(np.diff(arr("cx")), np.diff(arr("cy"))).sum() / fh * 100
    blink = arr("blink"); open_ = blink < 0.35
    G = np.array([r["gaze"] for r in ok]); dG = np.abs(np.diff(G, axis=0)).max(1)
    eye_moves = int(((dG > 0.03) & open_[1:] & open_[:-1]).sum())
    out = {"clip": os.path.basename(a.clip), "seconds": round(secs, 2), "frames": len(ok),
           "roll_sd": round(float(arr("roll").std()), 1), "yaw_sd": round(float(arr("yaw").std()), 1),
           "pitch_sd": round(float(arr("pitch").std()), 1),
           "head_travel_pct_s": round(float(path / secs), 1),
           "eye_moves_s": round(eye_moves / secs, 2),
           "blinks_10s": round(crossings(blink, 0.5) / secs * 10, 1),
           "brow_lifts_10s": round(crossings(arr("brow"), 0.35) / secs * 10, 1)}
    print("  ".join(f"{k} {v}" for k, v in out.items()))
    if a.json: json.dump(out, open(a.json, "w"), indent=1)


if __name__ == "__main__":
    main()
