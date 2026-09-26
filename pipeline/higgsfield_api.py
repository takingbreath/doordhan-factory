"""Shared Higgsfield REST helpers — the API-based sibling of the MCP connector.

Keys come from HIGGSFIELD_API_KEY + HIGGSFIELD_API_SECRET (a `key:secret` pair, as issued in the
Higgsfield dashboard), or from a git-ignored .env at the repo root. Nothing here ever prints, logs
or writes the key. Mirrors pipeline/elevenlabs_api.py's shape exactly (key(), request(),
error_text(), registry lookups) so the two clients read the same.

WHY THIS EXISTS
The pipeline used to reach Higgsfield only through the MCP connector inside a Claude session. This
module lets any process (a standalone renderer, a workflow-platform node, a cron job) drive the
same image/video/voice generation over plain HTTPS with the API key — no agent, no MCP.

⚠️ ENDPOINT/AUTH ARE CONFIG, NOT HARDCODED FACTS.
The MCP tool *names and payload fields* (generate_audio/text2speech_v2, wan2_7, seedance_2_5,
seedream_v4_5, gpt_image_2_5, start_image, audio_references, get_cost, media_upload/confirm) are
known from the repo's own playbooks/registry and are encoded below. The exact REST base URL, path
layout and auth header are NOT documented in this repo, so they are read from env with a documented
default and MUST be confirmed once against Higgsfield's real API reference. `--check` verifies
reachability + auth before any credit is spent; if it 404s/401s, set HIGGSFIELD_API_BASE /
HIGGSFIELD_AUTH_SCHEME to match the dashboard's API docs rather than guessing in code.
"""
import json, os, ssl, sys, time, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Verified against docs.higgsfield.ai (2026-09-26): the REST API host is api.higgsfield.ai, and
# model endpoints are path-based (/{provider}/{model}/.../{task}, e.g.
# /minimax/hailuo-2.3/standard/text-to-video). Overridable for preview environments.
API = os.environ.get("HIGGSFIELD_API_BASE", "https://api.higgsfield.ai").rstrip("/")
# Documented auth: `Authorization: Key <KEY_ID>:<KEY_SECRET>` (preferred). The legacy
# hf-api-key/hf-secret headers are also still accepted. Default to the documented header.
AUTH_SCHEME = os.environ.get("HIGGSFIELD_AUTH_SCHEME", "key")
# Cloudflare in front of the API rejects non-browser client fingerprints with `403 error code:
# 1010` unless a browser User-Agent is sent (confirmed 2026-09-26: with this UA /v1/health returns
# a real API 405, without it a CF 1010). Overridable if it ever needs refreshing.
UA = os.environ.get("HIGGSFIELD_UA", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0 Safari/537.36")


def _ssl_ctx():
    """Honor a corporate CA bundle (Zscaler MITM proxy) via SSL_CERT_FILE / REQUESTS_CA_BUNDLE /
    ~/.zscaler-bundle.pem, matching the platform's NODE_EXTRA_CA_CERTS convention (AGENTS.md §11)."""
    for cand in (os.environ.get("SSL_CERT_FILE"), os.environ.get("REQUESTS_CA_BUNDLE"),
                 os.path.expanduser("~/.zscaler-bundle.pem")):
        if cand and os.path.exists(cand):
            return ssl.create_default_context(cafile=cand)
    return None

# Model ids as used in the registry/playbooks (single source of truth for callers).
MODELS = {
    "tts": "text2speech_v2",       # variant elevenlabs, voice_type element
    "talking": "wan2_7",           # 720p talking shots from start_image + audio_references
    "bframe": "seedance_2_5",      # non-talking motion, 480p
    "wardrobe": "seedream_v4_5",   # Sarika wardrobe keyframes
    "keyframe": "gpt_image_2_5",   # general keyframes
}


def _env(name):
    v = os.environ.get(name, "").strip()
    if v:
        return v
    envf = os.path.join(ROOT, ".env")
    if os.path.exists(envf):
        for line in open(envf, encoding="utf-8"):
            k, _, val = line.strip().partition("=")
            if k.strip().replace("export ", "") == name:
                return val.strip().strip('"').strip("'")
    return ""


def creds():
    """(key, secret). Exits with a clear message if unset. Never printed."""
    k, s = _env("HIGGSFIELD_API_KEY"), _env("HIGGSFIELD_API_SECRET")
    if not k:
        sys.exit("HIGGSFIELD_API_KEY is not set (export it, or add it to the repo's .env — see .env.example)")
    return k, s


def _auth_headers():
    k, s = creds()
    if AUTH_SCHEME == "key":
        # Documented preferred scheme: `Authorization: Key <KEY_ID>:<KEY_SECRET>`.
        return {"Authorization": f"Key {k}:{s}"}
    if AUTH_SCHEME == "bearer":
        return {"Authorization": f"Bearer {k}"}
    if AUTH_SCHEME == "basic":
        import base64
        tok = base64.b64encode(f"{k}:{s}".encode()).decode()
        return {"Authorization": f"Basic {tok}"}
    # legacy hmac-style: key + secret as separate headers (still accepted by the API)
    return {"hf-api-key": k, **({"hf-secret": s} if s else {})}


def request(path, data=None, headers=None, method=None, timeout=180):
    """Returns (status, body bytes). HTTP errors come back as (code, body), never raise —
    same contract as elevenlabs_api.request()."""
    body = json.dumps(data).encode() if isinstance(data, (dict, list)) else data
    req = urllib.request.Request(
        API + path, data=body, method=method or ("POST" if body else "GET"),
        headers={"content-type": "application/json", "user-agent": UA, "accept": "application/json",
                 **_auth_headers(), **(headers or {})},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_ssl_ctx()) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except urllib.error.URLError as e:
        return 0, str(e.reason).encode()


def error_text(status, body):
    try:
        d = json.loads(body)
        d = d.get("detail") or d.get("message") or d.get("error") or body
        if isinstance(d, dict):
            d = f"{d.get('code', '')}: {d.get('message', '')}"
    except Exception:
        d = body[:300] if isinstance(body, (bytes, bytearray)) else str(body)[:300]
    return f"Higgsfield error {status}: {d}"


def registry():
    return json.load(open(os.path.join(ROOT, "registry", "assets.json"), encoding="utf-8"))


def voice_from_registry(name):
    v = registry().get("voices", {}).get(name)
    if not v:
        sys.exit(f"no voice '{name}' in registry/assets.json")
    if v.get("provider") != "higgsfield" or not v.get("voice_id"):
        sys.exit(f"registry voice '{name}' is not a Higgsfield voice element (provider={v.get('provider')})")
    return v


def poll(status_path, ok=("completed", "succeeded", "done"),
         fail=("failed", "error", "cancelled"), every=4, timeout=600):
    """Poll an async request to a terminal state. Returns the final request JSON.
    Higgsfield's documented lifecycle: submit -> {request_id, status_url} -> poll
    GET /requests/{request_id}/status -> download output when `completed`."""
    start = time.time()
    while time.time() - start < timeout:
        st, body = request(status_path, method="GET")
        if st != 200:
            return {"_http": st, "_error": error_text(st, body)}
        job = json.loads(body)
        state = str(job.get("status") or job.get("state") or "").lower()
        if state in ok or job.get("result") or job.get("output"):
            return job
        if state in fail:
            return job
        time.sleep(every)
    return {"_timeout": True, "status_path": status_path}
