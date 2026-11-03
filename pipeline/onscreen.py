#!/usr/bin/env python3
"""On-screen numbers must be numbers the script says (QC gate row "graphics"). A wrong figure on a card is the mistake
Akhilesh should never be the one to find, and the transcript check only covers what is spoken.

The build's QC manifest lists every graphic: "graphics": [{"t0", "t1", "text", "kind", "sourced"?}]. For each one this
reads the numbers off `text` and looks for the same value in the approved script's spoken lines, whatever the
spelling: 50.1% = 'fifty point one percent', ₹91,685 crore = 'इक्यानवे हज़ार छह सौ पचासी करोड़', 1.12 lakh crore =
'one point one two lakh crore' (compared as absolute values: lakh 1e5, crore 1e7, thousand, million, billion...).
  - a number the script never says FAILS, unless the graphic carries "sourced": "<where it comes from>" (a person has
    checked it; the reason goes into the row)
  - years 1900-2039 and graphics of kind logo / label / ticker / marker are exempt
  - a figure on screen under MIN_VISIBLE_S fails: after the old-TV softening nobody reads it
Only the declared text is read; no OCR (none is installed). A manifest with no "graphics" is reported as NOT CHECKED,
never as a pass. pipeline/verify_line.py's numbers() is not used: it splits 91,685 and 50.1 at the comma and the dot.

  onscreen.py SCRIPT.json MANIFEST.json     print the verdict for every graphic"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import verify_line as vl  # noqa: E402

MIN_VISIBLE_S = 1.0
TOL = 0.005
EXEMPT_KINDS = {"logo", "label", "ticker", "marker", "film", "credit"}   # names and credits, not claims
UNITS = {"lakh": 1e5, "lakhs": 1e5, "लाख": 1e5, "crore": 1e7, "crores": 1e7, "cr": 1e7, "करोड़": 1e7, "करोड": 1e7,
         "thousand": 1e3, "हज़ार": 1e3, "हजार": 1e3, "million": 1e6, "mn": 1e6, "billion": 1e9, "bn": 1e9,
         "trillion": 1e12, "trn": 1e12, "k": 1e3, "%": 1.0, "percent": 1.0, "प्रतिशत": 1.0}
PCT = {"%", "percent", "प्रतिशत"}
POINT = {"point", "दशमलव", "डेसिमल"}
EN = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
      "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
      "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
      "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90, "शून्य": 0, "ज़ीरो": 0, "zero": 0}
HALF = {"डेढ़": 1.5, "ढाई": 2.5}          # one and a half, two and a half
BEFORE = {"साढ़े": 0.5, "सवा": 0.25, "पौने": -0.25}   # sadhe/sava/paune N: N + 0.5 / + 0.25 / - 0.25
_nfc = lambda d: {vl.unicodedata.normalize("NFC", k): v for k, v in d.items()}
UNITS, EN, HALF, BEFORE = _nfc(UNITS), _nfc(EN), _nfc(HALF), _nfc(BEFORE)
NUMW = _nfc(vl.NUM_WORDS)
DIGIT = re.compile(r"\d[\d,]*(?:\.\d+)?")
MARK = "§"


def _float(tok):
    try:
        return float(tok)
    except ValueError:
        return None


def _hundreds(toks):
    """sava / sadhe / paune / dedh + a number + sau or hazaar, before compose() merges them: सवा दो सौ = 225,
    डेढ़ सौ = 150, सवा सौ = 125, साढ़े तीन सौ = 350, सवा दो हज़ार = 2250 (after lakh or crore, num_at multiplies instead)"""
    mult = {"सौ": 100, "hundred": 100, "हज़ार": 1000, "हजार": 1000, "thousand": 1000}
    delta = {**BEFORE, "डेढ़": 0.5}
    def base(t):
        t = t.lower()
        return EN.get(t, NUMW.get(t))
    out, i = [], 0
    while i < len(toks):
        t = toks[i].lower()
        if t in delta and i + 1 < len(toks):
            if toks[i + 1].lower() in mult:                                   # सवा सौ, डेढ़ सौ, डेढ़ हज़ार: 1 + delta
                out.append(str(int(round((1 + delta[t]) * mult[toks[i + 1].lower()])))); i += 2; continue
            b = base(toks[i + 1])
            if b is not None and t != "डेढ़" and i + 2 < len(toks) and toks[i + 2].lower() in mult:
                out.append(str(int(round((b + delta[t]) * mult[toks[i + 2].lower()])))); i += 3; continue
        out.append(toks[i]); i += 1
    return out


def values(text):
    """[(absolute value, is_percent, snippet)] for every number in the text, digits or words"""
    text = vl.unicodedata.normalize("NFC", text).translate(vl.DEV_DIGITS)
    text = re.sub(r"\[[^\]]*\]", " ", text)
    nums = []
    def hold(m):
        nums.append(m.group())                       # as written, comma and all: 2,000 is money, 2000 may be a year
        return f" {MARK}{len(nums) - 1}{MARK} "
    text = DIGIT.sub(hold, text)
    toks = vl.compose(_hundreds(vl.tokens(text)))
    ph = re.compile(MARK + r"(\d+)" + MARK)
    def num_at(i):
        """(value, next index) for a number starting at toks[i], or None"""
        t = toks[i]; m = ph.fullmatch(t)
        if m:
            return float(nums[int(m.group(1))].replace(",", "")), i + 1
        if re.fullmatch(r"\d+", t):
            return float(t), i + 1
        lo = t.lower()
        if lo in HALF:
            return HALF[lo], i + 1
        if lo in BEFORE and i + 1 < len(toks):
            n = num_at(i + 1)
            if n:
                return n[0] + BEFORE[lo], n[1]
        if lo in EN or lo in NUMW:
            v = EN.get(lo, NUMW.get(lo)); i += 1
            if lo in EN and v >= 20 and v % 10 == 0 and i < len(toks) and EN.get(toks[i].lower(), 0) in range(1, 10):
                v += EN[toks[i].lower()]; i += 1                      # twenty one
            if i < len(toks) and toks[i].lower() == "hundred" and lo != "hundred":
                v *= 100; i += 1
                if i < len(toks) and (EN.get(toks[i].lower(), 0) >= 1 or toks[i].lower() in NUMW):
                    v += EN.get(toks[i].lower(), NUMW.get(toks[i].lower(), 0)); i += 1
            return float(v), i
        return None
    out, i = [], 0
    while i < len(toks):
        n = num_at(i)
        if not n:
            i += 1; continue
        v, j = n; start = i
        if j < len(toks) and toks[j].lower() in POINT:       # fifty point one / 50 point 1
            digs, j = "", j + 1
            while j < len(toks):
                d = num_at(j)
                if not d or d[0] != int(d[0]) or not 0 <= d[0] <= 9:
                    break
                digs += str(int(d[0])); j = d[1]
            if digs:
                v = float(f"{int(v)}.{digs}")
        pct, mult = False, 1.0
        while j < len(toks) and toks[j].lower() in UNITS:
            u = toks[j].lower(); pct = pct or u in PCT; mult *= UNITS[u]; j += 1
        snippet = ph.sub(lambda m: nums[int(m.group(1))], " ".join(toks[start:j]))     # the number as written, not the placeholder
        if start and toks[start - 1].lower() in ("rs", "₹"):
            snippet = "₹" + snippet                  # money is never a year
        out.append((v * mult, pct, snippet))
        i = max(j, i + 1)
    return out


def same(a, b):
    return abs(a - b) <= TOL * max(abs(a), abs(b), 1e-9)


def is_year(v, snippet):
    return v == int(v) and 1900 <= v <= 2039 and snippet.strip().isdigit()


def spoken_values(script):
    return [v for ln in script["lines"] for v in values(ln.get("spoken") or ln.get("text", ""))]


def check(graphics, script):
    """[(id, ok or None (None = not checked), detail, fix)] one per graphic"""
    if graphics is None:
        return [("all", None, "the manifest lists no on-screen graphics, so no figure on screen was checked against the script",
                 'add "graphics": [{"t0","t1","text","kind"}] to the QC manifest')]
    heard = spoken_values(script)
    res = []
    for n, g in enumerate(graphics, 1):
        gid = f"g{n}"
        text, kind = g.get("text", ""), g.get("kind", "")
        if kind in EXEMPT_KINDS:
            continue
        vis = float(g.get("t1", 0)) - float(g.get("t0", 0))
        problems, notes = [], []
        for v, pct, snip in values(text):
            if is_year(v, snip):
                continue
            if not any(same(v, h) for h, _, _ in heard):
                if g.get("sourced"):
                    notes.append(f"{snip!r} not spoken, sourced: {g['sourced']}")
                else:
                    problems.append(f"{snip!r} ({v:g}) is on screen but the script never says it")
            else:
                notes.append(f"{snip!r} = spoken")
            if vis < MIN_VISIBLE_S:
                problems.append(f"{snip!r} is on screen {vis:.1f} s, under {MIN_VISIBLE_S:g} s")
        if not problems and not notes:
            continue
        shown = f"\"{text[:40]}\" at {float(g.get('t0', 0)):.1f} s: "
        res.append((gid, not problems, shown + ("; ".join(problems) if problems else "; ".join(notes)),
                    None if not problems else "say it in the script (Akhilesh's gate), change the card to a number the script says, "
                    'or add "sourced" with where a person checked it'))
    if not res:
        res.append(("all", True, f"{len(graphics)} graphics, no figures to check", None))
    return res


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    sc, mf = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
    bad = 0
    for gid, ok, detail, fix in check(mf.get("graphics"), sc):
        print(f"{'NOT CHECKED' if ok is None else 'PASS' if ok else 'FAIL':<11} {gid:<4} {detail}")
        bad += ok is False
    sys.exit(1 if bad else 0)
