#!/usr/bin/env python3
"""PreToolUse hook on every paid Higgsfield tool (.claude/settings.json; the matcher names the tools by their suffix,
because each person's connector has its own ID). Hard rules 1 and 2, whatever the instructions in the session:
- no credits without an active episode whose script is frozen and approved (registry/scripts/<slug>.json), or the
  weekly experiments budget;
- no call that takes the episode over its budget (60 credits, or what Akhilesh raised it to with `spend.py raise`);
- every call is written to the ledger (pipeline/spend.py) as it is sent.
Generations are priced from their own params with pipeline/prices.json; any other paid tool, or an unknown model,
needs `python3 pipeline/spend.py declare CREDITS "what"` first. A cost preflight (get_cost true) is free and passes.
Exit 2 blocks the call and tells Claude why; the guard fails closed (unreadable input or an error blocks)."""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import spend  # noqa: E402

GENERATE = {"generate_image", "generate_image_batch", "generate_video", "generate_video_batch",
            "generate_audio", "generate_audio_batch"}


def block(msg):
    print("Blocked by the spend guard (hard rules 1 and 2): " + msg, file=sys.stderr)
    sys.exit(2)


def requests_of(suffix, ti):
    if suffix.endswith("_batch"):
        return [r.get("params") for r in (ti.get("requests") or [])]
    p = ti.get("params", ti)
    if isinstance(p, str):
        try:
            p = json.loads(p)
        except ValueError:
            p = {"prompt": p}  # a bare prompt: no model to price
    return [p]


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        block("the hook could not read the tool call.")
    tool = data.get("tool_name") or ""
    suffix = tool.split("__")[-1]
    ti = data.get("tool_input") or {}
    reqs = requests_of(suffix, ti)
    if reqs and all(isinstance(p, dict) and p.get("get_cost") is True for p in reqs):
        sys.exit(0)  # a cost preflight spends nothing

    with spend.locked():
        slug = spend.active_slug()
        if not slug:
            block("no active episode. After the script is approved and frozen, run "
                  "`python3 pipeline/spend.py start <slug>` (or `start experiment` for the 15-credit weekly "
                  "experiments budget), then send the call again.")
        if slug != "experiment":
            ok, why = spend.script_approval(slug)
            if not ok:
                block(why)
        led = spend.load(slug)
        prices = spend.read_json(spend.PRICES, {})

        cost, parts, unpriced = 0.0, [], []
        if suffix in GENERATE:
            for p in reqs:
                c, desc = spend.price_one(p, prices)
                if c is None:
                    unpriced.append(desc)
                else:
                    cost += c
                    parts.append(f"{desc}: {c:g}")
        else:
            unpriced.append(f"{suffix} is a paid tool the guard cannot price")

        declared = None
        if unpriced:
            fresh = [e for e in led["pending"]
                     if (spend.dt.datetime.now().astimezone() - spend.dt.datetime.fromisoformat(e["at"])).total_seconds()
                     < spend.PENDING_MAX_AGE_S]
            if not fresh:
                block("; ".join(unpriced) + ". Find the price (the same call with get_cost true is free; add it with "
                      "`python3 pipeline/spend.py price MODEL CREDITS --per image|second|call`), or declare this "
                      "call's price with `python3 pipeline/spend.py declare CREDITS \"what\"`, then send it again.")
            declared = fresh[-1]
            cost = declared["credits"]
            parts = [f"declared: {declared['what']}: {cost:g}"]

        b, s = spend.budget(led), spend.spent(led)
        if s + cost > b + 1e-9:
            who = "the weekly experiments budget" if slug == "experiment" else f"episode {slug}'s budget"
            block(f"this call costs {cost:g} credits ({'; '.join(parts)}), and {who} has {b - s:g} of {b:g} left "
                  f"(spent {s:g}). Stop and send Akhilesh a breakdown (what is done, what is left and its cost). "
                  "Only his yes raises the budget: `python3 pipeline/spend.py raise <slug> <credits> --by Akhilesh "
                  "--quote \"<his words>\"`. Naveen can approve scripts and finals, not spending.")

        if declared:
            led["pending"].remove(declared)
        led["entries"].append({"at": spend.now(), "tool": suffix, "credits": round(cost, 2),
                               "what": "; ".join(parts), "source": "declared" if declared else "priced"})
        spend.write_json(spend.ledger_path(slug), led)
        print(f"spend guard: {cost:g} credits; {spend.status_text(slug)}")
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # fail closed
        block(f"the guard failed ({type(e).__name__}: {e}). Fix pipeline/hooks/spend_guard.py or tell Akhilesh; "
              "do not work around it.")
