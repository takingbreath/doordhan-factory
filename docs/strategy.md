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
- **Stage 1: Stop the scroll (26 Sep to 25 Oct; extended from 11 Oct by Akhilesh, 4 Oct).** Skip rate at or below 45%, watched at or above 45%, median plays at 72 h of 500 or more, one reel above 2,000 plays, 100 followers.
  - Strategy stop: after 20 reels (was 10), median plays still under 300.
- **Stage 2: Make it travel (26 Oct to 15 Nov).** Sends per 1,000 plays of 10 or more, one reel above 10,000 plays, 500 followers.
  - Likely levers: series and follow-ups on winners, formats built to be forwarded, Trial Reels.
- **Stage 3: Build the habit (Nov to Dec).** 2,000 followers by 31 Dec, viewers coming back for a recurring series, and YouTube Shorts live.

## The book and where we stand
<!-- scoreboard -->
_Updated 2026-10-07 21:32 IST by `scoreboard.py write`._

**Stage 1: Stop the scroll** (2026-09-26 to 2026-10-25): prove people stop for our reels and stay to the end

- skip rate %: now 56, target 45 → not yet
- watched %: now 29.8, target 45 → not yet
- median plays at 72 h: now 148, target 500 → not yet
- best reel's plays: now 2412, target 2000 → on target
- followers: now 210, target 100 → on target
- strategy stop: 9/20 reels posted this stage; median plays at 72 h now 148, must reach 300

| Bet | Lever | Judged on | Baseline | Now | Target | Stop | Reels (judged/carried) | Verdict |
|---|---|---|---|---|---|---|---|---|
| B1 Hook in frame one | Frame 1: the anchor looks into the lens, already saying the viewer's stake; the hook in 6 big words or fewer on screen; nothing (Namaskar, title, logo) before it; a cut or punch-in by 1 s; cover = frame 1 | skip rate % | 60.7 | 52.6 | 45 | 58 | 3/3 (judge at 3, max 6) | **HOLD** 3 reels, between stop and target |
| B2 Tight 20-30 s | 20-30 s total; title montage 1.5 s or less and only after the hook; payoff by 20 s; the last line echoes the hook so a replay feels natural; no dead air | watched % | 26.3 | 38.7 | 45 | 32 | 1/1 (judge at 3, max 6) | **HOLD** 1/3 reels |
| B3 A line worth sending | Every script lands one line a viewer would forward to a specific person (a number to remember, a jab at the system, an 'I told you so'); never ask for shares | sends per 1k plays | 2.6 | 3.2 | 8 | 2 | 3/4 (judge at 4, max 6) | **HOLD** 3/4 reels |
| W1 Glam Sarika | Sarika in the glam wardrobe (formats/samachar.md) on every Samachar reel | skip rate % | 66.9 | 55.8 | – | – | 3/3 (judge at 3, max 6) | **WATCH** tracked; judged at the monthly review |
<!-- /scoreboard -->

## This week's plan
_Written by the strategist every Sunday. The morning session executes it: each story option says which bets it carries, and each script says how it carries them._

**Week of Mon 5 Oct (written Sun 4 Oct)**
- **The strategy (Akhilesh, 4 Oct): current affairs bring viewers in, Sahayata Kendra gives them value.** Sarika and Gupta's Samachar reels ride the news cycle for reach; Sahayata Kendra episodes are evergreen topics that still mean something in a few months, never news. Still an experiment; no pivot, and consistency for the next few weeks is the lever.
- **Mix: at least 4 of 7 reels are short Samachar reels (20–30 s) on current affairs, carrying all three tests;** Sahayata Kendra (evergreen) at most 2 this week. The tight-length test got no new reel in 9 days because the week went to 66–67 s episodes.
- **Hook in frame one (skip rate, 52.5% on 3 reels, target 45%):** the on-screen hook is the rupee or % number the story turns on, 6 big words or fewer, spoken to camera from frame 1, as Policybazaar did. Sahayata keeps its hook strip from frame one (E6 and E7 are at 31–37% early).
- **Tight 20–30 s (watched %, 39.5% on 1 reel, target 45%):** our viewers give about 12 s on every reel, so the payoff lands by 12 s, the reel ends by 25 s, and the last line echoes the hook.
- **A line worth sending (sends per 1k, 3.8 on 3 reels, target 8):** the sendable line goes inside the first 12 s, not at the end; never ask for shares.
- **Ride now:** the market slump as one rupee number ("Sitambar mein ₹23 lakh crore saaf. Aapke SIP ka kya?"), Samachar, 20–25 s, index level only, figure checked at the desk. Then "1 October se kya badla" for salaried viewers. Big movers with a clear cause stay the desk's first source.
- **Posting:** one reel a day, 7 days, 7–9 pm IST (E6 and E7 went up at 17:00). Stage 1 now runs to 25 Oct and the strategy stop is judged after 20 reels, so consistency is the test: no day skipped. Trial Reel whenever the option shows.
- **Every reel through the log:** `scoreboard.py add-reel` with bets, credits and the desk score before it posts. Three of nine reels can't be judged. Reels made outside the loop are Naveen's (X1, X2, likely E4): log them with their tests and credits too.
- **Watching:** E6 and E7 at 72 h (does the low skip survive non-followers?); E7's saves (the checklist); followers to 100 by 11 Oct.

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
- 2026-10-01 (nightly):
  - No stop or target hit; all bets HOLD (B1 and B2 on 1 judged reel, B3 on 1 of 4). Followers 72 (+1). No reel posted on 29 Sep, 30 Sep or 1 Oct: three days off the one-a-day plan, so the bets haven't moved.
  - E5 and X1 matured at 72 h (226 and 106 plays). Stage median plays at 72 h fell to 187 (E3 2,388, E4 148, E5 226, X1 106), below the strategy stop's 300 line; the stop is judged after 10 reels this stage (4 so far). Policybazaar owner feed still frozen (329 vs 2,394 public); public reading logged.
- 2026-10-02 (nightly): Quiet. No stop or target hit; all bets HOLD. Followers 73 (+1). No reel posted on 29 Sep–2 Oct (four days off the one-a-day plan). Policybazaar owner feed still frozen (329 vs 2,394 public); public reading logged.
- 2026-10-03 (nightly): No stop or target hit; all bets HOLD. Followers 87 (+14, the biggest day since 27 Sep). A Sahayata Kendra reel ("Retire hone ke liye kitni SIP chahiye?", 67 s, Pandey with the cat, hook text in frame one, posted 16:59) went up outside the flow: logged as X2 with no bets. Early read at 4.5 h on 50 plays (mostly followers): skip 38.9%, watched 77.9%, the best of any reel so far; judge it at 72 h, not now. Policybazaar owner feed still frozen (336 vs 2,401 public); public reading logged.
- 2026-10-04 (studio session): "X2" was E6, made in the logged flow (script w1-2 from loop v0.3, QC gate PASS, 94.5 credits) but not pushed until today. Merged into E6 in reels.csv with its bets, B1 (hook strip from frame one) and B3 ("das hazaar ka SIP, pandrah hazaar ka kharcha"); its snapshot attaches by code. Not a B2 reel (67 s by format).
- 2026-10-04 (weekly review and first monthly campaign review):
  - Nightly: E7 linked to DeEikF2pd9Z (posted 17:16). A reel on the RBI repo rate and home-loan EMIs went up at 20:11 outside the flow: logged as X2 with no bets (EMIs and loans are a rested topic). Policybazaar owner feed still frozen (337 vs 2,402 public); public reading logged. No stop or target hit; nothing taking off (E7's 204 plays at 4 h are in line with E5's early follower burst).
  - Book unchanged. Hook in frame one reached 3 reels at 52.5%, between stop (58) and target (45): hold to 6. Tight 20–30 s still on 1 judged reel: starved by a week of 66–67 s episodes, so the plan now requires 4 short reels a week. A line worth sending at 3.8 per 1k on 3 reels (stop 2, target 8): hold.
  - Weakest stage: hold. Average watch time is 10–16 s on every reel whatever its length, so long reels read 17–21% watched. No new bet (book full, and the tight-length test is the hold lever); the fix is execution: short reels, payoff by 12 s.
  - Stage 1 review: behind on skip (54.4 vs 45), watched (37.1 vs 45), median plays at 72 h (187 vs 500) and followers (87 vs 100); best reel hit (2,402). Mostly volume (no reel 29 Sep–2 Oct; 7 reels in 9 days) and execution (3 of 7 off the log; 3 of 7 long by format), not yet thesis. The strategy stop (median under 300 after 10 reels) is judged after 3 more reels; with 4 matured readings at 106–2,388, it hits unless about five of the six still to mature (E6, E7, X2 and the next three) reach 300 at 72 h, so expect it. Three alternative strategies put to Akhilesh in advance, so he can pick before it hits.
  - Desk calibration not possible: only E3 carries a desk score. Every reel now records one at add-reel.
  - Glam Sarika: still not comparable (1 logged Samachar reel in the watch, Sahayata reels not matured). Carried to the next review.
  - vidIQ credits this week: about 45 (35 nightly cross-checks, 10 outlier scans).
- 2026-10-04 (Akhilesh's replies to the weekly review):
  - AI label: he marks every reel as AI-generated at upload. The AI-generated profile label and Account Status not yet confirmed.
  - No pivot. The strategy stays: current-affairs Samachar reels (Sarika, Gupta) to bring viewers in, evergreen Sahayata Kendra episodes for value. Give it more time and post consistently for the next few weeks. Plan B (A/B/C) shelved; extending Stage 1 and the strategy stop put to him with numbers.
  - Reels made outside the loop (X1, X2) are Naveen's.
  - No burned-in AI mark ("let's not overdo").
  - Account Status (Akhilesh's screenshots, 4 Oct): Recommendation eligibility, Features, Content removals and Under-18 availability all green. One monetisation flag, "Established presence" (account too new and too small for monetisation tools); it doesn't affect reach. Plumbing ruled out for the slow reach. The "AI-generated profile" label is ON (Akhilesh turned it on at 22:35, 4 Oct, in Edit profile).
  - Stage 1 extended to 25 Oct and its strategy stop moved to 20 reels (Akhilesh: yes). Targets unchanged. Stage 2 shifts to 26 Oct–15 Nov.
- 2026-10-05 (nightly): Quiet. No stop or target hit; all bets HOLD (hook in frame one 52.7% on 3 reels; tight 20–30 s on 1; a line worth sending 3.7 per 1k on 3 of 4). Followers 88 (+1). No reel posted on 5 Oct, the first day of the 7-a-week plan. Nothing taking off (E7 218 plays at 28 h; E6's 12.5 sends per 1k is one send on 80 plays). X2 (RBI repo, 27 s) fell from 42% to 64% skip as it reached non-followers. Policybazaar owner feed still frozen (338 vs 2,403 public); public reading logged.
- 2026-10-06 (nightly): Snapdeal listing (E8, posted 5 Oct 22:23) is taking off: 2,242 plays at 23 h by the public count (owner feed frozen at 773; public reading logged, as with Policybazaar), against roughly 80–280 for every other reel at a day old. Followers 88 → 202 (+114), past the Stage 1 target of 100. Ride-now line added to docs/learnings.md: famous company in today's news, named or pictured in frame one, explained in one number. E8 linked to DeHrHCByq9V; it carries only the glam-Sarika watch (Akhilesh's script, opens on the photo), so it moves no bet. E6 matured at 72 h on 94 plays; the stage median at 72 h is 148 (8 of 20 reels). No stop or target hit; all bets HOLD. Policybazaar owner feed still frozen (344 vs 2,409 public).
- 2026-10-07 (nightly): No stop or target hit; all bets HOLD (hook in frame one 52.6% on 3 reels; tight 20–30 s 38.7% on 1; a line worth sending 3.2 per 1k on 3 of 4). Followers 210 (+8). HUL (E9, Down to Business 3, posted 6 Oct 21:58) linked to DeKLxlcyRYX: 531 plays at 24 h, about 3× the ~175 median of earlier reels at a day old but under the taking-off line, with 64% skip and 16% watched on 57 s; it carries only the glam-Sarika watch. Snapdeal (E8) at 2,378 public plays (owner feed frozen at 832). E7 and X2 matured at 72 h (258 and 132); stage median at 72 h still 148 (9 of 20 reels). Policybazaar owner feed still frozen (347 vs 2,412 public). No reel posted on 7 Oct.
- 2026-10-08 (Akhilesh): the morning desk email is now HTML research only (facts, what others are making, the curiosity gap, the tracker board; no hooks or scripts; English). Keep this exact format every day; review whether it's working around Wed 14 Oct.
