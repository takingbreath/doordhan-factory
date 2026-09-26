# API-based generation (no MCP)

The pipeline can drive Higgsfield + ElevenLabs over plain HTTPS with API keys, so a standalone
renderer / a workflow-platform node / a cron job can produce a reel without an agent or MCP.

## Setup
Put keys in a git-ignored `.env` at the repo root (see `.env.example`):
```
ELEVENLABS_API_KEY=sk_...
HIGGSFIELD_API_KEY=<uuid>
HIGGSFIELD_API_SECRET=<hex>       # the second half of the dashboard's key:secret pair
# HIGGSFIELD_API_BASE=...         # see "Higgsfield transport" below
# HIGGSFIELD_AUTH_SCHEME=hmac     # bearer | hmac | basic
```

## ElevenLabs — WORKING (verified live)
`python3 pipeline/tts_elevenlabs.py --check` → `key OK (GET /v1/models 200)`, eleven_v3 + Hindi
available. Voice generation via `--voice sarika --text-file line.txt --out raw.mp3`. Client:
`pipeline/elevenlabs_api.py`.

## Higgsfield — client VERIFIED WORKING against the real API
`pipeline/higgsfield_api.py` + `pipeline/higgsfield.py`. Verified live against the documented API
(docs.higgsfield.ai, 2026-09-26):
- **Base URL `https://api.higgsfield.ai`**; endpoints are path-based `/{provider}/{model}/.../{task}`
  (e.g. `/minimax/hailuo-2.3/standard/text-to-video`, `/kling-video/v2.5-turbo/pro/text-to-video`).
- **Auth `Authorization: Key <KEY_ID>:<KEY_SECRET>`** (legacy `hf-api-key`/`hf-secret` also accepted).
- **Async lifecycle:** POST model endpoint -> `{request_id, status_url}` -> poll
  `GET /requests/{request_id}/status` -> download output when `completed`.
- **Transport:** Zscaler CA bundle (`~/.zscaler-bundle.pem` via SSL context) + browser User-Agent
  to clear Cloudflare 1010.
- **PROOF it works:** `higgsfield.py check` -> `/health 204, key auth accepted`; a POST to a real
  model endpoint with an empty body returns `400 "'prompt' is a required property"` — i.e. base,
  auth, path, and body-validation are all correct. A valid `{prompt: ...}` POST creates a real
  request (spends the account's prepaid USD balance).

**Remaining for the Doordhan E4 reel specifically:** the exact model slugs the engine uses
(`wan2_7` talking-head lip-sync from start_image+audio; the text-to-speech model) are not in the
public OpenAPI sample (which is explicitly non-authoritative) — they live in per-model docs on
console.higgsfield.ai (login-gated). Get the endpoint path + schema for the talking-head + TTS
models from the console, map them into `higgsfield.py`'s image/video/audio subcommands, then run
`work/e4-tax-audit-deadline/HANDOFF.md`. Documented models (hailuo/seedance text-to-video, kling)
are runnable via `higgsfield.py video --path /minimax/hailuo-2.3/standard/text-to-video` today.

## What's still Claude/agent-only vs API-able
- **Creative judgment** (story pick, script, wardrobe, QC "hot-and-classy" calls) — an agent (or a
  person) still makes these; the playbooks are the instructions.
- **Mechanical generation** (voice → keyframe → talking shot → QC → assemble) — API-able now, via
  the clients above, once the Higgsfield transport value is set. A future `render.py` can chain a
  `work/<slug>/HANDOFF.md` shot list straight through these calls with no agent.
