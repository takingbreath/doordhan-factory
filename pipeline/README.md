# Pipeline tools

Requirements: ffmpeg and ffprobe on PATH, Python 3.9+, numpy, pillow. Run tools from the repo root, e.g. `python3 pipeline/prep_line.py ...`.
Check the toolchain (no credits): `python3 pipeline/self_test.py` → must end with ALL PASS.

| Tool | Use |
|---|---|
| tts_elevenlabs.py | Generate a line with an ElevenLabs voice (key from ELEVENLABS_API_KEY). `--list` shows voices. |
| prep_line.py | Clean a raw line: trim, tighten pauses, -16 LUFS, tempo (1.15 anchors), `--phone` for callers. |
| make_track.py | Pad prepared lines into a whole-second track for one shot (upload this to Higgsfield). |
| put_upload.py | PUT a file to the presigned URL returned by Higgsfield media_upload (then call media_confirm). |
| speech_map.py | Speech start/end/pauses of any file. Use on generated clips to choose cut points. |
| check_match.py | Did the generated clip keep our audio? ≥95% = PASS (Wan). Low = re-voiced. |
| lipcheck.py | Mouth-motion ratio speaking vs silent. `--face-crop` saves a frame to locate the mouth box. |
| contact_sheet.py | Frames at an fps or at given times, tiled into one image. |
| inset_card.py | `card`: logo card for the anchor's inset box. `overlay`: put it on a clip (auto-detects the box). |
| montage.py | Title card + the last N seconds of the sting (ending kept intact). |
| assemble.py | Edit list → final reel with 90s finish, 1080x1920, -14 LUFS, plus a joins contact sheet. |
