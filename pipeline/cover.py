#!/usr/bin/env python3
"""Doordhan reel covers, v3 (Akhilesh, 2026-11-14: "high quality", not collage slop). The rules are in docs/covers.md.
A cover = ONE concept scene + our type layer:
  1. the scene: a single cinematic picture with the presenter inside the story (Gemini, with the presenter's master
     keyframe as the reference; gemini-media skill), no text in it;
  2. the type layer, set here in HTML/CSS and rendered by headless Chrome at exactly 1080x1920: the hook in the
     Doordhan lime box (Anton caps, ink outline and hard shadow, a slight tilt), an optional white kicker line above it,
     an optional hand-drawn arrow, a light vignette and film grain so the type sits in the picture.
The profile grid shows the centre 3:4 (y 240..1680): the hook, the face and the subject must sit inside it.
Usage (repo root):  python3 pipeline/cover.py work/<slug>/cover.json
Spec: {"out": "outputs/<slug>/E<n>_cover.jpg",
       "scene": "work/<slug>/cover/scene.png",          # any size; it covers the frame
       "scene_shift": [0, 0],                           # optional px nudge of the scene (x, y), after cover-fit
       "scene_zoom": 1.0,                               # optional extra zoom of the scene
       "hook": "AGLA BOOM?",                            # 1-4 words; "\\n" for a second line
       "kicker": "SPACE + CHIPS",                       # optional, small white line above the hook
       "hook_at": [x, y], "tilt": -4,                   # centre of the hook box (cover px) and its tilt in degrees
       "hook_size": 170,                                # optional, px
       "arrow": {"from": [x, y], "to": [x, y], "bend": 0.3}}   # optional, cover px
Writes the cover (JPG, quality 95), <out>_grid.jpg (the 3:4 tile at phone size, 360x480), <out>.html, and prints the
checks."""
import html, json, os, shutil, subprocess, sys, tempfile
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1080, 1920
TILE = (0, 240, 1080, 1680)
LIME, INK = "#C1FE06", "#0C1E14"
FONT = os.path.join(ROOT, "assets", "fonts", "Anton-Regular.ttf")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def path(p):
    return p if os.path.isabs(p) else os.path.join(ROOT, p)


def arrow_svg(a):
    (x0, y0), (x1, y1) = a["from"], a["to"]; bend = a.get("bend", 0.3)
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2; nx, ny = -(y1 - y0) * bend, (x1 - x0) * bend
    cx, cy = mx + nx, my + ny
    import math
    ang = math.atan2(y1 - cy, x1 - cx); L = 46
    h1 = (x1 - L * math.cos(ang - 0.55), y1 - L * math.sin(ang - 0.55))
    h2 = (x1 - L * math.cos(ang + 0.55), y1 - L * math.sin(ang + 0.55))
    d = f"M{x0},{y0} Q{cx},{cy} {x1},{y1}"
    head = f"M{h1[0]:.0f},{h1[1]:.0f} L{x1},{y1} L{h2[0]:.0f},{h2[1]:.0f}"
    return (f'<svg class="arrow" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<g fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#rough)">'
            f'<path d="{d}" stroke="{INK}" stroke-width="30"/><path d="{head}" stroke="{INK}" stroke-width="30"/>'
            f'<path d="{d}" stroke="#fff" stroke-width="17"/><path d="{head}" stroke="#fff" stroke-width="17"/></g>'
            f'<defs><filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="4"/>'
            f'<feDisplacementMap in="SourceGraphic" scale="6"/></filter></defs></svg>')


def page(spec):
    sx, sy = spec.get("scene_shift", [0, 0]); zoom = spec.get("scene_zoom", 1.0)
    hx, hy = spec.get("hook_at", [540, 360]); tilt = spec.get("tilt", -4); size = spec.get("hook_size", 170)
    hook = "<br>".join(html.escape(l) for l in spec["hook"].upper().split("\n"))
    kicker = spec.get("kicker")
    kick = f'<div class="kicker">{html.escape(kicker.upper())}</div>' if kicker else ""
    arrow = arrow_svg(spec["arrow"]) if spec.get("arrow") else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: Anton; src: url("file://{FONT}"); }}
html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: {INK}; }}
.cover {{ position: relative; width: {W}px; height: {H}px; overflow: hidden; }}
.scene {{ position: absolute; inset: 0; background: url("file://{path(spec['scene'])}") center / cover no-repeat;
  transform: translate({sx}px, {sy}px) scale({zoom}); filter: contrast(1.07) saturate(1.08); }}
.vignette {{ position: absolute; inset: 0; background:
  radial-gradient(ellipse 85% 70% at 50% 52%, transparent 55%, rgba(12,30,20,.55) 100%); }}
.grain {{ position: absolute; inset: 0; opacity: .16; mix-blend-mode: overlay; }}
.hook {{ position: absolute; left: {hx}px; top: {hy}px; transform: translate(-50%, -50%) rotate({tilt}deg);
  display: flex; flex-direction: column; align-items: center; gap: 14px; }}
.kicker {{ font: {round(size * 0.46)}px/1 Anton, sans-serif; letter-spacing: 3px; color: #fff;
  -webkit-text-stroke: 12px {INK}; paint-order: stroke fill; text-shadow: 0 6px 14px rgba(12,30,20,.6); }}
.box {{ font: {size}px/1.02 Anton, sans-serif; color: {INK}; background: {LIME}; padding: 14px 36px 10px;
  border: 7px solid {INK}; box-shadow: 16px 16px 0 {INK}, 0 22px 50px rgba(0,0,0,.45); text-align: center;
  white-space: nowrap; }}
.arrow {{ position: absolute; inset: 0; }}
</style></head><body><div class="cover">
<div class="scene"></div><div class="vignette"></div>
<svg class="grain" width="{W}" height="{H}"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".9"
 numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
 <rect width="100%" height="100%" filter="url(#n)"/></svg>
{arrow}
<div class="hook">{kick}<div class="box">{hook}</div></div>
</div><script>document.fonts.ready.then(() => document.body.dataset.ready = 1)</script></body></html>"""


def render(html_path, png):
    prof = tempfile.mkdtemp(prefix="cover-chrome-")
    try:
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        f"--window-size={W},{H}", "--allow-file-access-from-files", "--virtual-time-budget=4000",
                        f"--user-data-dir={prof}", f"--screenshot={png}", "file://" + html_path],
                       check=True, capture_output=True, timeout=120)
    finally:
        shutil.rmtree(prof, ignore_errors=True)


def checks(spec):
    words = (spec.get("kicker", "") + " " + spec["hook"]).replace("\n", " ").replace("+", " ").split()
    low = spec["hook"].lower() + " " + spec.get("kicker", "").lower()
    bad = [w for w in ("buy", "sell", "kharido", "becho", "target price") if w in low]
    hy = spec.get("hook_at", [540, 360])[1]
    notes = [("text 1-5 words in all", 1 <= len(words) <= 5, f"{len(words)} words"),
             ("hook inside the 3:4 tile", TILE[1] + 60 < hy < TILE[3] - 60, f"hook centre y {hy}"),
             ("no buy/sell call on the cover (hard rule 3)", not bad, ",".join(bad) or "none")]
    for name, ok, why in notes:
        print(("PASS " if ok else "FAIL ") + name + f" ({why})")
    return all(ok for _, ok, _ in notes)


def main():
    spec = json.load(open(sys.argv[1]))
    out = path(spec["out"]); stem = os.path.splitext(out)[0]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    hp = stem + ".html"; open(hp, "w").write(page(spec))
    png = stem + "_render.png"; render(hp, png)
    im = Image.open(png).convert("RGB")
    if im.size != (W, H):
        sys.exit(f"cover: Chrome rendered {im.size}, expected {(W, H)}")
    im.save(out, quality=95, subsampling=0); os.remove(png)
    im.crop(TILE).resize((360, 480), Image.LANCZOS).save(stem + "_grid.jpg", quality=92)
    ok = checks(spec)
    print(out, stem + "_grid.jpg")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
