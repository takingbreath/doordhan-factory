"""Shared helpers for the Doordhan pipeline. Requires ffmpeg/ffprobe on PATH, Python 3.9+, numpy, pillow."""
import shutil, subprocess
import numpy as np

FFMPEG = shutil.which("ffmpeg") or "ffmpeg"
FFPROBE = shutil.which("ffprobe") or "ffprobe"
W, H, FPS = 720, 1280, 25         # edit size (9:16; Wan 720p delivers 718x1282) and 25 fps, the Indian (PAL) TV rate.
                                  # The old-TV softness is made on purpose in look.py, not by shrinking the edit.
AW, AH = 480, 854                 # analysis frame: lipcheck boxes and inset-box coordinates are given in this frame
S = W / AW                        # analysis -> edit scale


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("command failed:\n" + " ".join(map(str, cmd)) + "\n" + r.stderr[-3000:])
    return r


def duration(path):
    r = run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)])
    return float(r.stdout.strip())


def loudness(path):
    """Integrated loudness (LUFS) and true peak (dBFS)."""
    r = subprocess.run([FFMPEG, "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True)
    I = P = None
    for line in r.stderr.splitlines():
        s = line.strip()
        if s.startswith("I:"):
            I = float(s.split()[1])
        elif s.startswith("Peak:"):
            P = float(s.split()[1])
    return I, P


def envelope(path, win=0.05, sr=8000):
    """Loudness per window (dBFS). Works on audio or video files."""
    raw = subprocess.run([FFMPEG, "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(float)
    w = int(sr * win)
    n = len(x) // w
    if n == 0:
        return np.array([])
    x = x[: n * w].reshape(n, w)
    return 20 * np.log10(np.sqrt((x ** 2).mean(axis=1) + 1e-9)) - 90.3


def speech_map(path, thresh=-38.0, min_gap=0.2, win=0.05):
    """Where speech starts/ends and where the pauses are. Use this to choose cut points."""
    db = envelope(path, win)
    on = np.where(db > thresh)[0]
    if len(on) == 0:
        return {"start": None, "end": None, "pauses": [], "duration": round(float(len(db) * win), 2)}
    pauses, prev = [], on[0]
    for i in on[1:]:
        if (i - prev) * win > min_gap:
            pauses.append((round(float((prev + 1) * win), 2), round(float(i * win), 2)))
        prev = i
    return {"start": round(float(on[0] * win), 2), "end": round(float((on[-1] + 1) * win), 2), "pauses": pauses,
            "duration": round(float(len(db) * win), 2)}


def silence(path, seconds, sr=48000, layout="mono"):
    run([FFMPEG, "-y", "-v", "error", "-f", "lavfi", "-i", f"anullsrc=r={sr}:cl={layout}", "-t", f"{seconds}", str(path)])
