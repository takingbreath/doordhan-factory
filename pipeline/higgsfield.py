#!/usr/bin/env python3
"""Higgsfield generation over the REST API (no MCP). Key from HIGGSFIELD_API_KEY[/_SECRET] or .env.

  higgsfield.py --check                    is the key valid + is the API reachable? (spends nothing)
  higgsfield.py cost   --json '<payload>'  preflight a job's credit cost (get_cost:true, free)
  higgsfield.py audio  --voice sarika --text-file line.txt --out raw.mp3   text2speech_v2
  higgsfield.py image  --model gpt_image_2_5 --prompt-file p.txt --refs A,B --out kf.png
  higgsfield.py video  --model wan2_7 --start-image ID --audio-ref MEDIA --prompt-file p.txt --out shot.mp4

Async models (image/video) submit a job, then poll to completion and download the result.
Everything reads the same registry as the MCP path, so IDs match. Never prints the key.

If --check fails with 401/404, the REST base/auth differ from the documented default: set
HIGGSFIELD_API_BASE and/or HIGGSFIELD_AUTH_SCHEME (bearer|hmac|basic) from the Higgsfield API docs.
The request *shapes* here match the MCP tool payloads; only the transport (base/auth/paths) is
environment config, so a wrong host is a 1-line env fix, not a code rewrite."""
import argparse, json, os, sys, urllib.request
from higgsfield_api import request, error_text, voice_from_registry, poll, registry, MODELS, API, AUTH_SCHEME

# Candidate probe paths for --check (first that returns <400 wins). Confirmed/pruned on first real run.
CHECK_PATHS = ["/v1/health", "/health", "/v1/account", "/v1/me", "/v1/models", "/api/v1/health"]


def _download(url, out):
    with urllib.request.urlopen(url, timeout=300) as r, open(out, "wb") as f:
        f.write(r.read())


def cmd_check():
    print(f"base={API}  auth={AUTH_SCHEME}")
    for p in CHECK_PATHS:
        st, body = request(p, method="GET")
        mark = "OK" if 200 <= st < 400 else ("AUTH?" if st in (401, 403) else "")
        print(f"  GET {p} -> {st} {mark}")
        if 200 <= st < 400:
            print(f"key reachable at {p}. Auth scheme '{AUTH_SCHEME}' accepted.")
            return
        if st in (401, 403):
            sys.exit(f"reached {p} but auth was rejected ({st}). Try a different HIGGSFIELD_AUTH_SCHEME "
                     f"(bearer|hmac|basic), or check the key/secret. {error_text(st, body)}")
    sys.exit("No probe path returned <400. Set HIGGSFIELD_API_BASE to the real API host from the "
             "Higgsfield dashboard's API docs, then re-run --check.")


def cmd_cost(a):
    payload = json.loads(a.json)
    payload["get_cost"] = True
    st, body = request(a.path or "/v1/generate", payload)
    print(body.decode() if st < 400 else error_text(st, body))


def cmd_audio(a):
    v = voice_from_registry(a.voice) if a.voice else None
    text = a.text or open(a.text_file, encoding="utf-8").read().strip()
    payload = {
        "model": MODELS["tts"], "variant": "elevenlabs", "voice_type": "element",
        "voice_id": a.voice_id or v["voice_id"], "text": text,
    }
    if a.cost:
        payload["get_cost"] = True
    st, body = request(a.path or "/v1/generate/audio", payload)
    if st >= 400:
        sys.exit(error_text(st, body))
    job = json.loads(body)
    url = job.get("result") or job.get("output") or (job.get("audio_url"))
    if not url and (job.get("id") or job.get("job_id")):
        job = poll((a.status_path or "/v1/jobs/") + str(job.get("id") or job.get("job_id")))
        url = job.get("result") or job.get("output")
    if a.out and url:
        _download(url, a.out); print(f"wrote {a.out}")
    else:
        print(json.dumps(job, ensure_ascii=False)[:500])


def cmd_image(a):
    refs = [r for r in (a.refs or "").split(",") if r]
    payload = {"model": a.model or MODELS["keyframe"],
               "prompt": a.prompt or open(a.prompt_file, encoding="utf-8").read().strip(),
               "reference_images": refs}
    if a.cost:
        payload["get_cost"] = True
    _submit_and_fetch(a, payload, a.path or "/v1/generate/image")


def cmd_video(a):
    payload = {"model": a.model or MODELS["talking"], "quality": a.quality,
               "prompt": a.prompt or open(a.prompt_file, encoding="utf-8").read().strip(),
               "start_image": a.start_image}
    if a.audio_ref:
        payload["audio_references"] = [a.audio_ref]
    dp = registry().get("style", {}).get("declined_preset_id")
    if dp:
        payload["declined_preset_id"] = dp   # avoid the preset that keeps re-firing (2026-09-25)
    if a.cost:
        payload["get_cost"] = True
    _submit_and_fetch(a, payload, a.path or "/v1/generate/video")


def _submit_and_fetch(a, payload, path):
    st, body = request(path, payload)
    if st >= 400:
        sys.exit(error_text(st, body))
    job = json.loads(body)
    if payload.get("get_cost"):
        print(body.decode()); return
    jid = job.get("id") or job.get("job_id")
    url = job.get("result") or job.get("output")
    if not url and jid:
        job = poll((a.status_path or "/v1/jobs/") + str(jid))
        url = job.get("result") or job.get("output")
    if a.out and url:
        _download(url, a.out); print(f"wrote {a.out}")
    else:
        print(json.dumps(job, ensure_ascii=False)[:500])


p = argparse.ArgumentParser()
sub = p.add_subparsers(dest="cmd", required=True)
sub.add_parser("check")
c = sub.add_parser("cost"); c.add_argument("--json", required=True); c.add_argument("--path")
au = sub.add_parser("audio")
au.add_argument("--voice"); au.add_argument("--voice-id"); au.add_argument("--text"); au.add_argument("--text-file")
au.add_argument("--out"); au.add_argument("--cost", action="store_true"); au.add_argument("--path"); au.add_argument("--status-path")
im = sub.add_parser("image")
im.add_argument("--model"); im.add_argument("--prompt"); im.add_argument("--prompt-file"); im.add_argument("--refs")
im.add_argument("--out"); im.add_argument("--cost", action="store_true"); im.add_argument("--path"); im.add_argument("--status-path")
vi = sub.add_parser("video")
vi.add_argument("--model"); vi.add_argument("--quality", default="720p"); vi.add_argument("--prompt"); vi.add_argument("--prompt-file")
vi.add_argument("--start-image", required=True); vi.add_argument("--audio-ref")
vi.add_argument("--out"); vi.add_argument("--cost", action="store_true"); vi.add_argument("--path"); vi.add_argument("--status-path")
a = p.parse_args()
{"check": lambda: cmd_check(), "cost": lambda: cmd_cost(a), "audio": lambda: cmd_audio(a),
 "image": lambda: cmd_image(a), "video": lambda: cmd_video(a)}[a.cmd]()
