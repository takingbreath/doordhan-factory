#!/usr/bin/env python3
"""How flat is a voice take? Pitch and pace numbers that track "sounds monotone / AI-like".

  python3 pipeline/prosody.py take.mp3 [more.mp3 ...] [--male]   (--male lowers the pitch floor to 70 Hz)

Per file:
  range_st   pitch range in semitones (5th to 95th percentile of voiced F0). Natural conversational
             Hindi/English storytelling usually sits around 8-12 st; under ~6 st reads flat.
  sd_st      standard deviation of pitch in semitones (natural speech is roughly 2.5-4).
  move_st    median absolute pitch movement per 100 ms: how much the melody moves inside phrases.
  phrase_sd  spread of each phrase's median pitch (semitones): do phrases start high/low differently,
             or does every sentence sit on the same note? Near 0 = "one pitch for the whole thing".
  pace_cv    spread of phrase speaking rates (voiced-time share) - natural speech speeds up and slows down.
  shape_r    mean correlation between the pitch shapes of phrases (each resampled to 20 points). High
             (> ~0.5) = every sentence has the same tune, the "reading" sound; told stories vary.
  pause_cv   spread of pause lengths. TTS pauses the same after every full stop (low); people don't.
  tail_fall  median pitch drop over each phrase's last 300 ms (semitones). A big, identical fall at
             every sentence end is the newsreader cadence.
Phrases are split at silences of 200 ms or more. Needs praat-parselmouth (pip install praat-parselmouth).
"""
import sys, subprocess, tempfile, os
import numpy as np
import parselmouth


def load(path):
    tmp = tempfile.mktemp(suffix=".wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", "16000", tmp], check=True)
    s = parselmouth.Sound(tmp); os.remove(tmp); return s


def analyse(path, floor=120, ceil=500):
    snd = load(path)
    pitch = snd.to_pitch_ac(time_step=0.01, pitch_floor=floor, pitch_ceiling=ceil)
    f0 = pitch.selected_array["frequency"]; t = pitch.xs()
    voiced = f0 > 0
    st = np.full_like(f0, np.nan); st[voiced] = 12 * np.log2(f0[voiced] / 100.0)
    v = st[voiced]
    rng = np.percentile(v, 95) - np.percentile(v, 5)
    # movement per 100 ms inside voiced runs
    d = st[10:] - st[:-10]; d = d[~np.isnan(d)]
    move = np.median(np.abs(d)) if len(d) else 0
    # phrases from intensity silences
    inten = snd.to_intensity(time_step=0.01); it = inten.xs(); iv = inten.values[0]
    loud = iv > (np.percentile(iv, 90) - 25)
    phrases, start, gap = [], None, 0
    for i, on in enumerate(loud):
        if on:
            if start is None: start = it[i]
            gap = 0; end = it[i]
        elif start is not None:
            gap += 1
            if gap >= 20: phrases.append((start, end)); start = None
    if start is not None: phrases.append((start, it[-1]))
    meds, paces, shapes, tails = [], [], [], []
    for a, b in phrases:
        m = (t >= a) & (t <= b)
        pv = st[m]; pv = pv[~np.isnan(pv)]
        if b - a > 0.6 and len(pv) > 10:
            meds.append(np.median(pv)); paces.append(len(pv) / (m.sum() or 1))
            seg = st[m]; idx = np.where(~np.isnan(seg))[0]
            if len(idx) > 10:
                y = np.interp(np.arange(len(seg)), idx, seg[idx]); x = np.linspace(0, len(y) - 1, 20)
                shapes.append(np.interp(x, np.arange(len(y)), y) - np.median(y))
                tl = seg[-30:]; tl = tl[~np.isnan(tl)]
                if len(tl) > 4: tails.append(tl[0] - tl[-1])
    rs = [np.corrcoef(shapes[i], shapes[j])[0, 1] for i in range(len(shapes)) for j in range(i + 1, len(shapes))]
    pauses = [phrases[i + 1][0] - phrases[i][1] for i in range(len(phrases) - 1)]
    return dict(file=os.path.basename(path), dur=round(snd.duration, 1), range_st=round(rng, 1), sd_st=round(np.std(v), 2),
                move_st=round(move, 2), phrases=len(meds), phrase_sd=round(np.std(meds), 2) if meds else 0,
                pace_cv=round(np.std(paces) / np.mean(paces), 2) if paces else 0,
                shape_r=round(float(np.nanmean(rs)), 2) if rs else 0,
                pause_cv=round(np.std(pauses) / np.mean(pauses), 2) if len(pauses) > 1 else 0,
                tail_fall=round(float(np.median(tails)), 1) if tails else 0)


if __name__ == "__main__":
    keys = ["file", "dur", "range_st", "sd_st", "move_st", "phrases", "phrase_sd", "pace_cv", "shape_r", "pause_cv", "tail_fall"]
    print("  ".join(f"{k:>10}" for k in keys))
    args = sys.argv[1:]; floor = 120
    if "--male" in args: args.remove("--male"); floor = 70
    for p in args:
        r = analyse(p, floor, 400 if floor < 100 else 500); print("  ".join(f"{str(r[k])[-28:]:>10}" for k in keys))
