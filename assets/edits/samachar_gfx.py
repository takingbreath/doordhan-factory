#!/usr/bin/env python3
"""TEMPLATE graphics for a Doordhan Samachar edit (Sarika, Gupta), rebuilt 2026-10-20 from E8 and the DTB3 rules
(the DTB3 helper, work/cd03-hul/gfx.py, was never committed). Built locally, no credits. Copy to work/<slug>/gfx.py.
- top_box(), stock_badge(): the only graphics allowed on Sarika's shots, inside the top-left box beside the DOORDHAN
  bug (x 22-440, y 30-245 at 720x1280). Akhilesh, 2026-10-06: never cover Sarika's neckline. check_sarika_safe()
  raises if anything drawn on a Sarika frame leaves that box.
- data_card(): a full-screen navy card (E8 "SNAPDEAL KE DO BUSINESS"): title, a header row, rows, a source line.
- lower_third(): a kicker tab and a headline strap, for Gupta's shots, photos and footage. Never on Sarika's shots.
Graphics are English, few words (DTB3): "UNILEVER BOUGHT / Minimalist / Rs 3,000 CR", not Hinglish sentences. A share
move is the ticker with a triangle and a falling line ("HUL 27%"). Text is big: the broadcast look softens to ~400 px.
  python3 work/<slug>/gfx.py   ->  work/<slug>/gfx/*_preview.png (look at them before animating)"""
import os
from PIL import Image, ImageDraw, ImageFont

EP = os.environ.get("EPISODE_DIR") or os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.abspath(__file__))       # the repo root: walk up from this file to CLAUDE.md
while ROOT != os.path.dirname(ROOT) and not os.path.exists(os.path.join(ROOT, "CLAUDE.md")):
    ROOT = os.path.dirname(ROOT)
FONTS = f"{ROOT}/assets/fonts"
W, H = 720, 1280
YEL, WHT, RED, GRN, INK = (255, 214, 0), (255, 255, 255), (235, 40, 40), (60, 220, 90), (15, 15, 25)
NAVY, NAVY2 = (14, 28, 74), (22, 40, 104)
SARIKA_BOX = (22, 30, 440, 245)          # x0, y0, x1, y1: everything on a Sarika shot stays inside this


def font(name, size):
    return ImageFont.truetype(f"{FONTS}/{name}", size)


def text(d, xy, s, f, fill, stroke=4, sfill=INK, anchor="ls", shadow=3):
    x, y = xy
    if shadow:
        d.text((x + shadow, y + shadow), s, font=f, fill=(0, 0, 0, 160), anchor=anchor, stroke_width=stroke,
               stroke_fill=(0, 0, 0, 160))
    d.text((x, y), s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sfill)


def fit(s, name, size, max_w, min_size=26):
    """the biggest font size <= size at which s fits max_w"""
    while size > min_size and font(name, size).getlength(s) > max_w:
        size -= 2
    return font(name, size)


def check_sarika_safe(layer):
    """raise if anything opaque on this full-frame RGBA layer sits outside SARIKA_BOX"""
    box = layer.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
    if box is None:
        return
    x0, y0, x1, y1 = SARIKA_BOX
    if box[0] < x0 - 2 or box[1] < y0 - 2 or box[2] > x1 + 2 or box[3] > y1 + 2:
        raise ValueError(f"graphic at {box} leaves Sarika's top-left box {SARIKA_BOX}: never cover her neckline "
                         "(Akhilesh, 2026-10-06). Shorten the text or move it to a full-screen card.")


def top_box(lines, accent=None, k=1.0):
    """the top-left box for a Sarika shot: 1-3 short lines, the first in yellow (or `accent`). k 0..1 = pop-in.
    Returns a full-frame RGBA layer, already checked against her box."""
    x0, y0, x1, y1 = SARIKA_BOX
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    rows = [(fit(s, "Bungee.ttf" if i else "TitanOne.ttf", 52 if i == 0 else 40, x1 - x0 - 44), s)
            for i, s in enumerate(lines[:3])]
    hgt = 30 + sum(f.size + 14 for f, _ in rows)
    hgt = min(hgt, y1 - y0)
    d.rounded_rectangle([x0, y0, x1, y0 + hgt], 18, fill=NAVY + (236,), outline=WHT + (255,), width=5)
    d.rounded_rectangle([x0 + 10, y0 + 10, x1 - 10, y0 + hgt - 10], 12, outline=YEL + (255,), width=2)
    y = y0 + 20
    for i, (f, s) in enumerate(rows):
        y += f.size
        text(d, (x0 + 22, y), s, f, (accent or YEL) if i == 0 else WHT, stroke=3)
        y += 14
    if k < 1:
        layer.putalpha(layer.getchannel("A").point(lambda a: int(a * max(0.0, k))))
    check_sarika_safe(layer)
    return layer


def stock_badge(ticker, pct, up=False, k=1.0):
    """'HUL [down] 27%' with a small line falling (or rising) under it, inside Sarika's top-left box"""
    x0, y0, x1, y1 = SARIKA_BOX
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    col = GRN if up else RED
    d.rounded_rectangle([x0, y0, x1, y0 + 196], 18, fill=NAVY + (236,), outline=WHT + (255,), width=5)
    tf = fit(ticker, "TitanOne.ttf", 64, 190)
    text(d, (x0 + 24, y0 + 82), ticker, tf, WHT, stroke=4)
    tx = x0 + 34 + tf.getlength(ticker)
    tri = [(tx, y0 + 40), (tx + 40, y0 + 40), (tx + 20, y0 + 76)] if not up else \
          [(tx, y0 + 76), (tx + 40, y0 + 76), (tx + 20, y0 + 40)]
    d.polygon(tri, fill=col, outline=INK)
    text(d, (tx + 52, y0 + 82), pct, fit(pct, "Bungee.ttf", 56, x1 - tx - 70), col, stroke=4)
    pts = [(x0 + 26, y0 + 112), (x0 + 110, y0 + 124), (x0 + 170, y0 + 118), (x0 + 250, y0 + 150), (x0 + 330, y0 + 146),
           (x1 - 30, y0 + 176)]
    if up:
        pts = [(x, 2 * (y0 + 144) - y) for x, y in pts]
    d.line(pts, fill=INK, width=12, joint="curve"); d.line(pts, fill=col, width=6, joint="curve")
    if k < 1:
        layer.putalpha(layer.getchannel("A").point(lambda a: int(a * max(0.0, k))))
    check_sarika_safe(layer)
    return layer


def data_card(kicker, title, header, rows, source, highlight=0):
    """the full-screen navy card: kicker (white) over title (yellow), a header row, rows of cells, a source line at
    the foot. header/rows: lists of strings, first column left-aligned; rows[highlight] gets the boxed highlight;
    a cell starting with '-' is drawn red (a loss)."""
    fr = Image.new("RGBA", (W, H), NAVY + (255,)); d = ImageDraw.Draw(fr)
    for y in range(0, H, 4):                                   # faint scanlines, as on E8
        d.line([(0, y), (W, y)], fill=(255, 255, 255, 6))
    text(d, (W / 2, 250), kicker, fit(kicker, "Bungee.ttf", 44, W - 120), WHT, anchor="ms")
    text(d, (W / 2, 330), title, fit(title, "TitanOne.ttf", 76, W - 100), YEL, stroke=6, anchor="ms")
    cols = len(header)
    left, label_w = 52, 250                                    # the first column: labels, left-aligned
    col_w = (W - 40 - (left + label_w)) / max(1, cols - 1)
    cx = [None] + [left + label_w + (i - 0.5) * col_w for i in range(1, cols)]   # value columns: centred

    def cell(x_i, y, s, size, fill, f_name="Bungee.ttf"):
        if x_i == 0:
            text(d, (left, y), s, fit(s, f_name, size, label_w - 12, 18), fill, stroke=2)
        else:
            text(d, (cx[x_i], y), s, fit(s, f_name, size, col_w - 14, 18), fill, stroke=2, anchor="ms")

    for i, h in enumerate(header):
        cell(i, 440, h, 26, YEL)
    d.line([(40, 470), (W - 40, 470)], fill=YEL, width=4)
    y = 540
    for r, row in enumerate(rows):
        if r == highlight:
            d.rectangle([40, y - 56, W - 40, y + 50], fill=NAVY2, outline=(90, 120, 220), width=3)
        for i, c in enumerate(row):
            cell(i, y, c, 34 if i else 30, RED if c.startswith("-") else WHT)
        y += 130
    text(d, (W / 2, H - 70), source, fit(source, "Baloo2-Latin-ExtraBold.ttf", 24, W - 80), (210, 215, 235),
         stroke=0, anchor="ms", shadow=0)
    return fr


def lower_third(kicker, headline, k=1.0):
    """kicker tab + headline strap near the foot (E8's photo opener). For Gupta, photos and footage only."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    y = 1010
    kf = fit(kicker, "Bungee.ttf", 30, 400)
    d.rectangle([20, y - 46, 40 + kf.getlength(kicker) + 24, y], fill=RED)
    text(d, (40, y - 12), kicker, kf, WHT, stroke=0, shadow=0)
    lines = headline.split("\n")[:2]
    hgt = 30 + 66 * len(lines)
    d.rectangle([20, y, W - 20, y + hgt], fill=NAVY + (240,), outline=YEL, width=4)
    for i, s in enumerate(lines):
        text(d, (W / 2, y + 74 + i * 66), s, fit(s, "TitanOne.ttf", 56, W - 80), WHT, stroke=4, anchor="ms")
    if k < 1:
        layer.putalpha(layer.getchannel("A").point(lambda a: int(a * max(0.0, k))))
    return layer


def studio_bg():
    """a stand-in for Sarika's powder-blue set in the previews (the edit draws on the real frames)"""
    bg = Image.new("RGBA", (W, H), (120, 160, 205, 255)); d = ImageDraw.Draw(bg)
    for y in range(0, H, 6):
        d.line([(0, y), (W, y)], fill=(255, 255, 255, int(20 * y / H)))
    d.rectangle([150, 520, 570, H], fill=(70, 60, 90, 255))     # where Sarika sits: nothing may cover it
    return bg


if __name__ == "__main__":
    os.makedirs(f"{EP}/gfx", exist_ok=True)
    fr = studio_bg(); fr.alpha_composite(top_box(["UNILEVER BOUGHT", "Minimalist", "RS 3,000 CR"]))
    fr.convert("RGB").save(f"{EP}/gfx/topbox_preview.png")
    fr = studio_bg(); fr.alpha_composite(stock_badge("HUL", "27%")); fr.convert("RGB").save(f"{EP}/gfx/badge_preview.png")
    data_card("SNAPDEAL KE", "DO BUSINESS", ["FY26", "KAAM", "EBITDA"],
              [["SNAPDEAL", "RS 294 CR", "-RS 50 CR"], ["UNICOMMERCE", "RS 130 CR", "RS 27 CR"]],
              "Source: AceVector RHP, FY26").convert("RGB").save(f"{EP}/gfx/card_preview.png")
    fr = Image.new("RGBA", (W, H), (60, 60, 60, 255)); fr.alpha_composite(lower_third("SNAPDEAL", "SHARK KI COMPANY\nLIST HUI"))
    fr.convert("RGB").save(f"{EP}/gfx/lowerthird_preview.png")
    print("wrote", ", ".join(f"{EP}/gfx/{n}_preview.png" for n in ("topbox", "badge", "card", "lowerthird")))
