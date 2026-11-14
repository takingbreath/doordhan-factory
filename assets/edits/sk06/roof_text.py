#!/usr/bin/env python3
"""sk06: "LONG-TERM" painted along the red bus roof in the opening's top shot (Akhilesh, 2026-11-14: "the 'long term' can
be yellow text on the bus roof ... in the shape of the bus as large text, but not overflowing the bus").

The roof is a plane, so it is tracked as one: the roof is found in the first frame by its colour (seeded at the frame
centre), then points on the roof are followed frame to frame (Lucas-Kanade) and a homography (RANSAC) carries the roof
from frame to frame. The word lives in roof coordinates, so it keeps the roof's perspective as the camera tilts down
to the windscreen, and it leaves the frame with the roof. It is worn a little (a fixed noise in roof coordinates) and
lit by the roof's own light, so it reads as paint, not as a graphic.
It is on the roof from the first frame (painted on the bus, part of the world) and fades only when the roof turns too
oblique to read.
Input: the graded dive (vid/S1_wan27_g.mp4). Output: vid/S1_wan27_gt.mp4 (same timing), and with --debug a copy
with the tracked roof outlined (vid/S1_wan27_track.mp4). Run with pipeline/qcpy from the repository root."""
import subprocess, sys, json
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

V = "work/sk06/vid"; W, H = 720, 1280; FPS = 30.0
import argparse
_ap = argparse.ArgumentParser()
_ap.add_argument("--src", default=f"{V}/S1_wan27_g.mp4"); _ap.add_argument("--dst", default=f"{V}/S1_wan27_gt.mp4")
_ap.add_argument("--seed", type=int, nargs=2, default=[370, 660], help="a roof pixel in the reference frame")
_ap.add_argument("--fade", type=float, nargs=2, default=[1.38, 1.62], help="seconds from the reference frame: the roof turns too oblique")
_ap.add_argument("--from-end", action="store_true", help="the reference (top-down) frame is the LAST frame (the outro)")
_ap.add_argument("--debug", action="store_true")
_A = _ap.parse_args()
SRC, DST = _A.src, _A.dst; DBG = DST.replace(".mp4", "_track.mp4")
SEED = tuple(_A.seed); FADE_FROM, FADE_TO = _A.fade
YEL = np.array([10, 229, 255], np.float32)   # BGR of #FFE50A
DEBUG = _A.debug


def read_frames():
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", SRC, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                         capture_output=True, check=True).stdout
    n = len(raw) // (W * H * 3)
    return np.frombuffer(raw[:n * W * H * 3], np.uint8).reshape(n, H, W, 3)


def roof_quad0(bgr):
    """the roof in the first frame: the red region that holds the seed, as a rectangle (top-down view)"""
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    m = (((hsv[..., 0] < 10) | (hsv[..., 0] > 168)) & (hsv[..., 1] > 35) & (hsv[..., 2] > 110)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    n, lab = cv2.connectedComponents(m)
    blob = (lab == lab[SEED[1], SEED[0]]).astype(np.uint8)
    assert lab[SEED[1], SEED[0]] != 0, "the seed is not on the roof"
    cs, _ = cv2.findContours(blob, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    box = cv2.boxPoints(cv2.minAreaRect(max(cs, key=cv2.contourArea)))
    box = box[np.argsort(box[:, 1])]
    top, bot = box[:2][np.argsort(box[:2, 0])], box[2:][np.argsort(box[2:, 0])]
    return np.array([top[0], top[1], bot[1], bot[0]], np.float32)     # TL, TR, BR, BL (rear of the bus at the top)


def track(frames, q0):
    """homography from frame 0 to every frame, carried by points on the roof"""
    Hs = [np.eye(3)]
    for i in range(1, len(frames)):
        g0 = cv2.cvtColor(frames[i - 1], cv2.COLOR_BGR2GRAY); g1 = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
        poly = cv2.perspectiveTransform(q0[None], Hs[-1])[0]
        mask = np.zeros((H, W), np.uint8); cv2.fillConvexPoly(mask, poly.astype(np.int32), 255)
        mask = cv2.erode(mask, np.ones((9, 9), np.uint8))
        p0 = cv2.goodFeaturesToTrack(g0, 400, 0.002, 5, mask=mask)
        if p0 is None or len(p0) < 12:
            Hs.append(Hs[-1]); continue
        p1, st, _ = cv2.calcOpticalFlowPyrLK(g0, g1, p0, None, winSize=(25, 25), maxLevel=4)
        ok = st[:, 0] == 1
        if ok.sum() < 12:
            Hs.append(Hs[-1]); continue
        Hstep, inl = cv2.findHomography(p0[ok], p1[ok], cv2.RANSAC, 2.0)
        Hs.append(Hstep @ Hs[-1] if Hstep is not None else Hs[-1])
    return Hs


def word_canvas():
    """the word, rotated to run along the roof: it reads from the rear of the bus (top) to the front (bottom), the way
    the camera travels. White on black (the alpha), worn a little."""
    font = ImageFont.truetype("assets/fonts/Anton-Regular.ttf", 360)
    word = "LONG-TERM"
    l, t, r, b = font.getbbox(word)
    im = Image.new("L", (r - l + 24, b - t + 24), 0)
    ImageDraw.Draw(im).text((12 - l, 12 - t), word, font=font, fill=255)
    a = np.asarray(im.rotate(-90, expand=True)).astype(np.float32) / 255
    rng = np.random.default_rng(6)
    wear = cv2.GaussianBlur(rng.random(a.shape).astype(np.float32), (0, 0), 6)
    wear = (wear - wear.min()) / (wear.max() - wear.min())
    speck = (cv2.GaussianBlur(rng.random(a.shape).astype(np.float32), (0, 0), 1.2) > 0.62).astype(np.float32)
    a *= np.clip(0.80 + 0.20 * wear, 0, 1) * (1 - 0.35 * speck)
    return a


def main():
    frames = read_frames()
    if _A.from_end: frames = frames[::-1]
    q0 = roof_quad0(frames[0])
    Wr, Lr = np.linalg.norm(q0[1] - q0[0]), np.linalg.norm(q0[3] - q0[0])
    R = np.float32([[0, 0], [Wr, 0], [Wr, Lr], [0, Lr]])
    P0 = cv2.getPerspectiveTransform(R, q0)                       # roof coordinates -> frame 0
    a = word_canvas(); ch, cw = a.shape
    s = min(0.80 * Wr / cw, 0.88 * Lr / ch)                       # margins: never touches the roof edge
    S = np.array([[s, 0, Wr / 2 - s * cw / 2], [0, s, Lr / 2 - s * ch / 2], [0, 0, 1]])
    Hs = track(frames, q0)
    out_v = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                              "-r", "30", "-i", "-", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", DST],
                             stdin=subprocess.PIPE)
    dbg = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", "30", "-i", "-", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", DBG],
                           stdin=subprocess.PIPE) if DEBUG else None
    log = []; outs = []
    for i, f in enumerate(frames):
        t = i / FPS
        k = 1.0 if t < FADE_FROM else max(0.0, 1 - (t - FADE_FROM) / (FADE_TO - FADE_FROM))
        f = f.copy()
        quad = cv2.perspectiveTransform(q0[None], Hs[i])[0]
        if k > 0:
            M = Hs[i] @ P0 @ S
            al = cv2.warpPerspective(a, M, (W, H), flags=cv2.INTER_LINEAR) * 0.94 * k
            lum = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32)
            roof = cv2.GaussianBlur(lum, (0, 0), 1.5)
            ref = np.median(roof[al > 0.3]) if (al > 0.3).any() else 128
            shade = np.clip(roof / max(ref, 1), 0.6, 1.2)[..., None]     # the roof's own light and dirt
            paint = np.clip(YEL * shade, 0, 255)
            f = (f * (1 - al[..., None]) + paint * al[..., None]).astype(np.uint8)
        log.append({"t": round(t, 3), "quad": quad.round(1).tolist()})
        d = None
        if dbg:
            d = f.copy(); cv2.polylines(d, [quad.astype(np.int32)], True, (0, 255, 0), 2)
        outs.append((f, d))
    if _A.from_end: outs = outs[::-1]
    for f, d in outs:
        out_v.stdin.write(f.tobytes())
        if dbg: dbg.stdin.write(d.tobytes())
    out_v.stdin.close(); out_v.wait()
    if dbg:
        dbg.stdin.close(); dbg.wait()
    json.dump({"q0": q0.tolist(), "roof_px": [round(Wr), round(Lr)], "scale": s, "frames": log},
              open(DST.replace(".mp4", "_roof.json"), "w"))
    print(DST, len(frames), "frames; roof", round(Wr), "x", round(Lr), "px; text scale", round(s, 3))


if __name__ == "__main__":
    main()
