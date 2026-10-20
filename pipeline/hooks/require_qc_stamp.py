#!/usr/bin/env python3
"""PreToolUse hook on SendUserFile (.claude/settings.json): a reel only reaches Akhilesh or Naveen with a QC stamp.
Reads the hook's JSON on stdin; for every video under outputs/, and every other video of 15 s or more, requires a
qc_gate.py stamp covering that exact file (pipeline/qc_stamp.py). Exit 2 blocks the send and tells Claude why;
unreadable input is blocked too."""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qc_stamp import check, ROOT  # noqa: E402

try:
    data = json.load(sys.stdin)
except Exception:  # fail closed: a send we can't read is a send we can't check
    print("QC gate: the SendUserFile hook could not read the call, so it blocks it. Send again.", file=sys.stderr)
    sys.exit(2)
files = (data.get("tool_input") or {}).get("files") or []
if isinstance(files, str):
    files = [files]
cwd = data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or ROOT
blocked = []
for f in files:
    p = f if os.path.isabs(f) else os.path.join(cwd, f)
    ok, why = check(p)
    if not ok:
        blocked.append(why)
if blocked:
    print("\n".join(blocked), file=sys.stderr)
    sys.exit(2)
