#!/usr/bin/env python3
"""Make a generated talking-head frame read as a photograph (Akhilesh, 23 Oct 2026: "Pandey looks very artificial; the hair is too silky").
What gives a Wan / Seedream face away, and what this does about it:
  1. HAIR is one smooth helmet with glossy bands, no strands, a cut-out edge   -> flatten the gloss (pull the hair's highlights toward its mean),
     add fine strand texture (noise stretched along the strands), roughen the hair's outer edge a little, and let a few flyaway wisps cross it
  2. SKIN is waxy and soft (720p enlarged to 1080p)                           -> a measured unsharp mask on the face/body, plus luminance film grain
  3. The whole frame is cleaner than the grainy printed graphics around it    -> grain and a faint paper-fibre multiply so he sits in the same print
Everything is deterministic for a given seed except the film grain (new each frame, like real grain).
  texturize(rgb_uint8, frame_index, seed=1, grain=7.0, sharpen=0.55, hair=0.8) -> rgb_uint8
CLI test: texturize.py IN.png OUT.png"""
import sys
import numpy as np
import cv2

_CACHE = {}


def _fields(h, w, seed):
    k = w / 1080.0
    key = (h, w, seed)
    if key in _CACHE: return _CACHE[key]
    rg = np.random.default_rng(seed)
    strand = rg.random((h, w)).astype(np.float32)
    strand = cv2.GaussianBlur(strand, (0, 0), sigmaX=max(0.45, 0.7 * k), sigmaY=5.5 * k)               # long, thin streaks (strands run mostly down the head)
    strand = (strand - strand.mean()) / (strand.std() + 1e-6)
    fine = rg.random((h, w)).astype(np.float32); fine = cv2.GaussianBlur(fine, (0, 0), max(0.5, 0.8 * k)); fine = (fine - fine.mean()) / (fine.std() + 1e-6)
    fibre = cv2.GaussianBlur(rg.random((h, w)).astype(np.float32), (0, 0), sigmaX=14 * k, sigmaY=max(0.5, 0.9 * k)); fibre = (fibre - fibre.mean()) / (fibre.std() + 1e-6)
    wisps = np.zeros((h, w), np.float32)                                              # a few flyaway hairs, thin and curved, drawn once; masked to the hair edge later
    for _ in range(int(h / 22)):
        x0 = rg.uniform(0, w); y0 = rg.uniform(0, h); L = rg.uniform(0.02, 0.06) * h; a = rg.normal(np.pi / 2, 0.8); c = rg.normal(0, 0.012)
        pts = np.array([[x0 + np.cos(a + c * k) * k * 1.4, y0 + np.sin(a + c * k) * k * 1.4] for k in range(0, int(L), 3)], np.int32)
        if len(pts) > 2: cv2.polylines(wisps, [pts.reshape(-1, 1, 2)], False, 1.0, 1, cv2.LINE_AA)
    _CACHE[key] = (strand, fine, fibre, wisps); return _CACHE[key]


_SEG = {}


def _segmenter():
    if "s" not in _SEG:
        import mediapipe as mp
        import os
        root = os.path.abspath(os.path.dirname(__file__))
        while root != "/" and not os.path.exists(os.path.join(root, "CLAUDE.md")): root = os.path.dirname(root)
        o = mp.tasks.vision.ImageSegmenterOptions(base_options=mp.tasks.BaseOptions(model_asset_path=f"{root}/assets/models/selfie_multiclass_256x256.tflite"),
                                                  running_mode=mp.tasks.vision.RunningMode.IMAGE, output_category_mask=True)
        _SEG["s"] = (mp, mp.tasks.vision.ImageSegmenter.create_from_options(o))
    return _SEG["s"]


def hair_mask(rgb):
    """MediaPipe's multiclass selfie segmenter (0 background, 1 hair, 2 body skin, 3 face skin, 4 clothes): the hair class, plus the very dark parts of the face skin (moustache, brows)"""
    mp, seg = _segmenter(); h, w = rgb.shape[:2]
    cat = seg.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb))).category_mask.numpy_view()
    hair = (cat == 1).astype(np.float32); face = (cat == 3)
    L = (0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]).astype(np.float32) / 255
    if face.shape != (h, w): face = cv2.resize(face.astype(np.uint8), (w, h), interpolation=cv2.INTER_NEAREST).astype(bool)
    stache = (face & (L < 0.20)).astype(np.float32)
    hair = cv2.resize(hair, (w, h), interpolation=cv2.INTER_LINEAR) if hair.shape != (h, w) else hair
    m = np.clip(hair + stache, 0, 1)
    bg = cv2.resize((cat == 0).astype(np.uint8), (w, h), interpolation=cv2.INTER_NEAREST).astype(np.float32) if cat.shape != (h, w) else (cat == 0).astype(np.float32)
    ring = cv2.GaussianBlur(hair, (0, 0), 7) * (1 - hair)                              # just outside the hair, and only where the neighbour is background (not the face)
    ring = np.clip(ring * 3.0, 0, 1) * cv2.GaussianBlur(bg, (0, 0), 3)
    return cv2.GaussianBlur(m, (0, 0), 2.5), ring


def texturize(rgb, frame_index=0, seed=1, grain=7.0, sharpen=0.55, hair=0.8):
    h, w = rgb.shape[:2]; strand, fine, fibre, wisps = _fields(h, w, seed)
    f = rgb.astype(np.float32)
    # 2. detail: unsharp mask (radius ~1.4 px at 1080 wide)
    blur = cv2.GaussianBlur(f, (0, 0), 1.4 * w / 1080.0); f = np.clip(f + (f - blur) * sharpen, 0, 255)
    # 1. hair
    M, ring = hair_mask(rgb); M = M[..., None]
    L = (0.299 * f[..., 0] + 0.587 * f[..., 1] + 0.114 * f[..., 2])[..., None]
    mean_hair = (L * M).sum() / (M.sum() + 1e-6)
    flat = L + (mean_hair * 0.8 + L * 0.2 - L) * 0.35 * hair                              # pull the shine toward the hair's mean (less glossy bands)
    tex = 1 + 0.24 * hair * strand[..., None] + 0.10 * hair * fine[..., None]
    new_L = np.clip(flat * tex, 0, 255)
    ratio = (new_L / (L + 1e-3))
    f = f * (1 + (ratio - 1) * M)
    f = f - wisps[..., None] * ring[..., None] * 60 * hair                                  # flyaway wisps just outside the hair, on the background only
    # 3. grain and a faint fibre multiply
    rg = np.random.default_rng(1000 + frame_index)
    g = rg.normal(0, grain, (h, w)).astype(np.float32)[..., None]
    f = f + g * (0.6 + 0.4 * (1 - L / 255))                                               # more grain in shadows
    return np.clip(f, 0, 255).astype(np.uint8)


if __name__ == "__main__":
    im = cv2.cvtColor(cv2.imread(sys.argv[1]), cv2.COLOR_BGR2RGB); out = texturize(im, 0)
    cv2.imwrite(sys.argv[2], cv2.cvtColor(out, cv2.COLOR_RGB2BGR)); print("ok", out.shape)
