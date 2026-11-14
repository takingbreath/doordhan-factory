#!/usr/bin/env python3
"""sk06: the song cue sheet for Instagram Edits (Akhilesh lays the song himself; our file has none). Times follow the
final edit (voice at 0.12 s, brake at 52.55, outro brake at 104.80, end 112.57). The loop: clip C ends at song 0:25.98
and clip S1 starts at song 0:25.98, so when the reel loops the song runs on without a jump.
Writes sfx/cues.json and prints the sheet. Usage: python3 work/sk06/cue_sheet.py"""
import json
END, BRAKE1, VOICE2, BRAKE2, C_IN, GLASS = 111.77, 52.55, 54.10, 104.86, 105.76, 1.30
SEAM = 25.98                                   # song time where C ends and S1 begins
f = lambda s: f"{int(s // 60)}:{s % 60:05.2f}"
clips = [
    {"clip": "S1", "reel": [0.0, GLASS], "song_from": SEAM, "level": "full", "why": "the drone dives to the bus; the song where C ended, so the loop is seamless"},
    {"clip": "S2", "reel": [GLASS, BRAKE1], "song_from": SEAM + GLASS, "level": "low", "why": "split S1 where the camera passes the windscreen; low under his voice"},
    {"clip": "mute", "reel": [BRAKE1, VOICE2], "why": "the brake"},
    {"clip": "B", "reel": [VOICE2, BRAKE2], "song_from": 126.0, "level": "low", "why": "second verse from 2:06, low under the semiconductor half and the payoff"},
    {"clip": "mute", "reel": [BRAKE2, C_IN], "why": "the outro brake"},
    {"clip": "C", "reel": [C_IN, END], "song_from": SEAM - (END - C_IN), "level": "full", "why": "the chorus over the pull-back and the drone rise; ends at song 0:25.98, which runs into S1 when the reel loops"},
]
out = {"song": "Zindagi Ek Safar Hai Suhana (Andaz, 1971), Kishore Kumar, Saregama: add it in Instagram Edits",
       "reel_length": f(END), "levels": "'full' = as loud as Pandey's voice; 'low' = about 19 dB under 'full' (in Edits start near 15-20% and set it by ear)",
       "clips": [dict(c, reel=f"{f(c['reel'][0])}-{f(c['reel'][1])}", **({"song_from": f(c["song_from"])} if "song_from" in c else {})) for c in clips]}
json.dump(out, open("work/sk06/sfx/cues.json", "w"), indent=1, ensure_ascii=False)
for c in out["clips"]:
    print(f"{c['clip']:5} reel {c['reel']:17} " + (f"song from {c['song_from']:8} {c['level']:5}" if "song_from" in c else "silent".ljust(26)) + f"  {c['why']}")
