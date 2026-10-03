#!/usr/bin/env python3
"""PreToolUse hook on Bash for the script loop's research stages (frontmatter of
.claude/agents/reel-1-research.md): Bash runs the stage's own Python file and nothing else.
Allowed: `python3 work/<...>.py`, one command, no shell operators. Reads the hook's JSON on stdin; exit 2 blocks the
command and tells the agent why. Unreadable input is blocked too: this guard fails closed."""
import json, re, sys

ALLOWED = re.compile(r"python3\s+(work/[A-Za-z0-9_./-]+\.py)")

try:
    command = ((json.load(sys.stdin).get("tool_input") or {}).get("command") or "").strip()
except Exception:
    command = None
m = ALLOWED.fullmatch(command) if command else None
if not m or ".." in m.group(1).split("/"):
    print("Blocked: in this stage Bash runs only `python3 work/<slug>/loop/<your file>.py`, from the repository root, "
          "one command with nothing before or after it. Put the calculation in your Python file and run that.",
          file=sys.stderr)
    sys.exit(2)
