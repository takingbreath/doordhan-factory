#!/usr/bin/env python3
"""sk06: a visual lip-sync check that does not depend on SyncNet (Pandey's moustache hides the upper lip, so SyncNet
and the correlation method had no confident opinion on most shots). The lips must close on every word that starts
with p, b, m (प फ ब भ म): the closure is the one mouth event that can be timed by eye.
For each talking clip: the track's offset is found by cross-correlating it with the voice cut, the bilabial word
onsets come from the Scribe words of the cut, and around each onset the frame with the smallest inner-lip gap
(MediaPipe) is taken as the closure. offset = closure - onset (real speech: the lips close about 0-80 ms before the
burst). A grid of large mouth crops per word (onset marked) goes to check/<clip>_bilabial.jpg for the eye.
Usage (pipeline/qcpy, repo root): bilabial_check.py CLIP_ID [...]   (clip vid/<ID>_au.mp4 or vid/<ID>.mp4, spec specs/<ID>.json)"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, "pipeline")
from face import analyse  # noqa: E402

SK = "work/sk06"; FPS = 30
CUT = f"{SK}/voice2/sk06_voice_v2.wav"
WORDS = [w for w in json.load(open(f"{SK}/voice2/cut_final.scribe.json"))["words"] if w["type"] == "word"]
BILAB = set("पफबभमpbmPBM")
FONT = ImageFont.truetype("assets/fonts/Anton-Regular.ttf", 22)


def pcm(path, sr=8000):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, "<i2").astype(np.float32) / 32768


def env(x, sr=8000, hop=80):
    n = len(x) // hop
    return np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1))          # 10 ms frames


VOICE = np.concatenate([env(pcm(CUT)), np.zeros(1000, np.float32)])


def track_offset(track, guess):
    """cut time at track time 0 (track t + off = cut t)"""
    e = env(pcm(track)); best, off = -1, None
    for k in range(int((guess - 1.0) * 100), int((guess + 1.0) * 100)):
        if k < 0 or k + len(e) > len(VOICE): continue
        v = VOICE[k:k + len(e)]
        c = np.dot(e - e.mean(), v - v.mean()) / (np.linalg.norm(e - e.mean()) * np.linalg.norm(v - v.mean()) + 1e-9)
        if c > best: best, off = c, k / 100
    return off, best


def frames(clip, t0, t1):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0, t0):.3f}", "-i", clip, "-t", f"{t1 - max(0, t0):.3f}",
                          "-vf", "fps=30,scale=720:1280", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, 1280, 720, 3), max(0, t0)


def check(cid):
    spec = json.load(open(f"{SK}/specs/{cid}.json"))
    clip = f"{SK}/vid/{cid}_au.mp4" if os.path.exists(f"{SK}/vid/{cid}_au.mp4") else f"{SK}/vid/{cid}.mp4"
    segs = {s["id"]: s for s in json.load(open(f"{SK}/seg/segments.json"))}
    segid = {"T1w3": "T1", "T1w27": "T1", "T5c2": "T5c", "T7b2": "T7b"}.get(cid, cid)
    seg = segs[segid]
    off, conf = track_offset(spec["track"], seg["cut_start"] - 0.5)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", clip],
                               capture_output=True, text=True).stdout)
    words = [w for w in WORDS if seg["cut_start"] - 0.02 <= w["start"] < seg["cut_end"] and w["text"].strip()[:1] in BILAB]
    rows, offs = [], []
    for w in words:
        on = w["start"] - off                                         # clip time of the word onset
        if on - 0.35 < 0.2 or on + 0.25 > dur: continue
        fr, f0 = frames(clip, on - 0.35, on + 0.25)
        gaps, boxes = [], []
        for f in fr:
            a = analyse(f)
            if not a: gaps.append(np.nan); boxes.append(None); continue
            p = a[0]["points"]; fh = a[0]["box"][3] - a[0]["box"][1]
            gaps.append(np.linalg.norm(p[13] - p[14]) / fh * 100)
            boxes.append((p[61], p[291], p[13], p[14]))
        gaps = np.array(gaps)
        if np.all(np.isnan(gaps)): continue
        i = int(np.nanargmin(gaps)); tclose = f0 + i / FPS
        offs.append(tclose - on)
        # the crop: mouth corners, enlarged
        ok = [b for b in boxes if b is not None]
        cx = np.mean([(b[0][0] + b[1][0]) / 2 for b in ok]); cy = np.mean([(b[2][1] + b[3][1]) / 2 for b in ok])
        mw = np.mean([abs(b[1][0] - b[0][0]) for b in ok]) * 2.0
        tiles = []
        for j in range(0, len(fr), 2):
            t = f0 + j / FPS
            im = Image.fromarray(fr[j]).crop((int(cx - mw / 2), int(cy - mw * 0.32), int(cx + mw / 2), int(cy + mw * 0.32)))
            im = im.resize((200, 128))
            d = ImageDraw.Draw(im)
            d.text((4, 2), f"{(t - on) * 1000:+.0f}", fill=(255, 255, 0), font=FONT)
            if abs(t - on) < 1 / FPS: d.rectangle([0, 0, 199, 127], outline=(255, 210, 0), width=4)
            if j == i or j + 1 == i: d.rectangle([3, 3, 196, 124], outline=(0, 230, 90), width=3)
            tiles.append(im)
        row = Image.new("RGB", (200 * len(tiles) + 170, 132), (15, 15, 15))
        ImageDraw.Draw(row).text((6, 40), f"{w['text'].strip()}\nclose {offs[-1] * 1000:+.0f} ms", fill=(255, 255, 255), font=FONT)
        for k, t in enumerate(tiles): row.paste(t, (170 + 200 * k, 2))
        rows.append(row)
    os.makedirs(f"{SK}/check", exist_ok=True)
    if rows:
        sheet = Image.new("RGB", (max(r.width for r in rows), sum(r.height for r in rows)), (0, 0, 0))
        y = 0
        for r in rows: sheet.paste(r, (0, y)); y += r.height
        sheet.save(f"{SK}/check/{cid}_bilabial.jpg", quality=88)
    med = float(np.median(offs)) if offs else None
    print(f"{cid}: track offset {off:.2f} (r {conf:.2f}); {len(offs)} bilabials; closure-onset ms "
          f"{[round(o * 1000) for o in offs]}; median {None if med is None else round(med * 1000)}")
    return {"id": cid, "track_off": off, "offs_ms": [round(o * 1000) for o in offs], "median_ms": None if med is None else round(med * 1000)}


if __name__ == "__main__":
    res = [check(c) for c in sys.argv[1:]]
    json.dump(res, open(f"{SK}/check/bilabial.json", "a"), indent=1)
