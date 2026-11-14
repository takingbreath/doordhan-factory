#!/usr/bin/env python3
"""Vox filter for a cut-out PHOTO (Akhilesh, 23 Oct 2026: Vox shoots a real, rusty object and filters it so it sits in the composition).
The three textures of the reference sheet are applied in this order:
  1. DIRTY HALFTONE  an AM dot screen at 45 degrees whose threshold is disturbed by blotchy grunge, so dots are uneven and some are missing
  2. SCANNER LINES   thin horizontal streaks of different length (light, and a few dark), as from a dirty flatbed
  3. PAPER FIBRES    a multiply of long soft fibres and fine grain, plus dust specks
then a warm two-tone (ink -> aged paper) with an optional amount of the photo's own colour kept (rust stays rust).
  pipeline/qcpy work/sk05/vox_filter.py IN.png OUT.png [--color 0.3] [--dots 120] [--mix 0.6] [--seed 1] [--ink 22,20,24] [--paper 242,236,218]
IN must be RGBA (a cut-out); the alpha is kept (eroded 1 px so no white halo)."""
import argparse
import numpy as np
from PIL import Image, ImageFilter


def blotch(h, w, cell, rg, octaves=1):
    out = np.zeros((h, w), np.float32)
    for o in range(octaves):
        c = max(2.0, cell / (2 ** o)); sm = rg.random((max(2, int(h / c)), max(2, int(w / c)))).astype(np.float32)
        out += np.asarray(Image.fromarray((sm * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(np.float32) / 255 / (2 ** o)
    return out / sum(1 / (2 ** o) for o in range(octaves))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--color", type=float, default=0.3, help="how much of the photo's own colour stays (0 = pure two-tone)")
    ap.add_argument("--dots", type=float, default=120, help="halftone cells across the picture width")
    ap.add_argument("--mix", type=float, default=0.6, help="how much of the result is halftone (the rest is the toned photo)")
    ap.add_argument("--seed", type=int, default=1); ap.add_argument("--ink", default="22,20,24"); ap.add_argument("--paper", default="242,236,218")
    ap.add_argument("--maxw", type=int, default=1100)
    a = ap.parse_args(); rg = np.random.default_rng(a.seed)
    im = Image.open(a.src).convert("RGBA")
    if im.width > a.maxw: im = im.resize((a.maxw, int(im.height * a.maxw / im.width)), Image.LANCZOS)
    arr = np.asarray(im).astype(np.float32) / 255; rgb, alpha = arr[..., :3], arr[..., 3]; h, w = alpha.shape
    L = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    m = alpha > 0.5
    lo, hi = np.percentile(L[m], [2, 98]); L = np.clip((L - lo) / (hi - lo + 1e-6), 0, 1); L = np.clip((L - 0.5) * 1.22 + 0.5, 0, 1)
    # 1. dirty halftone
    cell = max(3.0, w / a.dots); yy, xx = np.mgrid[0:h, 0:w].astype(np.float32); th = np.pi / 4
    u = (xx * np.cos(th) + yy * np.sin(th)) / cell; v = (-xx * np.sin(th) + yy * np.cos(th)) / cell; pat = (np.cos(2 * np.pi * u) + np.cos(2 * np.pi * v)) / 4 + 0.5
    grunge = blotch(h, w, cell * 9, rg, 2) * 0.34 + blotch(h, w, cell * 1.3, rg) * 0.12
    ht = np.clip((L - pat * 0.92 + (grunge - 0.2)) * 6.5 + 0.5, 0, 1)
    Lf = L * (1 - a.mix) + ht * a.mix
    # 2. scanner lines: a handful of long thin streaks, mostly light, a few dark
    streak = np.zeros((h, w), np.float32)
    for _ in range(int(h / 26)):
        y = rg.integers(0, h); t = rg.integers(1, 3); x0 = rg.integers(0, int(w * 0.7)); x1 = min(w, x0 + rg.integers(int(w * 0.15), int(w * 0.8))); s = rg.choice([1, 1, 1, -1]) * rg.uniform(0.25, 0.6)
        streak[y:y + t, x0:x1] += s
    streak = np.asarray(Image.fromarray(np.clip((streak + 1) * 127, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))).astype(np.float32) / 127 - 1
    Lf = np.clip(Lf + streak * 0.5, 0, 1)
    # 3. paper fibres (long, soft) and fine grain, dust
    fibre = np.asarray(Image.fromarray((blotch(h, w, 3, rg) * 255).astype(np.uint8)).resize((w, h)).filter(ImageFilter.GaussianBlur(0.5)).filter(ImageFilter.BoxBlur(1))).astype(np.float32) / 255
    long_f = np.asarray(Image.fromarray((rg.random((max(2, h // 2), max(2, w // 40))) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(np.float32) / 255
    Lf = np.clip(Lf * (1 - 0.14 * (fibre - 0.5) - 0.10 * (long_f - 0.5)) , 0, 1)
    dust = (rg.random((h, w)) > 0.9993).astype(np.float32); dust = np.asarray(Image.fromarray((dust * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))).astype(np.float32) / 255 * 6
    Lf = np.clip(Lf - dust * 0.6 + (np.asarray(Image.fromarray((((rg.random((h, w)) > 0.9996) * 255).astype(np.uint8))).filter(ImageFilter.GaussianBlur(0.9))).astype(np.float32) / 255) * 4, 0, 1)
    ink = np.array([int(x) for x in a.ink.split(",")], np.float32); paper = np.array([int(x) for x in a.paper.split(",")], np.float32)
    out = ink + (paper - ink) * Lf[..., None]
    if a.color > 0:                                                    # the photo's own colour, levelled, printed through the same screen
        mx = rgb.max(2, keepdims=True); mn = rgb.min(2, keepdims=True); sat = (mx - mn) / (mx + 1e-4)
        colr = np.clip((rgb - lo) / (hi - lo + 1e-6), 0, 1) * 255 * (0.55 + 0.45 * Lf[..., None])
        out = out * (1 - a.color * np.clip(sat * 1.6, 0, 1)) + colr * (a.color * np.clip(sat * 1.6, 0, 1))
    al = Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3))
    res = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert("RGBA"); res.putalpha(al); res.save(a.out); print(a.out, res.size)


if __name__ == "__main__":
    main()
