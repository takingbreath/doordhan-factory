#!/usr/bin/env python3
"""Did the generated clip keep the track we gave it? Wan 2.7 should (PASS). A re-voiced or re-timed line fails.
Main test: correlation of the loudness envelopes (20 ms windows) >= 0.90, after finding the best constant offset
up to 0.3 s. Calibrated 2026-09-25 on the Sarika test shot: kept audio 1.00; same audio shifted 0.2 s and 6 dB
quieter 0.996; the same line reversed 0.68 (the older on/off pattern score still gave it 97%, so it only
supports the verdict now); a different take 0.30. Level differences don't matter (Wan raised one clip by 3 dB).
An offset means cut points must come from speech_map on the clip, not the track.
Usage: check_match.py CLIP.mp4 TRACK.mp3"""
import sys
import numpy as np
from common import envelope


def best_alignment(a, b, win, score):
    n = min(len(a), len(b)); a, b = a[:n], b[:n]
    L, best = int(round(0.3 / win)), (-2.0, 0)
    for k in range(-L, L + 1):
        x, y = (a[k:], b[:n - k]) if k >= 0 else (a[:n + k], b[-k:])
        s = score(x, y)
        if s > best[0] + 1e-9 or (abs(s - best[0]) < 1e-9 and abs(k) < abs(best[1])):
            best = (s, k)
    return best[0], best[1] * win


clip, track = sys.argv[1], sys.argv[2]
a, b = envelope(clip, 0.02), envelope(track, 0.02)
if min(len(a), len(b)) < 10:
    print(f"FAIL  not enough audio to compare ({clip} vs {track})"); raise SystemExit
corr, lag = best_alignment(np.maximum(a, -60), np.maximum(b, -60), 0.02,
                           lambda x, y: float(np.corrcoef(x, y)[0, 1]) if x.std() and y.std() else 0.0)
a5, b5 = envelope(clip), envelope(track)
b5 = b5 + (np.percentile(a5, 95) - np.percentile(b5, 95))       # align levels on the speech frames
pattern, _ = best_alignment(a5, b5, 0.05, lambda x, y: 100.0 * ((x > -38) == (y > -38)).mean())
ok = corr >= 0.90 and pattern >= 95
note = f", clip offset {lag:+.2f}s" if abs(lag) >= 0.02 else ""
print(f"{'PASS' if ok else 'FAIL'}  envelope correlation {corr:.2f} (>=0.90), speech pattern match {pattern:.0f}%"
      f"{note}  ({clip} vs {track})")
