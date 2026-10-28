#!/usr/bin/env python3
"""Put a dressed background behind a talking clip without regenerating it (anthropic01, 2026-10-28: Akhilesh found
the walls behind Rashmi bare). The plate is a one-change edit of the clip's own keyframe ("the same photograph, the
woman not in it, the wall dressed"), so its angle, lens and light already match. Per frame, MediaPipe's multiclass
selfie segmenter gives the person (hair, skin, clothes); the matte is smoothed over time and feathered, the plate is
cropped exactly like the keyframe, colour-matched to the clip's own background and softened like the lens's depth of
field, and the person is laid over it. The clip's audio is kept as it is, so lip sync does not change.
Usage: bgswap.py CLIP.mp4 PLATE.png OUT.mp4 --crop X Y W H [--blur 2.5] [--match 0.6] [--keep-below Y] [--text T.json]
       bgswap.py CLIP.mp4 - OUT.mp4 --text T.json         (no plate: words behind the person on the clip's own background)
  --text: kinetic words BEHIND the person (the editing reference's look): a JSON list of
          {"t0": s, "t1": s, "big": "WORD", "small": "word", "x": 360, "y": 300, "size": 120}, clip time; a small white
          handwritten word over a big condensed yellow word, sliding in with blur over 0.22 s.
  --crop: the rectangle (in the plate's pixels) the keyframe was cut from before it became the start image.
  --keep-below: keep the clip's own pixels below this line (720x1280 frame), e.g. a sofa she leans on."""
import argparse, json, os, subprocess, sys
import numpy as np
import cv2
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from common import FFMPEG  # noqa: E402
ROOT = os.path.dirname(here)
W, H = 720, 1280

p = argparse.ArgumentParser()
p.add_argument("clip"); p.add_argument("plate"); p.add_argument("out")
p.add_argument("--crop", type=int, nargs=4)
p.add_argument("--blur", type=float, default=2.5); p.add_argument("--match", type=float, default=0.6)
p.add_argument("--keep-below", type=int); p.add_argument("--crop-default", action="store_true")
p.add_argument("--text")
a = p.parse_args()
from PIL import Image, ImageDraw, ImageFont, ImageFilter  # noqa: E402
TEXTS = json.load(open(a.text)) if a.text else []
ANTON, HAND = os.path.join(ROOT, "assets/fonts/Anton-Regular.ttf"), os.path.join(ROOT, "assets/fonts/Caveat.ttf")


def text_layer(t):
    """the words visible at clip time t, as an RGBA layer (W x H), or None"""
    lay = None
    for e in TEXTS:
        if not (e["t0"] <= t < e.get("t1", 1e9)): continue
        p = min(1.0, (t - e["t0"]) / 0.22); p = 1 - (1 - p) ** 3
        size = int(e.get("size", 120) * (1.12 - 0.12 * p))
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        fb = ImageFont.truetype(ANTON, size); bw = d.textlength(e["big"], font=fb)
        x, y = e.get("x", W / 2), e.get("y", 300) + (1 - p) * 34
        shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(shadow)
        ds.text((x - bw / 2, y - size * 0.55 + 6), e["big"], font=fb, fill=(0, 0, 0, 120))
        im.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(9)))
        d.text((x - bw / 2, y - size * 0.55), e["big"], font=fb, fill=tuple(e.get("color", (245, 217, 10))) + (255,))
        if e.get("small"):
            q = min(1.0, max(0.0, (t - e["t0"] - 0.08) / 0.2)); fs = ImageFont.truetype(HAND, int(size * 0.42))
            sw = d.textlength(e["small"], font=fs)
            d.text((x - sw / 2, y - size * 0.55 - size * 0.42), e["small"], font=fs, fill=(255, 255, 255, int(255 * q)))
        if p < 1: im = im.filter(ImageFilter.GaussianBlur((1 - p) * 10))
        im.putalpha(im.getchannel("A").point(lambda v: int(v * min(1.0, p * 1.4))))
        lay = im if lay is None else Image.alpha_composite(lay, im)
    return lay

import mediapipe as mp  # noqa: E402
seg = mp.tasks.vision.ImageSegmenter.create_from_options(mp.tasks.vision.ImageSegmenterOptions(
    base_options=mp.tasks.BaseOptions(model_asset_path=os.path.join(ROOT, "assets/models/selfie_multiclass_256x256.tflite")),
    running_mode=mp.tasks.vision.RunningMode.IMAGE, output_confidence_masks=True, output_category_mask=False))


def person(rgb):
    bg = seg.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb))).confidence_masks[0].numpy_view()
    return cv2.resize(1.0 - bg, (W, H), interpolation=cv2.INTER_LINEAR)


NOPLATE = a.plate == "-"
if not NOPLATE:
    x, y, w, h = a.crop
    plate = cv2.cvtColor(cv2.imread(a.plate), cv2.COLOR_BGR2RGB)
    plate = cv2.resize(plate[y:y + h, x:x + w], (W, H), interpolation=cv2.INTER_AREA)
fps = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", "-of",
                      "csv=p=0", a.clip], capture_output=True, text=True).stdout.strip()
dec = subprocess.Popen([FFMPEG, "-v", "error", "-i", a.clip, "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       stdout=subprocess.PIPE)
tmp = a.out + ".video.mp4"
enc = subprocess.Popen([FFMPEG, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", fps, "-i", "-",
                        "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
m_prev, n = None, 0
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    f = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    m = person(f)
    if NOPLATE: plate_f = f.astype(np.float32)
    elif n == 0:                                 # colour-match the plate to this clip's own background, once
        bgm = (m < 0.1)[..., None]
        fl, pl = cv2.cvtColor(f, cv2.COLOR_RGB2LAB).astype(np.float32), cv2.cvtColor(plate, cv2.COLOR_RGB2LAB).astype(np.float32)
        sel = bgm[..., 0]
        mu_f, sd_f = fl[sel].mean(0), fl[sel].std(0) + 1e-3
        mu_p, sd_p = pl.reshape(-1, 3).mean(0), pl.reshape(-1, 3).std(0) + 1e-3
        moved = (pl - mu_p) / sd_p * sd_f + mu_f
        pl = pl + a.match * (moved - pl)
        pl[..., 0] = np.clip(pl[..., 0], 0, 255)
        plate = cv2.cvtColor(np.clip(pl, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB)
        if a.blur > 0: plate = cv2.GaussianBlur(plate, (0, 0), a.blur)
        plate_f = plate.astype(np.float32)
    m = m if m_prev is None else 0.55 * m + 0.45 * m_prev          # steadier edges between frames
    m_prev = m
    alpha = cv2.GaussianBlur(np.clip((m - 0.15) / 0.7, 0, 1), (0, 0), 1.6)
    if a.keep_below is not None:                 # the clip's own pixels below the line, blended in over 60 px
        ramp = np.clip((np.arange(H, dtype=np.float32) - (a.keep_below - 60)) / 60.0, 0, 1)[:, None]
        alpha = np.maximum(alpha, ramp)
    back = plate_f
    lay = text_layer(n / float(eval(fps))) if TEXTS else None
    if lay is not None:
        la = np.asarray(lay).astype(np.float32); ta = la[..., 3:4] / 255
        back = back * (1 - ta) + la[..., :3] * ta
    out = alpha[..., None] * f.astype(np.float32) + (1 - alpha[..., None]) * back
    enc.stdin.write(np.clip(out, 0, 255).astype(np.uint8).tobytes()); n += 1
enc.stdin.close(); enc.wait(); dec.wait()
subprocess.run([FFMPEG, "-v", "error", "-y", "-i", tmp, "-i", a.clip, "-map", "0:v", "-map", "1:a?", "-c:v", "copy", "-c:a", "copy",
                a.out], check=True)
os.remove(tmp)
print(f"{a.out}: {n} frames, background from {os.path.basename(a.plate)}")
