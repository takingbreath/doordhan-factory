#!/usr/bin/env python3
"""PreToolUse hook on SendUserFile (.claude/settings.json): a final video only reaches Akhilesh with a QC stamp.
Reads the hook's JSON on stdin; for every file that is a video under outputs/, requires a qc_gate.py stamp covering
that exact file (pipeline/qc_stamp.py). Exit 2 blocks the send and tells Claude why; anything else passes."""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qc_stamp import check, ROOT  # noqa: E402

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)
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
