#!/usr/bin/env python3
"""A real analog VHS pass (lab test, 2026-09-29), in place of look.py's static grain/bleed finish.
Works in YCbCr on the 720x1280 edit, frame by frame, and changes over time the way a tape does:
  lifted blacks and soft whites; luma bandwidth ~300 lines with a slight right-hand smear and sharpness-circuit
  halo; chroma at a fraction of that resolution, bleeding ~4 px right, a little desaturated, with streaky colour
  noise; per-line time-base jitter (a smooth wobble plus small line-to-line error, new every frame) and a
  head-switching tear in the bottom lines; streak noise stretched sideways (survives re-compression better than
  single-pixel grain); a rare dropout speck; faint luma flicker.
Everything is sized to survive Instagram's re-encode (jitter ~1.5 px at 720 = ~2 px at 1080; noise in 6-px streaks).
Usage: vhs.py IN.mkv OUT.mkv [--strength 1.0]   (audio copied through)"""
import argparse, subprocess, sys
import numpy as np
from scipy.ndimage import gaussian_filter1d, gaussian_filter

W, H = 720, 1280


def ycc(rgb):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    y = 0.299 * r + 0.587 * g + 0.114 * b
    return y, (b - y) * 0.564, (r - y) * 0.713


def rgb(y, cb, cr):
    r = y + 1.403 * cr; b = y + 1.773 * cb; g = (y - 0.299 * r - 0.114 * b) / 0.587
    return np.stack([r, g, b], -1)


def shift_rows(img, dx):
    """shift each row right by dx[row] pixels (fractional, linear interpolation, edge clamped)"""
    xs = np.arange(img.shape[1])[None, :] - dx[:, None]
    x0 = np.clip(np.floor(xs).astype(int), 0, img.shape[1] - 1); x1 = np.clip(x0 + 1, 0, img.shape[1] - 1)
    f = xs - np.floor(xs)
    return np.take_along_axis(img, x0, 1) * (1 - f) + np.take_along_axis(img, x1, 1) * f


def process(fr, n, rng, k, wob_state):
    y, cb, cr = ycc(fr.astype(np.float32) / 255)
    # tone: lifted blacks, softened whites, slight gamma lift
    y = 0.065 * k + (1 - 0.065 * k - 0.04 * k) * np.power(np.clip(y, 0, 1), 1 - 0.06 * k)
    # luma bandwidth + smear + sharpness halo (horizontal only)
    yl = gaussian_filter1d(y, 1.25 * k, axis=1)
    smear = np.roll(gaussian_filter1d(yl, 3.0, axis=1), int(round(3 * k)), axis=1)
    y = (1 - 0.14 * k) * yl + 0.14 * k * smear
    y = y + 0.30 * k * (y - gaussian_filter1d(y, 2.5, axis=1))
    # chroma: low bandwidth, bleeding right, a little desaturated, streaky colour noise
    cb = np.roll(gaussian_filter(cb, (1.5, 7 * k)), int(round(4 * k)), axis=1) * (1 - 0.1 * k)
    cr = np.roll(gaussian_filter(cr, (1.5, 7 * k)), int(round(4 * k)), axis=1) * (1 - 0.1 * k)
    cn = np.repeat(rng.standard_normal((H, W // 24 + 1)), 24, axis=1)[:, :W]
    cb += 0.010 * k * cn; cr -= 0.008 * k * np.roll(cn, 7, 0)
    # time-base error: smooth wobble along the frame (correlated frame to frame) + line-to-line jitter
    wob_state[:] = 0.85 * wob_state + 0.15 * rng.standard_normal(wob_state.shape)
    wob = np.interp(np.arange(H), np.linspace(0, H, len(wob_state)), wob_state) * 3.0
    dx = k * (1.1 * wob + 0.45 * rng.standard_normal(H))
    tear = 16                                                   # head-switching lines at the bottom
    dx[-tear:] += k * np.linspace(2, 12, tear) * (0.7 + 0.6 * rng.random())
    y, cb, cr = shift_rows(y, dx), shift_rows(cb, dx), shift_rows(cr, dx)
    y[-tear:] += k * 0.05 * rng.standard_normal((tear, W))
    # streak noise (stretched sideways) + a touch of fine noise, faint flicker
    streak = np.repeat(rng.standard_normal((H, W // 6 + 1)), 6, axis=1)[:, :W]
    y += k * (0.018 * gaussian_filter1d(streak, 1.5, axis=1) + 0.008 * rng.standard_normal((H, W)))
    y *= 1 + k * 0.012 * np.sin(n * 0.9) * rng.random()
    # a rare dropout: a short bright streak for one frame
    if rng.random() < 0.012 * k:
        r0 = rng.integers(0, H - 3); c0 = rng.integers(0, W - 120); L = rng.integers(30, 120)
        y[r0:r0 + 2, c0:c0 + L] = np.maximum(y[r0:r0 + 2, c0:c0 + L], 0.9)
    return (np.clip(rgb(y, cb, cr), 0, 1) * 255 + 0.5).astype(np.uint8)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--strength", type=float, default=1.0)
    a = ap.parse_args()
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", a.src, "-vf", f"scale={W}:{H}", "-f", "rawvideo",
                            "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    fps = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
                          "-of", "csv=p=0", a.src], capture_output=True, text=True).stdout.strip()
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", fps, "-i", "-", "-i", a.src, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264",
                            "-crf", "14", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "copy", a.out],
                           stdin=subprocess.PIPE)
    rng = np.random.default_rng(11); wob = np.zeros(24); n = 0
    while True:
        raw = dec.stdout.read(W * H * 3)
        if len(raw) < W * H * 3:
            break
        enc.stdin.write(process(np.frombuffer(raw, np.uint8).reshape(H, W, 3), n, rng, a.strength, wob).tobytes())
        n += 1
    enc.stdin.close(); enc.wait(); dec.wait()
    print(f"{a.out}: {n} frames, strength {a.strength}", file=sys.stderr)


if __name__ == "__main__":
    main()
