#!/usr/bin/env python3
"""What was actually said, and when: ElevenLabs Scribe on a clip or line. Catches gibberish and re-voiced lines
that the envelope checks can miss, and gives word end times for cut points ("never cut before the last word").
Usage: transcribe.py CLIP.mp4 [--expect "script line" | --expect-file line.txt] [--language hi] [--json OUT.json]
Similarity compares the transcript with the script after stripping punctuation; English words may come back in
Devanagari or Latin, so treat 60-80% as "read the transcript", not as a failure. Below 60% = likely gibberish."""
import argparse, difflib, json, os, re, subprocess, sys, tempfile, uuid
from common import FFMPEG
from elevenlabs_api import STT_MODEL, request, error_text

p = argparse.ArgumentParser()
p.add_argument("clip"); p.add_argument("--expect"); p.add_argument("--expect-file")
p.add_argument("--language", default="hi"); p.add_argument("--json")
a = p.parse_args()

mp3 = os.path.join(tempfile.mkdtemp(), "a.mp3")
subprocess.run([FFMPEG, "-y", "-v", "error", "-i", a.clip, "-vn", "-ac", "1", "-ar", "16000", "-b:a", "64k", mp3],
               check=True)
boundary = uuid.uuid4().hex
fields = {"model_id": STT_MODEL, "language_code": a.language, "timestamps_granularity": "word",
          "tag_audio_events": "false"}
body = b"".join(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
                for k, v in fields.items())
body += (f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="a.mp3"\r\n'
         f"Content-Type: audio/mpeg\r\n\r\n").encode() + open(mp3, "rb").read() + f"\r\n--{boundary}--\r\n".encode()
st, raw = request("/v1/speech-to-text", data=body, method="POST",
                  headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
if st != 200:
    sys.exit(error_text(st, raw))
r = json.loads(raw)
words = [w for w in r.get("words", []) if w.get("type") == "word"]
print(f"transcript ({r.get('language_code')}): {r.get('text', '').strip()}")
if words:
    print(f"first word starts {words[0].get('start', 0):.2f}s, last word '{words[-1]['text']}' ends "
          f"{words[-1].get('end', 0):.2f}s  (cut after this)")
expect = a.expect or (open(a.expect_file, encoding="utf-8").read() if a.expect_file else None)
if expect:
    norm = lambda s: re.sub(r"[\W_]+", "", re.sub(r"\[[^\]]*\]", "", s.lower()))   # drops [delivery tags]
    sim = difflib.SequenceMatcher(None, norm(expect), norm(r.get("text", ""))).ratio() * 100
    verdict = "PASS" if sim >= 80 else ("READ" if sim >= 60 else "FAIL")
    print(f"{verdict}  similarity to script {sim:.0f}%")
if a.json:
    json.dump(r, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
