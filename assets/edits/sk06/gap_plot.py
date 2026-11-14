#!/usr/bin/env python3
"""Lip gap (MediaPipe inner lips, % of face height) against the track's loudness, per talking clip, with the
cross-correlation over +-500 ms, so the lag can be read by eye. Usage (qcpy, repo root): gap_plot.py ID [...]"""
import json, subprocess, sys
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, "pipeline")
from face import analyse  # noqa: E402
SK = "work/sk06"
for cid in sys.argv[1:]:
    clip = f"{SK}/vid/{cid}.mp4"; spec = json.load(open(f"{SK}/specs/{cid}.json"))
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", clip, "-vf", "fps=30,scale=720:1280", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 1280, 720, 3)
    gap = []
    for f in fr:
        a = analyse(f)
        if not a: gap.append(np.nan); continue
        p = a[0]["points"]; fh = a[0]["box"][3] - a[0]["box"][1]; gap.append(np.linalg.norm(p[13] - p[14]) / fh * 100)
    gap = np.array(gap); t = np.arange(len(gap)) / 30
    au = subprocess.run(["ffmpeg", "-v", "error", "-i", spec["track"], "-ac", "1", "-ar", "3000", "-f", "s16le", "-"], capture_output=True).stdout
    x = np.frombuffer(au, "<i2").astype(float) / 32768; n = len(x) // 100
    e = np.sqrt((x[:n * 100].reshape(n, 100) ** 2).mean(1)); te = np.arange(n) / 30
    m = min(len(e), len(gap)); g = np.nan_to_num(gap[:m] - np.nanmean(gap[:m])); ee = e[:m] - e[:m].mean()
    lags = np.arange(-15, 16); cc = []
    for L in lags:            # positive L: the mouth comes L frames after the sound
        if L >= 0: a, b = ee[:m - L], g[L:]
        else: a, b = ee[-L:], g[:m + L]
        cc.append(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))
    best = lags[int(np.argmax(cc))] * 33.3
    fig, ax = plt.subplots(2, 1, figsize=(14, 5), gridspec_kw={"height_ratios": [3, 1.3]})
    ax[0].plot(te, e / e.max() * np.nanmax(gap), color="orange", label="voice loudness")
    ax[0].plot(t, gap, color="navy", label="lip gap %")
    ax[0].set_xticks(np.arange(0, t[-1], 0.25), minor=True); ax[0].grid(True, which="both", alpha=0.3); ax[0].legend(loc="upper right")
    ax[0].set_title(f"{cid}: mouth after sound by {best:+.0f} ms at the correlation peak (r {max(cc):.2f})")
    ax[1].plot(lags * 33.3, cc, marker="o"); ax[1].axvline(0, color="grey"); ax[1].set_xlabel("ms the mouth comes after the sound")
    fig.tight_layout(); fig.savefig(f"{SK}/check/{cid}_gap.png", dpi=80); plt.close(fig)
    print(cid, f"peak {best:+.0f} ms r {max(cc):.2f}")
