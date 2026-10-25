#!/usr/bin/env python3
"""silver01 sounds from ElevenLabs sound generation (key from .env, never printed). Writes work/silver01/sfx/<kind>.wav."""
import json, os, subprocess, sys, tempfile, urllib.request
SK = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(SK))
env = dict(l.strip().split("=", 1) for l in open(f"{ROOT}/.env") if "=" in l and not l.startswith("#"))
KEY = env["ELEVENLABS_API_KEY"].strip().strip('"')
SFX = {
    "bar_slide": ("A heavy solid metal bar sliding slowly across a worn wooden desk, a low scraping drag, close microphone, dry", 1.6),
    "bar_clang": ("A heavy solid silver metal bar falling off a wooden desk and hitting a concrete floor, one loud metallic clang with a short ring, close microphone, dry", 1.4),
}
tmpd = tempfile.mkdtemp()
for kind in sys.argv[1:] or list(SFX):
    text, dur = SFX[kind]
    body = json.dumps({"text": text, "duration_seconds": dur, "prompt_influence": 0.7}).encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128", data=body,
                                 headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    mp3 = f"{tmpd}/{kind}.mp3"; open(mp3, "wb").write(urllib.request.urlopen(req, timeout=120).read())
    out = f"{SK}/sfx/{kind}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-ac", "1", "-ar", "48000", "-t", str(dur),
                    "-af", "loudnorm=I=-20:TP=-3:LRA=7", out], check=True)
    print(kind, os.path.getsize(out), "bytes")
