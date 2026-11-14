#!/usr/bin/env python3
"""strip.py SCENE V0 v1 v2 ... : render stills of a Remotion scene at the given voice times and tile them. Output review/rm_strip_<SCENE>.png"""
import subprocess, sys
from PIL import Image
n, v0 = sys.argv[1], float(sys.argv[2]); vs = [float(x) for x in sys.argv[3:]]; ims = []
for v in vs:
    f = max(0, int(round((v - v0) * 30))); out = f"/tmp/st_{n}_{f}.png"
    subprocess.run(["npx", "remotion", "still", "src/index.ts", n, out, f"--frame={f}"], capture_output=True, text=True)
    ims.append(Image.open(out).convert("RGB"))
h = 560; ims = [im.resize((int(im.width * h / im.height * (im.height / 1280) if False else im.width * h / 1280), int(im.height * h / 1280))) for im in ims]
sh = Image.new("RGB", (sum(i.width + 4 for i in ims), max(i.height for i in ims)), (30, 30, 34)); x = 0
for im in ims: sh.paste(im, (x, 0)); x += im.width + 4
sh.save(f"/Users/akhilesh/doordhan-factory/work/sk05/review/rm_strip_{n}.png"); print(sh.size)
