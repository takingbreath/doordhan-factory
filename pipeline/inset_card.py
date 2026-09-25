#!/usr/bin/env python3
"""Logo card for the anchor's inset box (the opening frame must show what the reel is about).
  inset_card.py card LOGO.png OUT.png [--label IPO] [--size 170 162]
  inset_card.py overlay CLIP.mp4 CARD.png OUT.mp4 [--at X Y]   (default: auto-detect the navy inset box)
--size and --at are in the 480x854 analysis frame (as documented in formats/); the card is rendered at edit resolution.
Use the company's official logo (e.g. from Wikimedia). Never let an image model draw a real logo."""
import argparse, os, subprocess, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from common import FFMPEG, W, H, AW, AH, S, FPS, run

FONTS = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
         "/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/Library/Fonts/Arial Bold.ttf",
         "C:/Windows/Fonts/arialbd.ttf"]


def font(size):
    for f in FONTS:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def make_card(logo, out, label, size):
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    cw, ch = round(size[0] * S), round(size[1] * S)
    card = Image.new("RGB", (cw, ch), (238, 233, 218))
    d = ImageDraw.Draw(card)
    d.rectangle([0, 0, cw - 1, ch - 1], outline=(24, 40, 110), width=round(4 * S))
    lg = Image.open(logo).convert("RGBA")
    lw = cw - round(22 * S)
    lh = round(lg.height * lw / lg.width)
    if label and lh > ch * 0.45:
        lh = int(ch * 0.45); lw = round(lg.width * lh / lg.height)
    lg = lg.resize((lw, lh), Image.LANCZOS)
    top = round(30 * S) if label else (ch - lh) // 2
    card.paste(lg, ((cw - lw) // 2, top), lg)
    if label:
        f = font(round(34 * S))
        tw = d.textlength(label, font=f)
        d.text(((cw - tw) / 2, top + lh + round(14 * S)), label, font=f, fill=(24, 40, 110))
    card.filter(ImageFilter.GaussianBlur(0.6 * S)).save(out)
    print(f"card {out} {cw}x{ch}")


def detect_box(clip, t=1.0):
    tmp = os.path.join(tempfile.mkdtemp(), "f.png")
    run([FFMPEG, "-y", "-v", "error", "-ss", str(t), "-i", clip, "-frames:v", "1", "-vf", f"scale={AW}:{AH}", tmp])
    im = np.array(Image.open(tmp).convert("RGB")).astype(int)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    m = (b > r + 25) & (b > g + 10) & (r < 90) & (g < 110)
    m[:, : AW // 2] = False; m[AH // 3:, :] = False
    if m.sum() < 500:
        return None
    cols, rows = m.sum(0), m.sum(1)
    xs = np.where(cols > 0.5 * cols.max())[0]; ys = np.where(rows > 0.5 * rows.max())[0]
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def overlay(clip, card, out, at):
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    if at:
        at = (round(at[0] * S), round(at[1] * S))
    else:
        box = detect_box(clip)
        if box is None:
            raise SystemExit("inset box not found; pass --at X Y")
        cw, ch = Image.open(card).size
        x0, y0, x1, y1 = box
        at = (round((x0 + x1) / 2 * S) - cw // 2, round((y0 + y1) / 2 * S) - ch // 2)
        print(f"inset box {box} (480 frame) -> card at {at} ({W}x{H} frame)")
    run([FFMPEG, "-y", "-v", "error", "-i", clip, "-loop", "1", "-i", card, "-filter_complex",
         f"[0:v]scale={W}:{H}:flags=lanczos,fps={FPS},setsar=1[b];[1:v]format=rgba,noise=alls=6:allf=t[c];"
         f"[b][c]overlay={at[0]}:{at[1]}:shortest=1,format=yuv420p[v]",
         "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-crf", "16", "-c:a", "copy", out])
    print(out)


p = argparse.ArgumentParser()
sub = p.add_subparsers(dest="cmd", required=True)
c = sub.add_parser("card"); c.add_argument("logo"); c.add_argument("out")
c.add_argument("--label", default=""); c.add_argument("--size", nargs=2, type=int, default=[170, 162])
o = sub.add_parser("overlay"); o.add_argument("clip"); o.add_argument("card"); o.add_argument("out")
o.add_argument("--at", nargs=2, type=int)
a = p.parse_args()
if a.cmd == "card":
    make_card(a.logo, a.out, a.label, a.size)
else:
    overlay(a.clip, a.card, a.out, a.at)
