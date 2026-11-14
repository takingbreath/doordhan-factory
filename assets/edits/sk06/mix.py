#!/usr/bin/env python3
"""sk06 sound: the approved voice (voice2/sk06_voice_v2.wav) at 0.12 s, the bus inside, the street outside (the dive
and the outro, so the loop joins on the same sound), the two bus brakes, the windscreen whoosh, a whoosh on every whip,
a thud on every word and logo, marker sounds on the chart marks. No music: Akhilesh lays the song in Instagram Edits
(sfx/cues.json, rebuilt by cue_sheet.py). Cue times = the edit's (rm/src/Reel.tsx). Writes mix/sk06_mix.wav (-14 LUFS).
Run from the repository root: python3 work/sk06/mix.py"""
import json, os, subprocess
import numpy as np

SK = "work/sk06"; A = "assets/audio"; SR = 48000
TOTAL = 111.77                      # rm/src/Reel.tsx TOTAL (v2: the outro starts at clip 0.9 s)
EXIT = 106.20                       # the outro camera leaves the bus through the windscreen
os.makedirs(f"{SK}/mix", exist_ok=True)


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def db(x): return 10 ** (x / 20)


out = np.zeros(int(TOTAL * SR) + SR, np.float32)


def put(x, at, gain_db=0.0, fade_in=0.0, fade_out=0.0, length=None):
    x = x[: int(length * SR)] if length else x.copy()
    x = x * db(gain_db)
    n = len(x)
    if fade_in: k = min(n, int(fade_in * SR)); x[:k] *= np.linspace(0, 1, k)
    if fade_out: k = min(n, int(fade_out * SR)); x[n - k:] *= np.linspace(1, 0, k)
    i = int(at * SR); j = min(len(out), i + n)
    if j > i: out[i:j] += x[: j - i]


def loop(x, dur, xf=1.0):
    """repeat a bed with crossfades to the length dur"""
    res = np.zeros(int(dur * SR) + SR, np.float32); pos = 0; k = int(xf * SR); ramp = np.linspace(0, 1, k)
    while pos < len(res):
        seg = x.copy(); seg[:k] *= ramp; seg[-k:] *= ramp[::-1]
        e = min(len(res), pos + len(seg)); res[pos:e] += seg[: e - pos]; pos += len(seg) - k
    return res[: int(dur * SR)]


# ---- voice
voice = load(f"{SK}/voice2/sk06_voice_v2.wav")
put(voice, 0.12)

# ---- the bus inside: 1.30 (the camera passes the windscreen) to 107.05 (it leaves through it), under everything
bed = np.concatenate([load(f"{SK}/sfx/bus_bed_a.mp3"), load(f"{SK}/sfx/bus_bed_c.mp3"), load(f"{SK}/sfx/bus_bed_b.mp3")])
bus = loop(bed, EXIT + 0.45 - 1.25)
env = np.ones_like(bus)
t = np.arange(len(bus)) / SR + 1.25
for a, b in [(7.30, 11.95), (17.60, 24.62), (29.40, 45.80), (45.80, 52.55), (55.92, 61.20), (68.75, 85.30), (91.90, 96.65)]:  # away from the bus (B-roll, cards, charts): the bus further away
    env[(t > a) & (t < b)] = db(-5)
k = int(0.25 * SR); cs = np.cumsum(np.concatenate([np.full(k // 2, env[0]), env, np.full(k - k // 2, env[-1])]))
env = ((cs[k:] - cs[:-k]) / k)[: len(bus)].astype(np.float32)            # a 0.25 s moving average (fast)
put(bus * env, 1.25, -21, fade_in=0.35, fade_out=0.5)
# ---- the street outside: the dive (to the windscreen) and the outro (from the windscreen to the top shot), same level
street = load(f"{SK}/sfx/street_top.mp3")
put(street, 0.0, -17, fade_out=0.45, length=1.75)
put(loop(street, TOTAL - (EXIT - 0.15)), EXIT - 0.15, -17, fade_in=0.45)
# the windscreen pass, both ways
gw = load(f"{SK}/sfx/glass_whoosh.mp3")
put(gw, 1.10, -11); put(gw, EXIT - 0.25, -11)

# ---- the brakes
brake = load(f"{SK}/sfx/brake_bus.wav")
put(brake, 52.55, -3, fade_out=0.6)
put(brake, 104.86, -3, fade_out=0.8, length=2.6)

# ---- whips, words, logos, marks
wh, th, pop, mk, scr, clk, sl = (load(f"{A}/{n}.wav") for n in ["sfx_whoosh", "sfx_thud", "sfx_pop", "sfx_marker", "sfx_scribble", "sfx_click", "sfx_slap"])
for c in [7.30, 24.62, 55.92, 85.30]:                                  # only the big whips get a whoosh (v3: fewer, softer)
    put(wh, c - 0.19, -13)
for c in [29.40, 45.80, 91.90]:                                         # zoom-through into a chart: a low thump, no whoosh
    put(th, c + 0.02, -14)
for w in [5.04, 6.36, 54.48, 103.76]:                                  # the words that matter: SPACE, SEMICONDUCTORS x2, SETUP
    put(th, w - 0.01, -7)
for w in [18.08, 37.22, 68.94, 77.38]:                                  # NO. 1 / NO. 2 slams
    put(th, w - 0.01, -7)
for l in [8.86, 9.76, 10.70, 19.60, 38.74, 70.50, 72.58, 78.70, 80.80]:  # official logos on their names
    put(pop, l - 0.01, -10); put(th, l, -17)
for m in [30.72, 31.30, 48.52]:                                         # lines and the range box drawn
    put(mk, m, -10, length=0.5, fade_out=0.1)
for a in [34.52, 47.78]:                                                # arrows
    put(scr, a, -12, length=0.5, fade_out=0.1)
for l in [33.30, 50.50, 51.74]:                                         # labels
    put(pop, l, -14)
for c in [92.90, 93.58, 94.22]:                                         # the four charts, one after another
    put(clk, c - 0.01, -10)
put(sl, 94.97, -12)
for p in [15.02, 27.58, 88.92, 100.26]:                                 # punch-ins: a small low bump
    put(th, p - 0.01, -19)

# (v3) no sound on the montage cuts: Akhilesh, "too many whooshes ... use it selectively"
peak = np.abs(out).max(); print("raw peak", round(float(peak), 3))
tmp = f"{SK}/mix/raw.wav"
pcm = (np.clip(out[: int(TOTAL * SR)] / max(1.0, peak * 1.05), -1, 1) * 32767).astype("<i2")
import wave
with wave.open(tmp, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
# loudness: two-pass loudnorm to -14 LUFS, true peak -1.5
m = subprocess.run(["ffmpeg", "-hide_banner", "-i", tmp, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                   capture_output=True, text=True).stderr
j = json.loads(m[m.rindex("{"): m.rindex("}") + 1])
af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:"
      f"measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", af, "-ar", "48000", f"{SK}/mix/sk06_mix.wav"], check=True)
print(f"{SK}/mix/sk06_mix.wav", "input", j["input_i"], "LUFS")
