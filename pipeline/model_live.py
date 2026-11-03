#!/usr/bin/env python3
"""Live check of the Higgsfield models in pipeline/models.json, using only the free cost preflight (get_cost true).
It never generates anything and never spends a credit.

  model_live.py refresh [--report-only]  for each model with a "probe" in models.json: ask what it would cost.
                                      Records availability in registry/model_state.json (models.py then skips a model the
                                      vendor rejected, for STATE_TTL_DAYS) and compares the quote with prices.json.
                                      A live price is applied automatically (Naveen, 2026-11-03), and every change is
                                      logged to registry/price_changes.jsonl. Two safeguards, because a misread reply
                                      must never set a price: a quote of 0 or below, or one that moves a price by more than
                                      MAX_MOVE (2x either way), is NOT applied and is flagged for a person. --report-only
                                      applies nothing. The spend guard is unchanged: it still prices every call from
                                      prices.json and blocks an unknown model; this keeps that table true (a stale low
                                      price is what could let a call overspend the 60-credit cap).
  model_live.py state                 what the last refresh found

Reading the answer: a 'model not found / not supported' style 4xx marks the model unavailable; 401/403 stop the run
(a key problem, not a model problem); 429, 5xx and network errors change nothing (unknown is not unavailable). The cost
is read from the first numeric field named cost / credits / total_cost / price in the reply; an unreadable reply records
'unparsed' and touches no price. The REST path/field names are config (see higgsfield_api.py); run `higgsfield.py check`
first. Not yet exercised against the live API in this repo's tests: tests use a stub fetcher."""
import argparse, datetime as dt, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import models  # noqa: E402

STATE = models.STATE
MAX_MOVE = 2.0
CHANGES = os.environ.get("MODEL_PRICE_LOG") or os.path.join(os.path.dirname(HERE), "registry", "price_changes.jsonl")
COST_KEYS = ("cost", "credits", "total_cost", "price", "credit_cost")
GONE_WORDS = ("not found", "unknown model", "not supported", "unsupported", "deprecated", "no longer", "invalid model", "retired")


def load_state(path=None):
    try:
        return json.load(open(path or STATE, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def parse_cost(body):
    try:
        d = json.loads(body)
    except (ValueError, TypeError):
        return None
    stack = [d]
    while stack:
        x = stack.pop(0)
        if isinstance(x, dict):
            for k in COST_KEYS:
                if isinstance(x.get(k), (int, float)) and not isinstance(x.get(k), bool):
                    return float(x[k])
            stack.extend(v for v in x.values() if isinstance(v, (dict, list)))
        elif isinstance(x, list):
            stack.extend(x)
    return None


def classify(status, body):
    """('ok'|'gone'|'auth'|'unknown', cost or None)"""
    if status in (401, 403):
        return "auth", None
    if status == 200 or status == 201:
        return "ok", parse_cost(body)
    text = (body.decode("utf-8", "replace") if isinstance(body, (bytes, bytearray)) else str(body)).lower()
    if status in (400, 404, 410, 422) and any(w in text for w in GONE_WORDS):
        return "gone", None
    return "unknown", None


def unit_price(spec, cost):
    """Credits per image / per second / per call from the probe's own units."""
    if "per_image" in spec:
        return {"per_image": cost / max(1, int(spec["per_image"]))}
    if "per_second" in spec:
        res, secs = spec["per_second"]["resolution"], float(spec["per_second"]["seconds"])
        return {"per_second": {res: cost / secs}}
    return {"per_call": cost}


def refresh(fetch, apply=True, state_path=None, prices_path=None, registry=None):
    reg = registry or models._load(models.REGISTRY)
    prices_path = prices_path or models.PRICES
    prices = models._load(prices_path)
    state, report, changed = load_state(state_path), [], False
    probes = {}
    for role in reg.get("roles", {}).values():
        for c in role["candidates"]:
            if c.get("provider") == "higgsfield" and c.get("probe"):
                probes[c["model"]] = c["probe"]
    for model, probe in sorted(probes.items()):
        payload = dict(probe["payload"], model=model, get_cost=True)
        status, body = fetch(probe["path"], payload)
        kind, cost = classify(status, body)
        if kind == "auth":
            sys.exit(f"model_live: HTTP {status} from Higgsfield: a key problem, not a model problem. Stopped; nothing recorded.")
        entry = {"checked_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"), "http": status}
        if kind == "gone":
            entry.update(available=False, reason="vendor rejected the model")
            report.append(f"{model}: UNAVAILABLE (HTTP {status}); models.py will skip it")
        elif kind == "ok":
            entry.update(available=True)
            if cost is None:
                entry["price"] = "unparsed"
                report.append(f"{model}: available; cost reply not readable, price untouched")
            else:
                new = unit_price(probe["units"], cost)
                entry["quote"] = new
                old = prices.get(model)
                if old != new and _differs(old, new):
                    sane, why = _sane(old, new)
                    if not sane:
                        report.append(f"{model}: price drift {json.dumps(old)} -> {json.dumps(new)} NOT applied ({why}); a person should check")
                    elif apply:
                        prices[model] = _merge(old, new); changed = True
                        with open(CHANGES, "a", encoding="utf-8") as lg:
                            lg.write(json.dumps({"at": entry["checked_at"], "model": model, "old": old, "new": new}) + "\n")
                        report.append(f"{model}: price drift {json.dumps(old)} -> {json.dumps(new)}  (applied)")
                    else:
                        report.append(f"{model}: price drift {json.dumps(old)} -> {json.dumps(new)}  (report only, not applied)")
                else:
                    report.append(f"{model}: available, price {json.dumps(new)} matches")
        else:
            entry.update(available=state.get(model, {}).get("available"), reason="inconclusive; kept previous state")
            report.append(f"{model}: inconclusive (HTTP {status}); nothing changed")
        state[model] = entry
    json.dump(state, open(state_path or STATE, "w"), indent=1)
    if changed:
        json.dump(prices, open(prices_path, "w"), indent=1)
    return report


def _near(a, b):
    return abs(a - b) <= 1e-6 + 0.005 * max(abs(a), abs(b))


def _differs(old, new):
    if not old:
        return True
    for k, v in new.items():
        if isinstance(v, dict):
            for r, x in v.items():
                if not _near((old.get(k) or {}).get(r, -1), x):
                    return True
        elif not _near(old.get(k, -1), v):
            return True
    return False


def _flat(p):
    out = {}
    for k, v in (p or {}).items():
        if isinstance(v, dict):
            out.update({f"{k}.{r}": x for r, x in v.items()})
        else:
            out[k] = v
    return out


def _sane(old, new):
    """A new price is believed only if every figure is positive and within MAX_MOVE of the old one (a new model has no old)."""
    o = _flat(old)
    for k, v in _flat(new).items():
        if not isinstance(v, (int, float)) or v <= 0:
            return False, f"{k} came back as {v}"
        if k in o and o[k] > 0 and not (1 / MAX_MOVE <= v / o[k] <= MAX_MOVE):
            return False, f"{k} moved {o[k]:g} -> {v:g}, more than {MAX_MOVE:g}x"
    return True, ""


def _merge(old, new):
    out = json.loads(json.dumps(old or {}))
    for k, v in new.items():
        if isinstance(v, dict):
            out.setdefault(k, {}).update(v)
        else:
            out[k] = v
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["refresh", "state"]); ap.add_argument("--report-only", action="store_true")
    a = ap.parse_args()
    if a.cmd == "state":
        print(json.dumps(load_state(), indent=1)); return
    from higgsfield_api import request
    print("\n".join(refresh(lambda path, payload: request(path, payload), not a.report_only)) or "no probes configured in models.json")


if __name__ == "__main__":
    main()
