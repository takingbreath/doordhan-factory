#!/usr/bin/env python3
"""Freeze the approved script at the script gate, so the final can be checked against what was approved rather than
against whatever the working copy says by then. Writes registry/scripts/<slug>.json (commit it) with each line's id,
speaker and text exactly as approved (delivery tags kept; `spoken` has them stripped) and a sha256 over the lines.
A frozen script is never overwritten silently: changing an approved script needs --reapprove "<who>: <why>", which
keeps the previous version inside the file's history list.
Usage: script_freeze.py SLUG --lines LINES.json --approved-by Akhilesh [--note "..."] [--reapprove "..."]
  LINES.json: [{"id": "P1", "speaker": "pandey", "text": "[flat, brisk] ..."}, ...]   (or {"P1": "...", ...})
Then, on the final:  script_diff.py registry/scripts/SLUG.json --transcript-file FINAL_SCRIBE.txt"""
import argparse, datetime, hashlib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def spoken(text):
    return re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", " ", text)).strip()


def digest(lines):
    return hashlib.sha256(json.dumps([[l["id"], l["text"]] for l in lines], ensure_ascii=False).encode()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug"); ap.add_argument("--lines", required=True); ap.add_argument("--approved-by", required=True)
    ap.add_argument("--note", default=""); ap.add_argument("--reapprove")
    ap.add_argument("--out-dir", default=os.path.join(ROOT, "registry", "scripts"))
    a = ap.parse_args()
    raw = json.load(open(a.lines))
    if isinstance(raw, dict):
        raw = [{"id": k, "speaker": "", "text": v} for k, v in raw.items()]
    lines = [{"id": l["id"], "speaker": l.get("speaker", ""), "text": l["text"], "spoken": spoken(l["text"])} for l in raw]
    os.makedirs(a.out_dir, exist_ok=True)
    path = os.path.join(a.out_dir, f"{a.slug}.json")
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30))).strftime("%Y-%m-%d %H:%M IST")
    doc = {"slug": a.slug, "approved_by": a.approved_by, "frozen_at": now, "note": a.note, "lines": lines,
           "sha256": digest(lines), "history": []}
    if os.path.exists(path):
        old = json.load(open(path))
        if old["sha256"] == doc["sha256"]:
            print(f"{path}: already frozen with the same lines (sha256 {old['sha256'][:12]}), nothing to do"); return
        if not a.reapprove:
            sys.exit(f"{path} is already frozen (approved by {old['approved_by']} at {old['frozen_at']}). "
                     f"Changing an approved script needs --reapprove \"<who>: <why>\".")
        doc["history"] = old.get("history", []) + [{k: old[k] for k in ("approved_by", "frozen_at", "note", "sha256", "lines")}]
        doc["note"] = f"re-approved: {a.reapprove}" + (f"; {a.note}" if a.note else "")
    json.dump(doc, open(path, "w"), indent=1, ensure_ascii=False)
    print(f"froze {len(lines)} lines -> {path} (sha256 {doc['sha256'][:12]}); commit it")


if __name__ == "__main__":
    main()
