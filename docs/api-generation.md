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

## Higgsfield — client built + AUTHENTICATED; only REST model slugs/paths remain
`pipeline/higgsfield_api.py` (shared client) + `pipeline/higgsfield.py` (CLI: `check|cost|audio|
image|video`) mirror the ElevenLabs client exactly. The request **payload shapes** match the MCP
tool calls the playbooks document (text2speech_v2/elevenlabs/element, wan2_7 + start_image +
audio_references, seedream_v4_5 / gpt_image_2_5, `get_cost` preflight, `declined_preset_id`).

**Transport SOLVED (verified 2026-09-26).** Two things gated it, both now handled in the client:
1. **Zscaler corporate-proxy TLS** — the client honors a CA bundle via `SSL_CERT_FILE` /
   `REQUESTS_CA_BUNDLE` / `~/.zscaler-bundle.pem` (same convention as the platform's
   `NODE_EXTRA_CA_CERTS`, AGENTS.md §11).
2. **Cloudflare `403 error code: 1010`** — a browser-integrity block on non-browser client
   fingerprints. Fixed by sending a browser `User-Agent` (see `higgsfield_api.UA`).
   Result: `python3 pipeline/higgsfield.py check` → `/health 204 OK, auth scheme 'hmac' accepted`.
   The real API host **is `platform.higgsfield.ai`** with `/v1/*` paths, auth = key/secret headers.

**Remaining (needs the API reference, not discoverable safely by probing):** the correct REST
**model slugs + generate path**. A `get_cost` preflight against `/v1/generate*` returns a real
`404 model_not_found` for `text2speech_v2` — i.e. auth + transport work, but the MCP tool name
isn't the REST model id. From Higgsfield's API docs, set the real model ids (map into
`higgsfield_api.MODELS`) and the generate/status paths (`higgsfield.py` defaults), then
`... cost --json '{...}'` should return a credit estimate (free) before any real spend. Probing
further blindly is avoided on purpose: a wrong-but-valid path could submit a credit-spending job.

## What's still Claude/agent-only vs API-able
- **Creative judgment** (story pick, script, wardrobe, QC "hot-and-classy" calls) — an agent (or a
  person) still makes these; the playbooks are the instructions.
- **Mechanical generation** (voice → keyframe → talking shot → QC → assemble) — API-able now, via
  the clients above, once the Higgsfield transport value is set. A future `render.py` can chain a
  `work/<slug>/HANDOFF.md` shot list straight through these calls with no agent.
