#!/usr/bin/env python3
"""The morning desk's research, written once and rendered twice: a Markdown file in the repo (for the local agent)
and an HTML email (for Akhilesh's phone).

  desk_report.py research/desk/2026-10-08.json [--html work/desk/2026-10-08.html]

Reads the day's research JSON (shape: research/desk/2026-10-08.json), the story tracker (registry/story_tracker.json)
and `scoreboard.py status`, then writes:
  research/desk/<date>.md     the day's research, in full
  research/desk/LATEST.md     a copy of it, so the local agent always knows where to look
  research/desk/TRACKER.md    the tracker board (story_tracker.py md)
  <html>                      the email body (default work/desk/<date>.html; work/ is git-ignored)

Research only: what is happening, what reels others are making, the curiosity gap, scores and sources.
No hooks, no lines, no scripts: Akhilesh writes the script (2026-10-08). English only.
"""
import argparse, html, json, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import story_tracker  # noqa: E402

# ---------- palette: warm newsprint, one vermilion accent, labels colour-coded by heat ----------
PAGE, CARD, INK, MUTED, RULE, TINT = "#F3EEE4", "#FFFDF8", "#1C1A17", "#5E574D", "#E4DCCD", "#F7F1E6"
ACCENT = "#A8361C"
LABEL = {  # text, background
    "HOT": ("#FFFFFF", "#A8361C"), "RISING": ("#5A3B00", "#F6DFA8"),
    "FLAT": ("#3B4650", "#E3E7EA"), "COLD": ("#24506E", "#DCE9F2"), "-": ("#3B4650", "#E3E7EA")}
DIRECTION = {"rising": ("Rising", "#2F6B3A"), "steady": ("Steady", MUTED), "fading": ("Fading", "#A8361C"),
             "new": ("New today", MUTED)}
SERIF = "Georgia,serif"
SANS = "Arial,sans-serif"
DIVIDER = f'<tr><td style="padding:0 24px"><div style="height:1px;background:{RULE};line-height:1px;font-size:0">&nbsp;</div></td></tr>'


def e(s):
    return html.escape(str(s), quote=True)


def pill(label):
    fg, bg = LABEL.get(label.split()[0], LABEL["-"])
    return (f'<span style="display:inline-block;padding:3px 9px;border-radius:999px;background:{bg};color:{fg};'
            f'font:600 11px/1.3 {SANS};letter-spacing:.06em">{e(label.split()[0])}</span>')


def heading(text):
    return (f'<div style="font:700 12px/1.4 {SANS};letter-spacing:.08em;text-transform:uppercase;color:{MUTED};'
            f'margin:22px 0 8px">{e(text)}</div>')


def bullets(items):
    li = "".join(f'<li style="margin:0 0 9px">{e(i)}</li>' for i in items)
    return f'<ul style="margin:0;padding:0 0 0 20px;font:400 15px/1.55 {SANS};color:{INK}">{li}</ul>'


def score_strip(sc):
    cells = [("Momentum", sc["momentum"], 3), ("Stake", sc["stake"], 2), ("Shareability", sc["share"], 2),
             ("Gap", sc["gap"], 2), ("Clarity", sc["clarity"], 1)]
    tds = "".join(
        f'<td align="center" width="20%" style="padding:8px 2px;{"border-right:1px solid " + RULE if n != "Clarity" else ""}">'
        f'<div style="font:700 16px/1.2 {SANS};color:{INK}">{v}<span style="color:{MUTED};font-weight:400">/{m}</span></div>'
        f'<div style="font:400 11px/1.3 {SANS};color:{MUTED};margin-top:2px">{n}</div></td>' for n, v, m in cells)
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" '
            f'style="border:1px solid {RULE};border-radius:10px;border-collapse:separate;margin-top:14px">'
            f'<tr>{tds}</tr></table>')


def others_table(rows):
    out = []
    for r in rows:
        out.append(
            f'<tr><td style="padding:10px 0;border-top:1px solid {RULE}">'
            f'<a href="{e(r["url"])}" style="font:600 14px/1.45 {SANS};color:{INK};text-decoration:underline;'
            f'text-decoration-color:{RULE}">{e(r["who"])}</a>'
            f'<div style="font:400 14px/1.5 {SANS};color:{INK};margin-top:2px">{e(r["what"])}</div>'
            f'<div style="font:400 13px/1.5 {SANS};color:{MUTED};margin-top:2px">'
            f'<strong style="color:{INK}">{e(r["views"])}</strong> views &middot; {e(r["multiple"])} &middot; {e(r["date"])}</div>'
            f'</td></tr>')
    return f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">{"".join(out)}</table>'


def facts_list(facts):
    out = []
    for f in facts:
        out.append(
            f'<div style="padding:10px 0;border-top:1px solid {RULE}">'
            f'<div style="font:400 14px/1.55 {SANS};color:{INK}">{e(f["text"])}</div>'
            f'<a href="{e(f["url"])}" style="display:inline-block;margin-top:4px;font:600 13px/1.4 {SANS};color:{ACCENT};'
            f'text-decoration:underline">{e(f["source"])}</a></div>')
    return "".join(out)


def story_html(s):
    sc = s["score"]
    gaps = "".join(f'<p style="margin:0 0 10px;font:400 15px/1.55 {SANS};color:{INK}">{e(g)}</p>' for g in s["curiosity_gaps"])
    return f'''
<tr><td style="padding:28px 24px 8px">
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr>
    <td valign="top" width="40" style="padding-right:12px">
      <div style="width:34px;height:34px;border-radius:17px;background:{INK};color:#FFFFFF;text-align:center;font:700 16px/34px {SANS}">{e(s["id"])}</div>
    </td>
    <td valign="top">
      <div style="font:400 12px/1.4 {SANS};color:{MUTED}">{e(s["lane"])}</div>
      <h2 style="margin:4px 0 10px;font:700 22px/1.25 {SERIF};color:{INK};letter-spacing:-.01em">{e(s["title"])}</h2>
      <div>{pill(s["label"])} <span style="font:700 14px/1.3 {SANS};color:{INK};margin-left:8px">{sc["total"]}/10</span></div>
      <div style="font:400 13px/1.5 {SANS};color:{MUTED};margin-top:8px">{e(s["window"])}</div>
    </td></tr></table>
  {score_strip(sc)}
  {heading("What's happening")}
  {bullets(s["happening"])}
  {heading("The curiosity gap")}
  <div style="background:{TINT};border-radius:10px;padding:14px 16px 4px">{gaps}</div>
  {heading("How hot it is")}
  {bullets(s["measured"])}
  {heading("What others are making")}
  {others_table(s["others"])}
  <p style="margin:10px 0 0;font:italic 400 14px/1.55 {SANS};color:{MUTED}">{e(s["others_takeaway"])}</p>
  {heading("Facts and sources")}
  {facts_list(s["facts"])}
  {heading("Watch out") if s.get("watch_out") else ""}
  {bullets(s.get("watch_out", []))}
</td></tr>'''


def tracker_html(rows):
    body = []
    for r in rows:
        if r["status"] == "retired" and r["retired"]["date"] != story_tracker.today():
            continue
        name, colour = DIRECTION[r["direction"]]
        status = {"active": "", "made": f' &middot; made ({e(r["made_episode"])})', "retired": " &middot; dropped today"}[r["status"]]
        body.append(
            f'<tr><td style="padding:10px 8px 10px 0;border-top:1px solid {RULE};font:600 14px/1.4 {SANS};color:{INK}">{e(r["title"])}'
            f'<div style="font:400 12px/1.5 {SANS};color:{MUTED};margin-top:2px">Day {r["days"]}{status}'
            f'{" &middot; history " + e(r["history"]) if len(r["history"]) > 1 else ""}</div></td>'
            f'<td align="right" valign="top" style="padding:10px 0;border-top:1px solid {RULE};white-space:nowrap">{pill(r["label"])}'
            f'<div style="font:600 12px/1.5 {SANS};color:{colour};margin-top:4px">{name}</div></td></tr>')
    return f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">{"".join(body)}</table>'


def email_html(d, rows, standing):
    pick = d["pick"]
    link = d["session_link"]
    correction = (f'<tr><td style="padding:0 24px 20px"><div style="background:{TINT};border-radius:10px;padding:12px 16px;'
                  f'font:400 14px/1.55 {SANS};color:{INK}"><strong>Correction to this morning:</strong> {e(d["correction"])}</div></td></tr>'
                  if d.get("correction") else "")
    stories = DIVIDER.join(story_html(s) for s in d["stories"])
    wire = bullets([w["text"] for w in d.get("wire", [])])
    paras = [l for l in standing if not l.startswith("-")]
    tests = [l.lstrip("- ") for l in standing if l.startswith("-")]
    standing_lines = "".join(f'<p style="margin:0 0 8px;font:400 14px/1.55 {SANS};color:{INK}">{e(l)}</p>' for l in paras) + bullets(tests)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light">
<title>Doordhan desk, {e(d["date_label"])}</title></head>
<body style="margin:0;padding:0;background:{PAGE};-webkit-text-size-adjust:100%">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background:{PAGE}"><tr><td align="center" style="padding:20px 10px 40px">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width:620px;background:{CARD};border-radius:16px;border:1px solid {RULE}">
<tr><td style="padding:26px 24px 6px">
  <div style="font:700 13px/1.3 {SANS};letter-spacing:.14em;color:{ACCENT}">DOORDHAN DESK</div>
  <div style="font:400 13px/1.5 {SANS};color:{MUTED};margin-top:2px">{e(d["date_label"])} &middot; research for today's reel</div>
</td></tr>
<tr><td style="padding:14px 24px 20px">
  <h1 style="margin:0 0 8px;font:700 26px/1.2 {SERIF};color:{INK};letter-spacing:-.015em">My pick: story {e(pick["id"])}</h1>
  <p style="margin:0 0 8px;font:400 15px/1.55 {SANS};color:{INK}">{e(pick["reason"])}</p>
  <p style="margin:0 0 18px;font:400 14px/1.55 {SANS};color:{MUTED}">Runner-up: {e(pick["runner_up"])}</p>
  <a href="{e(link)}" style="display:inline-block;background:{INK};color:#FFFFFF;text-decoration:none;font:600 15px/1 {SANS};padding:14px 20px;border-radius:10px">Reply with a story number</a>
</td></tr>
{correction}
{DIVIDER}
{stories}
{DIVIDER}
<tr><td style="padding:26px 24px 8px">
  <h2 style="margin:0 0 4px;font:700 20px/1.25 {SERIF};color:{INK}">Stories we're tracking</h2>
  <p style="margin:0 0 6px;font:400 13px/1.5 {SANS};color:{MUTED}">Measured again every morning until they leave the news cycle (cold on two checks running, or past their window).</p>
  {tracker_html(rows)}
</td></tr>
{DIVIDER}
<tr><td style="padding:26px 24px 8px">
  <h2 style="margin:0 0 10px;font:700 20px/1.25 {SERIF};color:{INK}">Also on the wire</h2>
  {wire}
</td></tr>
{DIVIDER}
<tr><td style="padding:26px 24px 8px">
  <h2 style="margin:0 0 10px;font:700 20px/1.25 {SERIF};color:{INK}">Where we stand</h2>
  {standing_lines}
</td></tr>
<tr><td style="padding:24px 24px 28px">
  <a href="{e(link)}" style="display:inline-block;background:{INK};color:#FFFFFF;text-decoration:none;font:600 15px/1 {SANS};padding:14px 20px;border-radius:10px">Reply with a story number</a>
  <p style="margin:12px 0 0;font:400 12px/1.5 {SANS};color:{MUTED}">The full research is also in the repo at research/desk/{e(d["date"])}.md (and LATEST.md).</p>
</td></tr>
</table></td></tr></table></body></html>'''


def compact(doc):
    """Email pass. Gmail (sending through its API) strips <head>, <style>, class attributes and the CSS `background`
    shorthand (checked 2026-10-08), so every style stays inline, colours use background-color plus a bgcolor attribute,
    and only the whitespace between tags goes."""
    import re
    doc = re.sub(r"\n\s*", "", doc)
    doc = re.sub(r"background:(#[0-9A-Fa-f]{6})", r"background-color:\1", doc)
    return re.sub(r'<(td|table)([^>]*?)style="([^"]*?)background-color:(#[0-9A-Fa-f]{6})',
                  r'<\1\2bgcolor="\4" style="\3background-color:\4', doc)


def md(d, rows, standing):
    L = [f"# Doordhan desk research — {d['date_label']}", "",
         f"Session: {d['session_link']}", "",
         f"**Pick: story {d['pick']['id']}.** {d['pick']['reason']}", "", f"Runner-up: {d['pick']['runner_up']}", ""]
    if d.get("correction"):
        L += [f"> **Correction:** {d['correction']}", ""]
    for s in d["stories"]:
        sc = s["score"]
        L += [f"## {s['id']}. {s['title']}", "",
              f"{s['lane']} · {s['label']} · **{sc['total']}/10** (momentum {sc['momentum']}/3, stake {sc['stake']}/2, "
              f"shareability {sc['share']}/2, gap {sc['gap']}/2, clarity {sc['clarity']}/1) · tracker id `{s['tracker_id']}`", "",
              f"Window: {s['window']}", "", "### What's happening"]
        L += [f"- {x}" for x in s["happening"]]
        L += ["", "### The curiosity gap"] + [f"- {x}" for x in s["curiosity_gaps"]]
        L += ["", "### How hot it is"] + [f"- {x}" for x in s["measured"]]
        L += ["", "### What others are making", "", "| Who | What | Views | vs usual | When |", "|---|---|---|---|---|"]
        L += [f"| [{o['who']}]({o['url']}) | {o['what']} | {o['views']} | {o['multiple']} | {o['date']} |" for o in s["others"]]
        L += ["", f"_{s['others_takeaway']}_", "", "### Facts and sources"]
        L += [f"- {f['text']} — [{f['source']}]({f['url']})" for f in s["facts"]]
        if s.get("watch_out"):
            L += ["", "### Watch out"] + [f"- {x}" for x in s["watch_out"]]
        L.append("")
    L += ["## Stories we're tracking", "", "Full board: research/desk/TRACKER.md", "",
          "| Story | Now | Direction | Day | Status |", "|---|---|---|---|---|"]
    L += [f"| {r['title']} (`{r['id']}`) | {r['label']} | {r['direction']} | {r['days']} | {r['status']} |"
          for r in rows if r["status"] != "retired"]
    L += ["", "## Also on the wire"] + [f"- {w['text']}" for w in d.get("wire", [])]
    L += ["", "## Where we stand", ""] + [l if l.startswith("-") else l + "  " for l in standing]
    return "\n".join(L) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("research_json")
    p.add_argument("--html")
    a = p.parse_args()
    with open(a.research_json) as f:
        d = json.load(f)
    db = story_tracker.load()
    rows = story_tracker.board_rows(db)
    standing = subprocess.run([sys.executable, os.path.join(ROOT, "pipeline", "scoreboard.py"), "status"],
                              capture_output=True, text=True, cwd=ROOT).stdout.strip().splitlines()
    out_dir = os.path.join(ROOT, "research", "desk")
    os.makedirs(out_dir, exist_ok=True)
    md_path = os.path.join(out_dir, f"{d['date']}.md")
    with open(md_path, "w") as f:
        f.write(md(d, rows, standing))
    shutil.copyfile(md_path, os.path.join(out_dir, "LATEST.md"))
    story_tracker.cmd_md(db, None)
    html_path = a.html or os.path.join(ROOT, "work", "desk", f"{d['date']}.html")
    os.makedirs(os.path.dirname(html_path), exist_ok=True)
    with open(html_path, "w") as f:
        f.write(compact(email_html(d, rows, standing)))
    print(f"wrote {os.path.relpath(md_path, ROOT)}, research/desk/LATEST.md and {os.path.relpath(html_path, ROOT)}")


if __name__ == "__main__":
    main()
