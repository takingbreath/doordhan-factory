#!/usr/bin/env python3
"""Write textured copies of Pandey's Wan clips: work/sk05/vid2/<n>.mp4 -> vid2/<n>_tx.mp4 (video textured by texturize.py, the clip's own audio copied).
usage: texturize_clips.py CLIPDIR T1n T2 T3 T4 T5   (CLIPDIR holds <name>.mp4; run with the QC python: pipeline/qcpy assets/edits/vox_desk/texturize_clips.py work/<slug>/vid ...)"""
import os, subprocess, sys
import cv2, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import texturize as T
CLIPDIR = os.path.abspath(sys.argv[1])
for n in sys.argv[2:]:
    src = f"{CLIPDIR}/{n}.mp4"; tmp = f"{CLIPDIR}/{n}_tx_noaudio.mp4"; out = f"{CLIPDIR}/{n}_tx.mp4"
    cap = cv2.VideoCapture(src); w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)); fps = cap.get(cv2.CAP_PROP_FPS)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-", "-c:v", "libx264", "-crf", "13", "-preset", "fast", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    i = 0
    while True:
        ok, bgr = cap.read()
        if not ok: break
        enc.stdin.write(np.ascontiguousarray(T.texturize(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB), i, seed=7)).tobytes()); i += 1
    enc.stdin.close(); enc.wait()
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-i", src, "-map", "0:v", "-map", "1:a?", "-c", "copy", "-shortest", out]); os.remove(tmp)
    print(n, i, "frames ->", out)
