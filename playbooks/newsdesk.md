# Playbook: news desk

_This is the path that has worked so far. Change it whenever you find a better way, and note what you changed in registry/episodes.md._

Goal: three story options Akhilesh can pick from in 30 seconds, each graded on how likely it is to travel.
**The desk does research, not writing** (Akhilesh, 2026-10-08). For each story it reports:
- what exactly is going on;
- what other creators are making on it, and which of their reels perform best;
- the curiosity gap.

No hooks, no "line worth sending", no script: Akhilesh writes those. Everything is in English (no Hinglish or Hindi).
**We're traders: we ride the trend.** Get in while a story is rising. A story everyone has already covered needs a sharper angle. And some of the best reels are well-researched stories the audience never read (Akhilesh, 2026-09-25).

## Two lanes
- **Hot lane (two options):** what people are searching for, watching and sharing right now.
- **Deep lane (one option):** a story from well-researched journalism (list in docs/sources.md) that most of our viewers haven't read, often behind a paywall. We use the headline and the public facts, verify everything ourselves from open sources, never copy paywalled text, and credit the outlet in the caption ("via The Ken") when the story is theirs.

## Steps
1. Get today's date from the system clock (do not trust injected dates).
2. `git pull` first (the tracker and yesterday's research live in the repo). Then read CLAUDE.md (rested topics, hard rules), docs/strategy.md (the open bets and "This week's plan"), registry/episodes.md (topics already made), docs/learnings.md (the strategist's "Ride now" and "This week" notes: follow-ups on reels that are taking off come first) and docs/platform-playbook.md. `python3 pipeline/scoreboard.py brief` gives three lines on where we stand; they go at the top of the email.
3. **Re-measure the tracked stories first:** run `python3 pipeline/story_tracker.py check`.
   - Every story the desk has sent stays on the board (registry/story_tracker.json) until it leaves the news cycle: COLD on two checks running, or past its window. Deep-lane stories go only at their window.
   - A tracked story that is rising, or has a new turn today, competes for today's three slots on equal terms with new candidates. If it wins a slot, say what's new since we last sent it.
   - Tracked stories that don't win a slot still appear on the board in the email, with their direction.
4. **Gather about ten new candidates:**
   - Web searches across markets, big stock movers, IPOs and listings, SEBI and RBI, tax, banks and salaries, gold and fuel, big company events, viral money stories (last 48 hours).
   - **Big stock movers (Akhilesh, 2026-09-26: people always want to know why a stock crashed or flew):** the biggest one-day and one-week gainers and losers among well-known listed companies (Nifty 500, recent IPOs, household brands). Search e.g. "top losers this week", "shares crash", "stock zooms", and keep any move of about 10% or more in a day, or 20% or more in a week, with a clear cause. The reel explains why it moved and what to watch next, never whether to buy or sell. Mind the SEBI price-data rule in docs/platform-playbook.md: report the move as news, with no price chart, price levels, targets or analyst ratings.
   - Google Trends India: the bottom line of `pipeline/trends.py` lists what India is searching for right now.
   - vidIQ connector: trending videos and outliers (videos far outperforming their channel's usual views) in Indian finance and business this week. Outliers show what is breaking out before the news catches up.
   - Deep lane: `python3 pipeline/deep_leads.py` gives the last 7 days of headlines from the top eight sources in docs/sources.md (The Ken, The Morning Context, SEBI orders, Moneylife, ET Prime, Reuters exclusives, The Arc, The Core).
5. **Filter out** rested topics, anything that would need a buy/sell call, and topics already made, unless there's a genuinely new turn.
6. **Measure** every surviving candidate: `python3 pipeline/trends.py "<english phrase>|<hindi phrase>" ...`. It labels each one HOT, RISING, FLAT or COLD, from Google Trends, Google News momentum (the share of the week's coverage that landed today) and YouTube this week (videos, views, best views per hour). On the top five, run vidIQ keyword research: search volume, competition and trend direction.
7. **Grade each candidate out of 10:**

   | Factor | Points | What earns them |
   |---|---|---|
   | Momentum | 0–3 | 3 HOT (trending on Google, or a video on it gaining ≥3,000 views/hour within 72 h); 2 RISING (≥35% of the week's coverage came today, or uploads are accelerating); 1 FLAT; 0 COLD or fading. The deep lane can score 0 here. |
   | Stake | 0–1 | Hits the viewer's money as an investor, now or some day (1), abstract (0). Our viewers watch for investing stories: everyday banking chores (a bank strike, a holiday, branch timings) score 0 here however hot they are (Akhilesh, 2026-09-26). |
   | Shareability | 0–2 | Makes someone send it to a friend: outrage at the system, a surprising number, relatable pain, an "I told you so". |
   | Gap | 0–2 | Plenty of interest but few good Hinglish shorts on it (vidIQ competition low, few Shorts), or a deep-lane story nobody has made yet. 0 if everyone has already posted the same angle. |
   | Known name | 0–2 | 2: a company, brand or person every viewer already knows can be named or shown in frame one (a logo, a licensed photo, their real footage) with one number or question that lands in two seconds. 1: no known name, but one number or image that lands in two seconds. 0: neither. (Strategist, 2026-10-11: all four reels that opened on a known name reached 582–3,224 plays, all eight that didn't stayed at 94–303; stake was worth less than it scored: Nana Patekar's story had no investor stake and is our best reel.) |

   In the research JSON the score keys are `momentum`, `stake`, `share`, `gap` and `name` (Known name; files before 2026-10-11 used `clarity`, out of 1, and `stake` out of 2, and still render).

   Also note the **window**: until when the story stays relevant, e.g. "post by Sun 27 Sep; the strike starts Monday".
8. **Find what others are making** on each of the top five:
   - vidIQ `vidiq_instagram_tiktok_outlier_search` (Indian audience, the last two weeks);
   - `vidiq_youtube_search` (Shorts, ordered by views, region IN);
   - `vidiq_trending_videos`.

   For the best-performing reels on the topic (and the closest adjacent topics when nothing on the topic itself broke out), record:
   - the creator;
   - what the reel did (its angle and format);
   - views;
   - how far above the creator's usual it ran;
   - when it was posted;
   - the link.

   End with one line on what's missing: the angle nobody has taken.
9. **Name the curiosity gap** for each story: why a viewer would stop and want to know. Usually it's a famous name or brand with an unknown inside, a number that doesn't add up, or a question nobody has answered yet. Example (Snapdeal, E8): a Shark Tank judge's company, a brand everyone used once and then stopped hearing about, is suddenly listing, and nobody knows what it does now. Give one to three gaps, each in one or two plain sentences.
10. **Pick** the top two from the hot lane and the best one from the deep lane, in different shapes (e.g. wallet hit, market move, rule or company story). Recommend one.
11. **Verify the facts:** open each source page and confirm every number is on it. A source older than a week can give context, marked as context, but never the story's headline number. When sources disagree, give the newest figure, and say that the earlier one differed.
12. **Write it up and send it:**
    - Write the day's research JSON in `research/desk/<date>.json` (the shape of `research/desk/2026-10-08.json`).
    - `python3 pipeline/story_tracker.py add ...` for each new story sent, and `score --id ... --score N` for each story graded today.
    - `python3 pipeline/desk_report.py research/desk/<date>.json` writes `research/desk/<date>.md`, `LATEST.md` and `TRACKER.md`, plus the HTML email in `work/desk/`.
    - Send the email as HTML through a Gmail draft, checked before sending (routines/email-style.md).
    - Commit `research/desk/` and `registry/story_tracker.json` and push them to main, so Akhilesh's local agent can read the research with `git pull`.
13. End with: "Reply with a story number, e.g. 1."

## Learning loop
Every reel's desk score goes into registry/reels.csv when the episode is recorded (`scoreboard.py add-reel --desk-score`). The strategist routine records its numbers nightly and, once a month, compares the desk's scores with what actually travelled and adjusts the weights above. The desk should get better at calling winners every week.
