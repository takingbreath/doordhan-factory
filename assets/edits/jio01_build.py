# Template from jio01 (E11, 2026-10-19): copy to work/<slug>/build.py. Creator edit with a split-screen opening
# (collage on top, Rashmi below), local collage scenes, AI collage clips with logo labels, and a multi-clip QC manifest.
#!/usr/bin/env python3
"""jio01 edit: the creator format (Rashmi) with Vox-style collage graphics. Shots -> base video -> captions/labels -> mix.

Times are in VOICE time (v, seconds into work/jio01/voice/cut.wav, Rashmiji take C); the reel runs v + V0.
  python3 work/jio01/build.py              full build -> work/jio01/edit_raw.mp4 (pre-finish) and outputs/jio01/...
  PLAN_ONLY=1 python3 work/jio01/build.py  prints the timeline and talking share
Opening: split screen, the collage hook (real photos) on top, Rashmi on the bottom; full screen from "Dekho".
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
W, H, FPS = 720, 1280, 30
V0 = 0.15                      # voice starts this far into the reel (a lead before the first word)
VID = f"{HERE}/vid"; G = f"{HERE}/gfx"; VOX = f"{HERE}/vox"; TMP = f"{HERE}/build"; os.makedirs(TMP, exist_ok=True)
FONT = f"{ROOT}/assets/fonts/Baloo2-Latin-ExtraBold.ttf"
DEVA = f"{ROOT}/assets/fonts/Baloo2-Deva-ExtraBold.ttf"
BUNGEE = f"{ROOT}/assets/fonts/Bungee.ttf"
SPLIT = 640                    # the seam: hook above, Rashmi below
FACE_Y0 = 170                  # Rashmi's window in her 720x1280 clip for the split (forehead ~255, chin ~735)
END_V = 58.60                  # voice time where the loop tail starts (last word ends 58.46)
TAIL = 0.45                    # the loop tail: the opening split frame again
L7_DUR = 51.46 - 40.95         # the 10 s collage clip, slowed to fill L7
L5_SS = 0.55                   # L5 clip in-point: the AirFiber antenna lands on "difficult hai", the satellite on "Starlink"

# ---- shots: (v_in, v_out, kind, args). Talking shots: src = v - off (off = the segment's cut start - 0.5 s lead,
# plus any lip-sync shift: +0.10 moves the source 0.10 s earlier)
SHOTS = [
    (-V0, 5.12, "split", dict(src=f"{VID}/T1a_r2.mp4", off=0.00 - 0.5, hook_ss=0.0, name="T1a")),
    (5.12, 8.62, "split", dict(src=f"{VID}/T1b_r2.mp4", off=5.04 - 0.5 - 0.06, hook_ss=5.12 + V0, name="T1b")),   # past a blink at src 0.36-0.50; syncnet +80/+40 -> -0.06 s
    (8.62, 13.00, "talk", dict(src=f"{VID}/T2.mp4", off=8.78 - 0.5, name="T2")),
    (13.00, 18.95, "gfx", dict(src=f"{G}/rhp.mp4", ss=0.0, name="rhp")),
    (18.95, 21.95, "talk", dict(src=f"{VID}/T4.mp4", off=19.05 - 0.5 + 0.10, name="T4")),       # judge: -160..-120 ms -> +0.10
    (21.95, 28.62, "gfx", dict(src=f"{G}/chart.mp4", ss=0.0, name="chart")),
    (28.62, 36.08, "vox", dict(src=f"{VOX}/test_L5.mp4", ss=L5_SS, speed=1.0, name="L5")),
    (36.08, 40.95, "talk", dict(src=f"{VID}/T6_r2.mp4", off=36.16 - 0.5, name="T6")),
    (40.95, 51.46, "vox", dict(src=f"{VOX}/L7.mp4", ss=0.0, speed=10.0 / L7_DUR, name="L7")),
    (51.46, 53.20, "talk", dict(src=f"{VID}/T8a.mp4", off=51.56 - 0.5, name="T8a")),
    (53.20, 55.15, "gfx", dict(src=f"{G}/mobile.mp4", ss=0.0, name="mobile")),        # "Jio's existing mobile customers"
    (55.15, END_V, "talk", dict(src=f"{VID}/T8b.mp4", off=55.26 - 0.5, punch=1.18, name="T8b")),
    (END_V, END_V + TAIL, "split", dict(src=f"{VID}/T1a_r2.mp4", off=END_V - 0.35, hook_ss=0.0, freeze=True, name="loop")),
]
TALK = {"T1a", "T1b", "T2", "T4", "T6", "T8a", "T8b"}
LINE_SHOTS = {"L1": ["T1a", "T1b"], "L2": ["T2"], "L4": ["T4"], "L6": ["T6"], "L8": ["T8a", "T8b"]}
REPAIRS = f"{HERE}/qc_repairs.json"
if os.path.exists(REPAIRS):
    for line, rp in json.load(open(REPAIRS)).items():
        for v_in, v_out, kind, a in SHOTS:
            if a["name"] in LINE_SHOTS.get(line, []) and "src_shift_s" in rp:
                a["off"] -= rp["src_shift_s"]          # moves the clip's source start by +src_shift_s

# ---- captions (Roman Hinglish groups from Scribe's word times on take C); * marks the highlighted words
CAPS = [(0.16, 1.14, "Jio ke *IPO* se"), (1.18, 2.30, "bas kuch din pehle"), (2.50, 3.62, "*Elon Musk* aur *Ambani*"),
        (3.66, 4.85, "Twitter par lad rahe hain"), (5.12, 6.00, "lekin *Starlink*"), (6.24, 7.30, "Jio ke business ko"),
        (7.32, 8.60, "kitna *hurt* kar sakta hai?"),
        (8.84, 10.34, "Dekho, filhaal India mein"), (10.40, 11.70, "*Starlink* tumhara *Jio SIM*"),
        (11.72, 12.95, "replace nahi kar raha"), (13.08, 13.98, "phir bhi Jio ne"), (14.02, 14.96, "*IPO filing* mein"),
        (15.00, 16.30, "*satellite competition* ko"), (16.48, 17.54, "*risk* bola hai"),
        (17.56, 18.95, "To *risk kahan hai?*"),
        (19.16, 19.90, "Jio ki agli"), (19.92, 21.06, "*growth opportunity* hai"), (21.10, 21.95, "*home broadband*"),
        (22.12, 23.10, "Last financial year"), (23.32, 24.00, "yahan customers"), (24.06, 25.38, "*55%* badhe"),
        (25.40, 26.30, "Mobile broadband mein"), (26.32, 28.62, "growth sirf *5.6%* thi"),
        (28.66, 29.40, "Ab *AirFiber*"), (29.46, 30.62, "un gharon tak pahunchta hai"), (30.64, 31.68, "jahan *fibre connection*"),
        (31.70, 32.85, "dena *difficult* hai"), (32.88, 34.05, "aur unhi gharon mein"), (34.10, 34.68, "*Starlink* bhi"),
        (34.72, 36.18, "ek *option* ban sakta hai"),
        (36.22, 37.08, "Yaani *competition*"), (37.12, 37.95, "un customers ke liye"), (37.96, 38.60, "ho sakta hai"),
        (38.64, 39.50, "jo Jio ko"), (39.54, 40.95, "abhi *acquire* karne hain"),
        (41.10, 42.14, "Uske liye *Starlink* ko"), (42.16, 43.10, "*cheaper* hona hoga"), (43.22, 44.76, "aur *capacity* badhani hogi"),
        (44.80, 45.80, "agar wo kar paya"), (45.94, 47.10, "to Jio ko ye customers"), (47.12, 47.90, "jeetne ke liye"),
        (47.92, 48.70, "*better deals* deni"), (48.74, 49.56, "pad sakti hain"), (49.58, 50.39, "ya *zyada spend*"),
        (50.40, 51.55, "karna pad sakta hai"),
        (51.66, 52.76, "So *Musk* doesn't need to"), (52.78, 54.12, "take away Jio's existing"), (54.14, 55.15, "*mobile customers*"),
        (55.30, 56.90, "Wo Jio ki *future growth* ko"), (56.98, 57.70, "*less profitable*"), (57.72, 58.60, "bana sakte hain")]
# labels on the collage clips: (v_in, v_out, image key, x, y, rot)
LOGOS = [(33.00, 35.25, f"{G}/lab_airfiber.png", 520, 860, 0), (34.10, 35.25, f"{G}/lab_starlink.png", 590, 330, 0),
         (41.00, 49.60, f"{G}/lab_starlink.png", 150, 340, 0), (41.00, 49.60, f"{G}/lab_jio.png", 600, 615, 0)]
YEL = (255, 214, 10)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"FAILED: {' '.join(cmd)[:300]}\n{r.stderr[-1500:]}")
    return r


def grade(grain=3):
    # clean modern phone look: a touch of contrast and warmth, fine light grain
    return f"eq=contrast=1.04:saturation=1.05,colorbalance=rs=0.02:bs=-0.02,noise=alls={grain}:allf=t"


def handheld(dur, seed=0.0, zoom=1.07, punch=1.0, w=W, h=H):
    z = zoom * punch
    cw, ch = f"trunc(iw/{z}/2)*2", f"trunc(ih/{z}/2)*2"
    x = f"(iw-ow)/2+(iw-ow)/2*0.55*(0.6*sin(2*PI*(t+{seed})*0.31)+0.3*sin(2*PI*(t+{seed})*1.07+1)+0.1*sin(2*PI*t*2.9))"
    y = f"(ih-oh)*0.42+(ih-oh)/2*0.5*(0.6*sin(2*PI*(t+{seed})*0.23+2)+0.3*sin(2*PI*(t+{seed})*0.93)+0.1*sin(2*PI*t*2.6+0.5))"
    return (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
            f"rotate='0.006*sin(2*PI*(t+{seed})*0.37)':fillcolor=none,crop=w={cw}:h={ch}:x='{x}':y='{y}',scale={w}:{h}")


def nframes(v_in, v_out):
    return int(round((v_out + V0) * FPS)) - int(round((v_in + V0) * FPS))


def render(i, shot):
    v_in, v_out, kind, a = shot
    nf = nframes(v_in, v_out)                                               # frame-exact: no drift across the concat
    dur = round(nf / FPS, 4)
    out = f"{TMP}/s{i:02d}_{a['name']}.mp4"
    enc = ["-r", str(FPS), "-frames:v", str(nf), "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p", "-an", out]
    if kind == "talk":
        ss = v_in - a["off"]
        vf = handheld(dur, seed=i * 1.7, punch=a.get("punch", 1.0)) + "," + grade(1)
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-t", f"{dur + 0.3:.3f}", "-i", a["src"], "-vf", vf] + enc)
    elif kind == "split":
        ss = v_in - a["off"]
        hook = f"{G}/hook.mp4"
        tin = ["-loop", "1", "-t", f"{dur + 0.3:.3f}", "-i", f"{TMP}/seam.png"]
        if a.get("freeze"):
            fv = (f"[0:v]trim=start_frame=0:end_frame=1,loop={nf + 5}:1:0,setpts=N/{FPS}/TB[hk];"
                  f"[1:v]trim=start_frame=0:end_frame=1,loop={nf + 5}:1:0,setpts=N/{FPS}/TB,")
            ins = ["-i", hook, "-ss", f"{ss:.3f}", "-i", a["src"]]
        else:
            fv = f"[0:v]fps={FPS},setpts=PTS-STARTPTS[hk];[1:v]"
            ins = ["-ss", f"{a['hook_ss']:.3f}", "-t", f"{dur + 0.3:.3f}", "-i", hook,
                   "-ss", f"{ss:.3f}", "-t", f"{dur + 0.3:.3f}", "-i", a["src"]]
        fc = (fv + f"{handheld(dur, seed=i * 1.7, zoom=1.04)},{grade(1)},crop={W}:{H - SPLIT}:0:{FACE_Y0}[rs];"
              f"[hk]scale={W}:{SPLIT}[hk2];[hk2][rs]vstack=inputs=2[st];[st][2:v]overlay=0:{SPLIT - 24}[v]")
        run(["ffmpeg", "-v", "error", "-y"] + ins + tin + ["-filter_complex", fc, "-map", "[v]"] + enc)
    elif kind == "gfx":
        vf = f"fps={FPS},tpad=stop_mode=clone:stop_duration=0.5,scale={W}:{H}," + grade(2)
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a['ss']:.3f}", "-i", a["src"], "-vf", vf] + enc)
    elif kind == "vox":
        sp = a.get("speed", 1.0)                                               # <1 slows the clip down
        vf = f"setpts=PTS/{sp},tpad=stop_mode=clone:stop_duration=0.6,fps={FPS},scale={W}:{H}," + grade(2)
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a['ss']:.3f}", "-i", a["src"], "-vf", vf] + enc)
    return out


def seam_png():
    """a torn white paper edge with a soft shadow, laid over the seam between the hook and Rashmi"""
    import random
    r = random.Random(4); im = Image.new("RGBA", (W, 48), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    top = [(x, 18 + r.randint(-4, 4)) for x in range(0, W + 12, 12)]
    bot = [(x, 30 + r.randint(-5, 5)) for x in range(W + 12, -12, -12)]
    sh = Image.new("RGBA", (W, 48), (0, 0, 0, 0)); ImageDraw.Draw(sh).polygon([(x, y + 6) for x, y in top + bot], fill=(0, 0, 0, 90))
    from PIL import ImageFilter
    sh = sh.filter(ImageFilter.GaussianBlur(4)); im.alpha_composite(sh)
    d.polygon(top + bot, fill=(248, 246, 238, 255))
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


def caption_img(text, size=60):
    parts = []; hi = False
    for seg in text.split("*"):
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


def overlays():
    """list of (t_in, t_out, x, y, rgba ndarray, pop) in REEL time"""
    ov = []
    split_end = 8.62
    for a, b, t in CAPS:
        im = caption_img(t)
        y = SPLIT - 52 if a < split_end else 985                          # on the seam in the split, low elsewhere
        ov.append((a + V0, b + V0, 0, y, np.asarray(im), True))
    for a, b, key, x, y, rot in LOGOS:
        im = Image.open(key).convert("RGBA")
        if rot:
            im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
        ov.append((a + V0, b + V0, int(x - im.width / 2), int(y - im.height / 2), np.asarray(im), True))
    return ov


def burn(base, out, ov):
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
                img = rgba; age = t - a
                if pop and age < 0.12:          # quick pop-in
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


def voice_prep():
    """cut.wav with one fix: the soft last word "हैं" (v 58.13-58.50, 10 dB under the line) lifted 7 dB with raised-cosine ramps"""
    import wave
    src, out = f"{HERE}/voice/cut.wav", f"{TMP}/voice_fixed.wav"
    w = wave.open(src); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32); w.close()
    g = np.ones_like(x); a, b, r = int(58.13 * sr), int(58.50 * sr), int(0.03 * sr); lift = 10 ** (7 / 20)
    ramp = 1 + (lift - 1) * (0.5 - 0.5 * np.cos(np.linspace(0, np.pi, r)))
    g[a - r:a] = ramp; g[a:b] = lift; g[b:b + r] = ramp[::-1]
    y = np.clip(x * g, -32768, 32767).astype(np.int16)
    o = wave.open(out, "wb"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr); o.writeframes(y.tobytes()); o.close()
    return out


def mix(total, out_wav):
    """voice + the collage clips' own paper sounds (low) + room tone + effects on slams and stamps"""
    A = f"{ROOT}/assets/audio"
    ms = lambda v: int(round((v + V0) * 1000))
    fx = [("sfx_whoosh.wav", 2.45, 0.16), ("sfx_pop.wav", 3.10, 0.25), ("sfx_pop.wav", 3.66, 0.25),   # hook: photos, the X post
          ("sfx_whoosh.wav", 5.30, 0.16), ("sfx_thud.wav", 7.62, 0.22),
          ("sfx_whoosh.wav", 8.55, 0.12),                                                         # into full screen
          ("sfx_pop.wav", 13.05, 0.22), ("sfx_whoosh.wav", 14.50, 0.14), ("sfx_stamp.wav", 16.45, 0.35),
          ("sfx_scratch.wav", 17.75, 0.18),
          ("sfx_pop.wav", 22.10, 0.2), ("sfx_whoosh.wav", 23.40, 0.14), ("sfx_thud.wav", 24.05, 0.24),
          ("sfx_thud.wav", 27.19, 0.24),
          ("sfx_pop.wav", 33.00, 0.18), ("sfx_pop.wav", 34.10, 0.18), ("sfx_pop.wav", 53.20, 0.2), ("sfx_scratch.wav", 54.0, 0.16),
          ("sfx_whoosh.wav", END_V - 0.05, 0.14)]
    inputs = ["-i", voice_prep(),
              "-ss", f"{L5_SS}", "-t", f"{36.08 - 28.62:.3f}", "-i", f"{VOX}/test_L5.mp4",
              "-i", f"{VOX}/L7.mp4",
              "-stream_loop", "-1", "-i", f"{A}/ambience/road_distant_loop.wav"]
    for f, _, _ in fx:
        inputs += ["-i", f"{A}/{f}"]
    fc = (f"[0:a]aresample=48000,adelay={int(V0 * 1000)}|{int(V0 * 1000)},volume=1.0[vo];"
          f"[1:a]aresample=48000,volume=0.20,afade=t=in:d=0.2,adelay={ms(28.62)}|{ms(28.62)}[l5];"
          f"[2:a]aresample=48000,atempo={10.0 / L7_DUR:.4f},volume=0.20,afade=t=in:d=0.2,adelay={ms(40.95)}|{ms(40.95)}[l7];"
          f"[3:a]aresample=48000,atrim=0:{total},volume=0.04[room];")
    labels = ["[vo]", "[l5]", "[l7]", "[room]"]
    for k, (f, v, vol) in enumerate(fx):
        fc += f"[{4 + k}:a]aresample=48000,volume={vol},adelay={ms(v)}|{ms(v)}[x{k}];"; labels.append(f"[x{k}]")
    fc += (f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{total:.3f},"
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
    L = [("L1", 0.00, 8.60, None), ("L2", 8.70, 17.45, 8.62), ("L3", 17.48, 18.90, None), ("L4", 19.00, 28.50, 18.95),
         ("L5", 28.52, 36.10, None), ("L6", 36.12, 40.90, 36.08), ("L7", 40.98, 51.45, None), ("L8", 51.50, 58.55, 51.46)]
    lines = []
    for lid, a, b, cut in L:
        shots = [x for x in SHOTS if x[3]["name"] in LINE_SHOTS.get(lid, [])]       # the talking shots of this line
        ln = {"id": lid, "speaker": "rashmi", "start": round(a + V0, 3), "end": round(b + V0, 3),
              "source": "work/jio01/build/dialogue_src.wav",
              "segments": [[round(x[0] + V0, 3), round(x[1] + V0, 3)] for x in shots]}
        if shots:                                 # identity judged on the raw clips (the split crops her forehead)
            ln["clips"] = [os.path.relpath(x[3]["src"], ROOT) for x in shots]
            ln["clip_spans"] = [[round(x[0] - x[3]["off"], 3), round(x[1] - x[3]["off"], 3)] for x in shots]
        if cut is not None:
            ln["cut_in"] = round(cut + V0, 3)
        lines.append(ln)
    M = {"slug": "jio01", "format": "creator", "final": os.path.relpath(final, ROOT), "script": "registry/scripts/jio01.json",
         "characters": {"rashmi": "assets/characters/rashmi_e11_master.jpg"}, "prefinish": "work/jio01/edit_raw.mp4",
         "dialogue_stem": "work/jio01/build/dialogue.wav", "length": {"min": 20, "max": 70, "expected": total},
         "loudness": {"target": -14}, "fps": FPS, "repairs_file": "work/jio01/qc_repairs.json",
         "rebuild": "python3 work/jio01/build.py", "lines": lines}
    json.dump(M, open(f"{HERE}/qc_manifest.json", "w"), indent=1)


def main():
    total = round(END_V + TAIL + V0, 3)
    print(f"reel {total:.2f} s  (voice starts {V0} s in)")
    talk = 0
    for s in SHOTS:
        d = s[1] - s[0]; talk += d if s[3]["name"] in TALK else 0
        extra = ""
        if s[2] in ("talk", "split") and "off" in s[3]:
            ss = s[0] - s[3]["off"]; extra = f"src {ss:.2f}-{ss + d:.2f}"
        print(f"  {s[0] + V0:6.2f}-{s[1] + V0:6.2f}  {d:5.2f}s  {s[2]:5s} {s[3]['name']:8s} {extra}")
    print(f"talking share {talk / total:.0%} (her on screen, lip-synced; the split counts in full)")
    if os.environ.get("PLAN_ONLY"):
        return
    seam_png()
    parts = [render(i, s) for i, s in enumerate(SHOTS)]
    with open(f"{TMP}/concat.txt", "w") as f:
        f.writelines(f"file '{p}'\n" for p in parts)
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{TMP}/concat.txt", "-c", "copy", f"{TMP}/base.mp4"])
    burn(f"{TMP}/base.mp4", f"{TMP}/burned.mp4", overlays())
    mix(total, f"{TMP}/mix.wav")
    os.makedirs(f"{ROOT}/outputs/jio01", exist_ok=True)
    out = f"{ROOT}/outputs/jio01/jio01_starlink_jio.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{TMP}/base.mp4", "-i", f"{TMP}/mix.wav", "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", f"{HERE}/edit_raw.mp4"])          # pre-finish, for lip sync
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{TMP}/voice_fixed.wav", "-ar", "48000", "-ac", "1", f"{TMP}/dialogue_src.wav"])
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{TMP}/voice_fixed.wav", "-af", f"adelay={int(V0 * 1000)},apad,atrim=0:{total}",
         "-ar", "48000", "-ac", "1", f"{TMP}/dialogue.wav"])
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{TMP}/burned.mp4", "-i", f"{TMP}/mix.wav", "-map", "0:v", "-map", "1:a",
         "-vf", "scale=1080:1920:flags=lanczos", "-r", str(FPS), "-c:v", "libx264", "-crf", "17", "-preset", "slow",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out])
    phone = out.replace(".mp4", "_phone.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-i", out, "-c:v", "libx264", "-crf", "26", "-preset", "slow", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", phone])
    write_manifest(total, out)
    print("wrote", out, "and", phone)


if __name__ == "__main__":
    main()
