#!/usr/bin/env bash
# Fetch the models and packages the QC tools need (lipsync_lag, preflight_keyframe, face_consistency).
# Free, about 600 MB, 2-4 minutes on the cloud machine. Models go to assets/models (git-ignored).
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
M="$ROOT/assets/models"; mkdir -p "$M"
if [ "$(uname)" = "Darwin" ]; then
  # macOS (2026-10-03): MediaPipe has no wheel for Homebrew's Python 3.14, so the QC tools get their own Python 3.11
  # environment (MediaPipe 1.0.1 aborts on macOS with "Service is unavailable"; 0.10.21 works). Run the pipeline with
  # it: ~/.venvs/doordhan-qc/bin/python pipeline/qc_gate.py ...
  brew list tesseract >/dev/null 2>&1 || brew install -q tesseract tesseract-lang
  V="$HOME/.venvs/doordhan-qc"
  [ -x "$V/bin/python" ] || uv venv -q -p python3.11 "$V"
  VIRTUAL_ENV="$V" uv pip install -q "numpy<2" pillow "scipy==1.16.2" "mediapipe==0.10.21" onnxruntime pytesseract \
    "opencv-python-headless==4.11.0.86" python_speech_features torch fonttools   # MediaPipe 0.10.21 needs numpy 1.x
  # collage reels (jio01): pdftoppm renders filing pages; rembg cuts photos out, in its own environment so its
  # dependencies can't move the QC environment's pinned numpy
  brew list poppler >/dev/null 2>&1 || brew install -q poppler
  C="$HOME/.venvs/doordhan-cut"
  [ -x "$C/bin/python" ] || uv venv -q -p python3.11 "$C"
  VIRTUAL_ENV="$C" uv pip install -q "rembg[cpu]"
  CUTPY="$C/bin/python"
else
  # a fresh cloud container has empty package lists: install fails with "Unable to locate package" (nana01, 2026-10-09)
  (sudo apt-get update -q || apt-get update -q) >/dev/null 2>&1
  (sudo apt-get install -y -q libegl1 libgles2 libgl1 tesseract-ocr tesseract-ocr-hin poppler-utils || \
   apt-get install -y -q libegl1 libgles2 libgl1 tesseract-ocr tesseract-ocr-hin poppler-utils) >/dev/null
  # "pip3" can belong to another Python than "python3" (the cloud image, 2026-10-19: pip3 -> 3.13, python3 -> 3.11), so
  # every install goes through the python3 that runs the pipeline
  PIP="python3 -m pip"
  $PIP install -q mediapipe onnxruntime pytesseract opencv-python-headless scipy numpy pillow praat-parselmouth fonttools
  # python_speech_features fails to build in an isolated env there; without isolation (and with Debian's setuptools,
  # SETUPTOOLS_USE_DISTUTILS=stdlib) it installs
  $PIP install -q python_speech_features || $PIP install -q --no-build-isolation python_speech_features || \
    SETUPTOOLS_USE_DISTUTILS=stdlib $PIP install -q --no-build-isolation python_speech_features
  $PIP install -q torch --index-url https://download.pytorch.org/whl/cpu
  $PIP install -q "rembg[cpu]"
  CUTPY=python3
fi
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
