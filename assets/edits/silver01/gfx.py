#!/usr/bin/env python3
"""silver01 graphics v3: the chart card on REAL TradingView screens, full width, on a clean white page, no filter, no captions.
Akhilesh, 2026-10-25: "use actual TradingView screens ... animate over the chart"; "make the chart clear, no filter, keep it clean";
"subtitles: mark what is required"; "chart max space"; "zoom in at particular sections temporarily".
Two native TradingView captures of his "Claude" layout (MCX:SILVER1! weekly, INR per kg), each 693 x 854 (the pane, then the time axis):
  WIDE: Aug 2025 to Nov 2026, the complete picture (work/silver01/tv/plate_wide2.png)
  ZOOM: Jul to Nov 2026, TradingView's own zoom on the bottoms, the support and the break (work/silver01/tv/plate_zoom2.png)
Between them the camera zooms (the wide pane is warped to the zoom's coordinates and dissolves into the native zoom).
Our marks sit at TradingView's own coordinates (calibrated on the candle bodies, about 1.5 px) and follow the zoom.
The two lines are Akhilesh's own: falling resistance 301,470 (2 Feb) -> 234,897 (2 Nov); flat support 215,653 from 1 Dec 2025.
Times are Scribe word times on the approved voice cut; reel time = cut time.
  python3 work/silver01/gfx.py [t ...]   ->  work/silver01/gfx/chart_t<time>.png previews
build.py imports chart_frame(t), T, fit, sprite, font, paste, pop."""
import csv, os, sys
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

SK = os.environ.get("EPISODE_DIR") or os.path.dirname(os.path.abspath(__file__))
ROOT = SK
while ROOT != os.path.dirname(ROOT) and not os.path.exists(os.path.join(ROOT, "CLAUDE.md")):
    ROOT = os.path.dirname(ROOT)
FONTS = f"{ROOT}/assets/fonts"
W, H = 720, 1280
YEL, WHT, RED, GRN, INK = (255, 214, 0), (255, 255, 255), (235, 40, 40), (30, 170, 70), (15, 15, 25)
BLU, NAVY = (35, 95, 230), (14, 28, 74)

# ---------------------------------------------------------------- data (bar index 0..62; 62 = the week of 19 Oct)
ROWS = list(csv.DictReader(open(f"{SK}/mcx_silver1_weekly_full.csv")))
OHLC = [(float(r["open"]), float(r["high"]), float(r["low"]), float(r["close"])) for r in ROWS]
N = len(OHLC); LAST = N - 1
IDX = {r["week_start"]: i for i, r in enumerate(ROWS)}
I_FEB, I_DEC = IDX["2026-02-02"], IDX["2025-12-01"]
TOP = 301470.4353992986                      # the falling line's first point (2 Feb): the highest point of the pattern
P_END, I_END = 234896.55250262617, LAST + 2  # its last point (2 Nov)
SUP = 215652.53947780677                     # his flat line
HEIGHT = TOP - SUP                           # 85,818
TARGET = SUP - HEIGHT                        # 129,835
TOUCH_HI = [IDX["2026-03-02"], IDX["2026-05-25"], IDX["2026-08-24"], IDX["2026-09-21"]]
BOTTOMS = [IDX["2026-03-16"], IDX["2026-06-22"], IDX["2026-07-13"], IDX["2026-07-27"], IDX["2026-08-03"]]

# ---------------------------------------------------------------- the two views (plate coordinates, calibrated on the candle bodies)
class View:
    def __init__(self, path, sp, x22, k, pref, yref):
        self.img = np.asarray(Image.open(path).convert("RGB"))
        self.sp, self.x22, self.k = sp, x22, k
        self.A = yref + pref * k                           # y(p) = A - k * p


WIDE = View(f"{SK}/tv/plate_wide2.png", 9.9775, 590.25, 0.0034910629, 301470.4353992986, 159.76992400277038)
ZOOM = View(f"{SK}/tv/plate_zoom2.png", 27.0, 432.75, 0.0108307201, 248800.0, 143.08745644599298)
S = 704 / 693.0                                            # plate -> card
CX0, CY0 = 8, 170                                          # card position of the plate's top-left
PANE_W, PANE_H = 627, 820


def ease(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def prog(t, a, b):
    return ease((t - a) / max(1e-6, b - a))


# ---------------------------------------------------------------- timeline (cut seconds, from the Scribe word times)
T = dict(
    CARD_IN=3.30, REVEAL=1.1,
    DOWN_ARROW=(5.66, 7.0),
    PATTERN=(7.86, 9.70),
    ASC=(9.76, 11.60), OPP=(11.64, 13.62),
    TREND=(13.68, 15.90),
    BOTTOM_RINGS=[16.66, 17.05, 17.95, 18.30, 18.62],      # Mar 16 and Jun 22 in the wide view; Jul 13, Jul 27, Aug 3 in the zoom
    ZOOM_IN=(17.20, 17.85), ZOOM_OUT=(21.45, 22.10),
    SUPPORT=(17.95, 18.80), SUP_TAG=18.30,
    BREAK=20.56,
    QMARK=(22.20, 23.70),
    TOPTAG=25.60,
    HEIGHT=(26.64, 28.30), HEIGHT_TAG=27.56,
    COPY=(29.08, 30.95),
    TARGET=(32.08, 33.30), TARGET_TAG=32.82, EST_TAG=33.4,
    KAMZORI=38.32, PROJECT=(39.42, 41.15),
    CARD_OUT=41.25, CARD2_IN=49.90, CARD2_OUT=53.88,
)
STRIPS = []                                                # no kicker lines, no captions: the marks on the chart say what is needed


def view_e(t):
    """0 = the wide picture, 1 = the zoom on the right end"""
    zi, zo = T["ZOOM_IN"], T["ZOOM_OUT"]
    if t < zi[0] or t >= zo[1]:
        return 0.0
    if t < zi[1]:
        return prog(t, *zi)
    if t < zo[0]:
        return 1.0
    return 1.0 - prog(t, *zo)


def xp(i, e):                                              # plate x of bar i in the view at blend e
    return (1 - e) * (WIDE.x22 - (LAST - i) * WIDE.sp) + e * (ZOOM.x22 - (LAST - i) * ZOOM.sp)


def yp(p, e):                                              # plate y of price p
    return (1 - e) * (WIDE.A - WIDE.k * p) + e * (ZOOM.A - ZOOM.k * p)


class Geo:
    def __init__(self, e):
        self.e = e

    def X(self, i):
        return CX0 + xp(i, self.e) * S

    def Y(self, p):
        return CY0 + yp(p, self.e) * S

    def P(self, wide_xy, zoom_xy):                         # a label position given for each view, in plate coordinates
        e = self.e
        return (CX0 + ((1 - e) * wide_xy[0] + e * zoom_xy[0]) * S, CY0 + ((1 - e) * wide_xy[1] + e * zoom_xy[1]) * S)


# ---------------------------------------------------------------- text
_CM = {}


def _has(fnt, ch):
    from fontTools.ttLib import TTFont
    if fnt.path not in _CM:
        _CM[fnt.path] = TTFont(fnt.path).getBestCmap()
    return ord(ch) in _CM[fnt.path] or ch == " "


def font(name, size):
    return ImageFont.truetype(f"{FONTS}/{name}", size, layout_engine=ImageFont.Layout.RAQM)


def sprite(text, fnt, fill, stroke=5, sfill=INK, shadow=4, pad=10):
    """text with a stroke and a drop shadow; the rupee sign comes from Baloo 2 Devanagari (no other font has it)"""
    fb = ImageFont.truetype(f"{FONTS}/Baloo2-Deva-ExtraBold.ttf", int(fnt.size * 1.08), layout_engine=ImageFont.Layout.RAQM)
    runs = []
    for ch in text:
        f = fnt if _has(fnt, ch) else fb
        if runs and runs[-1][1] is f:
            runs[-1][0] += ch
        else:
            runs.append([ch, f])
    widths = [f.getlength(s) for s, f in runs]
    asc = max(f.getmetrics()[0] for _, f in runs); desc = max(f.getmetrics()[1] for _, f in runs)
    im = Image.new("RGBA", (int(sum(widths) + 2 * pad + 2 * stroke + shadow), asc + desc + 2 * pad + shadow), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for layer in ("shadow", "text"):
        x = pad + stroke
        for (s, f), w in zip(runs, widths):
            if layer == "shadow":
                if shadow:
                    d.text((x + shadow, pad + asc + shadow), s, font=f, anchor="ls", fill=(0, 0, 0, 150),
                           stroke_width=stroke, stroke_fill=(0, 0, 0, 150))
            else:
                d.text((x, pad + asc), s, font=f, anchor="ls", fill=fill, stroke_width=stroke, stroke_fill=sfill)
            x += w
    return im.crop(im.getbbox()) if im.getbbox() else im


def fit(text, name, size, maxw, **kw):
    sp = sprite(text, font(name, size), **kw)
    while sp.width > maxw and size > 20:
        size -= 2
        sp = sprite(text, font(name, size), **kw)
    return sp


_SP = {}


def spr(key, *a, **kw):
    if key not in _SP:
        _SP[key] = fit(*a, **kw)
    return _SP[key]


def paste(fr, sp, cx, cy, scale=1.0, alpha=1.0):
    if scale <= 0 or alpha <= 0:
        return
    im = sp
    if abs(scale - 1) > 0.01:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if alpha < 1:
        a = im.getchannel("A").point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def pop(age, dur=0.18):
    if age < 0:
        return 0.0
    if age >= dur:
        return 1.0
    u = age / dur
    return 0.5 + 0.62 * np.sin(u * np.pi * 0.8) / np.sin(np.pi * 0.8) if u < 0.8 else 1.12 - 0.12 * (u - 0.8) / 0.2


# ---------------------------------------------------------------- the plate at blend e
CARD_W, CARD_H = 704, int(round(854 * S))
_CACHE = {}


def _affine_for(view, e):
    sp_e = (1 - e) * WIDE.sp + e * ZOOM.sp
    x22_e = (1 - e) * WIDE.x22 + e * ZOOM.x22
    k_e = (1 - e) * WIDE.k + e * ZOOM.k
    A_e = (1 - e) * WIDE.A + e * ZOOM.A
    ax = sp_e / view.sp; tx = x22_e - ax * view.x22
    ay = k_e / view.k; ty = A_e - ay * view.A
    return np.float32([[ax, 0, tx], [0, ay, ty]])


def plate_card(e, reveal=1.0):
    """the TradingView picture for this moment, at card size (RGB array)"""
    key = round(e, 3) if 0 < e < 1 else int(e)
    if key not in _CACHE or len(_CACHE) > 40:
        if e <= 0:
            src = WIDE.img
        elif e >= 1:
            src = ZOOM.img
        else:
            w = ease((e - 0.25) / 0.55)
            pane_w = cv2.warpAffine(WIDE.img[:PANE_H], _affine_for(WIDE, e), (693, PANE_H), flags=cv2.INTER_LINEAR, borderValue=(255, 255, 255))
            pane_z = cv2.warpAffine(ZOOM.img[:PANE_H], _affine_for(ZOOM, e), (693, PANE_H), flags=cv2.INTER_LINEAR, borderValue=(255, 255, 255))
            warped = ((1 - w) * pane_w.astype(np.float32) + w * pane_z.astype(np.float32))
            static = ((1 - w) * WIDE.img.astype(np.float32) + w * ZOOM.img.astype(np.float32))
            src = static.copy()
            src[48:PANE_H, :PANE_W] = warped[48:PANE_H, :PANE_W]
            src = src.astype(np.uint8)
        _CACHE[key] = cv2.resize(src, (CARD_W, CARD_H), interpolation=cv2.INTER_CUBIC if e <= 0 or e >= 1 else cv2.INTER_LINEAR)
    img = _CACHE[key]
    if reveal < 1.0:                                       # the real chart wipes in from the left
        img = img.copy(); xr = int(PANE_W * S * reveal)
        img[int(48 * S):int(PANE_H * S), xr:int(PANE_W * S)] = 255
    return img


# ---------------------------------------------------------------- dynamic overlay (2x supersampled, clipped to the pane)
SS = 2


def _line(d, a, b, col, w, dash=None):
    (x0, y0), (x1, y1) = a, b
    L = float(np.hypot(x1 - x0, y1 - y0))
    if L < 1:
        return
    if not dash:
        d.line([(x0 * SS, y0 * SS), (x1 * SS, y1 * SS)], fill=col, width=max(1, int(w * SS))); return
    n = int(L // (dash * 2)) + 1
    for k in range(n):
        s = k * dash * 2 / L; e = min(1.0, (k * dash * 2 + dash) / L)
        if s >= 1:
            break
        d.line([(x0 + (x1 - x0) * s) * SS, (y0 + (y1 - y0) * s) * SS, (x0 + (x1 - x0) * e) * SS, (y0 + (y1 - y0) * e) * SS],
               fill=col, width=max(1, int(w * SS)))


def _outlined(d, a, b, col, w, dash=None, al=255):
    _line(d, a, b, (8, 12, 30, al), w + 4, dash); _line(d, a, b, tuple(col) + (al,), w, dash)


def _arrow_head(d, tip, direction, col, size=14, al=255):
    x, y = tip; dy = 1 if direction == "down" else -1
    pts = [(x - size * 0.8, y - dy * size * 1.2), (x + size * 0.8, y - dy * size * 1.2), (x, y)]
    d.polygon([(px * SS, py * SS) for px, py in pts], fill=(8, 12, 30, al))
    s2 = size * 0.62
    pts = [(x - s2 * 0.8, y - dy * s2 * 1.2 - dy * 1), (x + s2 * 0.8, y - dy * s2 * 1.2 - dy * 1), (x, y - dy * 3)]
    d.polygon([(px * SS, py * SS) for px, py in pts], fill=tuple(col) + (al,))


def _ring(d, cx, cy, r, col, w, u=1.0, al=255):
    if u <= 0 or al <= 0:
        return
    box = [(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS]
    d.arc(box, -90, -90 + 360 * u, fill=(8, 12, 30, al), width=int((w + 3) * SS))
    d.arc(box, -90, -90 + 360 * u, fill=tuple(col) + (al,), width=int(w * SS))


def vis(t, t0, t1=None, fin=0.15, fout=0.45):
    """0..1 visibility of a mark: in from t0, out after t1 (None = stays). Each mark lives only for its own step."""
    a = prog(t, t0, t0 + fin)
    if t1 is not None:
        a *= 1 - prog(t, t1, t1 + fout)
    return a


# how long each mark stays (Akhilesh, 2026-10-25: "too much at one point, keep it simple and readable")
LIFE = dict(touch=(13.68, 16.9), bottoms_until=19.6, suptag=(18.30, 22.2), brk=(20.56, 22.0), top=(25.60, 30.0),
            height_tag=(27.56, 29.9), blue=(26.64, 30.3), copy=(29.08, 34.0), same=(30.75, 32.2))


def overlay(t, g):
    """marks (RGBA, full frame, clipped to the pane) and the labels to paste after: [(sprite, cx, cy, scale, alpha)]"""
    ov = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    sprites = []
    X, Y = g.X, g.Y
    px0, px1 = CX0, CX0 + PANE_W * S
    xr = px1 - 3
    ax = CX0 + 612 * S                                     # the free column right of the last candle (wide view): the measuring arrows
    broke = t >= T["BREAK"]
    yT, yS, yG = Y(TOP), Y(SUP), Y(TARGET)
    ring_r = 8 + 5 * g.e
    A = lambda a: int(255 * max(0.0, min(1.0, a)))

    # downward arrow on "badi girawat"
    if T["DOWN_ARROW"][0] <= t < T["PATTERN"][0] + 0.1:
        a = prog(t, T["DOWN_ARROW"][0], T["DOWN_ARROW"][0] + 0.2) * (1 - prog(t, T["PATTERN"][0] - 0.1, T["PATTERN"][0] + 0.1))
        x = X(LAST) - 28; y0 = Y(OHLC[LAST][2]) + 14; y1 = y0 + 90 * prog(t, T["DOWN_ARROW"][0], T["DOWN_ARROW"][0] + 0.5)
        _outlined(d, (x, y0), (x, y1), RED, 8, al=A(a)); _arrow_head(d, (x, y1 + 14), "down", RED, 20, A(a))

    # the pattern outline (7.86 to 13.68)
    a = prog(t, *T["PATTERN"]) if t < T["TREND"][0] else 1 - prog(t, T["TREND"][0], T["TREND"][0] + 0.4)
    if a > 0:
        x0, x1, y0, y1 = X(I_FEB) - 12, X(LAST) + 14, yT - 16, yS + 40
        for p, q in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
            _outlined(d, p, q, YEL, 3, 11, A(a))

    # the two little triangles (9.76 to 13.68): ascending, then the opposite; no name on screen (viewers name it in comments)
    if T["ASC"][0] <= t < T["TREND"][0] + 0.2:
        al = min(prog(t, T["ASC"][0], T["ASC"][0] + 0.3), 1 - prog(t, T["TREND"][0] - 0.1, T["TREND"][0] + 0.2))
        bx, by, bw, bh = CX0 + 330 * S, CY0 + 600 * S, 236, 126
        d.rounded_rectangle([bx * SS, by * SS, (bx + bw) * SS, (by + bh) * SS], 12 * SS, fill=(8, 12, 30, int(235 * al)),
                            outline=WHT + (int(255 * al),), width=3 * SS)
        flip = prog(t, T["OPP"][0], T["OPP"][0] + 0.45)
        x0, x1 = bx + 26, bx + bw - 26
        asc_top = (by + 30, by + 30); asc_bot = (by + bh - 24, by + 58)
        des_top = (by + 30, by + 72); des_bot = (by + bh - 24, by + bh - 24)
        top_l = asc_top[0] + (des_top[0] - asc_top[0]) * flip; top_r = asc_top[1] + (des_top[1] - asc_top[1]) * flip
        bot_l = asc_bot[0] + (des_bot[0] - asc_bot[0]) * flip; bot_r = asc_bot[1] + (des_bot[1] - asc_bot[1]) * flip
        col = ((60, 220, 90) if flip < 0.5 else RED) + (int(255 * al),)
        d.line([(x0 * SS, top_l * SS), (x1 * SS, top_r * SS)], fill=col, width=7 * SS)
        d.line([(x0 * SS, bot_l * SS), (x1 * SS, bot_r * SS)], fill=col, width=7 * SS)
        d.line([(x1 * SS, top_r * SS), (x1 * SS, bot_r * SS)], fill=col, width=4 * SS)
        lab = "ASCENDING" if flip < 0.5 else "ULTA?"
        sprites.append((spr("tri_" + lab, lab, "Bungee.ttf", 28, 200, fill=(YEL if flip >= 0.5 else NAVY), sfill=INK if flip >= 0.5 else WHT,
                            stroke=3, shadow=2, pad=3), bx + bw / 2, by - 22, 1.0, al))

    # the falling line along the highs: stays. The rings where it meets the highs fade after their moment
    u = prog(t, *T["TREND"])
    if u > 0:
        p0 = (X(I_FEB), Y(TOP)); p1 = (X(I_END), Y(P_END))
        pe = (p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u)
        _outlined(d, p0, pe, YEL, 5)
        ra = vis(t, LIFE["touch"][0], LIFE["touch"][1])
        for k in TOUCH_HI:
            if X(k) <= pe[0] + 1:
                _ring(d, X(k), Y(OHLC[k][1]), ring_r, YEL, 3, 1.0, A(ra))

    # the support line stays (green, red once broken); the rings on the bottoms fade before the break
    ub = prog(t, *T["SUPPORT"])
    if ub > 0:
        xa = max(px0, X(I_DEC)); xb = xa + (xr - xa) * ub
        if broke:
            _outlined(d, (xa, yS), (xr, yS), RED, 5, 12)
        else:
            _outlined(d, (xa, yS), (xb, yS), GRN, 6)
    for k, tr in zip(BOTTOMS, T["BOTTOM_RINGS"]):
        a = vis(t, tr, LIFE["bottoms_until"], 0.25)
        if a > 0:
            _ring(d, X(k), Y(OHLC[k][2]), ring_r, YEL, 3, prog(t, tr, tr + 0.25), A(a))

    # the break: the last two candles circled in red, only for a moment
    ba = vis(t, *LIFE["brk"], fin=0.25, fout=0.4)
    if ba > 0:
        for k in (LAST - 1, LAST):
            c = (Y(OHLC[k][1]) + Y(OHLC[k][2])) / 2
            _ring(d, X(k), c, (ring_r + 8) if k == LAST else ring_r + 3, RED, 3, 1.0, A(ba))

    # the measuring step: the top, a guide and a blue arrow, top to support (26.6 to 30.3, then gone)
    topa = vis(t, *LIFE["top"])
    if topa > 0:
        _ring(d, X(I_FEB), yT, ring_r + 2, BLU, 3, prog(t, T["TOPTAG"], T["TOPTAG"] + 0.25), A(topa))
    uh = prog(t, *T["HEIGHT"]); ha = vis(t, *LIFE["blue"])
    if uh > 0 and ha > 0:
        _outlined(d, (X(I_FEB), yT), (X(I_FEB) + (ax - X(I_FEB)) * min(1, uh * 2.2), yT), BLU, 2, 8, A(ha))
        ya = yT; yb = ya + (yS - ya) * uh
        _outlined(d, (ax, ya), (ax, yb), BLU, 8, None, A(ha))
        d.line([((ax - 15) * SS, ya * SS), ((ax + 15) * SS, ya * SS)], fill=BLU + (A(ha),), width=6 * SS)
        if uh >= 0.98:
            _arrow_head(d, (ax, yS + 2), "down", BLU, 19, A(ha))
    # its copy slides below the support (29.08 to 30.95) and stays until the target is shown
    uc = prog(t, *T["COPY"]); ca = vis(t, *LIFE["copy"])
    if uc > 0 and ca > 0:
        ya = yT + (yS - yT) * uc; yb = ya + (yS - yT)
        _outlined(d, (ax, ya), (ax, yb), YEL, 8, 10 if uc < 1 else None, A(ca))
        d.line([((ax - 15) * SS, ya * SS), ((ax + 15) * SS, ya * SS)], fill=YEL + (A(ca),), width=6 * SS)
        if uc >= 0.98:
            _arrow_head(d, (ax, yb + 2), "down", YEL, 19, A(ca))
    # the target line stays
    ut = prog(t, *T["TARGET"])
    if ut > 0:
        _outlined(d, (px0 + 6, yG), (px0 + 6 + (xr - px0 - 6) * ut, yG), RED, 5, 14)

    # "kamzori": a red arrow from the last candle toward the target, then the dotted projection (35 to 41.25 only)
    lx = X(LAST); ly = Y(OHLC[LAST][2]) + 10
    ux = prog(t, T["KAMZORI"], T["KAMZORI"] + 0.5)
    if ux > 0 and t < T["CARD_OUT"] + 0.2:
        yy = ly + (yG - 12 - ly) * (0.45 * ux if t < T["PROJECT"][0] else 0.45 + 0.55 * prog(t, *T["PROJECT"]))
        _outlined(d, (lx, ly), (lx, yy), RED, 5, 12 if t >= T["PROJECT"][0] else None); _arrow_head(d, (lx, yy + 12), "down", RED, 15)

    big = ov.resize((W, H), Image.LANCZOS)
    mask = Image.new("L", (W, H), 0)                        # marks stay inside the pane
    ImageDraw.Draw(mask).rectangle([int(px0), int(CY0 + 48 * S), int(px1), int(CY0 + PANE_H * S)], fill=255)
    big.putalpha(Image.composite(big.getchannel("A"), Image.new("L", (W, H), 0), mask))

    # labels: only what is required, each for its own step
    sa = vis(t, *LIFE["suptag"])
    if sa > 0:
        x, y = g.P((445, 548), (255, 555))
        sprites.append((spr("suptag_" + ("r" if broke else "g"), "SUPPORT ₹2.16 L", "Bungee.ttf", 26, 260,
                            fill=GRN if not broke else RED, stroke=4, shadow=2, pad=3), x, y, pop(t - T["SUP_TAG"]), sa))
    if ba > 0:
        x, y = g.P((300, 640), (240, 640))
        sprites.append((spr("toot", "TOOT GAYA", "TitanOne.ttf", 52, 300, fill=RED, stroke=6, shadow=3, pad=4), x, y, pop(t - T["BREAK"], 0.22), ba))
    if T["QMARK"][0] <= t < T["QMARK"][1]:
        al = min(1.0, (t - T["QMARK"][0]) / 0.1) * min(1.0, (T["QMARK"][1] - t) / 0.12)
        sc = pop(t - T["QMARK"][0], 0.25) * (1 + 0.04 * np.sin(t * 9))
        x, y = g.P((300, 690), (300, 690))
        sprites.append((spr("q", "?", "TitanOne.ttf", 130, 130, fill=YEL, stroke=8, shadow=4, pad=6), x, y, sc, al))
    tp = vis(t, LIFE["top"][0], LIFE["height_tag"][0])      # the top tag gives way to the height tag
    if tp > 0 and t < T["HEIGHT_TAG"] + 0.4:
        sprites.append((spr("top", "SABSE OONCHA ₹3.01 L", "Bungee.ttf", 30, 330, fill=NAVY, sfill=WHT, stroke=4, shadow=2, pad=3),
                        CX0 + 390 * S, CY0 + 118 * S, pop(t - T["TOPTAG"]), tp * (1 - prog(t, T["HEIGHT_TAG"] - 0.05, T["HEIGHT_TAG"] + 0.3))))
    hg = vis(t, *LIFE["height_tag"])
    if hg > 0:
        sprites.append((spr("height", "HEIGHT ₹86K", "Bungee.ttf", 30, 330, fill=YEL, stroke=4, shadow=2, pad=3),
                        ax - 128, yT - 30, pop(t - T["HEIGHT_TAG"]), hg))
    sm = vis(t, *LIFE["same"])
    if sm > 0:
        sprites.append((spr("same", "SAME HEIGHT", "Bungee.ttf", 28, 280, fill=YEL, stroke=4, shadow=2, pad=3),
                        ax - 128, (yS + yG) / 2, pop(t - LIFE["same"][0]), sm))
    if t >= T["TARGET_TAG"] and (t < T["CARD_OUT"] + 0.1 or T["CARD2_IN"] <= t < T["CARD2_OUT"] + 0.1):
        sprites.append((spr("tgt", "TARGET: ₹1.30 L", "Bungee.ttf", 32, 380, fill=RED, stroke=4, shadow=2, pad=3),
                        px1 - 175, yG - 26, pop(t - T["TARGET_TAG"]), 1.0))
        if t >= T["EST_TAG"] or t >= T["CARD2_IN"]:
            sprites.append((spr("est", "ESTIMATE, NOT ADVICE", "Baloo2-Latin-ExtraBold.ttf", 24, 300, fill=NAVY, sfill=WHT, stroke=3, shadow=0, pad=3),
                            px1 - 150, yG + 20, 1.0, 0.95))
    return big, sprites


def chart_frame(t, with_bg=True):
    """the whole 720x1280 RGBA frame of the chart at reel time t: the real TradingView picture, edge to edge, on white"""
    g = Geo(view_e(t))
    fr = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    reveal = prog(t, T["CARD_IN"], T["CARD_IN"] + T["REVEAL"]) if t < T["CARD2_IN"] else 1.0
    fr.alpha_composite(Image.fromarray(plate_card(g.e, reveal)).convert("RGBA"), (CX0, CY0))
    big, sprites = overlay(t, g)
    fr.alpha_composite(big)
    for sp, cx, cy, sc, al in sprites:
        paste(fr, sp, cx, cy, sc, al)
    return fr


def thumb(w=250, t=51.5):
    fr = chart_frame(t)
    box = fr.crop((CX0, CY0, CX0 + CARD_W, CY0 + CARD_H))
    return box.resize((w, int(box.height * w / box.width)), Image.LANCZOS)


if __name__ == "__main__":
    os.makedirs(f"{SK}/gfx", exist_ok=True)
    for tt in [float(a) for a in (sys.argv[1:] or ["3.8", "6.2", "8.6", "12.4", "15.9", "17.5", "18.9", "20.9", "22.4", "28.6", "31.2", "34.0", "40.0", "51.0"])]:
        chart_frame(tt).convert("RGB").save(f"{SK}/gfx/chart_t{tt:05.1f}.png")
    print("wrote previews in", f"{SK}/gfx")
