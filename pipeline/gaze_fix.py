#!/usr/bin/env python3
"""Do his eyes look straight into the lens, both the same way? Check it, and fix it by moving the irises 1-3 px.

Why (Akhilesh, 2026-10-23, sk05): "he talks to the camera, but his eyes appear misaligned". Measured on sk05's Wan clips: the two eyes
disagree by 0.20-0.33 on MediaPipe's eyeLook scale (a real person talking to camera: 0.03), and both irises sit toward the outer
corners (vergence -0.16..-0.23; a real person: -0.06). Seedream draws this character's eyes diverging and Wan makes it worse;
asking for "parallel eyes" in the prompt did not help in four tries, so the repair is mechanical.

  python3 pipeline/gaze_fix.py check CLIP_OR_IMAGE ...        numbers and PASS/FAIL (the gate: run it on every talking clip)
  python3 pipeline/gaze_fix.py fix IN.mp4 OUT.mp4 [--gaze 0.53]    re-seats both irises per frame, keeps the audio

Numbers (MediaPipe landmarks; ratios are the iris position between the eye corners, 0 = outer corner, 1 = inner):
  vergence = ratio(image-left eye) - ratio(image-right eye, measured from its inner corner)   real person -0.055 (sd 0.044)
  split    = the two eyes' horizontal eyeLook scores disagree                                 real person 0.029 (max 0.25)
  PASS: mean split <= 0.12 and the 90th-percentile split <= 0.25 (one noisy frame cannot fail a clip). Vergence is printed as an advisory only: this face reads -0.11 even when it looks right,
and the landmarks barely follow a 2-3 px iris shift, so after `fix` it stays low while the split score and the picture are right.
Fix: each iris is moved so that both eyes point the same way (target gaze 0.53 = looking into the lens, the real-person value),
vertical positions are equalised, nothing moves during a blink, and the shift is smoothed over time. An intended look-away
(more than 0.06 from the target) keeps its direction and only the two eyes are made to agree. Run `check` on the result.
Stills: the face model does not register a 2-3 px iris shift on one image (tested 23 Oct), so `check` on a keyframe is only a rough guide; judge keyframes by eye
and let the clip fix and the clip gate do the work. Tested on sk05 T1: split 0.22 -> 0.07, the largest shift 5.8 px at 720p."""
import argparse, os, subprocess, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import face as F  # noqa: E402

R_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
L_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
# per eye: iris centre, iris ring, outer/inner corner for the ratio (A -> B), upper and lower lid, contour
EYES = ({"c": 468, "ring": [469, 470, 471, 472], "A": 33, "B": 133, "top": 159, "bot": 145, "contour": R_EYE},     # subject's right = image left
        {"c": 473, "ring": [474, 475, 476, 477], "A": 362, "B": 263, "top": 386, "bot": 374, "contour": L_EYE})  # subject's left = image right
BASE_V = 0.055          # a real person's resting vergence (landmark bias): ratio(R) - ratio(L) = -BASE_V
GAZE_LENS = 0.53        # a real person's mean ratio when looking into the lens
PASS = {"vergence": -0.14, "split": 0.12, "split_p90": 0.25}


def geom(p, e):
    c = p[e["c"]]; ri = float(np.mean([np.linalg.norm(c - p[k]) for k in e["ring"]]))
    A, B = p[e["A"]], p[e["B"]]; top, bot = p[e["top"]], p[e["bot"]]
    w = B[0] - A[0]; h = max(1e-3, bot[1] - top[1])
    return {"c": c.copy(), "ri": ri, "r": (c[0] - A[0]) / (w + 1e-6), "v": (c[1] - top[1]) / h, "w": abs(w), "h": h,
            "open": h / (abs(w) + 1e-6), "contour": p[e["contour"]].copy()}


def split_score(face):
    b = face["blend"]; g = lambda k: b.get(k, 0.0)
    return abs((g("eyeLookOutRight") - g("eyeLookInRight")) - (g("eyeLookInLeft") - g("eyeLookOutLeft")))


def frames_of(path, width=None):
    """yield RGB frames of a video, or the single image"""
    if path.lower().endswith((".png", ".jpg", ".jpeg")):
        yield F.load_rgb(path, None, width=width); return
    w, h, fps = probe(path)
    sc = ["-vf", f"scale={width}:-2"] if width else []
    if width: h = int(round(h * width / w / 2) * 2); w = width
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path] + sc + ["-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    while True:
        buf = p.stdout.read(w * h * 3)
        if len(buf) < w * h * 3: break
        yield np.frombuffer(buf, np.uint8).reshape(h, w, 3).copy()
    p.stdout.close(); p.wait()


def probe(path):
    o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate", "-of", "csv=p=0", path],
                       capture_output=True, text=True).stdout.strip().split(",")
    a, b = o[2].split("/"); return int(o[0]), int(o[1]), float(a) / float(b)


def measure(path, step=1, width=None):
    """per sampled frame: (vergence, split, mean ratio, openness) of the largest face; None where no face"""
    rows = []
    for i, rgb in enumerate(frames_of(path, width)):
        if i % step: continue
        fs = F.analyse(rgb)
        if not fs: rows.append(None); continue
        g = [geom(fs[0]["points"], e) for e in EYES]
        rows.append((g[0]["r"] - g[1]["r"], split_score(fs[0]), (g[0]["r"] + g[1]["r"]) / 2, min(g[0]["open"], g[1]["open"])))
    return rows


def verdict(rows):
    ok = np.array([r for r in rows if r is not None and r[3] > 0.16])           # skip blinks and closed eyes
    if len(ok) == 0: return None
    v, s = ok[:, 0].mean(), ok[:, 1].mean()
    res = {"n": len(ok), "vergence": v, "split": s, "split_p90": float(np.percentile(ok[:, 1], 90)), "gaze": ok[:, 2].mean()}
    res["pass"] = s <= PASS["split"] and res["split_p90"] <= PASS["split_p90"]            # vergence is advisory: the landmarks barely follow a 2-3 px iris shift
    return res


def cmd_check(args):
    bad = 0
    for path in args.paths:
        res = verdict(measure(path, args.step))
        if res is None: print(f"{os.path.basename(path):24s} no face found"); bad += 1; continue
        print(f"{os.path.basename(path):24s} {'PASS' if res['pass'] else 'FAIL'}  vergence {res['vergence']:+.3f} (advisory, real person -0.06)  "
              f"split {res['split']:.3f} (<= {PASS['split']})  p90 {res['split_p90']:.2f} (<= {PASS['split_p90']})  gaze {res['gaze']:.3f}  n={res['n']}")
        bad += 0 if res["pass"] else 1
    return 1 if bad else 0


# ------------------------------------------------------------------ the fix
def sclera_colour(crop, M, c, ri):
    gray = crop.mean(2); yy, xx = np.mgrid[0:crop.shape[0], 0:crop.shape[1]]
    far = np.hypot(xx - c[0], yy - c[1]) > 1.5 * ri
    sel = (M > 200) & far
    if sel.sum() < 6: sel = (M > 200)
    if sel.sum() < 3: return np.array([205, 195, 190], np.float32)
    vals = crop[sel]; g = gray[sel]; top = vals[g >= np.percentile(g, 60)]
    return np.median(top, axis=0).astype(np.float32)


def move_iris(frame, geo, dx, dy):
    """frame: RGB uint8, edited in place. Moves the iris disc by (dx, dy) px inside the eye opening."""
    if abs(dx) < 0.05 and abs(dy) < 0.05: return
    c, ri = geo["c"], geo["ri"]; pad = int(4 * ri) + 4
    x0, y0 = int(c[0]) - pad, int(c[1]) - pad; x1, y1 = x0 + 2 * pad, y0 + 2 * pad
    if x0 < 0 or y0 < 0 or x1 > frame.shape[1] or y1 > frame.shape[0]: return
    crop = frame[y0:y1, x0:x1].astype(np.float32); import cv2
    cl = (c - np.array([x0, y0])).astype(np.float32)
    M = np.zeros(crop.shape[:2], np.uint8); cv2.fillPoly(M, [np.round(geo["contour"] - np.array([x0, y0])).astype(np.int32)], 255)
    M = cv2.GaussianBlur(cv2.erode(M, np.ones((3, 3), np.uint8)), (3, 3), 0); m = (M.astype(np.float32) / 255)[..., None]
    yy, xx = np.mgrid[0:crop.shape[0], 0:crop.shape[1]]; d = np.hypot(xx - cl[0], yy - cl[1])
    rad = 1.35 * ri
    soft = np.clip((rad - d) / (0.35 * ri), 0, 1).astype(np.float32)                         # the iris + limbus disc, soft edge
    hole = ((soft > 0.02) & (M > 100)).astype(np.uint8) * 255
    base = cv2.inpaint(np.clip(crop, 0, 255).astype(np.uint8), cv2.dilate(hole, np.ones((3, 3), np.uint8)), 3, cv2.INPAINT_TELEA).astype(np.float32)
    filled = crop * (1 - hole[..., None] / 255.0) + base * (hole[..., None] / 255.0)           # the vacated crescent takes its neighbours' colour
    disc = soft
    T = np.float32([[1, 0, dx], [0, 1, dy]])
    pr = cv2.warpAffine(crop, T, crop.shape[1::-1], flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    pa = cv2.warpAffine(disc, T, crop.shape[1::-1], flags=cv2.INTER_LINEAR)[..., None] * m
    out = filled * (1 - pa) + pr * pa
    frame[y0:y1, x0:x1] = np.clip(out, 0, 255).astype(np.uint8)


def smooth(a, med=5, sig=1.3):
    from scipy.ndimage import median_filter, gaussian_filter1d
    return gaussian_filter1d(median_filter(a, size=med, mode="nearest"), sig, mode="nearest")


def plan(path, target):
    """pass 1: landmarks for every frame -> smoothed pixel shifts (n, 2 eyes, 2 xy) and the geometry to apply them"""
    geos, n = [], 0
    for rgb in frames_of(path):
        fs = F.analyse(rgb); n += 1
        geos.append([geom(fs[0]["points"], e) for e in EYES] if fs else None)
    ok = [i for i, g in enumerate(geos) if g]
    if not ok: return geos, np.zeros((n, 2, 2))
    for i in range(n):                                                                         # a missed face reuses the nearest one
        if geos[i] is None: geos[i] = geos[min(ok, key=lambda j: abs(j - i))]
    r = np.array([[g[0]["r"], g[1]["r"]] for g in geos]); v = np.array([[g[0]["v"], g[1]["v"]] for g in geos])
    op = np.array([[g[0]["open"], g[1]["open"]] for g in geos]).min(1)
    g_meas = smooth(r.mean(1)); off = g_meas - target
    g_t = target + np.where(np.abs(off) < 0.06, 0.0, off - np.sign(off) * 0.06)                # a deliberate look-away keeps its direction
    r_t = np.stack([g_t - BASE_V / 2, g_t + BASE_V / 2], 1); v_t = np.repeat(smooth(v.mean(1))[:, None], 2, 1)
    gate = smooth(np.clip((op - 0.12) / 0.08, 0, 1), med=3, sig=1.0)                             # no change during a blink
    dx = np.stack([(r_t[:, k] - r[:, k]) * np.array([g[k]["w"] for g in geos]) for k in (0, 1)], 1)
    dy = np.stack([(v_t[:, k] - v[:, k]) * np.array([g[k]["h"] for g in geos]) for k in (0, 1)], 1)
    lim = np.array([[0.35 * g[k]["w"] for k in (0, 1)] for g in geos])
    dx = np.clip(np.stack([smooth(dx[:, 0]), smooth(dx[:, 1])], 1), -lim, lim) * gate[:, None]
    dy = np.clip(np.stack([smooth(dy[:, 0]), smooth(dy[:, 1])], 1), -0.25 * lim, 0.25 * lim) * gate[:, None]
    return geos, np.stack([dx, dy], 2)


def cmd_fix(args):
    w, h, fps = probe(args.inp)
    geos, sh = plan(args.inp, args.gaze)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", f"{fps:.4f}", "-i", "-",
                            "-i", args.inp, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p",
                            "-c:a", "copy", "-shortest", args.out], stdin=subprocess.PIPE)
    mx = 0.0
    for i, rgb in enumerate(frames_of(args.inp)):
        g = geos[min(i, len(geos) - 1)]
        for k in (0, 1):
            move_iris(rgb, g[k], sh[min(i, len(sh) - 1), k, 0], sh[min(i, len(sh) - 1), k, 1]); mx = max(mx, abs(sh[min(i, len(sh) - 1), k, 0]))
        enc.stdin.write(np.ascontiguousarray(rgb).tobytes())
    enc.stdin.close(); enc.wait()
    print(f"wrote {args.out}  (largest horizontal iris shift {mx:.1f} px at {w}x{h})")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    c = sp.add_parser("check"); c.add_argument("paths", nargs="+"); c.add_argument("--step", type=int, default=3, help="analyse every Nth frame")
    f = sp.add_parser("fix"); f.add_argument("inp"); f.add_argument("out"); f.add_argument("--gaze", type=float, default=GAZE_LENS)
    a = ap.parse_args()
    sys.exit(cmd_check(a) if a.cmd == "check" else cmd_fix(a))


if __name__ == "__main__":
    main()
