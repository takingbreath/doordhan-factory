#!/usr/bin/env python3
"""Sound effects for the v7 (Remotion) scenes: every sound sits on the word its picture shows. Reads voice/words_scribe.json; writes gfx6/<scene>.sfx.json
as [[voice time, kind, volume], ...] (kind = a file assets/audio/sfx_<kind>.wav). Kept quiet under speech; none on the short number words but the typed digits."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); W = json.load(open(f"{HERE}/voice/words_scribe.json"))
def wt(text, near=None, nth=0):
    hits = [s for s, e, t in W if t.strip(",.?!।").lower() == text.lower()]
    return min(hits, key=lambda s: abs(s - near)) if near is not None else hits[nth]
P = {
 "hook": [("stamp2", wt("कांड"), .30)],
 "chart": [("slap", wt("E-Mudhra", 4.4), .26), ("slap", wt("दो", 4.98), .26), ("scribble", wt("lower"), .30), ("tape", wt("lower") + .12, .24), ("scribble", wt("circuits"), .30), ("tape", wt("circuits") + .12, .24), ("click", wt("36%", 6.26), .16), ("thud", wt("गिर", 6.96), .30)],
 "gst": [("slap", wt("GST"), .28), ("slap", wt("income"), .28), ("slap", wt("import-export"), .28), ("slide", wt("E-Mudhra", 11.42), .16), ("stamp2", wt("digital", 12.18) + .06, .34), ("stamp2", wt("signature", 12.62) + .06, .34), ("stamp2", wt("certificates", 13.06) + .06, .34), ("scribble", wt("use"), .22), ("scribble", wt("होते"), .22), ("scribble", wt("हैं", 14.08), .22)],
 "cert": [("slap", wt("website", 16.44), .28), ("click", wt("असली", 17.04), .20), ("chime", wt("certificate", 18.38), .20), ("stamp2", wt("देती") + .04, .30), ("slide", wt("और", 19.84), .18), ("slap", wt("certificate", 20.0), .30), ("slide", wt("control"), .20), ("tape", wt("सिर्फ", 21.86) + .3, .20), ("scribble", wt("company", 22.18), .24)],
 "pass": [("slap", wt("security", 24.22), .30), ("scribble", wt("कमजोर"), .34), ("thud", wt("कमजोर"), .24), ("slap", wt("password"), .26), ("type", wt("एक", 28.72), .16), ("type", wt("दो", 28.9), .16), ("type", wt("तीन", 29.18), .16), ("scribble", wt("तीन", 29.18) + .08, .22), ("click", wt("हो", 29.44), .30), ("chime", wt("हो", 29.44) + .12, .22)],
 "hack": [("slide", wt("hacker"), .20), ("slap", wt("नकली", 30.78), .30), ("stamp2", 32.46, .40), ("slap", wt("website", 32.76), .30), ("click", wt("website", 32.76) + .1, .18), ("chime", wt("असली", 33.56), .20), ("scribble", wt("सकता"), .34), ("thud", wt("सकता"), .26)],
 "rob": [("slap", wt("Rob"), .30), ("slide", wt("email", 36.32), .20), ("slap", wt("कब"), .30), ("scribble", wt("बताई"), .26)],
 "quar": [("slide", wt("E-Mudhra", 43.76), .18), ("slap", wt("बोली"), .30), ("slide", wt("email", 45.04), .20), ("thud", wt("हो", 45.7), .30), ("slap", wt("गई", 45.84), .25), ("marker", wt("गई", 45.84) + .1, .24), ("slap", wt("Follow-up"), .25), ("scribble", wt("action"), .24), ("slap", wt("security", 49.28), .30), ("tear", wt("problem"), .30)],
 "audit": [("slap", wt("करीब", 52.92), .25), ("marker", wt("18", 53.24) - .05, .26), ("slide", wt("18", 53.24) - .1, .14), ("slap", wt("और", 54.32), .30), ("scribble", wt("दो", 54.58), .24), ("scribble", wt("audits"), .24)],
 "unaff": [("slap", wt("अब"), .25), ("slap", wt("data"), .25), ("marker", wt("breach"), .25), ("slap", wt("signing"), .25), ("marker", wt("services"), .25), ("scribble", wt("unaffected"), .34), ("chime", wt("unaffected"), .20)],
 "trust": [("slap", wt("भरोसा"), .30), ("tear", wt("उठने"), .30), ("tear", wt("समझो", 71.38), .40), ("thud", wt("समझो", 71.38) + .35, .30)],
 "digi": [("tape", wt("2011"), .26), ("slap", wt("Netherlands"), .30), ("marker", wt("Netherlands") + .5, .32), ("tape", wt("Netherlands") + .9, .24), ("slap", wt("DigiNotar"), .26), ("marker", wt("DigiNotar") + .15, .22), ("stamp2", wt("hack", 75.88), .40), ("slap", wt("नकली", 76.74), .30), ("slap", wt("certificates", 77.06), .30), ("slap", wt("सबने"), .22), ("slap", wt("उसकी"), .22), ("slap", wt("मुहर"), .22), ("scribble", wt("reject"), .30), ("scribble", wt("कर", 79.6), .30), ("scribble", wt("दी", 79.78), .30), ("slap", wt("तीन", 81.84), .30), ("marker", wt("हफ्ते"), .24), ("stamp2", wt("bankrupt"), .50), ("thud", wt("bankrupt"), .30)],
 "rev": [("coin", wt("revenue"), .14), ("coin", wt("revenue") + .2, .14), ("coin", wt("revenue") + .4, .14), ("coin", wt("revenue") + .6, .14), ("pop", wt("सिर्फ", 85.88), .24), ("scribble", wt("1%"), .24), ("slap", wt("1%"), .30)],
 "cred": [("slap", wt("पूरी"), .30), ("tear", wt("credibility"), .40), ("stamp2", wt("है", 90.06), .36)],
}
os.makedirs(f"{HERE}/gfx6", exist_ok=True)
for name, ev in P.items():
    json.dump([[round(t, 3), k, v] for k, t, v in sorted(ev, key=lambda e: e[1])], open(f"{HERE}/gfx6/{name}.sfx.json", "w"))
print(sum(len(v) for v in P.values()), "sound events in", len(P), "scenes")
