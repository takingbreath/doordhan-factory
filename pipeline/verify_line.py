#!/usr/bin/env python3
"""Check one voice line before any video is spent on it (free to rerun). Needs the audio, the line as sent to the
voice model (with its delivery tags), and what Scribe heard (ElevenLabs connector: creative_transcribe_audio, or
transcribe.py with an API key).
Checks:
  must-say   every number and key term in the script is in the transcript, after normalising digits, Hindi number
             words, Devanagari and Latin ("₹90 लाख" = "नब्बे लाख" = "90 lakh"; "Gold" = "गोल्ड"). Add your own with --must.
  tags       no delivery tag ([slowly], [deadpan], [pause], [sighs]...) was spoken aloud, in either script.
  last word  the transcript ends on the script's last word, and the audio doesn't end mid-sound (truncation).
  tail       no sound after the last word: a breath there makes Wan hold the mouth half open (E5 "Ghatao").
  lead       silence before the first word is within --lead-min/--lead-max (raw TTS: 0-0.35 s; a Wan track: 0.5 s).
  duration   with --episode LINES.json and --line-id, records this line and estimates the reel length
             (lines + 0.35 s gaps + --overhead) against --cap (default 30 s; --cap 0 for formats without a cap).
Usage: verify_line.py LINE.wav --script "[flat, brisk] घर है? गिनो।..." --transcript "घर है, गिनो। ..."
       [--transcript-file F] [--must "90 lakh" --must "net worth"] [--episode work/<slug>/lines.json --line-id P2]
       [--cap 30 --overhead 2.5] [--lead-min 0 --lead-max 0.35] [--json OUT]"""
import argparse, difflib, json, os, re, sys, unicodedata
import numpy as np

here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from common import envelope, duration  # noqa: E402

# ---------------------------------------------------------------- normalisation
END_FAIL_DB, END_WARN_DB = 6.0, 12.0
DEV_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")
NUM_WORDS = {  # Hindi number words (both nasal spellings) and English, -> value
    "एक": 1, "दो": 2, "तीन": 3, "चार": 4, "पाँच": 5, "पांच": 5, "छह": 6, "छः": 6, "सात": 7, "आठ": 8, "नौ": 9,
    "दस": 10, "बीस": 20, "तीस": 30, "चालीस": 40, "पचास": 50, "साठ": 60, "सत्तर": 70, "अस्सी": 80, "नब्बे": 90,
    "सौ": 100, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "ten": 10, "hundred": 100}
# 11-99 (E8, 2026-10-05: "दो सौ चौरानवे" = 294 failed the script check because only round tens were known)
NUM_WORDS.update(dict(zip(
    "ग्यारह बारह तेरह चौदह पंद्रह सोलह सत्रह अठारह उन्नीस इक्कीस बाईस तेईस चौबीस पच्चीस छब्बीस सत्ताईस अट्ठाईस उनतीस "
    "इकतीस बत्तीस तैंतीस चौंतीस पैंतीस छत्तीस सैंतीस अड़तीस उनतालीस इकतालीस बयालीस तैंतालीस चवालीस पैंतालीस छियालीस "
    "सैंतालीस अड़तालीस उनचास इक्यावन बावन तिरेपन चौवन पचपन छप्पन सत्तावन अट्ठावन उनसठ इकसठ बासठ तिरसठ चौंसठ पैंसठ "
    "छियासठ सड़सठ अड़सठ उनहत्तर इकहत्तर बहत्तर तिहत्तर चौहत्तर पचहत्तर छिहत्तर सतहत्तर अठहत्तर उन्यासी इक्यासी बयासी "
    "तिरासी चौरासी पचासी छियासी सत्तासी अट्ठासी नवासी इक्यानवे बानवे तिरानवे चौरानवे पचानवे छियानवे सत्तानवे अट्ठानवे "
    "निन्यानवे".split(),
    [n for n in range(11, 100) if n % 10])))
NUM_WORDS.update({"पन्द्रह": 15, "पचास": 50})
UNITS = {"लाख": "lakh", "lakh": "lakh", "lakhs": "lakh", "करोड़": "crore", "करोड": "crore", "crore": "crore",
         "crores": "crore", "हज़ार": "thousand", "हजार": "thousand", "thousand": "thousand", "%": "percent",
         "प्रतिशत": "percent", "percent": "percent", "पर्सेंट": "percent", "परसेंट": "percent"}
TAG_WORDS = {  # tag vocabulary as Scribe might write it if spoken aloud (Latin + Devanagari)
    "slowly": ["slowly", "स्लोली"], "brisk": ["brisk", "ब्रिस्क"], "flat": ["flat", "फ्लैट"],
    "deadpan": ["deadpan", "डेडपैन"], "pause": ["pause", "पॉज़", "पॉज", "पोज़"], "sighs": ["sighs", "sigh", "साइ"],
    "whispers": ["whispers", "विस्पर"], "laughs": ["laughs", "लाफ्स"], "matter-of-fact": ["matter of fact", "मैटर ऑफ फैक्ट"],
    "normal pace": ["normal pace", "नॉर्मल पेस"], "long pause": ["long pause", "लॉन्ग पॉज़"]}

CONS = {"क": "k", "ख": "kh", "ग": "g", "घ": "gh", "ङ": "n", "च": "ch", "छ": "chh", "ज": "j", "झ": "jh", "ञ": "n",
        "ट": "t", "ठ": "th", "ड": "d", "ढ": "dh", "ण": "n", "त": "t", "थ": "th", "द": "d", "ध": "dh", "न": "n",
        "प": "p", "फ": "f", "ब": "b", "भ": "bh", "म": "m", "य": "y", "र": "r", "ल": "l", "व": "v", "श": "sh",
        "ष": "sh", "स": "s", "ह": "h", "ळ": "l"}
NUKTA = {"क": "k", "ख": "kh", "ग": "g", "ज": "z", "ड": "r", "ढ": "rh", "फ": "f"}
MATRA = {"ा": "a", "ि": "i", "ी": "i", "ु": "u", "ू": "u", "े": "e", "ै": "ai", "ो": "o", "ौ": "au", "ॉ": "o",
         "ृ": "ri", "ॅ": "e"}
VOWEL = {"अ": "a", "आ": "a", "इ": "i", "ई": "i", "उ": "u", "ऊ": "u", "ए": "e", "ऐ": "ai", "ओ": "o", "औ": "au",
         "ऑ": "o", "ऋ": "ri"}


def translit(word):
    """rough Devanagari -> Latin (enough to compare loanwords across scripts)"""
    w = unicodedata.normalize("NFC", word)
    out, i = [], 0
    while i < len(w):
        c = w[i]; nxt = w[i + 1] if i + 1 < len(w) else ""
        if c in CONS:
            base = CONS[c]
            if nxt == "़":
                base = NUKTA.get(c, base); i += 1; nxt = w[i + 1] if i + 1 < len(w) else ""
            out.append(base)
            if nxt in MATRA:
                out.append(MATRA[nxt]); i += 1
            elif nxt == "्":
                i += 1
            elif nxt and (nxt in CONS or nxt in "ंँ"):
                out.append("a")
        elif c in VOWEL:
            out.append(VOWEL[c])
        elif c in "ंँ":
            out.append("n")
        elif c.isascii():
            out.append(c.lower())
        i += 1
    return "".join(out)


def skeleton(s):
    """consonant skeleton for fuzzy cross-script matching: vowels dropped, near-sounds merged"""
    s = translit(s) if re.search(r"[ऀ-ॿ]", s) else s.lower()
    s = s.replace("ph", "f").replace("w", "v").replace("z", "j").replace("th", "t").replace("dh", "d") \
         .replace("sh", "s").replace("ck", "k").replace("c", "k").replace("q", "k").replace("x", "ks")
    s = re.sub(r"[aeiouy]", "", s)
    s = re.sub(r"(.)\1+", r"\1", s)
    return re.sub(r"[^a-z0-9]", "", s)


def tokens(text):
    t = unicodedata.normalize("NFC", text).translate(DEV_DIGITS)
    t = re.sub(r"\[[^\]]*\]", " ", t)                      # delivery tags are not words
    t = t.replace("₹", " ₹ ").replace("%", " % ")
    return [x for x in re.split(r"[\s,।.?!…:;\"'“”‘’()\-–—/]+", t) if x]


def compose(toks):
    """number-word runs as one digit token: ['दो', 'सौ', 'चौरानवे'] -> ['294']; other tokens unchanged"""
    out, i = [], 0
    while i < len(toks):
        v = NUM_WORDS.get(toks[i].lower())
        # digits before हज़ार too: Scribe writes "पंद्रह-पंद्रह हज़ार" one run and "15-15 हजार" the next (nana01, 2026-10-09)
        if toks[i].isdigit() and int(toks[i]) < 1000 and i + 1 < len(toks) and toks[i + 1].lower() in ("हज़ार", "हजार", "thousand"):
            out.append(str(int(toks[i]) * 1000)); i += 2
            continue
        # "तीन हज़ार" = 3000 (DTB Ep 3, 2026-10-06: "तीन हज़ार करोड़" against Scribe's "₹3000 करोड़")
        if v is not None and v < 100 and i + 1 < len(toks) and toks[i + 1].lower() in ("हज़ार", "हजार", "thousand"):
            n = v * 1000; i += 2
            if i + 1 < len(toks) and NUM_WORDS.get(toks[i].lower(), 100) < 10 and toks[i + 1].lower() in ("सौ", "hundred"):
                n += NUM_WORDS[toks[i].lower()] * 100; i += 2
            w = NUM_WORDS.get(toks[i].lower()) if i < len(toks) else None
            if w is not None and w < 100:
                n += w; i += 1
            out.append(str(n))
        elif v is not None and v < 100 and i + 1 < len(toks) and toks[i + 1].lower() in ("सौ", "hundred"):
            n = v * 100; i += 2
            w = NUM_WORDS.get(toks[i].lower()) if i < len(toks) else None
            if w is not None and w < 100:
                n += w; i += 1
            out.append(str(n))
        else:
            out.append(toks[i]); i += 1
    return out


def numbers(text):
    """canonical number phrases: '90 lakh', '2 crore', '1 percent', bare numbers as '100'"""
    toks = compose(tokens(text)); out = []
    for i, tk in enumerate(toks):
        v = None
        if re.fullmatch(r"\d+(\.\d+)?", tk):
            v = tk
        elif tk.lower() in NUM_WORDS:
            v = str(NUM_WORDS[tk.lower()])
        if v is None:
            continue
        unit = UNITS.get(toks[i + 1].lower()) if i + 1 < len(toks) else None
        out.append(f"{v} {unit}" if unit else v)
    return out


def key_terms(script):
    """Latin words and multi-word English phrases in the script (the loanwords that carry the meaning)"""
    t = re.sub(r"\[[^\]]*\]", " ", script)
    phrases = re.findall(r"[A-Za-z][A-Za-z%&]*(?:\s+[A-Za-z][A-Za-z%&]*)*", t)
    out = []
    for ph in phrases:
        ph = ph.strip()
        if len(ph) >= 2 and ph.lower() not in ("ka", "ki", "ke", "hai", "na"):
            out.append(ph)
    return out


def has_term(term, transcript):
    """term present in the transcript? exact (case-folded) or skeleton match over a sliding word window"""
    if term.lower() in transcript.lower():
        return True, term
    sk = skeleton(term)
    if not sk:
        return True, ""
    words = tokens(transcript); n = len(term.split())
    best = (0.0, "")
    for k in range(max(1, n - 1), n + 2):
        for i in range(0, len(words) - k + 1):
            cand = " ".join(words[i:i + k])
            r = difflib.SequenceMatcher(None, sk, skeleton(cand)).ratio()
            if r > best[0]:
                best = (r, cand)
    return best[0] >= 0.75, best[1]


# ---------------------------------------------------------------- audio checks
def audio_checks(path, win=0.02, thresh=-38.0):
    db = envelope(path, win=win)
    D = duration(path)
    on = np.where(db > thresh)[0]
    if len(on) == 0:
        return {"duration": round(D, 2), "lead": None, "speech_end": None, "tail_sound": None, "ends_hot": None}
    lead = on[0] * win
    # last word = last run of speech followed by >=0.15 s quiet; anything after a >=0.15 s gap is a tail sound
    runs, s0, prev = [], on[0], on[0]
    for i in on[1:]:
        if (i - prev) * win > 0.15:
            runs.append((s0, prev)); s0 = i
        prev = i
    runs.append((s0, prev))
    # a tail sound: a short (<0.35 s) run after the main speech whose peak is well below the speech level
    speech_lvl = float(np.percentile(db[on], 75))
    tail = None
    if len(runs) >= 2:
        a, b = runs[-1]
        gap = (a - runs[-2][1]) * win
        L = (b - a + 1) * win
        touches_end = b >= len(db) - 2
        if 0.06 <= L < 0.4 and gap >= 0.15 and (db[a:b + 1].max() < speech_lvl - 6 or touches_end):
            tail = {"at": round(a * win, 2), "len": round(L, 2), "cut_off_by_file_end": bool(touches_end),
                    "peak_db_below_speech": round(speech_lvl - float(db[a:b + 1].max()), 1)}
            runs = runs[:-1]
    end = (runs[-1][1] + 1) * win
    # how far the level has fallen by the last 40 ms: a natural ending decays 20-60 dB below the speech level;
    # a hard cut (E5 test: line cut mid "lakh") ends at speech level. E5's approved lines: 4-58 dB.
    drop = float(speech_lvl - db[-2:].max())
    return {"duration": round(float(D), 2), "lead": round(float(lead), 2), "speech_end": round(float(end), 2),
            "tail_sound": tail, "end_drop_db": round(drop, 1)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio"); ap.add_argument("--script", required=True)
    ap.add_argument("--transcript"); ap.add_argument("--transcript-file")
    ap.add_argument("--must", action="append", default=[])
    ap.add_argument("--lead-min", type=float, default=0.0); ap.add_argument("--lead-max", type=float, default=0.35)
    ap.add_argument("--episode"); ap.add_argument("--line-id")
    ap.add_argument("--cap", type=float, default=30.0); ap.add_argument("--overhead", type=float, default=2.5)
    ap.add_argument("--gap", type=float, default=0.35)
    ap.add_argument("--json"); ap.add_argument("--label", default="")
    a = ap.parse_args()
    tr = a.transcript if a.transcript is not None else (open(a.transcript_file).read() if a.transcript_file else None)
    if tr is None:
        ap.error("give --transcript or --transcript-file (Scribe's text for this audio)")
    res = {"audio": a.audio, "label": a.label, "checks": {}}
    C = res["checks"]
    # must-say: numbers and key terms
    want_nums = numbers(a.script); got_nums = numbers(tr)
    missing_nums = [n for n in want_nums if n not in got_nums]
    terms = list(dict.fromkeys(key_terms(a.script) + a.must))
    missing_terms, matched = [], {}
    for t in terms:
        ok, hit = has_term(t, tr)
        (matched.__setitem__(t, hit) if ok else missing_terms.append(t))
    C["must_say"] = {"ok": not missing_nums and not missing_terms, "numbers": want_nums, "missing_numbers": missing_nums,
                     "terms": terms, "missing_terms": missing_terms}
    # tags spoken aloud
    tags = [t.strip().lower() for g in re.findall(r"\[([^\]]+)\]", a.script) for t in g.split(",")]
    spoken = []
    trl = tr.lower()
    for t in set(tags):
        forms = TAG_WORDS.get(t, [t])
        for f in forms:
            if f.lower() in trl:
                spoken.append(t); break
    # tags we don't know yet: look for their Latin form, or a close skeleton in the transcript
        else:
            if t not in TAG_WORDS and has_term(t, tr)[0] and len(skeleton(t)) >= 3:
                spoken.append(t)
    C["tags_not_spoken"] = {"ok": not spoken, "tags": sorted(set(tags)), "spoken": spoken}
    # last word
    sw, tw = tokens(a.script), tokens(tr)
    last_ok = bool(sw and tw) and (skeleton(sw[-1]) == skeleton(tw[-1]) or
                                   difflib.SequenceMatcher(None, skeleton(sw[-1]), skeleton(tw[-1])).ratio() >= 0.75
                                   or numbers(sw[-1]) == numbers(tw[-1]) != [])
    au = audio_checks(a.audio)
    C["last_word"] = {"ok": last_ok, "script": sw[-1] if sw else None, "heard": tw[-1] if tw else None}
    drop = au["end_drop_db"]
    C["end_cut"] = {"ok": drop >= END_FAIL_DB, "end_drop_db": drop,
                    "warn": None if drop >= END_WARN_DB or drop < END_FAIL_DB else
                    "ends without a fade: check the last word by ear; re-export without the tight trim or add a 30 ms fade",
                    "fix": None if drop >= END_FAIL_DB else
                    "hard cut at the end (the last word may be clipped): re-export or regenerate the line untrimmed"}
    C["tail"] = {"ok": au["tail_sound"] is None, "speech_end": au["speech_end"], "file_end": au["duration"],
                 "tail_sound": au["tail_sound"],
                 "fix": None if au["tail_sound"] is None else f"trim the line at {au['speech_end']} s (after the last word)"}
    C["lead"] = {"ok": au["lead"] is not None and a.lead_min <= au["lead"] <= a.lead_max, "lead_s": au["lead"],
                 "range": [a.lead_min, a.lead_max]}
    # running duration
    if a.episode and a.line_id:
        ep = json.load(open(a.episode)) if os.path.exists(a.episode) else {"lines": {}}
        span = (au["speech_end"] or 0) - (au["lead"] or 0)
        ep["lines"][a.line_id] = {"audio": a.audio, "speech_s": round(span, 2)}
        n = len(ep["lines"]); total = sum(v["speech_s"] for v in ep["lines"].values()) + a.gap * max(0, n - 1) + a.overhead
        json.dump(ep, open(a.episode, "w"), indent=1, ensure_ascii=False)
        C["duration"] = {"ok": a.cap <= 0 or total <= a.cap, "line_s": round(span, 2), "lines_so_far": n,
                         "reel_estimate_s": round(total, 1), "cap_s": a.cap if a.cap > 0 else "none"}
    res["verdict"] = "PASS" if all(v["ok"] for v in C.values()) else "FAIL"
    if a.json:
        json.dump(res, open(a.json, "w"), indent=1, ensure_ascii=False)
    print(f"{a.label or os.path.basename(a.audio)}: {res['verdict']}")
    for k, v in C.items():
        detail = {kk: vv for kk, vv in v.items() if kk != "ok" and vv is not None and vv != [] and vv != {}}
        flag = "BAD" if not v["ok"] else ("warn" if v.get("warn") else "ok ")
        print(f"  {flag} {k}: {json.dumps(detail, ensure_ascii=False)}")


if __name__ == "__main__":
    main()
