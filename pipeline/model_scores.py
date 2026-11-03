#!/usr/bin/env python3
"""Quality memory for models: what happened to each model's shots at the QC gate, so a role can prefer the model that
actually passes. One line per (reel, role, model) in registry/model_scores.jsonl:
  {"at", "reel", "role", "model", "ok": passed the gate without a repair, "failed": [checks], "repaired": [checks], "credits"}

  model_scores.py record --reel E16 --role talking_shot_creator --model wan3_0 [--failed lipsync] [--repaired face]
  model_scores.py table                      per role and model: reels, clean-pass rate (smoothed), and the verdict

qc_gate.py calls record_from_stamp() when its manifest says which model made which role ("models": {"talking_shot":
"wan2_7"}). The ranking is advice that models.py applies only to roles marked "adaptive": a model needs MIN_N reels of
its own before it can move, a challenger must beat the incumbent by MARGIN, and a model with no data is never promoted
(it can be tried on the weekly experiments budget: `models.py explore`). Nothing here spends credits."""
import argparse, datetime as dt, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCORES = os.environ.get("MODEL_SCORES_FILE") or os.path.join(os.path.dirname(HERE), "registry", "model_scores.jsonl")
MIN_N = 5          # reels of its own before a model's score counts
MARGIN = 0.15      # clean-pass rate a challenger must beat the listed first choice by


def _now():
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def rows(path=None):
    out = []
    try:
        for line in open(path or SCORES, encoding="utf-8"):
            if line.strip():
                out.append(json.loads(line))
    except OSError:
        pass
    return out


def record(reel, role, model, failed=(), repaired=(), credits=None, path=None):
    row = {"at": _now(), "reel": reel, "role": role, "model": model, "ok": not failed and not repaired,
           "failed": sorted(set(failed)), "repaired": sorted(set(repaired)), "credits": credits}
    with open(path or SCORES, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def record_from_stamp(doc, manifest, path=None):
    """After qc_gate stamps: one row per role the manifest names. Rows that failed or were repaired count against the model."""
    models = (manifest or {}).get("models") or {}
    mine = ("lipsync", "face")     # what a video model can be blamed for; a wrong hook, card or loudness is not its fault
    failed = [r["check"] for r in doc.get("rows", []) if r.get("status") in ("failed",) and r["check"] in mine]
    repaired = [r["check"] for r in doc.get("rows", []) if r.get("status") == "repaired" and r["check"] in mine]
    reel = os.path.splitext(os.path.basename(doc.get("final", "")))[0]
    # dedupe: re-running the gate on the same final must not count the reel twice
    seen = {(r["reel"], r["role"], r["model"]) for r in rows(path)}
    out = []
    for role, model in models.items():
        if (reel, role, model) not in seen:
            out.append(record(reel, role, model, failed, repaired, (manifest or {}).get("credits"), path))
    return out


def stats(role, path=None):
    """{model: (reels, clean_rate)} with a Laplace-smoothed rate, so 1 of 1 is not 100%."""
    agg = {}
    for r in rows(path):
        if r["role"] == role:
            n, ok = agg.get(r["model"], (0, 0))
            agg[r["model"]] = (n + 1, ok + (1 if r["ok"] else 0))
    return {m: (n, (ok + 1) / (n + 2)) for m, (n, ok) in agg.items()}


def preferred(role, listed, path=None):
    """Reorder `listed` (model ids, first choice first) by evidence. Returns (order, why or None).
    The first-listed model stays first unless a challenger with >= MIN_N reels beats it by MARGIN (and the incumbent
    has >= MIN_N reels too, or none at all so there is nothing to protect). Models without data keep their place."""
    st = stats(role, path)
    if len(listed) < 2:
        return list(listed), None
    inc = listed[0]
    n_i, s_i = st.get(inc, (0, None))
    best = None
    for m in listed[1:]:
        n, s = st.get(m, (0, None))
        if n >= MIN_N and (n_i >= MIN_N) and s - s_i >= MARGIN and (best is None or s > best[1]):
            best = (m, s)
    if not best:
        return list(listed), None
    order = [best[0]] + [m for m in listed if m != best[0]]
    return order, f"{best[0]} passes the gate clean {best[1]:.0%} of {st[best[0]][0]} reels vs {inc} {s_i:.0%} of {n_i}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("record"); r.add_argument("--reel", required=True); r.add_argument("--role", required=True)
    r.add_argument("--model", required=True); r.add_argument("--failed", nargs="*", default=[])
    r.add_argument("--repaired", nargs="*", default=[]); r.add_argument("--credits", type=float)
    sub.add_parser("table")
    a = ap.parse_args()
    if a.cmd == "record":
        print(json.dumps(record(a.reel, a.role, a.model, a.failed, a.repaired, a.credits)))
    else:
        roles = sorted({r["role"] for r in rows()})
        for role in roles:
            for m, (n, s) in sorted(stats(role).items(), key=lambda kv: -kv[1][1]):
                print(f"{role:<22} {m:<16} reels {n:<3} clean {s:.0%}{'' if n >= MIN_N else '  (too few to count)'}")
        if not roles:
            print("no scores yet")


if __name__ == "__main__":
    main()
