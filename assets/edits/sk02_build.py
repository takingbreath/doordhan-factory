#!/usr/bin/env python3
"""SK02 (E6) edit, "Retire hone ke liye kitni SIP chahiye?": composes every frame in Python (zooms, whips, shakes,
kinetic text, captions) and mixes the sound with numpy, then hands one raw 720x1280 file to assemble.py for the
kendra look, VHS motion and ambience. Made from assets/edits/sk01_build.py (E5).
  pipeline/qcpy work/sk02/build.py  ->  work/sk02/edit_raw.mkv + work/sk02/qc_manifest.json
The voice is the approved draft cut (work/sk02/voice, Akhilesh 2026-10-03) with the new hook: P1, the caller C1 on the
landline chain, and the monologue P2 placed segment by segment (work/sk02/seg) so each talking clip lines up with its
own part of the line. Talking clips (Wan 2.7, 0.5 s lead in each track) map clip time c = 0.5 + (reel - seg start)."""
import json, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SK = f"{ROOT}/work/sk02"
V, SFX, FONTS = f"{SK}/vid", f"{ROOT}/assets/audio", f"{ROOT}/assets/fonts"
W, H, FPS, SR = 720, 1280, 25, 48000
sys.path.insert(0, f"{ROOT}/pipeline")
import sahayata_endcard as EC  # noqa: E402
import voice_room  # noqa: E402
import voice_cut as VC  # noqa: E402  (the draft cut's ring, pick-up click and cradle clack)

rng = np.random.default_rng(6)
EDIT_JSON = os.environ.get("EDIT_JSON", f"{SK}/edit.json")
REPAIRS = os.environ.get("QC_REPAIRS", f"{SK}/qc_repairs.json")
REP = json.load(open(REPAIRS)) if os.path.exists(REPAIRS) else {}


def font(name, size):
    return ImageFont.truetype(f"{FONTS}/{name}", size, layout_engine=ImageFont.Layout.RAQM)


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                                capture_output=True, text=True).stdout)


# ---------------------------------------------------------------- audio timeline (reel seconds)
SEG = json.load(open(f"{SK}/seg/segments.json"))       # P2 segments: p2_start / p2_end inside lines/P2.wav
S = {"P1": 0.12}                                         # the hook; the cold-open shot starts 0.12 s before it
RING = S["P1"] + 2.50 + 0.25                             # P1.wav is 2.50 s; one ring 0.25 s after it (the draft cut)
CLICK = RING + 1.2
S["C1"] = CLICK + 0.33
C1_END = S["C1"] + 11.06
Q_OUT0, Q_OUT1 = C1_END - 0.05, C1_END + 0.35           # the question clears before he hangs up
HANGUP1 = Q_OUT1 + 0.25                                  # cradle clack, on a clean frame
S["P2"] = HANGUP1 + 0.75
P2_END = S["P2"] + 40.88
BILLU0 = P2_END + 0.23                                   # cut about 0.25 s after "nahi"
BILLU_END = BILLU0 + 3.40                                # Billu at the bowl, then the last ring
HANG = BILLU_END + 0.35 + 0.15                           # he hangs up without answering
CARD = HANG + 0.55
CARD_LEN = 4.8
TOTAL = CARD + CARD_LEN
LEAD = 0.12                                              # talking shots cut in 0.12 s before the first word
TRACK_LEAD = 0.5                                         # silence before the line in every Wan track


def R(seg):
    """reel time where segment seg's wav starts"""
    return S["P2"] + SEG[seg]["p2_start"]


def W2(seg, t):
    """reel time of a moment t seconds into the whole monologue (P2.wav), as placed by segment"""
    return S["P2"] + t


# Talking clips: line id -> (clip, reel time its track's line starts, segment wav, keyframe face centre)
TALK = {
    "P1": ("T1", S["P1"]), "P2A": ("T2", R("A")), "P2B": ("T3", R("B")), "P2D": ("T4", R("D")),
    "P2F": ("T5", R("F")), "P2G": ("T6", R("G")), "P2I": ("T7", R("I")), "P2J": ("T8", R("J")),
}
JUDGE_SHIFT = {"P2D": -0.10}   # shot_spec.py judge on T4: ACCEPT_WITH_SHIFT, -140 ms constant -> src_in -0.100 s


def CUT(line):
    """reel time the talking shot for this line cuts in (0.12 s before the first word; segment wavs start 0.02 s
    before their first word, P1.wav 0.12 s)"""
    first = 0.12 if line == "P1" else 0.02
    return TALK[line][1] + first - LEAD + REP.get(line, {}).get("cut_in_delay_s", 0.0)


def TK(line, t0):
    """(path, src_in) of the talking clip for this line, starting at reel t0, in sync with its voice"""
    clip, r0 = TALK[line]
    shift = JUDGE_SHIFT.get(line, 0.0) + REP.get(line, {}).get("src_shift_s", 0.0)
    return f"{V}/{clip}.mp4", TRACK_LEAD + (t0 - r0) + shift


# ---------------------------------------------------------------- text sprites (from sk01_build)
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


def caption(t0, t1, text, fill=WHT, cy=1015):
    sp = stack(text, "Baloo2-Latin-ExtraBold.ttf", 66, 610, fill=fill, stroke=6)

    def draw(fr, t):
        al = min(1.0, (t1 - t) / 0.08) if t1 - t < 0.08 else 1.0
        paste(fr, sp, W / 2, cy, pop_scale(t - t0), al)
    EVENTS.append((t0, t1, draw))


def tag(t0, t1, text, cy=215, fill=WHT, size=40):
    """a small assumption tag at the top ('12% RETURN MAAN KE'): navy plate, Bungee"""
    sp = sprite(text, font("Bungee.ttf", size), fill, stroke=4, shadow=4, pad=10)
    plate = Image.new("RGBA", (sp.width + 36, sp.height + 18), (0, 0, 0, 0))
    ImageDraw.Draw(plate).rounded_rectangle([0, 0, plate.width - 1, plate.height - 1], 14, fill=NAVY + (215,),
                                            outline=YEL, width=3)
    plate.alpha_composite(sp, (18, 9))

    def draw(fr, t):
        al = min(1.0, (t1 - t) / 0.1) if t1 - t < 0.1 else 1.0
        paste(fr, plate, W / 2, cy, pop_scale(t - t0, 0.12), al)
    EVENTS.append((t0, t1, draw))


# ---------------------------------------------------------------- shots
class Clip:
    """Sequential frame reader for one shot: frames at 25 fps from src_in, speed factor, scaled to 720x1280.
    A still image (.png) is held for the whole shot."""

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
    """piecewise zoom: [(from_time, zoom), ...]; glide > 0 eases each change over that many seconds"""
    def f(t):
        z = pairs[0][1]
        for i, (tt, zz) in enumerate(pairs):
            if t >= tt:
                prev = pairs[i - 1][1] if i else zz
                z = prev + (zz - prev) * ease((t - tt) / glide) if glide else zz
        return (z, c[0], c[1])
    return f


# face centres (720x1280), measured on each clip with work/sk02/mouthbox.py
FACE = {"T1": (386, 453), "T2": (380, 613), "T3": (394, 441), "T4": (411, 473), "T5": (358, 496), "T6": (390, 596),
        "T7": (412, 498), "T8": (360, 517), "K2": (364, 594)}
EYES = {"T3": (385, 378), "T7": (422, 432), "T8": (355, 468)}
SHOTS = []


def shot(t0, t1, path, src_in, zoom, speed=1.0, line=None):
    SHOTS.append(dict(t0=t0, t1=t1, path=path, src_in=src_in, zoom=zoom, speed=speed, line=line))


def talk(line, t0, t1, zoom):
    path, src = TK(line, t0)
    shot(t0, t1, path, src, zoom, line=line)


# P2 word times (seconds into P2.wav, Scribe on work/sk02/lines/P2.wav)
def p2(t):
    return S["P2"] + t


K1_IN = RING + 0.05
K5A, K5A_END = S["C1"] + 1.35, S["C1"] + 2.95          # Billu blinks on "...Sahayata Kendra? Pandey ji"
K2_OUT = Q_OUT1
K2_SPEED = 6.95 / ((K5A - CLICK) + (K2_OUT - K5A_END))  # the 7 s listening clip covers the call around Billu's cutaway
OH_SRC = 0.10

# 1. cold open: the hook to the lens, Billu big at left, phone right; a slow creep
talk("P1", 0.0, K1_IN, ramp(0.0, K1_IN, 1.0, 1.06, (380, 640)))
# 2. the ring: both look at the phone (K1 starts from T1's last clean frame)
shot(K1_IN, CLICK, f"{V}/K1.mp4", 0.15, const(1.03, (380, 640)), speed=1.3)
# 3. the pick-up: crash in on the listening close-up; Billu blinks; the question builds over the close-up
shot(CLICK, K5A, f"{V}/K2.mp4", 0.0,
     lambda t: (1.0 + 0.32 * (1 - ease((t - CLICK) / 0.22)) + 0.05 * ease((t - CLICK - 0.3) / 1.4), 364, 560),
     speed=K2_SPEED)
shot(K5A, K5A_END, f"{V}/K5.mp4", 0.0, const(1.06, (300, 700)))
K2B_SRC = (K5A - CLICK) * K2_SPEED
shot(K5A_END, Q_OUT1, f"{V}/K2.mp4", K2B_SRC,
     lambda t: (1.05 + 0.08 * ease((t - K5A_END) / 7.0) - 0.10 * ease((t - Q_OUT0) / (Q_OUT1 - Q_OUT0)), 364, 560),
     speed=K2_SPEED)
# 4. overhead: the receiver goes down (E5's clip, cropped so only his forearm and the steel watch show)
shot(Q_OUT1, CUT("P2A"), f"{V}/OH.mp4", OH_SRC, const(1.38, (360, 640)))
# 5. A, front: pull back as he starts; punch in on "teen crore banega"
talk("P2A", CUT("P2A"), CUT("P2B"), steps([(0, 1.15), (p2(0.10), 1.0), (p2(3.00), 1.18)], FACE["T2"], glide=0.5))
# 6. B, three-quarter right: crash zoom on the eyes at "tees saal baad"
TEES = p2(5.12)
talk("P2B", CUT("P2B"), R("C") + 0.02 - LEAD,
     lambda t: ((1.0, *FACE["T3"]) if t < TEES else (1.0 + 0.42 * ease((t - TEES) / 0.1), *EYES["T3"])
                if t < p2(6.28) else (1.12, *FACE["T3"])))
# 7. C, the calendar: years fly off ("tab tak daam badhte rahenge")
CAL0, CAL1 = R("C") + 0.02 - LEAD, CUT("P2D")
shot(CAL0, CAL1, f"{V}/K3.mp4", 0.0, const(1.02), speed=min(1.0, 1.98 / (CAL1 - CAL0)))
# 8. D, three-quarter left: a slow push
talk("P2D", CUT("P2D"), R("E") + 0.02 - LEAD, ramp(CUT("P2D"), R("E"), 1.0, 1.12, FACE["T4"]))
# 9. E, the hisaab board (a full-screen graphic over the blurred room): "60 se 90 tak kharchna hai"
BOARD0, BOARD1 = R("E") + 0.02 - LEAD, CUT("P2F")
shot(BOARD0, BOARD1, f"{SK}/gfx/board_bg.png", 0.0, ramp(BOARD0, BOARD1, 1.0, 1.05, (360, 640)))
# 10. F, three-quarter right: punch in on "kareeb pandrah hazaar"
KAREEB = p2(21.90)
talk("P2F", CUT("P2F"), CUT("P2G"), steps([(0, 1.0), (KAREEB, 1.22)], FACE["T5"], glide=0.12))
# 11. G, front: the line worth sending
PANDRAH2 = p2(25.52)
talk("P2G", CUT("P2G"), R("H") + 0.02 - LEAD, steps([(0, 1.0), (PANDRAH2, 1.15)], FACE["T6"], glide=0.15))
# 12. H, whip to Billu: "badhai ho, kaafi hai" -> he turns away
H0, H1 = R("H") + 0.02 - LEAD, CUT("P2I")
shot(H0, H1, f"{V}/K5.mp4", 1.10, const(1.0))
# 13. I, three-quarter left: the rule
SEEDHA, TIHAI, SIPW = p2(31.84), p2(35.32), p2(36.12)
talk("P2I", CUT("P2I"), CUT("P2J"), steps([(0, 1.0), (SEEDHA, 1.1), (TIHAI, 1.28)], FACE["T7"], glide=0.12))
# 14. J, low angle: slow push, crash zoom on the eyes at "nahi"
NAHI = p2(40.46)
talk("P2J", CUT("P2J"), BILLU0,
     lambda t: ((1.0 + 0.1 * ease((t - CUT("P2J")) / 3.5), *FACE["T8"]) if t < NAHI
                else (1.1 + 0.5 * ease((t - NAHI) / 0.1), *EYES["T8"])))
# 15. Billu at the big bowl: dips in, laps, lifts his head, stares at what's left
shot(BILLU0, BILLU_END + 0.15, f"{V}/K4.mp4", 0.0, ramp(BILLU0, BILLU_END, 1.0, 1.06, (360, 820)))
# 16. one ring; he hangs up without answering
shot(BILLU_END + 0.15, CARD, f"{V}/OH.mp4", OH_SRC, const(1.38, (360, 640)))

WHIPS = [H0, H1, BILLU0]
SHAKES = [(HANGUP1, 0.25, 14), (TEES, 0.2, 8), (KAREEB, 0.3, 12), (TIHAI, 0.3, 14), (NAHI, 0.35, 18),
          (HANG, 0.25, 14)]

# ---------------------------------------------------------------- graphics / text
# the hook, on screen from the first frame (no pop: the first frame is the cover)
hook1 = fit("RETIRE HONE KE LIYE", "TitanOne.ttf", 70, 640, fill=WHT, stroke=7)
hook2 = fit("KITNI SIP CHAHIYE?", "TitanOne.ttf", 92, 660, fill=YEL, stroke=8)


def draw_hook(fr, t):
    al = 1.0 if t < RING - 0.1 else max(0.0, (RING + 0.05 - t) / 0.15)
    band = Image.new("RGBA", (W, 250), NAVY + (int(200 * al),))
    d = ImageDraw.Draw(band); d.rectangle([0, 0, W, 6], fill=YEL + (int(255 * al),)); d.rectangle([0, 243, W, 249], fill=YEL + (int(255 * al),))
    fr.alpha_composite(band, (0, 955))
    paste(fr, hook1, W / 2, 1030, 1.0, al); paste(fr, hook2, W / 2, 1120, 1.0, al)


EVENTS.append((0.0, RING + 0.05, draw_hook))
# the ring
for k in range(3):
    a = RING + k * 0.2
    text_event(a, a + 0.18, "TRRRING!", name="Bungee.ttf", size=92, fill=YEL, cx=470 + (k % 2) * 22, cy=990 - k * 12,
               angle=(-8 if k % 2 else 6), pop=False, fade_out=0.02)
for k in range(2):
    a = RING + 0.6 + k * 0.2
    text_event(a, a + 0.18, "TRRRING!", name="Bungee.ttf", size=92, fill=YEL, cx=480 - (k % 2) * 22, cy=960 + k * 14,
               angle=(7 if k % 2 else -6), pop=False, fade_out=0.02)
# the question, in English, word by word over the caller (C1 phrase times from Scribe on work/sk02/lines/C1.wav)
Q = [(3.64, "I'M 30,", 110, WHT, 290), (4.88, "₹10,000 SIP.", 120, WHT, 435), (7.82, "AT 60,", 84, WHT, 575),
     (8.40, "₹3 CRORE.", 150, YEL, 700), (9.60, "ENOUGH TO", 100, WHT, 860), (10.48, "RETIRE?", 170, YEL, 1010)]
for tq, txt, sz, col, y in Q:
    sp = fit(txt, "TitanOne.ttf", sz, 600, fill=col, stroke=9)
    t0 = S["C1"] + tq

    def dq(fr, t, sp=sp, t0=t0, y=y):
        al = 1 - ease((t - Q_OUT0) / (Q_OUT1 - Q_OUT0))
        sc = pop_scale(t - t0) * (1 + 0.25 * ease((t - Q_OUT0) / (Q_OUT1 - Q_OUT0)))
        paste(fr, sp, W / 2, y, sc, al)
    EVENTS.append((t0, Q_OUT1, dq))
QDIM0 = S["C1"] + 3.5
EVENTS.insert(0, (QDIM0, Q_OUT1, lambda fr, t: fr.alpha_composite(
    Image.new("RGBA", (W, H), (0, 0, 0, int(105 * min(1, (t - QDIM0) / 0.2) *
                                         (1 - ease((t - Q_OUT0) / (Q_OUT1 - Q_OUT0)))))))))

# A
caption(p2(0.10), p2(0.80), "DOST KA HISAAB")
caption(p2(0.84), p2(1.48), "THEEK HAI.")
tag(p2(1.50), CUT("P2B"), "12% RETURN MAAN KE")
text_event(p2(3.00), CUT("P2B"), "₹3 CRORE", name="TitanOne.ttf", size=140, fill=YEL, cy=1010, stroke=10, maxw=600)
tick = tick_sprite(70)
CR_W = fit("₹3 CRORE", "TitanOne.ttf", 140, 600, fill=YEL, stroke=10).width
EVENTS.append((p2(3.50), CUT("P2B"), lambda fr, t: paste(fr, tick, min(W - 46, W / 2 + CR_W / 2 + 26), 985, pop_scale(t - p2(3.50)))))
# B
caption(p2(4.38), p2(5.10), "PAR WOH…")
text_event(TEES, p2(6.28), "30 SAAL BAAD KA", name="TitanOne.ttf", size=96, fill=WHT, cy=1010, stroke=9)
text_event(p2(6.28), CAL0, "₹3 CRORE", name="TitanOne.ttf", size=150, fill=YEL, cy=1010, stroke=10)
# C: the calendar; the year runs from 2026 to 2056 while the pages fly
caption(p2(7.56), p2(8.00), "TAB TAK…")
caption(p2(8.06), CAL1, "DAAM BADHTE RAHENGE.")
year_f = font("Bungee.ttf", 120)


def draw_year(fr, t):
    u = ease((t - CAL0 - 0.15) / (CAL1 - CAL0 - 0.5))
    y = 2026 + int(round(30 * u))
    sp = sprite(str(y), year_f, YEL if y == 2056 else WHT, stroke=8, shadow=6)
    paste(fr, sp, W / 2, 190, 1.0)


EVENTS.append((CAL0, CAL1, draw_year))
# D
tag(p2(10.30), R("E") - 0.08, "6% MEHANGAI MAAN KE")
caption(p2(11.58), p2(12.62), "AAJ KE HISAAB SE")
three_small = sprite("₹3 CRORE (2056)", font("TitanOne.ttf", 60), WHT, stroke=6)
lakh = fit("₹54 LAKH", "TitanOne.ttf", 140, 580, fill=YEL, stroke=10)
lag = sprite("LAGBHAG AADHA CRORE", font("Bungee.ttf", 38), WHT, stroke=4, shadow=4)


def draw_d(fr, t):
    paste(fr, three_small, W / 2, 900, pop_scale(t - p2(11.58)))
    d = ImageDraw.Draw(fr)
    if t >= p2(12.70):   # an arrow down, then the slam
        k = ease((t - p2(12.70)) / 0.15)
        d.line([(360, 935), (360, 935 + 40 * k)], fill=YEL, width=10)
        if k >= 1:
            d.polygon([(340, 972), (380, 972), (360, 996)], fill=YEL)
        paste(fr, lakh, W / 2, 1075, pop_scale(t - p2(12.78), 0.2))
        paste(fr, lag, W / 2, 1165, pop_scale(t - p2(13.30)))


EVENTS.append((p2(11.58), R("E") - 0.08, draw_d))


# E: the board. Background: the cold-open keyframe, blurred and darkened (made below in make_board_bg)
def draw_board(fr, t):
    d = ImageDraw.Draw(fr)
    x0, y0, x1, y1 = 50, 250, 670, 1030
    k = ease((t - BOARD0) / 0.18)
    if k <= 0:
        return
    yy = int(y0 + (1 - k) * 60)
    d.rounded_rectangle([x0, yy, x1, y1], 22, fill=NAVY + (240,), outline=(235, 235, 235, 255), width=8)
    d.rounded_rectangle([x0 + 16, yy + 16, x1 - 16, y1 - 16], 14, outline=YEL + (255,), width=3)
    paste(fr, BRD["title"], W / 2, yy + 85, 1.0)
    paste(fr, BRD["lakh"], W / 2, yy + 200, pop_scale(t - BOARD0 - 0.1, 0.2))
    if t >= p2(15.94):    # "ek baar mein nahi": a red line through EK BAAR MEIN
        paste(fr, BRD["ek"], W / 2, yy + 320, pop_scale(t - p2(15.94)))
        if t >= p2(16.54):
            kk = ease((t - p2(16.54)) / 0.12); w = BRD["ek"].width * 0.55
            d.line([(W / 2 - w, yy + 340), (W / 2 - w + 2 * w * kk, yy + 300)], fill=RED, width=14)
    if t >= p2(17.14):    # the 60 -> 90 bar draws, 30 ticks
        bx0, bx1, by = 110, 610, yy + 470
        kk = ease((t - p2(17.14)) / (p2(18.30) - p2(17.14)))
        d.line([(bx0, by), (bx0 + (bx1 - bx0) * kk, by)], fill=WHT, width=10)
        for i in range(31):
            x = bx0 + (bx1 - bx0) * i / 30
            if x <= bx0 + (bx1 - bx0) * kk:
                h = 26 if i % 10 == 0 else 14
                d.line([(x, by - h), (x, by + h)], fill=YEL if i % 10 == 0 else WHT, width=4)
        paste(fr, BRD["60"], bx0, by + 70, pop_scale(t - p2(17.14)))
        if t >= p2(17.84):
            paste(fr, BRD["90"], bx1, by + 70, pop_scale(t - p2(17.84)))
    if t >= p2(18.48):
        paste(fr, BRD["saal"], W / 2, yy + 650, pop_scale(t - p2(18.48), 0.2))


BRD = {"title": sprite("HISAAB", font("Bungee.ttf", 70), WHT, stroke=5, shadow=5),
       "lakh": fit("₹54 LAKH", "TitanOne.ttf", 120, 500, fill=YEL, stroke=9),
       "ek": sprite("EK BAAR MEIN", font("Bungee.ttf", 64), WHT, stroke=5, shadow=5),
       "60": sprite("60", font("TitanOne.ttf", 84), WHT, stroke=7), "90": sprite("90", font("TitanOne.ttf", 84), WHT, stroke=7),
       "saal": fit("30 SAAL KHARCHA", "TitanOne.ttf", 76, 520, fill=YEL, stroke=8)}
EVENTS.append((BOARD0, BOARD1, draw_board))
caption(p2(14.70), p2(15.72), "AUR YEH AADHA CRORE…", cy=1120)
# F
caption(p2(19.44), p2(20.62), "TOH MAHINA MILEGA…")
caption(p2(20.68), KAREEB, "AAJ KE HISAAB SE,")
text_event(KAREEB, CUT("P2G"), "₹15,000", name="TitanOne.ttf", size=170, fill=YEL, cy=980, stroke=11)
text_event(KAREEB + 0.25, CUT("P2G"), "/ MAHINA", name="Bungee.ttf", size=60, fill=WHT, cy=1100, stroke=5)
# G: the line worth sending
text_event(p2(23.88), H0, "₹10,000 SIP", name="TitanOne.ttf", size=104, fill=WHT, cy=880, stroke=9)
text_event(p2(25.30), H0, "=", name="TitanOne.ttf", size=90, fill=WHT, cy=975, stroke=8)
text_event(PANDRAH2, H0, "₹15,000 KHARCHA", name="TitanOne.ttf", size=104, fill=YEL, cy=1075, stroke=9)
# H: Billu
caption(p2(27.24), p2(29.02), "₹15,000 MEIN GHAR CHALTA HAI?")
caption(p2(29.02), p2(29.98), "TOH BADHAI HO,")
caption(p2(30.00), H1, "KAAFI HAI.", fill=GRN)
EVENTS.append((p2(30.30), H1, lambda fr, t: paste(fr, tick, 545, 1015, pop_scale(t - p2(30.30)))))
# I: the rule
caption(p2(31.00), p2(31.62), "NAHI CHALTA?")
caption(p2(31.84), p2(33.22), "HISAAB SEEDHA HAI:")
rule1 = fit("MAHINE KA KHARCHA", "Bungee.ttf", 54, 590, fill=WHT, stroke=5, shadow=5)
rule2 = sprite("× 2/3", font("TitanOne.ttf", 150), YEL, stroke=10)
rule3 = sprite("= SIP", font("TitanOne.ttf", 130), WHT, stroke=9)


def draw_rule(fr, t):
    paste(fr, rule1, W / 2, 880, pop_scale(t - p2(33.26)))
    if t >= TIHAI:
        paste(fr, rule2, W / 2, 1005, pop_scale(t - TIHAI, 0.2))
    if t >= SIPW:
        paste(fr, rule3, W / 2, 1135, pop_scale(t - SIPW, 0.2))


EVENTS.append((p2(33.26), CUT("P2J"), draw_rule))
# J
caption(p2(36.96), p2(37.72), "TUMRA DOST")
caption(p2(37.74), p2(38.80), "₹3 CRORE TAK GINA,")
caption(p2(39.18), NAHI, "USKE AAGE…")
text_event(NAHI, BILLU0, "NAHI.", name="TitanOne.ttf", size=180, fill=RED, cy=1060, stroke=11)
# the bowl
bowl_lbl = sprite("₹3 CRORE", font("TitanOne.ttf", 84), YEL, stroke=8)
EVENTS.append((BILLU0 + 0.6, BILLU_END + 0.15, lambda fr, t: paste(fr, bowl_lbl, 360, 1150, pop_scale(t - BILLU0 - 0.6))))
# the ring at the end
for k in range(2):
    a = BILLU_END - 0.55 + k * 0.5
    text_event(a, a + 0.25, "TRRRING!", name="Bungee.ttf", size=84, fill=YEL, cx=470, cy=320, angle=(-6 if k else 6),
               pop=False, fade_out=0.02)
# the DOORDHAN bug, top right, until the card
bug = sprite("DOORDHAN", font("Bungee.ttf", 30), (255, 255, 255, 215), stroke=3, shadow=3, pad=6)
EVENTS.append((0, CARD, lambda fr, t: paste(fr, bug, W - 20 - bug.width / 2, 58, 1, 0.85)))


def make_board_bg():
    os.makedirs(f"{SK}/gfx", exist_ok=True)
    im = Image.open(f"{SK}/kf/cold3.png").convert("RGB").resize((W, H), Image.LANCZOS)
    im = im.filter(ImageFilter.GaussianBlur(14))
    im = Image.blend(im, Image.new("RGB", (W, H), (8, 10, 20)), 0.45)
    im.save(f"{SK}/gfx/board_bg.png")


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


PLACED = {}   # line -> (reel start, reel end, source) of the voice as placed in the mix
VOICE_LINES = [("P1", f"{SK}/lines/P1.wav", S["P1"])] + [
    (f"P2{k}", f"{SK}/seg/{k}.wav", R(k)) for k in "ABCDEFGHIJ"]


def mix(out_wav):
    n = int(TOTAL * SR) + SR
    bus = np.zeros(n, np.float32)    # everything
    vbus = np.zeros(n, np.float32)   # Pandey's voice: gets the room treatment
    dbus = np.zeros(n, np.float32)   # the dialogue as placed (qc_gate's line checks)

    def put(b, x, t, g=1.0):
        i = int(round(t * SR)); j = min(n, i + len(x)); b[i:j] += g * x[: j - i]

    for lid, f, t0 in VOICE_LINES:
        x = load(f)
        end = REP.get(lid, {}).get("voice_end_s")
        if end is not None:
            fd = int(REP.get(lid, {}).get("fade_s", 0.05) * SR)
            x = x[: int(end * SR)].copy(); x[-fd:] *= np.linspace(1, 0, fd)
        put(vbus, x, t0); put(dbus, x, t0); PLACED[lid] = (t0, t0 + len(x) / SR, f)
    c1 = load(f"{SK}/lines/C1.wav")      # already on the landline chain; no room on it
    end = REP.get("C1", {}).get("voice_end_s")
    if end is not None:
        fd = int(REP.get("C1", {}).get("fade_s", 0.05) * SR); c1 = c1[: int(end * SR)].copy(); c1[-fd:] *= np.linspace(1, 0, fd)
    put(bus, c1, S["C1"]); put(dbus, c1, S["C1"]); PLACED["C1"] = (S["C1"], S["C1"] + len(c1) / SR, f"{SK}/lines/C1.wav")
    bus += voice_room.treat(vbus)
    ring_x = VC.room(VC.peak(VC.ring(), -9)); click_x = VC.room(VC.peak(VC.click(), -12)); clack_x = VC.room(VC.peak(VC.clack(), -7))
    put(bus, ring_x, RING); put(bus, click_x, CLICK); put(bus, clack_x, HANGUP1 - 0.02)
    put(bus, ring_x, BILLU_END - 0.6, 0.85); put(bus, clack_x, HANG - 0.02)
    fx = {k: load(f"{SFX}/sfx_{k}.wav") for k in ("whoosh", "pop", "ding", "thud", "scratch", "riser", "stamp")}
    put(bus, fx["whoosh"], CLICK - 0.12, 0.5)                                   # crash zoom on the pick-up
    for tq, *_ in Q:
        put(bus, fx["pop"], S["C1"] + tq, 0.45)
    put(bus, fx["thud"], S["C1"] + 8.40, 0.5)                                    # ₹3 CRORE AT 60
    put(bus, fx["whoosh"], Q_OUT0, 0.3)
    put(bus, fx["pop"], p2(1.50), 0.3); put(bus, fx["ding"], p2(3.00), 0.3)      # 12% tag, ₹3 crore
    put(bus, fx["whoosh"], TEES - 0.15, 0.4); put(bus, fx["thud"], p2(6.28), 0.4)
    put(bus, fx["whoosh"], CAL0 - 0.1, 0.35)
    put(bus, fx["pop"], p2(10.30), 0.3); put(bus, fx["ding"], p2(12.78), 0.35)   # 6% tag, ₹54 lakh
    put(bus, fx["whoosh"], BOARD0 - 0.1, 0.35); put(bus, fx["pop"], BOARD0 + 0.1, 0.35)
    put(bus, fx["scratch"], p2(16.40), 0.35); put(bus, fx["pop"], p2(17.14), 0.3); put(bus, fx["pop"], p2(17.84), 0.3)
    put(bus, fx["ding"], p2(18.48), 0.35)
    put(bus, fx["thud"], KAREEB, 0.6)
    put(bus, fx["pop"], p2(23.88), 0.35); put(bus, fx["thud"], PANDRAH2, 0.5)
    for tw in WHIPS:
        put(bus, fx["whoosh"], tw - 0.2, 0.55)
    put(bus, fx["stamp"], p2(30.30), 0.5)
    put(bus, fx["riser"], TIHAI - 1.4, 0.3); put(bus, fx["thud"], TIHAI, 0.6); put(bus, fx["ding"], SIPW, 0.35)
    put(bus, fx["scratch"], NAHI - 0.28, 0.5); put(bus, fx["thud"], NAHI, 0.7)
    put(bus, fx["pop"], BILLU0 + 0.6, 0.3)
    tmp = os.path.join(SK, "tmp"); os.makedirs(tmp, exist_ok=True)
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
    """work/sk02/qc_manifest.json for pipeline/qc_gate.py: each voice line (P2 by segment) and its talking shots"""
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
    man = {"slug": "sk02", "format": "sahayata_kendra", "final": edit["out"],
           "script": "registry/scripts/sk02.json",
           "characters": {"pandey": "assets/characters/pandey_sheet_v2.jpg"},
           "dialogue_stem": rel(os.path.join(SK, "tmp", "dialogue.wav")),
           "prefinish": rel(os.path.join(SK, "edit_raw.mkv")),
           "length": {"min": 40, "max": 70, "expected": round(TOTAL, 2)},
           "loudness": {"target": edit.get("target_lufs", -14)},
           "repairs_file": rel(REPAIRS),
           "rebuild": f"{env} {py} work/sk02/build.py && {py} pipeline/assemble.py {rel(EDIT_JSON)}",
           "lines": lines}
    path = os.path.join(os.path.dirname(EDIT_JSON), "qc_manifest.json")
    json.dump(man, open(path, "w"), indent=1, ensure_ascii=False)
    return path


if __name__ == "__main__":
    tmp = os.path.join(SK, "tmp"); os.makedirs(tmp, exist_ok=True)
    make_board_bg()
    vid, wav = os.path.join(tmp, "video.mp4"), os.path.join(tmp, "mix.wav")
    talking = sum(sh["t1"] - sh["t0"] for sh in SHOTS if sh["line"])
    print(f"timeline: ring {RING:.2f}  C1 {S['C1']:.2f}  P2 {S['P2']:.2f}  Billu {BILLU0:.2f}  card {CARD:.2f}  "
          f"total {TOTAL:.2f}  talking to camera {talking:.1f} s = {100 * talking / TOTAL:.0f}%")
    for sh in SHOTS:
        end_src = sh["src_in"] + (sh["t1"] - sh["t0"]) * sh["speed"]
        d = dur(sh["path"]) if sh["path"].endswith(".mp4") else 99
        flag = "  <-- runs past the clip" if end_src > d - 0.02 else ""
        print(f"  {sh['t0']:6.2f}-{sh['t1']:6.2f}  {os.path.basename(sh['path']):14s} src {sh['src_in']:5.2f}-{end_src:5.2f} of {d:5.2f}{flag}")
    mix(wav); print("mixed", wav)
    print("qc manifest", write_qc_manifest())
    render(vid); print("rendered", vid)
    out = os.path.join(SK, "edit_raw.mkv")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", "-shortest", out], check=True)
    print("wrote", out, f"{dur(out):.2f}s")
