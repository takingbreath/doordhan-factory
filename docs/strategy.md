# Doordhan strategy: how we trade for growth

**The goal is to grow the account** (Instagram now; YouTube Shorts once the channel exists). Everything else serves that.
We run it like a trading desk: form a strategy, execute it, read the results, refine. Every change is a bet with a target and a stop loss. One reel proves nothing, but we never keep building on a losing strategy (Akhilesh, 2026-09-25).

**Growth at any cost** means any effort, any idea, any format, any number of experiments. The one thing we never spend is the account itself. That rules out:
- breaking the hard rules in CLAUDE.md;
- breaking the platform rules in docs/platform-playbook.md;
- faking engagement (bought followers or views, engagement pods, follow/unfollow, bots).

Those get an account restricted or quietly demoted, and that is the one loss we can't trade our way back from.

## How we trade
1. **Every change is a bet**, written in registry/bets.json before the first reel carries it. Each bet has:
   - one lever;
   - one metric;
   - the baseline it opened at;
   - a target;
   - a stop;
   - how many reels it needs before we judge it, and the most we'll give it.
2. **We judge on rates, not luck.** The rates are skip rate, watched %, and sends, saves and likes per 1,000 plays, pooled over all the reels carrying the bet. Play counts are compared only at 72 hours. `pipeline/scoreboard.py` does the arithmetic and gives the verdict.
3. **Target hit: press it.** The lever becomes the default in the playbooks, and we make more reels in that vein, including follow-ups. Let winners run.
4. **Stop hit: cut it the same night.**
   - Undo the lever and write down why in docs/learnings.md.
   - No averaging down: a losing bet doesn't get more reels in the hope it turns.
   - A stop kills the trade, not necessarily the idea. Re-enter only with a different execution, under a new bet ID.
5. **Time stop.** If a bet reaches its maximum number of reels with neither target nor stop hit, close it as "no edge" and keep whichever option is simpler and cheaper.
6. **An execution miss is not a loss.** If a reel didn't actually carry the lever (for example, the hook text was dropped), take it out of the bet before judging.
7. **Position limits.**
   - At most 3 open bets, each on a different lever and judged on a different metric, so we know what caused what.
   - Every reel carries every bet marked "every reel".
   - "Watch" items are tracked but not traded until they can be separated from the open bets.
8. **Credits are our capital.** Every reel records what it cost, and the book tracks credits per 1,000 plays. The budgets in CLAUDE.md stand. When a winning bet needs more capital, the strategist asks for it with the numbers.
9. **Fix the funnel in order: stop, hold, share, follow.**
   - Stop: skip rate.
   - Hold: watched %.
   - Share: sends and saves.
   - Follow: new followers.

   The next bet goes on the weakest stage. There's no point perfecting the share line while 60% leave in the first 3 seconds.
10. **The account has its own stop.** Each campaign stage has targets and a strategy-level stop. When that stop hits, we don't tweak; we change strategy.

## The campaign
Stage 1 targets are live in the block below. Stages 2 and 3 are the plan after that, and the monthly review resets all of them. Every number is an opening proposal that Akhilesh can change.
- **Stage 1: Stop the scroll (26 Sep to 11 Oct).** Skip rate at or below 45%, watched at or above 45%, median plays at 72 h of 500 or more, one reel above 2,000 plays, 100 followers.
  - Strategy stop: after 10 reels, median plays still under 300.
- **Stage 2: Make it travel (12 Oct to 1 Nov).** Sends per 1,000 plays of 10 or more, one reel above 10,000 plays, 500 followers.
  - Likely levers: series and follow-ups on winners, formats built to be forwarded, Trial Reels.
- **Stage 3: Build the habit (Nov to Dec).** 2,000 followers by 31 Dec, viewers coming back for a recurring series, and YouTube Shorts live.

## The book and where we stand
<!-- scoreboard -->
_Updated 2026-09-30 21:32 IST by `scoreboard.py write`._

**Stage 1: Stop the scroll** (2026-09-26 to 2026-10-11): prove people stop for our reels and stay to the end

- skip rate %: now 57.2, target 45 → not yet
- watched %: now 38.4, target 45 → not yet
- median plays at 72 h: now 1268, target 500 → on target
- best reel's plays: now 2392, target 2000 → on target
- followers: now 71, target 100 → not yet
- strategy stop: 4/10 reels posted this stage; median plays at 72 h now 1268, must reach 300

| Bet | Lever | Judged on | Baseline | Now | Target | Stop | Reels (judged/carried) | Verdict |
|---|---|---|---|---|---|---|---|---|
| B1 Hook in frame one | Frame 1: the anchor looks into the lens, already saying the viewer's stake; the hook in 6 big words or fewer on screen; nothing (Namaskar, title, logo) before it; a cut or punch-in by 1 s; cover = frame 1 | skip rate % | 60.7 | 55.7 | 45 | 58 | 1/1 (judge at 3, max 6) | **HOLD** 1/3 reels |
| B2 Tight 20-30 s | 20-30 s total; title montage 1.5 s or less and only after the hook; payoff by 20 s; the last line echoes the hook so a replay feels natural; no dead air | watched % | 26.3 | 39.7 | 45 | 32 | 1/1 (judge at 3, max 6) | **HOLD** 1/3 reels |
| B3 A line worth sending | Every script lands one line a viewer would forward to a specific person (a number to remember, a jab at the system, an 'I told you so'); never ask for shares | sends per 1k plays | 2.6 | 0 | 8 | 2 | 1/2 (judge at 4, max 6) | **HOLD** 1/4 reels |
| W1 Glam Sarika | Sarika in the glam wardrobe (formats/samachar.md) on every Samachar reel | skip rate % | 66.9 | 55.7 | – | – | 1/1 (judge at 3, max 6) | **WATCH** tracked; judged at the monthly review |
<!-- /scoreboard -->

## This week's plan
_Written by the strategist every Sunday. The morning session executes it: each story option says which bets it carries, and each script says how it carries them._

**Week of Mon 28 Sep (written Sun 27 Sep)**
- **Every reel carries all three open tests, as written:** hook in frame one (skip rate), tight 20–30 s (watched %), a line worth sending (sends per 1k).
  - **Hook, sharpened (same lever, better execution):** make the on-screen hook the number the story turns on: the rupee or % hit, in 6 big words or fewer ("₹4 lakh crore saaf, ek din mein", "36% gira. Kyun?"). Our best reel did exactly this (Policybazaar "−36%: KYUN?", 2,331 plays, 10× the others), and so did four other creators who took the same story to 1.2M–6.5M plays.
  - **Length:** 30 s cap, payoff by 20 s, last line echoes the hook. The tax-audit reel hit exactly 30 s.
  - **Sendable line:** keep it. Policybazaar's shares are unknown for now (the owner feed froze at 270 plays with 3 shares).
- **Ride now:** a follow-up to the IRDAI commission-cap story from the viewer's stake ("Agent ka commission kata. Aapka premium sasta hoga?"): check the draft's status and dates first; no product advice. Then keep big stock movers with a clear cause (roughly 10%+ in a day) as the desk's first source.
- **Volume and slot:** one reel a day, 7 days (the desk runs daily), posted 7–9 pm IST. Two of four reels so far went up in the morning. Trial Reel whenever the option shows.
- **Log every reel before it posts:** `scoreboard.py add-reel` with bets, credits and desk score, and the script and contact sheet in the repo. The tax-audit reel skipped this, so it can't count toward the tests yet.
- **Every night, cross-check plays against the public count** (vidiq_ig_profile_reels, 5 credits): the owner feed froze on Policybazaar at 270 plays while the public count was 2,331.
- **Watching:** the tax-audit reel at 72 h; glam Sarika against the other formats (monthly review, 4 Oct).

## Working rhythm
| When | Who | What |
|---|---|---|
| Every day 7:30 IST | Morning session (cloud) | Desk email. The top three lines are the scoreboard brief: where we stand and what today's reel carries. Then three stories, each tagged with the bets it serves. |
| Morning | Akhilesh | Picks a story (30 s). |
| Midday | Session, then Akhilesh | Script, with the bets it carries and how. Akhilesh approves (2 min). |
| Afternoon | Session, then Akhilesh | Final with QC notes. Akhilesh approves (2 min). |
| 7–9 pm IST | Akhilesh | Posts with the posting kit (5 min). |
| Nightly 21:30 IST | Strategist (cloud) | Records every reel's numbers and checks every target and stop, acting the same night. Pings the phone only on a stop, a target or a reel taking off. |
| Sunday 21:30 IST | Strategist | Weekly review email: the account, the book (each bet's result), what we learned, next week's plan, and yes/no decisions. Akhilesh replies in that session. |
| First Sunday of the month | Strategist | Campaign review: stage targets, whether the desk's scores predict plays, the strategy-level stop, pivots. |
| Weekly | Akhilesh | Instagram → Settings → Account Status (1 min; only the app shows it). |

**The strategist decides alone:**
- opening, pressing, stopping and closing bets within the hard rules, the budgets, and the existing formats and looks;
- rewriting the playbooks and this week's plan;
- the story grading weights and the posting plan.

**It asks Akhilesh first about:**
- anything touching the hard rules;
- spending over budget;
- a change to Sarika's look;
- a brand-new format;
- changing a campaign target.

## Decision log
- 2026-09-25:
  - Book opened: B1 hook in frame one, B2 tight 20–30 s, B3 a line worth sending, plus W1 (glam Sarika) on watch.
  - Baselines come from E1 and E2: skip rate 60.7%, watched 26.3%, 2.6 sends per 1,000 plays.
  - Stage 1 campaign set.
- 2026-09-27 (weekly review):
  - Book unchanged: all three bets HOLD on 1 judged reel each (need 3–4). No new bet: the weakest stage is still the stop (skip 54.8%, target 45%), which the hook bet already covers, and the book is full at 3.
  - Hook execution sharpened inside the same lever: lead with the story's number on screen (outlier evidence: 4 of 4 viral IRDAI reels did).
  - Policybazaar reel is taking off by the plays rule: 2,331 plays (public count) vs a median of ~240 for the others. The first report said 259; vidIQ's owner feed had frozen for that reel. Corrected the same night after Akhilesh flagged it. It also hits the stage target of one reel above 2,000 plays.
  - scoreboard.py: a public reading (no shares or saves) counts as unknown, not zero, for sends and saves per 1k.
  - Tax-audit reel (E4) recorded with no bets: made outside the logged flow; no script, contact sheet or credits in the repo. Re-tag once confirmed.
  - Posting plan: one reel a day, 7–9 pm IST.
- 2026-09-28 (nightly):
  - vidIQ owner insights failed at 21:31 ("Meta token is inactive") although the account list said the token was active. Akhilesh reconnected Instagram in vidIQ; owner insights back at 21:49 (70 followers). The interim public readings were replaced by owner readings, except Policybazaar: the owner feed still shows 316 plays against 2,381 public, so its public reading stays the latest.
  - E5 (Sahayata Kendra debut, posted 19:58) linked to Dd1Y8EaSkJ7. A UPI reel ("96% UPI ABHI BHI FREE", 25 s, posted 12:44) went up outside the flow: logged as X1 with no bets.
  - No stop or target hit; all bets HOLD.
- 2026-09-29 (nightly):
  - No stop or target hit; all bets HOLD (B1 and B2 on 1 judged reel, B3 on 1 of 4). No reel posted on 29 Sep. Followers 70 (flat on the day).
  - Policybazaar's owner feed still frozen (323 plays vs 2,388 public); public reading logged. scoreboard.py now takes the higher of same-hour readings as a reel's 72 h plays, so a frozen owner feed no longer understates it. The stage's "median plays at 72 h" rests on that one reel until the tax-audit reel matures tomorrow.
  - Sahayata Kendra debut (67 s) worsened as it reached non-followers: skip 44% → 68%, watched 26% → 17.5% at 214 plays. Evidence for the length rule; judge the format at the weekly review.
- 2026-09-30 (nightly):
  - No stop or target hit; all bets HOLD (B1 and B2 on 1 judged reel, B3 on 1 of 4). Followers 71 (+1). No reel posted on 29 or 30 Sep: two days off the one-a-day plan, and the bets can't move without reels.
  - Tax-audit reel (E4) matured at 72 h: 148 plays, skip 61.2%, watched 41.3%, 2 sends (13.5 per 1k). Stage median plays at 72 h now 1,268 (E3 and E4). Policybazaar owner feed still frozen (327 vs 2,392 public); public reading logged.
