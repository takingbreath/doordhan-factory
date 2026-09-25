#!/usr/bin/env python3
"""ElevenLabs text-to-speech. Reads the key from the ELEVENLABS_API_KEY environment variable (never hard-code it).
  tts_elevenlabs.py --list                                   (voices on the account: name, id, category)
  tts_elevenlabs.py --voice-id ID --text "..." --out raw.mp3 [--model eleven_v3]
v3 supports inline delivery tags like [dryly] [warm] [chuckles]. Verify the model id on the first run."""
import argparse, json, os, sys, urllib.request, urllib.error

p = argparse.ArgumentParser()
p.add_argument("--list", action="store_true")
p.add_argument("--voice-id"); p.add_argument("--text"); p.add_argument("--text-file"); p.add_argument("--out")
p.add_argument("--model", default="eleven_v3")
a = p.parse_args()
key = os.environ.get("ELEVENLABS_API_KEY")
if not key:
    sys.exit("ELEVENLABS_API_KEY is not set")
H = {"xi-api-key": key}


def call(req):
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"ElevenLabs error {e.code}: {e.read().decode()[:500]}")


if a.list:
    data = json.loads(call(urllib.request.Request("https://api.elevenlabs.io/v1/voices", headers=H)))
    for v in data.get("voices", []):
        print(f"{v.get('name')}\t{v.get('voice_id')}\t{v.get('category')}")
    sys.exit()
text = a.text or open(a.text_file, encoding="utf-8").read()
body = json.dumps({"text": text, "model_id": a.model}).encode()
req = urllib.request.Request(
    f"https://api.elevenlabs.io/v1/text-to-speech/{a.voice_id}?output_format=mp3_44100_128",
    data=body, headers={**H, "Content-Type": "application/json"}, method="POST")
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
audio = call(req)
open(a.out, "wb").write(audio)
print(f"{a.out}: {len(audio)} bytes")
