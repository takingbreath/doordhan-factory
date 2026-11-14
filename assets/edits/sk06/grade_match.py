#!/usr/bin/env python3
"""sk06: match the Wan 2.7 clips (the dive S1_wan27, the glide T1g) to the Wan 3.0 look Akhilesh prefers (2026-11-14:
"keep the color grade and everything similar so that it looks like it's a single video").
The transfer is measured on matching framings (the glide's very close end against the start of T1w3, the same face,
set and light): per channel in Lab, mean and standard deviation (Reinhard), averaged over 12 frame pairs. The same
transfer is then applied to every frame of the Wan 2.7 clips, as one camera's grade.
Run with pipeline/qcpy from the repository root: grade_match.py  -> vid/S1_wan27_g.mp4, vid/T1g_g.mp4, grade.json"""
import json, subprocess
import cv2, numpy as np

V = "work/sk06/vid"
W, H = 720, 1280


def frames(path, t0, t1, n):
    out = []
    for t in np.linspace(t0, t1, n):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1", "-vf",
                              f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
        out.append(np.frombuffer(raw, np.uint8).reshape(H, W, 3))
    return out


def stats(imgs):
    lab = np.concatenate([cv2.cvtColor(i, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float64) for i in imgs])
    return lab.mean(0), lab.std(0)


src_m, src_s = stats(frames(f"{V}/T1g.mp4", 3.2, 4.9, 12))
ref_m, ref_s = stats(frames(f"{V}/T1w3.mp4", 3.6, 5.6, 12))
scale, shift = ref_s / src_s, ref_m - src_m * (ref_s / src_s)
json.dump({"scale_Lab": scale.round(4).tolist(), "shift_Lab": shift.round(3).tolist(),
           "src_mean": src_m.round(2).tolist(), "ref_mean": ref_m.round(2).tolist()},
          open(f"{V}/grade.json", "w"), indent=1)
print("Lab scale", scale.round(3), "shift", shift.round(2))


def apply(src, dst):
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
                            "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip()
    rd = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-vf", f"scale={W}:{H}", "-f", "rawvideo",
                           "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    wr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                           "-r", probe, "-i", "-", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", dst],
                          stdin=subprocess.PIPE)
    n = 0
    while True:
        buf = rd.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            break
        lab = cv2.cvtColor(np.frombuffer(buf, np.uint8).reshape(H, W, 3), cv2.COLOR_BGR2LAB).astype(np.float64)
        lab = np.clip(lab * scale + shift, 0, 255).astype(np.uint8)
        wr.stdin.write(cv2.cvtColor(lab, cv2.COLOR_LAB2BGR).tobytes()); n += 1
    wr.stdin.close(); wr.wait(); rd.wait()
    print(dst, n, "frames")


apply(f"{V}/S1_wan27.mp4", f"{V}/S1_wan27_g.mp4")
apply(f"{V}/T1g.mp4", f"{V}/T1g_g.mp4")
