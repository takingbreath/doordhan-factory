#!/usr/bin/env python3
"""The QC stamp: proof that qc_gate.py passed this exact file. Every video under outputs/, and any other video of
15 s or more wherever it is (a copy of a reel in work/ or /tmp, an edit_raw, a draft), needs one to leave the machine;
shorter clips (a test shot, a 5 s experiment) pass without one. The SendUserFile hook
(pipeline/hooks/require_qc_stamp.py) and put_upload.py (the Higgsfield upload behind the emailed link) both call
check() and refuse an unstamped or changed file.
A stamp is <final stem>.qc.json next to the final, written by qc_gate.py; it lists the sha256 of the final and of
the files derived from it (the _phone copy) under "covers", with the verdict.
Usage: qc_stamp.py FILE   (exit 0 if FILE may be sent, 2 with the reason if not)"""
import glob, hashlib, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUARDED = os.path.join(ROOT, "outputs")
VIDEO = (".mp4", ".mov", ".mkv", ".webm", ".m4v", ".avi")
SENDABLE = ("PASS",)
LONG_S = 15.0   # a reel is 20-70 s; a single shot is at most about 8 s


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def duration(path):
    """Seconds, or None when ffprobe can't read the file."""
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                             capture_output=True, text=True, timeout=30).stdout.strip()
        return float(out)
    except Exception:
        return None


def guarded(path):
    p = os.path.realpath(path)
    if not p.lower().endswith(VIDEO):
        return False
    if p.startswith(os.path.realpath(GUARDED) + os.sep) or not os.path.exists(p):
        return True
    d = duration(p)
    return d is None or d >= LONG_S   # unreadable counts as long: fail closed


def check(path):
    """(ok, reason). Not gated: files that aren't video, and videos outside outputs/ shorter than 15 s."""
    if not guarded(path):
        return True, "not a final (not a video, or a clip under 15 s outside outputs/)"
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
                   f"<manifest> and send only a final it passes, with its QC summary (the final under outputs/, "
                   f"not a copy: the stamp sits next to it).")


if __name__ == "__main__":
    ok, why = check(sys.argv[1])
    print(why, file=sys.stdout if ok else sys.stderr)
    sys.exit(0 if ok else 2)
