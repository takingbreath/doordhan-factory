#!/usr/bin/env python3
"""Is a story hot, rising, flat or cold? Trend signals for news-desk candidates, from sources that need no login.
We're traders: ride the trend while it's still rising, and bring a sharper angle to a story everyone has already covered.
Usage: trends.py "bank strike|बैंक हड़ताल" "nifty losing streak|सेंसेक्स गिरावट" ...
  One argument per candidate; separate alternative search phrases with |, English first.
Signals per candidate:
  news    Google News articles in the last 1 and 7 days, and the share of the week that landed today (momentum).
          The feed caps at 100, so 100/100 means saturated.
  gtrends whether any phrase word appears in Google Trends' daily trending searches for India, with the volume.
  youtube videos uploaded this week on the first phrase: count (and how many in 24h), total views, best views/hour.
vidIQ (the connector) adds keyword volume and competition, trending videos and outliers; use it on the shortlist.
Calibrated 2026-09-25: bank strike = news 100/100 (saturated), "बैंक" trending 5000+, today's YouTube videos to 162K views."""
import json, re, sys, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"


def get(url, timeout=20):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-IN,en;q=0.9,hi;q=0.8"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", "replace")
    except Exception as e:
        return f"__ERROR__ {e}"


def news_count(q, window):
    x = get("https://news.google.com/rss/search?" + urllib.parse.urlencode(
        {"q": f"{q} when:{window}", "hl": "en-IN", "gl": "IN", "ceid": "IN:en"}))
    return None if x.startswith("__ERROR__") else x.count("<item>")


def trending_india():
    x = get("https://trends.google.com/trending/rss?geo=IN")
    items = re.findall(r"<item>(.*?)</item>", x, re.S)
    out = []
    for it in items:
        t = re.search(r"<title>(.*?)</title>", it)
        tr = re.search(r"<ht:approx_traffic>(.*?)</ht:approx_traffic>", it)
        news = " ".join(re.findall(r"<ht:news_item_title>(.*?)</ht:news_item_title>", it))
        out.append((t.group(1) if t else "", tr.group(1) if tr else "", news))
    return out


def hours_ago(s):
    m = re.match(r"(\d+)\s+(second|minute|hour|day|week)", s or "")
    if not m:
        return None
    n, u = int(m.group(1)), m.group(2)
    return n * {"second": 1 / 3600, "minute": 1 / 60, "hour": 1, "day": 24, "week": 168}[u]


STOP = {"india", "indian", "news", "today", "week", "weeks", "market", "price", "share", "shares", "stock", "stocks",
        "rate", "rates", "latest", "update", "what", "with", "from", "this", "that", "will", "your", "after", "over"}


def youtube_search(q):
    """Videos uploaded this week on the query (YouTube's own 'this week' filter)."""
    x = get("https://www.youtube.com/results?" + urllib.parse.urlencode({"search_query": q, "sp": "EgIIAw=="}))
    vids = []
    for m in re.finditer(r'"videoRenderer":\{"videoId":"([\w-]{11})"', x):
        chunk = x[m.end():m.end() + 6000]
        title = re.search(r'"title":\{"runs":\[\{"text":"(.*?)"\}', chunk)
        when = re.search(r'"publishedTimeText":\{"simpleText":"(.*?)"', chunk)
        views = re.search(r'"viewCountText":\{"simpleText":"([\d,]+) views"', chunk)
        if not (title and when and views):
            continue
        h = hours_ago(when.group(1)); v = int(views.group(1).replace(",", ""))
        try:
            t = json.loads('"' + title.group(1) + '"')          # unescape \u0026 and friends
        except Exception:
            t = title.group(1)
        if h is not None:
            vids.append({"title": t, "hours": h, "views": v, "vph": v / max(h, 0.5)})
    return vids


def analyse(arg, trending):
    phrases = [p.strip() for p in arg.split("|") if p.strip()]
    q = " OR ".join(f'"{p}"' for p in phrases)
    n1, n7 = news_count(q, "1d"), news_count(q, "7d")
    words = {w.lower() for p in phrases for w in re.findall(r"\w{4,}", p)} - STOP
    # a trending search counts if its own title shares a distinctive word with the story, or its news headlines share two
    hits = [(t, tr) for t, tr, news in trending
            if words & {w.lower() for w in re.findall(r"\w{4,}", t)}
            or len(words & {w.lower() for w in re.findall(r"\w{4,}", news)}) >= 2]
    vids = youtube_search(phrases[0])
    top = max(vids, key=lambda v: v["vph"]) if vids else None
    fresh = [v for v in vids if v["hours"] <= 24]
    momentum = (n1 / n7) if n1 is not None and n7 else 0
    if hits or (top and top["vph"] > 3000 and top["hours"] <= 72):
        label = "HOT"
    elif momentum >= 0.35 and (n1 or 0) >= 10:
        label = "RISING"
    elif (n7 or 0) >= 10:
        label = "FLAT"
    else:
        label = "COLD"
    if n1 == 100 and n7 == 100:
        label += " (saturated: everyone has it; needs a sharper angle)"
    return {"story": phrases[0], "label": label, "news_1d": n1, "news_7d": n7, "momentum_pct": round(momentum * 100),
            "google_trending": hits[:3], "yt_week_videos": len(vids), "yt_week_views": sum(v["views"] for v in vids),
            "yt_today_videos": len(fresh), "yt_best_vph": round(top["vph"]) if top else 0,
            "yt_top": f'{top["title"][:70]} ({top["views"]:,} views in {top["hours"]:.0f}h)' if top else ""}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    trending = trending_india()
    with ThreadPoolExecutor(4) as ex:
        rows = list(ex.map(lambda a: analyse(a, trending), sys.argv[1:]))
    for r in rows:
        print(f"{r['label']:<8} {r['story']}")
        print(f"         news: {r['news_1d']} today / {r['news_7d']} this week ({r['momentum_pct']}% today)"
              f" | google trending: {', '.join(f'{t} {tr}' for t, tr in r['google_trending']) or 'no'}"
              f"\n         youtube this week: {r['yt_week_videos']} videos ({r['yt_today_videos']} in the last 24h),"
              f" {r['yt_week_views']:,} views, best {r['yt_best_vph']:,}/hr: {r['yt_top']}")
    print("\nTop Google trending searches in India right now:",
          "; ".join(f"{t} {tr}" for t, tr, _ in trending[:10]))
