#!/usr/bin/env python3
"""Level a tilted head in a keyframe by rotating the whole frame (it reads as a casually held phone).

preflight_keyframe.py fails a talking keyframe at 16 degrees of head roll (tilted starts drifted past the lip-sync
limit on E5). Seedream often tilts the creator's head 17-23 degrees; a regenerate costs a credit, this costs nothing.
  python3 pipeline/level_keyframe.py IN.png OUT.jpg DEGREES     (negative = clockwise; check with preflight after)
The frame is scaled up just enough that the rotated image still covers it, so the face also gets bigger (nana01:
roll 19 -> 7 degrees with -12, face 24% -> 27% of the frame height).
"""
import math, sys
from PIL import Image

src, out, deg = sys.argv[1], sys.argv[2], float(sys.argv[3])
im = Image.open(src).convert("RGB"); W, H = im.size
t = math.radians(abs(deg))
s = max(math.cos(t) + (H / W) * math.sin(t), math.cos(t) + (W / H) * math.sin(t))
big = im.resize((int(W * s), int(H * s)), Image.LANCZOS).rotate(deg, resample=Image.BICUBIC)
x0, y0 = (big.width - W) // 2, (big.height - H) // 2
big.crop((x0, y0, x0 + W, y0 + H)).save(out, quality=95)
print(out, "scale", round(s, 3))
