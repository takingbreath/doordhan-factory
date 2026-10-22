#!/usr/bin/env python3
"""sk05 edit (eMudhra, Pandey monologue): Sahayata Kendra shot as a mockumentary, with E11's Vox collage graphics.

The Jio reel (E11) is the look benchmark: modern phone grade, 30 fps, light grain, no CRT finish. The camera is The Office's:
handheld operator sway on every live shot, snap zooms that overshoot and settle with a focus hunt on the punch lines, a late
reframe after each snap, whip pans in and out of Pandey and Billu. All camera work is done here; the Wan clips are locked off.

Times are in VOICE time (v, seconds into voice/sk05_voice_cut.wav); the reel runs v + V0.
  python3 work/sk05/build.py              full build -> work/sk05/edit_raw.mp4 (pre-finish) and outputs/sk05/sk05.mp4
  PLAN_ONLY=1 python3 work/sk05/build.py  prints the timeline and talking share
  DRAFT=1 python3 work/sk05/build.py      a fast look-only copy
Opening: split (collage hook on top, Pandey below); the close returns to the same split and freezes on the opening frame,
so the reel loops into its first line.
"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
SLUG = os.path.basename(HERE); WREL = os.path.relpath(HERE, ROOT)
W, H, FPS = 720, 1280, 30
V0 = 0.15
VID = f"{HERE}/vid"; G = f"{HERE}/gfx"; KF = f"{HERE}/kf"; TMP = f"{HERE}/build"; os.makedirs(TMP, exist_ok=True)
FONT = f"{ROOT}/assets/fonts/Baloo2-Latin-ExtraBold.ttf"
DEVA = f"{ROOT}/assets/fonts/Baloo2-Deva-ExtraBold.ttf"
BUNGEE = f"{ROOT}/assets/fonts/Bungee.ttf"
VOICE = f"{HERE}/voice/sk05_voice_cut.wav"
SPLIT = 640
FACE_Y0 = 40                   # Pandey's window in the 720x1280 clip for the split (face centre ~343, hair top ~120)
END_V = 91.45                  # the last word ends 91.40 (speech_map)
TAIL = 0.40                    # the loop tail: the opening split frame, frozen
T1_OFF = 0.05 - 0.5            # talking-shot offsets: src = v - off (the segment's cut start - the 0.5 s lead)
CAT = (360, 860)               # Billu's face in his 720x1280 clips

# ---- shots: (v_in, v_out, kind, args). cam: z base zoom, snaps [(v, zoom)], face (x, y) the snap target,
# push (z0, z1) a slow push, whip_in / whip_out, hand (handheld amplitude; 0 for the collage, which has its own drift)
SHOTS = [
    (-V0, 3.05, "split", dict(src=f"{VID}/T1.mp4", off=T1_OFF, top=f"{G}/hook.mp4", top_ss=0.0, name="T1")),
    (3.05, 3.90, "live", dict(src=f"{G}/bars.mp4", ss=0.0, cam=dict(hand=0), grain=1, name="bars")),
    (3.90, 7.95, "live", dict(src=f"{G}/chart.mp4", ss=0.0, cam=dict(hand=0), grain=2, name="chart")),
    (7.95, 14.55, "live", dict(src=f"{G}/gst.mp4", ss=0.0, cam=dict(hand=0, whip_out=True), grain=2, name="gst")),
    (14.55, 15.75, "live", dict(src=f"{KF}/B1.png", ss=0.0, still=True, cam=dict(z=1.04, push=(1.04, 1.16), face=CAT, whip_in=True),
                                grain=2, name="B_still")),                                  # 'matlab samjho,' Billu leans in
    (15.75, 23.60, "live", dict(src=f"{G}/cert.mp4", ss=0.0, cam=dict(hand=0), grain=2, name="cert")),
    (23.60, 30.05, "live", dict(src=f"{G}/pass.mp4", ss=0.0, cam=dict(hand=0), grain=2, name="pass")),
    (30.05, 33.80, "live", dict(src=f"{G}/hack.mp4", ss=0.0, cam=dict(hand=0, whip_out=True), grain=2, name="hack")),
    (33.80, 35.05, "live", dict(src=f"{VID}/B_shock.mp4", ss=0.35, cam=dict(snaps=[(34.10, 1.5)], face=CAT, whip_in=True),
                                grain=1, name="B_shock")),                                  # snap onto Billu's shock
    (35.05, 39.30, "live", dict(src=f"{G}/rob.mp4", ss=0.0, cam=dict(hand=0, whip_out=True), grain=2, name="rob")),
    (39.30, 42.95, "talk", dict(src=f"{VID}/T2.mp4", off=39.30 - 0.5,
                                cam=dict(snaps=[(40.42, 1.36), (41.22, 1.55)], face=(399, 511), whip_in=True, whip_out=True),
                                name="T2")),                                                # 'Nahi' snap, 'atharah mahine' snap again
    (42.95, 51.80, "live", dict(src=f"{G}/quar.mp4", ss=0.0, cam=dict(hand=0, whip_in=True), grain=2, name="quar")),
    (51.80, 52.90, "talk", dict(src=f"{VID}/T3.mp4", off=51.80 - 0.5 + 0.08, cam=dict(z=1.10, face=(368, 600)), name="T3a")),
    (52.90, 55.55, "live", dict(src=f"{G}/audit.mp4", ss=0.0, cam=dict(hand=0), grain=2, name="audit")),
    (55.55, 58.45, "talk", dict(src=f"{VID}/T3.mp4", off=51.80 - 0.5 + 0.08,
                                cam=dict(z=1.10, snaps=[(56.78, 1.55)], face=(368, 600)), name="T3b")),   # 'To AUDIT mein'
    (58.45, 63.60, "live", dict(src=f"{G}/unaff.mp4", ss=0.0, cam=dict(hand=0), grain=2, name="unaff")),
    (63.60, 68.05, "talk", dict(src=f"{VID}/T4.mp4", off=63.60 - 0.5,
                                cam=dict(snaps=[(67.28, 1.42)], face=(342, 421), whip_out=True), name="T4")),  # 'sab changa si?'
    (68.05, 69.00, "live", dict(src=f"{VID}/B_turn.mp4", ss=0.30, cam=dict(z=1.12, push=(1.12, 1.2), face=CAT, whip_in=True),
                                grain=1, name="B_turn")),                                   # Billu turns away
    (69.00, 72.35, "live", dict(src=f"{G}/trust.mp4", ss=0.0, cam=dict(hand=0), grain=2, name="trust")),
    (72.35, 84.50, "live", dict(src=f"{G}/digi.mp4", ss=0.0, cam=dict(hand=0), grain=2, name="digi")),
    (84.50, 87.50, "live", dict(src=f"{G}/rev.mp4", ss=0.0, cam=dict(hand=0), grain=2, name="rev")),
    (87.50, END_V, "split", dict(src=f"{VID}/T5.mp4", off=87.50 - 0.5, top=f"{G}/cred.mp4", top_ss=0.0, name="T5")),
    (END_V, END_V + TAIL, "split", dict(src=f"{VID}/T1.mp4", off=END_V - (-V0 - T1_OFF), top=f"{G}/hook.mp4", top_ss=0.0,
                                        freeze=True, name="loop")),
]
TALK = {"T1", "T2", "T3a", "T3b", "T4", "T5"}
LINE_SHOTS = {"L1": ["T1"], "L3": ["T2"], "L5": ["T3a", "T3b"], "L7": ["T4"], "L9": ["T5"]}
REPAIRS = f"{HERE}/qc_repairs.json"
if os.path.exists(REPAIRS):
    for line, rp in json.load(open(REPAIRS)).items():
        for v_in, v_out, kind, a in SHOTS:
            if a["name"] in LINE_SHOTS.get(line, []) and "src_shift_s" in rp:
                a["off"] -= rp["src_shift_s"]

# ---- captions: Roman Hinglish groups, starts from Whisper word times on the cut (snapped to the end of a pause when
# Whisper put a word's start inside one); * marks the highlighted words
CAPS = [(0.05, "India ki is *security company* ne"), (1.44, "ye kya *kaand* kar diya?"),
        (4.30, "eMudhra do *lower circuits* mein"), (6.25, "*36%* gir gaya"),
        (7.90, "*GST, income tax*"), (9.40, "*import-export* registration"), (10.84, "mein eMudhra ke"),
        (12.10, "*digital signature*"), (12.90, "*certificates* use hote hain"),
        (14.65, "Matlab samjho,"),
        (15.80, "ee company website"), (16.82, "*asli* hone ki"), (17.82, "*digital certificate* deti hai"),
        (19.68, "aur certificate dene ka"), (20.92, "*control* sirf"), (22.04, "company ke paas hona chahiye"),
        (23.90, "par is *SECURITY* company mein"), (25.34, "security itni *kamzor*"), (26.68, "nikli, ki jaise aapka"),
        (27.90, "*password* ek, do, teen ho!"),
        (30.00, "koi *hacker*"), (30.66, "*nakli certificate* bana ke"), (32.45, "*fake website* ko"), (33.38, "*asli* dikha sakta tha"),
        (35.00, "Pata hai"), (35.40, "*Rob Stradling* ne"), (36.20, "email karke isi system ki"), (37.64, "ek *gadbad* kab batayi thi?"),
        (39.30, "Do-teen din pehle?"), (40.50, "*Nahi*,"), (41.20, "*atharah mahine* pehle!"),
        (43.40, "eMudhra boli,"), (44.50, "*email miss* ho gayi thi"), (46.24, "follow-up karne par"), (47.50, "action bhi hua"),
        (48.40, "lekin ee security"), (49.86, "*problem*... reh gayi"),
        (51.80, "Company ke mutabik"), (52.86, "kareeb *atharah mahine*"), (54.24, "aur *do audits* mein bhi"),
        (55.38, "*nahi pakdi gayi!*"),
        (56.80, "To *AUDIT* mein"), (57.48, "*check* kya ho raha tha?"),
        (58.90, "Ab keh rahe hain,"), (59.74, "*data breach* nahi hua"), (60.98, "India ki *signing services*"),
        (62.44, "*unaffected* hain"),
        (63.60, "aur *website certificates* ka"), (64.84, "*business* hi band kar rahe hain"), (66.50, "Matlab..."),
        (67.30, "*sab changa si?*"),
        (68.50, "Is *business* mein"), (69.60, "*bharosa* uthne ka"), (70.76, "matlab samjho."),
        (72.30, "*2011* mein"), (73.50, "*Netherlands* ki certificate company"), (75.12, "*DigiNotar* hack hui"),
        (76.65, "*nakli certificates* chale"), (77.86, "to sabne uski"), (78.90, "*mohar reject* kar di"),
        (80.25, "maamla *public* hone ke"), (81.28, "kareeb *teen hafte* baad"), (82.90, "company *bankrupt* thi"),
        (84.50, "Ee business *revenue* ka"), (85.70, "sirf *ek percent* hai,"),
        (87.50, "par *sawaal*"), (88.18, "poori company ki"), (89.32, "*credibility* ka hai!"),
        (90.55, "Tabhi toh main kehta hoon...")]
YEL = (255, 214, 10)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"FAILED: {' '.join(cmd)[:300]}\n{r.stderr[-1500:]}")
    return r


def grade(grain=1):
    # clean modern phone look (E11): a touch of contrast and warmth, fine light grain
    return f"eq=contrast=1.04:saturation=1.05,colorbalance=rs=0.02:bs=-0.02,noise=alls={grain}:allf=t"


def handheld(dur, seed=0.0, zoom=1.07, punch=1.0, w=W, h=H):
    """ffmpeg operator sway, for the split's bottom half"""
    z = zoom * punch
    cw, ch = f"trunc(iw/{z}/2)*2", f"trunc(ih/{z}/2)*2"
    x = f"(iw-ow)/2+(iw-ow)/2*0.55*(0.6*sin(2*PI*(t+{seed})*0.31)+0.3*sin(2*PI*(t+{seed})*1.07+1)+0.1*sin(2*PI*t*2.9))"
    y = f"(ih-oh)*0.42+(ih-oh)/2*0.5*(0.6*sin(2*PI*(t+{seed})*0.23+2)+0.3*sin(2*PI*(t+{seed})*0.93)+0.1*sin(2*PI*t*2.6+0.5))"
    return (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
            f"rotate='0.006*sin(2*PI*(t+{seed})*0.37)':fillcolor=none,crop=w={cw}:h={ch}:x='{x}':y='{y}',scale={w}:{h}")


# ---- the mockumentary camera (from camtest/cam.py, which Akhilesh approved)
def sway(t, amp):
    x = amp * (5.5 * math.sin(2 * math.pi * 0.31 * t + 1.0) + 2.5 * math.sin(2 * math.pi * 0.83 * t + 2.1) + 0.9 * math.sin(2 * math.pi * 2.3 * t))
    y = amp * (4.0 * math.sin(2 * math.pi * 0.27 * t + 0.4) + 2.0 * math.sin(2 * math.pi * 0.71 * t + 1.3) + 0.7 * math.sin(2 * math.pi * 2.9 * t + 0.5))
    r = amp * (0.35 * math.sin(2 * math.pi * 0.23 * t + 0.7) + 0.12 * math.sin(2 * math.pi * 1.1 * t))
    return x, y, r


def snap(s, z0, z1, dur=0.22):
    """s seconds after a snap starts: (zoom, motion 0..1). A fast zoom that overshoots ~6% and settles, like a hand on the rocker"""
    x = s / dur
    if x < 1:
        e = 1 - (1 - x) ** 3
        return z0 + (z1 - z0) * e * 1.06, x
    q = s - dur
    return z1 + (z1 - z0) * 0.06 * math.exp(-q * 7) * math.cos(q * 18), 0.0


def cam_at(c, v, t, dur):
    """zoom, centre, rotation, blur (px) and whip offset (px) for one frame: v voice time, t seconds into the shot"""
    zb = c.get("z", 1.06); z = zb; moving = 0.0; landed = None
    if "push" in c:
        a, b = c["push"]; u = t / max(dur, 1e-3); z = zb = a + (b - a) * (u * u * (3 - 2 * u))
    for vs, zt in c.get("snaps", []):
        if v >= vs:
            z, moving = snap(v - vs, z, zt); landed = vs + 0.22
    fx, fy = c.get("face", (W / 2, H / 2))
    k = min(1.0, max(0.0, (z - zb) / 0.3)) if c.get("snaps") else min(1.0, max(0.0, (z - 1.0) / 0.3))
    cx, cy = W / 2 + (fx - W / 2) * k, H / 2 + (fy - H / 2) * k
    if landed is not None and v > landed + 0.45:            # late reframe: the operator nudges after landing
        u = min(1.0, (v - landed - 0.45) / 0.5); u = u * u * (3 - 2 * u); cx += 14 * u; cy -= 9 * u
    hand = c.get("hand", 1.0)
    hx, hy, hr = sway(t + 3.1 * (int(sum(c.get("face", (0, 0)))) % 7), hand * (1.0 + 0.6 * (z - 1.06)))
    cx += hx; cy += hy
    half_w, half_h = W / (2 * z), H / (2 * z)               # keep the crop inside the picture
    cx = min(max(cx, half_w), W - half_w); cy = min(max(cy, half_h), H - half_h)
    blur = 1.6 * math.sin(math.pi * moving) if moving > 0 else 0.0
    if landed is not None and 0.0 < v - landed < 0.28:      # the focus breathes once after landing
        blur = max(blur, 0.9 * math.sin(math.pi * (v - landed) / 0.28))
    wx = 0.0
    if c.get("whip_out") and t > dur - 0.18:
        u = (t - (dur - 0.18)) / 0.18; wx = u * u * 820
    if c.get("whip_in") and t < 0.15:
        u = 1 - t / 0.15; wx = -u * u * 820
    return z, cx, cy, hr, blur, wx


def decode(path, ss, n, still=False):
    """n frames of a clip (or a still) from ss, as 720x1280 RGB arrays; holds the last frame if the clip runs out"""
    inp = ["-loop", "1", "-i", path] if still else ["-ss", f"{ss:.3f}", "-i", path]
    vf = f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},tpad=stop_mode=clone:stop_duration=2"
    p = subprocess.Popen(["ffmpeg", "-v", "error"] + inp + ["-vf", vf, "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         stdout=subprocess.PIPE)
    last = None
    for _ in range(n):
        buf = p.stdout.read(W * H * 3)
        if len(buf) == W * H * 3:
            last = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        yield last
    p.stdout.close(); p.wait()


def nframes(v_in, v_out):
    return int(round((v_out + V0) * FPS)) - int(round((v_in + V0) * FPS))


def render_live(v_in, v_out, a, out):
    import cv2
    nf = nframes(v_in, v_out); dur = nf / FPS; c = a.get("cam", {})
    ss = v_in - a["off"] if "off" in a else a.get("ss", 0.0)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-vf", grade(a.get("grain", 1)), "-frames:v", str(nf), "-c:v", "libx264", "-crf", "16",
                            "-preset", "fast", "-pix_fmt", "yuv420p", "-an", out], stdin=subprocess.PIPE)
    for i, fr in enumerate(decode(a["src"], ss, nf, a.get("still", False))):
        t = i / FPS; v = v_in + t
        z, cx, cy, rot, blur, wx = cam_at(c, v, t, dur)
        M = cv2.getRotationMatrix2D((cx, cy), rot, z)
        M[0, 2] += W / 2 - cx - wx; M[1, 2] += H / 2 - cy
        f = cv2.warpAffine(fr, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)   # smears like a whip; reflect mirrors
        if blur > 0.05:
            f = cv2.GaussianBlur(f, (0, 0), blur)
        if abs(wx) > 1:
            k = int(9 + 70 * min(1.0, abs(wx) / 820)) | 1
            f = cv2.filter2D(f, -1, np.full((1, k), 1.0 / k, np.float32))
        enc.stdin.write(np.ascontiguousarray(f).tobytes())
    enc.stdin.close(); enc.wait()


def render(i, shot):
    v_in, v_out, kind, a = shot
    nf = nframes(v_in, v_out); dur = round(nf / FPS, 4)
    out = f"{TMP}/s{i:02d}_{a['name']}.mp4"
    enc = ["-r", str(FPS), "-frames:v", str(nf), "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p", "-an", out]
    if kind in ("live", "talk"):
        render_live(v_in, v_out, a, out)
    elif kind == "split":
        ss = v_in - a["off"]
        tin = ["-loop", "1", "-t", f"{dur + 0.3:.3f}", "-i", f"{TMP}/seam.png"]
        if a.get("freeze"):
            fv = (f"[0:v]trim=start_frame=0:end_frame=1,loop={nf + 5}:1:0,setpts=N/{FPS}/TB[hk];"
                  f"[1:v]trim=start_frame=0:end_frame=1,loop={nf + 5}:1:0,setpts=N/{FPS}/TB,")
            ins = ["-i", a["top"], "-ss", f"{ss:.3f}", "-i", a["src"]]
            seed = 0.0                                    # the same sway phase as the opening shot's first frame
        else:
            fv = f"[0:v]fps={FPS},tpad=stop_mode=clone:stop_duration=1,setpts=PTS-STARTPTS[hk];[1:v]"
            ins = ["-ss", f"{a['top_ss']:.3f}", "-t", f"{dur + 0.3:.3f}", "-i", a["top"],
                   "-ss", f"{ss:.3f}", "-t", f"{dur + 0.3:.3f}", "-i", a["src"]]
            seed = 0.0 if a["name"] == "T1" else i * 1.7
        fc = (fv + f"{handheld(dur, seed=seed, zoom=1.04)},{grade(1)},crop={W}:{H - SPLIT}:0:{FACE_Y0}[rs];"
              f"[hk]scale={W}:{SPLIT},{grade(2)}[hk2];[hk2][rs]vstack=inputs=2[st];[st][2:v]overlay=0:{SPLIT - 24}[v]")
        run(["ffmpeg", "-v", "error", "-y"] + ins + tin + ["-filter_complex", fc, "-map", "[v]"] + enc)
    return out


def seam_png():
    """a torn white paper edge with a soft shadow over the seam between the collage and Pandey (E11)"""
    import random
    from PIL import ImageFilter
    r = random.Random(4); im = Image.new("RGBA", (W, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    top = [(x, 18 + r.randint(-4, 4)) for x in range(0, W + 12, 12)]
    bot = [(x, 30 + r.randint(-5, 5)) for x in range(W + 12, -12, -12)]
    sh = Image.new("RGBA", (W, 48), (0, 0, 0, 0)); ImageDraw.Draw(sh).polygon([(x, y + 6) for x, y in top + bot], fill=(0, 0, 0, 90))
    sh = sh.filter(ImageFilter.GaussianBlur(4)); im.alpha_composite(sh)
    d.polygon(top + bot, fill=(248, 246, 238, 255))
    if not os.path.exists(f"{TMP}/seam.png"):
        im.save(f"{TMP}/seam.png")


# ---- text overlays
def font(size):
    return ImageFont.truetype(FONT, size)


def runs(text, size):
    out = []
    for i, piece in enumerate(text.split("₹")):
        if i:
            out.append(("₹", ImageFont.truetype(DEVA, size)))
        if piece:
            out.append((piece, font(size)))
    return out


def textlen(text, size):
    d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    return sum(d.textlength(p, font=f) for p, f in runs(text, size))


def draw_text(d, xy, text, size, **kw):
    x, y = xy
    for p, f in runs(text, size):
        d.text((x, y), p, font=f, **kw); x += d.textlength(p, font=f)


def caption_line(parts, size):
    widths = [textlen(p, size) for p, _ in parts]; tw = sum(widths)
    im = Image.new("RGBA", (W, size + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = (W - tw) / 2
    for (p, hi), pw in zip(parts, widths):
        draw_text(d, (x, 6), p, size, fill=YEL if hi else (255, 255, 255), stroke_width=6, stroke_fill=(0, 0, 0))
        x += pw
    return im, tw


def caption_img(text, size=64):
    """66 px Kendra captions; wrap to two lines rather than shrinking (formats/sahayata_kendra.md)"""
    def parts_of(t):
        out = []; hi = False
        for seg in t.split("*"):
            if seg:
                out.append((seg, hi))
            hi = not hi
        return out
    im, tw = caption_line(parts_of(text), size)
    if tw <= W - 60:
        return im
    words = text.split(" "); best = None
    for k in range(1, len(words)):
        a, b = " ".join(words[:k]), " ".join(words[k:])
        if a.count("*") % 2:                              # keep a highlight inside one line
            a += "*"; b = "*" + b
        la, wa = caption_line(parts_of(a), size); lb, wb = caption_line(parts_of(b), size)
        if best is None or max(wa, wb) < best[0]:
            best = (max(wa, wb), la, lb)
    _, la, lb = best
    out = Image.new("RGBA", (W, la.height + lb.height - 14), (0, 0, 0, 0))
    out.alpha_composite(la, (0, 0)); out.alpha_composite(lb, (0, la.height - 14))
    return out


def bug_img():
    f = ImageFont.truetype(BUNGEE, 30); d0 = ImageDraw.Draw(Image.new("L", (1, 1)))
    w = int(d0.textlength("DOORDHAN", font=f)) + 16
    im = Image.new("RGBA", (w, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((8, 6), "DOORDHAN", font=f, fill=(255, 255, 255, 215), stroke_width=3, stroke_fill=(20, 20, 20, 200))
    return im


def in_split(v):
    return v < 3.05 or v >= 87.50


def overlays():
    """(t_in, t_out, x, y, rgba ndarray, pop) in REEL time"""
    ov = []
    ends = [c[0] for c in CAPS[1:]] + [END_V]
    for (a, t), b in zip(CAPS, ends):
        im = caption_img(t)
        y = SPLIT - im.height // 2 - 4 if in_split(a) else 1000
        ov.append((a + V0, min(b, a + 3.0) + V0, 0, y, np.asarray(im), True))
    bg = bug_img()
    ov.append((0, END_V + TAIL + V0 + 1, W - 20 - bg.width, 36, np.asarray(bg), False))
    return ov


def burn(base, out, ov):
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", base, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", out],
                           stdin=subprocess.PIPE)
    k = 0; loop_from = (END_V + V0)
    while True:
        buf = dec.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            break
        t = k / FPS; fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32)
        for a, b, x, y, rgba, pop in ov:
            if t >= loop_from and pop:                    # the loop tail is the clean opening frame: no captions
                continue
            if a <= t < b:
                img = rgba; age = t - a
                if pop and age < 0.12:
                    s = 0.85 + 0.15 * age / 0.12
                    pil = Image.fromarray(rgba); pil = pil.resize((max(1, int(pil.width * s)), max(1, int(pil.height * s))))
                    img = np.asarray(pil); x2 = x + (rgba.shape[1] - img.shape[1]) // 2; y2 = y + (rgba.shape[0] - img.shape[0]) // 2
                else:
                    x2, y2 = x, y
                sx, sy = max(0, -x2), max(0, -y2); x2, y2 = max(0, x2), max(0, y2)
                img = img[sy:, sx:]
                h_, w_ = img.shape[:2]; h_ = min(h_, H - y2); w_ = min(w_, W - x2)
                al = img[:h_, :w_, 3:4].astype(np.float32) / 255
                fr[y2:y2 + h_, x2:x2 + w_] = fr[y2:y2 + h_, x2:x2 + w_] * (1 - al) + img[:h_, :w_, :3] * al
        enc.stdin.write(fr.astype(np.uint8).tobytes()); k += 1
    enc.stdin.close(); enc.wait(); dec.wait()
    print(f"  burned {k} frames ({k / FPS:.2f} s)")


def mix(total, out_wav):
    """voice + a quiet office fan + effects on stamps, pops, snaps and whips (no music: the voice carries it)"""
    A = f"{ROOT}/assets/audio"
    ms = lambda v: int(round((v + V0) * 1000))
    fx = [("sfx_pop.wav", 0.20, 0.18), ("sfx_stamp.wav", 2.00, 0.32),                                        # hook
          ("sfx_thud.wav", 4.65, 0.22), ("sfx_thud.wav", 5.45, 0.22), ("sfx_stamp.wav", 6.35, 0.30),           # chart
          ("sfx_pop.wav", 8.00, 0.2), ("sfx_pop.wav", 8.80, 0.2), ("sfx_pop.wav", 9.60, 0.2),                   # gst tabs
          ("sfx_pop.wav", 11.40, 0.2), ("sfx_pop.wav", 12.20, 0.2), ("sfx_whoosh.wav", 14.40, 0.14),
          ("sfx_stamp.wav", 18.00, 0.32), ("sfx_pop.wav", 21.05, 0.18),                                         # cert
          ("sfx_stamp.wav", 31.65, 0.30), ("sfx_stamp.wav", 33.20, 0.34), ("sfx_whoosh.wav", 33.65, 0.14),      # hack
          ("sfx_whoosh.wav", 34.08, 0.12),                                                                      # Billu snap
          ("sfx_pop.wav", 35.40, 0.2), ("sfx_whoosh.wav", 38.20, 0.12), ("sfx_whoosh.wav", 39.15, 0.14),        # rob
          ("sfx_scratch.wav", 40.45, 0.18), ("sfx_whoosh.wav", 41.20, 0.10), ("sfx_whoosh.wav", 42.80, 0.14),   # T2
          ("sfx_ding.wav", 46.95, 0.16), ("sfx_thud.wav", 50.45, 0.22),                                          # quar
          ("sfx_stamp.wav", 54.30, 0.30), ("sfx_stamp.wav", 54.80, 0.30),                                       # audit
          ("sfx_whoosh.wav", 56.76, 0.12),                                                                      # T3 snap
          ("sfx_stamp.wav", 61.40, 0.32),                                                                       # unaffected
          ("sfx_whoosh.wav", 67.26, 0.10), ("sfx_whoosh.wav", 67.90, 0.14),                                     # T4 snap, whip
          ("sfx_thud.wav", 70.40, 0.2),                                                                          # padlock splits
          ("sfx_stamp.wav", 74.90, 0.32), ("sfx_stamp.wav", 76.40, 0.28), ("sfx_stamp.wav", 76.80, 0.28),
          ("sfx_stamp.wav", 77.20, 0.28), ("sfx_pop.wav", 78.30, 0.2), ("sfx_pop.wav", 79.65, 0.2),
          ("sfx_thud.wav", 81.65, 0.24),                                                                         # BANKRUPT
          ("sfx_ding.wav", 85.90, 0.14)]
    inputs = ["-i", VOICE, "-stream_loop", "-1", "-i", f"{A}/ambience/fan_loop.wav"]
    for f, _, _ in fx:
        inputs += ["-i", f"{A}/{f}"]
    fc = (f"[0:a]aresample=48000,adelay={int(V0 * 1000)}|{int(V0 * 1000)},volume=1.0[vo];"
          f"[1:a]aresample=48000,atrim=0:{total},volume=0.05[room];")
    labels = ["[vo]", "[room]"]
    for k, (f, v, vol) in enumerate(fx):
        fc += f"[{2 + k}:a]aresample=48000,volume={vol},adelay={ms(v)}|{ms(v)}[x{k}];"; labels.append(f"[x{k}]")
    fc += (f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{total:.3f},"
           f"pan=mono|c0=0.5*c0+0.5*c1[a]")
    raw = out_wav.replace(".wav", "_raw.wav")
    run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", fc, "-map", "[a]", "-ar", "48000", "-ac", "2", raw])
    sys.path.insert(0, f"{ROOT}/pipeline"); from common import loudness
    lufs, _ = loudness(raw); gain = -14.0 - lufs
    run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", f"volume={gain:.2f}dB,alimiter=limit=0.79:level=false",
         "-ar", "48000", "-ac", "2", out_wav])
    print(f"  mix {lufs:.1f} LUFS -> gain {gain:+.1f} dB")


def write_manifest(total, final):
    """the QC gate's manifest: lines at speech_map's pauses on the cut (reel time = v + V0)"""
    L = [("L1", 0.05, 2.65, None), ("L2", 3.20, 38.90, None), ("L3", 39.30, 42.90, 39.30), ("L4", 43.40, 51.30, None),
         ("L5", 51.80, 58.40, 51.80), ("L6", 58.90, 63.40, None), ("L7", 63.60, 68.00, 63.60), ("L8", 68.50, 87.00, None),
         ("L9", 87.50, 91.40, 87.50)]
    lines = []
    for lid, a, b, cut in L:
        shots = [x for x in SHOTS if x[3]["name"] in LINE_SHOTS.get(lid, [])]
        ln = {"id": lid, "speaker": "pandey", "start": round(a + V0, 3), "end": round(b + V0, 3),
              "source": f"{WREL}/build/dialogue_src.wav",
              "segments": [[round(max(x[0], a) + V0, 3), round(min(x[1], b) + V0, 3)] for x in shots]}
        if shots:
            ln["clips"] = [os.path.relpath(x[3]["src"], ROOT) for x in shots]
            ln["clip_spans"] = [[round(max(x[0], a) - x[3]["off"], 3), round(min(x[1], b) - x[3]["off"], 3)] for x in shots]
        if cut is not None:
            ln["cut_in"] = round(cut + V0, 3)
        lines.append(ln)
    M = {"slug": SLUG, "format": "sahayata_kendra", "final": os.path.relpath(final, ROOT), "script": f"registry/scripts/{SLUG}.json",
         "characters": {"pandey": "assets/characters/pandey_sheet_v2.jpg"}, "prefinish": f"{WREL}/edit_raw.mp4",
         "dialogue_stem": f"{WREL}/build/dialogue.wav", "length": {"min": 20, "max": 95, "expected": total},
         "loudness": {"target": -14}, "fps": FPS, "repairs_file": f"{WREL}/qc_repairs.json",
         "rebuild": f"pipeline/qcpy {WREL}/build.py", "lines": lines}
    json.dump(M, open(f"{HERE}/qc_manifest.json", "w"), indent=1)


def main():
    total = round(END_V + TAIL + V0, 3)
    print(f"reel {total:.2f} s  (voice starts {V0} s in)")
    talk = 0
    for s in SHOTS:
        d = s[1] - s[0]; talk += d if s[3]["name"] in TALK else 0
        extra = f"src {s[0] - s[3]['off']:.2f}-{s[1] - s[3]['off']:.2f}" if "off" in s[3] else ""
        print(f"  {s[0] + V0:6.2f}-{s[1] + V0:6.2f}  {d:5.2f}s  {s[2]:5s} {s[3]['name']:8s} {extra}")
    print(f"talking share {talk / total:.0%} (Pandey on screen, lip-synced; the split counts in full)")
    if os.environ.get("PLAN_ONLY"):
        return
    seam_png()
    sys.path.insert(0, f"{ROOT}/pipeline"); import buildkit
    parts = buildkit.render_all(SHOTS, render, lambda i, s: f"{TMP}/s{i:02d}_{s[3]['name']}.mp4",
                                [handheld, grade, sway, snap, cam_at, decode, render_live],
                                {i: [f"{TMP}/seam.png"] for i, s in enumerate(SHOTS) if s[2] == "split"})
    with open(f"{TMP}/concat.txt", "w") as f:
        f.writelines(f"file '{p}'\n" for p in parts)
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{TMP}/concat.txt", "-c", "copy", f"{TMP}/base.mp4"])
    burn(f"{TMP}/base.mp4", f"{TMP}/burned.mp4", overlays())
    mix(total, f"{TMP}/mix.wav")
    os.makedirs(f"{ROOT}/outputs/{SLUG}", exist_ok=True)
    out = os.environ.get("OUT") or f"{ROOT}/outputs/{SLUG}/{SLUG}.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{TMP}/base.mp4", "-i", f"{TMP}/mix.wav", "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", f"{HERE}/edit_raw.mp4"])
    run(["ffmpeg", "-v", "error", "-y", "-i", VOICE, "-ar", "48000", "-ac", "1", f"{TMP}/dialogue_src.wav"])
    run(["ffmpeg", "-v", "error", "-y", "-i", VOICE, "-af", f"adelay={int(V0 * 1000)},apad,atrim=0:{total}",
         "-ar", "48000", "-ac", "1", f"{TMP}/dialogue.wav"])
    phone = out.replace(".mp4", "_phone.mp4")
    written = buildkit.encode_finals(f"{TMP}/burned.mp4", f"{TMP}/mix.wav", out, phone, FPS)
    write_manifest(total, out)
    print("wrote", " and ".join(written))


if __name__ == "__main__":
    main()
