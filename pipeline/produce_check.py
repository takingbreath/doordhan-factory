#!/usr/bin/env python3
"""Is this machine ready to produce a video? The /produce-video skill runs it first; run it yourself on a new machine.
Checks only local things (no credits, no network except the ElevenLabs key check): tools on PATH, Python packages,
the QC environment and models, the tracked assets the edit and the QC gate read, and the ElevenLabs key (never
printed). The Higgsfield connector is a sign-in, so the skill checks it with a tool call, not here.
Usage: python3 pipeline/produce_check.py [--no-network]     exit 0 when ready, 1 with a fix for each missing piece"""
import argparse, importlib.util, json, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QC_PY = os.path.expanduser("~/.venvs/doordhan-qc/bin/python")
SYNCNET = os.environ.get("SYNCNET_DIR", os.path.expanduser("~/syncnet_python"))
rows = []


def row(ok, what, fix=""):
    rows.append((ok, what, fix))


def py_has(python, mod):
    if python == sys.executable:
        return importlib.util.find_spec(mod) is not None
    r = subprocess.run([python, "-c", f"import {mod}"], capture_output=True)
    return r.returncode == 0


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--no-network", action="store_true")
    a = ap.parse_args()
    for tool in ("ffmpeg", "ffprobe"):
        row(bool(shutil.which(tool)), f"{tool} on PATH", "brew install ffmpeg (Mac) / sudo apt-get install -y ffmpeg")
    row(sys.version_info >= (3, 9), f"python3 {sys.version.split()[0]} (3.9+)", "install Python 3.9 or newer")
    for mod, pkg in (("numpy", "numpy"), ("PIL", "pillow"), ("fontTools", "fonttools")):
        row(py_has(sys.executable, mod), f"python3 package {pkg}", "pip3 install -r requirements.txt")
    qc = os.path.exists(QC_PY)
    row(qc or py_has(sys.executable, "mediapipe"), "QC Python with MediaPipe (~/.venvs/doordhan-qc on a Mac)",
        "bash pipeline/fetch_models.sh  (makes the venv on a Mac; pip installs on Linux)")
    qpy = QC_PY if qc else sys.executable
    for mod in ("mediapipe", "onnxruntime", "torch", "fontTools"):
        row(py_has(qpy, mod), f"QC package {mod} ({os.path.basename(os.path.dirname(os.path.dirname(qpy)))})",
            "bash pipeline/fetch_models.sh")
    for f in ("assets/models/face_landmarker.task", "assets/models/auraface_glintr100.onnx"):
        row(os.path.exists(os.path.join(ROOT, f)), f, "bash pipeline/fetch_models.sh")
    row(os.path.exists(os.path.join(SYNCNET, "data", "syncnet_v2.model")), f"SyncNet model in {SYNCNET}",
        "bash pipeline/fetch_models.sh")
    # collage reels (jio01): filing pages rendered with pdftoppm, photos cut out with rembg (its own venv on a Mac)
    row(bool(shutil.which("pdftoppm")), "pdftoppm on PATH (poppler)", "brew install poppler (Mac) / sudo apt-get install -y poppler-utils")
    cut_py = os.path.expanduser("~/.venvs/doordhan-cut/bin/python")
    cut_py = cut_py if os.path.exists(cut_py) else sys.executable
    isnet = [os.path.expanduser(p) for p in ("~/.rembg/models/isnet-general-use/isnet-general-use.onnx",  # rembg 2.0.8x
                                             "~/.u2net/isnet-general-use.onnx")]                        # older rembg
    row(py_has(cut_py, "rembg") and any(os.path.exists(p) for p in isnet),
        "rembg and its isnet-general-use model (pipeline/cutout.py)", "bash pipeline/fetch_models.sh")
    tracked = ["assets/characters/pandey_sheet_v2.jpg", "assets/characters/billu_sheet.jpg",
               "assets/references/doordhan_look_vertical.jpg", "assets/clips/sahayata_endcard.mp4",
               "assets/edits/sk03_build.py", "assets/edits/sk03_gfx.py", "assets/edits/sk02_mouthbox.py",
               "assets/edits/nana01_build.py", "assets/edits/jio01_build.py", "assets/edits/jio01_vox.py",
               "assets/fonts/TitanOne.ttf", "assets/fonts/Bungee.ttf", "assets/fonts/Baloo2-Latin-ExtraBold.ttf",
               "assets/fonts/Baloo2-Deva-ExtraBold.ttf", "assets/audio/ambience",
               "assets/edits/samachar_gfx.py", "assets/fonts/PermanentMarker-Regular.ttf",
               "assets/fonts/DejaVuSerif-Bold.ttf", "assets/references/vox/plate_paper.jpg",
               "assets/references/vox/plate_chart.jpg", "assets/references/mirror/index.json",
               "pipeline/prices.json", "docs/gallery/graphics_styles.jpg"]
    for f in tracked:
        row(os.path.exists(os.path.join(ROOT, f)), f, "git pull (it is tracked in the repo)")
    hooks = json.load(open(os.path.join(ROOT, ".claude", "settings.json"))).get("hooks", {}).get("PreToolUse", [])
    cmds = " ".join(h.get("command", "") for m in hooks for h in m.get("hooks", []))
    row(all(k in cmds for k in ("spend_guard.py", "never_tools.py", "require_qc_stamp.py")),
        "guard hooks registered (spend guard, never-post, QC stamp) in .claude/settings.json",
        "git pull; restore the hooks in .claude/settings.json")
    sfx = [f"assets/audio/sfx_{k}.wav" for k in ("whoosh", "pop", "ding", "thud", "scratch", "riser", "stamp")]
    row(all(os.path.exists(os.path.join(ROOT, f)) for f in sfx), "sound-effect kit assets/audio/sfx_*.wav",
        "python3 pipeline/sfx.py")
    env_key = bool(os.environ.get("ELEVENLABS_API_KEY")) or (
        os.path.exists(os.path.join(ROOT, ".env")) and "ELEVENLABS_API_KEY=" in open(os.path.join(ROOT, ".env")).read())
    row(env_key, "ElevenLabs key in the environment or the git-ignored .env (value never printed)",
        "ask Akhilesh for your own named key (SETUP.md, Adding a teammate); put ELEVENLABS_API_KEY=... in .env")
    if env_key and not a.no_network:
        r = subprocess.run([sys.executable, os.path.join(ROOT, "pipeline", "tts_elevenlabs.py"), "--check"],
                           capture_output=True, text=True)
        row(r.returncode == 0, "ElevenLabs key accepted, eleven_v3 offered (tts_elevenlabs.py --check)",
            (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else "check the key")
    width = max(len(w) for _, w, _ in rows)
    for ok, what, fix in rows:
        print(f"  {'ok  ' if ok else 'MISS'}  {what:<{width}}" + ("" if ok else f"   -> {fix}"))
    missing = [r for r in rows if not r[0]]
    print(f"\n{'READY' if not missing else f'{len(missing)} missing'}: local checks only. The skill also checks the "
          "Higgsfield connector (balance) and that the registry's reference IDs resolve from this workspace.")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
