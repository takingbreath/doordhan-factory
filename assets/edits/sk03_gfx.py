#!/usr/bin/env python3
"""TEMPLATE graphics for a Sahayata Kendra edit, from SK03 (E7): a checklist board (title, numbered items with ticks,
a red COMMENT plate), a chain diagram of boxes and arrows, and their blurred-set background. Built locally, no credits.
Copy to work/<slug>/gfx.py next to build.py and change ITEMS, the titles and the diagram boxes for the episode.
Roman Hinglish only (format section 1). Text is big on purpose: the kendra look softens to ~400 px across.
  python3 work/<slug>/gfx.py   ->  work/<slug>/gfx/checklist_preview.png, diagram_preview.png (look before animating)
build.py imports ITEMS, draw_checklist() and draw_diagram() and animates them frame by frame."""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SK = os.environ.get("EPISODE_DIR") or os.path.dirname(os.path.abspath(__file__))
ROOT = SK
while ROOT != os.path.dirname(ROOT) and not os.path.exists(os.path.join(ROOT, "CLAUDE.md")):
    ROOT = os.path.dirname(ROOT)
FONTS = f"{ROOT}/assets/fonts"
W, H = 720, 1280
YEL, WHT, RED, GRN, INK = (255, 214, 0), (255, 255, 255), (235, 40, 40), (60, 220, 90), (15, 15, 25)
NAVY = (14, 28, 74)

# (label, detail): the eight checks, in the order Pandey says them (item 8 is his last line before the payoff)
ITEMS = [
    ("OCCUPANCY", "society full hone pe?"),
    ("LIFT", "ek lift, kitne flat?"),
    ("BIJLI", "power cut mein lift?"),
    ("PAANI", "borewell sookha toh?"),
    ("MAINTENANCE", "kya included? likhwa lo"),
    ("DUES", "noidaauthorityonline.in"),
    ("OC + RERA", "up-rera.in"),
    ("15 SAAL PURANI", "society ghoom aao"),
]


def font(name, size):
    return ImageFont.truetype(f"{FONTS}/{name}", size, layout_engine=ImageFont.Layout.RAQM)


def text(d, xy, s, f, fill, stroke=4, sfill=INK, anchor="ls", shadow=4):
    x, y = xy
    if shadow:
        d.text((x + shadow, y + shadow), s, font=f, fill=(0, 0, 0, 160), anchor=anchor, stroke_width=stroke,
               stroke_fill=(0, 0, 0, 160))
    d.text((x, y), s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sfill)


def tick(d, x, y, s=40):
    pts = [(x, y + s * 0.55), (x + s * 0.38, y + s * 0.92), (x + s, y + s * 0.08)]
    d.line(pts, fill=INK, width=15, joint="curve"); d.line(pts, fill=GRN, width=8, joint="curve")


def cross(d, x, y, s=40):
    for a, b in (((x, y), (x + s, y + s)), ((x + s, y), (x, y + s))):
        d.line([a, b], fill=INK, width=15); d.line([a, b], fill=RED, width=8)


def background(kf=f"{SK}/kf/front_clean.png", darken=0.5):
    im = Image.open(kf).convert("RGB").resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(14))
    return Image.blend(im, Image.new("RGB", (W, H), (8, 10, 20)), darken).convert("RGBA")


def board(fr, y0=130, y1=1110, slide=1.0):
    d = ImageDraw.Draw(fr)
    yy = int(y0 + (1 - slide) * 60)
    d.rounded_rectangle([28, yy, W - 28, y1], 22, fill=NAVY + (242,), outline=(235, 235, 235, 255), width=8)
    d.rounded_rectangle([44, yy + 16, W - 44, y1 - 16], 14, outline=YEL + (255,), width=3)
    return yy


def draw_checklist(fr, shown, ticked, pop=None, footer=1.0):
    """the full board: the first `shown` items listed, the first `ticked` of them ticked; pop maps an item index to
    a 0..1 pop-in amount; footer 0..1 shows the COMMENT 'FULL LIST' plate"""
    yy = board(fr, 96, 1066)
    d = ImageDraw.Draw(fr)
    text(d, (W / 2, yy + 66), "FLAT LENE SE PEHLE", font("Bungee.ttf", 40), WHT, anchor="ms")
    text(d, (W / 2, yy + 158), "CHECKLIST", font("TitanOne.ttf", 92), YEL, stroke=7, anchor="ms")
    lab_f, det_f = font("Bungee.ttf", 32), font("Baloo2-Latin-ExtraBold.ttf", 38)
    row0, rh = yy + 214, 92
    for i, (lab, det) in enumerate(ITEMS[:shown]):
        k = 1.0 if pop is None else pop.get(i, 1.0)
        if k <= 0:
            continue
        y = row0 + i * rh
        x_off = int((1 - k) * 80)
        layer = Image.new("RGBA", (W, rh), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
        ld.rounded_rectangle([62, 10, 108, 56], 8, outline=WHT + (255,), width=4)
        if i < ticked:
            tick(ld, 65, 8, 44)
        text(ld, (128, 40), lab, lab_f, YEL, stroke=4)
        text(ld, (128, 82), det, det_f, WHT, stroke=4)
        if k < 1:
            a = layer.getchannel("A").point(lambda v: int(v * k)); layer.putalpha(a)
        fr.alpha_composite(layer, (x_off, y))
    if footer > 0:
        plate = Image.new("RGBA", (W - 80, 124), (0, 0, 0, 0)); pd = ImageDraw.Draw(plate)
        pd.rounded_rectangle([0, 0, plate.width - 1, plate.height - 1], 20, fill=RED + (255,), outline=WHT, width=6)
        text(pd, (plate.width / 2, 52), "POORI LIST CHAHIYE?", font("Bungee.ttf", 34), WHT, stroke=3, anchor="ms")
        text(pd, (plate.width / 2, 106), "COMMENT: FULL LIST", font("TitanOne.ttf", 50), YEL, stroke=5, anchor="ms")
        if footer < 1:
            a = plate.getchannel("A").point(lambda v: int(v * footer)); plate.putalpha(a)
        fr.alpha_composite(plate, (40, 1088))


def draw_diagram(fr, step, pops=None):
    """the registry trap as a chain of four boxes: ZAMEEN (Noida Authority) -> BUILDER (lease) -> DUES (not paid)
    -> REGISTRY ATKI. step 0..4 shows that many boxes; pops maps a box index to its 0..1 pop-in (the last box slams)"""
    yy = board(fr, 150, 1150)
    d = ImageDraw.Draw(fr)
    text(d, (W / 2, yy + 92), "NOIDA KA KHEL", font("TitanOne.ttf", 70), YEL, stroke=6, anchor="ms")
    boxes = [("ZAMEEN", "NOIDA AUTHORITY KI", YEL, WHT), ("BUILDER", "SIRF LEASE PE", YEL, WHT),
             ("DUES", "AUTHORITY KO NAHI BHARE", RED, RED), ("REGISTRY", "ATAK GAYI", RED, RED)]
    y = yy + 150
    for i, (a, b, col, edge) in enumerate(boxes[:step]):
        k = 1.0 if pops is None else pops.get(i, 1.0)
        if k <= 0:
            y += 212; continue
        layer = Image.new("RGBA", (W, 210), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
        fill = (120, 10, 10, 200) if i == 3 else (255, 255, 255, 28)
        ld.rounded_rectangle([90, 4, W - 90, 144], 16, fill=fill, outline=edge + (255,), width=6)
        text(ld, (W / 2, 68), a, font("Bungee.ttf", 54), col if i < 3 else WHT, anchor="ms")
        text(ld, (W / 2, 122), b, font("Baloo2-Latin-ExtraBold.ttf", 40), WHT if i < 3 else YEL, anchor="ms")
        if i < step - 1:
            cx = W / 2
            ld.line([(cx, 150), (cx, 188)], fill=YEL, width=10)
            ld.polygon([(cx - 20, 182), (cx + 20, 182), (cx, 206)], fill=YEL)
        if i == 3 and k < 1:      # the last box slams in from big
            sc = 1.5 - 0.5 * k
            layer = layer.resize((int(W * sc), int(210 * sc)), Image.BILINEAR)
            fr.alpha_composite(layer, (int(W / 2 - layer.width / 2), int(y + 74 - 74 * sc)))
        else:
            if k < 1:
                al = layer.getchannel("A").point(lambda v: int(v * k)); layer.putalpha(al)
            fr.alpha_composite(layer, (0, y + int((1 - k) * 30)))
        y += 212


if __name__ == "__main__":
    os.makedirs(f"{SK}/gfx", exist_ok=True)
    fr = background(); draw_checklist(fr, 8, 8); fr.convert("RGB").save(f"{SK}/gfx/checklist_preview.png")
    fr = background(f"{SK}/kf/low.png"); draw_diagram(fr, 4); fr.convert("RGB").save(f"{SK}/gfx/diagram_preview.png")
    print("wrote", f"{SK}/gfx/checklist_preview.png", f"{SK}/gfx/diagram_preview.png")
