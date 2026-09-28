#!/usr/bin/env python3
"""The QC stamp: proof that qc_gate.py passed this exact file. Anything under outputs/ that is a video needs one to
leave the machine: the SendUserFile hook (pipeline/hooks/require_qc_stamp.py) and put_upload.py (the Higgsfield
upload behind the emailed link) both call check() and refuse an unstamped or changed file.
A stamp is <final stem>.qc.json next to the final, written by qc_gate.py; it lists the sha256 of the final and of
the files derived from it (the _phone copy) under "covers", with the verdict.
Usage: qc_stamp.py FILE   (exit 0 if FILE may be sent, 2 with the reason if not)"""
import glob, hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUARDED = os.path.join(ROOT, "outputs")
VIDEO = (".mp4", ".mov", ".mkv", ".webm", ".m4v", ".avi")
SENDABLE = ("PASS",)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def guarded(path):
    p = os.path.realpath(path)
    return p.lower().endswith(VIDEO) and p.startswith(os.path.realpath(GUARDED) + os.sep)


def check(path):
    """(ok, reason). Files outside outputs/ or that aren't video are not gated."""
    if not guarded(path):
        return True, "not a final (not a video under outputs/)"
    if not os.path.exists(path):
        return False, f"{path} does not exist"
    digest = sha256(path)
    seen = []
    for st in glob.glob(os.path.join(os.path.dirname(os.path.realpath(path)), "*.qc.json")):
        try:
            doc = json.load(open(st))
        except Exception:
            continue
        if digest in doc.get("covers", {}).values():
            if doc.get("verdict") in SENDABLE:
                return True, f"stamped {doc['verdict']} by {os.path.basename(st)} at {doc.get('at')}"
            seen.append(f"{os.path.basename(st)} says {doc.get('verdict')}")
    why = "; ".join(seen) if seen else "no QC stamp covers this exact file (changed since the gate, or never gated)"
    return False, (f"QC gate: {os.path.relpath(path, ROOT)} is blocked: {why}. Run python3 pipeline/qc_gate.py "
                   f"<manifest> and send only a final it passes, with its QC summary.")


if __name__ == "__main__":
    ok, why = check(sys.argv[1])
    print(why, file=sys.stdout if ok else sys.stderr)
    sys.exit(0 if ok else 2)
