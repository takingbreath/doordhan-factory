#!/bin/zsh
# silver01: build -> assemble (old-TV finish) -> phone copy -> transcript -> QC gate. Run from the repo root.
set -e
F=outputs/silver01/E14_silver_pattern.mp4
bash work/silver01/make_final.sh
ffmpeg -v error -y -i $F -c:v libx264 -crf 28 -preset slow -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart outputs/silver01/E14_silver_pattern_phone.mp4
python3 pipeline/transcribe.py $F --json work/silver01/final.scribe.json > /dev/null 2>&1
python3 -c "import json;open('work/silver01/final_transcript.txt','w').write(json.load(open('work/silver01/final.scribe.json'))['text']+'\n')"
pipeline/qcpy pipeline/qc_gate.py bind-transcript $F work/silver01/final_transcript.txt 2>&1 | tail -1
pipeline/qcpy pipeline/qc_gate.py work/silver01/qc_manifest.json 2>&1 | grep -v "^W0000\|^INFO\|^I0000\|^WARNING" | tail -32
