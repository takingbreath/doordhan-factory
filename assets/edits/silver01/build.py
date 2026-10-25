#!/usr/bin/env python3
"""silver01 (Sahayata Kendra, Pandey monologue, no caller, broadcast cards A): "Silver weekly chart: support toot gaya".
Built from assets/edits/sk04_build.py. Frame-composed edit: Pandey on camera for the hook, "Analysts ..." and the closing call;
the chart card (gfx.py, real MCX weekly candles, lines drawn on the spoken words) is the hero in between; Billu pushes a silver
bar off the desk on "gehri".
  pipeline/qcpy work/silver01/build.py  ->  work/silver01/edit_raw.mkv + work/silver01/qc_manifest.json
  PLAN_ONLY=1 ... prints the timeline;  DRAFT=1 writes a fast low-res look copy (never gated)
Reel time = cut time of work/silver01/voice/silver01_voice_cut.wav (59.16 s: the cut's own 0.15 s lead is the gate's lead).
Each talking clip (Wan 2.7, 0.5 s lead in each track, texture pass on) maps clip time c = 0.5 + (reel - segment start)."""
import json, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


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
DRAFT = bool(os.environ.get("DRAFT"))
sys.path.insert(0, f"{ROOT}/pipeline"); sys.path.insert(0, SK)
import sahayata_endcard as EC  # noqa: E402
import voice_room  # noqa: E402
import gfx  # noqa: E402  (work/silver01/gfx.py: the chart card)

EDIT_JSON = os.environ.get("EDIT_JSON", f"{SK}/edit.json")
FINAL = "outputs/silver01/E14_silver_pattern.mp4"
REPAIRS = os.environ.get("QC_REPAIRS", f"{SK}/qc_repairs.json")
REP = json.load(open(REPAIRS)) if os.path.exists(REPAIRS) else {}
CUTWAV = f"{SK}/voice/{SLUG}_voice_cut.wav"
rng = np.random.default_rng(7)
YEL, WHT, RED, GRN, INK = gfx.YEL, gfx.WHT, gfx.RED, gfx.GRN, gfx.INK
NAVY = gfx.NAVY


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                                capture_output=True, text=True).stdout)


# ---------------------------------------------------------------- timeline (reel seconds = cut seconds; Scribe on the cut)
SEGS = json.load(open(f"{SK}/seg/segments.json"))          # T1, T3, T4: cut_start / cut_end of each talking line's wav
LEAD = 0.12                                                # talking shots cut in 0.12 s before the first word
TRACK_LEAD = 0.5                                           # silence before the line in every Wan track
FIRST = {"T1": 0.14, "T3": 44.63, "T4": 54.00}             # first word of each talking segment (verify_line on each seg wav)
CLIP0 = {"T1": 0.0, "T3": 44.35, "T4": 52.85}              # where each Wan track's wav starts in cut time (T4 was generated from 52.85; the shot uses it from 53.88)
CARD_IN = 3.30                                             # 0.25 s after "hai"
BILLU_IN, BILLU_SRC = 41.25, 0.0                           # B2: the bar tips over the desk edge 1.3 s in (42.55 s, "aur") and lands 1.95 s in = 43.20 s, on "gehri"
T3_IN = FIRST["T3"] - LEAD                                 # 44.54
CARD2_IN = 49.90
T4_IN = FIRST["T4"] - LEAD                                 # 53.88
CARD = 59.40                                               # 0.30 s after the last word (cut ends at 59.16)
CARD_LEN = 4.8
TOTAL = CARD + CARD_LEN
TALK = {"T1": ("T1_tx", "T1"), "T3": ("T3_tx", "T3"), "T4": ("T4_tx", "T4")}
JUDGE_SHIFT = {}                                           # shot_spec.py judge said ACCEPT on all three: no shift


def S0(line):
    return SEGS[line]["cut_start"]


def CUT(line):
    if line == "T1":
        return 0.0
    return FIRST[line] - LEAD + REP.get(line, {}).get("cut_in_delay_s", 0.0)


def TK(line, t0):
    shift = JUDGE_SHIFT.get(line, 0.0) + REP.get(line, {}).get("src_shift_s", 0.0)
    return f"{V}/{TALK[line][0]}.mp4", TRACK_LEAD + (t0 - CLIP0[line]) + shift


# ---------------------------------------------------------------- video helpers
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


class Clip:
    def __init__(self, path, src_in=0.0, speed=1.0):
        vf = f"fps={FPS},scale={W}:{H}:flags=lanczos,format=rgb24"
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{max(0, src_in):.3f}", "-i", path, "-vf", vf, "-an",
                                   "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
        self.last = None

    def next(self, t=None):
        b = self.p.stdout.read(W * H * 3)
        if len(b) == W * H * 3:
            self.last = np.frombuffer(b, np.uint8).reshape(H, W, 3)
        return self.last

    def close(self):
        self.p.kill()


BROLL = f"{V}/broll.mp4"
BROLL_IN = float(os.environ.get("BROLL_IN", "0.0"))


class SplitClip:
    """the opening: silver B-roll on the top half, Pandey on the bottom half (his face stays below y 850, above the app's caption area)"""
    def __init__(self, bot_path, bot_in):
        self.top = Clip(BROLL, BROLL_IN) if os.path.exists(BROLL) else None
        self.bot = Clip(bot_path, bot_in)

    def next(self, t=None):
        b = self.bot.next()
        out = np.zeros((H, W, 3), np.uint8)
        out[640:1280] = b[345:985]
        tp = self.top.next() if self.top is not None else None
        if tp is not None:
            out[0:640] = tp[420:1060]
        else:
            out[0:640] = (150, 160, 175)
        out[636:644] = (255, 214, 0)
        return out

    def close(self):
        self.top and self.top.close(); self.bot.close()


class ChartCard:
    """the chart card as a shot: frames come from gfx.chart_frame(reel time)"""
    def next(self, t):
        return np.asarray(gfx.chart_frame(t).convert("RGB"))

    def close(self):
        pass


# face centres (720x1280), measured on each textured clip with work/silver01/mouthbox.py
FACE = {"T1": (370, 605), "T3": (371, 566), "T4": (381, 581)}
SHOTS = []


def shot(t0, t1, path, src_in, zoom, speed=1.0, line=None, kind="clip"):
    SHOTS.append(dict(t0=t0, t1=t1, path=path, src_in=src_in, zoom=zoom, speed=speed, line=line, kind=kind))


def talk(line, t0, t1, zoom):
    path, src = TK(line, t0)
    shot(t0, t1, path, src, zoom, line=line)


talk("T1", 0.0, CARD_IN, const(1.0))
SHOTS[-1]["kind"] = "split"
shot(CARD_IN, BILLU_IN, "", 0.0, const(1.0), kind="chart")
shot(BILLU_IN, T3_IN, f"{V}/B2.mp4", BILLU_SRC, const(1.0))
talk("T3", T3_IN, CARD2_IN, ramp(T3_IN, CARD2_IN, 1.0, 1.07, FACE["T3"]))
shot(CARD2_IN, T4_IN, "", 0.0, const(1.0), kind="chart")
talk("T4", T4_IN, CARD, const(1.0))

WHIPS = [CARD_IN, BILLU_IN, T3_IN, CARD2_IN, T4_IN]
SHAKES = [(gfx.T["BREAK"], 0.25, 10), (gfx.T["TARGET_TAG"], 0.20, 6), (43.20, 0.22, 9)]   # only on the punch beats

# ---------------------------------------------------------------- overlays
EVENTS = []   # (start, end, drawer(frame, t))
paste, pop_scale = gfx.paste, gfx.pop

# the opening: a silver B-roll on the top half, Pandey on the bottom half, the hook on the B-roll (on screen from the first frame)
hook1 = gfx.fit("SILVER", "TitanOne.ttf", 104, 620, fill=YEL, stroke=9)
hook2 = gfx.fit("SUPPORT TOOT GAYA", "TitanOne.ttf", 54, 640, fill=WHT, stroke=7)


def draw_hook(fr, t):
    al = 1.0 if t < CARD_IN - 0.10 else max(0.0, (CARD_IN - t) / 0.10)
    paste(fr, hook1, W / 2, 468, 1.0, al); paste(fr, hook2, W / 2, 566, 1.0, al)


EVENTS.append((0.0, CARD_IN, draw_hook))



# the closing call, on the word "naam": a bouncing yellow arrow under the caption points down at the comment button
def _arrow():
    im = Image.new("RGBA", (90, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for col, grow in ((INK + (255,), 8), (YEL + (255,), 0)):
        d.rectangle([32 - 12 + grow * -0, 8 + grow, 58 + 12 - 24, 58], fill=col) if False else None
        d.polygon([(45 - 17 + grow * -1, 10 + grow), (45 + 17 + grow, 10 + grow), (45 + 17 + grow, 56), (45 + 38 + grow, 56), (45, 100 - grow),
                   (45 - 38 - grow, 56), (45 - 17 + grow * -1, 56)], fill=col)
    return im


ARROW = _arrow()
CALLTXT = gfx.fit("COMMENT", "TitanOne.ttf", 44, 200, fill=YEL, stroke=6)


def draw_call(fr, t):
    t0 = 57.94
    al = min(1.0, (t - t0) / 0.1)
    bounce = 14 * abs(np.sin((t - t0) * 3.2 * np.pi))
    paste(fr, ARROW, 560, 1052 + bounce, pop_scale(t - t0), al)
    paste(fr, CALLTXT, 560, 996, pop_scale(t - t0), al)


EVENTS.append((57.94, CARD, draw_call))



# the DOORDHAN bug, top right (right edge x = 700, y = 36), until the card
bug = gfx.sprite("DOORDHAN", gfx.font("Bungee.ttf", 30), (255, 255, 255, 215), stroke=3, shadow=3, pad=6)
bug_dark = gfx.sprite("DOORDHAN", gfx.font("Bungee.ttf", 30), (30, 40, 90, 255), stroke=3, sfill=(255, 255, 255), shadow=0, pad=6)
CHART_WINDOWS = [(CARD_IN, BILLU_IN), (CARD2_IN, T4_IN)]


def draw_bug(fr, t):
    on_chart = any(a <= t < b for a, b in CHART_WINDOWS)
    paste(fr, bug_dark if on_chart else bug, W - 20 - bug.width / 2, 58, 1, 0.95 if on_chart else 0.85)


EVENTS.append((0, CARD, draw_bug))


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
    crf, preset = ("28", "ultrafast") if DRAFT else ("15", "veryfast")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", crf, "-preset", preset,
                            "-pix_fmt", "yuv420p", out_video], stdin=subprocess.PIPE)
    si, cur, clip = -1, None, None
    for fi in range(int(round(CARD * FPS))):
        t = fi / FPS
        while si + 1 < len(SHOTS) and t >= SHOTS[si + 1]["t0"] - 1e-6:
            si += 1; cur = SHOTS[si]
            if clip:
                clip.close()
            clip = (ChartCard() if cur["kind"] == "chart" else SplitClip(cur["path"], cur["src_in"]) if cur["kind"] == "split"
                    else Clip(cur["path"], cur["src_in"], cur["speed"]))
        arr = clip.next(t)
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
VOICE_LINES = [("T1", f"{SK}/seg/T1.wav", S0("T1")), ("T3", f"{SK}/seg/T3.wav", S0("T3")), ("T4", f"{SK}/seg/T4.wav", S0("T4"))]
BAR_SLIDE_AT, BAR_CLANG_AT, BAR_BOUNCE_AT = 41.80, 43.22, 43.95


def mix(out_wav):
    n = int(TOTAL * SR) + SR
    bus = np.zeros(n, np.float32)
    dbus = np.zeros(n, np.float32)

    def put(b, x, t, g=1.0):
        i = int(round(t * SR)); j = min(n, i + len(x)); b[i:j] += g * x[: j - i]

    voice = load(CUTWAV)                                   # the whole approved cut: the voice is continuous under every shot
    put(dbus, voice, 0.0)
    put(bus, voice_room.treat(np.pad(voice, (0, 0))), 0.0)
    for lid, f, t0 in VOICE_LINES:                         # the talking lines as placed, for the gate's mix check
        x = load(f)
        end = REP.get(lid, {}).get("voice_end_s")
        if end is not None:
            fd = int(REP.get(lid, {}).get("fade_s", 0.05) * SR)
            x = x[: int(end * SR)].copy(); x[-fd:] *= np.linspace(1, 0, fd)
        PLACED[lid] = (t0, t0 + len(x) / SR, f)
    tmp = os.path.join(SK, "tmp"); os.makedirs(tmp, exist_ok=True)
    fx = {k: load(f"{SFX}/sfx_{k}.wav") for k in ("whoosh", "pop", "ding", "thud", "stamp2", "marker", "scribble", "slide", "slap", "chime")}
    own = {k: load(f"{SK}/sfx/{k}.wav") for k in ("bar_slide", "bar_clang")}
    T = gfx.T
    for tw in WHIPS:
        put(bus, fx["whoosh"], tw - 0.2, 0.5)
    put(bus, fx["slide"], T["CARD_IN"] + 0.15, 0.3)                                       # the candles draw in
    put(bus, fx["whoosh"], T["DOWN_ARROW"][0], 0.3)                                       # the red arrow
    put(bus, fx["marker"], T["PATTERN"][0], 0.35)                                         # the dashed outline
    put(bus, fx["slap"], T["ASC"][0], 0.3); put(bus, fx["slide"], T["OPP"][0], 0.35)      # the two small triangles
    put(bus, fx["marker"], T["TREND"][0] + 0.02, 0.5); put(bus, fx["scribble"], T["TREND"][0] + 0.9, 0.35)
    u = lambda k: T["TREND"][0] + (T["TREND"][1] - T["TREND"][0]) * 0.0                    # noqa: E731
    for tt in (14.10, 14.64, 15.17, 15.34):                                              # rings where the falling line meets the highs
        put(bus, fx["pop"], tt, 0.4)
    for tt in T["BOTTOM_RINGS"]:
        put(bus, fx["pop"], tt, 0.4)
    put(bus, fx["marker"], T["SUPPORT"][0], 0.5); put(bus, fx["pop"], T["SUP_TAG"], 0.35)
    put(bus, fx["stamp2"], T["BREAK"], 0.9); put(bus, fx["thud"], T["BREAK"], 0.45)       # TOOT GAYA
    put(bus, fx["pop"], T["QMARK"][0], 0.45)
    put(bus, fx["pop"], T["TOPTAG"], 0.4); put(bus, fx["marker"], T["HEIGHT"][0], 0.5); put(bus, fx["pop"], T["HEIGHT_TAG"], 0.4)
    put(bus, fx["slide"], T["COPY"][0], 0.5); put(bus, fx["pop"], T["COPY"][1] - 0.2, 0.4)
    put(bus, fx["marker"], T["TARGET"][0], 0.5); put(bus, fx["ding"], T["TARGET_TAG"], 0.35); put(bus, fx["thud"], T["TARGET_TAG"], 0.4)
    put(bus, fx["whoosh"], T["KAMZORI"], 0.3); put(bus, fx["marker"], T["PROJECT"][0], 0.4)
    sl = own["bar_slide"][: int(0.9 * SR)].copy(); sl[-int(0.25 * SR):] *= np.linspace(1, 0, int(0.25 * SR))
    put(bus, sl, BAR_SLIDE_AT, 0.5)                                                       # the paw pushes the bar to the edge
    put(bus, own["bar_clang"], BAR_CLANG_AT, 0.9)                                         # it hits the floor, on "gehri"
    put(bus, fx["thud"], BAR_BOUNCE_AT, 0.3)                                              # it topples flat after the bounce
    put(bus, fx["pop"], 57.94, 0.4)                                                       # the call arrow
    ew = os.path.join(tmp, "end.wav"); EC.audio(ew, CARD_LEN)
    ewq = os.path.join(tmp, "end_eq.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", ew, "-af", "highpass=f=300,lowpass=f=3400", "-ar", str(SR), ewq], check=True)
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
    lines = []
    for lid, f, t0 in VOICE_LINES:
        ln = {"id": lid, "speaker": "pandey", "start": round(PLACED[lid][0], 3), "end": round(PLACED[lid][1], 3),
              "source": rel(PLACED[lid][2])}
        if lid in TALK:
            ln.update(cut_in=round(CUT(lid), 3), segments=segs.get(lid, []), clip=rel(f"{V}/{TALK[lid][0]}.mp4"),
                      clip_spans=spans.get(lid, []))
        lines.append(ln)
    py = "pipeline/qcpy"
    env = f"EDIT_JSON={rel(EDIT_JSON)} QC_REPAIRS={rel(REPAIRS)}"
    man = {"slug": SLUG, "format": "sahayata_kendra", "final": FINAL,
           "script": f"registry/scripts/{SLUG}.json",
           "characters": {"pandey": "assets/characters/pandey_sheet_v2.jpg"},
           "dialogue_stem": rel(os.path.join(SK, "tmp", "dialogue.wav")),
           "prefinish": rel(os.path.join(SK, "edit_raw.mkv")),
           "length": {"min": 40, "max": 75, "expected": round(TOTAL, 2)},
           "loudness": {"target": edit.get("target_lufs", -14)},
           "repairs_file": rel(REPAIRS),
           "rebuild": f"{env} bash {rel(SK)}/make_final.sh",
           "lines": lines}
    path = os.path.join(os.path.dirname(EDIT_JSON), "qc_manifest.json")
    json.dump(man, open(path, "w"), indent=1, ensure_ascii=False)
    return path


if __name__ == "__main__":
    tmp = os.path.join(SK, "tmp"); os.makedirs(tmp, exist_ok=True)
    vid, wav = os.path.join(tmp, "video.mp4"), os.path.join(tmp, "mix.wav")
    talking = sum(sh["t1"] - sh["t0"] for sh in SHOTS if sh["line"])
    chart = sum(sh["t1"] - sh["t0"] for sh in SHOTS if sh["kind"] == "chart")
    print(f"timeline: card {CARD_IN:.2f}  Billu {BILLU_IN:.2f}  T3 {T3_IN:.2f}  card2 {CARD2_IN:.2f}  T4 {T4_IN:.2f}  "
          f"end {CARD:.2f}  total {TOTAL:.2f}\n  face talking to camera {talking:.1f} s = {100 * talking / TOTAL:.0f}%   "
          f"chart card {chart:.1f} s = {100 * chart / TOTAL:.0f}%")
    for sh in SHOTS:
        end_src = sh["src_in"] + (sh["t1"] - sh["t0"]) * sh["speed"]
        d = dur(sh["path"]) if sh["path"].endswith(".mp4") else 99
        flag = "  <-- runs past the clip" if end_src > d - 0.02 else ""
        print(f"  {sh['t0']:6.2f}-{sh['t1']:6.2f}  {os.path.basename(sh['path']) or 'CHART CARD':14s} src {sh['src_in']:5.2f}-{end_src:5.2f} of {d:5.2f}{flag}")
    if os.environ.get("PLAN_ONLY"):
        sys.exit()
    json.dump(CHART_WINDOWS, open(os.path.join(SK, "chart_windows.json"), "w"))
    mix(wav); print("mixed", wav)
    print("qc manifest", write_qc_manifest())
    render(vid); print("rendered", vid)
    out = os.path.join(SK, "edit_draft.mkv" if DRAFT else "edit_raw.mkv")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", "-shortest", out], check=True)
    print("wrote", out, f"{dur(out):.2f}s")
