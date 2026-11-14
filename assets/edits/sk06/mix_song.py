#!/usr/bin/env python3
"""sk06 SONG PREVIEW (Akhilesh, 2026-11-14: "for the next version, give me the song so I can see how the song fits").
For review only, never for posting: Akhilesh lays the song himself in Instagram Edits (the posted file has no song).
Adds Zindagi Ek Safar Hai Suhana (music/zindagi.mp3, the test copy) to the reel's own mix (mix/sk06_mix.wav) exactly as
sfx/cues.json says: 'full' = the song's loudness matched to the voice, 'low' = 19 dB under that, mutes at the brakes,
short fades at every cue edge. Writes mix/sk06_mix_song.wav (stereo, -14 LUFS).
Run from the repository root after mix.py and cue_sheet.py: python3 work/sk06/mix_song.py"""
import json, subprocess, wave
import numpy as np
SK = "work/sk06"; SR = 48000


def load(path, ch):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", str(ch), "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, ch).copy()


def lufs(x):
    tmp = f"{SK}/mix/_m.wav"; write(tmp, x)
    e = subprocess.run(["ffmpeg", "-hide_banner", "-i", tmp, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(e[e.rindex("I:"):].split()[1])


def write(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(x.shape[1]); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


ts = lambda s: int(s.split(":")[0]) * 60 + float(s.split(":")[1])
mix = load(f"{SK}/mix/sk06_mix.wav", 1); mix = np.repeat(mix, 2, axis=1)
voice = load(f"{SK}/mix/dialogue.wav", 1)
song = load(f"{SK}/music/zindagi.mp3", 2)
g_full = 10 ** ((lufs(np.repeat(voice[voice[:, 0] != 0][: SR * 60], 2, axis=1)) - lufs(song[SR * 20: SR * 80])) / 20)
track = np.zeros_like(mix)
for c in json.load(open(f"{SK}/sfx/cues.json"))["clips"]:
    if "song_from" not in c: continue
    a, b = (ts(x) for x in c["reel"].split("-")); s0 = ts(c["song_from"])
    seg = song[int(s0 * SR): int((s0 + b - a) * SR)].copy()
    g = g_full * (1.0 if c["level"] == "full" else 10 ** (-19 / 20))
    n = len(seg); f = int(0.08 * SR); env = np.ones(n, np.float32); env[:f] = np.linspace(0, 1, f); env[-f:] = np.linspace(1, 0, f)
    i = int(a * SR); track[i: i + n] += seg[: len(track) - i] * g * env[: len(track) - i, None]
out = mix + track
tmp = f"{SK}/mix/_song_raw.wav"; write(tmp, out / max(1.0, np.abs(out).max() * 1.02))
m = subprocess.run(["ffmpeg", "-hide_banner", "-i", tmp, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
j = json.loads(m[m.rindex("{"): m.rindex("}") + 1])
af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:"
      f"measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", af, "-ar", "48000", f"{SK}/mix/sk06_mix_song.wav"], check=True)
print(f"{SK}/mix/sk06_mix_song.wav", "song full gain", round(20 * np.log10(g_full), 1), "dB")
