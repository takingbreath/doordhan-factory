"""Mockumentary camera test (The Office style) on a locked-off Wan clip: handheld operator drift, a snap zoom that
overshoots and settles with a brief focus hunt, a late reframe, and a whip pan out. All in the edit; no regeneration."""
import cv2, numpy as np, math, subprocess
cap = cv2.VideoCapture("src.mp4"); frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f)
H0, W0 = frames[0].shape[:2]; FPS = 30; OW, OH = 1080, 1920
FACE = (490, 760)                      # face centre in the source
def handheld(t, amp=1.0):
    # operator sway: a few slow sines + a little faster breathing jitter (px in source space, degrees)
    x = amp * (5.5*math.sin(2*math.pi*0.31*t+1.0) + 2.5*math.sin(2*math.pi*0.83*t+2.1) + 0.9*math.sin(2*math.pi*2.3*t))
    y = amp * (4.0*math.sin(2*math.pi*0.27*t+0.4) + 2.0*math.sin(2*math.pi*0.71*t+1.3) + 0.7*math.sin(2*math.pi*2.9*t+0.5))
    r = amp * (0.35*math.sin(2*math.pi*0.23*t+0.7) + 0.12*math.sin(2*math.pi*1.1*t))
    return x, y, r
def snap(t, t0, z0, z1, dur=0.22):
    """fast zoom with ~6% overshoot, then a damped settle (like a hand on the zoom rocker)"""
    if t < t0: return z0, 0.0
    x = (t - t0) / dur
    if x < 1:
        e = 1 - (1 - x) ** 3; return z0 + (z1 - z0) * e * 1.06, x      # still moving: blur weight
    s = t - t0 - dur
    return z1 + (z1 - z0) * 0.06 * math.exp(-s * 7) * math.cos(s * 18), 0.0
out = []
n = len(frames)
for i in range(n):
    t = i / FPS
    z, moving = snap(t, 1.55, 1.08, 1.50)
    cx, cy = W0/2 + (FACE[0]-W0/2) * min(1, max(0, (z-1.08)/0.42)), H0/2 + (FACE[1]-H0/2) * min(1, max(0, (z-1.08)/0.42))
    if t > 3.4:                                   # late reframe: the operator nudges right and up after the line
        k = min(1, (t-3.4)/0.5); k = k*k*(3-2*k); cx += 22*k; cy -= 14*k
    hx, hy, hr = handheld(t, 1.0 + 0.6*(z-1.08))
    whip = max(0.0, (t - 4.45) / 0.45)            # whip pan out at the end
    wx = 0 if whip <= 0 else (whip ** 2) * 900
    M = cv2.getRotationMatrix2D((cx + hx, cy + hy), hr, z)
    M[0, 2] += W0/2 - (cx + hx) - wx; M[1, 2] += H0/2 - (cy + hy)
    f = cv2.warpAffine(frames[i], M, (W0, H0), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    if moving > 0:                                # motion blur + focus hunt during the zoom
        f = cv2.GaussianBlur(f, (0, 0), 1.6 * math.sin(math.pi * moving) + 0.01)
    elif 1.77 < t < 2.05:                         # focus breathes once after landing
        f = cv2.GaussianBlur(f, (0, 0), 0.9 * math.sin(math.pi * (t - 1.77) / 0.28) + 0.01)
    if wx > 0:
        k = int(10 + 60 * whip) | 1; ker = np.zeros((1, k), np.float32); ker[0, :] = 1 / k
        f = cv2.filter2D(f, -1, ker)
    out.append(cv2.resize(f, (OW, OH), interpolation=cv2.INTER_CUBIC))
p = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{OW}x{OH}","-r",str(FPS),"-i","-",
    "-i","src.mp4","-map","0:v","-map","1:a?","-c:v","libx264","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-shortest","camtest_mockumentary.mp4"],stdin=subprocess.PIPE)
for f in out: p.stdin.write(f.tobytes())
p.stdin.close(); p.wait(); print("ok", n)
