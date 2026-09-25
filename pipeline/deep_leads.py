#!/usr/bin/env python3
"""Deep-lane leads: the last N days of headlines from the research-journalism sources in docs/sources.md.
Usage: deep_leads.py [--days 7] [--per 8]
Prints newest first per source: date, headline and link. Headlines are leads only; research the facts from open sources."""
import argparse, email.utils, html, re, time, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"


def gn(q):
    return "https://news.google.com/rss/search?" + urllib.parse.urlencode(
        {"q": q + " when:7d", "hl": "en-IN", "gl": "IN", "ceid": "IN:en"})


SOURCES = [
    ("The Ken", gn("site:the-ken.com"), None),
    ("The Morning Context", gn("site:themorningcontext.com"), None),
    ("SEBI orders and board decisions", "https://www.sebi.gov.in/sebirss.xml", ("/enforcement/orders/", "/press-releases/")),
    ("Moneylife", gn("site:moneylife.in"), None),
    ("ET Prime", "https://economictimes.indiatimes.com/prime/rssfeeds/69891145.cms", None),
    ("Reuters India exclusives", gn("site:reuters.com India (exclusive OR insight)"), None),
    ("The Arc", "https://www.thearcweb.com/rss.xml", None),
    ("The Core", "https://www.thecore.in/feed", None),
]


def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8", "replace")
    except Exception as e:
        return f"__ERROR__ {e}"


def parse_date(s):
    s = (s or "").strip()
    try:
        w = email.utils.parsedate_to_datetime(s)
    except Exception:
        w = None
    if w is None:
        for fmt in ("%d %b, %Y %z", "%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S%z"):
            try:
                w = datetime.strptime(s, fmt); break          # SEBI: "24 Sep, 2026 +0530"; The Arc: "2026-09-25 02:30:00.0"
            except ValueError:
                continue
    if w is not None and w.tzinfo is None:
        w = w.replace(tzinfo=timezone(timedelta(hours=5, minutes=30)))
    return w


def clean(t):
    t = html.unescape(t.replace("<![CDATA[", "").replace("]]>", "")).strip()
    return re.sub(r"\s+-\s+(The Ken|The Morning Context|Moneylife|Reuters)$", "", t)


def items(xml):
    for it in re.findall(r"<item>(.*?)</item>", xml, re.S):
        t = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", it, re.S)
        l = re.search(r"<link>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</link>", it, re.S)
        d = re.search(r"<pubDate>(.*?)</pubDate>", it, re.S)
        when = parse_date(d.group(1)) if d else None
        yield (clean(t.group(1)) if t else "", clean(l.group(1)) if l else "", when)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--days", type=int, default=7); ap.add_argument("--per", type=int, default=8)
    a = ap.parse_args()
    cutoff = datetime.now(timezone.utc) - timedelta(days=a.days)
    for i, (name, url, must) in enumerate(SOURCES):
        if i:
            time.sleep(3)                      # cloud IPs get throttled by Google News
        x = fetch(url)
        if x.startswith("__ERROR__") or "Just a moment" in x[:2000]:
            print(f"\n## {name}: unavailable ({x[:80]})"); continue
        seen, rows = set(), []
        for t, l, w in items(x):
            key = re.sub(r"\W", "", t.lower())
            if (not w or w < cutoff or key in seen or t.startswith("Tag |") or "Financial Magazines online" in t
                    or (must and not any(m in l for m in must))):
                continue
            seen.add(key); rows.append((t, l, w))
        rows.sort(key=lambda r: r[2], reverse=True)
        print(f"\n## {name} ({len(rows)} in {a.days} days)")
        for t, l, w in rows[:a.per]:
            print(f"- {w:%d %b} {t}\n  {l}")
