#!/usr/bin/env python3
"""Role -> model resolver. Code asks for a job, not a model id, so a retired or renamed model is a one-line change in
pipeline/models.json instead of a hunt through the scripts and docs.

  from models import resolve
  resolve("talking_shot")                  # 'wan2_7'
  resolve("tts_clone", detail=True)        # the whole candidate (model, provider, shape, why, skipped)

CLI:
  models.py show                 every role and its candidates, with price and usability
  models.py resolve ROLE         what a role resolves to now, and what was skipped and why
  models.py check                exit 1 if a role has no usable candidate, or a script names a model id the registry
                                 doesn't know (drift)

A candidate is usable when its status is 'active', it is not in MODEL_UNAVAILABLE, and it is priced in
pipeline/prices.json (or billing is 'free'). A skipped first choice is reported on stderr, so a silent downgrade
(wan3_0 -> wan2_7) never goes unnoticed. This module never spends credits and never calls a vendor; the spend guard
still prices every call from prices.json and still blocks an unknown model."""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REGISTRY = os.path.join(HERE, "models.json")
PRICES = os.path.join(HERE, "prices.json")


def _load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def roles():
    return _load(REGISTRY).get("roles", {})


def priced(model, prices=None):
    p = (prices if prices is not None else _load(PRICES)).get(model)
    return isinstance(p, dict) and any(k in p for k in ("per_image", "per_second", "per_call"))


def _unavailable():
    return {m.strip() for m in os.environ.get("MODEL_UNAVAILABLE", "").split(",") if m.strip()}


def _usable(c, prices, gone):
    if c.get("status", "active") != "active":
        return f"status is {c.get('status')}"
    if c["model"] in gone:
        return "listed in MODEL_UNAVAILABLE"
    if c.get("billing") != "free" and not priced(c["model"], prices):
        return "no price in pipeline/prices.json (spend guard would block it)"
    return None


def resolve(role, shape=None, detail=False):
    """First usable candidate for a role (optionally of one request shape). Exits with the reasons if none."""
    spec = roles().get(role)
    if not spec:
        sys.exit(f"models: no role {role!r} in pipeline/models.json (roles: {', '.join(sorted(roles()))})")
    forced = os.environ.get("MODEL_" + role.upper(), "").strip()
    prices, gone, skipped = _load(PRICES), _unavailable(), []
    cands = list(spec["candidates"])
    if forced:
        cands = [c for c in cands if c["model"] == forced] or [{"model": forced, "provider": "override"}]
    for c in cands:
        if shape and c.get("shape") not in (None, shape):
            skipped.append((c["model"], f"shape {c.get('shape')} is not {shape}"))
            continue
        why = _usable(c, prices, gone)
        if why:
            skipped.append((c["model"], why))
            continue
        if skipped:
            print(f"models: {role}: using {c['model']}; skipped " + "; ".join(f"{m} ({w})" for m, w in skipped),
                  file=sys.stderr)
        return dict(c, skipped=skipped) if detail else c["model"]
    sys.exit(f"models: no usable model for role {role!r}: " + "; ".join(f"{m} ({w})" for m, w in skipped))


def candidates(role):
    """Every model id the role can use, in order, whatever its status (for argparse choices)."""
    return [c["model"] for c in roles().get(role, {}).get("candidates", [])]


def known_models():
    return {c["model"] for r in roles().values() for c in r["candidates"]}


MODEL_ID = re.compile(r"""["'](?:wan\d_\d|seedream_v\d+(?:_\w+)?|seedance_[\d_]+|gpt_image_[\d_]+|text2speech_v\d+|"""
                      r"""eleven_v\d+|scribe_v\d+|gemini_omni|nano_banana\w*|kling[\w.]*|veo\d*\w*)["']""")


def drift():
    """Model-id literals in pipeline/*.py (except tests and the registry's own readers) the registry doesn't list."""
    known, out = known_models() | set(_load(PRICES)), []
    for fn in sorted(os.listdir(HERE)):
        if not fn.endswith(".py") or fn in ("models.py", "self_test.py") or fn.startswith("test_"):
            continue
        for n, line in enumerate(open(os.path.join(HERE, fn), encoding="utf-8"), 1):
            if line.lstrip().startswith("#"):
                continue
            for m in MODEL_ID.findall(line):
                if m.strip("\"'") not in known:
                    out.append(f"{fn}:{n}: {m} is not in models.json or prices.json")
    return out


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "show"
    prices, gone = _load(PRICES), _unavailable()
    if cmd == "show":
        for name, spec in roles().items():
            print(f"{name}: {spec.get('about', '')}")
            for c in spec["candidates"]:
                why = _usable(c, prices, gone)
                print(f"   {c['model']:<16} {c.get('provider', ''):<11} {'ok' if not why else 'SKIPPED: ' + why}")
    elif cmd == "resolve" and len(sys.argv) > 2:
        c = resolve(sys.argv[2], detail=True)
        print(c["model"], f"({c.get('provider')}, shape {c.get('shape', '-')})")
    elif cmd == "check":
        bad = []
        for name in roles():
            try:
                resolve(name)
            except SystemExit as e:
                bad.append(str(e))
        bad += drift()
        print("\n".join(bad) if bad else f"models: {len(roles())} roles all resolve; no unregistered model ids")
        sys.exit(1 if bad else 0)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
