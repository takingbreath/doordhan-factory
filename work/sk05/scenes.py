#!/usr/bin/env python3
"""sk05 (eMudhra) Vox-style collage scenes, built on the jio01 toolkit (vox.py: kraft plate, stickers, marker, highlighter,
stamps, 12 fps stop-motion with boil). Every element keeps moving a little: boil, a slow drift, a slow camera push.
Times inside a scene are local (0 = the scene's first frame); the comments give the voice time (v) of each beat.
  python3 work/sk05/scenes.py hook bars chart ...   |   PREVIEW=0.5,1.5 python3 work/sk05/scenes.py chart
"""
import math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vox as V  # noqa: E402
from vox import (F, st, ease_out, pop, boil, plate, plate_src, sticker, place, marker_path, ellipse_pts, highlight,  # noqa: E402
                 stamp_img, strip_img, write_video, camera, slam, wrap, BUNGEE, BALOO, SERIF, MARKER, YEL, RED, INK, NAVY, CORAL)

R, G = V.R, V.G
W, H = 720, 1280
GREEN = (30, 140, 70)
TITAN = f"{V.ROOT}/assets/fonts/TitanOne.ttf"


# ---------------- helpers
def shot(path, box, width, torn=None, border=10, shadow=0.38):
    im = Image.open(f"{R}/{path}").convert("RGBA").crop(box)
    im = im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)
    return sticker(im, border=border, shadow=shadow, torn=torn)


def shot_raw(path, box, width):
    im = Image.open(f"{R}/{path}").convert("RGBA").crop(box)
    k = width / im.width
    return im.resize((width, int(im.height * k)), Image.LANCZOS), k


def drift(seed, t, ax=6, ay=5, rate=0.18):
    """a slow sway on top of the stop-motion boil, so nothing ever sits dead still"""
    r = random.Random(seed); p1, p2 = r.uniform(0, 6.28), r.uniform(0, 6.28)
    tt = st(t)
    return ax * math.sin(2 * math.pi * rate * tt + p1), ay * math.sin(2 * math.pi * rate * 0.8 * tt + p2)


def put(f, stk, seed, cx, cy, t, t0=0.0, rot=0.0, scale=1.0, dur=0.25, alpha=1.0):
    s = pop(t, t0, dur)
    if s <= 0:
        return
    bx, by, br = boil(seed, t); dx, dy = drift(seed, t)
    place(f, stk, cx + bx + dx, cy + by + dy, s * scale, rot + br, alpha)


def label(text, size=34, fg=(250, 248, 240), bg=NAVY, font=BUNGEE):
    size = int(size * 1.45)
    im = strip_img([text] if isinstance(text, str) else text, size=size, font=font, fg=fg, bg=bg, pad=(18, 10))
    if im.width > 600:                         # never wider than the frame minus the margins
        im = im.resize((600, round(im.height * 600 / im.width)), Image.LANCZOS)
    return sticker(im, border=0, shadow=0.3)


def quote(lines, size=40):
    """a typed verbatim quote, big enough to read on a phone, next to the real screenshot it comes from"""
    return sticker(strip_img(lines, size=size, font=SERIF, bg=(252, 251, 246), pad=(26, 18)), border=0, shadow=0.38)


def source_line(f, text):
    q = Image.new("RGBA", (W, 40), (0, 0, 0, 0))
    ImageDraw.Draw(q).text((24, 6), text, font=F(BALOO, 22), fill=(40, 30, 10, 230)); f.alpha_composite(q, (0, H - 90))


def padlock(size=200, color=(40, 150, 70), cracked=0.0, seed=3):
    """a drawn padlock; cracked 0..1 draws a jagged crack across the body"""
    im = Image.new("RGBA", (size, int(size * 1.2)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    w = size; bw = int(w * 0.16)
    d.arc((w * 0.2, 0, w * 0.8, w * 0.7), 180, 360, fill=(70, 70, 76, 255), width=bw)
    d.line((w * 0.2 + bw / 2, w * 0.35, w * 0.2 + bw / 2, w * 0.55), fill=(70, 70, 76, 255), width=bw)
    d.line((w * 0.8 - bw / 2, w * 0.35, w * 0.8 - bw / 2, w * 0.55), fill=(70, 70, 76, 255), width=bw)
    d.rounded_rectangle((0, w * 0.5, w, w * 1.18), int(w * 0.12), fill=color + (255,))
    d.ellipse((w * 0.43, w * 0.72, w * 0.57, w * 0.86), fill=(20, 20, 20, 255)); d.rectangle((w * 0.475, w * 0.8, w * 0.525, w * 1.0), fill=(20, 20, 20, 255))
    if cracked > 0:
        r = random.Random(seed); pts = [(w * 0.05, w * 0.62)]
        for i in range(1, 9):
            pts.append((w * 0.05 + w * 0.9 * i / 8, w * 0.62 + w * 0.5 * i / 8 + r.uniform(-w * 0.07, w * 0.07)))
        n = max(2, int(len(pts) * min(1, cracked)))
        d.line(pts[:n], fill=(15, 15, 15, 255), width=max(3, int(w * 0.035)))
    return sticker(im, border=8, shadow=0.35)


def envelope(text, w=230):
    h = int(w * 0.62); im = Image.new("RGBA", (w, h), (252, 251, 246, 255)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w - 1, h - 1), outline=(150, 140, 120, 255), width=3)
    d.line((0, 0, w / 2, h * 0.55, w, 0), fill=(150, 140, 120, 255), width=3)
    f = F(BUNGEE, 22); d.text(((w - d.textlength(text, font=f)) / 2, h - 36), text, font=f, fill=INK)
    return sticker(im, border=6, shadow=0.35)


def box_img(text, w=300, h=190, color=(120, 92, 52), open_=0.0):
    im = Image.new("RGBA", (w, h + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((0, 60, w, h + 60), fill=color + (255,)); d.rectangle((0, 60, w, h + 60), outline=(70, 52, 30, 255), width=4)
    lid = int(55 * open_)
    d.polygon([(0, 60), (w, 60), (w - 12, 60 - lid - 8), (12, 60 - lid - 8)], fill=tuple(int(c * 0.85) for c in color) + (255,))
    f = F(BUNGEE, 30); d.text(((w - d.textlength(text, font=f)) / 2, 60 + h / 2 - 18), text, font=f, fill=(250, 245, 230))
    return sticker(im, border=0, shadow=0.35)


def key_img(w=220):
    im = Image.new("RGBA", (w, int(w * 0.45)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); gold = (214, 170, 60, 255)
    d.ellipse((0, 0, w * 0.42, w * 0.42), fill=gold); d.ellipse((w * 0.12, w * 0.12, w * 0.3, w * 0.3), fill=(0, 0, 0, 0))
    d.rectangle((w * 0.38, w * 0.17, w * 0.98, w * 0.26), fill=gold)
    for x in (0.72, 0.84): d.rectangle((w * x, w * 0.26, w * (x + 0.07), w * 0.38), fill=gold)
    return sticker(im, border=6, shadow=0.35)


def tick(d, cx, cy, s, frac, color=GREEN, width=12):
    marker_path(d, [(cx - s, cy), (cx - s * 0.3, cy + s * 0.7), (cx + s, cy - s * 0.8)], frac, color=color, width=width)


def big_number():
    """what a proper P-384 key looks like: a random ~116-digit number (illustrative, seeded)"""
    r = random.Random(384); digits = "".join(str(r.randint(0, 9)) for _ in range(116))
    lines = [digits[i:i + 19] for i in range(0, 116, 19)]
    im = strip_img(lines, size=40, font=SERIF, bg=(250, 248, 240)); return sticker(im, border=0, shadow=0.3)


# ---------------- scenes
def scene_hook(dur):
    """split top 720x640, v 0.00-3.05: the eMudhra logo slaps on, a padlock, then '-36%' stamped on 'kaand' (v 2.04)"""
    HH = 640
    logo = Image.open(f"{R}/emudhra_logo_3x.png").convert("RGBA"); logo = logo.resize((440, int(440 * logo.height / logo.width)), Image.LANCZOS)
    plate_logo = Image.new("RGBA", (logo.width + 40, logo.height + 34), (252, 251, 246, 255)); plate_logo.alpha_composite(logo, (20, 17))
    lg = sticker(plate_logo, border=0, shadow=0.4)
    lock = padlock(150)
    tag = label("SECURITY COMPANY", 30)
    stamp = stamp_img("-36%", size=96, rot=-10)
    T_STAMP = 2.0

    def fr(t):
        f = plate(W, HH, t).convert("RGBA")
        put(f, lg, "lg", 360, 250, t, -1.0, -3)       # on screen from the first frame: the subject, and the loop frame
        put(f, tag, "tag", 330, 110, t, 0.35, -4)
        put(f, lock, "lock", 600, 420, t, 0.7, 8)
        if t >= T_STAMP:
            sc = max(1.0, 1.7 - 0.7 * (st(t) - T_STAMP) / 0.17)
            place(f, stamp, 300, 450, sc, 0, alpha=min(1, (st(t) - T_STAMP) / 0.08 + 0.3))
        return camera(f, t, 1.0, 1.06, 0.0, dur)
    return fr


def scene_bars(dur):
    """the beep, v 3.05-3.90: old TV colour bars with BEEP (the only old-TV moment, as a censor gag)"""
    cols = [(192, 192, 192), (192, 192, 0), (0, 192, 192), (0, 192, 0), (192, 0, 192), (192, 0, 0), (0, 0, 192)]
    base = Image.new("RGB", (W, H)); d = ImageDraw.Draw(base); bw = W / 7
    for i, c in enumerate(cols): d.rectangle((i * bw, 0, (i + 1) * bw, H * 0.72), fill=c)
    for i, c in enumerate([(0, 0, 192), (19, 19, 19), (192, 0, 192), (19, 19, 19), (0, 192, 192), (19, 19, 19), (192, 192, 192)]):
        d.rectangle((i * bw, H * 0.72, (i + 1) * bw, H * 0.8), fill=c)
    d.rectangle((0, H * 0.8, W, H), fill=(16, 16, 16))
    f = F(TITAN, 150); txt = "BEEP"; tw = d.textlength(txt, font=f)
    rng = np.random.default_rng(1)

    def fr(t):
        im = base.copy(); dd = ImageDraw.Draw(im)
        dd.rounded_rectangle((W / 2 - tw / 2 - 30, 470, W / 2 + tw / 2 + 30, 680), 24, fill=(10, 10, 10))
        dd.text((W / 2 - tw / 2, 485), txt, font=f, fill=(255, 255, 255))
        a = np.asarray(im).astype(np.int16); a += rng.integers(-14, 14, a.shape, dtype=np.int16)
        return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    return fr


def scene_chart(dur):
    """v 3.90-7.95: the real TradingView 5-day chart; marker traces the fall; two LOWER CIRCUIT stickers; -36%"""
    head, _ = shot_raw("chart_screenshot_5d.png", (40, 300, 1340, 720), 600)
    chart, k = shot_raw("chart_screenshot_5d.png", (40, 990, 2520, 1700), 680)
    heads = sticker(head, border=8, shadow=0.35)
    lc = label(["LOWER", "CIRCUIT"], 26, bg=RED)
    src = "Chart: TradingView, NSE:EMUDHRA, 5 days to 22 Oct 2026"
    # the fall, in screenshot px (full res): 21 Oct drop at x~1432, 22 Oct at x~1892
    path = [(1432, 1090), (1446, 1290), (1490, 1380), (1890, 1380), (1910, 1490), (1960, 1540), (2100, 1600), (2340, 1612)]
    P = [((x - 40) * k, (y - 990) * k) for x, y in path]
    T_L1, T_L2, T_SL = 0.75, 1.55, 2.45            # 'do lower circuits' v 4.85-5.73; 'chhattis percent' v 6.29

    def fr(t):
        f = plate(W, H, t, src=plate_src("plate_chart.png"), key="chart").convert("RGBA")
        put(f, heads, "head", 340, 230, t, 0.0, -2)
        c = chart.copy(); d = ImageDraw.Draw(c)
        marker_path(d, P, (st(t, 24) - 0.4) / 1.7, color=RED, width=9)
        put(f, sticker(c, border=10, shadow=0.38), "chart", 360, 640, t, 0.05, 1)
        put(f, lc, "lc1", 470, 500, t, T_L1, -8)
        put(f, lc, "lc2", 570, 800, t, T_L2, 6)
        if t >= T_SL:
            put(f, slam("-36% IN 2 DIN", 70), "sl", 360, 900, t, T_SL, -3, dur=0.17)
        source_line(f, src)
        return camera(f, t, 1.0, 1.07, 0.0, dur, cy=0.5)
    return fr


def scene_gst(dur):
    """v 7.95-14.70: GST / INCOME TAX / IMPORT-EXPORT file tabs pop on each word, a DSC token, eMudhra tied to all"""
    tabs = [("GST", 0.05, 200, 250, -5), ("INCOME TAX", 0.85, 440, 390, 4), ("IMPORT-EXPORT", 1.65, 330, 530, -2)]
    tabimgs = {n: label(n, 44, fg=INK, bg=(238, 214, 150)) for n, *_ in tabs}
    logo = Image.open(f"{R}/emudhra_logo_3x.png").convert("RGBA"); logo = logo.resize((300, int(300 * logo.height / logo.width)), Image.LANCZOS)
    pl = Image.new("RGBA", (logo.width + 30, logo.height + 26), (252, 251, 246, 255)); pl.alpha_composite(logo, (15, 13))
    lg = sticker(pl, border=0, shadow=0.4)
    tok = Image.new("RGBA", (260, 90), (0, 0, 0, 0)); d = ImageDraw.Draw(tok)
    d.rounded_rectangle((0, 10, 190, 80), 14, fill=(40, 46, 60, 255)); d.rectangle((190, 26, 250, 64), fill=(170, 170, 176, 255))
    d.text((18, 26), "DSC", font=F(BUNGEE, 32), fill=(250, 214, 10))
    tokens = sticker(tok, border=6, shadow=0.35)
    lab = label(["DIGITAL SIGNATURE", "CERTIFICATE"], 30, bg=NAVY)
    T_LOGO, T_DSC = 3.45, 4.25                      # 'eMudhra' v 11.41; 'digital signature' v 12.21

    def fr(t):
        f = plate(W, H, t).convert("RGBA")
        for n, t0, x, y, r in tabs:
            put(f, tabimgs[n], n, x, y, t, t0, r)
        if t >= T_LOGO:
            d = ImageDraw.Draw(f)
            for i, (n, t0, x, y, r) in enumerate(tabs):
                marker_path(d, [(360, 720), ((x + 360) / 2 + 20, (y + 720) / 2 + 40), (x, y + 30)],
                            (st(t, 24) - T_LOGO - 0.1 * i) / 0.4, color=RED, width=6, seed=i)
            put(f, lg, "lg", 360, 730, t, T_LOGO, 2)
        put(f, tokens, "tok", 590, 830, t, T_DSC, -6)
        put(f, lab, "lab", 300, 910, t, T_DSC + 0.25, 3)
        return camera(f, t, 1.0, 1.08, 0.0, dur)
    return fr


def scene_cert(dur):
    """v 15.75-23.60: a browser bar with a padlock; 'SSL VERIFIED' stamped on 'digital certificate' (~v 18.0);
    a key goes into a box 'SIRF COMPANY KE PAAS' on 'control ... sirf company' (~v 21.3)"""
    bar = Image.new("RGBA", (620, 96), (245, 245, 247, 255)); d = ImageDraw.Draw(bar)
    d.rounded_rectangle((10, 14, 610, 82), 34, fill=(255, 255, 255, 255), outline=(200, 200, 205, 255), width=3)
    d.text((110, 26), "https://website.com", font=F(BALOO, 36), fill=(40, 40, 46))
    bars = sticker(bar, border=0, shadow=0.35)
    lock = padlock(70)
    st_ssl = stamp_img("SSL VERIFIED", size=56, color=GREEN, rot=-9)
    k = key_img(200); bx_closed = box_img("SIRF COMPANY", 340, 200)
    lab = label("KEY = CONTROL", 30, bg=INK)
    T_SSL, T_KEY = 2.25, 5.3

    def fr(t):
        f = plate(W, H, t).convert("RGBA")
        put(f, bars, "bar", 360, 260, t, 0.0, -1)
        put(f, lock, "lk", 105, 262, t, 0.3, 0)
        if t >= T_SSL:
            sc = max(1.0, 1.6 - 0.6 * (st(t) - T_SSL) / 0.17); place(f, st_ssl, 430, 400, sc, 0, alpha=min(1, (st(t) - T_SSL) / 0.08 + 0.3))
        put(f, bx_closed, "box", 360, 790, t, T_KEY - 0.6, 1)
        if t >= T_KEY - 0.3:
            y = 520 + 190 * ease_out((st(t) - T_KEY) / 0.6) if t >= T_KEY else 520
            put(f, k, "key", 360, y, t, T_KEY - 0.3, -20)
        put(f, lab, "lab", 360, 930, t, T_KEY + 0.5, -2)
        return camera(f, t, 1.0, 1.08, 0.0, dur)
    return fr


def scene_pass(dur):
    """v 23.60-30.05: what a key should be (a 116-digit number) vs eMudhra's: 4 (~v 26.3);
    then a password field types 1, 2, 3 on 'ek, do, teen' (v 28.66 / 28.95 / 29.19)"""
    num = big_number()
    lab1 = label("ASLI KEY AISI HONI CHAHIYE", 28, bg=NAVY)
    four = Image.new("RGBA", (300, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(four)
    d.text((70, -30), "4", font=F(TITAN, 300), fill=RED + (255,)); fours = sticker(four, border=10, shadow=0.4)
    lab2 = label("eMUDHRA KI EK KEY", 30, bg=RED)
    field_bg = (255, 255, 255)
    T4, T1, T2, T3 = 2.75, 5.05, 5.35, 5.59

    def field(n):
        im = Image.new("RGBA", (560, 130), field_bg + (255,)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((4, 4, 556, 126), 18, outline=(120, 120, 128, 255), width=4)
        d.text((24, 6), "PASSWORD", font=F(BALOO, 26), fill=(110, 110, 118))
        d.text((24, 36), "  ".join(["1", "2", "3"][:n]), font=F(TITAN, 70), fill=INK)
        return sticker(im, border=0, shadow=0.35)
    fields = [field(i) for i in range(4)]

    def fr(t):
        f = plate(W, H, t).convert("RGBA")
        if t < T1 - 0.4:
            put(f, lab1, "l1", 360, 150, t, 0.1, -2)
            put(f, num, "num", 360, 420, t, 0.25, 1)
            if t >= T4:
                put(f, lab2, "l2", 360, 700, t, T4 - 0.15, 3)
                put(f, fours, "four", 360, 870, t, T4, -5, dur=0.18)
        else:
            n = 0 + (t >= T1) + (t >= T2) + (t >= T3)
            put(f, fields[n], "fld", 360, 560, t, T1 - 0.4, -2)
            if t >= T3 + 0.35:
                put(f, slam("SECURITY?", 70), "sq", 360, 820, t, T3 + 0.35, 4, dur=0.17)
        return camera(f, t, 1.0, 1.06, 0.0, dur)
    return fr


def scene_hack(dur):
    """v 30.05-33.80: a hooded silhouette (no face) stamps 'SSL VERIFIED' on a fake bank login; red FAKE"""
    hood = Image.new("RGBA", (300, 360), (0, 0, 0, 0)); d = ImageDraw.Draw(hood)
    d.ellipse((60, 20, 240, 220), fill=(18, 18, 22, 255)); d.polygon([(10, 360), (60, 160), (240, 160), (290, 360)], fill=(18, 18, 22, 255))
    d.ellipse((105, 85, 195, 190), fill=(4, 4, 6, 255))
    hoods = sticker(hood, border=8, shadow=0.4)
    page = Image.new("RGBA", (520, 560), (250, 250, 252, 255)); d = ImageDraw.Draw(page)
    d.rectangle((0, 0, 520, 80), fill=(20, 60, 140, 255)); d.text((24, 16), "BANK LOGIN", font=F(BUNGEE, 40), fill=(255, 255, 255))
    for i, lbl in enumerate(["Customer ID", "Password"]):
        d.text((40, 120 + i * 140), lbl, font=F(BALOO, 30), fill=(60, 60, 70)); d.rounded_rectangle((40, 165 + i * 140, 480, 225 + i * 140), 10, outline=(150, 150, 160), width=3)
    d.rounded_rectangle((40, 440, 480, 510), 14, fill=(20, 60, 140)); d.text((200, 450), "LOGIN", font=F(BUNGEE, 36), fill=(255, 255, 255))
    pages = sticker(page, border=10, shadow=0.4)
    lock = padlock(80)
    st_ssl = stamp_img("SSL VERIFIED", size=50, color=GREEN, rot=-8); st_fake = stamp_img("FAKE", size=110, rot=12)
    lab = label("NAKLI CERTIFICATE", 30, bg=INK)
    T_SSL, T_FAKE = 1.6, 3.15

    def fr(t):
        f = plate(W, H, t).convert("RGBA")
        put(f, pages, "pg", 400, 640, t, 0.0, 2)
        put(f, lock, "lk", 600, 360, t, 0.6, 6)
        put(f, hoods, "hd", 150, 1010, t, 0.2, -4)
        put(f, lab, "lab", 330, 200, t, 0.5, -3)
        if t >= T_SSL:
            sc = max(1.0, 1.6 - 0.6 * (st(t) - T_SSL) / 0.17); place(f, st_ssl, 420, 560, sc, 0, alpha=min(1, (st(t) - T_SSL) / 0.08 + 0.3))
        if t >= T_FAKE:
            sc = max(1.0, 1.7 - 0.7 * (st(t) - T_FAKE) / 0.17); place(f, st_fake, 400, 760, sc, 0, alpha=min(1, (st(t) - T_FAKE) / 0.08 + 0.3))
        return camera(f, t, 1.0, 1.08, 0.0, dur)
    return fr


def scene_rob(dur):
    """v 35.05-39.35: Rob Stradling's photo pops on his name (v 35.4); the real Mozilla bug page, 'Reporter' highlighted;
    an envelope flies into a QUARANTINE box on 'kab batayi thi' (~v 38.3)"""
    rob = Image.open(f"{R}/rob_1_upscaled_1100.jpg").convert("RGBA").resize((330, 330), Image.LANCZOS)
    rob = rob.resize((380, 380), Image.LANCZOS); robs = sticker(rob, border=12, shadow=0.42)
    name = label(["ROB STRADLING", "Sectigo"], 28, bg=NAVY)
    title, k = shot_raw("bugzilla_1970728.png", (256, 270, 1120, 350), 620)
    com, k2 = shot_raw("bugzilla_1970728.png", (262, 1180, 700, 1262), 380)
    titles = sticker(title, border=8, shadow=0.35)
    env = envelope("WARNING"); qbox = box_img("QUARANTINE", 320, 170, color=(90, 96, 110))
    yr = label("JUNE 2025", 28, bg=RED)
    T_ENV = 3.15

    def fr(t):
        f = plate(W, H, t).convert("RGBA")
        put(f, robs, "rob", 230, 310, t, 0.3, -5)
        put(f, name, "nm", 240, 550, t, 0.55, -3)
        put(f, titles, "tt", 370, 690, t, 0.9, 2)
        c = highlight(com, (80, 6, 380, 44), (st(t) - 1.6) / 0.4)
        put(f, sticker(c, border=8, shadow=0.35), "cm", 470, 830, t, 1.3, -3)
        put(f, yr, "yr", 560, 470, t, 2.2, 6)
        put(f, qbox, "qb", 540, 910, t, T_ENV - 0.5, 2)
        if t >= T_ENV - 0.2:
            x = 150 + 330 * ease_out((st(t) - T_ENV) / 0.5) if t >= T_ENV else 150
            y = 850 + 50 * ease_out((st(t) - T_ENV) / 0.5) if t >= T_ENV else 880
            sc = 1 - 0.5 * ease_out((st(t) - T_ENV) / 0.5) if t >= T_ENV else 1
            put(f, env, "env", x, y, t, T_ENV - 0.2, -10, scale=sc)
        return camera(f, t, 1.0, 1.07, 0.0, dur)
    return fr


def scene_quar(dur):
    """v 42.95-51.80: the bug page's own words, 'quarantined by internal filters and not seen' highlighted;
    a FOLLOW-UP envelope gets a green tick (~v 46.9 'action bhi hua'); the padlock cracks on 'reh gayi' (~v 50.6)"""
    txt, k = shot_raw("bugzilla_1970728_quarantine.png", (270, 1550, 1600, 1608), 660)
    hl = (0, 4, 660, 54)                       # 'the message was quarantined by internal filters and not seen.'
    q = quote(["“...the message was", "quarantined by internal", "filters and not seen.”"], 44)
    tag = label("eMUDHRA KI APNI INCIDENT REPORT", 26, bg=NAVY)
    env = envelope("FOLLOW-UP")
    T_HL, T_TICK, T_CRACK = 0.9, 4.0, 7.5

    def fr(t):
        f = plate(W, H, t).convert("RGBA")
        put(f, tag, "tag", 360, 150, t, 0.0, -2)
        c = highlight(txt, hl, (st(t) - T_HL) / 0.8)
        put(f, sticker(c, border=10, shadow=0.38, torn="tb"), "txt", 360, 290, t, 0.15, 1)
        put(f, q, "q", 360, 470, t, 0.6, -2)
        put(f, env, "env", 190, 760, t, 2.6, -6)
        if t >= T_TICK:
            tick(ImageDraw.Draw(f), 290, 760, 45, (st(t, 24) - T_TICK) / 0.35)
        cr = 0 if t < T_CRACK else min(1, (st(t) - T_CRACK) / 0.4)
        put(f, padlock(220, cracked=cr), "lock", 520, 790, t, 3.6, 4)
        if t >= T_CRACK + 0.3:
            put(f, label("PROBLEM REH GAYI", 30, bg=RED), "rg", 330, 920, t, T_CRACK + 0.3, -3)
        return camera(f, t, 1.0, 1.07, 0.0, dur)
    return fr


def scene_audit(dur):
    """cutaway inside T3, v 52.90-55.55: eMudhra's statement, 'about 18 months, through two independent audit cycles'
    highlighted; two AUDIT PASSED stamps thump down"""
    txt, k = shot_raw("emudhra_statement_18months.png", (510, 555, 1760, 610), 660)
    hl = (0, 4, 660, 50)
    q = quote(["“The issue went undetected", "for about 18 months, through", "two independent audit cycles.”"], 40)
    tag = label("eMUDHRA KA STATEMENT", 28, bg=NAVY)
    sp = stamp_img("AUDIT PASSED", size=64, color=GREEN, rot=-10)

    def fr(t):
        f = plate(W, H, t).convert("RGBA")
        put(f, tag, "tag", 360, 330, t, 0.0, -2)
        c = highlight(txt, hl, (st(t) - 0.35) / 0.7)
        put(f, sticker(c, border=10, shadow=0.38, torn="tb"), "tx", 360, 460, t, 0.05, 1)
        put(f, q, "q", 360, 640, t, 0.3, -2)
        for i, (t0, x, y, r) in enumerate([(1.4, 260, 850, -10), (1.9, 420, 930, 8)]):
            if t >= t0:
                sc = max(1.0, 1.6 - 0.6 * (st(t) - t0) / 0.17); place(f, sp, x, y, sc, r, alpha=min(1, (st(t) - t0) / 0.08 + 0.3))
        return camera(f, t, 1.0, 1.05, 0.0, dur)
    return fr


def scene_unaff(dur):
    """v 58.45-63.60: the statement's own words, 'no data was breached' and 'no impact whatsoever on ... India';
    a slightly crooked UNAFFECTED stamp (~v 61.4)"""
    a, ka = shot_raw("emudhra_statement_nobreach.png", (620, 612, 1710, 668), 640)
    b, kb = shot_raw("emudhra_statement_18months.png", (560, 1712, 1870, 1768), 640)
    hla = (0, 4, 640, 50); hlb = (0, 4, 640, 50)
    qa = quote(["“no data was breached”"], 44); qb = quote(["“no impact whatsoever on our", "digital signature and eSign", "services, in India...”"], 38)
    st_u = stamp_img("UNAFFECTED", size=78, color=GREEN, rot=-17)
    tag = label("COMPANY KEHTI HAI", 28, bg=NAVY)

    def fr(t):
        f = plate(W, H, t).convert("RGBA")
        put(f, tag, "tag", 360, 200, t, 0.0, -3)
        put(f, sticker(highlight(a, hla, (st(t) - 0.5) / 0.6), border=10, shadow=0.38, torn="tb"), "a", 360, 330, t, 0.1, -1)
        put(f, qa, "qa", 360, 440, t, 0.4, 2)
        put(f, sticker(highlight(b, hlb, (st(t) - 1.6) / 0.6), border=10, shadow=0.38, torn="tb"), "b", 360, 600, t, 1.2, 2)
        put(f, qb, "qb", 360, 760, t, 1.5, -2)
        if t >= 2.95:
            sc = max(1.0, 1.6 - 0.6 * (st(t) - 2.95) / 0.17); place(f, st_u, 380, 910, sc, 0, alpha=min(1, (st(t) - 2.95) / 0.08 + 0.3))
        return camera(f, t, 1.0, 1.06, 0.0, dur)
    return fr


def scene_trust(dur):
    """v 69.00-72.35: 'bharosa uthne ka matlab samjho': a big BHAROSA sticker; the padlock shatters in stop-motion"""
    w = label("BHAROSA", 90, fg=INK, bg=(250, 248, 240), font=TITAN)

    def fr(t):
        f = plate(W, H, t).convert("RGBA")
        put(f, w, "w", 360, 420, t, 0.0, -3)
        cr = min(1, max(0, (st(t) - 0.9) / 0.6))
        if t < 2.2:
            put(f, padlock(260, cracked=cr), "lk", 360, 820, t, 0.15, 3)
        else:                                         # it falls apart: two halves drift and drop
            x = (st(t) - 2.2); lk = padlock(260, cracked=1)
            L = lk.crop((0, 0, lk.width // 2, lk.height)); Rr = lk.crop((lk.width // 2, 0, lk.width, lk.height))
            place(f, L, 360 - 70 - 120 * x, 820 + 260 * x * x, 1, 8 + 30 * x); place(f, Rr, 360 + 70 + 120 * x, 820 + 300 * x * x, 1, -6 - 34 * x)
        return camera(f, t, 1.0, 1.10, 0.0, dur)
    return fr


def scene_digi(dur):
    """v 72.35-84.50: 2011, The Register's headline; NAKLI CERTIFICATES on 'nakli certificates chale' (~v 74.9);
    REJECTED stamps on 'sabne uski mohar reject kar di' (~v 76.4-77.4); public -> 3 hafte -> BANKRUPT (v 78.3-81.7)"""
    reg, k = shot_raw("register_diginotar_2011.png", (60, 290, 2500, 730), 680)
    regs = sticker(reg, border=10, shadow=0.38, torn="b")
    rq = quote(["“DigiNotar goes titsup:", "Disgraced certificate", "firm is sunk”"], 40)
    yr = label(["2011", "NETHERLANDS"], 30, bg=NAVY)
    cert = Image.new("RGBA", (330, 220), (252, 247, 228, 255)); d = ImageDraw.Draw(cert)
    d.rectangle((8, 8, 322, 212), outline=(160, 120, 40), width=5); d.text((40, 30), "DigiNotar", font=F(BUNGEE, 40), fill=INK)
    d.text((40, 90), "CERTIFICATE", font=F(BALOO, 34), fill=(90, 70, 30)); d.ellipse((240, 130, 300, 190), fill=(200, 40, 40))
    certs = sticker(cert, border=6, shadow=0.38)
    nakli = stamp_img("NAKLI", size=60, rot=-12)
    rej = [stamp_img(n, size=46, rot=r) for n, r in [("CHROME: REJECT", -8), ("FIREFOX: REJECT", 6), ("MICROSOFT: REJECT", -4)]]
    steps = [("PUBLIC", 5.95), ("3 HAFTE", 7.3), ("BANKRUPT", 9.3)]
    T_N, T_R = 2.55, [4.05, 4.45, 4.85]

    def fr(t):
        f = plate(W, H, t).convert("RGBA")
        put(f, regs, "reg", 360, 150, t, 0.0, -1)
        put(f, rq, "rq", 360, 330, t, 0.3, -2)
        put(f, yr, "yr", 330, 475, t, 0.8, -4)
        put(f, certs, "ct", 470, 655, t, 1.4, 4)
        if t >= T_N:
            sc = max(1.0, 1.6 - 0.6 * (st(t) - T_N) / 0.17); place(f, nakli, 490, 665, sc, 0, alpha=min(1, (st(t) - T_N) / 0.08 + 0.3))
        for i, t0 in enumerate(T_R):
            if t >= t0:
                sc = max(1.0, 1.5 - 0.5 * (st(t) - t0) / 0.17); place(f, rej[i], 360 + (-120, 110, -40)[i], 782 + i * 64, sc, 0, alpha=min(1, (st(t) - t0) / 0.08 + 0.3))
        d = ImageDraw.Draw(f)
        for i, (s, t0) in enumerate(steps):
            if t >= t0:
                x = 140 + i * 220
                put(f, label(s, 21, bg=(RED if s == "BANKRUPT" else INK)), "s" + s, x, 968, t, t0, (-3, 2, -2)[i], dur=0.2)
                if i:
                    marker_path(d, [(x - 150, 968), (x - 100, 968)], (st(t, 24) - t0 + 0.1) / 0.2, color=INK, width=7)
        return camera(f, t, 1.0, 1.06, 0.0, dur)
    return fr


def scene_rev(dur):
    """v 84.50-87.55: 'sirf ek percent': eMudhra's revenue as one bar, the TLS business a 1% yellow sliver"""
    lab = label("eMUDHRA KA REVENUE", 32, bg=NAVY)
    BW, BH = 520, 150

    def fr(t):
        f = plate(W, H, t, src=plate_src("plate_chart.png"), key="chart").convert("RGBA")
        put(f, lab, "lab", 360, 330, t, 0.0, -2)
        g = ease_out((st(t) - 0.2) / 0.5)
        if g > 0:
            im = Image.new("RGBA", (max(8, int(BW * g)), BH), NAVY + (255,)); d = ImageDraw.Draw(im)
            if g >= 1:
                d.rectangle((BW - 14, 0, BW, BH), fill=YEL + (255,))
            put(f, sticker(im, border=6, shadow=0.3, torn="t"), "bar", 100 + BW * g / 2, 600, t, 0.2, 0)
        if t >= 0.95:
            d = ImageDraw.Draw(f); marker_path(d, ellipse_pts(612, 600, 46, 110), (st(t, 24) - 0.95) / 0.5, color=RED, width=8)
            put(f, slam("SIRF 1%", 70), "sl", 520, 830, t, 1.1, 4, dur=0.17)
        return camera(f, t, 1.0, 1.06, 0.0, dur)
    return fr


def scene_cred(dur):
    """split top 720x640 under T5, v 87.50-91.45: the whole company's value bar drops 36%: CREDIBILITY?"""
    HH = 640
    lab = label("POORI COMPANY KI VALUE", 28, bg=NAVY)

    def fr(t):
        f = plate(W, HH, t, src=plate_src("plate_chart.png"), key="chart2").convert("RGBA")
        put(f, lab, "lab", 360, 90, t, 0.0, -2)
        drop = 0.36 * ease_out((st(t) - 0.5) / 0.6) if t >= 0.5 else 0
        full = 360; h1 = int(full * (1 - drop))
        im = Image.new("RGBA", (220, full), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rectangle((0, full - h1, 220, full), fill=NAVY + (255,))
        if drop > 0:
            d.rectangle((0, 0, 220, full - h1), outline=RED + (255,), width=5)
        put(f, sticker(im, border=0, shadow=0.3), "bar", 220, 360, t, 0.0, 0)
        if t >= 1.1:
            put(f, slam("-36%", 70), "sl", 220, 160, t, 1.1, -4, dur=0.17)
        if t >= 1.5:
            put(f, label(["CREDIBILITY", "?"], 40, bg=RED, font=TITAN), "cr", 520, 360, t, 1.5, 5, dur=0.2)
        return camera(f, t, 1.0, 1.05, 0.0, dur)
    return fr


SCENES = {"hook": (scene_hook, 3.05, 640), "bars": (scene_bars, 0.85, H), "chart": (scene_chart, 4.05, H),
          "gst": (scene_gst, 6.75, H), "cert": (scene_cert, 7.85, H), "pass": (scene_pass, 6.45, H),
          "hack": (scene_hack, 3.75, H), "rob": (scene_rob, 4.30, H), "quar": (scene_quar, 8.85, H),
          "audit": (scene_audit, 2.65, H), "unaff": (scene_unaff, 5.15, H), "trust": (scene_trust, 3.35, H),
          "digi": (scene_digi, 12.15, H), "rev": (scene_rev, 3.05, H), "cred": (scene_cred, 4.20, 640)}

if __name__ == "__main__":
    os.makedirs(G, exist_ok=True)
    which = sys.argv[1:] or list(SCENES)
    for name in which:
        fn, dur, hh = SCENES[name]
        fr = fn(dur)
        if os.environ.get("PREVIEW"):
            ts = [float(x) for x in os.environ["PREVIEW"].split(",")]
            ims = [fr(t).convert("RGB") for t in ts]; ims = [im.resize((240, int(im.height * 240 / im.width))) for im in ims]
            sheet = Image.new("RGB", (240 * len(ims), ims[0].height)); [sheet.paste(im, (240 * i, 0)) for i, im in enumerate(ims)]
            sheet.save(f"{G}/{name}_preview.jpg"); print("preview", f"{G}/{name}_preview.jpg")
        else:
            write_video(fr, int(round((dur + 0.3) * V.FPS)), W, hh, f"{G}/{name}.mp4")
