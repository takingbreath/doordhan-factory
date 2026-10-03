#!/usr/bin/env python3
"""Is the mouth in time with the voice? Measures the audio-video offset of a talking shot, overall and in rolling
windows (so drift within a line shows), from two opinions:
  1. SyncNet (Chung & Zisserman 2016, pretrained syncnet_v2): a model that has learned what in-sync mouths look like.
     Primary when it's installed (torch + ~/syncnet_python + data/syncnet_v2.model; see pipeline/README.md).
  2. Correlation: mouth openness per frame from MediaPipe Face Landmarker (inner-lip gap / mouth width, 478-point
     mesh) cross-correlated with the speech envelope (common.envelope) over +-500 ms. Always runs; the fallback.

Sign convention (ITU-R BT.1359 detectability): offset = how much the SOUND LEADS the mouth, in ms.
  +  sound before the mouth (audio early)   limit +45 ms
  -  mouth before the sound (audio late)    limit -125 ms
E5 v1's bug (tracks 8.8% fast) is a negative offset that grows through each line.

Verdict: FAIL if any confident 2 s window is outside [-125, +45] ms; drift = the slope of window offsets.
Repair hint: a constant offset -> shift the part's audio in assembly (assemble.py "audio_shift_ms");
             drift within a line -> split the line into shorter shots and regenerate (no edit can fix it).

Usage: lipsync_lag.py CLIP.mp4 [--audio MASTER.wav] [--start S --end E] [--win 2 --hop 1] [--json OUT]
       [--method auto|corr|syncnet] [--lo -125 --hi 45]
  --audio: judge the clip's picture against another audio file (the edit's master), from the same --start.
  --start/--end: a time range, e.g. one talking segment of a finished reel. Frames with no face are skipped."""
import argparse, json, os, subprocess, sys
import numpy as np

here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from common import FFMPEG, FFPROBE, envelope  # noqa: E402

ROOT = os.path.dirname(here)
MODEL = os.path.join(ROOT, "assets", "models", "face_landmarker.task")
SYNCNET_DIR = os.environ.get("SYNCNET_DIR", os.path.expanduser("~/syncnet_python"))
FPS = 25.0            # analysis rate for the correlation method (SyncNet needs 25 fps)
MAXLAG = 0.5          # seconds searched each way
MIN_CONF = 0.30       # a window's correlation peak below this is "no opinion", not a failure
# inner-lip pairs (upper, lower) and mouth corners on the 478-point Face Landmarker mesh
LIP_PAIRS = [(82, 87), (13, 14), (312, 317)]
CORNERS = (61, 291)


def probe(path):
    r = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height:format=duration", "-of", "json", path], capture_output=True, text=True)
    j = json.loads(r.stdout)
    s = j["streams"][0]
    return int(s["width"]), int(s["height"]), float(j["format"]["duration"])


def frames(path, start, dur, width=None):
    w0, h0, _ = probe(path)
    width = width or min(720, w0 - w0 % 2)
    h = int(round(h0 * width / w0 / 2)) * 2
    cmd = [FFMPEG, "-v", "error", "-ss", f"{start:.3f}", "-i", path, "-t", f"{dur:.3f}",
           "-vf", f"fps={FPS},scale={width}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    n = len(raw) // (width * h * 3)
    return np.frombuffer(raw[: n * width * h * 3], np.uint8).reshape(n, h, width, 3)


def mouth_openness(fr):
    """per-frame inner-lip gap / mouth width (NaN where no face) and the mouth box per frame (for SyncNet)"""
    import mediapipe as mp
    from mediapipe.tasks.python import vision, BaseOptions
    opts = vision.FaceLandmarkerOptions(base_options=BaseOptions(model_asset_path=MODEL),
                                        running_mode=vision.RunningMode.VIDEO, num_faces=1,
                                        min_face_detection_confidence=0.3, min_tracking_confidence=0.3)
    out, boxes, mw = np.full(len(fr), np.nan), [None] * len(fr), np.full(len(fr), np.nan)
    with vision.FaceLandmarker.create_from_options(opts) as lm:
        for i, f in enumerate(fr):
            res = lm.detect_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(f)),
                                      int(i * 1000 / FPS))
            if not res.face_landmarks:
                continue
            p = np.array([[q.x * f.shape[1], q.y * f.shape[0]] for q in res.face_landmarks[0]])
            width = np.linalg.norm(p[CORNERS[0]] - p[CORNERS[1]])
            if width < 5:
                continue
            out[i] = np.mean([np.linalg.norm(p[a] - p[b]) for a, b in LIP_PAIRS]) / width
            mw[i] = width
            # face box for SyncNet: from the whole mesh
            x0, y0 = p.min(0); x1, y1 = p.max(0)
            boxes[i] = (x0, y0, x1, y1)
    return out, boxes, mw


def audio_env(path, start, dur, n):
    """linear speech envelope at the analysis rate, aligned with the frames"""
    tmp = os.path.join("/tmp", f"lsl_{os.getpid()}.wav")
    subprocess.run([FFMPEG, "-v", "error", "-y", "-ss", f"{start:.3f}", "-i", path, "-t", f"{dur:.3f}", "-vn",
                    "-ac", "1", "-ar", "16000", tmp], check=True)
    db = envelope(tmp, win=1 / FPS, sr=16000)
    os.remove(tmp)
    lin = 10 ** (np.maximum(db, -60) / 20)
    lin = np.pad(lin, (0, max(0, n - len(lin))))[:n]
    return lin, db[:n] if len(db) >= n else np.pad(db, (0, n - len(db)), constant_values=-90)


def xcorr_lag(m, e, valid, maxlag):
    """best lag in frames (+ = sound leads the mouth: the mouth trails the envelope), peak r, with parabolic refinement"""
    L = int(round(maxlag * FPS)); rs = []
    for k in range(-L, L + 1):
        # mouth at t pairs with sound at t - k  (k>0: the sound came k frames earlier)
        if k >= 0:
            a, b, v = m[k:], e[: len(e) - k], valid[k:] & valid[: len(valid) - k]
        else:
            a, b, v = m[: len(m) + k], e[-k:], valid[: len(valid) + k] & valid[-k:]
        if v.sum() < 0.6 * FPS:
            rs.append(np.nan); continue
        a, b = a[v], b[v]
        if a.std() < 1e-6 or b.std() < 1e-6:
            rs.append(np.nan); continue
        rs.append(float(np.corrcoef(a, b)[0, 1]))
    rs = np.array(rs)
    if np.all(np.isnan(rs)):
        return None, None
    i = int(np.nanargmax(rs)); peak = rs[i]; frac = 0.0
    if i <= 1 or i >= len(rs) - 2:     # peak at the search edge: the true lag is outside the range, or it's noise
        return None, None
    if 0 < i < len(rs) - 1 and not np.isnan(rs[i - 1]) and not np.isnan(rs[i + 1]):
        d = rs[i - 1] - 2 * rs[i] + rs[i + 1]
        if d < 0:
            frac = 0.5 * (rs[i - 1] - rs[i + 1]) / d
    return (i - L + frac) / FPS * 1000.0, peak


def windows(n, win, hop):
    W, Hh = int(win * FPS), int(hop * FPS)
    if n <= W:
        return [(0, n)]
    s = list(range(0, n - W + 1, Hh))
    if s[-1] + W < n:
        s.append(n - W)
    return [(a, a + W) for a in s]


def corr_method(m, e, db, args):
    valid = ~np.isnan(m)
    mm = np.where(valid, m, np.nanmean(m) if valid.any() else 0)
    # standardise the mouth signal; take the envelope in dB-ish compressed form, which follows syllables better
    ee = np.sqrt(e)
    speech = db > -45
    overall, conf = xcorr_lag(mm, ee, valid, MAXLAG)
    wins = []
    for a, b in windows(len(m), args.win, args.hop):
        # widen by the search range so lags near the window edge still see data
        pa, pb = max(0, a), min(len(m), b)
        sp = speech[pa:pb].mean()
        off, r = xcorr_lag(mm[pa:pb], ee[pa:pb], valid[pa:pb], MAXLAG)
        wins.append({"t": round(a / FPS, 2), "offset_ms": None if off is None else round(off),
                     "r": None if r is None else round(r, 2), "speech": round(float(sp), 2),
                     "face": round(float(valid[pa:pb].mean()), 2)})
    return overall, conf, wins


# ------------------------------------------------------------------ SyncNet (optional, primary when available)
def syncnet_available():
    try:
        import torch  # noqa: F401
        return os.path.exists(os.path.join(SYNCNET_DIR, "data", "syncnet_v2.model"))
    except Exception:
        return False


def syncnet_method(fr, boxes, audio_path, start, dur, args, speech=None):
    """SyncNet offset per window: the classic 'av offset' search (+-15 frames at 25 fps) on 224x224 face crops.
    SyncNet reports offset in frames with + meaning the audio must be shifted later, i.e. the sound leads."""
    import torch, python_speech_features
    sys.path.insert(0, SYNCNET_DIR)
    from SyncNetModel import S as SyncNetS
    net = SyncNetS(num_layers_in_fc_layers=1024)
    state = torch.load(os.path.join(SYNCNET_DIR, "data", "syncnet_v2.model"), map_location="cpu")
    own = net.state_dict()
    for k, v in state.items():
        if k in own:
            own[k].copy_(v)
    net.eval()
    # face crops: a steady square box around the lower-face-inclusive mesh box, smoothed over time
    ok = [b for b in boxes if b is not None]
    if len(ok) < 10:
        return None
    B = np.array([b if b is not None else (np.nan,) * 4 for b in boxes], float)
    for j in range(4):
        col = B[:, j]; idx = np.where(~np.isnan(col))[0]
        B[:, j] = np.interp(np.arange(len(col)), idx, col[idx])
    k = 5; B = np.array([B[max(0, i - k):i + k + 1].mean(0) for i in range(len(B))])
    crops = []
    H, Wd = fr.shape[1], fr.shape[2]
    import cv2
    for f, (x0, y0, x1, y1) in zip(fr, B):
        cx, cy, s = (x0 + x1) / 2, (y0 + y1) / 2, max(x1 - x0, y1 - y0) * 0.65
        xa, ya, xb, yb = int(cx - s), int(cy - s), int(cx + s), int(cy + s)
        pad = np.pad(f, ((s_ := int(s) + 2, s_), (s_, s_), (0, 0)), mode="edge")
        c = pad[ya + s_:yb + s_, xa + s_:xb + s_]
        crops.append(cv2.resize(c, (224, 224)))
    crops = np.stack(crops)
    # audio MFCC at 100 Hz (SyncNet's front end)
    tmp = os.path.join("/tmp", f"lss_{os.getpid()}.wav")
    subprocess.run([FFMPEG, "-v", "error", "-y", "-ss", f"{start:.3f}", "-i", audio_path, "-t", f"{dur:.3f}", "-vn",
                    "-ac", "1", "-ar", "16000", tmp], check=True)
    import wave
    with wave.open(tmp) as w:
        sig = np.frombuffer(w.readframes(w.getnframes()), np.int16)
    os.remove(tmp)
    mfcc = np.stack([np.array(i) for i in zip(*python_speech_features.mfcc(sig, 16000))])  # (13, T)
    nf = min(len(crops), int(mfcc.shape[1] / 4))
    crops = crops[:nf]
    ims = torch.from_numpy(crops[None].transpose(0, 4, 1, 2, 3).astype(np.float32))  # 1,3,T,224,224
    cc = torch.from_numpy(mfcc[None, None].astype(np.float32))                        # 1,1,13,T*4
    lastframe = nf - 5
    with torch.no_grad():
        im_feat, cc_feat = [], []
        for i in range(0, lastframe, 20):
            e = min(lastframe, i + 20)
            im_in = torch.cat([ims[:, :, v:v + 5] for v in range(i, e)], 0)
            cc_in = torch.cat([cc[:, :, :, v * 4:v * 4 + 20] for v in range(i, e)], 0)
            im_feat.append(net.forward_lip(im_in)); cc_feat.append(net.forward_aud(cc_in))
        im_feat, cc_feat = torch.cat(im_feat, 0), torch.cat(cc_feat, 0)
    vshift = 15
    cc_pad = torch.nn.functional.pad(cc_feat, (0, 0, vshift, vshift))
    dists = torch.stack([torch.nn.functional.pairwise_distance(im_feat[[i], :].repeat(vshift * 2 + 1, 1),
                                                               cc_pad[i:i + vshift * 2 + 1, :])
                         for i in range(len(im_feat))]).numpy()          # (N, 31): per frame, per candidate shift

    face = np.array([b is not None for b in boxes[:len(dists)]], float)

    def score(a, b):
        d = dists[a:b][face[a:b] > 0].mean(0) if face[a:b].sum() >= 5 else dists[a:b].mean(0)
        i = int(np.argmin(d)); conf = float(np.median(d) - d[i])
        if i == 0 or i == len(d) - 1:   # pinned at the +-600 ms search edge: no reading
            conf = 0.0
        # SyncNet convention: offset = vshift - argmin  (frames; + = audio leads the video)
        return (vshift - i) * 40.0, conf
    overall, conf = score(0, len(dists))
    wins = []
    for a, b in windows(len(dists), args.win, args.hop):
        off, c = score(a, b)
        wins.append({"t": round(a / FPS, 2), "offset_ms": round(off), "conf": round(c, 2),
                     "face": round(float(face[a:b].mean()), 2),
                     "speech": round(float(speech[a:b].mean()), 2) if speech is not None else 1.0})
    return overall, conf, wins


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip"); ap.add_argument("--audio"); ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float); ap.add_argument("--win", type=float, default=2.0)
    ap.add_argument("--hop", type=float, default=1.0); ap.add_argument("--lo", type=float, default=-125)
    ap.add_argument("--hi", type=float, default=45); ap.add_argument("--json")
    ap.add_argument("--method", default="auto", choices=["auto", "corr", "syncnet"])
    ap.add_argument("--label", default="")
    a = ap.parse_args()
    _, _, D = probe(a.clip)
    end = min(a.end if a.end else D, D)
    dur = end - a.start
    fr = frames(a.clip, a.start, dur)
    m, boxes, mw = mouth_openness(fr)
    audio_path = a.audio or a.clip
    e, db = audio_env(audio_path, a.start, dur, len(m))
    res = {"clip": a.clip, "label": a.label, "start": a.start, "end": round(end, 2), "face_frames": round(float(np.mean(~np.isnan(m))), 2)}
    c_over, c_conf, c_wins = corr_method(m, e, db, a)
    res["corr"] = {"offset_ms": None if c_over is None else round(c_over), "r": None if c_conf is None else round(c_conf, 2),
                   "windows": c_wins}
    method = a.method
    if method in ("auto", "syncnet") and syncnet_available():
        try:
            s = syncnet_method(fr, boxes, audio_path, a.start, dur, a, speech=db > -45)
            if s:
                res["syncnet"] = {"offset_ms": s[0], "conf": round(s[1], 2), "windows": s[2]}
        except Exception as ex:  # keep the correlation verdict if SyncNet breaks
            res["syncnet_error"] = str(ex)[-300:]
    primary = "syncnet" if "syncnet" in res and method != "corr" else "corr"
    P = res[primary]
    if primary == "syncnet":
        judged = [w for w in P["windows"] if w["conf"] >= args_min_conf_syncnet and w["face"] >= 0.8
                  and w["speech"] >= 0.4]
    else:
        judged = [w for w in P["windows"] if w["r"] is not None and w["r"] >= MIN_CONF and w["speech"] >= 0.3
                  and w["face"] >= 0.6]
    bad = [w for w in judged if not (a.lo <= w["offset_ms"] <= a.hi)]
    offs = np.array([w["offset_ms"] for w in judged], float)
    ts = np.array([w["t"] for w in judged], float)
    slope = float(np.polyfit(ts, offs, 1)[0]) if len(judged) >= 2 and np.ptp(ts) > 0 else 0.0
    spread = float(offs.max() - offs.min()) if len(offs) else 0.0
    res.update(primary=primary, judged_windows=len(judged), drift_ms_per_s=round(slope, 1), spread_ms=round(spread),
               failing_windows=[w["t"] for w in bad])
    if not judged:
        res["verdict"] = "UNSURE (no confident window: no face, no speech, or no correlation)"
    elif not bad:
        res["verdict"] = "PASS"
    else:
        res["verdict"] = "FAIL"
    res["mouth_px"] = round(float(np.nanmedian(mw)), 1) if np.any(~np.isnan(mw)) else None
    confs = [w.get("conf", w.get("r")) or 0 for w in P["windows"] if w.get("speech", 1) >= 0.4]
    res["median_conf"] = round(float(np.median(confs)), 2) if confs else None
    weak = (res["mouth_px"] is not None and res["mouth_px"] < WEAK_MOUTH_PX) or \
           (primary == "syncnet" and res["median_conf"] is not None and res["median_conf"] < WEAK_CONF)
    drifting = len(judged) >= 2 and abs(slope) >= 25 and spread >= 100
    # judged against its own audio (the track the model was driven with), a clip can't really drift 40+ ms/s: Wan's
    # own timing drifts about -8 ms/s. A steep "drift" there means the mouth isn't following the audio at all.
    own_audio = a.audio is None and a.start == 0 and a.end is None
    if drifting and own_audio and abs(slope) > 40:
        drifting, weak = False, True
    if weak and res.get("verdict") == "FAIL" and not drifting:
        res["pattern"] = "weak lips"
        res["repair"] = (f"the lips barely track the audio (mouth {res['mouth_px']} px wide, SyncNet confidence "
                         f"{res['median_conf']}): an offset or drift reading here is unreliable. Regenerate from a "
                         "tighter keyframe (face larger in frame, mouth unobstructed) rather than shifting audio.")
    elif judged:
        if abs(slope) >= 25 and spread >= 100:
            res["pattern"] = "drift"
            res["repair"] = ("offset drifts within the line: an audio shift can't fix it. Check the track speed "
                             "(make_track), then split the line into shots of about 6 s or less and regenerate.")
        else:
            med = float(np.median(offs))
            res["pattern"] = "constant"
            res["median_offset_ms"] = round(med)
            # a shift fixes it when every judged window fits inside the pass window at once (a constant offset, or
            # Wan's mild -8 ms/s drift over a long line: E5 v4 P4 ran -80..-160 ms). Shifting the audio by S ms moves
            # every offset by -S: centre the judged range on the middle of the window.
            if bad and spread <= (a.hi - a.lo) - 20:
                mid = (float(offs.max()) + float(offs.min())) / 2
                sh = int(round(mid - REPAIR_TARGET_MS))
                res["audio_shift_ms"] = sh
                res["repair"] = (f'offset {offs.min():.0f}..{offs.max():.0f} ms: set "audio_shift_ms": {sh} on this part in edit.json '
                                 f'({"pulls the audio earlier" if sh < 0 else "delays the audio"} by {abs(sh)} ms; '
                                 f'lands near {REPAIR_TARGET_MS} ms). In a custom edit (build.py) move the clip\'s '
                                 f'source start (src_in) by {sh / 1000:+.3f} s instead.')
    if a.json:
        json.dump(res, open(a.json, "w"), indent=1)
    wins = P["windows"]
    key = "conf" if primary == "syncnet" else "r"
    print(f"{a.label or os.path.basename(a.clip)}: {res['verdict']}  [{primary}] overall {P['offset_ms']} ms "
          f"({key} {P.get(key)})  drift {res['drift_ms_per_s']} ms/s  spread {res['spread_ms']} ms  "
          f"pattern {res.get('pattern', '-')}")
    print("  windows (t: offset ms/" + key + "): " + "  ".join(
        f"{w['t']:.0f}s:{w['offset_ms']}/{w.get(key)}" for w in wins))
    if primary == "syncnet":
        print(f"  corr fallback: overall {res['corr']['offset_ms']} ms (r {res['corr']['r']})")
    if res.get("repair"):
        print("  repair:", res["repair"])


args_min_conf_syncnet = 1.5   # SyncNet confidence (median - min distance) below this is "no opinion"
WEAK_MOUTH_PX = 40           # mouth corner-to-corner width at native res; below this readings are unreliable
WEAK_CONF = 2.0
REPAIR_TARGET_MS = -40        # a repaired part is centred here: the middle of the -125..+45 pass window

if __name__ == "__main__":
    main()
