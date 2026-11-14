#!/bin/bash
# Save a Gemini full-size picture or video WITHOUT the Mac Save sheet (tested 2026-10-16).
# Use it when the Save sheet cannot appear (for example the session window is closed, so the
# browser pane is hidden) or as the default: it touches nothing on the Mac desktop.
# 1. In the Gemini tab, run the JS from capture_full_url.js (javascript_tool). It hooks fetch,
#    clicks the LAST "Download full-sized image" button, and returns the final
#    lh3.googleusercontent.com/rd-gg/... URL (the longest one ending in "=s0-d-I?alr=yes").
# 2. fetch_full.sh 'URL' DEST.png   (quote the URL). It checks the result is an image or video.
# The URL is a private capability link to the owner's file: never share it or put it in a post.
set -euo pipefail
URL="$1"; DEST="$2"
TMP="$(mktemp)"
code=$(curl -sL -o "$TMP" -w '%{http_code}' "$URL")
type=$(file -b "$TMP")
if [ "$code" != "200" ] || ! echo "$type" | grep -qiE 'PNG|JPEG|ISO Media|MP4|WebP'; then
  echo "fetch failed: HTTP $code, $type" >&2; rm -f "$TMP"; exit 1
fi
mkdir -p "$(dirname "$DEST")"; mv "$TMP" "$DEST"
echo "saved $DEST ($type)"
