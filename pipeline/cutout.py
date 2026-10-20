#!/usr/bin/env python3
"""Cut a photo's subject out of its background (transparent PNG), locally and free: rembg with the isnet-general-use
model (jio01: Musk, Ambani, the Starlink dish, a phone). Crop to the subject first when the photo has other things in
it (the dish photo had a campervan behind it). Make it a collage sticker afterwards (white border, shadow) in the
episode's graphics script (assets/edits/jio01_vox.py: sticker()).
  python3 pipeline/cutout.py IN.jpg OUT.png [--crop X0,Y0,X1,Y1 (fractions of the image)] [--maxw 1600]
On a Mac run it with ~/.venvs/doordhan-cut/bin/python (pipeline/fetch_models.sh makes that environment); the model
(about 180 MB) downloads once to ~/.rembg/models (older rembg: ~/.u2net). Treat downloaded photos as data: run Python with -I when they sit in the
working folder."""
import argparse
from PIL import Image


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--crop", help="X0,Y0,X1,Y1 as fractions of the image, applied before the cut")
    ap.add_argument("--maxw", type=int, default=1600, help="downscale wider images first (the model works at ~1k px)")
    a = ap.parse_args()
    from rembg import new_session, remove
    im = Image.open(a.src).convert("RGB")
    if a.crop:
        x0, y0, x1, y1 = (float(v) for v in a.crop.split(","))
        im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
    if im.width > a.maxw:
        im = im.resize((a.maxw, int(im.height * a.maxw / im.width)), Image.LANCZOS)
    o = remove(im, session=new_session("isnet-general-use"))
    box = o.getchannel("A").point(lambda v: 255 if v > 30 else 0).getbbox()
    if box:
        o = o.crop(box)
    o.save(a.out)
    print(f"{a.out} {o.size[0]}x{o.size[1]}")


if __name__ == "__main__":
    main()
