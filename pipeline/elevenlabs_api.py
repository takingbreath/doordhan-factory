"""Shared ElevenLabs helpers. The key comes from ELEVENLABS_API_KEY, or from a git-ignored .env at the repo root.
Nothing here ever prints, logs or writes the key."""
import json, os, sys, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.elevenlabs.io"
TTS_MODEL = "eleven_v3"      # GA since Feb 2026; still the flagship with Hindi + audio tags (checked 2026-09-25)
STT_MODEL = "scribe_v2"      # scribe_v1 was removed on 2026-07-09


def key():
    k = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    env = os.path.join(ROOT, ".env")
    if not k and os.path.exists(env):
        for line in open(env, encoding="utf-8"):
            name, _, value = line.strip().partition("=")
            if name.strip() in ("ELEVENLABS_API_KEY", "export ELEVENLABS_API_KEY"):
                k = value.strip().strip('"').strip("'")
    if not k:
        sys.exit("ELEVENLABS_API_KEY is not set (export it, or put ELEVENLABS_API_KEY=... in the repo's .env)")
    return k


def request(path, data=None, headers=None, method=None, timeout=120):
    """Returns (status, body bytes). HTTP errors come back as (code, body) instead of raising."""
    req = urllib.request.Request(API + path, data=data, method=method,
                                 headers={"xi-api-key": key(), **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def error_text(status, body):
    try:
        d = json.loads(body).get("detail", body)
        if isinstance(d, dict):
            d = f"{d.get('code') or d.get('status', '')}: {d.get('message', '')}"
    except Exception:
        d = body[:300]
    return f"ElevenLabs error {status}: {d}"


def voice_from_registry(name):
    reg = json.load(open(os.path.join(ROOT, "registry", "assets.json"), encoding="utf-8"))
    v = reg.get("voices", {}).get(name)
    if not v:
        sys.exit(f"no voice '{name}' in registry/assets.json")
    if not v.get("elevenlabs_voice_id"):
        sys.exit(f"registry voice '{name}' has no elevenlabs_voice_id (it lives on {v.get('provider')}); "
                 "use --voice-id, or add the ElevenLabs id to the registry")
    return v["elevenlabs_voice_id"]
