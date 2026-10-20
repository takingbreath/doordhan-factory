#!/usr/bin/env python3
"""TEMPLATE (Sahayata Kendra frame-composed edit), from SK03 (E7) "Noida mein flat lene se pehle ka dekhein?", approved
2026-10-04. Copy it with assets/edits/sk03_gfx.py into work/<slug>/ as build.py and gfx.py (the /produce-video skill
does this), then change the episode-specific parts: SEG/FIRST/RING/C1/K_LAST timings, TALK, FACE, the SHOTS list, the
text EVENTS and the sound effects. Paths come from where the copy sits, so nothing else needs editing.
Composes every frame in Python (zooms, whips, shakes, kinetic text, the checklist graphics) and mixes the sound with
numpy, then hands one raw 720x1280 file to assemble.py for the kendra look, VHS motion and ambience.
  pipeline/qcpy work/<slug>/build.py  ->  work/<slug>/edit_raw.mkv + work/<slug>/qc_manifest.json
  PLAN_ONLY=1 ... prints the timeline, talking share and each shot's source span without rendering
The voice is the approved draft cut (work/<slug>/voice/<slug>_voice_cut.wav, Akhilesh 2026-10-04, with his four fixes),
cut into segments at its pauses (work/<slug>/seg, segments.json in cut seconds). Reel time = cut time until Billu's
button; each talking clip (Wan 2.7, 0.5 s lead in each track) maps clip time c = 0.5 + (reel - segment start)."""
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


# ---------------------------------------------------------------- audio timeline (reel seconds = cut seconds)
SEG = json.load(open(f"{SK}/seg/segments.json"))      # every Pandey segment: cut_start / cut_end in the draft cut
RING, CLICK = 2.43, 3.63                               # the draft cut's ring and pick-up (work/<slug>/voice/cut.json)
C1_IN, C1_OUT = 3.90, 13.40                            # the caller, sliced from the cut (landline chain already on)
Q_OUT0, Q_OUT1 = 13.22, 13.58                          # the question clears before he hangs up
HANGUP1 = 13.76                                        # the cut's cradle clack
P1_AT = 0.12                                           # the hook voice starts 0.12 s into the reel (a lead for the gate)
FIRST = {"P1": P1_AT + 0.14, "A": 14.68, "B": 19.18, "C": 25.46, "D": 29.06, "E": 30.48, "F": 34.60, "G": 39.34, "H": 41.60,
         "I": 46.42, "J": 49.92, "K": 53.30}           # first word of each segment (Scribe on the cut)
K_LAST = 56.54                                         # "dikhega" ends
BILLU0 = K_LAST + 0.28                                 # cut about 0.25 s after the last word
BE_A, BE_B = 1.60, 2.70                                # Billu's paw flip in BE.mp4 (clip s): played at x2.2
BE_FAST = 2.2
BE_END_SRC = 5.00
BILLU_END = BILLU0 + BE_A + (BE_B - BE_A) / BE_FAST + (BE_END_SRC - BE_B)
RING2 = BILLU_END - 1.50                               # the phone rings over the sleeping Billu; nobody answers
CARD = BILLU_END + 0.03
CARD_LEN = 4.8
TOTAL = CARD + CARD_LEN
LEAD = 0.12                                            # talking shots cut in 0.12 s before the first word
TRACK_LEAD = 0.5                                       # silence before the line in every Wan track


def S0(seg):
    return SEG[seg]["cut_start"]


# Talking clips: line id -> (clip, reel time its track's line starts, segment)
TALK = {"P1": ("S1", P1_AT, "P1"), "P2A": ("T2", S0("A"), "A"), "P2B": ("T3", S0("B"), "B"),
        "P2C": ("T4", S0("C"), "C"), "P2E": ("T5", S0("E"), "E"), "P2H": ("T6", S0("H"), "H"),
        "P2K": ("T7", S0("K"), "K")}
JUDGE_SHIFT = {}   # shot_spec.py judge: every talking clip ACCEPT with no shift


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


# face centres (720x1280), measured on each clip with assets/edits/sk02_mouthbox.py (copy it as work/<slug>/mouthbox.py)
FACE = {"S1": (376, 495), "T2": (368, 599), "T3": (354, 529), "T4": (368, 547), "T5": (362, 563), "T6": (354, 545),
        "T7": (370, 593)}
EYES = {"T3": (337, 464), "T5": (364, 516)}
SHOTS = []


def shot(t0, t1, path, src_in, zoom, speed=1.0, line=None):
    SHOTS.append(dict(t0=t0, t1=t1, path=path, src_in=src_in, zoom=zoom, speed=speed, line=line))


def talk(line, t0, t1, zoom):
    path, src = TK(line, t0)
    shot(t0, t1, path, src, zoom, line=line)


R_IN = RING + 0.12                                    # cut to the ring shot just after the first burst starts
Y_IN, Y_OUT = 9.40, 11.50                             # Billu's yawn over "pool hai, clubhouse hai, sab hai"
L_SPEED = 6.95 / ((Y_IN - CLICK) + (Q_OUT1 - Y_OUT))  # the 7 s listening clip covers the call around the yawn
OH_IN = Q_OUT1 + 0.04
OH_SRC = float(os.environ.get("OH_SRC", "0.10"))      # OH.mp4: the receiver seats at clip 0.24 s = reel 13.76, the clack
BA_IN = 28.70                                         # Billu's ears on "Ab asli khel"
DIAG0, DIAG1 = SEG["F"]["cut_start"] - 0.18, SEG["G"]["cut_start"] - 0.01
INS0, INS1 = DIAG1, CUT("P2H")
BOARD0, BOARD1 = SEG["I"]["cut_start"] - 0.01, CUT("P2K")

# 1. cold open: the hook to the lens while Billu walks in along the desk; a slow creep
talk("P1", 0.0, R_IN, ramp(0.0, R_IN, 1.0, 1.05, (376, 640)))
# 2. the ring: Billu stops and turns his head to the phone, Pandey looks down at it (chained from S1's last frame)
shot(R_IN, CLICK, f"{V}/R.mp4", float(os.environ.get("R_SRC", "0.0")), const(1.0), speed=float(os.environ.get("R_SPEED", "1.2")))
# 3. the pick-up: crash in on the listening close-up; the question builds
shot(CLICK, Y_IN, f"{V}/L.mp4", 0.0,
     lambda t: (1.0 + 0.32 * (1 - ease((t - CLICK) / 0.22)) + 0.05 * ease((t - CLICK - 0.3) / 1.4), 370, 600),
     speed=L_SPEED)
# 4. whip to Billu: a huge yawn at the pool and the clubhouse
shot(Y_IN, Y_OUT, f"{V}/Y.mp4", float(os.environ.get("Y_SRC", "0.2")), const(1.04, (360, 700)),
     speed=float(os.environ.get("Y_SPEED", "1.2")))
L2_SRC = (Y_IN - CLICK) * L_SPEED
shot(Y_OUT, OH_IN, f"{V}/L.mp4", L2_SRC,
     lambda t: (1.05 + 0.06 * ease((t - Y_OUT) / 2.0) - 0.10 * ease((t - Q_OUT0) / (Q_OUT1 - Q_OUT0)), 370, 600),
     speed=L_SPEED)
# 5. overhead: the receiver goes down on a clean frame
shot(OH_IN, CUT("P2A"), f"{V}/OH.mp4", OH_SRC, const(1.08, (360, 640)))
# 6. A, front: pull back as he starts; punch in on the first check
talk("P2A", CUT("P2A"), CUT("P2B"), steps([(0, 1.12), (FIRST["A"] + 0.05, 1.0), (16.96, 1.16)], FACE["T2"], glide=0.4))
# 7. B, three-quarter right: one punch-in per question
talk("P2B", CUT("P2B"), CUT("P2C"), steps([(0, 1.0), (20.82, 1.14), (22.94, 1.28)], FACE["T3"], glide=0.12))
# 8. C, three-quarter left: a slow push; the stamp on "likhwa ke lo"
talk("P2C", CUT("P2C"), BA_IN, ramp(CUT("P2C"), BA_IN, 1.0, 1.12, FACE["T4"]))
# 9. whip to Billu: his ears prick up at "Ab asli khel"
shot(BA_IN, CUT("P2E"), f"{V}/BA.mp4", float(os.environ.get("BA_SRC", "0.15")), const(1.04, (360, 700)))
# 10. E, low angle under the damp ceiling: "zameen Noida Authority ki hai, builder ke paas lease pe"
talk("P2E", CUT("P2E"), DIAG0, ramp(CUT("P2E"), DIAG0, 1.0, 1.08, FACE["T5"]))
# 11. F, the diagram (full-screen graphic over the blurred room): the registry trap
shot(DIAG0, DIAG1, f"{SK}/gfx/diag_bg.png", 0.0, ramp(DIAG0, DIAG1, 1.0, 1.05, (360, 640)))
# 12. G, the insert: a key on an empty REGISTRY file ("chaabi mil jaati hai, kaagaz nahi")
shot(INS0, INS1, f"{SK}/kf/insert_key.png", 0.0, ramp(INS0, INS1, 1.0, 1.14, (380, 700)))
# 13. H, three-quarter right: where to check; punch in on "OC"
talk("P2H", CUT("P2H"), BOARD0, steps([(0, 1.0), (44.34, 1.14)], FACE["T6"], glide=0.12))
# 14. I + J, the full checklist board; item 8 arrives with "pandrah saal purani society"
shot(BOARD0, BOARD1, f"{SK}/gfx/board_bg.png", 0.0, ramp(BOARD0, BOARD1, 1.0, 1.06, (360, 640)))
# 15. K, front: start tight on the face and pull back to the cracked wall and the POSSESSION 2011 poster


def pullback(t):
    u = ease((t - CUT("P2K")) / 2.9)
    z = 1.55 - 0.55 * u
    cx = FACE["T7"][0] + (360 - FACE["T7"][0]) * u; cy = FACE["T7"][1] + (640 - FACE["T7"][1]) * u
    return (z, cx, cy)


talk("P2K", CUT("P2K"), BILLU0, pullback)
# 16. Billu's button: paws the REGISTRY file open, it's empty, he sleeps on it; the phone rings, he doesn't wake
B1 = BILLU0 + BE_A
B2 = B1 + (BE_B - BE_A) / BE_FAST
shot(BILLU0, B1, f"{V}/BE.mp4", 0.0, const(1.0))
shot(B1, B2, f"{V}/BE.mp4", BE_A, const(1.0), speed=BE_FAST)
shot(B2, CARD, f"{V}/BE.mp4", BE_B, ramp(B2, CARD, 1.0, 1.06, (360, 760)))

WHIPS = [Y_IN, Y_OUT, BA_IN, CUT("P2E")]
SHAKES = [(HANGUP1, 0.25, 14), (27.68, 0.25, 10), (38.20, 0.35, 16), (40.52, 0.25, 10)]

# ---------------------------------------------------------------- graphics / text
# the hook, on screen from the first frame (no pop: the first frame is the cover)
hook1 = fit("NOIDA MEIN FLAT", "TitanOne.ttf", 68, 620, fill=WHT, stroke=7)
hook1b = fit("LENE SE PEHLE", "TitanOne.ttf", 68, 620, fill=WHT, stroke=7)
hook2 = fit("KYA DEKHEIN?", "TitanOne.ttf", 104, 640, fill=YEL, stroke=9)
HOOK_Y = 572   # the band sits on his chest: Billu walks in along the desk below it and must stay visible


def draw_hook(fr, t):
    al = 1.0 if t < RING - 0.1 else max(0.0, (RING + 0.05 - t) / 0.15)
    band = Image.new("RGBA", (W, 252), NAVY + (int(200 * al),))
    d = ImageDraw.Draw(band); d.rectangle([0, 0, W, 6], fill=YEL + (int(255 * al),)); d.rectangle([0, 245, W, 251], fill=YEL + (int(255 * al),))
    fr.alpha_composite(band, (0, HOOK_Y))
    paste(fr, hook1, W / 2, HOOK_Y + 52, 1.0, al); paste(fr, hook1b, W / 2, HOOK_Y + 118, 1.0, al)
    paste(fr, hook2, W / 2, HOOK_Y + 196, 1.0, al)


EVENTS.append((0.0, RING + 0.05, draw_hook))
# the ring (one ring: two bursts, 0.4 s on, 0.2 off, 0.4 on)
for burst in (RING, RING + 0.6):
    for k in range(2):
        a = burst + k * 0.2
        text_event(a, a + 0.18, "TRRRING!", name="Bungee.ttf", size=92, fill=YEL, cx=470 + (k % 2) * 22,
                   cy=880 - k * 12, angle=(-8 if k % 2 else 6), pop=False, fade_out=0.02)
# the question, in English, word by word over the caller (C1 word times from Scribe on the cut)
Q = [(7.40, "FOUND A FLAT", 96, WHT, 290), (8.04, "IN NOIDA.", 128, YEL, 410)]
for tq, txt, sz, col, y in Q:
    sp = fit(txt, "TitanOne.ttf", sz, 600, fill=col, stroke=9)

    def dq(fr, t, sp=sp, t0=tq, y=y):
        al = 1 - ease((t - Q_OUT0) / (Q_OUT1 - Q_OUT0))
        sc = pop_scale(t - t0) * (1 + 0.25 * ease((t - Q_OUT0) / (Q_OUT1 - Q_OUT0)))
        paste(fr, sp, W / 2, y, sc, al)
    EVENTS.append((tq, Q_OUT1, dq))
# the amenities, ticked, over Billu's yawn
# (below Billu's face during the yawn, then they glide up and shrink to make room for the question)
AM = [(9.52, "POOL", 840, 548), (10.14, "CLUBHOUSE", 945, 632), (10.98, "EVERYTHING", 1050, 716)]
tick_s = mark_sprite("tick", 64)
for ta, txt, ylo, yhi in AM:
    sp = sprite(txt, font("TitanOne.ttf", 84), WHT, stroke=8)

    def da(fr, t, sp=sp, t0=ta, ylo=ylo, yhi=yhi):
        al = 1 - ease((t - Q_OUT0) / (Q_OUT1 - Q_OUT0))
        u = ease((t - Y_OUT) / 0.25)
        y, sc = ylo + (yhi - ylo) * u, 1.0 - 0.22 * u
        paste(fr, sp, W / 2 - 30 * sc, y, pop_scale(t - t0) * sc, al)
        paste(fr, tick_s, W / 2 - 30 * sc + (sp.width / 2 + 40) * sc, y - 6, pop_scale(t - t0 - 0.12) * sc, al)
    EVENTS.append((ta, Q_OUT1, da))
Q2 = [(11.94, "WHAT DO I CHECK", 84, WHT, 950), (12.68, "BEFORE BOOKING?", 104, YEL, 1075)]
for tq, txt, sz, col, y in Q2:
    sp = fit(txt, "TitanOne.ttf", sz, 610, fill=col, stroke=9)

    def dq2(fr, t, sp=sp, t0=tq, y=y):
        al = 1 - ease((t - Q_OUT0) / (Q_OUT1 - Q_OUT0))
        sc = pop_scale(t - t0) * (1 + 0.25 * ease((t - Q_OUT0) / (Q_OUT1 - Q_OUT0)))
        paste(fr, sp, W / 2, y, sc, al)
    EVENTS.append((tq, Q_OUT1, dq2))
QDIM0 = 7.25
EVENTS.insert(0, (QDIM0, Q_OUT1, lambda fr, t: fr.alpha_composite(
    Image.new("RGBA", (W, H), (0, 0, 0, int(100 * min(1, (t - QDIM0) / 0.2) *
                                         (1 - ease((t - Q_OUT0) / (Q_OUT1 - Q_OUT0)))))))))

# A
text_event(FIRST["A"], 15.62, "POOL CHHODO.", name="TitanOne.ttf", size=104, fill=RED, cy=1030, stroke=9)
caption(16.16, 16.94, "POOCHHO…")
item_card(16.96, CUT("P2B"), 1, "OCCUPANCY LOAD", "society full hone pe?")
# B: one card per question
item_card(19.18, 20.80, 2, "LIFT", "ek lift, kitne flat?")
item_card(20.86, 22.92, 3, "BIJLI BACKUP", "power cut mein lift?")
item_card(22.98, CUT("P2C"), 4, "PAANI", "borewell sookha toh?")
# C: maintenance, then the stamp
item_card(25.46, BA_IN, 5, "MAINTENANCE", "kya included, kya nahi?")
stamp = sprite("LIKHWA KE LO!", font("Bungee.ttf", 70), RED, stroke=5, sfill=WHT, shadow=6)


def draw_stamp(fr, t):
    k = min(1.0, (t - 27.68) / 0.12)
    paste(fr, stamp, W / 2, 860, 1.6 - 0.6 * k, min(1.0, k * 1.5), angle=8)


EVENTS.append((27.68, BA_IN, draw_stamp))
# D: Billu
text_event(FIRST["D"], CUT("P2E"), "AB ASLI KHEL.", name="TitanOne.ttf", size=110, fill=YEL, cy=1060, stroke=10)
# E
caption(30.48, 32.60, "ZAMEEN: NOIDA AUTHORITY KI")
caption(32.68, DIAG0, "BUILDER: SIRF LEASE PE")
# F: the diagram


def draw_diag(fr, t):
    pops = {0: min(1, (t - DIAG0) / 0.15), 1: min(1, (t - DIAG0 - 0.15) / 0.15),
            2: min(1, (t - 35.58) / 0.15), 3: min(1, (t - 38.20) / 0.14)}
    step = 4 if t >= 38.20 else 3 if t >= 35.58 else 2
    gfx.draw_diagram(fr, step, pops)


EVENTS.append((DIAG0, DIAG1, draw_diag))
# G: the insert
chaabi = sprite("CHAABI", font("TitanOne.ttf", 96), WHT, stroke=8)
kaagaz = sprite("KAAGAZ", font("TitanOne.ttf", 96), WHT, stroke=8)
cross_s = mark_sprite("cross", 70)


def draw_insert(fr, t):
    paste(fr, chaabi, W / 2 - 50, 1010, pop_scale(t - FIRST["G"]))
    paste(fr, tick_s, W / 2 - 50 + chaabi.width / 2 + 46, 1000, pop_scale(t - FIRST["G"] - 0.15))
    if t >= 40.52:
        paste(fr, kaagaz, W / 2 - 50, 1130, pop_scale(t - 40.52))
        paste(fr, cross_s, W / 2 - 50 + kaagaz.width / 2 + 46, 1120, pop_scale(t - 40.62))


EVENTS.append((INS0 + 0.02, INS1, draw_insert))
# H: where to check
item_card(42.22, 44.32, 6, "AUTHORITY DUES", "noidaauthorityonline.in")
item_card(44.36, BOARD0, 7, "OC + RERA", "up-rera.in")
# I + J: the board


def draw_board(fr, t):
    pops = {i: min(1.0, (t - BOARD0 - 0.15 - 0.07 * i) / 0.12) for i in range(7)}
    pops[7] = min(1.0, (t - 50.60) / 0.15)
    shown = 8 if t >= 50.60 else 7
    ticked = 8 if t >= 52.42 else 7
    gfx.draw_checklist(fr, shown, ticked, pops, footer=min(1.0, (t - 47.48) / 0.15) if t >= 47.48 else 0)
    if t >= 47.48:   # bouncing down-arrows on "comment"
        d = ImageDraw.Draw(fr); b = 8 * abs(np.sin((t - 47.48) * 7))
        for x in (78, W - 78):
            d.polygon([(x - 22, 1132 + b), (x + 22, 1132 + b), (x, 1166 + b)], fill=YEL, outline=INK)


EVENTS.append((BOARD0, BOARD1, draw_board))
# K: the payoff, then a red ring round POSSESSION 2011 on the poster (2011 + 15 = 2026)
caption(53.30, 55.30, "TUMRA FLAT 15 SAAL BAAD…")
text_event(55.38, BILLU0, "WAISA HI DIKHEGA.", name="TitanOne.ttf", size=92, fill=YEL, cy=1050, stroke=9, maxw=620)
POSTER = (606, 633)   # "POSSESSION 2011" on front_clean at zoom 1.0 (720x1280)
tag15 = sprite("15 SAAL PEHLE", font("Bungee.ttf", 34), WHT, stroke=4, shadow=4, pad=8)


def draw_ring(fr, t):
    k = ease((t - 55.90) / 0.35)
    z, cx, cy = pullback(t)
    x0 = min(max(0, cx - W / z / 2), W - W / z); y0 = min(max(0, cy - H / z / 2), H - H / z)
    px, py = (POSTER[0] - x0) * z, (POSTER[1] - y0) * z
    d = ImageDraw.Draw(fr)
    a0 = -100; a1 = a0 + 370 * k
    d.arc([px - 118, py - 40, px + 104, py + 40], a0, a1, fill=RED, width=9)
    if k >= 1:
        paste(fr, tag15, min(px - 10, W - tag15.width / 2 - 12), py - 78, pop_scale(t - 56.25))


EVENTS.append((55.90, BILLU0, draw_ring))
# the ring over the sleeping Billu
for burst in (RING2, RING2 + 0.6):
    for k in range(2):
        a = burst + k * 0.2
        text_event(a, a + 0.18, "TRRRING!", name="Bungee.ttf", size=84, fill=YEL, cx=470, cy=300 - k * 10,
                   angle=(-6 if k else 6), pop=False, fade_out=0.02)
# the DOORDHAN bug, top right, until the card
bug = sprite("DOORDHAN", font("Bungee.ttf", 30), (255, 255, 255, 215), stroke=3, shadow=3, pad=6)
EVENTS.append((0, CARD, lambda fr, t: paste(fr, bug, W - 20 - bug.width / 2, 58, 1, 0.85)))


def make_backgrounds():
    os.makedirs(f"{SK}/gfx", exist_ok=True)
    gfx.background(f"{SK}/kf/low.png").convert("RGB").save(f"{SK}/gfx/diag_bg.png")
    gfx.background(f"{SK}/kf/front_clean.png").convert("RGB").save(f"{SK}/gfx/board_bg.png")


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
VOICE_LINES = [("P1", f"{SK}/seg/P1.wav", P1_AT)] + [
    (f"P2{k}", f"{SK}/seg/{'H_voice' if k == 'H' else k}.wav", S0("H_voice" if k == "H" else k)) for k in "ABCDEFGHIJK"]


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
    put(bus, ring_x, RING2, 0.85)
    fx = {k: load(f"{SFX}/sfx_{k}.wav") for k in ("whoosh", "pop", "ding", "thud", "scratch", "riser", "stamp")}
    put(bus, fx["whoosh"], CLICK - 0.12, 0.5)                                  # crash zoom on the pick-up
    for tq, *_ in Q + Q2:
        put(bus, fx["pop"], tq, 0.45)
    for ta, *_ in AM:
        put(bus, fx["pop"], ta, 0.4); put(bus, fx["ding"], ta + 0.12, 0.25)
    put(bus, fx["thud"], 12.68, 0.5)                                            # BEFORE BOOKING?
    put(bus, fx["whoosh"], Q_OUT0, 0.3)
    put(bus, fx["scratch"], FIRST["A"] - 0.05, 0.3)                             # POOL CHHODO
    for t0 in (16.96, 19.18, 20.86, 22.98, 25.46, 42.22, 44.36):               # each check card, then its tick
        put(bus, fx["pop"], t0, 0.35); put(bus, fx["ding"], t0 + 0.35, 0.3)
    put(bus, fx["stamp"], 27.68, 0.55)                                          # LIKHWA KE LO
    for tw in WHIPS:
        put(bus, fx["whoosh"], tw - 0.2, 0.5)
    put(bus, fx["thud"], FIRST["D"], 0.45)                                      # AB ASLI KHEL
    put(bus, fx["whoosh"], DIAG0 - 0.1, 0.35)
    put(bus, fx["pop"], DIAG0 + 0.05, 0.3); put(bus, fx["pop"], DIAG0 + 0.2, 0.3); put(bus, fx["pop"], 35.58, 0.35)
    put(bus, fx["riser"], 38.20 - 1.3, 0.25); put(bus, fx["thud"], 38.20, 0.65)    # REGISTRY ATAK GAYI
    put(bus, fx["ding"], FIRST["G"] + 0.15, 0.3)                                # CHAABI ✓
    put(bus, fx["scratch"], 40.52 - 0.2, 0.4); put(bus, fx["thud"], 40.62, 0.45)  # KAAGAZ ✗
    put(bus, fx["whoosh"], BOARD0 - 0.1, 0.35)
    for i in range(7):
        put(bus, fx["pop"], BOARD0 + 0.15 + 0.07 * i, 0.2)
    put(bus, fx["pop"], 47.48, 0.35)                                            # COMMENT: FULL LIST
    put(bus, fx["pop"], 50.60, 0.35); put(bus, fx["ding"], 52.42, 0.35)         # item 8
    put(bus, fx["whoosh"], CUT("P2K") + 0.2, 0.25)                              # the pull-back
    put(bus, fx["thud"], 55.38, 0.45)                                           # WAISA HI DIKHEGA
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
           "length": {"min": 40, "max": 70, "expected": round(TOTAL, 2)},
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
    print(f"timeline: ring {RING:.2f}  P2 {FIRST['A']:.2f}  Billu {BILLU0:.2f}  card {CARD:.2f}  total {TOTAL:.2f}  "
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
