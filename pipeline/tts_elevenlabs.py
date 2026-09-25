#!/usr/bin/env python3
"""ElevenLabs text-to-speech. The key comes from ELEVENLABS_API_KEY or the repo's .env; it is never printed.
  tts_elevenlabs.py --check                       (is the key valid? plan quota, and is the default model current?)
  tts_elevenlabs.py --list                        (voices on the account: name, id, category)
  tts_elevenlabs.py --voice sarika --text "..." --out raw.mp3      (voice looked up in registry/assets.json)
  tts_elevenlabs.py --voice-id ID --text-file line.txt --out raw.mp3 [--model eleven_v3] [--language hi]
                    [--seed 7] [--stability 0.5]
eleven_v3 supports inline delivery tags like [dryly] [warm] [chuckles]; it has no request stitching
(previous_text/next_text) and its stability takes 0.0 (creative), 0.5 (natural) or 1.0 (robust)."""
import argparse, json, os, sys
from elevenlabs_api import TTS_MODEL, request, error_text, voice_from_registry

p = argparse.ArgumentParser()
p.add_argument("--check", action="store_true"); p.add_argument("--list", action="store_true")
p.add_argument("--voice", help="registry voice name, e.g. sarika"); p.add_argument("--voice-id")
p.add_argument("--text"); p.add_argument("--text-file"); p.add_argument("--out")
p.add_argument("--model", default=TTS_MODEL)
p.add_argument("--language", help="ISO 639-1, e.g. hi (ignored by models that don't support it)")
p.add_argument("--seed", type=int); p.add_argument("--stability", type=float)
a = p.parse_args()

if a.check:
    st, body = request("/v1/models")
    if st != 200:
        sys.exit(error_text(st, body))
    models = json.loads(body)
    tts = [m for m in models if m.get("can_do_text_to_speech")]
    print("key OK (GET /v1/models 200)")
    print("TTS models:", ", ".join(m["model_id"] for m in tts))
    cur = next((m for m in tts if m["model_id"] == a.model), None)
    if not cur:
        sys.exit(f"default model '{a.model}' is NOT offered any more; pick one above and update elevenlabs_api.py")
    langs = {l.get("language_id") for l in cur.get("languages", [])}
    print(f"default model {a.model}: available, Hindi {'yes' if langs & {'hi', 'hin'} else 'not listed'}")
    st, body = request("/v1/user/subscription")
    if st == 200:
        s = json.loads(body)
        print(f"plan {s.get('tier')}, {s.get('character_count')}/{s.get('character_limit')} characters used "
              f"this period, status {s.get('status')}")
    else:
        print(f"(subscription not readable: {error_text(st, body)}; a key scoped to TTS can still generate)")
    sys.exit()

if a.list:
    st, body = request("/v1/voices")
    if st != 200:
        sys.exit(error_text(st, body))
    for v in json.loads(body).get("voices", []):
        print(f"{v.get('name')}\t{v.get('voice_id')}\t{v.get('category')}")
    sys.exit()

voice_id = a.voice_id or (voice_from_registry(a.voice) if a.voice else None)
if not voice_id or not a.out or not (a.text or a.text_file):
    p.error("need --voice or --voice-id, --text or --text-file, and --out")
text = a.text or open(a.text_file, encoding="utf-8").read().strip()
payload = {"text": text, "model_id": a.model}
if a.language: payload["language_code"] = a.language
if a.seed is not None: payload["seed"] = a.seed
if a.stability is not None: payload["voice_settings"] = {"stability": a.stability}
st, audio = request(f"/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128",
                    data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
if st != 200:
    sys.exit(error_text(st, audio))
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
open(a.out, "wb").write(audio)
print(f"{a.out}: {len(audio)} bytes ({a.model})")
