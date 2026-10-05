#!/usr/bin/env python3
"""Did the final say the approved script? Aligns the final reel's Scribe transcript against the frozen script
(script_freeze.py) and fails on a dropped or changed line, whatever the working copy says.
Matching uses verify_line's normalisation: numbers canonicalised ("₹90 लाख" = "नब्बे लाख" = "90 lakh"), words compared
across Devanagari/Latin by consonant skeleton, punctuation and delivery tags ignored.
Per line: coverage = share of the line's words found in order in the transcript.
  PASS  every line covers >= --min (0.85), no run of --max-run (3) consecutive words is missing, and every number
        and unit in the line is heard in that line's position
  FAIL  DROPPED (coverage < 0.3), NUMBER (a number or unit not heard where the line says it), CHANGED (below
        --min, or a missing run of 3+ words: a dropped sentence inside a long line)
Also lists transcript runs of 3+ words that match no line (EXTRA: ad-libs, a wrong take, a line from another draft).
Usage: script_diff.py registry/scripts/SLUG.json --transcript-file FINAL.txt [--min 0.85] [--json OUT]"""
import argparse, difflib, json, os, sys

here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from verify_line import tokens, compose, skeleton, numbers, NUM_WORDS, UNITS  # noqa: E402


def norm_tokens(text):
    """[(normalised token, original)] with number words -> digits, units -> latin, words -> skeleton"""
    out = []
    for t in compose(tokens(text)):
        tl = t.lower()
        if tl == "₹":
            continue
        if tl in NUM_WORDS:
            out.append((str(NUM_WORDS[tl]), t))
        elif tl in UNITS:
            out.append((UNITS[tl], t))
        elif t.isdigit():
            out.append((t, t))
        else:
            sk = skeleton(t)
            if sk:
                out.append((sk, t))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script"); ap.add_argument("--transcript"); ap.add_argument("--transcript-file")
    ap.add_argument("--min", type=float, default=0.85); ap.add_argument("--json")
    ap.add_argument("--max-run", type=int, default=3, help="this many consecutive missing words fail the line")
    a = ap.parse_args()
    doc = json.load(open(a.script))
    tr = a.transcript if a.transcript is not None else open(a.transcript_file).read()
    T = norm_tokens(tr)
    line_tok = [(l["id"], norm_tokens(l["spoken"])) for l in doc["lines"]]
    S = [(tok, li) for li, (_, toks) in enumerate(line_tok) for tok, _ in toks]
    sm = difflib.SequenceMatcher(None, [s for s, _ in S], [t for t, _ in T], autojunk=False)
    hit_s, hit_t = set(), set()
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            hit_s.add(blk.a + k); hit_t.add(blk.b + k)
    # near-matches (a skeleton off by a letter: 'khatam' vs 'khatm') inside replace opcodes
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "replace":
            for i in range(i1, i2):
                for j in range(j1, j2):
                    if j not in hit_t and difflib.SequenceMatcher(None, S[i][0], T[j][0]).ratio() >= 0.7:
                        hit_s.add(i); hit_t.add(j); break
    res = {"script": a.script, "sha256": doc["sha256"], "lines": [], "extra": []}
    idx = 0; ok_all = True
    for li, (lid, toks) in enumerate(line_tok):
        n = len(toks); got = sum(1 for k in range(idx, idx + n) if k in hit_s)
        cov = got / n if n else 1.0
        missing = [toks[k - idx][1] for k in range(idx, idx + n) if k not in hit_s]
        # the longest run of consecutive missing words: a dropped phrase or sentence, even in a long line
        run_len = best_run = 0
        for k in range(idx, idx + n):
            run_len = run_len + 1 if k not in hit_s else 0; best_run = max(best_run, run_len)
        # numbers are judged token by token in the line's own position: a changed amount can't hide behind the
        # same amount said elsewhere in the reel
        bad_n = [toks[k - idx][1] for k in range(idx, idx + n)
                 if k not in hit_s and (toks[k - idx][0].isdigit() or toks[k - idx][0] in ("lakh", "crore", "percent", "thousand"))]
        if cov < 0.3:
            status = "DROPPED"
        elif bad_n:
            status = "NUMBER"
        elif cov < a.min or best_run >= a.max_run:
            status = "CHANGED"
        else:
            status = "OK"
        ok_all &= status == "OK"
        res["lines"].append({"id": lid, "coverage": round(cov, 2), "status": status, "missing_words": missing,
                             "missing_numbers": bad_n})
        idx += n
    run = []
    for j, (t, orig) in enumerate(T + [("", "")]):
        if j < len(T) and j not in hit_t:
            run.append(orig)
        else:
            if len(run) >= 3:
                res["extra"].append(" ".join(run))
            run = []
    res["verdict"] = "PASS" if ok_all and not res["extra"] else "FAIL"
    if a.json:
        json.dump(res, open(a.json, "w"), indent=1, ensure_ascii=False)
    print(f"{os.path.basename(a.script)} vs transcript: {res['verdict']}  (frozen sha256 {doc['sha256'][:12]})")
    for l in res["lines"]:
        extra = ""
        if l["missing_words"]:
            extra += f"  missing: {' '.join(l['missing_words'])}"
        if l["missing_numbers"]:
            extra += f"  numbers not heard: {l['missing_numbers']}"
        print(f"  {l['status']:8s} {l['id']:4s} coverage {l['coverage']:.2f}{extra}")
    for e in res["extra"]:
        print(f"  EXTRA    heard but not in the script: {e}")


if __name__ == "__main__":
    main()
