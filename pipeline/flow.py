#!/usr/bin/env python3
"""The /make-reel flow's state: one file per reel, registry/flows/<slug>.json, committed at every gate so any session
(the laptop, a cloud session, tomorrow) can see where a reel stands and continue it. It keeps the order of the gates,
whatever anyone types: research -> script -> format -> voice -> graphics -> production -> final.

  python3 pipeline/flow.py new SLUG --topic "..." --by Naveen        start a reel (stage: research)
  python3 pipeline/flow.py list                                      reels not finished yet
  python3 pipeline/flow.py show SLUG                                 where it stands and the one thing to do next
  python3 pipeline/flow.py done SLUG research --brief research/briefs/SLUG.md  [--skip "why"]
  python3 pipeline/flow.py done SLUG script --by Naveen --words N    the script is confirmed (N spoken words)
  python3 pipeline/flow.py done SLUG format --value samachar|sahayata_kendra|creator --by Naveen
           [--exception-by Akhilesh --quote "his words"]           a script longer than the format allows
  python3 pipeline/flow.py done SLUG voice --by Naveen --value <voice cut file>
  python3 pipeline/flow.py done SLUG graphics --value A|B|C --by Naveen [--experiment]
  python3 pipeline/flow.py done SLUG production --value outputs/SLUG/<final>.mp4      (needs a PASS QC stamp)
  python3 pipeline/flow.py done SLUG final --by Naveen|Akhilesh
Exit 1 with the reason when a step is out of order or breaks a rule."""
import argparse, datetime as dt, json, os, subprocess, sys

ROOT = os.environ.get("DOORDHAN_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLOWS = os.path.join(ROOT, "registry", "flows")
STAGES = ["research", "script", "format", "voice", "graphics", "production", "final"]
APPROVERS = {"script": ("akhilesh", "naveen"), "voice": ("akhilesh", "naveen"), "final": ("akhilesh", "naveen"),
             "format": ("akhilesh", "naveen"), "graphics": ("akhilesh", "naveen")}
# the formats the flow offers (Akhilesh, 2026-10-20: the three that are ready; Teleshop has no voice for Sachdev)
FORMATS = {
    "samachar": {"name": "Doordhan Samachar (Sarika, Gupta)", "words": (50, 75), "seconds": "20-30 s",
                 "tested_graphics": ["A"], "file": "formats/samachar.md"},
    "sahayata_kendra": {"name": "Sahayata Kendra (Pandey, a caller, Billu)", "words": (90, 155), "seconds": "40-60 s, 70 at most",
                        "tested_graphics": ["A"], "file": "formats/sahayata_kendra.md"},
    "creator": {"name": "Creator (Rashmi at home)", "words": (50, 75), "seconds": "20-30 s",
                "tested_graphics": ["B", "C"], "file": "formats/creator.md"},
}
GRAPHICS = {"A": "Broadcast cards (old-TV navy and gold: E7, E8)", "B": "Vox collage (torn paper, cut-out photos: E11)",
            "C": "Creator captions and stickers (E10)"}
NEXT = {
    "research": "Research the story (no credits): write research/briefs/{slug}.md, send the summary, then ask for the script.",
    "script": "Wait for the script. Check facts, length and the hard rules (pipeline/compliance_check.py); report, don't rewrite. Record it when the approver says confirmed.",
    "format": "Show the formats that fit ({fits}) with docs/gallery pictures and a recommendation; record the choice, freeze the script, `spend.py start {slug}`.",
    "voice": "Make the voice cut in the format's voice (no Higgsfield credits), check it (verify_line, transcript), send it; record the approval.",
    "graphics": "Show docs/gallery/graphics_styles.jpg (A, B, C) with the tested ones for this format and a recommendation; record the choice.",
    "production": "Produce it (.claude/skills/produce-video from step 4) inside the budget; run the QC gate; record the stamped final.",
    "final": "Send the stamped final with what was checked; record the approval; then the posting kit (compliance_check --caption), the registry log and the push.",
}


def now():
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def path(slug):
    return os.path.join(FLOWS, f"{slug}.json")


def load(slug):
    try:
        return json.load(open(path(slug), encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"no reel {slug!r}: start one with `python3 pipeline/flow.py new {slug} --topic ... --by ...`")


def save(doc):
    os.makedirs(FLOWS, exist_ok=True)
    with open(path(doc["slug"]), "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
        f.write("\n")


def stage_of(doc):
    for s in STAGES:
        if s not in doc["gates"]:
            return s
    return "done"


def fits(words):
    return [k for k, f in FORMATS.items() if words is not None and words <= f["words"][1]]


def show(doc):
    st = stage_of(doc)
    lines = [f"{doc['slug']}: {doc['topic']}  (started by {doc['by']}, {doc['started'][:10]})", f"  stage now: {st}"]
    for s in STAGES:
        g = doc["gates"].get(s)
        if g:
            extra = ", ".join(f"{k}={v}" for k, v in g.items() if k not in ("at",))
            lines.append(f"  done  {s:<10} {extra}  ({g['at'][:16]})")
    if st != "done":
        words = (doc["gates"].get("script") or {}).get("words")
        f = ", ".join(fits(words)) or "none: the script needs a cut, or Akhilesh's exception"
        lines.append("  next: " + NEXT[st].format(slug=doc["slug"], fits=f))
    return "\n".join(lines)


def fail(msg):
    sys.exit("Not recorded: " + msg)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new"); n.add_argument("slug"); n.add_argument("--topic", required=True); n.add_argument("--by", required=True)
    sub.add_parser("list")
    s = sub.add_parser("show"); s.add_argument("slug")
    d = sub.add_parser("done"); d.add_argument("slug"); d.add_argument("stage", choices=STAGES)
    d.add_argument("--by"); d.add_argument("--value"); d.add_argument("--words", type=int); d.add_argument("--brief")
    d.add_argument("--skip"); d.add_argument("--note"); d.add_argument("--experiment", action="store_true")
    d.add_argument("--exception-by"); d.add_argument("--quote")
    a = ap.parse_args()

    if a.cmd == "new":
        if not a.slug.replace("_", "").isalnum() or a.slug != a.slug.lower():
            fail("a slug is lowercase letters, digits and _ (e.g. gold01)")
        if os.path.exists(path(a.slug)) or os.path.exists(os.path.join(ROOT, "registry", "scripts", f"{a.slug}.json")):
            fail(f"{a.slug} is taken; pick the next number")
        doc = {"slug": a.slug, "topic": a.topic, "by": a.by, "started": now(), "gates": {}}
        save(doc); print(show(doc)); return
    if a.cmd == "list":
        for f in sorted(os.listdir(FLOWS)) if os.path.isdir(FLOWS) else []:
            if f.endswith(".json"):
                doc = json.load(open(os.path.join(FLOWS, f), encoding="utf-8"))
                if stage_of(doc) != "done":
                    print(f"{doc['slug']:<14} stage {stage_of(doc):<10} {doc['topic']}")
        return
    doc = load(a.slug)
    if a.cmd == "show":
        print(show(doc)); return

    st = stage_of(doc)
    if a.stage in doc["gates"]:
        fail(f"{a.stage} is already done for {a.slug}. A change after a gate is a new approval: say so to the approver.")
    if a.stage != st:
        fail(f"{a.slug} is at '{st}', so '{a.stage}' can't be recorded yet. The order is {' -> '.join(STAGES)}.")
    g = {"at": now()}
    if a.stage in APPROVERS:
        if not a.by or a.by.strip().lower().split()[0] not in APPROVERS[a.stage]:
            fail(f"the {a.stage} gate is approved by Akhilesh or Naveen (--by), in their own words in this session")
        g["by"] = a.by
    if a.stage == "research":
        if a.skip:
            g["skipped"] = a.skip
        elif not a.brief or not os.path.exists(os.path.join(ROOT, a.brief)):
            fail("give --brief research/briefs/<slug>.md (written and committed), or --skip \"why\"")
        else:
            g["brief"] = a.brief
    if a.stage == "script":
        if not a.words:
            fail("give --words: the spoken words in the confirmed script")
        g["words"] = a.words
    if a.stage == "format":
        if a.value not in FORMATS:
            fail(f"the formats on offer are {', '.join(FORMATS)} (Teleshop has no voice yet; new formats are Akhilesh's call)")
        lo, hi = FORMATS[a.value]["words"]
        words = doc["gates"]["script"]["words"]
        if words > hi:
            if (a.exception_by or "").strip().lower() != "akhilesh" or not a.quote:
                fail(f"the script has {words} words; {a.value} takes {hi} at most ({FORMATS[a.value]['seconds']}). "
                     "Ask the approver for a cut, or Akhilesh for an exception (--exception-by Akhilesh --quote \"...\").")
            g["length_exception"] = {"by": a.exception_by, "quote": a.quote}
        if words < lo:
            g["note"] = f"short: {words} words, the format usually has {lo}+"
        g["value"] = a.value
    if a.stage == "voice":
        if not a.value:
            fail("give --value: the voice cut that was approved")
        g["value"] = a.value
    if a.stage == "graphics":
        if a.value not in GRAPHICS:
            fail("graphics is A, B or C (docs/gallery/graphics_styles.jpg)")
        tested = FORMATS[doc["gates"]["format"]["value"]]["tested_graphics"]
        if a.value not in tested and not a.experiment:
            fail(f"{a.value} hasn't been made with this format yet (tested: {', '.join(tested)}). Offer it as an "
                 "experiment and record it with --experiment if the approver still wants it.")
        g["value"] = a.value
        if a.value not in tested:
            g["experiment"] = True
    if a.stage == "production":
        if not a.value or not os.path.exists(os.path.join(ROOT, a.value)):
            fail("give --value outputs/<slug>/<final>.mp4")
        r = subprocess.run([sys.executable, os.path.join(ROOT, "pipeline", "qc_stamp.py"), os.path.join(ROOT, a.value)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            fail("the final has no PASS stamp: " + (r.stderr or r.stdout).strip())
        g["value"] = a.value
    if a.note:
        g["note"] = a.note
    doc["gates"][a.stage] = g
    save(doc)
    print(show(doc))
    print(f"commit it: git add registry/flows/{a.slug}.json && git commit -m '{a.slug}: {a.stage} done' && git push")


if __name__ == "__main__":
    main()
