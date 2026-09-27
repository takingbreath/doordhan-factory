#!/usr/bin/env python3
"""The Doordhan picture: an off-air 1990s Indian TV look (PAL, CRT, a bit of VHS), applied at the very end.
Generated clips come out crisp and modern; making the edit smaller only blurs them. Old TV had its own failures,
and this builds those on purpose, in this order:
  milky blacks and soft whites, faded warm colour -> SD resolution (about 400 pixels across) -> edge-enhancement
  halos -> colour that bleeds sideways and sits a little right of the picture -> a faint antenna ghost -> chunky
  grain made at SD size -> soft upscale to 1080x1920 -> highlight bloom -> 640 soft scanlines -> CRT vignette.
Presets: broadcast (default: a clean Doordarshan-style off-air picture), vhs (a worn tape of it: teleshop,
old recordings), kendra (Sahayata Kendra: clearer, fine grain), clean (the Sept 2026 finish: fine grain and colour fringe only).
Preview on any clip:  look.py IN.mp4 OUT.mp4 [--preset vhs]   (writes OUT and a side-by-side OUT_compare.png)"""
import argparse, os, tempfile
import numpy as np
from PIL import Image

PRESETS = {
    #            SD size      chroma bleed/shift  ghost px/amount  halo  grain  colour: sat, black lift, mid (offsets the
    #            scanlines' ~10% darkening), white top, warm
    "broadcast": dict(sd=(400, 712), cblur=7, cshift=3, ghost=(6, 0.045), halo=0.6, grain=16, cgrain=5,
                      sat=1.12, lift=0.05, mid=0.60, top=0.96, warm=0.02, bloom=0.18, scan=0.20, vignette=0.22),
    "vhs":       dict(sd=(320, 570), cblur=11, cshift=5, ghost=(9, 0.06), halo=0.9, grain=20, cgrain=8,
                      sat=0.98, lift=0.07, mid=0.57, top=0.93, warm=0.045, bloom=0.24, scan=0.24, vignette=0.42),
    # Sahayata Kendra (Akhilesh 2026-09-27: "the grain is too huge, make it a little clearer"): same 90s colour,
    # "and the colours brighter, it looks very dull"): sharper SD (about 540 across), fine grain, lighter bleed,
    # ghost and scanlines; richer colour, near-black blacks and lifted mids instead of the milky off-air fade.
    "kendra":    dict(sd=(540, 960), cblur=4, cshift=2, ghost=(4, 0.025), halo=0.4, grain=6, cgrain=2,
                      sat=1.32, lift=0.015, mid=0.63, top=1.0, warm=0.025, bloom=0.12, scan=0.08, vignette=0.16),
    "clean": None,
}
OUT_W, OUT_H = 1080, 1920


def scanline_mask(path, strength, pitch=3):
    """RGBA overlay: soft dark rows every `pitch` px (640 lines at 1920 high, about a PAL raster).
    A sine profile rather than hard lines, so it doesn't moire when a phone rescales the video."""
    y = np.arange(OUT_H)
    a = strength * (0.5 - 0.5 * np.cos(2 * np.pi * y / pitch))
    alpha = np.repeat((a * 255).astype(np.uint8)[:, None], OUT_W, axis=1)
    img = np.zeros((OUT_H, OUT_W, 4), np.uint8); img[..., 3] = alpha
    Image.fromarray(img, "RGBA").save(path)
    return path


def filtergraph(preset, src="[0:v]", mask="[1:v]", out="[v]"):
    """filter_complex string. Needs the scanline mask as a looped second input (see scanline_mask)."""
    p = PRESETS[preset]
    if p is None:
        return (f"{src}noise=alls=7:allf=t,rgbashift=rh=1:bh=-1,gblur=sigma=0.35,"
                f"scale={OUT_W}:{OUT_H}:flags=lanczos,format=yuv420p{out}")
    sw, sh = p["sd"]; gx, ga = p["ghost"]; w = p["warm"]
    return (
        f"{src}format=gbrp,curves=master='0/{p['lift']} 0.5/{p['mid']} 1/{p['top']}',"
        f"colorbalance=rs={w}:bs={-w}:rm={w / 2}:bm={-w / 2},eq=saturation={p['sat']},"
        f"scale={sw}:{sh}:flags=area,unsharp=5:5:{p['halo']}:5:5:0,"
        f"format=yuv444p,avgblur=sizeX={p['cblur']}:sizeY=1:planes=6,chromashift=cbh={p['cshift']}:crh={p['cshift']},"
        f"split[lk_a][lk_b];[lk_b]crop=iw-{gx}:ih:0:0,pad=iw+{gx}:ih:{gx}:0[lk_g];"
        f"[lk_a][lk_g]blend=all_expr='A*{1 - ga:.3f}+B*{ga:.3f}',"
        f"noise=c0s={p['grain']}:c0f=t+u:c1s={p['cgrain']}:c1f=t:c2s={p['cgrain']}:c2f=t,"
        f"scale={OUT_W}:{OUT_H}:flags=bicubic,format=gbrp,split[lk_c][lk_d];"
        f"[lk_d]curves=master='0/0 0.72/0 1/1',gblur=sigma=22[lk_glow];"
        f"[lk_c][lk_glow]blend=all_mode=screen:all_opacity={p['bloom']},format=yuv444p[lk_e];"
        f"[lk_e]{mask}overlay=0:0:shortest=1,vignette=angle={p['vignette']},format=yuv420p{out}")


if __name__ == "__main__":
    import subprocess, sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from common import FFMPEG, run
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out"); ap.add_argument("--preset", default="broadcast", choices=PRESETS)
    ap.add_argument("--at", type=float, default=1.5, help="time for the comparison frame")
    a = ap.parse_args()
    mask = scanline_mask(os.path.join(tempfile.mkdtemp(), "scan.png"), (PRESETS[a.preset] or {}).get("scan", 0))
    run([FFMPEG, "-y", "-v", "error", "-i", a.src, "-loop", "1", "-i", mask, "-filter_complex",
         filtergraph(a.preset), "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
         "-c:a", "aac", "-b:a", "192k", a.out])
    cmp_png = os.path.splitext(a.out)[0] + "_compare.png"
    run([FFMPEG, "-y", "-v", "error", "-ss", str(a.at), "-i", a.src, "-ss", str(a.at), "-i", a.out, "-filter_complex",
         f"[0:v]scale={OUT_W // 2}:{OUT_H // 2}[x];[1:v]scale={OUT_W // 2}:{OUT_H // 2}[y];[x][y]hstack",
         "-frames:v", "1", cmp_png])
    print(f"{a.out} ({a.preset}); before/after frame: {cmp_png}")
