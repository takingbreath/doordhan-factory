#!/usr/bin/env python3
"""TEMPLATE (Sahayata Kendra, voice-over variant) from sk04 / E12, approved 2026-10-22: copy into work/<slug>/ as build.py with gfx.py
(assets/edits/sk03_gfx.py), seg/segments.json, seg/V.wav and the pictures in pics/; change the timeline, CARDS, texts and mix.
Original header follows.

sk04 (Sahayata Kendra, voice-over variant): "Salman Khan, maafi maango ya paanch crore do?" Built from the E7 template
(assets/edits/sk03_build.py): frame-composed edit, Pandey on camera for the opening, the first sentence of his answer and the
punchline; the middle of the answer is voice-over on pictures and local graphic cards.
  pipeline/qcpy work/sk04/build.py  ->  work/sk04/edit_raw.mkv + work/sk04/qc_manifest.json
  PLAN_ONLY=1 ... prints the timeline without rendering
Reel time = cut time of work/sk04/voice/sk04_voice_cut.wav (65.16 s), except the hook voice, 0.12 s in. Each talking clip (Wan 2.7,
0.5 s lead in each track) maps clip time c = 0.5 + (reel - segment start)."""
import json, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def _repo_root(start):
    d = start
    while d != os.path.dirname(d):
        if os.path.exists(os.path.join(d, "CLAUDE.md")) and os.path.isdir(os.path.join(d, "pipeline")):
            return d
        d = os.path.dirname(d)
    sys.exit("build.py: run it from a copy inside the doordhan-factory repo (work/<slug>/build.py)")


SK = os.environ.get("EPISODE_DIR") or os.path.dirname(os.path.abspath(__file__))
ROOT = _repo_root(SK)
SLUG = os.path.basename(SK.rstrip("/"))
V, SFX, FONTS = f"{SK}/vid", f"{ROOT}/assets/audio", f"{ROOT}/assets/fonts"
W, H, FPS, SR = 720, 1280, 25, 48000
sys.path.insert(0, f"{ROOT}/pipeline"); sys.path.insert(0, SK)
import sahayata_endcard as EC  # noqa: E402
import voice_room  # noqa: E402
import voice_cut as VC  # noqa: E402  (the draft cut's ring, pick-up click and cradle clack)
import gfx  # noqa: E402  (work/<slug>/gfx.py, from assets/edits/sk03_gfx.py: the checklist board and the diagram)

rng = np.random.default_rng(7)
EDIT_JSON = os.environ.get("EDIT_JSON", f"{SK}/edit.json")
REPAIRS = os.environ.get("QC_REPAIRS", f"{SK}/qc_repairs.json")
REP = json.load(open(REPAIRS)) if os.path.exists(REPAIRS) else {}
CUTWAV = f"{SK}/voice/{SLUG}_voice_cut.wav"      # voice_cut.py writes <name>_voice_cut.wav; name = the slug


def font(name, size):
    return ImageFont.truetype(f"{FONTS}/{name}", size, layout_engine=ImageFont.Layout.RAQM)


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                                capture_output=True, text=True).stdout)



def font(name, size):
    return ImageFont.truetype(f"{FONTS}/{name}", size, layout_engine=ImageFont.Layout.RAQM)


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                                capture_output=True, text=True).stdout)


# ---------------------------------------------------------------- audio timeline (reel seconds = cut seconds)
SEG = json.load(open(f"{SK}/seg/segments.json"))      # P1, A (P2's opening), C (the punchline): cut_start / cut_end
RING, CLICK = 5.40, 6.60                               # work/sk04/voice/cut.json
C1_IN, C1_OUT = 6.93, 17.05                            # the caller (landline chain already on), ends after "kyun?"
Q_OUT0, Q_OUT1 = 16.95, 17.30                          # the question clears before he hangs up
HANGUP1 = 18.31                                        # the cut's cradle clack
P1_AT = 0.12                                           # the hook voice starts 0.12 s into the reel (a lead for the gate)
FIRST = {"P1": P1_AT + 0.14, "A": 19.20, "C": 57.74}   # first word of each talking segment (Scribe on the cut)
P2_LAST = 62.66                                        # "ka" ends
BILLU0 = P2_LAST + 0.30                                # cut about 0.25 s after the last word
CARD = 65.16                                           # the cut's length: Billu's beat runs to here
CARD_LEN = 4.8
TOTAL = CARD + CARD_LEN
LEAD = 0.12                                            # talking shots cut in 0.12 s before the first word
TRACK_LEAD = 0.5                                       # silence before the line in every Wan track
VO0, VO1 = 23.85, 57.60                                # the voice-over stretch of P2 (one wav, seg/V.wav)


def S0(seg):
    return SEG[seg]["cut_start"]


# Talking clips: line id -> (clip, reel time its track's line starts, segment)
TALK = {"P1": ("T1b", P1_AT, "P1"), "P2A": ("T2", S0("A"), "A"), "P2C": ("T3", S0("C"), "C")}
JUDGE_SHIFT = {"P1": -0.10}   # shot_spec.py judge on T1b: ACCEPT_WITH_SHIFT -100 ms (src earlier = lips +100 ms)


def CUT(line):
    if line == "P1":   # the cold open starts the reel
        return 0.0
    return FIRST[TALK[line][2]] - LEAD + REP.get(line, {}).get("cut_in_delay_s", 0.0)


def TK(line, t0):
    clip, r0, _ = TALK[line]
    shift = JUDGE_SHIFT.get(line, 0.0) + REP.get(line, {}).get("src_shift_s", 0.0)
    return f"{V}/{clip}.mp4", TRACK_LEAD + (t0 - r0) + shift


# ---------------------------------------------------------------- text sprites (from sk02_build)
YEL, WHT, RED, GRN, INK = (255, 214, 0), (255, 255, 255), (235, 40, 40), (60, 220, 90), (15, 15, 25)
NAVY = (14, 28, 74)
_CMAPS = {}


def has(fnt, ch):
    from fontTools.ttLib import TTFont
    path = fnt.path
    if path not in _CMAPS:
        _CMAPS[path] = TTFont(path).getBestCmap()
    return ord(ch) in _CMAPS[path] or ch == " "


def runs(text, fnt):
    fb = ImageFont.truetype(f"{FONTS}/Baloo2-Deva-ExtraBold.ttf", int(fnt.size * 1.08), layout_engine=ImageFont.Layout.RAQM)
    out = []
    for ch in text:
        f = fnt if has(fnt, ch) else fb
        if out and out[-1][1] is f:
            out[-1][0] += ch
        else:
            out.append([ch, f])
    return out


def sprite(text, fnt, fill, stroke=6, sfill=INK, shadow=8, pad=24):
    rs = runs(text, fnt)
    widths = [f.getlength(s) for s, f in rs]
    asc = max(f.getmetrics()[0] for _, f in rs); desc = max(f.getmetrics()[1] for _, f in rs)
    im = Image.new("RGBA", (int(sum(widths) + 2 * pad + 2 * stroke + shadow), asc + desc + 2 * pad + shadow),
                   (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for layer in ("shadow", "text"):
        x = pad + stroke
        for (s, f), w in zip(rs, widths):
            if layer == "shadow":
                d.text((x + shadow, pad + asc + shadow), s, font=f, anchor="ls", fill=(0, 0, 0, 170),
                       stroke_width=stroke, stroke_fill=(0, 0, 0, 170))
            else:
                d.text((x, pad + asc), s, font=f, anchor="ls", fill=fill, stroke_width=stroke, stroke_fill=sfill)
            x += w
    return im.crop(im.getbbox()) if im.getbbox() else im


def mark_sprite(kind, size=60):
    im = Image.new("RGBA", (size + 20, size + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    (gfx.tick if kind == "tick" else gfx.cross)(d, 10, 10, size)
    return im


def fit(text, name, size, maxw, **kw):
    while size > 20:
        sp = sprite(text, font(name, size), **kw)
        if sp.width <= maxw:
            return sp
        size -= 4
    return sp


def pop_scale(age, dur=0.16):
    if age < 0:
        return 0
    if age >= dur:
        return 1.0
    u = age / dur
    return 0.55 + 0.57 * np.sin(u * np.pi * 0.75) / np.sin(np.pi * 0.75) if u < 0.75 else 1.12 - 0.12 * (u - 0.75) / 0.25


def paste(frame, sp, cx, cy, scale=1.0, alpha=1.0, angle=0):
    if scale <= 0 or alpha <= 0:
        return
    im = sp
    if angle:
        im = im.rotate(angle, resample=Image.BICUBIC, expand=True)
    if abs(scale - 1) > 0.01:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if alpha < 1:
        a = im.getchannel("A").point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    frame.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


EVENTS = []   # (start, end, drawer(frame, t))


def text_event(t0, t1, text, name="Baloo2-Latin-ExtraBold.ttf", size=64, fill=WHT, cx=W / 2, cy=1010,
               maxw=600, pop=True, fade_out=0.08, angle=0, stroke=6):
    sp = fit(text, name, size, maxw, fill=fill, stroke=stroke)

    def draw(fr, t):
        sc = pop_scale(t - t0) if pop else 1.0
        al = min(1.0, (t1 - t) / fade_out) if t1 - t < fade_out else 1.0
        paste(fr, sp, cx, cy, sc, al, angle)
    EVENTS.append((t0, t1, draw))


def stack(text, name, size, maxw, **kw):
    sp = sprite(text, font(name, size), **kw)
    if sp.width <= maxw:
        return sp
    words = text.split(); best = None
    for k in range(1, len(words)):
        a, b = " ".join(words[:k]), " ".join(words[k:])
        sa, sb = sprite(a, font(name, size), **kw), sprite(b, font(name, size), **kw)
        m = max(sa.width, sb.width)
        if best is None or m < best[0]:
            best = (m, sa, sb)
    _, sa, sb = best
    im = Image.new("RGBA", (max(sa.width, sb.width), sa.height + sb.height - 14), (0, 0, 0, 0))
    im.alpha_composite(sa, ((im.width - sa.width) // 2, 0)); im.alpha_composite(sb, ((im.width - sb.width) // 2, sa.height - 14))
    return im


def caption(t0, t1, text, fill=WHT, cy=1015):
    sp = stack(text, "Baloo2-Latin-ExtraBold.ttf", 66, 610, fill=fill, stroke=6)

    def draw(fr, t):
        al = min(1.0, (t1 - t) / 0.08) if t1 - t < 0.08 else 1.0
        paste(fr, sp, W / 2, cy, pop_scale(t - t0), al)
    EVENTS.append((t0, t1, draw))


def item_card(t0, t1, n, label, detail, tick_at=None, cy=1060):
    """a running checklist card in the lower third: number badge, label, detail, and a tick that pops in"""
    plate = Image.new("RGBA", (650, 190), (0, 0, 0, 0)); d = ImageDraw.Draw(plate)
    d.rounded_rectangle([6, 6, 643, 183], 22, fill=NAVY + (236,), outline=WHT + (255,), width=6)
    d.rounded_rectangle([18, 18, 631, 171], 14, outline=YEL + (255,), width=3)
    d.ellipse([34, 50, 124, 140], fill=YEL + (255,), outline=INK, width=4)
    d.text((79, 112), str(n), font=font("TitanOne.ttf", 64), fill=INK, anchor="ms")
    lab = fit(label, "Bungee.ttf", 50, 400, fill=YEL, stroke=4, shadow=4, pad=6)
    det = fit(detail, "Baloo2-Latin-ExtraBold.ttf", 46, 450, fill=WHT, stroke=4, shadow=4, pad=6)
    plate.alpha_composite(lab, (144, 34)); plate.alpha_composite(det, (144, 98))
    tk = mark_sprite("tick", 70)
    ta = t0 + 0.35 if tick_at is None else tick_at

    def draw(fr, t):
        al = min(1.0, (t1 - t) / 0.08) if t1 - t < 0.08 else 1.0
        x_in = int(80 * (1 - min(1.0, (t - t0) / 0.14)))
        paste(fr, plate, W / 2 + x_in, cy, 1.0, al * min(1.0, (t - t0) / 0.1))
        if t >= ta:
            paste(fr, tk, W / 2 + 280, cy - 70, pop_scale(t - ta, 0.18), al)
    EVENTS.append((t0, t1, draw))


# ---------------------------------------------------------------- shots
class Clip:
    def __init__(self, path, src_in=0.0, speed=1.0):
        self.still = None
        if path.endswith(".png"):
            self.still = np.asarray(Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS)); self.last = self.still
            return
        vf = f"setpts=PTS/{speed},fps={FPS},scale={W}:{H}:flags=lanczos,format=rgb24" if speed != 1 else \
            f"fps={FPS},scale={W}:{H}:flags=lanczos,format=rgb24"
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{max(0, src_in):.3f}", "-i", path, "-vf", vf, "-an",
                                   "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
        self.last = None

    def next(self):
        if self.still is not None:
            return self.still
        b = self.p.stdout.read(W * H * 3)
        if len(b) == W * H * 3:
            self.last = np.frombuffer(b, np.uint8).reshape(H, W, 3)
        return self.last

    def close(self):
        if self.still is None:
            self.p.kill()


def ease(u):
    u = min(1, max(0, u)); return u * u * (3 - 2 * u)


def zoomed(arr, z, cx=W / 2, cy=H / 2):
    if z <= 1.001:
        return Image.fromarray(arr)
    cw, ch = W / z, H / z
    x0 = min(max(0, cx - cw / 2), W - cw); y0 = min(max(0, cy - ch / 2), H - ch)
    return Image.fromarray(arr).resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))


def const(z, c=(W / 2, H / 2)):
    return lambda t: (z, c[0], c[1])


def ramp(t0, t1, z0, z1, c):
    return lambda t: (z0 + (z1 - z0) * ease((t - t0) / max(1e-3, t1 - t0)), c[0], c[1])


def steps(pairs, c, glide=0.0):
    def f(t):
        z = pairs[0][1]
        for i, (tt, zz) in enumerate(pairs):
            if t >= tt:
                prev = pairs[i - 1][1] if i else zz
                z = prev + (zz - prev) * ease((t - tt) / glide) if glide else zz
        return (z, c[0], c[1])
    return f


# face centres (720x1280), measured on each clip with work/sk04/mouthbox.py
FACE = {"T1": (512, 783), "T1b": (495, 764), "T2": (376, 602), "T3": (364, 601), "L1": (361, 610)}
SHOTS = []


def shot(t0, t1, path, src_in, zoom, speed=1.0, line=None):
    SHOTS.append(dict(t0=t0, t1=t1, path=path, src_in=src_in, zoom=zoom, speed=speed, line=line))


def talk(line, t0, t1, zoom):
    path, src = TK(line, t0)
    shot(t0, t1, path, src, zoom, line=line)


R_IN = 4.55                                           # T1's clip is 5 s: 0.5 s lead + 4.5 s of reel
LOOP_AT = 12.60                                       # the listening clip is 6 s: it plays once, then again tighter
OH_IN = HANGUP1 - 0.40                                # the receiver is pressed home 0.4 s into O1 = the clack
P2A_CUT = CUT("P2A")
VO_END = CUT("P2C")                                   # P2's punchline starts here, on camera
BILLU_IN = 62.95                                      # cut 0.25 s after the last word of the punchline

# 1. cold open: the hook to the lens, Billu big at left
talk("P1", 0.0, R_IN, ramp(0.0, R_IN, 1.0, 1.04, FACE["T1b"]))
# 2. the ring: Billu turns his head to the phone, Pandey looks down
shot(R_IN, CLICK, f"{V}/R1.mp4", 0.0, const(1.0), speed=2.066 / (CLICK - R_IN))
# 3. the pick-up: crash in on the listening close-up; the question builds
shot(CLICK, LOOP_AT, f"{V}/L1.mp4", 0.0,
     lambda t: (1.0 + 0.30 * (1 - ease((t - CLICK) / 0.22)) + 0.04 * ease((t - CLICK - 0.3) / 3.0), FACE["L1"][0], 600))
shot(LOOP_AT, OH_IN, f"{V}/L1.mp4", 0.0,
     lambda t: (1.22 + 0.06 * ease((t - LOOP_AT) / 4.0) - 0.10 * ease((t - Q_OUT0) / (Q_OUT1 - Q_OUT0)), FACE["L1"][0], 600))
# 4. overhead: the receiver goes down on the clack
shot(OH_IN, P2A_CUT, f"{V}/O1.mp4", 0.0, const(1.08, (360, 640)))
# 5. A: the first sentence of his answer, three-quarter left
talk("P2A", P2A_CUT, VO0 + 0.05, steps([(0, 1.0), (20.20, 1.10)], FACE["T2"], glide=0.4))
# 6. the voice-over: pictures and cards (built in gfx_cards(), pngs in work/sk04/cards)
CARDS = [  # (start, end, file, zoom0, zoom1)
    (VO0 + 0.05, 27.00, "blackbuck", 1.00, 1.08),
    (27.00, 30.00, "lawrence", 1.00, 1.06),
    (30.00, 33.00, "nokha", 1.00, 1.08),
    (33.00, 35.05, "zero", 1.00, 1.10),
    (35.05, 40.30, "whatsapp", 1.00, 1.07),
    (40.30, 44.70, "sabzi", 1.00, 1.07),
    (44.70, 46.45, "galti", 1.00, 1.08),
    (46.45, 49.10, "mazdoor", 1.00, 1.08),
    (49.10, 50.70, "asli", 1.00, 1.10),
    (50.70, 54.80, "galaxy", 1.00, 1.07),
    (54.80, VO_END, "lakh", 1.00, 1.12),
]
for a, b, nm, z0, z1 in CARDS:
    shot(a, b, f"{SK}/cards/{nm}.png", 0.0, ramp(a, b, z0, z1, (360, 640)))
# 7. C: the punchline, three-quarter right, a slow push
talk("P2C", VO_END, BILLU_IN, ramp(VO_END, BILLU_IN, 1.0, 1.10, FACE["T3"]))
# 8. Billu's button: the note
shot(BILLU_IN, CARD, f"{V}/B1.mp4", 0.0, const(1.0), speed=2.02 / (CARD - BILLU_IN))

WHIPS = [VO0 + 0.05, VO_END]
SHAKES = [(HANGUP1, 0.25, 14), (35.05, 0.25, 8), (50.84, 0.25, 8)]

# ---------------------------------------------------------------- graphics / text
# the hook, on screen from the first frame (no pop: the first frame is the cover). It sits on the wall between the board and his head.
hook1 = fit("SALMAN KHAN:", "TitanOne.ttf", 64, 620, fill=WHT, stroke=7)
hook2 = fit("MAAFI YA \u20b95 CRORE?", "TitanOne.ttf", 84, 640, fill=YEL, stroke=8)
HOOK_Y = 352


def draw_hook(fr, t):
    al = 1.0 if t < RING - 0.1 else max(0.0, (RING + 0.05 - t) / 0.15)
    band = Image.new("RGBA", (W, 176), NAVY + (int(200 * al),))
    d = ImageDraw.Draw(band); d.rectangle([0, 0, W, 6], fill=YEL + (int(255 * al),)); d.rectangle([0, 169, W, 175], fill=YEL + (int(255 * al),))
    fr.alpha_composite(band, (0, HOOK_Y))
    paste(fr, hook1, W / 2, HOOK_Y + 52, 1.0, al); paste(fr, hook2, W / 2, HOOK_Y + 122, 1.0, al)


EVENTS.append((0.0, RING + 0.05, draw_hook))
# the ring (one ring: two bursts, 0.4 s on, 0.2 off, 0.4 on)
for burst in (RING, RING + 0.6):
    for k in range(2):
        a = burst + k * 0.2
        text_event(a, a + 0.18, "TRRRING!", name="Bungee.ttf", size=92, fill=YEL, cx=470 + (k % 2) * 22,
                   cy=880 - k * 12, angle=(-8 if k % 2 else 6), pop=False, fade_out=0.02)
# the question, in English, word by word over the caller (C1 word times from Scribe on the cut)
Q = [(10.66, "SALMAN KHAN:", 68, WHT, 800), (12.04, "APOLOGISE", 96, YEL, 890), (12.94, "OR PAY \u20b95 CRORE?", 76, WHT, 985),
     (14.40, "BUT THE FIGHT IS A DEER.", 56, WHT, 1075), (15.98, "WHY MONEY?", 100, YEL, 1175)]
for tq, txt, sz, col, y in Q:
    sp = fit(txt, "TitanOne.ttf", sz, 500, fill=col, stroke=8)

    def dq(fr, t, sp=sp, t0=tq, y=y):
        al = 1 - ease((t - Q_OUT0) / (Q_OUT1 - Q_OUT0))
        sc = pop_scale(t - t0) * (1 + 0.25 * ease((t - Q_OUT0) / (Q_OUT1 - Q_OUT0)))
        paste(fr, sp, W / 2, y, sc, al)
    EVENTS.append((tq, Q_OUT1, dq))
QDIM0 = 10.50
EVENTS.insert(0, (QDIM0, Q_OUT1, lambda fr, t: fr.alpha_composite(
    Image.new("RGBA", (W, H), (0, 0, 0, int(100 * min(1, (t - QDIM0) / 0.2) *
                                         (1 - ease((t - Q_OUT0) / (Q_OUT1 - Q_OUT0)))))))))

# the voice-over cards: a caption each, on the words (Scribe word times on the cut)
caption(25.54, 27.00, "BISHNOI SAMAAJ MEIN PAVITRA")
caption(31.00, 33.00, "NOKHA DHAM, BIKANER")
# (the typed cards carry their own words; no caption repeats them)
# the punchline: goli vs naam
text_event(58.00, 59.60, "GOLI: \u20b94 LAKH", name="TitanOne.ttf", size=84, fill=WHT, cy=1040, stroke=8, maxw=480)
text_event(60.70, BILLU_IN, "NAAM: \u20b95 CRORE", name="TitanOne.ttf", size=88, fill=YEL, cy=1150, stroke=8, maxw=480)
# the ring on Billu's last beat is not used: the cut has none
# the DOORDHAN bug, top right, until the card
bug = sprite("DOORDHAN", font("Bungee.ttf", 30), (255, 255, 255, 215), stroke=3, shadow=3, pad=6)
EVENTS.append((0, CARD, lambda fr, t: paste(fr, bug, W - 20 - bug.width / 2, 58, 1, 0.85)))


def gfx_cards():
    """the voice-over cards (720x1280 png): real pictures on a blurred copy of themselves, and typographic cards"""
    os.makedirs(f"{SK}/cards", exist_ok=True)
    pics = f"{SK}/pics"

    def base(col=(18, 24, 60)):
        im = Image.new("RGB", (W, H), col); d = ImageDraw.Draw(im)
        for y in range(0, H, 6):
            d.line([(0, y), (W, y)], fill=tuple(max(0, c - 8) for c in col), width=1)
        return im

    def photo_card(src, name, crop=None, rot=-1.5):
        p = Image.open(f"{pics}/{src}").convert("RGB")
        if "nokha" in src:   # paint out the site's text overlay and logo badge (top right, over sky only)
            import cv2
            a = np.asarray(p).copy(); m = np.zeros(a.shape[:2], np.uint8)
            m[60:290, 1280:1900] = 255
            p = Image.fromarray(cv2.inpaint(a, m, 9, cv2.INPAINT_TELEA))
        if crop:
            p = p.crop(crop)
        bg = p.resize((W, H), Image.LANCZOS, box=None).filter(ImageFilter.GaussianBlur(28))
        bg = Image.blend(bg, Image.new("RGB", (W, H), (10, 12, 30)), 0.55)
        w = 640; h = int(p.height * w / p.width)
        if h > 860:
            h = 860; w = int(p.width * h / p.height)
        ph = p.resize((w, h), Image.LANCZOS)
        fr = Image.new("RGB", (w + 28, h + 28), (245, 245, 240)); fr.paste(ph, (14, 14))
        fr = fr.convert("RGBA").rotate(rot, resample=Image.BICUBIC, expand=True)
        bg = bg.convert("RGBA"); bg.alpha_composite(fr, ((W - fr.width) // 2, (H - fr.height) // 2 - 30))
        bg.convert("RGB").save(f"{SK}/cards/{name}.png")

    def type_card(name, lines, col=(18, 24, 60), accent=YEL):
        im = base(col).convert("RGBA"); d = ImageDraw.Draw(im)
        d.rectangle([34, 34, W - 34, H - 34], outline=WHT + (255,), width=6)
        d.rectangle([52, 52, W - 52, H - 52], outline=accent + (255,), width=3)
        y = 360
        for txt, size, fill in lines:
            sp = fit(txt, "TitanOne.ttf", size, 600, fill=fill, stroke=8)
            im.alpha_composite(sp, ((W - sp.width) // 2, y)); y += sp.height + 26
        im.convert("RGB").save(f"{SK}/cards/{name}.png")

    photo_card("01_blackbuck.jpg", "blackbuck")
    photo_card("02_nokha_dham.jpg", "nokha", crop=(0, 150, 1920, 1080))
    type_card("lawrence", [("LAWRENCE", 120, WHT), ("BISHNOI", 120, WHT), ("JAIL INTERVIEW", 62, YEL), ("NOKHA DHAM: MAAFI", 62, YEL)])
    type_card("zero", [("PAISE KA", 100, WHT), ("ZIKR:", 100, WHT), ("ZERO", 190, RED)], col=(40, 14, 20), accent=RED)
    type_card("whatsapp", [("\u20b95 CRORE", 130, YEL), ("MESSAGE", 96, WHT), ("MUMBAI TRAFFIC", 66, GRN), ("POLICE WHATSAPP", 66, GRN)], col=(10, 44, 38), accent=GRN)
    type_card("sabzi", [("JAMSHEDPUR", 96, WHT), ("KA", 70, YEL), ("SABZIWALA", 112, YEL)])
    type_card("galti", [("DO DIN BAAD:", 80, WHT), ("\u201cGALTI SE", 100, YEL), ("CHALA GAYA\u201d", 100, YEL)])
    type_card("mazdoor", [("KARNATAKA", 100, WHT), ("KA", 70, YEL), ("MAZDOOR", 120, YEL)])
    type_card("asli", [("ASLI PAISA", 112, WHT), ("KITNA", 112, WHT), ("CHALA?", 150, YEL)])
    type_card("galaxy", [("GALAXY", 120, WHT), ("APARTMENTS", 92, WHT), ("BANDRA", 92, YEL), ("APRIL 2024", 80, WHT)])
    type_card("lakh", [("GOLI:", 110, WHT), ("\u20b94 LAKH", 170, YEL), ("POLICE SOURCES KE", 56, WHT), ("HISAAB SE", 56, WHT)], col=(40, 14, 20), accent=RED)


def make_backgrounds():
    gfx_cards()


# ---------------------------------------------------------------- render video
def shake_offset(t):
    dx = dy = 0.0
    for t0, d, amp in SHAKES:
        if t0 <= t < t0 + d:
            k = 1 - (t - t0) / d
            dx += amp * k * np.sin(t * 91.0); dy += amp * k * np.cos(t * 77.0)
    return int(dx), int(dy)


def whip(img, u, direction):
    a = np.asarray(img).astype(np.float32)
    shift = int(u * W * 0.6) * direction
    acc = np.zeros_like(a)
    n = 7
    for k in range(n):
        acc += np.roll(a, shift + int((k - n / 2) * abs(u) * 40) * direction, axis=1)
    return Image.fromarray((acc / n).astype(np.uint8))


def endcard_frames(tmp):
    png = os.path.join(tmp, "card.png"); EC.card(png)
    card = Image.open(png).convert("RGB").resize((W, H), Image.LANCZOS)
    frames = []
    for i in range(int(CARD_LEN * FPS)):
        t = i / FPS
        if t < 0.25:
            frames.append(Image.fromarray(rng.integers(0, 255, (H, W, 1), dtype=np.uint8).repeat(3, 2)))
        else:
            frames.append(zoomed(np.asarray(card), 1 + 0.015 * (t - 0.25)))
    return frames


def render(out_video):
    tmp = os.path.join(SK, "tmp"); os.makedirs(tmp, exist_ok=True)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "15", "-preset", "veryfast",
                            "-pix_fmt", "yuv420p", out_video], stdin=subprocess.PIPE)
    si, cur, clip = -1, None, None
    for fi in range(int(round(CARD * FPS))):
        t = fi / FPS
        while si + 1 < len(SHOTS) and t >= SHOTS[si + 1]["t0"] - 1e-6:
            si += 1; cur = SHOTS[si]
            if clip:
                clip.close()
            clip = Clip(cur["path"], cur["src_in"], cur["speed"])
        arr = clip.next()
        z, cx, cy = cur["zoom"](t)
        img = zoomed(arr, z, cx, cy)
        dx, dy = shake_offset(t)
        if dx or dy:
            img = Image.fromarray(np.roll(np.roll(np.asarray(img), dy, 0), dx, 1))
        for k, tw in enumerate(WHIPS):
            d = 1 if k % 2 == 0 else -1
            if tw - 0.12 <= t < tw:
                img = whip(img, -(1 - (tw - t) / 0.12), d)
            elif tw <= t < tw + 0.12:
                img = whip(img, 1 - (t - tw) / 0.12, d)
        fr = img.convert("RGBA")
        for t0, t1, dr in EVENTS:
            if t0 <= t < t1:
                dr(fr, t)
        enc.stdin.write(fr.convert("RGB").tobytes())
    for im in endcard_frames(tmp):
        enc.stdin.write(im.convert("RGB").tobytes())
    enc.stdin.close(); enc.wait()


# ---------------------------------------------------------------- mix audio
def load(f):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


PLACED = {}
VOICE_LINES = [("P1", f"{SK}/seg/T1.wav", P1_AT), ("P2A", f"{SK}/seg/T2.wav", S0("A")),
               ("P2B", f"{SK}/seg/V.wav", VO0), ("P2C", f"{SK}/seg/T3.wav", S0("C"))]


def mix(out_wav):
    n = int(TOTAL * SR) + SR
    bus = np.zeros(n, np.float32)
    vbus = np.zeros(n, np.float32)
    dbus = np.zeros(n, np.float32)

    def put(b, x, t, g=1.0):
        i = int(round(t * SR)); j = min(n, i + len(x)); b[i:j] += g * x[: j - i]

    for lid, f, t0 in VOICE_LINES:
        x = load(f)
        end = REP.get(lid, {}).get("voice_end_s")
        if end is not None:
            fd = int(REP.get(lid, {}).get("fade_s", 0.05) * SR)
            x = x[: int(end * SR)].copy(); x[-fd:] *= np.linspace(1, 0, fd)
        put(vbus, x, t0); put(dbus, x, t0); PLACED[lid] = (t0, t0 + len(x) / SR, f)
    tmp = os.path.join(SK, "tmp"); os.makedirs(tmp, exist_ok=True)
    c1f = os.path.join(SK, "lines", "C1.wav")
    os.makedirs(os.path.dirname(c1f), exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{C1_IN:.3f}", "-to", f"{C1_OUT:.3f}", "-i", CUTWAV, "-ac", "1",
                    "-ar", str(SR), c1f], check=True)
    c1 = load(c1f)
    end = REP.get("C1", {}).get("voice_end_s")
    if end is not None:
        fd = int(REP.get("C1", {}).get("fade_s", 0.05) * SR); c1 = c1[: int(end * SR)].copy(); c1[-fd:] *= np.linspace(1, 0, fd)
    put(bus, c1, C1_IN); put(dbus, c1, C1_IN); PLACED["C1"] = (C1_IN, C1_IN + len(c1) / SR, c1f)
    bus += voice_room.treat(vbus)
    ring_x = VC.room(VC.peak(VC.ring(), -9)); click_x = VC.room(VC.peak(VC.click(), -12)); clack_x = VC.room(VC.peak(VC.clack(), -7))
    put(bus, ring_x, RING); put(bus, click_x, CLICK); put(bus, clack_x, HANGUP1 - 0.02)
    fx = {k: load(f"{SFX}/sfx_{k}.wav") for k in ("whoosh", "pop", "ding", "thud", "scratch", "riser", "stamp")}
    put(bus, fx["whoosh"], CLICK - 0.12, 0.5)                                  # crash zoom on the pick-up
    for tq, *_ in Q:
        put(bus, fx["pop"], tq, 0.45)
    put(bus, fx["thud"], 15.98, 0.5)                                            # WHY MONEY?
    put(bus, fx["whoosh"], Q_OUT0, 0.3)
    for tw in WHIPS:
        put(bus, fx["whoosh"], tw - 0.2, 0.5)
    for t0 in (25.54, 31.00):   # each caption
        put(bus, fx["pop"], t0, 0.3)
    put(bus, fx["scratch"], 33.40 - 0.05, 0.35); put(bus, fx["thud"], 33.40, 0.45)       # the ZERO card
    put(bus, fx["ding"], 49.30, 0.3); put(bus, fx["thud"], 49.30, 0.35)                  # the ASLI PAISA card
    put(bus, fx["riser"], 58.00 - 1.2, 0.25); put(bus, fx["thud"], 58.00, 0.5)           # GOLI: 4 LAKH
    put(bus, fx["thud"], 60.70, 0.6)                                                     # NAAM: 5 CRORE
    ew = os.path.join(tmp, "end.wav"); EC.audio(ew, CARD_LEN)
    ewq = os.path.join(tmp, "end_eq.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", ew, "-af", "highpass=f=300,lowpass=f=3400", "-ar", str(SR),
                    ewq], check=True)
    put(bus, load(ewq), CARD, 0.9)
    bus = bus[: int(TOTAL * SR)]; dbus = dbus[: int(TOTAL * SR)]
    m = max(1.0, np.abs(bus).max() / 0.95)
    for path, b, g in ((out_wav, bus, m), (os.path.join(tmp, "dialogue.wav"), dbus, 1.0)):
        pcm = (np.clip(b / g, -1, 1) * 32767).astype(np.int16)
        with wave.open(path, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


def write_qc_manifest():
    rel = lambda p: os.path.relpath(p, ROOT)
    segs, spans = {}, {}
    for sh in SHOTS:
        if sh["line"]:
            segs.setdefault(sh["line"], []).append([round(sh["t0"], 3), round(sh["t1"], 3)])
            spans.setdefault(sh["line"], []).append(
                [round(sh["src_in"], 3), round(sh["src_in"] + (sh["t1"] - sh["t0"]) * sh["speed"], 3)])
    edit = json.load(open(EDIT_JSON))
    lines = [{"id": "C1", "speaker": "caller", "start": round(PLACED["C1"][0], 3), "end": round(PLACED["C1"][1], 3),
              "source": rel(PLACED["C1"][2])}]
    for lid, f, t0 in VOICE_LINES:
        ln = {"id": lid, "speaker": "pandey", "start": round(PLACED[lid][0], 3), "end": round(PLACED[lid][1], 3),
              "source": rel(PLACED[lid][2])}
        if lid in TALK:
            ln.update(cut_in=round(CUT(lid), 3), segments=segs.get(lid, []), clip=rel(f"{V}/{TALK[lid][0]}.mp4"),
                      clip_spans=spans.get(lid, []))
        lines.append(ln)
    py = "pipeline/qcpy"   # the QC environment on a Mac, python3 in the cloud
    env = f"EDIT_JSON={rel(EDIT_JSON)} QC_REPAIRS={rel(REPAIRS)}"
    man = {"slug": SLUG, "format": "sahayata_kendra", "final": edit["out"],
           "script": f"registry/scripts/{SLUG}.json",
           "characters": {"pandey": "assets/characters/pandey_sheet_v2.jpg"},
           "dialogue_stem": rel(os.path.join(SK, "tmp", "dialogue.wav")),
           "prefinish": rel(os.path.join(SK, "edit_raw.mkv")),
           "length": {"min": 40, "max": 75, "expected": round(TOTAL, 2)},
           "loudness": {"target": edit.get("target_lufs", -14)},
           "repairs_file": rel(REPAIRS),
           "rebuild": f"{env} {py} {rel(SK)}/build.py && {py} pipeline/assemble.py {rel(EDIT_JSON)}",
           "lines": lines}
    path = os.path.join(os.path.dirname(EDIT_JSON), "qc_manifest.json")
    json.dump(man, open(path, "w"), indent=1, ensure_ascii=False)
    return path


if __name__ == "__main__":
    tmp = os.path.join(SK, "tmp"); os.makedirs(tmp, exist_ok=True)
    make_backgrounds()
    vid, wav = os.path.join(tmp, "video.mp4"), os.path.join(tmp, "mix.wav")
    talking = sum(sh["t1"] - sh["t0"] for sh in SHOTS if sh["line"])
    print(f"timeline: ring {RING:.2f}  P2 {FIRST['A']:.2f}  Billu {BILLU_IN:.2f}  card {CARD:.2f}  total {TOTAL:.2f}  "
          f"talking to camera {talking:.1f} s = {100 * talking / TOTAL:.0f}%")
    for sh in SHOTS:
        end_src = sh["src_in"] + (sh["t1"] - sh["t0"]) * sh["speed"]
        d = dur(sh["path"]) if sh["path"].endswith(".mp4") else 99
        flag = "  <-- runs past the clip" if end_src > d - 0.02 else ""
        print(f"  {sh['t0']:6.2f}-{sh['t1']:6.2f}  {os.path.basename(sh['path']):14s} src {sh['src_in']:5.2f}-{end_src:5.2f} of {d:5.2f}{flag}")
    if os.environ.get("PLAN_ONLY"):
        sys.exit()
    mix(wav); print("mixed", wav)
    print("qc manifest", write_qc_manifest())
    render(vid); print("rendered", vid)
    out = os.path.join(SK, "edit_raw.mkv")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", "-shortest", out], check=True)
    print("wrote", out, f"{dur(out):.2f}s")
