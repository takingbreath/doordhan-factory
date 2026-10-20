# Template from jio01 (E11, 2026-10-19): copy to work/<slug>/vox.py (fonts and paper plates come from assets/).
# Local Vox-style collage scenes (paper plate, stickers, marker strokes, stamps, stop-motion at 12 fps);
# scene_* functions are episode-specific examples.
#!/usr/bin/env python3
"""jio01 Vox-style collage graphics, rendered locally (real documents and photos, exact numbers).

Paper plate + stickers (white border, drop shadow), stop-motion at 12 fps with a little boil, marker strokes that draw
themselves, a highlighter, rubber stamps. Each scene renders to gfx/<scene>.mp4 at 30 fps.
  python3 work/jio01/vox.py rhp|chart|hook|all      (PREVIEW=1 writes a few stills instead)
"""
import math, os, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
FPS = 30
G = f"{HERE}/gfx"; R = f"{HERE}/real"
MARKER = f"{ROOT}/assets/fonts/PermanentMarker-Regular.ttf"
BUNGEE = f"{ROOT}/assets/fonts/Bungee.ttf"
BALOO = f"{ROOT}/assets/fonts/Baloo2-Latin-ExtraBold.ttf"
SERIF = f"{ROOT}/assets/fonts/DejaVuSerif-Bold.ttf"
PHONE_SCREEN = (226, 228)         # set from the phone sticker (centre of its screen, in the 640-px-tall sticker)
YEL = (255, 214, 10); RED = (214, 38, 38); INK = (22, 22, 24); CORAL = (232, 85, 62); NAVY = (28, 42, 82)


def F(path, size):
    return ImageFont.truetype(path, size)


# ---------- time helpers (stop-motion: animation steps at 12 fps)
def st(t, fps=12):
    return math.floor(t * fps + 1e-6) / fps


def ease_out(x):
    x = min(1, max(0, x)); return 1 - (1 - x) ** 3


def pop(t, t0, dur=0.25):
    """scale for a pop-in with overshoot; 0 before t0"""
    t = st(t)
    if t < t0:
        return 0.0
    x = (t - t0) / dur
    if x >= 1:
        return 1.0
    return 1.12 * math.sin(x * math.pi / 2) if x < 0.7 else 1.12 - 0.12 * (x - 0.7) / 0.3


def boil(seed, t, amp=1.6, rot=0.45, rate=8):
    r = random.Random(f"{seed}:{math.floor(t * rate)}")
    return r.uniform(-amp, amp), r.uniform(-amp, amp), r.uniform(-rot, rot)


# ---------- plate
_PLATE = {}


def plate_src(name):
    """The episode's own plate (work/<slug>/gfx/<name>) if it has one, else the house plate in assets/references/vox/
    (assets/edits/vox_plates.py makes those)."""
    own = f"{G}/{name}"
    return own if os.path.exists(own) else f"{ROOT}/assets/references/vox/{os.path.splitext(name)[0]}.jpg"


def plate(w, h, t, src=None, key="paper"):
    src = src or plate_src("plate_paper.png")
    k = (key, w, h)
    if k not in _PLATE:
        im = Image.open(src).convert("RGB")
        s = max(w * 1.03 / im.width, h * 1.03 / im.height)
        _PLATE[k] = im.resize((int(im.width * s + 0.5), int(im.height * s + 0.5)), Image.LANCZOS)
    big = _PLATE[k]
    dx, dy, _ = boil(key, t, amp=2.0, rot=0, rate=6)
    x0 = (big.width - w) // 2 + int(dx); y0 = (big.height - h) // 2 + int(dy)
    return big.crop((x0, y0, x0 + w, y0 + h))


# ---------- stickers
def torn_mask(w, h, edges="b", depth=7, seed=1):
    r = random.Random(seed)
    m = Image.new("L", (w, h), 255); d = ImageDraw.Draw(m)
    if "b" in edges:
        pts = [(0, h)] + [(x, h - r.randint(0, depth)) for x in range(0, w + 8, 8)] + [(w, h)]
        d.polygon(pts, fill=0)
    if "t" in edges:
        pts = [(0, 0)] + [(x, r.randint(0, depth)) for x in range(0, w + 8, 8)] + [(w, 0)]
        d.polygon(pts, fill=0)
    return m


def sticker(img, border=9, shadow=0.38, torn=None):
    """RGBA image -> RGBA sticker with a white paper border and a soft drop shadow (padding around it)"""
    img = img.convert("RGBA")
    if torn:
        a = ImageChops.multiply(img.getchannel("A"), torn_mask(img.width, img.height, torn))
        img.putalpha(a)
    pad = border + 22
    W, H = img.width + 2 * pad, img.height + 2 * pad
    a = Image.new("L", (W, H), 0); a.paste(img.getchannel("A"), (pad, pad))
    a = a.point(lambda v: 255 if v > 40 else 0)
    wa = a.filter(ImageFilter.MaxFilter(2 * (border // 2) + 1)) if border else a
    if border > 6:
        wa = wa.filter(ImageFilter.MaxFilter(2 * (border - border // 2) + 1))
    wa = wa.filter(ImageFilter.GaussianBlur(0.8))
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if shadow:
        sh = wa.filter(ImageFilter.GaussianBlur(7)).point(lambda v: int(v * shadow))
        sh_img = Image.new("RGBA", (W, H), (40, 28, 10, 0)); sh_img.putalpha(sh)
        tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0)); tmp.paste(sh_img, (6, 9), sh_img); out = Image.alpha_composite(out, tmp)
    white = Image.new("RGBA", (W, H), (250, 248, 240, 0)); white.putalpha(wa)
    out = Image.alpha_composite(out, white)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); lay.paste(img, (pad, pad), img)
    return Image.alpha_composite(out, lay)


def place(frame, stk, cx, cy, scale=1.0, rot=0.0, alpha=1.0):
    """paste an RGBA sticker centred at (cx, cy) with scale/rotation onto an RGBA frame"""
    if scale <= 0.01 or alpha <= 0:
        return
    s = stk
    if abs(scale - 1) > 1e-3:
        s = s.resize((max(1, int(s.width * scale)), max(1, int(s.height * scale))), Image.BICUBIC)
    if abs(rot) > 1e-3:
        s = s.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1:
        s = s.copy(); s.putalpha(s.getchannel("A").point(lambda v: int(v * alpha)))
    frame.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2))) if (
        cx - s.width / 2 >= 0 and cy - s.height / 2 >= 0 and cx + s.width / 2 <= frame.width and cy + s.height / 2 <= frame.height) else \
        _paste_clip(frame, s, int(cx - s.width / 2), int(cy - s.height / 2))


def _paste_clip(frame, s, x, y):
    tmp = Image.new("RGBA", frame.size, (0, 0, 0, 0)); tmp.paste(s, (x, y), s)
    frame.alpha_composite(tmp)


# ---------- marker and highlighter
def marker_path(draw, pts, frac, color=INK, width=9, seed=0):
    """draw the first frac of a polyline, slightly doubled for a felt-tip look"""
    if frac <= 0 or len(pts) < 2:
        return
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    total = sum(seg); want = total * min(1, frac); acc = 0; out = [pts[0]]
    for i, L in enumerate(seg):
        if acc + L >= want:
            u = (want - acc) / L if L else 0
            out.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * u, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * u)); break
        out.append(pts[i + 1]); acc += L
    draw.line(out, fill=color, width=width, joint="curve")
    for p in (out[0], out[-1]):
        draw.ellipse((p[0] - width / 2, p[1] - width / 2, p[0] + width / 2, p[1] + width / 2), fill=color)
    r = random.Random(seed)
    draw.line([(x + r.uniform(-1.2, 1.2), y + r.uniform(-1.2, 1.2)) for x, y in out], fill=color, width=max(2, width - 3), joint="curve")


def ellipse_pts(cx, cy, rx, ry, start=-100, sweep=400, n=90, wobble=0.04, seed=3):
    r = random.Random(seed); pts = []
    for i in range(n + 1):
        a = math.radians(start + sweep * i / n); k = 1 + wobble * math.sin(i * 0.21) + r.uniform(-0.01, 0.01)
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a) + i * 0.08))
    return pts


def highlight(img_rgba, box, frac, color=(255, 226, 40)):
    """multiply a highlighter band over box (x0, y0, x1, y1) of an RGBA image, revealed left to right"""
    if frac <= 0:
        return img_rgba
    x0, y0, x1, y1 = box; xe = x0 + (x1 - x0) * min(1, frac)
    band = Image.new("RGB", img_rgba.size, (255, 255, 255)); d = ImageDraw.Draw(band)
    d.rounded_rectangle((x0, y0, xe, y1), 6, fill=color)
    rgb = ImageChops.multiply(img_rgba.convert("RGB"), band)
    out = rgb.convert("RGBA"); out.putalpha(img_rgba.getchannel("A")); return out


def stamp_img(text, size=64, color=RED, rot=-12, seed=5):
    f = F(BUNGEE, size); d0 = ImageDraw.Draw(Image.new("L", (1, 1)))
    tw = d0.textlength(text, font=f); pad = 18
    im = Image.new("RGBA", (int(tw) + 2 * pad, size + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((3, 3, im.width - 4, im.height - 4), 10, outline=color + (255,), width=6)
    d.text((pad, pad - size * 0.12), text, font=f, fill=color + (255,))
    r = np.random.default_rng(seed); a = np.asarray(im.getchannel("A")).astype(np.float32)
    grit = (r.random(a.shape) > 0.16).astype(np.float32); a = a * grit * 0.92
    im.putalpha(Image.fromarray(a.astype(np.uint8)))
    return im.rotate(rot, resample=Image.BICUBIC, expand=True)


def strip_img(lines, size=40, font=SERIF, fg=INK, bg=(250, 248, 240), pad=(22, 14), width=None):
    f = F(font, size); d0 = ImageDraw.Draw(Image.new("L", (1, 1)))
    tw = max(d0.textlength(l, font=f) for l in lines); lh = int(size * 1.25)
    W = int(width or tw + 2 * pad[0]); H = lh * len(lines) + 2 * pad[1]
    im = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        d.text(((W - d0.textlength(l, font=f)) / 2, pad[1] + i * lh), l, font=f, fill=fg)
    return im


def write_video(frames_fn, n, w, h, out):
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "14", "-preset", "medium",
                            "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i in range(n):
        enc.stdin.write(np.asarray(frames_fn(i / FPS).convert("RGB")).tobytes())
    enc.stdin.close(); enc.wait()
    print(f"  wrote {out} ({n} frames, {n / FPS:.2f} s)")


def camera(frame, t, z0=1.0, z1=1.0, t0=0.0, t1=1.0, cy=0.5):
    """slow push-in on an RGB(A) frame"""
    x = ease_out((t - t0) / max(1e-3, t1 - t0)) if t > t0 else 0; z = z0 + (z1 - z0) * x
    if abs(z - 1) < 1e-3:
        return frame
    w, h = frame.size; cw, ch = w / z, h / z
    x0 = (w - cw) / 2; y0 = (h - ch) * cy
    return frame.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((w, h), Image.BICUBIC)


# =================================================================== scenes
W, H = 720, 1280


def scene_rhp(dur):
    """v 13.00 -> 19.05: the real RHP cover, then risk factor 6 (p. 35) highlighted and stamped RISK; '?' on 'to risk kahan hai?'"""
    cov = Image.open(f"{R}/rhp220-001.png").convert("RGBA")
    s = 220 / 72
    cov = cov.crop((int(18 * s), int(10 * s), int(578 * s), int(178 * s)))       # QR, logo, RED HERRING PROSPECTUS, JIO PLATFORMS LIMITED
    cov = cov.resize((590, int(590 * cov.height / cov.width)), Image.LANCZOS)
    cov_s = sticker(cov, border=8, torn="b")
    pg = Image.open(f"{R}/rhp300-035.png").convert("RGBA"); s3 = 300 / 72
    box = (64, 336, 531, 395)                                                    # risk factor 6 heading, in pt
    crop = pg.crop(tuple(int(v * s3) for v in box)); k = 660 / crop.width
    crop = crop.resize((660, int(crop.height * k)), Image.LANCZOS)
    P = lambda x, y: ((x - box[0]) * s3 * k, (y - box[1]) * s3 * k)
    hl1 = (*P(413.5, 344.5), *P(524.5, 357.6))                                    # "more competitive satellite-"
    hl2 = (*P(88.5, 356.0), *P(201.0, 369.0))                                     # "based broadband services"
    quote = strip_img(["“...more competitive", "satellite-based broadband", "services...”"], size=38, font=SERIF)
    tag = sticker(strip_img(["JIO KI IPO FILING"], size=34, font=BUNGEE, fg=(250, 248, 240), bg=NAVY), border=0, shadow=0.3)
    quote_s = sticker(quote, border=0, shadow=0.3)
    stamp = stamp_img("RISK", size=70, rot=-11)
    src = F(BALOO, 22)
    q = Image.new("RGBA", (W, 40), (0, 0, 0, 0)); ImageDraw.Draw(q).text((24, 6), "Jio Platforms RHP, 14 Oct 2026, page 35", font=src, fill=(40, 30, 10, 230))

    def fr(t):
        f = plate(W, H, t).convert("RGBA")
        bx, by, br = boil("cov", t)
        place(f, cov_s, 360 + bx, 235 + by, pop(t, 0.05), -3 + br)
        place(f, tag, 250 + bx, 110 + by, pop(t, 0.6), -4 + br)
        if t >= 1.55:
            frac1 = (st(t) - 2.0) / 0.5; frac2 = (st(t) - 2.55) / 0.45
            c = highlight(crop, hl1, frac1); c = highlight(c, hl2, frac2)
            ps = sticker(c, border=10, torn="tb")
            y = 720 + 260 * (1 - ease_out((st(t) - 1.55) / 0.3))
            bx, by, br = boil("p35", t)
            place(f, ps, 360 + bx, y + by, 1.0, 1.5 + br)
        if t >= 2.6:
            bx, by, br = boil("q", t)
            place(f, quote_s, 360 + bx, 480 + by, pop(t, 2.6), -2 + br)
        if t >= 3.45:
            sc = max(1.0, 1.6 - 0.6 * (st(t) - 3.45) / 0.17)
            place(f, stamp, 575, 790, sc, 0, alpha=min(1, (st(t) - 3.45) / 0.08 + 0.3))
        if t >= 4.75:
            d = ImageDraw.Draw(f)
            qm = [(92, 850), (117, 830), (147, 833), (160, 857), (147, 885), (124, 903), (120, 925)]
            marker_path(d, qm, (st(t, 24) - 4.75) / 0.35, color=RED, width=11)
            if t >= 5.15:
                d.ellipse((112, 942, 128, 958), fill=RED)
        f = camera(f, t, 1.0, 1.10, 4.5, dur, cy=0.55)
        f.alpha_composite(q, (0, 1190))
        return f
    return fr


def scene_chart(dur):
    """v 21.95 -> 28.62: FY26 customer growth, home broadband +55% vs mobile broadband +5.6% (real, from the prospectus)"""
    BASE = 600; HOME_X = 205; MOB_X = 560; BAR_W = 150; FULL = 360              # +55% -> 360 px; +5.6% -> 37 px
    fy = sticker(strip_img(["FY 2025-26"], size=46, font=BUNGEE), border=0, shadow=0.3)
    lab_h = strip_img(["HOME", "BROADBAND"], size=30, font=BUNGEE, bg=(250, 248, 240))
    lab_m = strip_img(["MOBILE", "BROADBAND"], size=30, font=BUNGEE, bg=(250, 248, 240))
    lab_h, lab_m = sticker(lab_h, border=0, shadow=0.25), sticker(lab_m, border=0, shadow=0.25)
    src = F(BALOO, 22)
    q = Image.new("RGBA", (W, 40), (0, 0, 0, 0)); ImageDraw.Draw(q).text((24, 6), "Customer growth, FY26. Source: Jio Platforms IPO prospectus", font=src, fill=(40, 30, 10, 230))
    rng = np.random.default_rng(7)

    def bar(hpx, color, seed):
        hpx = max(4, int(hpx)); im = Image.new("RGBA", (BAR_W, hpx), color + (255,))
        a = np.asarray(im).copy(); yy, xx = np.mgrid[0:hpx, 0:BAR_W]
        dots = ((xx % 9 - 4) ** 2 + (yy % 9 - 4) ** 2) < 5
        a[dots, :3] = (a[dots, :3] * 0.86).astype(np.uint8)
        im = Image.fromarray(a); return sticker(im, border=6, shadow=0.3, torn="t")

    def fr(t):
        f = plate(W, H, t, src=plate_src("plate_chart.png"), key="chart").convert("RGBA")
        bx, by, br = boil("fy", t)
        place(f, fy, 360 + bx, 80 + by, pop(t, 0.15), -2 + br)
        hh = FULL * ease_out((st(t) - 1.45) / 0.75) if t >= 1.45 else 0
        if hh > 2:
            b = bar(hh, CORAL, 1); bx, by, br = boil("hb", t, rot=0.25)
            place(f, b, HOME_X + bx, BASE - b.height / 2 + 31 + by, 1.0, br)
        mh = FULL * 5.6 / 55 * ease_out((st(t) - 4.0) / 0.5) if t >= 4.0 else 0
        if mh > 2:
            b = bar(mh, NAVY, 2); bx, by, br = boil("mb", t, rot=0.25)
            place(f, b, MOB_X + bx, BASE - b.height / 2 + 31 + by, 1.0, br)
        bx, by, br = boil("lh", t)
        place(f, lab_h, HOME_X + bx, BASE + 50 + by, pop(t, 1.3), -3 + br)
        place(f, lab_m, MOB_X + bx, BASE + 50 + by, pop(t, 3.5), 2 + br)
        if t >= 2.11:
            sl = slam("+55%"); place(f, sl, HOME_X, BASE - FULL - 50, pop(t, 2.11, 0.17), -4)
        if t >= 5.25:
            sl = slam("+5.6%"); place(f, sl, MOB_X, BASE - 37 - 75, pop(t, 5.25, 0.17), 3)
        f.alpha_composite(q, (0, 1190))
        return f
    return fr


def slam(text, size=78):
    f = F(BALOO, size); d0 = ImageDraw.Draw(Image.new("L", (1, 1))); tw = d0.textlength(text, font=f); pad = 26
    im = Image.new("RGBA", (int(tw) + 2 * pad, size + 34), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 4, im.width - 1, im.height - 4), 18, fill=YEL + (255,))
    d.text((pad, -2), text, font=f, fill=(15, 15, 15, 255))
    return sticker(im, border=0, shadow=0.35)


def wrap(text, f, width):
    d0 = ImageDraw.Draw(Image.new("L", (1, 1))); words = text.split(); lines = [""]
    for w in words:
        cand = (lines[-1] + " " + w).strip()
        if d0.textlength(cand, font=f) <= width:
            lines[-1] = cand
        else:
            lines.append(w)
    return lines


def quote_card():
    """our own card with the verbatim post (not a screenshot): attribution line + quote"""
    hf = F(BALOO, 24); qf = F(SERIF, 27); width = 520
    q = ("“Dear Prime Minister Ambani, Please accept my humble apologies for not realizing that you are "
         "the real boss of India.”")
    lines = wrap(q, qf, width); lh = 36
    im = Image.new("RGBA", (width + 44, 70 + lh * len(lines) + 18), (252, 251, 246, 255)); d = ImageDraw.Draw(im)
    d.text((22, 14), "Elon Musk on X  ·  9 Oct 2026", font=hf, fill=(90, 90, 96))
    d.line((22, 54, im.width - 22, 54), fill=(200, 196, 186), width=2)
    for i, l in enumerate(lines):
        d.text((22, 64 + i * lh), l, font=qf, fill=INK)
    return sticker(im, border=0, shadow=0.4)


def calendar():
    im = Image.new("RGBA", (176, 214), (252, 251, 246, 255)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 176, 50), fill=RED + (255,))
    f1 = F(BUNGEE, 34); d.text(((176 - d.textlength("OCT", font=f1)) / 2, 4), "OCT", font=f1, fill=(255, 255, 255))
    f2 = F(BUNGEE, 96); d.text(((176 - d.textlength("21", font=f2)) / 2, 46), "21", font=f2, fill=INK)
    f3 = F(BALOO, 25); t = "IPO OPENS"; d.text(((176 - d.textlength(t, font=f3)) / 2, 170), t, font=f3, fill=(70, 70, 70))
    for x in range(20, 170, 30):
        d.ellipse((x, -6, x + 12, 6), fill=(0, 0, 0, 0))
    return sticker(im, border=6, shadow=0.35)


def cut_sticker(path, box, height, border=10):
    im = Image.open(path).convert("RGBA")
    x0, y0, x1, y1 = box; im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
    im = im.resize((int(im.width * height / im.height), height), Image.LANCZOS)
    return sticker(im, border=border, shadow=0.4)


def fly(t, t0, t1, a, b):
    """position from a to b between t0 and t1 (stop-motion steps, ease-out)"""
    x = ease_out((st(t) - t0) / max(1e-3, t1 - t0)); return a + (b - a) * x


def scene_hook(dur):
    """the top half of the split (720x640, reel time): Jio IPO in days -> Musk vs Ambani on X -> Starlink vs Jio, hurt?"""
    HH = 640
    jio = sticker(Image.open(f"{R}/jio_logo.png").convert("RGBA").resize((230, 230), Image.LANCZOS), border=8, shadow=0.4)
    jio_s = sticker(Image.open(f"{R}/jio_logo.png").convert("RGBA").resize((200, 200), Image.LANCZOS), border=8, shadow=0.4)
    ipo = stamp_img("IPO", size=62, rot=-12)
    cal = calendar()
    musk = cut_sticker(f"{G}/musk_cut.png", (0.07, 0.0, 1.0, 0.93), 470)
    amb = cut_sticker(f"{G}/ambani_cut.png", (0.0, 0.0, 0.80, 0.86), 470)
    card = quote_card()
    dish = cut_sticker(f"{G}/dish2_cut.png", (0.0, 0.0, 1.0, 1.0), 135, border=8)     # official Starlink photo
    sl = Image.open(f"{R}/starlink_logo_black.png").convert("RGBA"); sl = sl.resize((300, int(300 * sl.height / sl.width)), Image.LANCZOS)
    slw = sticker(Image.alpha_composite(Image.new("RGBA", (sl.width + 28, sl.height + 22), (252, 251, 246, 255)),
                                        Image.new("RGBA", (sl.width + 28, sl.height + 22), (0, 0, 0, 0))), border=0, shadow=0.3)
    tmp = Image.new("RGBA", (sl.width + 28, sl.height + 22), (252, 251, 246, 255)); tmp.alpha_composite(sl, (14, 11))
    slw = sticker(tmp, border=0, shadow=0.3)
    T_OFF, T_MUSK, T_AMB, T_X, T_SL, T_JIO, T_HURT = 2.40, 2.65, 3.33, 3.78, 5.25, 6.36, 7.76
    jio_m = sticker(Image.open(f"{R}/jio_logo.png").convert("RGBA").resize((150, 150), Image.LANCZOS), border=7, shadow=0.4)
    cal_m = cal.resize((int(cal.width * 0.72), int(cal.height * 0.72)), Image.LANCZOS)

    def bump(t, t0):
        """a quick punch on a sticker when its name is said"""
        x = (st(t) - t0) / 0.25
        return 1.0 if x < 0 or x >= 1 else 1.0 + 0.07 * math.sin(math.pi * x)

    def fr(t):
        f = plate(W, HH, t).convert("RGBA")
        act3 = t >= T_SL
        out2 = 0 if t < T_SL else ease_out((st(t) - T_SL) / 0.2)            # act 2 leaves upward
        if out2 < 1:
            # Musk and Ambani are on from the first frame (the visual hook, Akhilesh 2026-10-19)
            bx, by, br = boil("musk", t)
            place(f, musk, 185 + bx, 330 - 800 * out2 + by, bump(t, T_MUSK), 2 + br)
            bx, by, br = boil("amb", t)
            place(f, amb, 540 + bx, 330 - 800 * out2 + by, bump(t, T_AMB), -2 + br)
            # act 1 on top of them: the Jio logo, the IPO stamp, the calendar; they leave at T_OFF
            out = 0 if t < T_OFF else ease_out((st(t) - T_OFF) / 0.2)
            if out < 1:
                bx, by, br = boil("jio", t)
                place(f, jio_m, 360 + bx, 445 + 700 * out + by, 1.0, -4 + br)
                if t >= 0.79:
                    sc = max(1.0, 1.6 - 0.6 * (st(t) - 0.79) / 0.17); place(f, ipo, 440, 520 + 700 * out, 0.8 * sc)
                if t >= 1.33:
                    bx, by, br = boil("cal", t)
                    place(f, cal_m, 360 + bx, 125 - 700 * out + by, pop(t, 1.33), 5 + br)
            if t >= T_AMB + 0.3:
                d = ImageDraw.Draw(f)
                bolt = [(372, 60), (340, 130), (385, 140), (345, 225)]
                marker_path(d, [(x, y - 800 * out2) for x, y in bolt], (st(t, 24) - T_AMB - 0.3) / 0.2, color=RED, width=12)
            if t >= T_X:
                bx, by, br = boil("card", t)
                place(f, card, 360 + bx, fly(t, T_X, T_X + 0.2, 900, 445) - 800 * out2 + by, 1.0, -2 + br)
        if act3:
            bx, by, br = boil("dish", t)
            place(f, dish, fly(t, T_SL, T_SL + 0.3, 900, 505) + bx, fly(t, T_SL, T_SL + 0.3, -150, 190) + by, 1.0, -6 + br)
            place(f, slw, fly(t, T_SL + 0.1, T_SL + 0.4, 900, 505) + bx, 320 + by, 1.0, -3 + br)
            if t >= T_JIO:
                bx, by, br = boil("jio2", t)
                place(f, jio_s, 185 + bx, 300 + by, pop(t, T_JIO), 3 + br)
                d = ImageDraw.Draw(f)
                arrow = [(420, 250), (380, 262), (330, 278), (292, 290)]
                marker_path(d, [(x, y) for x, y in arrow], (st(t, 24) - T_JIO - 0.25) / 0.3, color=INK, width=7)
                if st(t, 24) - T_JIO - 0.25 > 0.3:
                    marker_path(d, [(306, 268), (292, 290), (318, 300)], 1.0, color=INK, width=7)
            if t >= T_HURT:
                d = ImageDraw.Draw(f)
                crack = [(150, 205), (178, 250), (160, 285), (200, 322), (182, 360), (214, 398)]
                marker_path(d, crack, (st(t, 24) - T_HURT) / 0.2, color=INK, width=8)
        return f
    return fr


JIO_BLUE = (15, 60, 201)


def labels():
    """stickers laid over the AI collage clips in the edit (build.py LOGOS)"""
    a = strip_img(["JIO AIRFIBER"], size=30, font=BUNGEE, fg=(255, 255, 255), bg=JIO_BLUE, pad=(16, 10))
    sticker(a, border=0, shadow=0.35).rotate(-3, resample=Image.BICUBIC, expand=True).save(f"{G}/lab_airfiber.png")
    sl = Image.open(f"{R}/starlink_logo_black.png").convert("RGBA"); sl = sl.resize((230, int(230 * sl.height / sl.width)), Image.LANCZOS)
    tmp = Image.new("RGBA", (sl.width + 26, sl.height + 22), (252, 251, 246, 255)); tmp.alpha_composite(sl, (13, 11))
    sticker(tmp, border=0, shadow=0.35).rotate(3, resample=Image.BICUBIC, expand=True).save(f"{G}/lab_starlink.png")
    j = Image.open(f"{R}/jio_logo.png").convert("RGBA").resize((112, 112), Image.LANCZOS)
    sticker(j, border=6, shadow=0.35).save(f"{G}/lab_jio.png")
    print("labels written")


def scene_mobile(dur):
    """v 53.20 -> 55.15 over "Jio's existing mobile customers": Jio's phone users; Starlink's arrow at them crossed out"""
    ph = Image.open(f"{G}/phone_cut.png").convert("RGBA")
    ph = ph.resize((int(ph.width * 640 / ph.height), 640), Image.LANCZOS)
    j = Image.open(f"{R}/jio_logo.png").convert("RGBA").resize((150, 150), Image.LANCZOS)
    ph.alpha_composite(j, (PHONE_SCREEN[0] - 75, PHONE_SCREEN[1] - 75))
    phs = sticker(ph, border=0, shadow=0.4)
    lab = sticker(strip_img(["EXISTING", "MOBILE CUSTOMERS"], size=40, font=BUNGEE), border=0, shadow=0.3)
    dish = cut_sticker(f"{G}/dish2_cut.png", (0.0, 0.0, 1.0, 1.0), 110, border=8)

    def fr(t):
        f = plate(W, H, t).convert("RGBA")
        bx, by, br = boil("ph", t)
        place(f, phs, 245 + bx, 650 + by, pop(t, 0.0, 0.2), -3 + br)
        place(f, lab, 360 + bx, 190 + by, pop(t, 0.30), 2 + br)
        place(f, dish, 610 + bx, 400 + by, pop(t, 0.15), -8 + br)
        d = ImageDraw.Draw(f)
        dots = [(560, 480), (520, 520), (480, 560)]
        if t >= 0.35:
            for k in range(int(min(1, (st(t, 24) - 0.35) / 0.3) * 6)):
                x0 = 590 - k * 20; y0 = 455 + k * 20; d.line((x0, y0, x0 - 9, y0 + 9), fill=INK, width=6)
        if t >= 0.8:
            marker_path(d, [(490, 470), (570, 560)], (st(t, 24) - 0.8) / 0.12, color=RED, width=12)
            marker_path(d, [(570, 470), (490, 560)], (st(t, 24) - 0.95) / 0.12, color=RED, width=12)
        return f
    return fr


SCENES = {"rhp": (scene_rhp, 19.05 - 13.00), "chart": (scene_chart, 28.62 - 21.95), "hook": (scene_hook, 9.2), "mobile": (scene_mobile, 2.10)}

if __name__ == "__main__":
    which = sys.argv[1:] or ["rhp", "chart"]
    if which == ["labels"]:
        labels(); sys.exit()
    if which == ["all"]:
        which = list(SCENES)
    for name in which:
        fn, dur = SCENES[name]
        fr = fn(dur); n = int(round(dur * FPS))
        if os.environ.get("PREVIEW"):
            ts = [float(x) for x in os.environ["PREVIEW"].split(",")]
            ims = [fr(t).convert("RGB") for t in ts]; ims = [im.resize((240, int(im.height * 240 / im.width))) for im in ims]
            sheet = Image.new("RGB", (240 * len(ims), ims[0].height)); [sheet.paste(im, (240 * i, 0)) for i, im in enumerate(ims)]
            sheet.save(f"{G}/{name}_preview.jpg"); print("preview", f"{G}/{name}_preview.jpg")
        else:
            write_video(fr, n, W, 640 if name == "hook" else H, f"{G}/{name}.mp4")
