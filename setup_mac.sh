#!/usr/bin/env bash
# One-shot setup for a Mac (Intel or Apple silicon). Safe to re-run: every step skips what is already done.
# Usage: bash setup_mac.sh
# It never writes API keys: it copies .env.example to .env if there is no .env, and you fill in the keys.
set -u
ROOT="$(cd "$(dirname "$0")" && pwd)"; cd "$ROOT"
say() { printf '\n==> %s\n' "$*"; }
SKIPPED=()

say "uv (Python environments)"
command -v uv >/dev/null || { command -v brew >/dev/null && brew install uv || curl -LsSf https://astral.sh/uv/install.sh | sh; }
export PATH="$HOME/.local/bin:$PATH"

say "QC environment: ~/.venvs/doordhan-qc (Python 3.11, from requirements.txt)"
V="$HOME/.venvs/doordhan-qc"
[ -x "$V/bin/python" ] || uv venv -q -p 3.11 "$V"
VIRTUAL_ENV="$V" uv pip install -q -r requirements.txt

say "ffmpeg and ffprobe (static builds, linked into a folder on PATH)"
if ! command -v ffmpeg >/dev/null || ! command -v ffprobe >/dev/null; then
  "$V/bin/python" -c "import static_ffmpeg.run as r; r.get_or_fetch_platform_executables_else_raise()"
  D="$("$V/bin/python" -c "import static_ffmpeg,os;print(os.path.join(os.path.dirname(static_ffmpeg.__file__),'bin','darwin'))")"
  T=/usr/local/bin; [ -w "$T" ] || { T="$HOME/.local/bin"; mkdir -p "$T"; echo "NOTE: add $T to your PATH"; }
  chmod +x "$D/ffmpeg" "$D/ffprobe"; ln -sf "$D/ffmpeg" "$T/ffmpeg"; ln -sf "$D/ffprobe" "$T/ffprobe"
fi
ffmpeg -version | head -1

say "tesseract and poppler (OCR for on-screen text, PDF pages for collage reels)"
if command -v brew >/dev/null; then
  brew list tesseract >/dev/null 2>&1 || brew install -q tesseract tesseract-lang || SKIPPED+=("tesseract (Homebrew refused: update Xcode Command Line Tools in System Settings > Software Update, then re-run)")
  brew list poppler  >/dev/null 2>&1 || brew install -q poppler || SKIPPED+=("poppler (same reason)")
else SKIPPED+=("tesseract, poppler (no Homebrew)"); fi

say "cut-out environment: ~/.venvs/doordhan-cut (rembg, kept apart so it can't move the pinned numpy)"
C="$HOME/.venvs/doordhan-cut"
[ -x "$C/bin/python" ] || uv venv -q -p 3.11 "$C"
VIRTUAL_ENV="$C" uv pip install -q "rembg[cpu]"
"$C/bin/python" -c "from rembg import new_session; new_session('isnet-general-use')" >/dev/null 2>&1 || SKIPPED+=("rembg model download")

say "models (about 600 MB, once) into assets/models and ~/syncnet_python"
M="$ROOT/assets/models"; mkdir -p "$M"
[ -s "$M/face_landmarker.task" ] || curl -sSfL -o "$M/face_landmarker.task" \
  https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task
[ -s "$M/auraface_glintr100.onnx" ] || curl -sSfL -o "$M/auraface_glintr100.onnx" \
  https://huggingface.co/fal/AuraFace-v1/resolve/main/glintr100.onnx
S="${SYNCNET_DIR:-$HOME/syncnet_python}"
[ -d "$S" ] || git clone -q --depth 1 https://github.com/joonson/syncnet_python.git "$S"
mkdir -p "$S/data"
[ -s "$S/data/syncnet_v2.model" ] || curl -sSfL -o "$S/data/syncnet_v2.model" \
  http://www.robots.ox.ac.uk/~vgg/software/lipsync/data/syncnet_v2.model

say "Higgsfield CLI and skills"
command -v higgsfield >/dev/null || npm i -g @higgsfield/cli
[ -d "$ROOT/.claude/skills/higgsfield-generate" ] || npx -y skills add higgsfield-ai/skills
higgsfield auth status >/dev/null 2>&1 || SKIPPED+=("Higgsfield sign-in: run 'higgsfield auth login', then 'higgsfield workspace list' and 'higgsfield workspace set <id>'")

say "API keys file"
[ -f .env ] || { cp .env.example .env; chmod 600 .env; SKIPPED+=("fill in the keys in .env (ELEVENLABS_API_KEY, HIGGSFIELD_API_KEY, HIGGSFIELD_API_SECRET)"); }

say "check"
pipeline/qcpy -c "import numpy, scipy, cv2, mediapipe, onnxruntime, torch; print('python packages ok')"
echo "Self-test: pipeline/qcpy pipeline/self_test.py   (must end ALL PASS)"
if [ ${#SKIPPED[@]} -gt 0 ]; then printf '\nStill to do:\n'; printf '  - %s\n' "${SKIPPED[@]}"; fi
