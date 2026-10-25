#!/bin/zsh
# silver01: build the edit, finish it twice (old-TV look for Pandey and Billu, nothing for the chart), join them.
# The chart scenes come from the clean pass: no filter on the chart (Akhilesh, 2026-10-25). Run from anywhere.
set -e
cd "$(dirname "$0")/../.."
mkdir -p outputs/silver01/_pass
pipeline/qcpy work/silver01/build.py 2>&1 | grep -i "Traceback\|Error:\|wrote\|total" || true
pipeline/qcpy pipeline/assemble.py work/silver01/edit.json 2>&1 | grep -v "^W0000\|^INFO\|^I0000" | tail -2
pipeline/qcpy pipeline/assemble.py work/silver01/edit_clean.json 2>&1 | grep -v "^W0000\|^INFO\|^I0000" | tail -1
EN=$(python3 -c "import json;print('+'.join(f'between(t,{a:.3f},{b:.3f})' for a,b in json.load(open('work/silver01/chart_windows.json'))))")
ffmpeg -v error -y -i outputs/silver01/_pass/looked.mp4 -i outputs/silver01/_pass/clean.mp4 \
  -filter_complex "[0:v][1:v]overlay=enable='${EN}':shortest=1[v]" -map "[v]" -map 0:a \
  -c:v libx264 -crf 14 -preset medium -pix_fmt yuv420p -c:a copy -movflags +faststart outputs/silver01/E14_silver_pattern.mp4
cp outputs/silver01/_pass/looked_prefinish.mkv outputs/silver01/E14_silver_pattern_prefinish.mkv 2>/dev/null || true
echo "final: outputs/silver01/E14_silver_pattern.mp4 (chart windows: ${EN})"
