#!/usr/bin/env python3
"""Mouth box (480x854 analysis frame, for lipcheck/qc.py) and face centre (720x1280 edit frame) of a clip or image.
Usage: mouthbox.py FILE [t]"""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
import numpy as np
from face import load_rgb, analyse
f = sys.argv[1]; t = float(sys.argv[2]) if len(sys.argv) > 2 else 0.3
rgb = load_rgb(f, t if f.endswith(".mp4") else None, width=480)
H, W = rgb.shape[:2]
fc = analyse(rgb)
if not fc:
    print(json.dumps({"file": f, "error": "no face"})); sys.exit()
p = fc[0]["points"]
lips = p[[61, 291, 0, 17, 13, 14, 37, 267, 84, 314]]
x0, y0 = lips.min(0); x1, y1 = lips.max(0); w, h = x1 - x0, y1 - y0
box = [int(x0 - 0.25 * w), int(y0 - 0.2 * h), int(1.5 * w), int(max(h * 1.9, 1.1 * w))]
bx = fc[0]["box"]; s = 720 / W
centre = [round((bx[0] + bx[2]) / 2 * s), round((bx[1] + bx[3]) / 2 * s)]
eyes = [round((p[468][0] + p[473][0]) / 2 * s), round((p[468][1] + p[473][1]) / 2 * s)]
print(json.dumps({"file": f, "frame": [W, H], "mouth_box_480": box, "face_centre_720": centre, "eyes_720": eyes,
                  "face_h_720": round((bx[3] - bx[1]) * s)}))
