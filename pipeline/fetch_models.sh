#!/usr/bin/env bash
# Fetch the models and packages the QC tools need (lipsync_lag, preflight_keyframe, face_consistency).
# Free, about 600 MB, 2-4 minutes on the cloud machine. Models go to assets/models (git-ignored).
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
M="$ROOT/assets/models"; mkdir -p "$M"
sudo apt-get install -y -q libegl1 libgles2 libgl1 tesseract-ocr tesseract-ocr-hin >/dev/null
pip3 install -q mediapipe onnxruntime pytesseract opencv-python-headless python_speech_features scipy
pip3 install -q torch --index-url https://download.pytorch.org/whl/cpu
[ -s "$M/face_landmarker.task" ] || curl -sSfL -o "$M/face_landmarker.task" \
  https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task
# AuraFace-v1 (Apache-2.0). Not InsightFace buffalo_*: those weights are licensed for non-commercial research only.
[ -s "$M/auraface_glintr100.onnx" ] || curl -sSfL -o "$M/auraface_glintr100.onnx" \
  https://huggingface.co/fal/AuraFace-v1/resolve/main/glintr100.onnx
# SyncNet (Chung & Zisserman 2016) for lipsync_lag's primary score
S="${SYNCNET_DIR:-/home/user/syncnet_python}"
[ -d "$S" ] || git clone -q --depth 1 https://github.com/joonson/syncnet_python.git "$S"
mkdir -p "$S/data"
[ -s "$S/data/syncnet_v2.model" ] || curl -sSfL -o "$S/data/syncnet_v2.model" \
  http://www.robots.ox.ac.uk/~vgg/software/lipsync/data/syncnet_v2.model
echo "QC models ready in $M and $S"
