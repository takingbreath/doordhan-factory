#!/bin/bash
# Remove the Gemini sparkle mark from a Gemini-app picture.
# Usage: clear_sparkle.sh IN.png OUT.png [CHECK.png]
#
# Measured on 2026-10-14 (1536x2752, 9:16): the sparkle is a 96x96 px star whose box starts
# 192 px from the right edge and 192 px from the bottom edge, measured to the far side of the box
# (box = x 1248..1344, y 2464..2560). That is size = short side / 16, margin = short side / 8.
# 2026-10-15: a 4:5 picture (1856x2304) has the SAME star: 96 px, 192 px from the right and bottom
# edges. So the mark has a fixed pixel size and margin; it does not scale with the picture.
# Always look at the CHECK picture; if a new size misses, measure again and set SIZE / MARGIN below.
#
# Method: ffmpeg delogo (fills the box from its border pixels). The mark sits on plain background
# in most pictures, so the fill is invisible. Keep the AI label on the post: this removes a visual
# mark only; the picture is still AI-made and still carries Google's invisible SynthID mark.
set -euo pipefail
IN="$1"; OUT="$2"; CHECK="${3:-}"
# 2026-10-16: Gemini moved the star to 64 px from the right and bottom edges (same 96 px size).
# find_sparkle.py picks the margin (64 or 192) that holds the star, unless SPARKLE_MARGIN is set.
SIZE=${SPARKLE_SIZE:-96}; PAD_DIV=8
MARGIN=${SPARKLE_MARGIN:-$(python3 -W ignore "$(dirname "$0")/find_sparkle.py" "$IN" "$SIZE" 2>/dev/null || echo 192)}
read -r W H < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$IN" | tr ',' ' ')
PAD=$(( SIZE / PAD_DIV ))
X=$(( W - MARGIN - SIZE - PAD )); Y=$(( H - MARGIN - SIZE - PAD )); BW=$(( SIZE + 2 * PAD )); BH=$(( SIZE + 2 * PAD ))
ffmpeg -loglevel error -y -i "$IN" -vf "delogo=x=$X:y=$Y:w=$BW:h=$BH" -frames:v 1 "$OUT"
echo "image ${W}x${H}; cleared box x=$X y=$Y w=$BW h=$BH -> $OUT"
if [ -n "$CHECK" ]; then
  CX=$(( X - BW )); CY=$(( Y - BH )); CW=$(( BW * 3 )); CH=$(( BH * 3 ))
  ffmpeg -loglevel error -y -i "$IN" -i "$OUT" -filter_complex \
    "[0]crop=$CW:$CH:$CX:$CY[a];[1]crop=$CW:$CH:$CX:$CY[b];[a][b]hstack" -frames:v 1 "$CHECK"
  echo "check (before | after): $CHECK"
fi
