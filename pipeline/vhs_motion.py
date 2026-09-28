#!/usr/bin/env python3
"""The tape's movement, without its colour: VHS motion elements for the finish (adopted 2026-09-29 from the realism
test, docs/lab/2026-09-29-reads-as-ai.md). look.py's presets are static per frame except the grain, which is part
of why a finished reel still reads as digital. This adds, at `strength` (default 0.65):
  per-line time-base jitter (a smooth wobble plus line-to-line error, new every frame) and a head-switching tear in
  the bottom lines; colour bleed (chroma at low horizontal resolution, bleeding right) with streaky colour noise;
  streak noise stretched sideways; a rare dropout speck.
It deliberately leaves tone and saturation alone, so a preset's colour (the Kendra's brighter look) is kept.
Runs on the 720x1280 edit before look.py (the jitter survives the look's SD pass and an Instagram-like re-encode:
1.06 of 1.08 px at full strength in the test). Frames are processed in parallel; the random state is seeded per
frame, so a render is repeatable.
Usage: vhs_motion.py IN OUT [--strength 0.65]   (audio copied)"""
import argparse, os, subprocess, sys
from multiprocessing import Pool
import numpy as np
from scipy.ndimage import gaussian_filter1d

W, H = 720, 1280
DEFAULT_STRENGTH = 0.65


def shift_rows(img, dx):
    xs = np.arange(img.shape[1], dtype=np.float32)[None, :] - dx[:, None]
    x0 = np.clip(np.floor(xs).astype(np.int32), 0, img.shape[1] - 1); x1 = np.minimum(x0 + 1, img.shape[1] - 1)
    f = xs - np.floor(xs)
    return np.take_along_axis(img, x0, 1) * (1 - f) + np.take_along_axis(img, x1, 1) * f


def wobble_states(n, seed=5):
    """the slow time-base wobble, correlated from frame to frame (an AR(1) process over 24 control rows)"""
    rng = np.random.default_rng(seed); s = np.zeros(24, np.float32); out = []
    for _ in range(n):
        s = 0.85 * s + 0.15 * rng.standard_normal(24).astype(np.float32); out.append(s.copy())
    return out


def process(args):
    raw, n, k, wob = args
    rng = np.random.default_rng(1000 + n)
    fr = np.frombuffer(raw, np.uint8).reshape(H, W, 3).astype(np.float32) / 255
    r, g, b = fr[..., 0], fr[..., 1], fr[..., 2]
    y = 0.299 * r + 0.587 * g + 0.114 * b; cb = (b - y) * 0.564; cr = (r - y) * 0.713
    # colour bleed: chroma bandwidth cut horizontally and pushed right; streaky colour noise
    cb = (1 - k) * cb + k * np.roll(gaussian_filter1d(cb, 7, axis=1), 4, axis=1)
    cr = (1 - k) * cr + k * np.roll(gaussian_filter1d(cr, 7, axis=1), 4, axis=1)
    cn = np.repeat(rng.standard_normal((H, W // 24 + 1)).astype(np.float32), 24, axis=1)[:, :W]
    cb += 0.010 * k * cn; cr -= 0.008 * k * np.roll(cn, 7, 0)
    # time-base error and head switching
    wv = np.interp(np.arange(H), np.linspace(0, H, len(wob)), wob).astype(np.float32) * 3.0
    dx = k * (1.1 * wv + 0.45 * rng.standard_normal(H).astype(np.float32))
    tear = 16
    dx[-tear:] += k * np.linspace(2, 12, tear, dtype=np.float32) * (0.7 + 0.6 * rng.random())
    y, cb, cr = shift_rows(y, dx), shift_rows(cb, dx), shift_rows(cr, dx)
    y[-tear:] += k * 0.05 * rng.standard_normal((tear, W)).astype(np.float32)
    # streak noise, stretched sideways (survives re-compression better than single-pixel grain)
    streak = np.repeat(rng.standard_normal((H, W // 6 + 1)).astype(np.float32), 6, axis=1)[:, :W]
    y += k * (0.018 * gaussian_filter1d(streak, 1.5, axis=1) + 0.006 * rng.standard_normal((H, W)).astype(np.float32))
    if rng.random() < 0.012 * k:                       # a rare dropout: a short bright streak for one frame
        r0 = rng.integers(0, H - 3); c0 = rng.integers(0, W - 120); L = rng.integers(30, 120)
        y[r0:r0 + 2, c0:c0 + L] = np.maximum(y[r0:r0 + 2, c0:c0 + L], 0.9)
    rgb = np.stack([y + 1.403 * cr, (y - 0.299 * (y + 1.403 * cr) - 0.114 * (y + 1.773 * cb)) / 0.587, y + 1.773 * cb], -1)
    return (np.clip(rgb, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes()


def run(src, out, strength=DEFAULT_STRENGTH, crf=15):
    from common import FFMPEG, FFPROBE
    fps = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
                          "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip()
    nfr = int(subprocess.run([FFPROBE, "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                              "stream=nb_read_packets", "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip() or 0)
    wob = wobble_states(nfr + 16)
    dec = subprocess.Popen([FFMPEG, "-v", "error", "-i", src, "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen([FFMPEG, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", fps,
                            "-i", "-", "-i", src, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", str(crf),
                            "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "copy", out], stdin=subprocess.PIPE)

    def frames():
        n = 0
        while True:
            raw = dec.stdout.read(W * H * 3)
            if len(raw) < W * H * 3:
                return
            yield raw, n, strength, wob[min(n, len(wob) - 1)]
            n += 1
    with Pool(max(1, (os.cpu_count() or 2) - 1)) as pool:
        for fr in pool.imap(process, frames(), chunksize=4):
            enc.stdin.write(fr)
    enc.stdin.close(); enc.wait(); dec.wait()
    return out


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--strength", type=float, default=DEFAULT_STRENGTH)
    a = ap.parse_args()
    print(run(a.src, a.out, a.strength))
