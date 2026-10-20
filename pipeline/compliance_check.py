#!/usr/bin/env python3
"""Hard rule 3 as a check (no model, no network): run it on a script at the script gate and on the posting kit before
it is handed over. It flags; a person decides (Akhilesh or Naveen at the script gate).
- BUY/SELL: a line that may tell viewers to buy or sell (Hinglish, English or Devanagari: "kharid lo", "bech do",
  "buy karo", "add karo", "target price", ...). Telling viewers to buy or sell a specific stock is never allowed.
- RETURN: a percentage next to a return word ("return", "CAGR", "milega", ...) with no "maan ke"/"assume"/"agar" in the
  line: say a return used in a worked example out loud as an assumption ("12% maan ke").
- CAPTION (with --caption): the caption must say "Not investment advice".
  python3 pipeline/compliance_check.py SCRIPT.txt|registry/scripts/<slug>.json [--caption post_kit.md]
Exit 0 nothing to look at, 1 lines to look at (BUY/SELL or RETURN), 2 the caption lacks the disclaimer."""
import argparse, json, re, sys

BUY_SELL = re.compile(r"(?i)\b(kh?ar(i|ee|ii|e)d(o|\s*lo|\s*le|\s*lijiye|\s*daalo)|bech(o|\s*do|\s*dijiye|\s*daalo)|"
                      r"buy\s*(karo|kar\s*lo|now|kijiye)|sell\s*(karo|kar\s*do|now|kijiye)|you\s+should\s+(buy|sell)|"
                      r"(must|should)\s+(buy|sell)|add\s*(karo|kar\s*lo)|accumulate|exit\s*(karo|kar\s*lo)|"
                      r"target\s*price|stop\s*-?\s*loss|paisa\s*lagao|invest\s*(karo|kar\s*do|kar\s*lo))\b"
                      r"|(ख़|ख़|ख)रीद(\s*(लो|लें|लीजिए|डालो)|ो)|बेच\s*(दो|दें|दीजिए|डालो)|बेचो|पैसा\s*लगाओ")
PERCENT = re.compile(r"\d+(\.\d+)?\s*(%|percent|pratishat|प्रतिशत|फ़ीसदी|फीसदी)|"
                     r"(बारह|दस|आठ|पंद्रह|बीस)\s*(परसेंट|प्रतिशत)", re.I)
RETURN = re.compile(r"(?i)return|ritarn|cagr|xirr|milega|milta|badhega|grow|रिटर्न|मिलेगा|मिलता|बढ़ेगा")
ASSUME = re.compile(r"(?i)maan\s*ke|maan\s*lo|maano|assum|agar|suppose|मान\s*के|मान\s*लो|मानो|अगर")
DISCLAIMER = re.compile(r"(?i)not\s+investment\s+advice")


def lines_of(path):
    if path.endswith(".json"):
        doc = json.load(open(path, encoding="utf-8"))
        return [f"{l.get('id', i)} {l.get('speaker', '')}: {l.get('text', '')}" for i, l in enumerate(doc.get("lines", []))]
    return [l.rstrip("\n") for l in open(path, encoding="utf-8")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--caption", help="the posting kit or caption file; must say Not investment advice")
    a = ap.parse_args()
    flags = []
    for n, line in enumerate(lines_of(a.script), 1):
        if BUY_SELL.search(line):
            flags.append(f"BUY/SELL  line {n}: {line.strip()}\n          Is this telling viewers to buy or sell a "
                         "specific stock? That is never allowed (hard rule 3). Explaining what others did is fine.")
        if PERCENT.search(line) and RETURN.search(line) and not ASSUME.search(line):
            flags.append(f"RETURN    line {n}: {line.strip()}\n          Say the return as an assumption "
                         "(\"12% maan ke\") if it is a worked example. A reported fact with its source is fine.")
    code = 1 if flags else 0
    if a.caption:
        if not DISCLAIMER.search(open(a.caption, encoding="utf-8").read()):
            flags.append(f"CAPTION   {a.caption} does not say \"Not investment advice\" (hard rule 3). Add it.")
            code = 2
    print("\n".join(flags) if flags else "compliance: nothing to look at")
    sys.exit(code)


if __name__ == "__main__":
    main()
