#!/usr/bin/env python3
"""The desk's master list of stories: what we are tracking, and whether each is heating up or fading.

A story stays on the list from the morning the desk first sends it until it drops out of the news cycle, so a
story Akhilesh didn't pick yesterday is measured again today instead of being forgotten.

  story_tracker.py add --id jio-ipo --title "Jio Platforms IPO" --query "Jio IPO|जियो आईपीओ" [--window 2026-10-28] [--note ...]
  story_tracker.py check              measure every active story with trends.py (one reading per story per day),
                                      then retire what has gone cold (COLD two checks running, or past its window).
                                      A deep-lane story (--lane deep) is never hot by nature: it retires only at its
                                      window (default 14 days after it was first sent) or by hand
  story_tracker.py score --id jio-ipo --score 8 [--note "valuation cut to $114 bn"]   today's desk score and news
  story_tracker.py made --id jio-ipo --episode E10    we made a reel on it; keep tracking it for a follow-up
  story_tracker.py retire --id jio-ipo --reason "listed; out of the news"
  story_tracker.py list [--json]      the board: status, direction, last readings
  story_tracker.py md                 write research/desk/TRACKER.md (the board for the local agent)

Data: registry/story_tracker.json. No login, no credits (Google News and YouTube via trends.py).
"""
import argparse, datetime as dt, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "registry", "story_tracker.json")
BOARD = os.path.join(ROOT, "research", "desk", "TRACKER.md")
RANK = {"COLD": 0, "FLAT": 1, "RISING": 2, "HOT": 3}
COLD_CHECKS_TO_RETIRE = 2


def today():
    return (dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)).date().isoformat()  # IST


def load():
    if not os.path.exists(DATA):
        return {"stories": []}
    with open(DATA) as f:
        return json.load(f)


def save(db):
    with open(DATA, "w") as f:
        json.dump(db, f, indent=1, ensure_ascii=False)
        f.write("\n")


def find(db, sid):
    for s in db["stories"]:
        if s["id"] == sid:
            return s
    sys.exit(f"no story with id {sid!r}; story_tracker.py list shows them")


def label_of(reading):
    return (reading.get("label") or "COLD").split()[0]


def direction(s):
    """rising / steady / fading / new, from the last two readings: the label first, then YouTube views and news."""
    r = [x for x in s.get("readings", []) if x.get("label")]
    if len(r) < 2:
        return "new"
    a, b = r[-2], r[-1]
    d = RANK[label_of(b)] - RANK[label_of(a)]
    if d:
        return "rising" if d > 0 else "fading"
    va, vb = a.get("yt_week_views") or 0, b.get("yt_week_views") or 0
    na, nb = a.get("news_1d") or 0, b.get("news_1d") or 0
    if vb > va * 1.25 or nb > na * 1.5 + 2:
        return "rising"
    if vb < va * 0.8 and nb <= na:
        return "fading"
    return "steady"


def reading_for(s, day):
    for r in s.setdefault("readings", []):
        if r["date"] == day:
            return r
    r = {"date": day}
    s["readings"].append(r)
    return r


def cmd_add(db, a):
    if any(s["id"] == a.id for s in db["stories"]):
        sys.exit(f"{a.id} is already tracked")
    db["stories"].append({"id": a.id, "title": a.title, "query": a.query, "first_seen": today(),
                          "lane": a.lane, "window_until": a.window or (None if a.lane == "hot" else
                          (dt.date.fromisoformat(today()) + dt.timedelta(days=14)).isoformat()), "status": "active", "notes": [a.note] if a.note else [],
                          "readings": []})
    save(db)
    print(f"tracking {a.id}")


def cmd_check(db, a):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import trends
    active = [s for s in db["stories"] if s["status"] in ("active", "made")]
    if not active:
        print("nothing active to check")
        return
    trending = trends.trending_india()
    day = today()
    for s in active:
        r = trends.analyse(s["query"], trending)
        rd = reading_for(s, day)
        rd.update({k: r[k] for k in ("label", "news_1d", "news_7d", "momentum_pct", "yt_week_videos",
                                     "yt_week_views", "yt_best_vph", "yt_top")})
        rd["google_trending"] = [f"{t} {tr}" for t, tr in r["google_trending"]]
        labels = [label_of(x) for x in s["readings"] if x.get("label")]
        past_window = s.get("window_until") and s["window_until"] < day
        gone_cold = s.get("lane", "hot") == "hot" and labels[-COLD_CHECKS_TO_RETIRE:] == ["COLD"] * COLD_CHECKS_TO_RETIRE
        if gone_cold or past_window:
            s["status"] = "retired"
            s["retired"] = {"date": day, "reason": "past its window" if past_window
                            else f"COLD on {COLD_CHECKS_TO_RETIRE} checks running"}
        print(f"{label_of(rd):<7} {direction(s):<8} {s['id']:<28} news {rd['news_1d']}/{rd['news_7d']}"
              f"  yt {rd['yt_week_views']:,} views, best {rd['yt_best_vph']:,}/hr"
              + ("  -> retired" if s["status"] == "retired" else ""))
    save(db)


def cmd_score(db, a):
    s = find(db, a.id)
    rd = reading_for(s, today())
    rd["desk_score"] = a.score
    if a.note:
        s.setdefault("notes", []).append(f"{today()}: {a.note}")
    save(db)


def cmd_made(db, a):
    s = find(db, a.id)
    s["status"] = "made"
    s["made_episode"] = a.episode
    save(db)


def cmd_retire(db, a):
    s = find(db, a.id)
    s["status"] = "retired"
    s["retired"] = {"date": today(), "reason": a.reason}
    save(db)


def board_rows(db):
    order = {"active": 0, "made": 1, "retired": 2}
    rows = []
    for s in sorted(db["stories"], key=lambda s: (order[s["status"]], s["first_seen"])):
        r = [x for x in s.get("readings", []) if x.get("label")]
        last = r[-1] if r else {}
        scores = [x["desk_score"] for x in s.get("readings", []) if "desk_score" in x]
        days = (dt.date.fromisoformat(today()) - dt.date.fromisoformat(s["first_seen"])).days + 1
        rows.append({"id": s["id"], "title": s["title"], "status": s["status"], "direction": direction(s),
                     "label": label_of(last) if last else "-", "days": days, "first_seen": s["first_seen"],
                     "window_until": s.get("window_until"), "news_today": last.get("news_1d"),
                     "news_week": last.get("news_7d"), "yt_week_views": last.get("yt_week_views"),
                     "yt_best_vph": last.get("yt_best_vph"), "desk_score": scores[-1] if scores else None,
                     "history": " ".join(label_of(x)[0] for x in r[-7:]),
                     "made_episode": s.get("made_episode"), "retired": s.get("retired"),
                     "notes": s.get("notes", [])[-2:]})
    return rows


def cmd_list(db, a):
    rows = board_rows(db)
    if a.json:
        print(json.dumps(rows, indent=1, ensure_ascii=False))
        return
    for r in rows:
        print(f"{r['status']:<8} {r['label']:<7} {r['direction']:<8} day {r['days']:<3} {r['id']:<28} {r['title']}")


def cmd_md(db, a):
    rows = board_rows(db)
    out = [f"# Story tracker\n", f"_Written {today()} by `pipeline/story_tracker.py md`. Data: registry/story_tracker.json._\n",
           "Every story the desk has sent stays here until it leaves the news cycle (COLD on two checks running, "
           "or past its window). Each morning `story_tracker.py check` measures them all again.\n",
           "Label history reads oldest to newest: H hot, R rising, F flat, C cold.\n",
           "| Story | Status | Now | Direction | Day | History | News today/week | YouTube views this week | Best views/hr | Desk score | Window |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        status = r["status"] + (f" ({r['made_episode']})" if r["made_episode"] else "") + \
            (f": {r['retired']['reason']}" if r["retired"] else "")
        out.append(f"| {r['title']} (`{r['id']}`) | {status} | {r['label']} | {r['direction']} | {r['days']} | {r['history']} | "
                   f"{r['news_today'] if r['news_today'] is not None else '-'}/{r['news_week'] if r['news_week'] is not None else '-'} | "
                   f"{r['yt_week_views'] or 0:,} | {r['yt_best_vph'] or 0:,} | {'-' if r['desk_score'] is None else format(r['desk_score'], 'g')} | {r['window_until'] or '-'} |")
    notes = [(r["title"], n) for r in rows if r["status"] != "retired" for n in r["notes"]]
    if notes:
        out.append("\n## Latest notes")
        out += [f"- **{t}:** {n}" for t, n in notes]
    os.makedirs(os.path.dirname(BOARD), exist_ok=True)
    with open(BOARD, "w") as f:
        f.write("\n".join(out) + "\n")
    print(f"wrote {os.path.relpath(BOARD, ROOT)}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    x = sub.add_parser("add"); x.add_argument("--id", required=True); x.add_argument("--title", required=True)
    x.add_argument("--query", required=True, help='trends.py phrases, "english|hindi"'); x.add_argument("--window")
    x.add_argument("--note"); x.add_argument("--lane", choices=["hot", "deep"], default="hot")
    sub.add_parser("check")
    x = sub.add_parser("score"); x.add_argument("--id", required=True); x.add_argument("--score", type=float, required=True)
    x.add_argument("--note")
    x = sub.add_parser("made"); x.add_argument("--id", required=True); x.add_argument("--episode", required=True)
    x = sub.add_parser("retire"); x.add_argument("--id", required=True); x.add_argument("--reason", required=True)
    x = sub.add_parser("list"); x.add_argument("--json", action="store_true")
    sub.add_parser("md")
    a = p.parse_args()
    db = load()
    globals()["cmd_" + a.cmd](db, a)


if __name__ == "__main__":
    main()
