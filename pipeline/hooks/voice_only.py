#!/usr/bin/env python3
"""PreToolUse hook on Bash for the script loop's voice step (frontmatter of .claude/agents/reel-7-performance.md):
Bash runs pipeline/voice_cut.py on a lines file under work/ and nothing else.
Allowed: `python3 pipeline/voice_cut.py work/<...>.json work/<...> [--retake ID ...] [--monologue-takes N]`, one
command, no shell operators. Reads the hook's JSON on stdin; exit 2 blocks the command and tells the agent why.
Unreadable input is blocked too: this guard fails closed."""
import json, re, sys

PATH = r"work/[A-Za-z0-9_./-]+"
ALLOWED = re.compile(rf"python3\s+pipeline/voice_cut\.py\s+({PATH}\.json)\s+({PATH})"
                     r"((?:\s+--retake\s+[A-Za-z0-9-]+|\s+--monologue-takes\s+[1-3])*)")

try:
    command = ((json.load(sys.stdin).get("tool_input") or {}).get("command") or "").strip()
except Exception:
    command = None
m = ALLOWED.fullmatch(command) if command else None
if not m or any(".." in g.split("/") for g in (m.group(1), m.group(2))):
    print("Blocked: in this step Bash runs only `python3 pipeline/voice_cut.py work/<slug>/loop/audio/<script>/lines.json "
          "work/<slug>/loop/audio/<script>`, optionally with `--retake <line id>`, from the repository root, one "
          "command with nothing before or after it.", file=sys.stderr)
    sys.exit(2)
