#!/usr/bin/env python3
"""The strategy desk's scoreboard: every reel's numbers, every bet's position, and a verdict on each bet.

Data, all in registry/ (edit these, never the generated tables):
  reels.csv      one row per reel we made (id, what it carried, credits, and its Instagram code once posted)
  snapshots.csv  one row per reading of a posted reel (plays, likes, comments, shares, saves, watch, skip)
  account.csv    one row per reading of the account (followers, 30-day views)
  bets.json      the book: bets with a metric, baseline, target, stop and sample size, plus the campaign

Usage (from the repo root):
  scoreboard.py                     full report
  scoreboard.py brief               three lines on where we stand (for sessions; uses bet IDs)
  scoreboard.py status              the same in plain English, for emails
  scoreboard.py write               regenerate registry/performance.md and the book in docs/strategy.md
  scoreboard.py ingest-ig FILE      add a reading from vidIQ's Instagram owner insights (the tool's JSON, saved to FILE)
  scoreboard.py link REEL CODE      tie a reel row to its Instagram shortcode once it's posted
  scoreboard.py add-reel --id E3 --format samachar --story "Bank strike" --bets B1,B2 --length 27 --credits 48
Options: --root DIR (another repo root, for tests), --now "YYYY-MM-DD HH:MM" (IST, for tests)."""
import argparse, csv, json, os, re, statistics, sys
from datetime import datetime, timedelta, timezone

IST = timezone(timedelta(hours=5, minutes=30))
MATURE_H = 72          # plays are compared at the first reading after 72 hours
MIN_PLAYS = 50         # a reel with fewer plays says nothing yet
REEL_COLS = ["id", "platform", "ig_code", "yt_id", "posted_ist", "format", "story", "bets", "length_s", "outfit",
             "desk_score", "credits", "notes"]
SNAP_COLS = ["platform", "code", "posted_ist", "taken_ist", "hours", "views", "likes", "comments", "shares", "saves",
             "avg_watch_s", "watched_pct", "skip_rate", "length_s", "caption"]
ACCT_COLS = ["taken_ist", "platform", "followers", "views_30d"]
METRICS = {  # name: (label, which way is better)
    "skip_rate": ("skip rate %", "lower"),
    "watched_pct": ("watched %", "higher"),
    "sends_per_1k": ("sends per 1k plays", "higher"),
    "saves_per_1k": ("saves per 1k plays", "higher"),
    "likes_per_1k": ("likes per 1k plays", "higher"),
    "comments_per_1k": ("comments per 1k plays", "higher"),
    "views": ("median plays at 72 h", "higher"),
    "credits_per_1k": ("credits per 1k plays", "lower"),
}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def P(*a):
    return os.path.join(ROOT, *a)


def now_ist(arg=None):
    return datetime.strptime(arg, "%Y-%m-%d %H:%M").replace(tzinfo=IST) if arg else datetime.now(IST)


def num(x):
    try:
        return float(x) if str(x).strip() not in ("", "None", "null") else None
    except ValueError:
        return None


def read_csv(path, cols):
    if not os.path.exists(path):
        return []
    with open(path, newline="") as f:
        return [{c: (r.get(c) or "") for c in cols} for r in csv.DictReader(f)]


def write_csv(path, cols, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n"); w.writeheader(); w.writerows(rows)


def load():
    return dict(reels=read_csv(P("registry", "reels.csv"), REEL_COLS),
                snaps=read_csv(P("registry", "snapshots.csv"), SNAP_COLS),
                acct=read_csv(P("registry", "account.csv"), ACCT_COLS),
                book=json.load(open(P("registry", "bets.json"))))


# ---------- per-reel readings ----------
def readings(d, platform="instagram"):
    """reel id -> (latest snapshot, mature snapshot or None). Only reels that are posted and have readings."""
    code_key = "ig_code" if platform == "instagram" else "yt_id"
    by_code = {}
    for s in d["snaps"]:
        if s["platform"] == platform:
            by_code.setdefault(s["code"], []).append(s)
    out = {}
    for r in d["reels"]:
        ss = sorted(by_code.get(r[code_key], []), key=lambda s: num(s["hours"]) or 0) if r[code_key] else []
        if ss:
            mature = next((s for s in ss if (num(s["hours"]) or 0) >= MATURE_H), None)
            out[r["id"]] = (ss[-1], mature)
    return out


def metric(name, reels, reads):
    """Pooled value of a metric over reels (weighted by plays), and how many reels it rests on."""
    pairs = []
    for r in reels:
        latest, mature = reads.get(r["id"], (None, None))
        snap = mature if name == "views" else latest
        if snap and (num(snap["views"]) or 0) >= MIN_PLAYS:
            pairs.append((r, snap))
    if not pairs:
        return None, 0
    v = lambda s: num(s["views"]) or 0
    if name == "views":
        return statistics.median(v(s) for _, s in pairs), len(pairs)
    if name in ("skip_rate", "watched_pct"):
        pts = [(v(s), num(s[name])) for _, s in pairs if num(s[name]) is not None]
        tot = sum(w for w, _ in pts)
        return (round(sum(w * x for w, x in pts) / tot, 1) if tot else None), len(pts)
    if name == "credits_per_1k":
        pts = [(v(s), num(r["credits"])) for r, s in pairs if num(r["credits"]) is not None]
        tot = sum(w for w, _ in pts)
        return (round(1000 * sum(c for _, c in pts) / tot, 1) if tot else None), len(pts)
    field = {"sends_per_1k": "shares", "saves_per_1k": "saves", "likes_per_1k": "likes", "comments_per_1k": "comments"}[name]
    # A public reading has no shares or saves: unknown, not zero, so it stays out of the pool.
    pairs = [(r, s) for r, s in pairs if num(s[field]) is not None]
    tot = sum(v(s) for _, s in pairs)
    return (round(1000 * sum(num(s[field]) for _, s in pairs) / tot, 1) if tot else None), len(pairs)


def better(name, a, b):
    """True when value a is at least as good as level b."""
    return a <= b if METRICS[name][1] == "lower" else a >= b


def verdict(bet, value, n):
    m = bet["metric"]
    if bet.get("status") == "watch":
        return "WATCH", "tracked; judged at the monthly review"
    if bet.get("status") != "open":
        return bet.get("status", "?").upper(), bet.get("result") or ""
    if value is None:
        return "WAITING", "no reel with readings yet"
    if n < bet["min_reels"]:
        warn = n >= 2 and not better(m, value, bet["stop"]) and value != bet["stop"]
        return "HOLD", f"{n}/{bet['min_reels']} reels" + (" · warning: beyond the stop so far" if warn else "")
    if better(m, value, bet["target"]):
        return "TARGET HIT", "make the lever the default; press it"
    if better(m, bet["stop"], value):
        return "STOP HIT", "close it, undo the lever, write down why"
    if n >= bet["max_reels"]:
        return "TIME STOP", "no edge after the full sample; close it"
    return "HOLD", f"{n} reels, between stop and target"


def bet_reels(d, bet):
    return [r for r in d["reels"] if bet["id"] in re.split(r"[;, ]+", r["bets"])]


def book_rows(d, platform="instagram"):
    reads = readings(d, platform)
    rows = []
    for b in d["book"]["bets"]:
        reels = bet_reels(d, b)
        val, n = metric(b["metric"], reels, reads)
        v, why = verdict(b, val, n)
        rows.append(dict(bet=b, value=val, n=n, carried=len(reels), verdict=v, why=why))
    return rows


def fmt(x):
    return "–" if x is None else (f"{x:.0f}" if abs(x) >= 100 else f"{x:g}")


# ---------- account and campaign ----------
def followers(d, platform="instagram", days=7, now=None):
    a = [r for r in d["acct"] if r["platform"] == platform and num(r["followers"]) is not None]
    if not a:
        return None, None
    a.sort(key=lambda r: r["taken_ist"])
    last = a[-1]
    cutoff = ((now or now_ist()) - timedelta(days=days)).strftime("%Y-%m-%d %H:%M")
    before = [r for r in a if r["taken_ist"] <= cutoff] or a[:1]
    return int(num(last["followers"])), int(num(last["followers"]) - num(before[-1]["followers"]))


def campaign_rows(d, platform="instagram"):
    c = d["book"].get("campaign") or {}
    reads = readings(d, platform)
    reels = [r for r in d["reels"] if r["posted_ist"] and r["posted_ist"][:10] >= c.get("started", "")]
    out = []
    for t in c.get("targets", []):
        if t["metric"] == "followers":
            val, n = followers(d, platform)[0], None
            ok = val is not None and val >= t["target"]
        elif t["metric"] == "best_views":
            vals = [num(reads[r["id"]][0]["views"]) for r in reels if r["id"] in reads]
            val, n = (max(vals) if vals else None), len(vals)
            ok = val is not None and val >= t["target"]
        else:
            val, n = metric(t["metric"], reels, reads)
            ok = val is not None and better(t["metric"], val, t["target"])
        out.append(dict(t=t, value=val, n=n, ok=ok))
    stop = c.get("stop")
    stop_state = None
    if stop:
        val, n = metric(stop["metric"], reels, reads)
        posted = len([r for r in reels if r["id"] in reads])
        if posted >= stop["after_reels"] and val is not None and not better(stop["metric"], val, stop["level"]):
            stop_state = f"STRATEGY STOP HIT: {METRICS[stop['metric']][0]} {fmt(val)} after {posted} reels (needed {fmt(stop['level'])}). {stop['means']}"
        else:
            stop_state = f"strategy stop: {posted}/{stop['after_reels']} reels posted this stage; {METRICS[stop['metric']][0]} now {fmt(val)}, must reach {fmt(stop['level'])}"
    return c, out, stop_state


# ---------- reports ----------
def label(m):
    return METRICS.get(m, (m,))[0] if m != "followers" and m != "best_views" else {"followers": "followers", "best_views": "best reel's plays"}[m]


def book_table(d):
    L = ["| Bet | Lever | Judged on | Baseline | Now | Target | Stop | Reels (judged/carried) | Verdict |",
         "|---|---|---|---|---|---|---|---|---|"]
    for x in book_rows(d):
        b = x["bet"]
        L.append(f"| {b['id']} {b['name']} | {b['lever']} | {label(b['metric'])} | {fmt(b.get('baseline'))} | {fmt(x['value'])} | "
                 f"{fmt(b['target'])} | {fmt(b['stop'])} | {x['n']}/{x['carried']} (judge at {b['min_reels']}, max {b['max_reels']}) | "
                 f"**{x['verdict']}** {x['why']} |")
    return "\n".join(L)


def campaign_block(d):
    c, rows, stop = campaign_rows(d)
    if not c:
        return ""
    L = [f"**{c['name']}** ({c['started']} to {c['ends']}): {c.get('goal', '')}", ""]
    for x in rows:
        L.append(f"- {label(x['t']['metric'])}: now {fmt(x['value'])}, target {fmt(x['t']['target'])} → {'on target' if x['ok'] else 'not yet'}")
    if stop:
        L.append(f"- {stop}")
    return "\n".join(L)


def reel_table(d):
    reads = readings(d)
    L = ["| Reel | Posted | Format · story | Bets | Length | Desk | Credits | Plays @72h | Plays now (age) | Skip % | Watched % | Sends/1k | Saves/1k | Likes/1k | Notes |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in d["reels"]:
        latest, mature = reads.get(r["id"], (None, None))
        one = [r] if latest else []
        per = lambda m: fmt(metric(m, one, reads)[0]) if one else "–"
        L.append(f"| {r['id']} | {r['posted_ist'] or 'not posted'} | {r['format']} · {r['story']} | {r['bets'] or '–'} | {r['length_s'] or '–'} | "
                 f"{r['desk_score'] or '–'} | {r['credits'] or '–'} | {fmt(num(mature['views'])) if mature else '–'} | "
                 f"{(fmt(num(latest['views'])) + ' (' + fmt(num(latest['hours'])) + ' h)') if latest else '–'} | "
                 f"{fmt(num(latest['skip_rate'])) if latest else '–'} | {fmt(num(latest['watched_pct'])) if latest else '–'} | "
                 f"{per('sends_per_1k')} | {per('saves_per_1k')} | {per('likes_per_1k')} | {r['notes']} |")
    linked = {r["ig_code"] for r in d["reels"] if r["ig_code"]}
    stray = sorted({(s["code"], s["posted_ist"], s["caption"][:40]) for s in d["snaps"] if s["platform"] == "instagram" and s["code"] not in linked})
    if stray:
        L += ["", "Posted but not linked to a reel row (run `scoreboard.py link`):"] + [f"- {c} posted {p}: \"{cap}\"" for c, p, cap in stray]
    return "\n".join(L)


def report(d):
    f, df = followers(d)
    return "\n".join([
        f"## Account\nInstagram followers: {f if f is not None else '–'} ({'+' if (df or 0) >= 0 else ''}{df if df is not None else '–'} in 7 days)", "",
        "## Campaign", campaign_block(d), "",
        "## The book", book_table(d), "",
        "## Reels (Instagram, latest reading)", reel_table(d)])


def brief(d):
    f, df = followers(d)
    reads = readings(d)
    posted = [r for r in d["reels"] if r["id"] in reads]
    last = max(posted, key=lambda r: r["posted_ist"], default=None)
    L = [f"Account: {f if f is not None else '–'} followers ({'+' if (df or 0) >= 0 else ''}{df if df is not None else '–'} this week)"]
    if last:
        s = reads[last["id"]][0]
        L[0] += (f" · latest reel {last['id']} ({last['story']}): {fmt(num(s['views']))} plays at {fmt(num(s['hours']))} h, "
                 f"skip {fmt(num(s['skip_rate']))}%, watched {fmt(num(s['watched_pct']))}%")
    opens = [x for x in book_rows(d) if x["bet"].get("status") == "open"]
    L.append("Book: " + " · ".join(f"{x['bet']['id']} {x['bet']['name']}: {label(x['bet']['metric'])} {fmt(x['value'])} "
                                    f"(target {fmt(x['bet']['target'])}, stop {fmt(x['bet']['stop'])}) {x['verdict']} {x['n']}/{x['bet']['min_reels']}"
                                    for x in opens) if opens else "Book: no open bets")
    every = [x["bet"]["id"] for x in opens if x["bet"].get("applies") == "every reel"]
    L.append("Today's reel carries: " + (", ".join(every) if every else "no standing bets") + " (docs/strategy.md, This week's plan)")
    return "\n".join(L)


PLAIN = {  # how each metric reads in an email: (name, unit)
    "skip_rate": ("swipe-aways in the first 3 s", "%"),
    "watched_pct": ("average watched", "%"),
    "sends_per_1k": ("shares per 1,000 plays", ""),
    "saves_per_1k": ("saves per 1,000 plays", ""),
    "likes_per_1k": ("likes per 1,000 plays", ""),
    "comments_per_1k": ("comments per 1,000 plays", ""),
    "views": ("plays per reel", ""),
    "credits_per_1k": ("credits per 1,000 plays", ""),
}
VERDICT_PLAIN = {"TARGET HIT": "hit its target, now standard", "STOP HIT": "hit its stop, dropped",
                 "TIME STOP": "no clear effect, closed", "WON": "won", "STOPPED": "stopped", "NO-EDGE": "no clear effect"}


def status(d):
    """Plain-English status for emails: no bet IDs, no file paths, no jargon."""
    f, df = followers(d)
    reads = readings(d)
    posted = [r for r in d["reels"] if r["id"] in reads]
    L = [f"{f if f is not None else '?'} followers ({'+' if (df or 0) >= 0 else ''}{df if df is not None else 0} this week)"]
    last = max(posted, key=lambda r: r["posted_ist"], default=None)
    if last:
        s = reads[last["id"]][0]
        bits = [f"{fmt(num(s['views']))} plays so far"]
        if num(s["skip_rate"]) is not None:
            bits.append(f"{num(s['skip_rate']):.0f}% swiped away in the first 3 s")
        if num(s["watched_pct"]) is not None:
            bits.append(f"watched {num(s['watched_pct']):.0f}% of the way")
        L.append(f"Last reel ({last['story']}): " + ", ".join(bits))
    opens = [x for x in book_rows(d) if x["bet"].get("status") == "open"]
    if opens:
        L.append("What every reel is testing:")
        for x in opens:
            b, m = x["bet"], x["bet"]["metric"]
            name, unit = PLAIN.get(m, (label(m), ""))
            now = x["value"] if x["value"] is not None else b.get("baseline")
            v = lambda n: "?" if n is None else (f"{n:.0f}" if unit == "%" else f"{n:g}") + unit
            where = VERDICT_PLAIN.get(x["verdict"], f"{x['n']} of {b['min_reels']} reels in")
            if x["value"] is None and x["carried"]:  # reels carry it, but none has a readable value yet
                L.append(f"- {b['name']}: {name} unknown yet (was {v(b.get('baseline'))}), target {v(b['target'])} ({where})")
                continue
            L.append(f"- {b['name']}: {name} {v(now)} now, target {v(b['target'])} ({where})")
    return "\n".join(L)


def replace_between(path, tag, body):
    s = open(path).read()
    a, b = f"<!-- {tag} -->", f"<!-- /{tag} -->"
    if a not in s or b not in s:
        raise SystemExit(f"{path}: markers {a} ... {b} missing")
    i, j = s.index(a) + len(a), s.index(b)
    open(path, "w").write(s[:i] + "\n" + body.strip() + "\n" + s[j:])


def write(d, now):
    head = ("# Performance log\n\n_Generated by `python3 pipeline/scoreboard.py write` on "
            f"{now:%Y-%m-%d %H:%M} IST. Edit registry/reels.csv, snapshots.csv, account.csv and bets.json, never this file._\n\n")
    open(P("registry", "performance.md"), "w").write(head + report(d) + "\n")
    replace_between(P("docs", "strategy.md"), "scoreboard",
                    f"_Updated {now:%Y-%m-%d %H:%M} IST by `scoreboard.py write`._\n\n" + campaign_block(d) + "\n\n" + book_table(d))


# ---------- data entry ----------
def ingest_ig(d, path, now):
    data = json.load(open(path))
    items = data.get("reels", []) if isinstance(data, dict) else data
    snaps = d["snaps"]
    linked = {r["ig_code"]: r["id"] for r in d["reels"] if r["ig_code"]}
    added, stray = 0, []
    for it in items:
        code = it.get("shortcode") or it.get("reelId")
        ts = datetime.fromisoformat(it["timestamp"].replace("Z", "+00:00")).astimezone(IST)
        hours = round((now - ts).total_seconds() / 3600, 1)
        row = dict(platform="instagram", code=code, posted_ist=f"{ts:%Y-%m-%d %H:%M}", taken_ist=f"{now:%Y-%m-%d %H:%M}",
                   hours=hours, views=it.get("playCount"), likes=it.get("likeCount"), comments=it.get("commentCount"),
                   shares=it.get("shares"), saves=it.get("saves"),
                   avg_watch_s=round(it["avgWatchTimeMs"] / 1000, 1) if it.get("avgWatchTimeMs") is not None else "",
                   watched_pct=round(it["avgWatchedPct"], 1) if it.get("avgWatchedPct") is not None else "",
                   skip_rate=it.get("skipRate"), length_s=it.get("durationSeconds"),
                   caption=(it.get("caption") or "").replace("\n", " ")[:120])
        row = {k: ("" if v is None else v) for k, v in row.items()}
        snaps[:] = [s for s in snaps if not (s["platform"] == "instagram" and s["code"] == code and abs((num(s["hours"]) or 0) - hours) < 1)]
        snaps.append(row); added += 1
        if code not in linked:
            stray.append(f"{code} posted {row['posted_ist']} \"{row['caption'][:50]}\" ({row['views']} plays)")
    snaps.sort(key=lambda s: (s["platform"], s["posted_ist"], s["code"], num(s["hours"]) or 0))
    write_csv(P("registry", "snapshots.csv"), SNAP_COLS, snaps)
    if isinstance(data, dict) and data.get("followersCount") is not None:
        d["acct"].append(dict(taken_ist=f"{now:%Y-%m-%d %H:%M}", platform="instagram", followers=data["followersCount"],
                              views_30d=(data.get("summary") or {}).get("views", "")))
        write_csv(P("registry", "account.csv"), ACCT_COLS, d["acct"])
    print(f"ingested {added} Instagram readings at {now:%Y-%m-%d %H:%M} IST")
    if stray:
        print("Not linked to a reel row yet. Match each to its episode (date, caption, topic) and run `scoreboard.py link <reel id> <code>`, "
              "or add-reel it with --bets none if it was posted outside the flow:")
        print("\n".join("  " + s for s in stray))


def link(d, reel_id, code, platform):
    key = "ig_code" if platform == "instagram" else "yt_id"
    r = next((r for r in d["reels"] if r["id"] == reel_id), None)
    if not r:
        raise SystemExit(f"no reel {reel_id} in registry/reels.csv")
    r[key] = code
    s = [s for s in d["snaps"] if s["platform"] == platform and s["code"] == code]
    if s:
        r["posted_ist"] = r["posted_ist"] or s[-1]["posted_ist"]
        r["length_s"] = r["length_s"] or s[-1]["length_s"]
    write_csv(P("registry", "reels.csv"), REEL_COLS, d["reels"])
    print(f"linked {reel_id} to {platform} {code}" + (f", posted {r['posted_ist']}" if r["posted_ist"] else ""))


def add_reel(d, a):
    if any(r["id"] == a.id for r in d["reels"]):
        raise SystemExit(f"reel {a.id} already exists")
    ids = {b["id"] for b in d["book"]["bets"]} | {"none", "pre"}
    bets = [b for b in re.split(r"[;, ]+", a.bets or "none") if b]
    bad = [b for b in bets if b not in ids]
    if bad:
        raise SystemExit(f"unknown bets {bad}; the book has {sorted(ids)}")
    d["reels"].append(dict(id=a.id, platform="instagram", ig_code="", yt_id="", posted_ist="", format=a.format, story=a.story,
                           bets=";".join(bets), length_s=a.length or "", outfit=a.outfit or "", desk_score=a.desk_score or "",
                           credits=a.credits or "", notes=a.notes or ""))
    write_csv(P("registry", "reels.csv"), REEL_COLS, d["reels"])
    print(f"added reel {a.id} carrying {';'.join(bets)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", nargs="?", default="report", choices=["report", "brief", "status", "write", "ingest-ig", "link", "add-reel"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--root"); ap.add_argument("--now"); ap.add_argument("--platform", default="instagram")
    for f in ("id", "format", "story", "bets", "length", "outfit", "desk-score", "credits", "notes"):
        ap.add_argument("--" + f)
    a = ap.parse_args()
    if a.root:
        ROOT = os.path.abspath(a.root)
    now, d = now_ist(a.now), load()
    if a.cmd == "report":
        print(report(d))
    elif a.cmd == "brief":
        print(brief(d))
    elif a.cmd == "status":
        print(status(d))
    elif a.cmd == "write":
        write(d, now); print("wrote registry/performance.md and the book in docs/strategy.md")
    elif a.cmd == "ingest-ig":
        ingest_ig(d, a.args[0], now)
    elif a.cmd == "link":
        link(d, a.args[0], a.args[1], a.platform)
    elif a.cmd == "add-reel":
        add_reel(d, a)
