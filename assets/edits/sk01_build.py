#!/usr/bin/env python3
"""SK01 edit: composes every frame in Python (zooms, whip pans, shakes, kinetic text, captions) and mixes the
sound with numpy, then hands one raw 720x1280 file to assemble.py for the kendra look and loudness.
  python3 work/sk01/build.py  ->  work/sk01/edit_raw.mkv"""
import os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = "/home/user/doordhan-factory"
SK = f"{ROOT}/work/sk01"
V, VO, SFX = f"{SK}/vid", f"{SK}/voice", f"{ROOT}/assets/audio"
FONTS = f"{ROOT}/assets/fonts"
W, H, FPS, SR = 720, 1280, 25, 48000
sys.path.insert(0, f"{ROOT}/pipeline")
import sahayata_endcard as EC  # noqa: E402

rng = np.random.default_rng(3)


def font(name, size):
    return ImageFont.truetype(f"{FONTS}/{name}", size, layout_engine=ImageFont.Layout.RAQM)


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                                capture_output=True, text=True).stdout)


# ---------------------------------------------------------------- audio timeline (reel seconds)
S = {}  # line starts
S["C1"] = 3.55
C1_END = S["C1"] + 5.05
Q_OUT0, Q_OUT1 = C1_END - 0.05, C1_END + 0.35   # the question clears before he hangs up
HANGUP1 = Q_OUT1 + 0.25                        # first cradle clack, on a clean frame
S["P1"] = HANGUP1 + 0.75
S["P2"] = S["P1"] + 5.80 + 0.30
P2_END = 9.05                     # "Ghatao" ends here; the file then has a breath Wan lip-syncs as a half-open mouth
S["P3"] = S["P2"] + P2_END + 0.35
S["P4"] = S["P3"] + 10.20 + 0.35
S["P5"] = S["P4"] + 11.20 + 0.35
S["P6"] = S["P5"] + 6.45 + 0.50
P6_END = S["P6"] + 4.40
BILLU_END = P6_END + 2.7          # Billu blinks, then turns away
HANG = BILLU_END + 0.35           # cradle clack of the final hang-up (ring burst before it)
CARD = HANG + 0.55                # closing card starts
CARD_LEN = 4.8
TOTAL = CARD + CARD_LEN
LEAD = 0.12                       # Wan tracks start 0.12 s before the line

# qc_gate.py repairs (pipeline/qc_gate.py writes them; this build applies them), per line:
#   src_shift_s      move the talking clip's source start (a constant lip-sync offset)
#   cut_in_delay_s   cut to the talking shot later (+) or earlier (-) than LEAD before the line (a wrong lead)
#   voice_end_s      end the voice line here, with a fade_s fade (default 50 ms): a hard-cut or truncated line end
import json  # noqa: E402
EDIT_JSON = os.environ.get("EDIT_JSON", f"{SK}/edit.json")
REPAIRS = os.environ.get("QC_REPAIRS", f"{SK}/qc_repairs.json")
REP = json.load(open(REPAIRS)) if os.path.exists(REPAIRS) else {}


def CUT(line):
    """reel time the talking shot for this line cuts in"""
    return S[line] - LEAD + REP.get(line, {}).get("cut_in_delay_s", 0.0)


def P(line, t):
    """reel time of a moment t seconds into a voice line"""
    return S[line] + t


# ---------------------------------------------------------------- text sprites
YEL, WHT, RED, GRN, INK = (255, 214, 0), (255, 255, 255), (235, 40, 40), (60, 220, 90), (15, 15, 25)


_CMAPS = {}


def has(fnt, ch):
    from fontTools.ttLib import TTFont
    path = fnt.path
    if path not in _CMAPS:
        _CMAPS[path] = TTFont(path).getBestCmap()
    return ord(ch) in _CMAPS[path] or ch == " "


def runs(text, fnt):
    """split text into (string, font) runs; characters the font lacks (the rupee sign) fall back to Baloo 2 Devanagari"""
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


def tick_sprite(size=54):
    im = Image.new("RGBA", (size + 16, size + 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = [(8, size * 0.55), (size * 0.4, size * 0.9), (size + 6, 10)]
    d.line(pts, fill=INK, width=18, joint="curve"); d.line(pts, fill=GRN, width=10, joint="curve")
    return im


def fit(text, name, size, maxw, **kw):
    while size > 20:
        sp = sprite(text, font(name, size), **kw)
        if sp.width <= maxw:
            return sp
        size -= 4
    return sp


def pop_scale(age, dur=0.16):
    """0.55 -> 1.12 -> 1.0 over dur: a word popping on"""
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


# events: (start, end, drawer(frame, t))
EVENTS = []


def text_event(t0, t1, text, name="Baloo2-Latin-ExtraBold.ttf", size=64, fill=WHT, cx=W / 2, cy=1010,
               maxw=660, pop=True, fade_out=0.08, angle=0, stroke=6):
    sp = fit(text, name, size, maxw, fill=fill, stroke=stroke)

    def draw(fr, t):
        age = t - t0
        sc = pop_scale(age) if pop else 1.0
        al = min(1.0, (t1 - t) / fade_out) if t1 - t < fade_out else 1.0
        paste(fr, sp, cx, cy, sc, al, angle)
    EVENTS.append((t0, t1, draw))


def stack(text, name, size, maxw, **kw):
    """one line if it fits at full size, else two balanced lines (never shrink a caption to fit)"""
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


def caption(t0, t1, text, fill=WHT):
    sp = stack(text, "Baloo2-Latin-ExtraBold.ttf", 66, 660, fill=fill, stroke=6)

    def draw(fr, t):
        al = min(1.0, (t1 - t) / 0.08) if t1 - t < 0.08 else 1.0
        paste(fr, sp, W / 2, 1015, pop_scale(t - t0), al)
    EVENTS.append((t0, t1, draw))


# ---------------------------------------------------------------- shots
class Clip:
    """Sequential frame reader for one shot: frames at 25 fps from src_in, speed factor, scaled to 720x1280."""

    def __init__(self, path, src_in=0.0, speed=1.0):
        vf = f"setpts=PTS/{speed},fps={FPS},scale={W}:{H}:flags=lanczos,format=rgb24" if speed != 1 else \
            f"fps={FPS},scale={W}:{H}:flags=lanczos,format=rgb24"
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{src_in:.3f}", "-i", path, "-vf", vf, "-an",
                                   "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
        self.last = None

    def next(self):
        b = self.p.stdout.read(W * H * 3)
        if len(b) == W * H * 3:
            self.last = np.frombuffer(b, np.uint8).reshape(H, W, 3)
        return self.last


def ease(u):
    u = min(1, max(0, u)); return u * u * (3 - 2 * u)


def zoomed(arr, z, cx=W / 2, cy=H / 2):
    if z <= 1.001:
        return Image.fromarray(arr)
    cw, ch = W / z, H / z
    x0 = min(max(0, cx - cw / 2), W - cw); y0 = min(max(0, cy - ch / 2), H - ch)
    return Image.fromarray(arr).resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))


# Each shot: start, end, clip factory, zoom(t) -> (z, cx, cy)
FACE_FRONT = (360, 600)     # T1/T5 face centre in 720x1280
FACE_LEFT = (395, 490)      # T2
FACE_LOW = (400, 500)       # T3
FACE_RIGHT = (370, 490)     # T4/T6


def const(z, c=(W / 2, H / 2)):
    return lambda t: (z, c[0], c[1])


def ramp(t0, t1, z0, z1, c):
    return lambda t: (z0 + (z1 - z0) * ease((t - t0) / max(1e-3, t1 - t0)), c[0], c[1])


def steps(pairs, c):
    """piecewise constant zoom: [(from_time, zoom), ...]"""
    def f(t):
        z = pairs[0][1]
        for tt, zz in pairs:
            if t >= tt:
                z = zz
        return (z, c[0], c[1])
    return f


# Talking clips: (file, the silence before the first word in its Wan track). v1 tracks had 0.12 s (and ran 8.8% fast:
# the make_track concat bug); v2 tracks have 0.5 s so Wan's slow first second happens before he speaks.
TALK = {k: (f"{V}/{f}", lead) for k, (f, lead) in {
    "P1": ("T1b.mp4", 0.12), "P2": ("T2.mp4", 0.12), "P3": ("T3.mp4", 0.12), "P4": ("T4.mp4", 0.12),
    "P5": ("T5.mp4", 0.12), "P6": ("T6.mp4", 0.12)}.items()}
for k in TALK:  # prefer a v2 clip when it exists
    n = k[1]
    if os.path.exists(f"{V}/T{n}v2.mp4"):
        TALK[k] = (f"{V}/T{n}v2.mp4", 0.5)


V1_STRETCH = 48000 / 44100   # v1 clips were lip-synced to speech played this much too fast
SPEED = {}                   # path -> playback speed used by shot()


def TK(line, t0):
    """(path, src_in) for a talking shot of this line that starts at reel time t0, in sync with the voice at S[line].
    v1 clips: after their 0.12 s lead the speech ran 8.8% fast, so they play slowed by the same factor, which puts
    the lips back on the real-speed voice (clip time c = 0.12 + (u - 0.12) / 1.0884 for reel offset u)."""
    path, lead = TALK[line]
    extra = t0 - (S[line] - LEAD)
    shift = REP.get(line, {}).get("src_shift_s", 0.0)
    if lead == 0.12:
        SPEED[path] = 1 / V1_STRETCH
        return path, 0.12 - (0.12 - extra) / V1_STRETCH + shift
    return path, lead - LEAD + extra + shift


SHOTS = []


def shot(t0, t1, path, src_in, zoom, speed=None):
    SHOTS.append(dict(t0=t0, t1=t1, path=path, src_in=src_in, zoom=zoom, speed=speed or SPEED.get(path, 1.0)))


# 1. cold open: both turn to the ringing phone; slow creep
shot(0.0, 2.74, f"{V}/t01_coldopen.mp4", 1.30, ramp(0, 2.74, 1.0, 1.07, (360, 760)))
# 2. pick-up: crash in on the listening close-up, question builds
shot(2.74, Q_OUT1, f"{V}/K2.mp4", 0.0,
     lambda t: (1.0 + 0.32 * (1 - ease((t - 2.74) / 0.22)) + 0.10 * ease((t - 3.0) / 5.2)
                - 0.12 * ease((t - Q_OUT0) / (Q_OUT1 - Q_OUT0)), 360, 560), speed=0.80)
# 3. overhead: receiver slammed down (jolt at the clack)
shot(Q_OUT1, CUT("P1"), f"{V}/K3.mp4", 0.10, const(1.12, (360, 560)))
# 4. P1 front: pull back on the sigh, punch in on "net worth kya hai"
T1_0 = CUT("P1")
shot(T1_0, CUT("P2"), *TK("P1", T1_0),
     lambda t: (ramp(P("P1", 0.0), P("P1", 1.1), 1.25, 1.0, FACE_FRONT)(t)[0] if t < P("P1", 4.95)
                else 1.0 + 0.22 * ease((t - P("P1", 4.95)) / 0.12), *FACE_FRONT))
# 5. P2 3/4 left: a new framing on every "Gino"; whip to Billu on "Loan hai?", whip back for "Ghatao"
g = [P("P2", x) for x in (0.65, 1.85, 2.95, 5.5)]
LOAN, GHATAO = P("P2", 6.30), P("P2", 8.10)
shot(CUT("P2"), LOAN, *TK("P2", CUT("P2")),
     steps([(0, 1.0), (g[0], 1.28), (g[1], 1.0), (g[2], 1.45), (g[3], 1.12)], FACE_LEFT))
shot(LOAN, GHATAO, f"{V}/K4.mp4", 0.0, ramp(LOAN, GHATAO, 1.05, 1.18, (360, 700)))
shot(GHATAO, CUT("P3"), *TK("P2", GHATAO), const(1.22, FACE_LEFT))
# 6. P3 low angle: numbers fly; crash zoom on the eyes at "Nahi"; slam "90 lakh"
NAHI, MOTA, LAKH = P("P3", 6.28), P("P3", 7.25), P("P3", 8.88)
shot(CUT("P3"), CUT("P4"), *TK("P3", CUT("P3")),
     lambda t: ((1.0 + 0.1 * ease((t - S["P3"]) / 6.0)) if t < NAHI else
                (1.0 + 0.6 * ease((t - NAHI) / 0.1)) if t < MOTA else
                (1.0 if t < LAKH else 1.0 + 0.1 * ease((t - LAKH) / 0.15)), *FACE_LOW))
# 7. P4 3/4 right: neighbour; slow push from "Bhai"
BHAI, WOH = P("P4", 7.95), P("P4", 9.10)
shot(CUT("P4"), CUT("P5"), *TK("P4", CUT("P4")),
     lambda t: (1.0 if t < BHAI else 1.0 + 0.1 * ease((t - BHAI) / (P("P4", 11.2) - BHAI)), *FACE_RIGHT))
# 8. P5 front: comment / like
shot(CUT("P5"), CUT("P6"), *TK("P5", CUT("P5")),
     steps([(0, 1.0), (P("P5", 3.8), 1.2), (P("P5", 5.85), 1.35)], FACE_FRONT))
# 9. P6: Billu line, eyes to the cat
BILLU_IN_TWO = (175, 860)   # Billu's centre in the v2 two-shot (720x1280)
if TALK["P6"][1] == 0.5:  # v2: the two-shot with Billu in frame; creep in on Billu over the line
    shot(CUT("P6"), P6_END + 0.05, *TK("P6", CUT("P6")),
         lambda t: (1.0 + 1.05 * ease((t - P("P6", 0.3)) / 3.9), 360 + (BILLU_IN_TWO[0] - 360) * ease((t - P("P6", 0.3)) / 3.9),
                    640 + (BILLU_IN_TWO[1] - 640) * ease((t - P("P6", 0.3)) / 3.9)))
else:
    shot(CUT("P6"), P6_END + 0.05, *TK("P6", CUT("P6")), ramp(S["P6"], P6_END, 1.0, 1.12, FACE_RIGHT))
# 10. Billu turns away
if os.path.exists(f"{V}/K5.mp4") and TALK["P6"][1] == 0.5:  # continues the zoom-in on the sitting Billu
    shot(P6_END + 0.05, BILLU_END + 0.15, f"{V}/K5.mp4", 0.6, const(1.0))
else:
    shot(P6_END + 0.05, BILLU_END + 0.15, f"{V}/K4.mp4", 1.05, const(1.05, (360, 700)))
# 11. phone rings again; he hangs up without answering
shot(BILLU_END + 0.15, CARD, f"{V}/K3.mp4", 0.10, const(1.12, (360, 560)))

WHIPS = [LOAN, GHATAO] + ([] if TALK["P6"][1] == 0.5 else [P6_END + 0.05])          # whip-pan transitions (direction alternates)
SHAKES = [(HANGUP1, 0.25, 14), (GHATAO + 0.12, 0.3, 16), (NAHI, 0.2, 10), (LAKH, 0.35, 22), (HANG, 0.25, 14),
          (P("P4", 9.1), 0.25, 8)]

# ---------------------------------------------------------------- graphics / text events
# ring onomatopoeia on each ring pair
for t0 in (0.05, 1.65):
    for k in range(3):
        a, b = t0 + k * 0.24, t0 + k * 0.24 + 0.2
        text_event(a, b, "TRRRING!", name="Bungee.ttf", size=92, fill=YEL, cx=500 + (k % 2) * 18,
                   cy=985 - k * 10, angle=(-8 if k % 2 else 6), pop=False, fade_out=0.02)
# the question, in English, builds word by word over the caller (from C1 phrase timings)
Q = [(1.85, "HOW MUCH", 108, WHT, 250), (2.60, "MONEY", 150, WHT, 395), (3.30, "TO BE IN", 100, WHT, 560),
     (3.90, "INDIA'S", 132, WHT, 700), (4.30, "TOP 1%?", 210, YEL, 900)]
for tq, txt, sz, col, y in Q:
    sp = fit(txt, "TitanOne.ttf", sz, 680, fill=col, stroke=9)
    t0 = S["C1"] + tq

    def dq(fr, t, sp=sp, t0=t0, y=y):
        al = 1 - ease((t - Q_OUT0) / (Q_OUT1 - Q_OUT0))
        sc = pop_scale(t - t0) * (1 + 0.25 * ease((t - Q_OUT0) / (Q_OUT1 - Q_OUT0)))
        paste(fr, sp, W / 2, y, sc, al)
    EVENTS.append((t0, Q_OUT1, dq))
# dim the picture behind the question
EVENTS.insert(0, (S["C1"] + 1.8, Q_OUT1, lambda fr, t: fr.alpha_composite(
    Image.new("RGBA", (W, H), (0, 0, 0, int(95 * min(1, (t - S["C1"] - 1.8) / 0.2) *
                                         (1 - ease((t - Q_OUT0) / (Q_OUT1 - Q_OUT0))))))) ))

# P1 captions
caption(P("P1", 0.95), P("P1", 2.40), "SABKE TOP 1% MEIN JAANA HAI,")
caption(P("P1", 2.62), P("P1", 3.0), "KA.", fill=YEL)
caption(P("P1", 3.02), P("P1", 4.0), "LEKIN AAP NET WORTH")
caption(P("P1", 4.0), P("P1", 4.95), "KI BAAT KAR RAHE HAIN NA?")
text_event(P("P1", 4.97), S["P2"] - LEAD, "NET WORTH = ?", name="TitanOne.ttf", size=112, fill=YEL, cy=300,
           stroke=9)

# P2 tally board (top) + captions
ITEMS = [("GHAR", 0.0, 0.65), ("ZAMEEN", 1.15, 1.85), ("GOLD", 2.35, 2.95), ("SHARES · MF · FD", 3.5, 5.5)]
board_f = font("Bungee.ttf", 40)
tally_spr = {}
for name, ta, tg in ITEMS:
    tally_spr[name] = (sprite(name, board_f, WHT, stroke=4, shadow=4, pad=8),
                       sprite("+", font("Bungee.ttf", 50), GRN, stroke=4, shadow=4, pad=8))
loan_spr = sprite("LOAN", board_f, WHT, stroke=4, shadow=4, pad=8)
minus_spr = sprite("−", font("Bungee.ttf", 58), RED, stroke=4, shadow=4, pad=8)
BOARD_END = S["P3"] - LEAD


def draw_board(fr, t):
    d = ImageDraw.Draw(fr)
    n_rows = sum(1 for _, ta, _ in ITEMS if t >= P("P2", ta)) + (1 if t >= GHATAO else 0)
    d.rounded_rectangle([40, 150, 470, 170 + 64 * n_rows], 18, fill=(10, 20, 60, 190), outline=YEL, width=4)
    for i, (name, ta, tg) in enumerate(ITEMS):
        if t < P("P2", ta):
            continue
        y = 196 + i * 64
        ns, ps = tally_spr[name]
        paste(fr, ps, 78, y, pop_scale(t - P("P2", tg)) if t >= P("P2", tg) else 0)
        paste(fr, ns, 108 + ns.width / 2, y, pop_scale(t - P("P2", ta), 0.12))
    if t >= GHATAO:
        y = 196 + 4 * 64
        paste(fr, minus_spr, 78, y, pop_scale(t - GHATAO - 0.1))
        paste(fr, loan_spr, 108 + loan_spr.width / 2, y, pop_scale(t - GHATAO, 0.12))


EVENTS.append((P("P2", 0.0), LOAN, draw_board))
EVENTS.append((GHATAO, BOARD_END, draw_board))
for (name, ta, tg), q in zip(ITEMS, ["GHAR HAI?", "ZAMEEN HAI?", "GOLD HAI?", "SHARES, MF, FD HAI?"]):
    caption(P("P2", ta), P("P2", tg), q)
    nxt = [x for x in [i[1] for i in ITEMS] if x > tg]
    text_event(P("P2", tg), P("P2", nxt[0]) if nxt else LOAN, "GINO.", name="TitanOne.ttf", size=120, fill=GRN,
               cy=1000, stroke=8)
text_event(LOAN, GHATAO, "LOAN HAI?", name="TitanOne.ttf", size=110, fill=WHT, cy=1030, stroke=8)
text_event(GHATAO + 0.05, BOARD_END, "GHATAO!", name="TitanOne.ttf", size=150, fill=RED, cy=1000, stroke=9,
           angle=-6)

# P3 numbers: bigger each time, crossed out on "Nahi", then the slam
NUMS = [(3.2, "₹2 CRORE?", 88, (170, 430), -8), (4.25, "₹5 CRORE?", 112, (540, 600), 7),
        (5.15, "₹100 CRORE?", 138, (360, 830), -4)]
caption(P("P3", 0.0), P("P3", 1.1), "AB TUM KAHOGE…")
caption(P("P3", 1.5), P("P3", 3.1), "TOP 1% HAI…")
for tn, txt, sz, (x, y), ang in NUMS:
    sp = fit(txt, "TitanOne.ttf", sz, 600, fill=YEL, stroke=8)
    t0 = P("P3", tn)

    def dn(fr, t, sp=sp, t0=t0, x=x, y=y, ang=ang):
        xx = min(max(x, sp.width / 2 - 6), W - sp.width / 2 + 6)
        paste(fr, sp, xx, y, pop_scale(t - t0, 0.2), 1, ang)
        if t >= NAHI:  # red strike
            d = ImageDraw.Draw(fr); w = sp.width * 0.45
            k = ease((t - NAHI) / 0.1)
            d.line([xx - w, y + 12, xx - w + 2 * w * k, y - 12 + 0], fill=RED, width=16)
    EVENTS.append((t0, MOTA, dn))
text_event(NAHI, MOTA, "NAHI.", name="TitanOne.ttf", size=170, fill=RED, cy=1040, stroke=10)
caption(MOTA, LAKH, "MOTA-MOTA…")
text_event(LAKH, S["P4"] - LEAD, "₹90 LAKH", name="TitanOne.ttf", size=190, fill=YEL, cy=900, stroke=11)
text_event(LAKH + 0.05, S["P4"] - LEAD, "= TOP 1% (PER ADULT)", name="Bungee.ttf", size=44, fill=WHT, cy=1045,
           stroke=5)

# P4 neighbour checklist
caption(P("P4", 0.1), P("P4", 1.3), "AB ISKA MATLAB SAMJHO:")
CHECK = [(1.65, "PADOSI KA ₹1 CR GHAR"), (4.55, "LOAN POORA KHATAM"), (5.75, "THODA MF + FD")]
ck_spr = [(P("P4", tc), sprite(tx, font("Bungee.ttf", 38), WHT, stroke=4, shadow=4, pad=8)) for tc, tx in CHECK]
tick = tick_sprite()


def draw_check(fr, t):
    n = sum(1 for tc, _ in ck_spr if t >= tc)
    d = ImageDraw.Draw(fr)
    d.rounded_rectangle([30, 150, 690, 170 + 70 * n], 18, fill=(10, 20, 60, 190), outline=YEL, width=4)
    for i, (tc, sp) in enumerate(ck_spr):
        if t < tc:
            continue
        y = 200 + i * 70
        paste(fr, tick, 75, y, pop_scale(t - tc - 0.25))
        paste(fr, sp, 115 + sp.width / 2, y, pop_scale(t - tc, 0.12))


EVENTS.append((P("P4", 1.65), BHAI, draw_check))
caption(BHAI, WOH, "BHAI…")
text_event(WOH, S["P5"] - LEAD, "WOH TOP 1% MEIN HAI.", name="TitanOne.ttf", size=86, fill=YEL, cy=1010,
           stroke=8)

# P5
caption(P("P5", 0.05), P("P5", 1.2), "AB BATAO,")
caption(P("P5", 1.2), P("P5", 3.4), "KIS-KIS KE PAAS ₹90 LAKH HAI?")
text_event(P("P5", 3.8), P("P5", 4.9), "COMMENT KARO", name="TitanOne.ttf", size=110, fill=WHT, cy=1000, stroke=8)
caption(P("P5", 4.9), P("P5", 5.85), "AUR BAAKI GAREEB…")
text_event(P("P5", 5.85), S["P6"] - LEAD, "BAS LIKE KARO", name="TitanOne.ttf", size=104, fill=RED, cy=1000,
           stroke=8)

def arrow_sprite(col):
    im = Image.new("RGBA", (150, 190), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = [(45, 8), (105, 8), (105, 95), (142, 95), (75, 182), (8, 95), (45, 95)]
    d.polygon([(x + 5, y + 5) for x, y in pts], fill=(0, 0, 0, 160)); d.polygon(pts, fill=col, outline=INK, width=6)
    return im


def arrows(t0, t1, col):
    a = arrow_sprite(col)

    def draw(fr, t):
        bob = 18 * abs(np.sin((t - t0) * 9))
        for x in (170, 550):
            paste(fr, a, x, 1150 + bob, pop_scale(t - t0), 1)
    EVENTS.append((t0, t1, draw))


arrows(P("P5", 3.8), P("P5", 4.9), WHT)
arrows(P("P5", 5.85), S["P6"] - LEAD, RED)

# P6
caption(P("P6", 0.0), P("P6", 1.5), "BILLU KA GHAR HOTA,")
caption(P("P6", 1.55), P("P6", 4.15), "TOH WOH BHI TOP 1% MEIN HOTA,")
text_event(P("P6", 4.15), P6_END + 0.6, "KA?", name="TitanOne.ttf", size=150, fill=YEL, cy=1150, stroke=9)

# the DOORDHAN bug, top right, throughout the programme (not on the card)
bug = sprite("DOORDHAN", font("Bungee.ttf", 30), (255, 255, 255, 215), stroke=3, shadow=3, pad=6)
EVENTS.append((0, CARD, lambda fr, t: paste(fr, bug, W - 20 - bug.width / 2, 58, 1, 0.85)))


# ---------------------------------------------------------------- render video
def shake_offset(t):
    dx = dy = 0.0
    for t0, d, amp in SHAKES:
        if t0 <= t < t0 + d:
            k = 1 - (t - t0) / d
            dx += amp * k * np.sin(t * 91.0); dy += amp * k * np.cos(t * 77.0)
    return int(dx), int(dy)


def whip(img, u, direction):
    """u in [-1,1]: 0 = no offset; blur and slide horizontally"""
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
    n = int(CARD_LEN * FPS)
    for i in range(n):
        t = i / FPS
        if t < 0.25:
            frames.append(Image.fromarray(rng.integers(0, 255, (H, W, 1), dtype=np.uint8).repeat(3, 2)))
        else:
            z = 1 + 0.015 * (t - 0.25)
            frames.append(zoomed(np.asarray(card), z))
    return frames


def render(out_video):
    tmp = os.path.join(SK, "tmp"); os.makedirs(tmp, exist_ok=True)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "15", "-preset", "veryfast",
                            "-pix_fmt", "yuv420p", out_video], stdin=subprocess.PIPE)
    nframes = int(round(CARD * FPS))
    si, cur, clip = -1, None, None
    whip_dir = 1
    for fi in range(nframes):
        t = fi / FPS
        while si + 1 < len(SHOTS) and t >= SHOTS[si + 1]["t0"] - 1e-6:
            si += 1; cur = SHOTS[si]
            if clip:
                clip.p.kill()
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
def load(f, mono=True):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def lufs_gain(x, target):
    rms = np.sqrt(np.mean(x[np.abs(x) > 1e-3] ** 2) + 1e-12)
    return 10 ** ((target - 20 * np.log10(rms)) / 20)


def mix(out_wav):
    n = int(TOTAL * SR) + SR
    bus = np.zeros(n, np.float32)

    dbus = np.zeros(n, np.float32)   # the dialogue as placed in the mix (qc_gate's line checks)

    def put(x, t, g=1.0):
        i = int(t * SR); j = min(n, i + len(x)); bus[i:j] += g * x[: j - i]

    def put_d(x, t):
        i = int(t * SR); j = min(n, i + len(x)); dbus[i:j] += x[: j - i]

    ring = load(f"{VO}/ring2.wav"); put(ring, 0.0, 0.8)
    put(load(f"{VO}/click.wav"), 3.22, 0.9)
    c1 = load(f"{VO}/C1_phone2.wav"); put(c1, S["C1"]); put_d(c1, S["C1"]); PLACED["C1"] = (S["C1"], S["C1"] + len(c1) / SR)
    put(load(f"{VO}/cradle.wav"), HANGUP1 - 0.02, 1.0)
    for ln in ("P1", "P2", "P3", "P4", "P5", "P6"):
        x = load(f"{VO}/v2/lev/{ln}.wav")
        end = REP.get(ln, {}).get("voice_end_s", P2_END + 0.05 if ln == "P2" else None)  # P2: drop the breath after "Ghatao"
        if end is not None:
            fd = int(REP.get(ln, {}).get("fade_s", 0.05) * SR)
            x = x[: int(end * SR)].copy(); x[-fd:] *= np.linspace(1, 0, fd)
        put(x, S[ln]); put_d(x, S[ln]); PLACED[ln] = (S[ln], S[ln] + len(x) / SR)
    # final: one ring burst, then the hang-up clack
    burst = load(f"{VO}/burst.wav"); put(burst, BILLU_END - 0.55, 0.8); put(burst, BILLU_END - 0.05, 0.8)
    put(load(f"{VO}/cradle.wav"), HANG - 0.02, 1.0)
    fx = {k: load(f"{SFX}/sfx_{k}.wav") for k in ("whoosh", "pop", "ding", "thud", "scratch", "riser", "stamp", "room")}
    put(fx["whoosh"], 2.62, 0.55)                                    # crash zoom on pick-up
    for tq, *_ in Q:
        put(fx["pop"], S["C1"] + tq, 0.5)
    put(fx["thud"], S["C1"] + 4.30, 0.55)                             # TOP 1%?
    put(fx["whoosh"], Q_OUT0, 0.35)                                   # zoom out as the question clears
    put(fx["pop"], P("P1", 4.97), 0.5)
    for name, ta, tg in ITEMS:
        put(fx["pop"], P("P2", ta), 0.35); put(fx["ding"], P("P2", tg), 0.25)
    for tw in WHIPS:
        put(fx["whoosh"], tw - 0.2, 0.6)
    put(fx["stamp"], GHATAO + 0.1, 0.8); put(fx["thud"], GHATAO + 0.1, 0.4)
    for tn, *_ in NUMS:
        put(fx["ding"], P("P3", tn), 0.3)
    put(fx["scratch"], NAHI - 0.28, 0.55)
    put(fx["thud"], LAKH, 0.75)
    for tc, _ in CHECK:
        put(fx["pop"], P("P4", tc), 0.35)
    put(fx["riser"], WOH - 1.4, 0.35); put(fx["ding"], WOH, 0.3)
    put(fx["pop"], P("P5", 3.8), 0.45); put(fx["pop"], P("P5", 5.85), 0.45)
    put(fx["pop"], P("P6", 4.15), 0.4)
    # room tone: the office fan, under everything until the card
    room = fx["room"]; reps = np.tile(room, int(CARD / (len(room) / SR)) + 2)[: int(CARD * SR)]
    reps *= lufs_gain(reps, -44) if False else 0.12
    fade = int(0.3 * SR); reps[-fade:] *= np.linspace(1, 0, fade)
    put(reps, 0.0, 1.0)
    # the closing card's own sound (disconnect beeps + hold music, phone EQ in ffmpeg below)
    tmp = os.path.join(SK, "tmp"); os.makedirs(tmp, exist_ok=True)
    ew = os.path.join(tmp, "end.wav"); EC.audio(ew, CARD_LEN)
    ewq = os.path.join(tmp, "end_eq.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", ew, "-af", "highpass=f=300,lowpass=f=3400", "-ar", str(SR),
                    ewq], check=True)
    put(load(ewq), CARD, 0.9)
    bus = bus[: int(TOTAL * SR)]; dbus = dbus[: int(TOTAL * SR)]
    m = max(1.0, np.abs(bus).max() / 0.95)
    for path, b in ((out_wav, bus), (os.path.join(tmp, "dialogue.wav"), dbus)):
        pcm = (np.clip(b / m, -1, 1) * 32767).astype(np.int16)
        with wave.open(path, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


PLACED = {}   # line -> (reel start, reel end) of the voice as placed in the mix


def write_qc_manifest():
    """work/sk01/qc_manifest.json for pipeline/qc_gate.py: where each line and its talking shots sit in the final"""
    talk_paths = {TALK[k][0]: k for k in TALK}
    segs, spans = {}, {}
    for sh in SHOTS:
        if sh["path"] in talk_paths:
            segs.setdefault(talk_paths[sh["path"]], []).append([round(sh["t0"], 3), round(sh["t1"], 3)])
            spans.setdefault(talk_paths[sh["path"]], []).append(
                [round(sh["src_in"], 3), round(sh["src_in"] + (sh["t1"] - sh["t0"]) * sh["speed"], 3)])
    rel = lambda p: os.path.relpath(p, ROOT)
    edit = json.load(open(EDIT_JSON))
    lines = [{"id": "C1", "speaker": "caller", "start": round(PLACED["C1"][0], 3), "end": round(PLACED["C1"][1], 3),
              "source": rel(f"{VO}/C1_phone2.wav")}]
    for ln in ("P1", "P2", "P3", "P4", "P5", "P6"):
        lines.append({"id": ln, "speaker": "pandey", "start": round(PLACED[ln][0], 3), "end": round(PLACED[ln][1], 3),
                      "source": rel(f"{VO}/v2/lev/{ln}.wav"), "cut_in": round(CUT(ln), 3), "segments": segs.get(ln, []),
                      "clip": rel(TALK[ln][0]), "clip_spans": spans.get(ln, [])})
    env = f"EDIT_JSON={rel(EDIT_JSON)} QC_REPAIRS={rel(REPAIRS)}"
    man = {"slug": "sk01", "format": "sahayata_kendra", "final": rel(edit["out"]),
           "script": "registry/scripts/sk01.json",
           "characters": {"pandey": "assets/characters/pandey_sheet_v2.jpg"},
           "dialogue_stem": rel(os.path.join(SK, "tmp", "dialogue.wav")),
           "prefinish": rel(os.path.join(SK, "edit_raw.mkv")),
           "length": {"min": 20, "max": 90, "expected": round(TOTAL, 2)},
           "loudness": {"target": edit.get("target_lufs", -14)},
           "repairs_file": rel(REPAIRS),
           "rebuild": f"{env} python3 work/sk01/build.py && python3 pipeline/assemble.py {rel(EDIT_JSON)}",
           "lines": lines}
    path = os.path.join(os.path.dirname(EDIT_JSON), "qc_manifest.json")
    json.dump(man, open(path, "w"), indent=1, ensure_ascii=False)
    return path


if __name__ == "__main__":
    tmp = os.path.join(SK, "tmp"); os.makedirs(tmp, exist_ok=True)
    vid, wav = os.path.join(tmp, "video.mp4"), os.path.join(tmp, "mix.wav")
    print(f"timeline: P1 {S['P1']:.2f}  P2 {S['P2']:.2f}  P3 {S['P3']:.2f}  P4 {S['P4']:.2f}  P5 {S['P5']:.2f}  "
          f"P6 {S['P6']:.2f}  card {CARD:.2f}  total {TOTAL:.2f}")
    mix(wav); print("mixed", wav)
    print("qc manifest", write_qc_manifest())
    render(vid); print("rendered", vid)
    out = os.path.join(SK, "edit_raw.mkv")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", "-shortest", out], check=True)
    print("wrote", out, f"{dur(out):.2f}s")
