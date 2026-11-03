#!/usr/bin/env bash
# Fetch the models and packages the QC tools need (lipsync_lag, preflight_keyframe, face_consistency).
# Free, about 600 MB, 2-4 minutes on the cloud machine. Models go to assets/models (git-ignored).
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
M="$ROOT/assets/models"; mkdir -p "$M"
# ONE recipe on every machine: a Python 3.11 or 3.12 venv at ~/.venvs/doordhan-qc (pipeline/qcpy prefers it), filled from
# the pinned requirements.txt. The pins (numpy 1.26.4, torch 2.2.2, MediaPipe 0.10.21) have no Python 3.13+ wheels, and the
# cloud image's python3 is now 3.13 (2026-11-03): installing the pins into python3 failed, the session hook stopped there, and
# the QC tools were never installed. rembg lives in its own venv (requirements-cut.txt) so it can't move the pinned numpy.
if command -v uv >/dev/null 2>&1; then
  mkvenv() { uv venv -q -p "$2" "$1"; }
  pipin() { VIRTUAL_ENV="$1" uv pip install -q "${@:2}"; }
else
  mkvenv() { "$2" -m venv "$1"; }
  pipin() { "$1/bin/python" -m pip install -q "${@:2}"; }
fi
PYV="$(command -v python3.11 || command -v python3.12 || true)"      # 3.11 first: MediaPipe has no macOS wheel for 3.12+
[ -n "$PYV" ] || PYV=python3.11     # uv can fetch 3.11 itself; without uv and without 3.11/3.12 this fails loudly below
if [ "$(uname)" = "Darwin" ]; then
  brew list tesseract >/dev/null 2>&1 || brew install -q tesseract tesseract-lang
  brew list poppler >/dev/null 2>&1 || brew install -q poppler
else
  # a fresh cloud container has empty package lists: install fails with "Unable to locate package" (nana01, 2026-10-09)
  (sudo apt-get update -q || apt-get update -q) >/dev/null 2>&1
  (sudo apt-get install -y -q libegl1 libgles2 libgl1 tesseract-ocr tesseract-ocr-hin poppler-utils || \
   apt-get install -y -q libegl1 libgles2 libgl1 tesseract-ocr tesseract-ocr-hin poppler-utils) >/dev/null
fi
V="$HOME/.venvs/doordhan-qc"
[ -x "$V/bin/python" ] || mkvenv "$V" "$PYV"
case "$("$V/bin/python" -c 'import sys; print("%d.%d" % sys.version_info[:2])')" in
  3.11|3.12) ;;
  *) echo "$V runs a Python the pinned requirements have no wheels for; delete it and rerun (needs python3.11 or 3.12)" >&2; exit 1 ;;
esac
# Linux: torch from the CPU index first (the default wheel drags in about 2 GB of CUDA libraries nobody here uses)
[ "$(uname)" = "Darwin" ] || pipin "$V" "torch==2.2.2" --index-url https://download.pytorch.org/whl/cpu
pipin "$V" -r "$ROOT/requirements.txt"
C="$HOME/.venvs/doordhan-cut"        # collage reels (jio01): rembg cuts photos out; pdftoppm (poppler) renders filing pages
[ -x "$C/bin/python" ] || mkvenv "$C" "$PYV"
pipin "$C" -r "$ROOT/requirements-cut.txt"
CUTPY="$C/bin/python"
# the cut-out model for pipeline/cutout.py (about 180 MB, once)
"$CUTPY" -c "from rembg import new_session; new_session('isnet-general-use')" >/dev/null 2>&1   # quick once cached
[ -s "$M/face_landmarker.task" ] || curl -sSfL -o "$M/face_landmarker.task" \
  https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task
# AuraFace-v1 (Apache-2.0). Not InsightFace buffalo_*: those weights are licensed for non-commercial research only.
[ -s "$M/auraface_glintr100.onnx" ] || curl -sSfL -o "$M/auraface_glintr100.onnx" \
  https://huggingface.co/fal/AuraFace-v1/resolve/main/glintr100.onnx
# SyncNet (Chung & Zisserman 2016) for lipsync_lag's primary score
S="${SYNCNET_DIR:-$HOME/syncnet_python}"
[ -d "$S" ] || git clone -q --depth 1 https://github.com/joonson/syncnet_python.git "$S"
mkdir -p "$S/data"
[ -s "$S/data/syncnet_v2.model" ] || curl -sSfL -o "$S/data/syncnet_v2.model" \
  http://www.robots.ox.ac.uk/~vgg/software/lipsync/data/syncnet_v2.model
echo "QC models ready in $M and $S"
