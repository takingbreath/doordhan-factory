#!/usr/bin/env python3
"""Remove breaths from a TTS take without touching the words.

Akhilesh, 2026-11-14 (sk06): "Remove that. Breath sounds. He's not sitting in a studio." ElevenLabs v3/v4 takes
breathe at commas, dashes and full stops; under a scene's ambience a breath reads as a studio voice.

Every 10 ms frame is classed from the sound itself (Scribe's word edges were not reliable: it stretches a word over
the breath beside it):
  - voiced (a pitch is found, with a 40 Hz floor and a 0.30 voicing threshold so creaky phrase ends count): speech,
    kept;
  - quiet (under -50 dBFS): silence, gated (no audible change);
  - unvoiced hiss (more than 45% of its energy above 4 kHz: s, sh, ch, f): kept within 0.22 s of voicing, so the "s"
    of "space" or "stock" survives the stop closure after it;
  - unvoiced and breathy (the rest): kept within 0.07 s of voicing (an aspirated "h", a stop's burst), otherwise a
    breath: gated.
Gated runs shorter than 30 ms are left alone, and so is a run under 80 ms that is louder than -40 dBFS (sk06: the
"s" of "Space" at 0.16 s, a 30 ms burst at -19 dBFS); each gated run gets 10 ms raised-cosine edges. Fill the silence with
the scene's ambience in the mix, never with room tone from the take.

Check the result: transcribe.py on OUT against the script, and compare the word list with the take's own transcript
(sk06 build_cut.py does both). Run with the QC Python (pipeline/qcpy), which has parselmouth.

Usage: debreath.py IN.wav OUT.wav [--report OUT.json]
Prints one line per gated run that held a breath (louder than -50 dBFS), with its peak."""
import argparse, json, sys, wave
import numpy as np

try:
    import parselmouth
except ImportError:
    sys.exit("debreath.py needs parselmouth: run it with pipeline/qcpy")

HOP, WIN = 0.01, 0.03
QUIET_DB = -50.0
HISS_HF, HISS_GUARD, BREATH_GUARD = 0.45, 0.22, 0.07
MIN_RUN, RAMP = 0.03, 0.01
SHORT_RUN, SHORT_LOUD_DB = 0.08, -40.0


def read_wav(path):
    """16-bit PCM wav (what ffmpeg writes by default) as float64 mono, and its rate"""
    with wave.open(path, "rb") as w:
        assert w.getsampwidth() == 2, f"{path}: 16-bit PCM expected (ffmpeg -c:a pcm_s16le)"
        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float64) / 32768.0
        ch, sr = w.getnchannels(), w.getframerate()
    return (x.reshape(-1, ch).mean(axis=1) if ch > 1 else x), sr


def write_wav(path, x, sr):
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


def classify(x, sr):
    n = int(len(x) / sr / HOP) + 1
    half = int(WIN * sr / 2)
    db, hf = np.full(n, -120.0), np.zeros(n)
    for i in range(n):
        c = int(i * HOP * sr)
        seg = x[max(0, c - half): c + half]
        if len(seg) < 64:
            continue
        db[i] = 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9)
        spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2
        fr = np.fft.rfftfreq(len(seg), 1 / sr)
        hf[i] = spec[fr > 4000].sum() / (spec.sum() + 1e-12)
    # A low floor and a permissive voicing threshold: a dry, low voice ends phrases in creak, which the default
    # tracker (70 Hz, 0.45) calls unvoiced, and this tool would then cut the syllable (sk06: "चाहिए", "हैं").
    pitch = parselmouth.Sound(x, sr).to_pitch_ac(time_step=HOP, pitch_floor=40, pitch_ceiling=450,
                                                 voicing_threshold=0.30)
    voiced = np.zeros(n, bool)
    for t, f in zip(pitch.xs(), pitch.selected_array["frequency"]):
        if f > 0:
            voiced[min(n - 1, int(round(t / HOP)))] = True
    # distance (s) from each frame to the nearest voiced frame
    vi = np.flatnonzero(voiced)
    dist = np.full(n, 99.0)
    if len(vi):
        idx = np.arange(n)
        pos = np.searchsorted(vi, idx)
        left = vi[np.clip(pos - 1, 0, len(vi) - 1)]
        right = vi[np.clip(pos, 0, len(vi) - 1)]
        dist = np.minimum(np.abs(idx - left), np.abs(right - idx)) * HOP
    keep = voiced.copy()
    loud = db > QUIET_DB
    hiss = loud & ~voiced & (hf > HISS_HF)
    breathy = loud & ~voiced & ~(hf > HISS_HF)
    keep |= hiss & (dist <= HISS_GUARD)
    keep |= breathy & (dist <= BREATH_GUARD)
    return keep, db, hf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--report")
    a = ap.parse_args()
    x, sr = read_wav(a.src)
    keep, db, hf = classify(x, sr)
    gain = np.ones(len(x))
    runs, i, n = [], 0, len(keep)
    while i < n:
        if keep[i]:
            i += 1; continue
        j = i
        while j < n and not keep[j]:
            j += 1
        if (j - i) * HOP >= MIN_RUN:
            runs.append((i, j))
        i = j
    ramp = int(RAMP * sr)
    gated = []
    for i, j in runs:
        if (j - i) * HOP < SHORT_RUN and db[i:j].max() > SHORT_LOUD_DB:
            continue          # a short, loud unvoiced bit is a consonant edge (the "s" of "Space"), not a breath
        s0, s1 = int(i * HOP * sr), min(len(x), int(j * HOP * sr))
        r = min(ramp, (s1 - s0) // 2)
        env = np.zeros(s1 - s0)
        if r > 0:
            env[:r] = 0.5 * (1 + np.cos(np.linspace(0, np.pi, r)))
            env[-r:] = 0.5 * (1 - np.cos(np.linspace(0, np.pi, r)))
        gain[s0:s1] = np.minimum(gain[s0:s1], env)
        peak = float(db[i:j].max())
        gated.append({"from": round(i * HOP, 2), "to": round(j * HOP, 2), "peak_db": round(peak, 1),
                      "hf": round(float(hf[i:j][db[i:j].argmax()]), 2)})
    write_wav(a.out, x * gain, sr)
    breaths = [g for g in gated if g["peak_db"] > QUIET_DB]
    for g in breaths:
        print(f"  {g['from']:7.2f}-{g['to']:7.2f} s  peak {g['peak_db']:6.1f} dBFS  hf {g['hf']:.2f}")
    print(f"{a.out}: {len(gated)} runs gated, {len(breaths)} held sound (breaths)")
    if a.report:
        json.dump({"gated": gated}, open(a.report, "w"), indent=1)


if __name__ == "__main__":
    main()
