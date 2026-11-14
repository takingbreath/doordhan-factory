#!/usr/bin/env python3
"""Vox-style desk sounds from ElevenLabs sound generation (23 Oct 2026: the old synthesized set did not match the paper-collage look).
Writes assets/audio/sfx_<kind>.wav (44.1 kHz mono, peak about -3 dB). Key from .env, never printed. Cost: a few hundred credits in all."""
import json, os, subprocess, sys, urllib.request
ROOT = os.path.abspath(os.path.dirname(__file__))
while ROOT != "/" and not os.path.exists(os.path.join(ROOT, "CLAUDE.md")): ROOT = os.path.dirname(ROOT)
env = dict(l.strip().split("=", 1) for l in open(f"{ROOT}/.env") if "=" in l and not l.startswith("#")); KEY = env["ELEVENLABS_API_KEY"].strip().strip('"')
SFX = {
    "scribble": ("A black felt-tip marker quickly scribbling a loose circle on paper, close microphone, dry, no music", 0.8),
    "marker": ("A yellow highlighter marker swiping once across paper, close microphone, dry", 0.6),
    "tape": ("A strip of masking tape being pulled off a roll and pressed onto paper, short, close microphone", 0.7),
    "slap": ("A printed photograph dropped flat onto a wooden desk, a soft paper slap, close microphone", 0.5),
    "slide": ("A sheet of paper sliding fast across a wooden desk, short soft swish, close microphone", 0.5),
    "stamp2": ("A rubber hand stamp pressed hard onto a paper pad, one solid dry thump, close microphone", 0.5),
    "type": ("One soft mechanical keyboard key press, single click, close microphone, dry", 0.5),
    "click": ("One computer mouse button click, crisp, dry", 0.5),
    "chime": ("A very short soft success chime, two gentle notes, clean", 0.9),
    "tear": ("A piece of paper being torn sharply in two, close microphone", 0.7),
    "coin": ("One metal coin dropped onto a wooden table, a short clink, close microphone", 0.6),
}
only = sys.argv[1:] or list(SFX)
for kind in only:
    text, dur = SFX[kind]
    body = json.dumps({"text": text, "duration_seconds": dur, "prompt_influence": 0.6}).encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128", data=body, headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    mp3 = f"/tmp/sfx_{kind}.mp3"; open(mp3, "wb").write(urllib.request.urlopen(req, timeout=120).read())
    out = f"{ROOT}/assets/audio/sfx_{kind}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-ac", "1", "-ar", "44100", "-t", str({"type": 0.35, "click": 0.25}.get(kind, dur)), "-af", "loudnorm=I=-22:TP=-3:LRA=7,afade=t=out:st=%s:d=0.08" % max(0.1, round(dur - 0.1, 2)), out], check=True)
    print(kind, os.path.getsize(out), "bytes")
