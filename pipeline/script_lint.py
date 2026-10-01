#!/usr/bin/env python3
"""Deterministic lint for a loop script. No model calls, no network.

Reads the "### Lint table" in section 0 of a format file and the "### Lint table" in each speaker's voice card
(docs/voices/<speaker>/voice-card.md), checks the main script and any alternates, and writes two files next to the
main script: <name>-lint-fails.md (the fails only) and <name>-lint-report.md (measures, reports, fails). Only fails
decide the verdict; reports never do. Exit 0 on PASS, 1 on FAIL, 2 when a table or a file can't be read (then no
verdict is written).

Usage: python3 pipeline/script_lint.py formats/sahayata_kendra.md work/<slug>/loop/r1-script.md [alternate.md ...]
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICES = os.path.join(ROOT, "docs", "voices")

# Format rows: name -> (how the Limit cell is read, check or setting). Exactly these rows, no others.
FORMAT_ROWS = {
    "cast": ("list", "check"), "silent": ("list", "check"), "silent_beats_max": ("int", "check"),
    "silent_beats_min": ("int", "check"), "opening_order": ("list", "check"), "versions_match": ("lineref", "check"),
    "banned_phrases": ("list", "check"), "length_max_s": ("num", "check"), "length_aim_s": ("range", "check"),
    "opening_words": ("int", "check"), "second_speaker_by_s": ("num", "check"), "numbers_reel": ("int", "check"),
    "numbers_line": ("int", "check"), "return_assumption": ("list", "check"), "pace_wps": ("num", "setting"),
    "ring_s": ("num", "setting"), "card_s": ("num", "setting"), "beat_s": ("num", "setting"),
}
SETTING_MARKS = ("—", "–", "-")

# Counting (letters include Devanagari marks, which Python's \w leaves out)
WCH = r"[\wऀ-ॿ]"
TOKEN = re.compile(r"\d+(?:[.,]\d+)*%?|(?:[^\W\d_]|[ऀ-ॣ॰-ॿ])+")
NUMBER_WORDS = set("ek do teen char chaar paanch chhe saat aath nau das gyarah barah baarah terah chaudah pandrah solah "
                   "satrah athaarah unnees bees pachchees tees chalees chaalees pachaas saath sattar assi nabbe sau "
                   "hazaar lakh crore arab dedh dhaai aadha".split())
UNITS = set("hazaar lakh crore sau arab saal mahina mahine percent pratishat rupaye guna".split())
AMBIGUOUS = {"ek", "do", "saath"}  # also "a", "give", "with": a number only before a number word or a unit
PERCENT_WORDS = {"percent", "pratishat"}
QUOTED = re.compile(r'"[^"]*"|“[^”]*”')
LINE = re.compile(r"^\*\*([^*]+)\*\*:\s*(.*)$")
SILENT_ACTION = re.compile(r"^\[([^\[\]]+)\]$")


class TableError(Exception):
    pass


# ------------------------------------------------------------------ tables
def table_after(lines, start, end, path, where):
    """The markdown table under the '### Lint table' heading between lines[start:end]: (header, [(row cells, line no)])."""
    head = next((i for i in range(start, end) if lines[i].strip() == "### Lint table"), None)
    if head is None:
        raise TableError(f"{path}: no '### Lint table' {where}")
    i = head + 1
    while i < end and not lines[i].strip().startswith("|"):
        i += 1
    rows = []
    while i < end and lines[i].strip().startswith("|"):
        rows.append(([c.strip() for c in lines[i].strip().strip("|").split("|")], i + 1))
        i += 1
    if len(rows) < 3:
        raise TableError(f"{path}: the '### Lint table' {where} has no rows")
    return rows[0][0], rows[2:]


def columns(header, want, path):
    idx = {}
    for name in want:
        if name not in header:
            raise TableError(f"{path}: the lint table has no '{name}' column")
        idx[name] = header.index(name)
    return idx


def split_list(v):
    items = [x.strip() for x in v.split(";")]
    return items if items and all(items) else None


def read_value(kind, v):
    if kind == "list":
        return split_list(v)
    if kind == "int":
        return int(v) if re.fullmatch(r"\d+", v) else None
    if kind == "num":
        return float(v) if re.fullmatch(r"\d+(?:\.\d+)?", v) else None
    if kind == "range":
        m = re.fullmatch(r"(\d+(?:\.\d+)?)\s*[–-]\s*(\d+(?:\.\d+)?)", v)
        return (float(m.group(1)), float(m.group(2))) if m and float(m.group(1)) <= float(m.group(2)) else None
    if kind == "lineref":
        m = re.fullmatch(r"([A-Za-z][A-Za-z0-9_]*)['’]s\s+(\d+)(?:st|nd|rd|th)\s+line", v)
        return (m.group(1).upper(), int(m.group(2))) if m and int(m.group(2)) >= 1 else None


def read_format(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    start = next((i for i, l in enumerate(lines) if re.match(r"^##\s+0\b", l)), None)
    if start is None:
        raise TableError(f"{path}: no section 0 ('## 0.')")
    end = next((i for i in range(start + 1, len(lines)) if re.match(r"^##\s", lines[i])), len(lines))
    header, rows = table_after(lines, start, end, path, "in section 0")
    col = columns(header, ("Check", "Limit", "On breach", "What it checks"), path)
    errors, rules, errored = [], {}, set()
    for cells, n in rows:
        name = cells[col["Check"]] if len(cells) > col["Check"] else ""
        errored.add(name)  # cleared below once the row reads cleanly
        if name not in FORMAT_ROWS:
            errors.append(f"{path}: row '{name}' (line {n}): not a row the lint knows")
            continue
        if name in rules:
            errors.append(f"{path}: row '{name}' (line {n}): appears twice")
            continue
        if len(cells) < len(header):
            errors.append(f"{path}: row '{name}' (line {n}): has {len(cells)} cells, the header has {len(header)}")
            continue
        kind, role = FORMAT_ROWS[name]
        value = read_value(kind, cells[col["Limit"]])
        if value is None:
            errors.append(f"{path}: row '{name}' (line {n}): can't read the limit '{cells[col['Limit']]}'")
            continue
        breach = cells[col["On breach"]].strip().lower()
        if role == "setting" and breach not in SETTING_MARKS:
            errors.append(f"{path}: row '{name}' (line {n}): a setting, so 'On breach' must be —, not '{breach}'")
            continue
        if role == "check" and breach not in ("fail", "report"):
            errors.append(f"{path}: row '{name}' (line {n}): 'On breach' must be fail or report, not '{breach}'")
            continue
        rules[name] = {"value": value, "mode": breach if role == "check" else None}
        errored.discard(name)
    for name in FORMAT_ROWS:
        if name not in rules and name not in errored:
            errors.append(f"{path}: row '{name}': missing")
    if errors:
        raise TableError("\n".join(errors))
    return rules


def read_card(speaker):
    """(card rules or None, a note for the report). Rules: {row: {...}}; pace is None when the card says not measured."""
    path = os.path.join(VOICES, speaker.lower(), "voice-card.md")
    rel = os.path.relpath(path, ROOT)
    if not os.path.exists(path):
        return None, f"no voice card ({rel}), so no character checks"
    lines = open(path, encoding="utf-8").read().splitlines()
    try:
        header, rows = table_after(lines, 0, len(lines), rel, "in the card")
    except TableError as e:
        if "no '### Lint table'" in str(e):
            return None, f"{rel} has no lint table, so no character checks"
        raise
    col = columns(header, ("Check", "Words", "Max per reel", "On breach"), rel)
    errors, rules = [], {}
    for cells, n in rows:
        name = cells[col["Check"]] if len(cells) > col["Check"] else ""
        if not name or len(cells) < len(header):
            errors.append(f"{rel}: row '{name}' (line {n}): can't read the row")
            continue
        if name in rules:
            errors.append(f"{rel}: row '{name}' (line {n}): appears twice")
            continue
        words, mx, breach = cells[col["Words"]], cells[col["Max per reel"]], cells[col["On breach"]].strip().lower()
        if name == "pace_wps":
            if words.strip().lower() == "not measured":
                rules[name] = {"pace": None}
            elif re.fullmatch(r"\d+(?:\.\d+)?", words.strip()) and float(words) > 0:
                rules[name] = {"pace": float(words)}
            else:
                errors.append(f"{rel}: row 'pace_wps' (line {n}): Words must be a number or 'not measured', not '{words}'")
            continue
        if not re.fullmatch(r"\d+", mx):
            errors.append(f"{rel}: row '{name}' (line {n}): can't read 'Max per reel' '{mx}'")
            continue
        if breach not in ("fail", "report"):
            errors.append(f"{rel}: row '{name}' (line {n}): 'On breach' must be fail or report, not '{breach}'")
            continue
        if name == "one_word_lines":
            rules[name] = {"max": int(mx), "mode": breach}
            continue
        items = split_list(words)
        if items is None:
            errors.append(f"{rel}: row '{name}' (line {n}): can't read the words '{words}'")
            continue
        rules[name] = {"items": items, "pats": [phrase_pattern(x) for x in items], "max": int(mx), "mode": breach}
    if errors:
        raise TableError("\n".join(errors))
    note = rel
    pace = rules.get("pace_wps", {}).get("pace")
    note += f", pace {pace:g} w/s" if pace else ", pace not measured (the format's pace is used)"
    return rules, note


# ------------------------------------------------------------------ matching and counting
def phrase_pattern(item):
    """Whole-word, any case. 'ka?' matches only straight before a question mark; ', ka' only straight after a comma."""
    item = item.strip()
    after_comma = item.startswith(",")
    item = item.lstrip(",").strip()
    before_q = item.endswith("?")
    item = item.rstrip("?").strip()
    body = r"\s+".join(re.escape(w) for w in item.split())
    return re.compile((r",\s*" if after_comma else rf"(?<!{WCH})") + body + (r"\?" if before_q else rf"(?!{WCH})"), re.I)


def words(text):
    return TOKEN.findall(text)


def numbers(text):
    """(numbers, percentages) in a line. A number in digits, or a run of Hindi number words, plus any unit words
    straight after it, is one number."""
    toks = [t.lower() for t in words(text)]
    n = pct = i = 0

    def counts(j):  # is toks[j] part of a number run?
        t = toks[j]
        if t not in NUMBER_WORDS:
            return False
        return t not in AMBIGUOUS or (j + 1 < len(toks) and (toks[j + 1] in NUMBER_WORDS or toks[j + 1] in UNITS))

    while i < len(toks):
        t = toks[i]
        if t[0].isdigit():
            j = i + 1
        elif counts(i):
            j = i + 1
            while j < len(toks) and counts(j):
                j += 1
        else:
            i += 1
            continue
        k = j
        while k < len(toks) and toks[k] in UNITS:
            k += 1
        n += 1
        if t.endswith("%") or any(u in PERCENT_WORDS for u in toks[j:k]):
            pct += 1
        i = k
    return n, pct


# ------------------------------------------------------------------ scripts
def read_script(path, silent):
    """Parsed lines and script_format breaches."""
    parsed, bad = [], []
    for n, raw in enumerate(open(path, encoding="utf-8").read().splitlines(), 1):
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        m = LINE.match(s)
        if not m:
            bad.append({"n": n, "raw": s})
            continue
        spk, text = m.group(1).strip().upper(), m.group(2).strip()
        is_silent = spk in silent
        ws = [] if is_silent else words(text)
        nums, pcts = (0, 0) if is_silent else numbers(text)
        parsed.append({"n": n, "raw": s, "speaker": spk, "text": text, "silent": is_silent, "words": ws,
                       "nums": nums, "pcts": pcts})
    return parsed, bad


class Version:
    def __init__(self, path, label, rules, cards):
        self.path, self.label = path, label
        self.lines, self.bad = read_script(path, set(rules["silent"]["value"]))
        self.spoken = [l for l in self.lines if not l["silent"]]
        self.beats = [l for l in self.lines if l["silent"]]
        fmt_pace = rules["pace_wps"]["value"]

        def pace(spk):
            c = cards.get(spk)
            p = c and c.get("pace_wps", {}).get("pace")
            return p or fmt_pace
        self.pace = pace
        ring, card, beat = rules["ring_s"]["value"], rules["card_s"]["value"], rules["beat_s"]["value"]
        self.words = sum(len(l["words"]) for l in self.spoken)
        self.length = sum(len(l["words"]) / pace(l["speaker"]) for l in self.spoken) + ring + card + beat * len(self.beats)
        self.first = self.spoken[0] if self.spoken else None
        self.first_words = len(self.first["words"]) if self.first else 0
        self.second_at = (self.first_words / pace(self.first["speaker"]) if self.first else 0) + ring
        self.numbers = sum(l["nums"] for l in self.spoken)
        self.most_numbers = max((l["nums"] for l in self.spoken), default=0)
        self.longest = max((len(l["words"]) for l in self.spoken), default=0)


# ------------------------------------------------------------------ checks
def check_version(v, rules, cards):
    """[(check, line or None, sentence)] with the row's mode attached: [(mode, check, line, sentence)]."""
    out = []

    def add(check, line, msg, mode=None):
        out.append((mode or rules[check]["mode"], check, line, msg))
    for b in v.bad:
        add("script_format", b, "Not a script line: script lines look like **SPEAKER**: text.", "fail")
    cast = [c.upper() for c in rules["cast"]["value"]]
    for l in v.lines:
        if l["speaker"] not in cast:
            add("cast", l, f"{l['speaker']} is not in the cast ({', '.join(cast)}).")
    for l in v.beats:
        m = SILENT_ACTION.match(l["text"])
        if not m or not 1 <= len(words(m.group(1))) <= 5:
            add("silent", l, f"{l['speaker']} never speaks: the line must be one action in square brackets, 5 words at most.")
    mx = rules["silent_beats_max"]["value"]
    if len(v.beats) > mx:
        add("silent_beats_max", v.beats[mx], f"{len(v.beats)} silent beats in the reel, at most {mx}.")
    mn = rules["silent_beats_min"]["value"]
    if len(v.beats) < mn:
        add("silent_beats_min", None, f"{len(v.beats)} silent beats in the reel, at least {mn}.")
    order = [c.upper() for c in rules["opening_order"]["value"]]
    for i, want in enumerate(order):
        if i >= len(v.spoken):
            add("opening_order", None, f"Only {len(v.spoken)} spoken lines; the opening order is {', '.join(order)}.")
            break
        if v.spoken[i]["speaker"] != want:
            add("opening_order", v.spoken[i], f"Spoken line {i + 1} is {v.spoken[i]['speaker']}'s; the opening order is {', '.join(order)}.")
            break
    banned = [(p, phrase_pattern(p)) for p in rules["banned_phrases"]["value"]]
    for l in v.spoken:
        for p, pat in banned:
            if pat.search(l["text"]):
                add("banned_phrases", l, f"Contains the banned phrase “{p}”.")
    if v.length > rules["length_max_s"]["value"]:
        add("length_max_s", None, f"Estimated length {v.length:.1f} s, at most {rules['length_max_s']['value']:g} s.")
    lo, hi = rules["length_aim_s"]["value"]
    if not lo <= round(v.length, 1) <= hi:
        add("length_aim_s", None, f"Estimated length {v.length:.1f} s, the aim is {lo:g}–{hi:g} s.")
    if v.first and v.first_words > rules["opening_words"]["value"]:
        add("opening_words", v.first, f"{v.first_words} words in the first spoken line, at most {rules['opening_words']['value']}.")
    if v.first and round(v.second_at, 1) > rules["second_speaker_by_s"]["value"]:
        add("second_speaker_by_s", v.first, f"The second speaker starts at about {v.second_at:.1f} s, at most "
            f"{rules['second_speaker_by_s']['value']:g} s.")
    if v.numbers > rules["numbers_reel"]["value"]:
        add("numbers_reel", None, f"{v.numbers} numbers in the reel, at most {rules['numbers_reel']['value']}.")
    for l in v.spoken:
        if l["nums"] > rules["numbers_line"]["value"]:
            add("numbers_line", l, f"{l['nums']} numbers in this line, at most {rules['numbers_line']['value']}.")
    assume = [phrase_pattern(p) for p in rules["return_assumption"]["value"]]
    for i, l in enumerate(v.lines):
        if l["pcts"]:
            near = l["text"] + " " + (v.lines[i - 1]["text"] if i else "")
            if not any(p.search(near) for p in assume):
                add("return_assumption", l, "A percentage with no assumption (" +
                    "; ".join(rules["return_assumption"]["value"]) + ") in its line or the line before.")
    # voice-card checks: each character's own spoken lines, quoted text skipped
    for spk, card in cards.items():
        if not card:
            continue
        own = [l for l in v.spoken if l["speaker"] == spk]
        for row, r in card.items():
            if row == "pace_wps":
                continue
            seen = 0
            for l in own:
                if row == "one_word_lines":
                    hits = 1 if len(l["words"]) == 1 else 0
                    what = "a one-word line"
                else:
                    text = QUOTED.sub(" ", l["text"])
                    found = [(item, len(pat.findall(text))) for item, pat in zip(r["items"], r["pats"])]
                    hits = sum(c for _, c in found)
                    what = ", ".join(f"“{item}”" for item, c in found if c)
                if hits and seen + hits > r["max"]:
                    add(row, l, f"{spk} says {what} ({row}): {seen + hits} in the reel, at most {r['max']}.", r["mode"])
                seen += hits
    return out


def check_versions_match(main, alt, rules):
    spk, nth = rules["versions_match"]["value"]
    mode = rules["versions_match"]["mode"]

    def start(v):
        idx = [i for i, l in enumerate(v.lines) if l["speaker"] == spk and not l["silent"]]
        return idx[nth - 1] if len(idx) >= nth else None
    m0, a0 = start(main), start(alt)
    if m0 is None:
        return [(mode, "versions_match", None, f"The main version has no {spk}'s line {nth} to match from.")]
    if a0 is None:
        return [(mode, "versions_match", None, f"This version has no {spk}'s line {nth} to match from.")]
    ms, as_ = main.lines[m0:], alt.lines[a0:]
    key = lambda l: (l["speaker"], [w.lower() for w in words(l["text"])])
    for k in range(max(len(ms), len(as_))):
        if k >= len(as_):
            return [(mode, "versions_match", None, f"Ends early: the main version goes on to its line {ms[k]['n']} (“{ms[k]['raw']}”).")]
        if k >= len(ms):
            return [(mode, "versions_match", as_[k], "An extra line: the main version has ended by here.")]
        if key(ms[k]) != key(as_[k]):
            return [(mode, "versions_match", as_[k], f"Differs from the main version's line {ms[k]['n']} (“{ms[k]['raw']}”).")]
    return []


# ------------------------------------------------------------------ output
def shown(p):
    r = os.path.relpath(p)
    return os.path.abspath(p) if r.startswith("..") else r


def cell(s):
    return s.replace("|", "\\|")


def rows_table(items, last_col):
    if not items:
        return ["None."]
    out = [f"| Check | Version | Line | Text | {last_col} |", "|---|---|---|---|---|"]
    for label, check, line, msg in items:
        out.append(f"| {check} | {cell(label)} | {line['n'] if line else '—'} | {cell(line['raw']) if line else '—'} | {cell(msg)} |")
    return out


def write_error(fails_path, report_path, msg):
    body = ["# Lint error", "", "The lint could not read what it needs, so it gave no verdict:", ""]
    body += [f"- {m}" for m in msg.splitlines()] + ["", "Fix the table or the file and run the lint again."]
    for p in (fails_path, report_path):
        open(p, "w", encoding="utf-8").write("\n".join(body) + "\n")


def main(argv):
    if len(argv) < 2:
        print(__doc__.strip().splitlines()[-1])
        return 2
    fmt_path, scripts = argv[0], argv[1:]
    stem = os.path.splitext(scripts[0])[0]
    fails_path, report_path = stem + "-lint-fails.md", stem + "-lint-report.md"
    try:
        rules = read_format(fmt_path)
        for s in scripts:
            if not os.path.isfile(s):
                raise TableError(f"{s}: no such script file")
        silent = set(c.upper() for c in rules["silent"]["value"])
        speakers = []
        for s in scripts:
            for l in read_script(s, silent)[0]:
                if l["speaker"] not in speakers:
                    speakers.append(l["speaker"])
        cards, notes = {}, {}
        for spk in speakers:
            cards[spk], notes[spk] = read_card(spk)
        labels = [os.path.basename(s) for s in scripts]
        if len(set(labels)) < len(labels):
            labels = [os.path.relpath(s) for s in scripts]
        versions = [Version(s, lab, rules, cards) for s, lab in zip(scripts, labels)]
    except (TableError, OSError, UnicodeDecodeError) as e:
        write_error(fails_path, report_path, str(e))
        for m in str(e).splitlines():
            print(f"ERROR: {m}")
        print("No verdict.")
        print(f"Wrote {shown(fails_path)} and {shown(report_path)}")
        return 2

    fails, reports = [], []
    for i, v in enumerate(versions):
        res = check_version(v, rules, cards)
        if i:
            res += check_versions_match(versions[0], v, rules)
        for mode, check, line, msg in res:
            (fails if mode == "fail" else reports).append((v.label, check, line, msg))
    verdict = "VERDICT: FAIL" if fails else "VERDICT: PASS"
    names = ", ".join(v.label + (" (main)" if i == 0 else "") for i, v in enumerate(versions))

    F = [f"# Lint fails: {versions[0].label}", "", f"Format: {shown(fmt_path)}. Versions: {names}.", ""]
    F += rows_table(fails, "What's wrong") + ["", verdict]
    open(fails_path, "w", encoding="utf-8").write("\n".join(F) + "\n")

    R = [f"# Lint report: {versions[0].label}", "", f"Format: {shown(fmt_path)}. Versions: {names}.", "",
         "Voice cards:"]
    R += [f"- {spk}: " + ("silent, so no spoken lines; " if spk in silent else "") + notes[spk] for spk in speakers]
    for v in versions:
        R += ["", f"## {v.label}", "", "| Measure | Value |", "|---|---|", f"| Words | {v.words} |",
              f"| Estimated length | {v.length:.1f} s |", f"| Words in the first spoken line | {v.first_words} |",
              f"| Second speaker starts | {v.second_at:.1f} s |", f"| Numbers in the reel | {v.numbers} |",
              f"| Most numbers in one line | {v.most_numbers} |", f"| Longest line (words) | {v.longest} |",
              f"| Silent beats | {len(v.beats)} |"]
    R += ["", "## Report-only checks outside their limits", ""] + rows_table(reports, "Outside the limit")
    R += ["", "## Fails", ""] + rows_table(fails, "What's wrong") + ["", verdict]
    open(report_path, "w", encoding="utf-8").write("\n".join(R) + "\n")

    print(verdict)
    print(f"Fails:  {shown(fails_path)}")
    print(f"Report: {shown(report_path)}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
