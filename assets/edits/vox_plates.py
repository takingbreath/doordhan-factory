#!/usr/bin/env python3
"""The house paper plates for the Vox-style collage (assets/edits/jio01_vox.py reads them when an episode has none of
its own): warm kraft paper with fibres and grain, torn coloured scraps at the edges (the look of
style.vox_mixed_media_key), and the same paper with a faint graph grid for charts. Free, local, deterministic.
  python3 assets/edits/vox_plates.py      -> assets/references/vox/plate_paper.jpg, plate_chart.jpg (+ preview.jpg)"""
import os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "assets", "references", "vox")
W, H = 1200, 2100                       # a little over 9:16 at 1080x1920; plate() crops and boils inside it
KRAFT = (228, 205, 158)                 # the key's background
SCRAPS = [(40, 66, 120), (196, 82, 58), (92, 128, 104), (150, 110, 70), (232, 196, 92)]


def paper(seed):
    rng = np.random.default_rng(seed)
    base = np.ones((H, W, 3), np.float32) * np.array(KRAFT, np.float32)
    for cell, amp in ((300, 0.035), (90, 0.02), (24, 0.015)):                  # soft unevenness at three scales
        n = Image.fromarray((rng.random((H // cell + 2, W // cell + 2)) * 255).astype(np.uint8))
        n = n.resize((W + 2 * cell, H + 2 * cell), Image.BICUBIC).crop((cell, cell, W + cell, H + cell))
        base += (np.asarray(n, np.float32)[..., None] - 128) * amp
    base += rng.normal(0, 4.0, (H, W, 1))                                     # fine grain
    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im, "RGBA"); r = random.Random(seed)
    for _ in range(2600):                                                     # fibres
        x, y = r.uniform(0, W), r.uniform(0, H); a = r.uniform(0, 6.283); n = r.uniform(6, 26)
        dx, dy = n * np.cos(a), n * np.sin(a); c = r.choice([(120, 92, 52, 34), (255, 245, 220, 40)])
        d.line([(x, y), (x + dx, y + dy)], fill=c, width=1)
    yy, xx = np.mgrid[0:H, 0:W]
    v = ((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2
    shade = 1 - 0.10 * np.clip(v, 0, 1.6)                                     # soft vignette
    return Image.fromarray(np.clip(np.asarray(im, np.float32) * shade[..., None], 0, 255).astype(np.uint8))


def torn(w, h, seed):
    """An irregular torn shape: a wobbly outline (slow drift plus fine teeth) inside a w x h box."""
    r = random.Random(seed); m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m)
    def edge(n, depth):
        drift, out = 0.0, []
        for _ in range(n):
            drift = max(0.0, min(depth, drift + r.uniform(-4, 4)))
            out.append(drift + r.uniform(0, 6))
        return out
    top, right, bottom, left = (edge(w // 8 + 2, 40), edge(h // 8 + 2, 40), edge(w // 8 + 2, 40), edge(h // 8 + 2, 40))
    pts = [(i * 8, top[i]) for i in range(len(top)) if i * 8 <= w] + \
          [(w - right[i], i * 8) for i in range(len(right)) if i * 8 <= h] + \
          [(w - i * 8, h - bottom[i]) for i in range(len(bottom)) if i * 8 <= w] + \
          [(left[i], h - i * 8) for i in range(len(left)) if i * 8 <= h]
    d.polygon(pts, fill=255)
    return m


def scraps(im, seed):
    r = random.Random(seed)
    spots = [(-190, -150, 560, 330, -14), (W - 360, -170, 580, 340, 17), (-230, H - 250, 640, 380, 11),
             (W - 400, H - 230, 660, 360, -13), (-280, H * 0.45, 380, 280, 21)]
    for i, (x, y, w, h, ang) in enumerate(spots):
        col = SCRAPS[(i + seed) % len(SCRAPS)]
        layer = Image.new("RGBA", (w, h), col + (255,))
        rim = Image.new("RGBA", (w, h), (246, 240, 226, 255))                 # the torn white core shows at the edge
        mask, inner = torn(w, h, seed + i), torn(w - 16, h - 16, seed + 50 + i)
        rim.putalpha(mask)
        inner_full = Image.new("L", (w, h), 0); inner_full.paste(inner, (8, 8)); layer.putalpha(inner_full)
        piece = Image.alpha_composite(rim, layer).rotate(ang + r.uniform(-2, 2), expand=True, resample=Image.BICUBIC)
        shadow = Image.new("RGBA", piece.size, (60, 40, 20, 0)); shadow.putalpha(piece.getchannel("A").point(lambda a: a * 0.35))
        shadow = shadow.filter(ImageFilter.GaussianBlur(6))
        im.alpha_composite(shadow, (int(x) + 6, int(y) + 8)); im.alpha_composite(piece, (int(x), int(y)))
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    p = scraps(paper(7).convert("RGBA"), 3).convert("RGB")
    p.save(os.path.join(OUT, "plate_paper.jpg"), quality=90)
    c = paper(11).convert("RGBA"); d = ImageDraw.Draw(c, "RGBA")
    for x in range(0, W, 40):
        d.line([(x, 0), (x, H)], fill=(70, 96, 140, 70 if x % 200 == 0 else 32), width=2 if x % 200 == 0 else 1)
    for y in range(0, H, 40):
        d.line([(0, y), (W, y)], fill=(70, 96, 140, 70 if y % 200 == 0 else 32), width=2 if y % 200 == 0 else 1)
    c = scraps(c, 5).convert("RGB")
    c.save(os.path.join(OUT, "plate_chart.jpg"), quality=90)
    prev = Image.new("RGB", (540 * 2 + 30, 960), (255, 255, 255))
    prev.paste(p.resize((540, 945)), (0, 0)); prev.paste(c.resize((540, 945)), (570, 0))
    prev.save(os.path.join(OUT, "preview.jpg"), quality=80)
    print("wrote", OUT, "plate_paper.jpg plate_chart.jpg preview.jpg")


if __name__ == "__main__":
    main()
