#!/usr/bin/env python3
"""nana01 edit: the Instagram-creator format (first episode). Shots -> base video -> captions/labels -> audio mix.

Times are in VOICE time (v, seconds into work/nana/voice/cut.wav, Rashmiji v4_2); the reel runs v + V0.
  python3 work/nana/build.py            full build -> work/nana/edit_raw.mp4 (pre-finish) and outputs/nana01/...
  PLAN_ONLY=1 python3 work/nana/build.py   prints the timeline and talking share
  DRAFT=1 python3 work/nana/build.py       a fast look-only <stem>_draft.mp4 between fixes (the QC gate needs a normal build)
"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
SLUG = os.path.basename(HERE)       # the episode is the folder this copy sits in: work/<slug>/build.py
WREL = os.path.relpath(HERE, ROOT)  # work/<slug>
W, H, FPS = 720, 1280, 30
V0 = 0.15                      # voice starts this far into the reel (a lead before the first word)
CLIPS = f"{HERE}/clips"; VID = f"{HERE}/vid"; KF = f"{HERE}/kf"; TMP = f"{HERE}/build"; os.makedirs(TMP, exist_ok=True)
FONT = f"{ROOT}/assets/fonts/Baloo2-Latin-ExtraBold.ttf"
DEVA = f"{ROOT}/assets/fonts/Baloo2-Deva-ExtraBold.ttf"
ATC_OPEN = 8.35                # atc2 source time where the reel starts (Nana close-up in shades); the close plays ATC_CLOSE -> ATC_OPEN (loop)
ATC_CLOSE = 6.75
END_V = 39.20                  # voice time where the close starts (last word ends 39.15)

# ---- shots: (v_in, v_out, kind, args). Talking shots: src = v - offset (+ lip-sync shift measured by lipsync_lag)
SHOTS = [
    (-V0, 2.35, "band", dict(src=f"{CLIPS}/atc2_short.mp4", ss=ATC_OPEN - 0.0, box=(0, 290, 584, 519), name="atc_open")),
    (2.35, 5.95, "talk", dict(src=f"{VID}/T1.mp4", off=2.30 - 0.5 + 0.08, name="T1")),           # syncnet -80..-120 -> -0.08 s
    (5.95, 7.90, "still", dict(img=f"{KF}/car2.png", zoom=(1.0, 1.12), name="car")),
    (7.90, 10.62, "tv", dict(src=f"{TMP}/TVc.mp4", ss=0.05, name="TV")),
    (10.62, 12.95, "band", dict(src=f"{CLIPS}/nana_lallantop.mp4", ss=168.0, box=(528, 0, 864, 1080), kb=1.06, name="earth")),
    (12.95, 14.70, "band", dict(src=f"{CLIPS}/nana_lallantop.mp4", ss=174.0, box=(528, 0, 864, 1080), kb=1.05, name="farmer")),
    (14.70, 18.30, "talk", dict(src=f"{VID}/T3b.mp4", off=14.80 - 0.5, name="T3")),               # PASS -40 ms
    (18.30, 19.75, "band", dict(src=f"{CLIPS}/nana_lallantop.mp4", ss=144.0, box=(40, 140, 1040, 830), kb=1.05, name="widow")),
    (19.75, 21.30, "band", dict(src=f"{CLIPS}/nana_lallantop.mp4", ss=158.0, box=(40, 140, 1040, 830), kb=1.05, name="cheque")),
    (21.30, 22.50, "band", dict(src=f"{CLIPS}/nana_lallantop.mp4", ss=152.0, box=(40, 140, 1040, 830), kb=1.05, name="bigcheque")),
    (22.80, 25.35, "band", dict(src=f"{CLIPS}/naam_storydotcom.mp4", ss=120.5, box=(0, 300, 608, 480), kb=1.08, name="farmers")),
    (25.35, 26.95, "band", dict(src=f"{CLIPS}/naam_storydotcom.mp4", ss=72.5, box=(0, 230, 608, 560), kb=1.06, name="stage")),
    (26.95, 28.55, "full", dict(src=f"{CLIPS}/naam_storydotcom.mp4", ss=112.5, box=(0, 140, 608, 940), kb=1.06, name="logo")),
    (28.55, 30.55, "band", dict(src=f"{CLIPS}/naam_storydotcom.mp4", ss=85.0, box=(0, 395, 608, 340), kb=1.06, name="lake_people")),
    (30.55, 32.58, "band", dict(src=f"{CLIPS}/naam_storydotcom.mp4", ss=137.0, box=(0, 790, 608, 270), kb=1.08, name="reservoir")),
    (32.58, 35.90, "talk", dict(src=f"{VID}/T5.mp4", off=32.70 - 0.5 - 0.10, name="T5a")),        # +40..+80 -> +0.10 s
    (35.90, END_V, "talk", dict(src=f"{VID}/T5.mp4", off=32.70 - 0.5 - 0.10, punch=1.20, name="T5b")),
    (END_V, END_V + ATC_OPEN - ATC_CLOSE, "band", dict(src=f"{CLIPS}/atc2_short.mp4", ss=ATC_CLOSE, box=(0, 290, 584, 519), name="atc_close")),
]
TALK = {"T1", "T3", "T5a", "T5b"}
LINE_SHOTS = {"L1": ["T1"], "L3": ["T3"], "L6": ["T5a", "T5b"]}
REPAIRS = f"{HERE}/qc_repairs.json"
if os.path.exists(REPAIRS):
    for line, rp in json.load(open(REPAIRS)).items():
        for v_in, v_out, kind, a in SHOTS:
            if a["name"] in LINE_SHOTS.get(line, []) and "src_shift_s" in rp:
                a["off"] -= rp["src_shift_s"]          # moves the clip's source start by +src_shift_s

# ---- captions (Roman Hinglish groups from Scribe's word times on v4_2); * marks the highlighted words
CAPS = [(0.26, 1.30, "*2015* mein"), (1.34, 2.36, "Nana Patekar ki"), (2.38, 3.70, "*Ab Tak Chhappan 2*"),
        (3.70, 4.38, "release hui thi"), (4.40, 5.10, "unhone ek *car*"), (5.14, 5.98, "khareedne ke liye"),
        (6.04, 6.86, "*₹1.5 crore*"), (6.88, 7.90, "jod rakhe the"), (7.92, 8.90, "lekin phir..."),
        (8.92, 10.60, "TV par ek *khabar* dekhi"), (10.64, 11.40, "ek kisan ne"), (11.42, 12.92, "aatmahatya kar li thi"),
        (12.92, 13.56, "uska parivar"), (13.58, 14.86, "mushkil mein tha"), (14.90, 15.94, "Nana ne car ka plan"),
        (15.98, 16.72, "*chhod diya*"), (16.74, 17.40, "aur woh paise"), (17.42, 18.56, "kisanon ke parivaron ki"),
        (18.60, 19.74, "madad mein laga diye"), (19.76, 20.72, "kai parivaron ko"), (20.74, 22.00, "*15-15 hazaar* ke"),
        (22.00, 22.60, "cheques mile"), (22.88, 23.76, "lekin madad"), (23.80, 24.54, "sirf cheques tak"),
        (24.56, 25.36, "*nahin ruki*"), (25.40, 26.90, "Makarand Anaspure ke saath"), (26.94, 28.08, "unhone *NAAM Foundation*"),
        (28.14, 28.66, "shuru ki"), (28.68, 30.00, "jo kisanon ke parivaron"), (30.02, 30.52, "ki madad"),
        (30.54, 31.56, "aur *paani* bachane ka"), (31.58, 32.68, "kaam karti hai"), (32.70, 33.56, "hum apni *wealth*"),
        (33.58, 34.50, "usse naapte hain"), (34.52, 35.88, "jo humare paas hai"), (35.90, 36.66, "kabhi usse bhi"),
        (36.68, 37.85, "naapkar dekhein"), (37.86, 38.52, "jo hum *peeche*"), (38.54, 39.30, "*chhod jaate hain?*")]
# labels: (v_in, v_out, text, kind)
LABELS = [(-V0, 2.35, "Ab Tak Chhappan 2  (2015)", "film"),
          (6.04, 7.90, "₹1.5 CRORE", "slam"),
          (7.90, 10.62, "RECREATION  ·  2015", "tag"),
          (20.74, 22.50, "₹15,000 per family", "slam"),
          (END_V, END_V + ATC_OPEN - ATC_CLOSE, "Ab Tak Chhappan 2  (2015)", "film")]

# ---- the silent chai beat (Akhilesh, 2026-10-09: "while she's sipping tea, her voice is there"): the voice pauses
# GAP s at GAP_AT (inside the pause after "cheques mile") and she sips in silence. Everything after moves by GAP.
GAP_AT, GAP = 22.65, 1.20


def S(v):
    return v + GAP if v >= GAP_AT else v


for _i, (_a, _b, _k, _d) in enumerate(SHOTS):
    if _k == "talk" and _a >= GAP_AT:
        _d["off"] += GAP                                   # same source frames under the shifted voice
    SHOTS[_i] = (S(_a), S(_b), _k, _d)
SHOTS.insert([x[0] for x in SHOTS].index(S(22.80)),
             (22.50, 22.80 + GAP, "talk", dict(src=f"{VID}/chai.mp4", off=22.50 - 1.10, name="chai")))  # silent: no voice
CAPS = [(S(a), S(b), t) for a, b, t in CAPS]
LABELS = [(S(a), S(b), t, k) for a, b, t, k in LABELS]
END_V = S(END_V)

CREDITS = {"nana_lallantop.mp4": "Footage: Naam Foundation via The Lallantop",
           "naam_storydotcom.mp4": "Footage: Story Dot Com / Naam Foundation"}
for _v_in, _v_out, _k, _a in SHOTS:                      # a credit on every archive shot, and only there
    _c = CREDITS.get(os.path.basename(_a.get("src", "")))
    if _c:
        LABELS.append((_v_in, _v_out, _c, "credit"))
YEL = (255, 214, 10)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"FAILED: {' '.join(cmd)[:300]}\n{r.stderr[-1500:]}")
    return r


def grade(grain=3):
    # clean modern phone look: a touch of contrast and warmth, fine light grain
    return f"eq=contrast=1.04:saturation=1.05,colorbalance=rs=0.02:bs=-0.02,noise=alls={grain}:allf=t"


def handheld(dur, seed=0.0, zoom=1.07, punch=1.0):
    z = zoom * punch
    cw, ch = f"trunc(iw/{z}/2)*2", f"trunc(ih/{z}/2)*2"
    x = f"(iw-ow)/2+(iw-ow)/2*0.55*(0.6*sin(2*PI*(t+{seed})*0.31)+0.3*sin(2*PI*(t+{seed})*1.07+1)+0.1*sin(2*PI*t*2.9))"
    y = f"(ih-oh)*0.42+(ih-oh)/2*0.5*(0.6*sin(2*PI*(t+{seed})*0.23+2)+0.3*sin(2*PI*(t+{seed})*0.93)+0.1*sin(2*PI*t*2.6+0.5))"
    return (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
            f"rotate='0.006*sin(2*PI*(t+{seed})*0.37)':fillcolor=none,crop=w={cw}:h={ch}:x='{x}':y='{y}',scale={W}:{H}")


def render(i, shot):
    v_in, v_out, kind, a = shot
    nf = int(round((v_out + V0) * FPS)) - int(round((v_in + V0) * FPS))     # frame-exact: no drift across the concat
    dur = round(nf / FPS, 4)
    out = f"{TMP}/s{i:02d}_{a['name']}.mp4"
    enc = ["-r", str(FPS), "-frames:v", str(nf), "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p", "-an", out]
    if kind == "talk":
        ss = v_in - a["off"]
        vf = handheld(dur, seed=i * 1.7, punch=a.get("punch", 1.0)) + "," + grade(1)
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-t", f"{dur + 0.3:.3f}", "-i", a["src"], "-vf", vf] + enc)
    elif kind == "still":
        z0, z1 = a["zoom"]; n = int(round(dur * FPS))
        vf = (f"scale=1440:2560,zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},"
              + grade())
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", a["img"], "-vf", vf] + enc)
    elif kind == "tv":
        vf = handheld(dur, seed=3.3, zoom=1.03) + "," + grade()
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a['ss']:.3f}", "-t", f"{dur + 0.3:.3f}", "-i", a["src"], "-vf", vf] + enc)
    elif kind in ("band", "full"):
        bx, by, bw, bh = a["box"]; kb = a.get("kb", 1.0)
        if kind == "full":
            vf = (f"fps={FPS},crop={bw}:{bh}:{bx}:{by},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                  f"zoompan=z='1+({kb}-1)*on/{int(dur * FPS)}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},"
                  + grade())
            run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a['ss']:.3f}", "-t", f"{dur + 0.3:.3f}", "-i", a["src"], "-vf", vf] + enc)
        else:
            band_h = int(round(W * bh / bw / 2) * 2)
            band_y = int(max(150, 0.43 * H - band_h / 2))
            fc = (f"[0:v]fps={FPS},crop={bw}:{bh}:{bx}:{by},split[a][b];"
                  f"[b]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},gblur=sigma=28,eq=brightness=-0.12:saturation=0.8[bg];"
                  f"[a]scale={W}:{band_h},zoompan=z='1+({kb}-1)*on/{int(dur * FPS)}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{band_h}:fps={FPS}[fg];"
                  f"[bg][fg]overlay=0:{band_y},{grade()}[v]")
            run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a['ss']:.3f}", "-t", f"{dur + 0.3:.3f}", "-i", a["src"],
                 "-filter_complex", fc, "-map", "[v]"] + enc)
    return out


def tv_composite():
    """key the 2015 bulletin into the blue TV screen of the Wan clip (locked-off camera)"""
    src = f"{VID}/TV.mp4"; out = f"{TMP}/TVc.mp4"
    w, h = [int(x) for x in run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                                 "-of", "csv=p=0", src]).stdout.strip().split(",")]
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", "30",
                            "-i", "-", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    bul = Image.open(f"{HERE}/gfx/tv_bulletin.png").convert("RGB"); box = None; n = 0
    while True:
        buf = dec.stdout.read(w * h * 3)
        if len(buf) < w * h * 3:
            break
        f = np.frombuffer(buf, np.uint8).reshape(h, w, 3).astype(np.float32)
        r, g, b = f[..., 0], f[..., 1], f[..., 2]
        m = ((b > 140) & (b > 2.2 * r) & (b > 1.9 * g)).astype(np.float32)
        if box is None:
            from scipy import ndimage
            lab, nl = ndimage.label(m > 0); sizes = ndimage.sum(m > 0, lab, range(1, nl + 1))
            big = lab == (int(np.argmax(sizes)) + 1); ys, xs = np.where(big)
            box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
        x0, y0, x1, y1 = box
        inside = np.zeros_like(m); inside[y0:y1, x0:x1] = 1; m = m * inside
        x0, y0, x1, y1 = box
        tile = np.asarray(bul.resize((x1 - x0, y1 - y0), Image.LANCZOS)).astype(np.float32) * 0.92
        full = f.copy(); full[y0:y1, x0:x1] = tile
        ms = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32)[..., None] / 255
        o = f * (1 - ms) + full * ms
        enc.stdin.write(np.clip(o, 0, 255).astype(np.uint8).tobytes()); n += 1
    enc.stdin.close(); enc.wait(); dec.wait()
    print(f"  TV composite: {n} frames, screen box {box}")


# ---- text overlays
def font(size):
    return ImageFont.truetype(FONT, size)


def runs(text, size):
    """split text into (piece, font) runs: the rupee sign comes from the Devanagari font"""
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


def caption_img(text, size=60):
    parts = []; hi = False
    for i, seg in enumerate(text.split("*")):
        if seg:
            parts.append((seg, hi))
        hi = not hi
    widths = [textlen(p, size) for p, _ in parts]
    tw = sum(widths); scale = min(1.0, (W - 60) / tw)
    if scale < 1:
        return caption_img(text, int(size * scale))
    im = Image.new("RGBA", (W, size + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x = (W - tw) / 2
    for (p, hi), pw in zip(parts, widths):
        draw_text(d, (x, 10), p, size, fill=YEL if hi else (255, 255, 255), stroke_width=6, stroke_fill=(0, 0, 0))
        x += pw
    return im


def label_img(text, kind):
    if kind == "slam":
        tw = textlen(text, 78)
        im = Image.new("RGBA", (W, 130), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        pad = 26; x0 = (W - tw) / 2 - pad
        d.rounded_rectangle((x0, 12, x0 + tw + 2 * pad, 118), 18, fill=YEL)
        draw_text(d, ((W - tw) / 2, 10), text, 78, fill=(15, 15, 15))
        return im
    size = {"film": 30, "tag": 26, "credit": 22}[kind]
    f = font(size); d = ImageDraw.Draw(Image.new("RGBA", (1, 1))); tw = d.textlength(text, font=f)
    im = Image.new("RGBA", (int(tw) + 36, size + 26), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, im.width - 1, im.height - 1), 12, fill=(0, 0, 0, 245 if kind == "film" else 165))
    d.text((18, 6), text, font=f, fill=(255, 255, 255))
    return im


def overlays():
    """list of (t_in, t_out, x, y, rgba ndarray, pop) in REEL time"""
    ov = []
    for a, b, t in CAPS:
        im = caption_img(t); ov.append((a + V0, b + V0, 0, 985, np.asarray(im), True))
    for a, b, t, k in LABELS:
        im = label_img(t, k)
        if k == "slam":
            xy = (0, 240)
        elif k == "film":
            xy = ((W - im.width) // 2, int(0.43 * H + 0.5 * W * 519 / 584) - im.height - 14)   # over the source watermark
        elif k == "tag":
            xy = (24, 120)
        else:
            xy = (24, 120)
        ov.append((max(0, a + V0), b + V0, xy[0], xy[1], np.asarray(im), k == "slam"))
    return ov


def burn(base, out, ov):
    dur = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", base]).stdout)
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", base, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", out],
                           stdin=subprocess.PIPE)
    k = 0
    while True:
        buf = dec.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            break
        t = k / FPS; fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32)
        for a, b, x, y, rgba, pop in ov:
            if a <= t < b:
                img = rgba
                age = t - a
                if pop and age < 0.12:          # quick pop-in
                    s = 0.85 + 0.15 * age / 0.12
                    pil = Image.fromarray(rgba); pil = pil.resize((max(1, int(pil.width * s)), max(1, int(pil.height * s))))
                    img = np.asarray(pil); x2 = x + (rgba.shape[1] - img.shape[1]) // 2; y2 = y + (rgba.shape[0] - img.shape[0]) // 2
                else:
                    x2, y2 = x, y
                h_, w_ = img.shape[:2]; h_ = min(h_, H - y2); w_ = min(w_, W - x2)
                al = img[:h_, :w_, 3:4].astype(np.float32) / 255
                fr[y2:y2 + h_, x2:x2 + w_] = fr[y2:y2 + h_, x2:x2 + w_] * (1 - al) + img[:h_, :w_, :3] * al
        enc.stdin.write(fr.astype(np.uint8).tobytes()); k += 1
    enc.stdin.close(); enc.wait(); dec.wait()
    print(f"  burned {k} frames ({k / FPS:.2f} s of {dur:.2f})")


def voice_prep():
    """cut.wav with one fix: the softly swallowed "मिले" (v 22.24-22.48) lifted 6 dB with raised-cosine ramps"""
    import wave
    src, out = f"{HERE}/voice/cut.wav", f"{TMP}/voice_fixed.wav"
    w = wave.open(src); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32); w.close()
    g = np.ones_like(x); a, b, r = int(22.24 * sr), int(22.48 * sr), int(0.03 * sr); lift = 10 ** (6 / 20)
    ramp = 1 + (lift - 1) * (0.5 - 0.5 * np.cos(np.linspace(0, np.pi, r)))
    g[a - r:a] = ramp; g[a:b] = lift; g[b:b + r] = ramp[::-1]
    y = np.clip(x * g, -32768, 32767).astype(np.int16)
    k = int(GAP_AT * sr); y = np.concatenate([y[:k], np.zeros(int(GAP * sr), np.int16), y[k:]])    # the silent beat
    o = wave.open(out, "wb"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr); o.writeframes(y.tobytes()); o.close()
    return out


def mix(total, out_wav, music_free=True):
    """voice + the film clip's own sound at both ends (the loop) + room tone + a few soft effects"""
    A = f"{ROOT}/assets/audio"
    voice = voice_prep()
    inputs = ["-i", voice,
              "-ss", f"{ATC_OPEN}", "-t", f"{2.35 + V0:.3f}", "-i", f"{CLIPS}/atc2_short.mp4",
              "-ss", f"{ATC_CLOSE}", "-t", f"{ATC_OPEN - ATC_CLOSE:.3f}", "-i", f"{CLIPS}/atc2_short.mp4",
              "-stream_loop", "-1", "-i", f"{A}/ambience/road_distant_loop.wav",
              "-stream_loop", "-1", "-i", f"{A}/ambience/fan_loop.wav",
              "-i", f"{A}/sfx_whoosh.wav", "-i", f"{A}/sfx_thud.wav", "-i", f"{A}/sfx_whoosh.wav", "-i", f"{A}/sfx_thud.wav"]
    ms = lambda v: int(round((v + V0) * 1000))
    fc = (f"[0:a]aresample=48000,adelay={int(V0 * 1000)}|{int(V0 * 1000)},volume=1.0[vo];"
          f"[1:a]aresample=48000,volume=0.22[fo];"
          f"[2:a]aresample=48000,volume=0.22,adelay={ms(END_V)}|{ms(END_V)}[fc];"
          f"[3:a]aresample=48000,atrim=0:{total},volume=0.05[room];"
          f"[4:a]aresample=48000,atrim=0:{10.62 - 7.90:.2f},volume=0.10,afade=t=in:d=0.2,afade=t=out:st={10.62 - 7.90 - 0.25:.2f}:d=0.25,adelay={ms(7.90)}|{ms(7.90)}[fan];"
          f"[5:a]aresample=48000,volume=0.18,adelay={ms(5.80)}|{ms(5.80)}[w1];"
          f"[6:a]aresample=48000,volume=0.22,adelay={ms(6.02)}|{ms(6.02)}[t1];"
          f"[7:a]aresample=48000,volume=0.14,adelay={ms(S(22.80) - 0.12)}|{ms(S(22.80) - 0.12)}[w2];"
          f"[8:a]aresample=48000,volume=0.2,adelay={ms(20.72)}|{ms(20.72)}[t2];"
          f"[vo][fo][fc][room][fan][w1][t1][w2][t2]amix=inputs=9:normalize=0:duration=longest,atrim=0:{total:.3f},"
          f"pan=mono|c0=0.5*c0+0.5*c1[a]")
    raw = out_wav.replace(".wav", "_raw.wav")
    run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", fc, "-map", "[a]", "-ar", "48000", "-ac", "2", raw])
    sys.path.insert(0, f"{ROOT}/pipeline"); from common import loudness
    lufs, _ = loudness(raw); gain = -14.0 - lufs                    # measure, then one gain and a true-peak limiter
    run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", f"volume={gain:.2f}dB,alimiter=limit=0.79:level=false",
         "-ar", "48000", "-ac", "2", out_wav])
    print(f"  mix {lufs:.1f} LUFS -> gain {gain:+.1f} dB")


def write_manifest(total, final):
    """the QC gate's manifest: lines at speech_map's pauses on cut.wav (reel time = v + V0)"""
    L = [("L1", 0.05, 10.20, None, []), ("L2", 10.60, 14.40, None, []),
         ("L3", 14.80, 22.65, 14.70, [[14.70, 18.30]]), ("L4", 22.85, 25.10, None, []),
         ("L5", 25.30, 32.45, None, []), ("L6", 32.70, 39.25, 32.58, [[32.58, 35.90], [35.90, END_V]])]
    L[0] = ("L1", 0.05, 10.20, None, [[2.35, 5.95]])
    L[5] = ("L6", 32.70, 39.25, 32.58, [[32.58, 35.90], [35.90, 39.20]])
    L = [(i, S(a), S(b), None if c is None else S(c), [[S(x), S(y)] for x, y in g]) for i, a, b, c, g in L]
    lines = []
    for lid, a, b, cut, segs in L:
        ln = {"id": lid, "speaker": "rashmi", "start": round(a + V0, 3), "end": round(b + V0, 3),
              "source": f"{WREL}/build/voice_fixed.wav", "segments": [[round(x + V0, 3), round(y + V0, 3)] for x, y in segs]}
        if cut is not None:
            ln["cut_in"] = round(cut + V0, 3)
        lines.append(ln)
    M = {"slug": SLUG, "format": "creator", "final": os.path.relpath(final, ROOT), "script": f"registry/scripts/{SLUG}.json",
         "characters": {"rashmi": "assets/characters/rashmi_e10_master.jpg"}, "prefinish": f"{WREL}/edit_raw.mp4",
         "dialogue_stem": f"{WREL}/build/dialogue.wav", "length": {"min": 20, "max": 45, "expected": total},
         "loudness": {"target": -14}, "fps": FPS, "repairs_file": f"{WREL}/qc_repairs.json",
         "rebuild": f"pipeline/qcpy {WREL}/build.py", "lines": lines}
    json.dump(M, open(f"{HERE}/qc_manifest.json", "w"), indent=1)


def main():
    total = round(END_V + ATC_OPEN - ATC_CLOSE + V0, 3)
    print(f"reel {total:.2f} s  (voice starts {V0} s in)")
    talk = 0
    for s in SHOTS:
        d = s[1] - s[0]; talk += d if s[3]["name"] in TALK else 0
        extra = ""
        if s[2] == "talk":
            ss = s[0] - s[3]["off"]; extra = f"src {ss:.2f}-{ss + d:.2f}"
        print(f"  {s[0] + V0:6.2f}-{s[1] + V0:6.2f}  {d:4.2f}s  {s[2]:5s} {s[3]['name']:12s} {extra}")
    print(f"talking share {talk / total:.0%} (her on screen, lip-synced)")
    if os.environ.get("PLAN_ONLY"):
        return
    if not os.path.exists(f"{TMP}/TVc.mp4"):
        tv_composite()
    sys.path.insert(0, f"{ROOT}/pipeline"); import buildkit                      # parallel shots, cached when unchanged
    parts = buildkit.render_all(SHOTS, render, lambda i, s: f"{TMP}/s{i:02d}_{s[3]['name']}.mp4", [handheld, grade])
    with open(f"{TMP}/concat.txt", "w") as f:
        f.writelines(f"file '{p}'\n" for p in parts)
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{TMP}/concat.txt", "-c", "copy", f"{TMP}/base.mp4"])
    burn(f"{TMP}/base.mp4", f"{TMP}/burned.mp4", overlays())
    mix(total, f"{TMP}/mix.wav")
    os.makedirs(f"{ROOT}/outputs/{SLUG}", exist_ok=True)
    out = os.environ.get("OUT") or f"{ROOT}/outputs/{SLUG}/{SLUG}.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{TMP}/base.mp4", "-i", f"{TMP}/mix.wav", "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", f"{HERE}/edit_raw.mp4"])          # pre-finish, for lip sync
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{TMP}/voice_fixed.wav", "-af", f"adelay={int(V0 * 1000)},apad,atrim=0:{total}",
         "-ar", "48000", "-ac", "1", f"{TMP}/dialogue.wav"])
    phone = out.replace(".mp4", "_phone.mp4")
    written = buildkit.encode_finals(f"{TMP}/burned.mp4", f"{TMP}/mix.wav", out, phone, FPS)   # DRAFT=1: a fast look-only copy
    write_manifest(total, out)
    print("wrote", " and ".join(written))


if __name__ == "__main__":
    main()
