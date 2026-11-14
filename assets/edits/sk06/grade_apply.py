#!/usr/bin/env python3
"""Apply the sk06 grade (vid/grade.json: the Wan 2.7 -> Wan 3.0 Lab transfer measured by grade_match.py) to more
Wan 2.7 clips, so every model's clip reads as one camera. Usage (qcpy, repo root): grade_apply.py IN.mp4 OUT.mp4 [...pairs]"""
import json, subprocess, sys
import cv2, numpy as np
V = "work/sk06/vid"; W, H = 720, 1280
g = json.load(open(f"{V}/grade.json")); scale, shift = np.array(g["scale_Lab"]), np.array(g["shift_Lab"])
args = sys.argv[1:]
for src, dst in zip(args[::2], args[1::2]):
    rd = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    wr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                           "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
    n = 0
    while True:
        buf = rd.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        lab = cv2.cvtColor(np.frombuffer(buf, np.uint8).reshape(H, W, 3), cv2.COLOR_BGR2LAB).astype(np.float64)
        wr.stdin.write(cv2.cvtColor(np.clip(lab * scale + shift, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR).tobytes()); n += 1
    wr.stdin.close(); wr.wait(); rd.wait(); print(dst, n, "frames")
