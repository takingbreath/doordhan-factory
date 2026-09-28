#!/usr/bin/env python3
"""Upload a file to a Higgsfield presigned URL (from the media_upload MCP tool), then call media_confirm.
Usage: put_upload.py FILE "URL" [content-type, default audio/mpeg]
The content type must match what media_upload signed (usually audio/mpeg for .mp3, image/png for .png).
A video under outputs/ (a final) is refused unless qc_gate.py stamped that exact file (pipeline/qc_stamp.py)."""
import os, sys, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qc_stamp import check
f, url = sys.argv[1], sys.argv[2]
ok, why = check(f)
if not ok:
    sys.exit(why)
ctype = sys.argv[3] if len(sys.argv) > 3 else "audio/mpeg"
# Higgsfield's upload host (Sept 2026) sits behind Cloudflare, which answers 403 "error code: 1010" to Python's default
# User-Agent; and its presigned URLs sign an If-None-Match header, which S3 then requires
headers = {"Content-Type": ctype, "User-Agent": "doordhan-factory/1.0 (put_upload.py)"}
if "if-none-match" in urllib.parse.unquote(url).lower():
    headers["If-None-Match"] = "*"
req = urllib.request.Request(url, data=open(f, "rb").read(), headers=headers, method="PUT")
with urllib.request.urlopen(req, timeout=120) as r:
    print(f"{f} -> HTTP {r.status}")
