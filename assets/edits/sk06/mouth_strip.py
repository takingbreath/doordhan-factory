#!/usr/bin/env python3
"""Mouth close-ups at 10 fps with the voice loudness under each frame, one row per clip (the Kendra QC step 7 check:
"look at the mouth frames at a known word against the audio"). Run with pipeline/qcpy.
Usage: mouth_strip.py OUT.jpg CLIP_au.mp4 [...]"""
import sys, subprocess, numpy as np, mediapipe as mp
from PIL import Image, ImageDraw
out, clips = sys.argv[1], sys.argv[2:]
fd = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.3)
rows = []
for c in clips:
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", c], capture_output=True, text=True).stdout)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", c, "-vf", "fps=10,scale=360:640", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 640, 360, 3)
    au = subprocess.run(["ffmpeg", "-v", "error", "-i", c, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True).stdout
    a = np.frombuffer(au, "<i2").astype(float) / 32768
    det = fd.process(fr[len(fr) // 2]).detections
    d = max(det, key=lambda d: d.location_data.relative_bounding_box.width)
    k = d.location_data.relative_keypoints[3]; bw = d.location_data.relative_bounding_box.width * 360
    cx, cy = int(k.x * 360), int(k.y * 640); w, h = int(bw * 0.75), int(bw * 0.45)
    tiles = []
    for i, f in enumerate(fr[5:]):                     # from 0.5 s (the lead)
        t = (i + 5) / 10
        crop = Image.fromarray(f).crop((cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2)).resize((72, 44))
        seg = a[int(t * 8000): int((t + 0.1) * 8000)]
        lv = 0 if len(seg) == 0 else min(1, np.sqrt(np.mean(seg ** 2)) * 8)
        tile = Image.new("RGB", (72, 60), (20, 20, 20)); tile.paste(crop, (0, 0))
        ImageDraw.Draw(tile).rectangle([0, 46, int(72 * lv), 58], fill=(255, 200, 0))
        tiles.append(tile)
    row = Image.new("RGB", (72 * len(tiles), 74), (0, 0, 0)); [row.paste(t, (i * 72, 14)) for i, t in enumerate(tiles)]
    ImageDraw.Draw(row).text((2, 1), c.split("/")[-1], fill=(255, 255, 255)); rows.append(row)
W = max(r.width for r in rows); sheet = Image.new("RGB", (W, sum(r.height for r in rows)), (0, 0, 0))
y = 0
for r in rows: sheet.paste(r, (0, y)); y += r.height
sheet.save(out); print(out, sheet.size)
