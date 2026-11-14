#!/usr/bin/env python3
"""Print the sparkle margin (px from the right and bottom edges) that holds Gemini's star.
Usage: find_sparkle.py IMAGE [SIZE]. Candidates: 64 (seen 2026-10-16) and 192 (2026-10-14/15).
Score = share of low-saturation pixels in the box that are clearly brighter than the box median."""
import sys
from PIL import Image
im = Image.open(sys.argv[1]).convert("RGB"); W, H = im.size
size = int(sys.argv[2]) if len(sys.argv) > 2 else 96
best = None
for m in (64, 192):
    box = im.crop((W - m - size, H - m - size, W - m, H - m))
    px = list(box.getdata()) if not hasattr(box, "get_flattened_data") else list(box.get_flattened_data()); lum = sorted(sum(p) / 3 for p in px); med = lum[len(lum) // 2]
    hits = sum(1 for p in px if max(p) - min(p) < 30 and sum(p) / 3 > med + 25)
    score = hits / len(px)
    print(f"margin {m}: score {score:.3f}", file=sys.stderr)
    if best is None or score > best[1]: best = (m, score)
print(best[0])
