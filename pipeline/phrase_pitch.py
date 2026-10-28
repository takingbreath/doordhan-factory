#!/usr/bin/env python3
"""Does one phrase of a take sound excited? (anthropic01, 2026-10-28: Akhilesh heard "jise tum kabhi khareed nahi
paoge" as excited, "the pitch is up when it is not supposed to be".) Splits a take at a word and compares the pitch
of the part from that word on with the part before it, in semitones: the median, the peak (95th percentile), the last
word, and the part's range. On v3's hook the second half sat +1.7 st above the first and peaked +6.0 st; the calm
retake that Akhilesh chose sat +0.3 st and its last word fell 6.7 st. Words come from transcribe.py's --json.
Run with pipeline/qcpy (parselmouth).
Usage: phrase_pitch.py --split WORD AUDIO SCRIBE.json [AUDIO SCRIBE.json ...]"""
import argparse, json, os, subprocess, tempfile
import numpy as np
import parselmouth


def analyse(audio, scribe, split):
    words = [w for w in json.load(open(scribe))["words"] if w.get("type", "word") == "word"]
    i = next(k for k, w in enumerate(words) if w["text"].strip(",.।?!") == split)
    tmp = tempfile.mktemp(suffix=".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", audio, "-ac", "1", "-ar", "16000", tmp], check=True)
    p = parselmouth.Sound(tmp).to_pitch(time_step=0.01, pitch_floor=120, pitch_ceiling=500)
    t, f = p.xs(), p.selected_array["frequency"]; os.remove(tmp)

    def st(a, b):
        sel = (t >= a) & (t <= b) & (f > 0)
        return 12 * np.log2(f[sel] / 200.0)
    first, second = st(words[0]["start"], words[i - 1]["end"]), st(words[i]["start"], words[-1]["end"])
    last = st(words[-1]["start"], words[-1]["end"]); base = np.median(first)
    return {"length_s": round(words[-1]["end"], 2), "median_st": round(float(np.median(second) - base), 1),
            "peak_st": round(float(np.percentile(second, 95) - base), 1), "last_word_st": round(float(np.median(last) - base), 1),
            "range_st": round(float(np.percentile(second, 95) - np.percentile(second, 5)), 1)}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--split", required=True); ap.add_argument("pairs", nargs="+")
    a = ap.parse_args()
    if len(a.pairs) % 2: ap.error("give AUDIO SCRIBE.json pairs")
    for audio, scribe in zip(a.pairs[::2], a.pairs[1::2]):
        r = analyse(audio, scribe, a.split)
        print(f"{os.path.basename(audio):24s} from '{a.split}' vs before: median {r['median_st']:+5.1f} st, peak "
              f"{r['peak_st']:+5.1f} st, last word {r['last_word_st']:+5.1f} st, range {r['range_st']:4.1f} st, "
              f"length {r['length_s']} s")


if __name__ == "__main__":
    main()
