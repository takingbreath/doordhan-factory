#!/usr/bin/env python3
"""The credit ledger behind hard rules 1 and 2. pipeline/hooks/spend_guard.py reads it before every paid Higgsfield call
and blocks a call that has no approved script behind it or would go over the budget; this file is the command line
for the same ledger, and the library the guard uses.

  python3 pipeline/spend.py start SLUG          the episode we are spending on now; needs registry/scripts/SLUG.json,
                                                frozen with approved_by (script_freeze.py). Budget 60 credits.
  python3 pipeline/spend.py start experiment    the weekly experiments budget instead (15 credits a week)
  python3 pipeline/spend.py status              active episode, budget, spent, left, the last entries
  python3 pipeline/spend.py raise SLUG CREDITS --by Akhilesh --quote "his words"
                                                Akhilesh's yes to a bigger budget, in his own words (only he can)
  python3 pipeline/spend.py declare CREDITS "what"   the price of the next paid call the guard can't price itself
                                                (get it with get_cost true, or from the tool's own answer)
  python3 pipeline/spend.py refund CREDITS "what"    a job that failed and was refunded, or was charged twice here
  python3 pipeline/spend.py price MODEL CREDITS --per image|second|call [--resolution 720p]
  python3 pipeline/spend.py stop                no active episode (the guard then blocks every paid call)

The ledger lives in work/ (git-ignored): work/active_episode.json, work/<slug>/spend.json and
work/experiments/spend-<year>-W<week>.json. Credits are charged when the call is sent; a failed or refunded job is
put back with `refund`. The ledger is per machine: an episode moved to another machine starts a new ledger there, so
carry the running total over with `declare` + a note if that ever happens."""
import argparse, contextlib, datetime as dt, fcntl, json, os, sys

ROOT = os.environ.get("DOORDHAN_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, "work")
ACTIVE = os.path.join(WORK, "active_episode.json")
PRICES = os.path.join(ROOT, "pipeline", "prices.json")
EPISODE_BUDGET = 60        # hard rule 2
EXPERIMENT_BUDGET = 15     # hard rule 2, per ISO week
PENDING_MAX_AGE_S = 30 * 60


def now():
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def week():
    y, w, _ = dt.date.today().isocalendar()
    return f"{y}-W{w:02d}"


def ledger_path(slug):
    if slug == "experiment":
        return os.path.join(WORK, "experiments", f"spend-{week()}.json")
    return os.path.join(WORK, slug, "spend.json")


def read_json(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def write_json(path, doc):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


@contextlib.contextmanager
def locked():
    os.makedirs(WORK, exist_ok=True)
    with open(os.path.join(WORK, ".spend.lock"), "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        yield


def active_slug():
    doc = read_json(ACTIVE) or {}
    return doc.get("slug")


def script_approval(slug):
    """(ok, why) for registry/scripts/<slug>.json: frozen, with an approver."""
    path = os.path.join(ROOT, "registry", "scripts", f"{slug}.json")
    doc = read_json(path)
    if doc is None:
        return False, (f"registry/scripts/{slug}.json does not exist. No credits are spent before the script is "
                       "approved and frozen (hard rule 1): freeze it with pipeline/script_freeze.py, naming who approved it.")
    if not str(doc.get("approved_by") or "").strip():
        return False, f"registry/scripts/{slug}.json has no approved_by. Hard rule 1: Akhilesh or Naveen approves the script first."
    return True, f"script approved by {doc['approved_by']}"


def load(slug):
    led = read_json(ledger_path(slug)) or {}
    led.setdefault("slug", slug)
    led.setdefault("budget", EXPERIMENT_BUDGET if slug == "experiment" else EPISODE_BUDGET)
    for k in ("raises", "entries", "pending"):
        led.setdefault(k, [])
    return led


def budget(led):
    return led["raises"][-1]["to"] if led["raises"] else led["budget"]


def spent(led):
    return round(sum(e["credits"] for e in led["entries"]), 2)


def status_text(slug):
    led = load(slug)
    b, s = budget(led), spent(led)
    label = f"experiments, week {week()}" if slug == "experiment" else f"episode {slug}"
    return f"{label}: spent {s:g} of {b:g} credits, {b - s:g} left"


# ---- pricing, used by the guard ----

def price_one(params, prices):
    """Credits for one generation request, or (None, why) when the guard can't price it."""
    if not isinstance(params, dict):
        return None, "the request's params are not an object"
    model = params.get("model")
    p = prices.get(model)
    if not p:
        return None, f"no price for model {model!r} in pipeline/prices.json"
    count = int(params.get("count") or 1)
    if "per_image" in p:
        return p["per_image"] * count, f"{model} x{count}"
    if "per_call" in p:
        return p["per_call"] * count, f"{model}"
    if "per_second" in p:
        dur = params.get("duration")
        if dur is None:
            return None, f"{model} without a duration: pass duration explicitly (billing is per requested second)"
        res = params.get("resolution") or "default"
        rate = p["per_second"].get(res, p["per_second"].get("default"))
        if rate is None:
            return None, f"no price for {model} at {res} in pipeline/prices.json"
        return rate * float(dur) * count, f"{model} {res} {dur}s"
    return None, f"pipeline/prices.json has no usable price for {model}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("start"); s.add_argument("slug")
    sub.add_parser("status")
    sub.add_parser("stop")
    r = sub.add_parser("raise"); r.add_argument("slug"); r.add_argument("credits", type=float)
    r.add_argument("--by", required=True); r.add_argument("--quote", required=True)
    d = sub.add_parser("declare"); d.add_argument("credits", type=float); d.add_argument("what")
    f = sub.add_parser("refund"); f.add_argument("credits", type=float); f.add_argument("what")
    p = sub.add_parser("price"); p.add_argument("model"); p.add_argument("credits", type=float)
    p.add_argument("--per", choices=["image", "second", "call"], required=True); p.add_argument("--resolution", default="default")
    a = ap.parse_args()

    with locked():
        if a.cmd == "start":
            if a.slug != "experiment":
                ok, why = script_approval(a.slug)
                if not ok:
                    sys.exit("Not started: " + why)
                print(why)
            write_json(ACTIVE, {"slug": a.slug, "since": now()})
            print("active: " + status_text(a.slug))
        elif a.cmd == "stop":
            with contextlib.suppress(FileNotFoundError):
                os.remove(ACTIVE)
            print("no active episode: every paid Higgsfield call is blocked until `spend.py start`")
        elif a.cmd == "status":
            slug = active_slug()
            if not slug:
                print("no active episode (python3 pipeline/spend.py start SLUG)")
                return
            led = load(slug)
            print("active: " + status_text(slug))
            for e in led["entries"][-8:]:
                print(f"  {e['at'][:16]}  {e['credits']:>6g}  {e['what']}")
            for e in led["pending"]:
                print(f"  declared, not yet used: {e['credits']:g}  {e['what']}")
        elif a.cmd == "raise":
            if a.by.strip().lower() != "akhilesh":
                sys.exit("Only Akhilesh approves spending above the budget (hard rule 1). Send him the breakdown and wait.")
            led = load(a.slug)
            led["raises"].append({"to": a.credits, "by": a.by, "quote": a.quote, "at": now()})
            write_json(ledger_path(a.slug), led)
            print("raised: " + status_text(a.slug))
        elif a.cmd in ("declare", "refund"):
            slug = active_slug()
            if not slug:
                sys.exit("no active episode (python3 pipeline/spend.py start SLUG)")
            led = load(slug)
            if a.cmd == "declare":
                led["pending"].append({"credits": a.credits, "what": a.what, "at": now()})
            else:
                led["entries"].append({"credits": -abs(a.credits), "what": "refund: " + a.what, "at": now(), "source": "refund"})
            write_json(ledger_path(slug), led)
            print(f"{'declared' if a.cmd == 'declare' else 'refunded'} {a.credits:g}: " + status_text(slug))
        elif a.cmd == "price":
            prices = read_json(PRICES, {})
            entry = prices.setdefault(a.model, {})
            if a.per == "second":
                entry.setdefault("per_second", {})[a.resolution] = a.credits
            else:
                entry["per_" + a.per] = a.credits
            write_json(PRICES, prices)
            print(f"{a.model}: {entry}; commit pipeline/prices.json")


if __name__ == "__main__":
    main()
