#!/bin/bash
# Cloud sessions only: every Claude Code cloud session on this repo must be able to produce a video, because the
# cloud route is Naveen's only route and Akhilesh's fallback ("produce it here"); the laptop sets itself up once with
# pipeline/fetch_models.sh. Installs ffmpeg, poppler, the Python packages, the QC models, SyncNet and rembg.
# Idempotent: when everything is there (a cached container), it only checks, in a few seconds. A fresh container
# takes several minutes once; the environment is cached after the hook finishes.
set -euo pipefail
[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0
cd "$CLAUDE_PROJECT_DIR"
LOG=/tmp/doordhan-session-start.log

ready() {
  command -v ffmpeg >/dev/null && command -v pdftoppm >/dev/null &&
  python3 -c "import numpy, PIL, fontTools, scipy, cv2, mediapipe, onnxruntime, torch, python_speech_features, parselmouth, rembg" \
    >/dev/null 2>&1 &&
  [ -s assets/models/face_landmarker.task ] && [ -s assets/models/auraface_glintr100.onnx ] &&
  [ -s "${SYNCNET_DIR:-$HOME/syncnet_python}/data/syncnet_v2.model" ] &&
  { [ -s "$HOME/.rembg/models/isnet-general-use/isnet-general-use.onnx" ] || [ -s "$HOME/.u2net/isnet-general-use.onnx" ]; }
}

if ready; then
  echo "Doordhan: production tools ready (cloud route)."
  exit 0
fi
if {
  command -v ffmpeg >/dev/null || { (sudo apt-get update -q || apt-get update -q) && (sudo apt-get install -y -q ffmpeg || apt-get install -y -q ffmpeg); }
  python3 -m pip install -q -r requirements.txt
  bash pipeline/fetch_models.sh
} >>"$LOG" 2>&1 && ready; then
  echo "Doordhan: production tools installed (cloud route)."
else
  # never block the session (the morning desk needs none of this); production will see it in produce_check.py
  echo "Doordhan: production tool setup incomplete; see $LOG, then run: bash pipeline/fetch_models.sh"
fi
exit 0
