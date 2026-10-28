#!/usr/bin/env python3
"""A light-makeup skin pass for a generated talking clip (anthropic01, 2026-10-28: Akhilesh saw Rashmi's face as dull,
"no makeup", with spots that read as acne). Wan adds small dark specks to the cheeks and forehead and flattens the
skin; this evens it the way foundation and a little glow would, on the FACE ONLY:
  1. a skin mask from MediaPipe's face mesh: the face oval, minus the eyes, brows and lips (dilated), feathered, so the
     mouth that lip sync is judged on is never touched;
  2. speck removal: a morphological closing of the lightness fills dark dots smaller than about 9 px; only where the
     closing is lighter by more than SPOT_T is the dot replaced;
  3. even tone: an edge-preserving (bilateral) smooth blended at SMOOTH inside the mask, so some texture stays;
  4. glow: the skin a little lighter and warmer (GLOW lightness, a touch of rose).
  --ref KEYFRAME: also bring the clip back to the approved look it started from ("she was fair, now she looks dark and
  uneven"): the whole frame's exposure and colour toward the keyframe, then the skin's own tone and evenness (its
  lightness spread) toward the keyframe's skin. Hair is left out of the skin mask (MediaPipe's hair class).
  --forehead-only: only the forehead creases (see forehead()); the made-up look from the keyframe stays untouched. Akhilesh
  (2026-10-28) wants character, not plastic skin: with a made-up keyframe this is the only pass to use.
Audio is copied unchanged.  Usage: skinfix.py IN.mp4 OUT.mp4 [--ref KF.png] [--smooth 0.5] [--glow 3] [--test 1]
                                  [--forehead-only]"""
import argparse, os, subprocess, sys
import numpy as np
import cv2
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from common import FFMPEG  # noqa: E402
from face import landmarker  # noqa: E402

OVAL = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150,
        136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]
EYES = [[263, 249, 390, 373, 374, 380, 381, 382, 362, 398, 384, 385, 386, 387, 388, 466],
        [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]]
BROWS = [[276, 283, 282, 295, 285, 300, 293, 334, 296, 336], [46, 53, 52, 65, 55, 70, 63, 105, 66, 107]]
LIPS = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 409, 270, 269, 267, 0, 37, 39, 40, 185]
SPOT_T = 4.0


_SEG = {}


def hair(rgb):
    import mediapipe as mp
    if "s" not in _SEG:
        root = os.path.dirname(here)
        _SEG["s"] = mp.tasks.vision.ImageSegmenter.create_from_options(mp.tasks.vision.ImageSegmenterOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=os.path.join(root, "assets/models/selfie_multiclass_256x256.tflite")),
            running_mode=mp.tasks.vision.RunningMode.IMAGE, output_category_mask=True))
    cat = _SEG["s"].segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb))).category_mask.numpy_view()
    return cv2.resize((cat == 1).astype(np.uint8) * 255, (rgb.shape[1], rgb.shape[0]), interpolation=cv2.INTER_NEAREST)


def skin_mask(rgb):
    import mediapipe as mp
    H, W = rgb.shape[:2]
    res = landmarker().detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb)))
    if not res.face_landmarks: return None
    lm = res.face_landmarks[0]; P = lambda ids: np.array([[lm[i].x * W, lm[i].y * H] for i in ids], np.int32)
    face_h = P(OVAL)[:, 1].ptp(); k = max(3, int(face_h * 0.035)) | 1
    oval = P(OVAL).astype(np.float32); cy = oval[:, 1].mean()
    up = oval[oval[:, 1] < cy].copy(); up[:, 1] -= face_h * 0.16       # the face outline stops short of the hairline: reach up
    m = np.zeros((H, W), np.uint8); cv2.fillPoly(m, [cv2.convexHull(np.vstack([oval, up]).astype(np.int32))], 255)
    cut = np.zeros((H, W), np.uint8)
    for ids in EYES + BROWS: cv2.fillPoly(cut, [cv2.convexHull(P(ids))], 255)
    cv2.fillPoly(cut, [cv2.convexHull(P(LIPS))], 255)
    cut = cv2.dilate(cut, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k * 2 + 1, k * 2 + 1)))
    cut = cv2.max(cut, cv2.dilate(hair(rgb), np.ones((7, 7), np.uint8)))      # strands over the cheek stay hair
    m = cv2.subtract(m, cut).astype(np.float32) / 255
    m = cv2.GaussianBlur(m, (0, 0), max(2.0, face_h * 0.012))
    brow_y = min(P(b)[:, 1].min() for b in BROWS)
    fore = np.clip((brow_y - np.arange(H, dtype=np.float32)) / max(4.0, face_h * 0.05), 0, 1)[:, None] * m   # above the brows
    skin_mask.last = (fore, face_h)
    return m


def stats(rgb, m=None):
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32).reshape(-1, 3)
    if m is not None:
        sel = m.reshape(-1) > 0.6; lab = lab[sel]
    return lab.mean(0), lab.std(0)


def look_match(rgb, P):
    """the whole frame toward the keyframe (exposure and colour), then the skin toward the keyframe's skin"""
    if not P: return rgb
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    (gm, gs), (rm, rs) = P["clip_g"], P["ref_g"]
    lab[..., 0] = (lab[..., 0] - gm[0]) * (1 + 0.5 * (rs[0] / gs[0] - 1)) + gm[0]
    lab += 1.0 * (rm - gm)
    m = P.get("mask")
    if m is not None:
        (sm, ss), (tm, ts) = P["clip_s"], P["ref_s"]
        sm2 = sm + 1.0 * (rm - gm)
        L = lab[..., 0]; r = min(1.0, ts[0] / ss[0])
        Ls = (L - sm2[0]) * r + tm[0]                                   # even the skin's lightness and set its level
        lab[..., 0] = L + (Ls - L) * m * 0.95
        for c in (1, 2): lab[..., c] += (tm[c] - sm2[c]) * m * 0.7
    return cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB)


def forehead(rgb, amount=1.0, spots=False):
    """--forehead-only: Wan creases her forehead when the brows lift (a mid-20s face). Take out only the creases' band of
    detail (a few px to about 3% of the face height) above the brows; pores, grain and freckles elsewhere stay as made.
    --spots also fills the small dark dots Wan adds on the nose and cheeks (Akhilesh reads freckles as marks), with the
    same closing as fix() and nothing else: no smoothing, no glow."""
    m = skin_mask(rgb)
    if m is None: return rgb
    fore, face_h = skin_mask.last
    if spots:
        lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32); L = lab[..., 0]
        closed = cv2.morphologyEx(L, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
        spot = np.clip((closed - L - SPOT_T) / 6.0, 0, 1); spot = cv2.GaussianBlur(spot, (0, 0), 1.2) * m
        lab[..., 0] = L + (closed - L) * spot
        rgb = cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB)
    x = rgb.astype(np.float32)
    fine = cv2.GaussianBlur(x, (0, 0), 0.6)                              # below this: grain, kept
    wide = cv2.GaussianBlur(x, (0, 0), max(5.0, face_h * 0.03))          # above this: tone and shading, kept
    out = x - (fine - wide) * (amount * fore)[..., None]                 # the band between: creases, removed
    return np.clip(out, 0, 255).astype(np.uint8)


def fix(rgb, smooth=0.5, glow=5.0, P=None):
    m = skin_mask(rgb)
    if m is None: return look_match(rgb, P)
    if P is not None: P = dict(P, mask=m)
    rgb = look_match(rgb, P)
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32); L = lab[..., 0]
    closed = cv2.morphologyEx(L, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    spot = np.clip((closed - L - SPOT_T) / 6.0, 0, 1); spot = cv2.GaussianBlur(spot, (0, 0), 1.2) * m
    lab[..., 0] = L + (closed - L) * spot
    out = cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB).astype(np.float32)
    bil = cv2.bilateralFilter(out.astype(np.uint8), 9, 22, 7).astype(np.float32)
    out = out + (bil - out) * (m * smooth)[..., None]
    # fine lines (Wan creases her forehead when the brows lift; she is in her mid-20s): turn the fine detail down,
    # strongly above the brows, gently on the rest of the skin so some pores stay
    fore, face_h = skin_mask.last
    low = cv2.GaussianBlur(out, (0, 0), max(2.0, face_h * 0.011))
    cutw = np.clip(0.45 * m, 0, 0.9)[..., None]
    out = low + (out - low) * (1 - cutw)
    wide = cv2.GaussianBlur(out, (0, 0), max(5.0, face_h * 0.03))      # forehead creases are a few px wide: a wider blur there
    out = out + (wide - out) * (0.85 * fore)[..., None]
    lab = cv2.cvtColor(np.clip(out, 0, 255).astype(np.uint8), cv2.COLOR_RGB2LAB).astype(np.float32)
    lab[..., 0] += glow * m; lab[..., 1] += 1.5 * m; lab[..., 2] -= 1.0 * m          # lighter, a touch of rose, a little less orange
    return cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB)


def main():
    p = argparse.ArgumentParser(); p.add_argument("src"); p.add_argument("out")
    p.add_argument("--smooth", type=float, default=0.5); p.add_argument("--glow", type=float, default=5.0); p.add_argument("--test")
    p.add_argument("--ref"); p.add_argument("--forehead-only", action="store_true")
    p.add_argument("--spots", action="store_true", help="with --forehead-only: also fill small dark dots")
    a = p.parse_args()
    if a.forehead_only: a.ref = None
    step = (lambda fr, P: forehead(fr, spots=a.spots)) if a.forehead_only else (lambda fr, P: fix(fr, a.smooth, a.glow, P))

    def params(first):
        if not a.ref: return None
        ref = cv2.cvtColor(cv2.imread(a.ref), cv2.COLOR_BGR2RGB); ref = cv2.resize(ref, (first.shape[1], first.shape[0]))
        mr, mc = skin_mask(ref), skin_mask(first)
        return {"ref_g": stats(ref), "clip_g": stats(first), "ref_s": stats(ref, mr), "clip_s": stats(first, mc)}
    if a.test:
        rgb = cv2.cvtColor(cv2.imread(a.src), cv2.COLOR_BGR2RGB)
        cv2.imwrite(a.out, cv2.cvtColor(step(rgb, params(rgb)), cv2.COLOR_RGB2BGR)); print(a.out); return
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate",
                            "-of", "csv=p=0", a.src], capture_output=True, text=True).stdout.strip().split(",")
    W, H, fps = int(probe[0]), int(probe[1]), probe[2]
    dec = subprocess.Popen([FFMPEG, "-v", "error", "-i", a.src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    tmp = a.out + ".v.mp4"
    enc = subprocess.Popen([FFMPEG, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", fps, "-i", "-",
                            "-c:v", "libx264", "-crf", "13", "-preset", "medium", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    n = 0; P = None
    while True:
        buf = dec.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy()
        if n == 0: P = params(fr)                                       # one set of corrections for the whole clip: no flicker
        enc.stdin.write(step(fr, P).tobytes()); n += 1
    enc.stdin.close(); enc.wait(); dec.wait()
    subprocess.run([FFMPEG, "-v", "error", "-y", "-i", tmp, "-i", a.src, "-map", "0:v", "-map", "1:a?", "-c", "copy", a.out], check=True)
    os.remove(tmp); print(f"{a.out}: {n} frames")


if __name__ == "__main__":
    main()
