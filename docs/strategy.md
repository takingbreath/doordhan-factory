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
_Updated 2026-10-25 21:41 IST by `scoreboard.py write`._

**Stage 1: Stop the scroll** (2026-09-26 to 2026-10-25): prove people stop for our reels and stay to the end

- skip rate %: now 56, target 45 → not yet
- watched %: now 29.3, target 45 → not yet
- median plays at 72 h: now 420, target 500 → not yet
- best reel's plays: now 6709, target 2000 → on target
- followers: now 467, target 100 → on target
- strategy stop: 14/20 reels posted this stage; median plays at 72 h now 420, must reach 300

| Bet | Lever | Judged on | Baseline | Now | Target | Stop | Reels (judged/carried) | Verdict |
|---|---|---|---|---|---|---|---|---|
| B1 Hook in frame one | Frame 1: the anchor looks into the lens, already saying the viewer's stake; the hook in 6 big words or fewer on screen; nothing (Namaskar, title, logo) before it; a cut or punch-in by 1 s; cover = frame 1 | skip rate % | 60.7 | 52.4 | 45 | 58 | 3/5 (judge at 3, max 6) | **HOLD** 3 reels, between stop and target |
| B2 Tight 20-30 s | 20-30 s total; title montage 1.5 s or less and only after the hook; payoff by 20 s; the last line echoes the hook so a replay feels natural; no dead air | watched % | 26.3 | 38.6 | 45 | 32 | 1/1 (judge at 3, max 6) | **HOLD** 1/3 reels |
| B3 A line worth sending | Every script lands one line a viewer would forward to a specific person (a number to remember, a jab at the system, an 'I told you so'); never ask for shares | sends per 1k plays | 2.6 | 3.2 | 8 | 2 | 3/5 (judge at 4, max 6) | **HOLD** 3/4 reels |
| W1 Glam Sarika | Sarika in the glam wardrobe (formats/samachar.md) on every Samachar reel | skip rate % | 66.9 | 55.8 | – | – | 3/3 (judge at 3, max 6) | **WATCH** tracked; judged at the monthly review |
| W2 Famous name in frame one | Frame one shows a company, brand or person every viewer already knows (their name, logo, or a licensed photo or real footage), with the number or question it turns on | median plays at 72 h | 243 | 2395 | – | – | 5/5 (judge at 3, max 6) | **WATCH** tracked; judged at the monthly review |
<!-- /scoreboard -->

## This week's plan
_Written by the strategist every Sunday. The morning session executes it: each story option says which bets it carries, and each script says how it carries them._

**Week of Mon 26 Oct (written Sun 25 Oct)**
- **News of the day, one reel a day.** Every breakout so far was on a story in that day's market news; every evergreen reel stayed under 310 plays. The desk leads with the day's market story; the session produces any approved script the same day and it posts the same day, morning or evening (E13 and E14 broke out on 08:15 and 09:19 posts).
- **Ride now: Jio allotment (Mon 26 Oct) and listing (Wed 28 Oct).** 1.35 crore applications; the "allotment is a lottery" explainer did 3.7M (359× median) for @samjho.exe. Jio's logo in frame one, IPO facts only, no apply, hold or sell call. Then gold or silver before Dhanteras, following E14.
- **Split-screen opener on every reel** (watching, not yet a bet): the story's picture, logo or B-roll on the top half with the hook in 6 words or fewer, the presenter below, from frame one. E11, E13 and E14 used it; all three broke out.
- **Hook in frame one (skip rate, 52.4% on 3 judged reels):** the stake said inside the first second, the hook text on screen from frame one, a cut or punch-in by 1 s (E14 missed the cut).
- **A line worth sending (sends per 1k, 3.2 on 3 of 4 reels):** one line a viewer would forward to a specific person, inside the first 12 s; never ask for shares. E13 and E14 had none.
- **Length:** Samachar and creator reels 20–30 s as CLAUDE.md says; Sahayata Kendra 70 s at most (E13 ran 92). The tight-length test is put to Akhilesh (retire or keep).
- **Log every reel before it posts:** `scoreboard.py add-reel` with its bets and credits; E13's production, credits and outfit are still missing from the repo.
- **Watching:** whether the Jio listing reel travels like E11; likes per 1k on Sahayata Kendra (7–17) against the creator format (57–78); vidIQ's owner feed (dark since 9 Oct).

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
- 2026-10-08 (nightly): Quiet. No stop or target hit; all bets HOLD (hook in frame one 52.4% on 3 reels; tight 20–30 s 38.6% on 1; a line worth sending 3.2 per 1k on 3 of 4). Followers 209 (−1). No reel posted on 7 or 8 Oct (two days off the 7-a-week plan; 9 of 20 stage reels with 17 days left). Snapdeal (E8) at 2,387 public plays at 71 h (owner feed frozen at 840; public reading logged); HUL (E9) 546 at 48 h, flattening, not taking off. Policybazaar owner feed still frozen (348 vs 2,413 public).
- 2026-10-08 (Akhilesh): the morning desk email is now HTML research only (facts, what others are making, the curiosity gap, the tracker board; no hooks or scripts; English). Keep this exact format every day; review whether it's working around Wed 14 Oct.
- 2026-10-09 (nightly): vidIQ owner insights unavailable at 21:31 ("Meta token is inactive"; the account list says active, as on 28 Sep). Akhilesh to reconnect Instagram in vidIQ. Public counts only (ig_profile_reels): no new reel since E9, and every older reel within 0–7 plays of last night, so public readings logged only for E8 (2,395) and E9 (553 at 72 h); no bets judged on public data. No stop or target hit; all bets HOLD (hook in frame one 52.4% on 3 reels; tight 20–30 s 38.6% on 1; a line worth sending 3.2 per 1k on 3 of 4). Stage median plays at 72 h 187 with E8 matured (10 readings, 9 of 20 stage reels). No reel posted 7, 8 or 9 Oct: three days off the 7-a-week plan, with 11 stage reels needed in 16 days. Followers not read (owner feed down).
- 2026-10-10 (nightly): Nana Patekar (E10, creator format, posted 9 Oct about 22:00) is taking off: 1,768 public plays at about 23 h, about 8× the ~214 median of our reels at a day old. Linked to DeSScR6ycpo; it carries no bet. Ride-now line added to docs/learnings.md: a famous Indian's money decision, told in the creator format, under 30 s. vidIQ owner insights unavailable for a second night ("Meta token is inactive"); public counts only, logged for E10, E9 (582) and E8 (2,420); no bets judged on public data. Followers 213 (public profile; +4 since 8 Oct). No stop or target hit; all bets HOLD (hook in frame one 52.4% on 3 reels; tight 20–30 s 38.6% on 1; a line worth sending 3.2 per 1k on 3 of 4). Stage median plays at 72 h 226 (10 of 20 reels). Instagram lists E10 at 84 s against the 42.1 s final: to confirm.
- 2026-10-11 (weekly review):
  - vidIQ owner insights unavailable for a third night ("Meta token is inactive"); public counts only, logged for E10 (3,224 at 48 h, 252 likes), E9 (598), E8 (2,434) and E3 (2,425). Followers 291 (public profile), +78 since last night and +204 in the week (87 → 291). No bets judged on public data; no stop or target hit; all bets HOLD.
  - The week: 3 reels (E8 Snapdeal, E9 HUL, E10 Nana Patekar) against a plan of 7, about 6,500 plays (about 10× the week before) and 297 episode credits (about 47 per 1,000 plays on the week's reels). None of the three carried a bet, so the book has not moved since 4 Oct; tight 20–30 s still has 1 judged reel.
  - Weakest stage: stop. Skip rate 55.9% against 45%, and the three breakouts skipped at 54–55% too: they won on distribution, not the opening.
  - Book unchanged (full at 3, nothing at a stop, target or time stop). New watch item W2, "famous name in frame one", tracked on median plays at 72 h (243 baseline across all reels; 2,388 on the 3 matured W2 reels). Not traded: confounded with topic.
  - Desk grading weights changed: Stake 0–2 → 0–1, Clarity 0–1 → "Known name" 0–2 (playbooks/newsdesk.md; desk_report.py renders both). Evidence: four known-name openers at 582–3,224 plays vs eight others at 94–303; E10 had no investor stake and is the best reel.
  - Asked Akhilesh to keep his scripts to 30 s so the length test can be judged, and to reconnect Instagram in vidIQ.
  - Platform: YouTube Shorts now favours original clips and cuts reach for re-uploaders (1 Oct); the creator format's film clips stay a few seconds inside our own edit. No Instagram ranking, SEBI or MeitY change found.
- 2026-10-12 (nightly): Quiet. vidIQ owner insights unavailable for a fourth night ("Meta token is inactive"; the account list still says active); public counts only, no bets judged on public data. No reel posted on 10, 11 or 12 Oct (the plan says one a day; 10 of 20 stage reels with 13 days left). Nana Patekar (E10) 3,275 public plays at 71.6 h (257 likes), flattening (+51 on the day); every older reel within 0–3 plays of last night, so only E10 logged. Followers 291 (public profile, flat). No stop or target hit; all bets HOLD (hook in frame one 52.4% on 3 reels; tight 20–30 s 38.6% on 1; a line worth sending 3.2 per 1k on 3 of 4). vidIQ credits this week: 10.
- 2026-10-13 (nightly): Quiet. vidIQ owner insights unavailable for a fifth night ("Meta token is inactive"; the account list still says active); public counts only, no bets judged on public data. No reel posted on 10–13 Oct (four days off the one-a-day plan; 10 of 20 stage reels with 12 days left, so 10 more means almost one a day to 25 Oct). Every reel within 0–6 plays of the last reading (E10 3,279), so no public reading logged. No stop or target hit; all bets HOLD (hook in frame one 52.4% on 3 reels; tight 20–30 s 38.6% on 1; a line worth sending 3.2 per 1k on 3 of 4). vidIQ credits this week: 15.
- 2026-10-14 (nightly): Quiet. vidIQ owner insights unavailable for a sixth night ("Meta token is inactive"; the account list still says active); public counts only, no bets judged on public data. No reel posted on 10–14 Oct (five days off the one-a-day plan; 10 of 20 stage reels with 11 days left). Every reel within 0–6 plays of the last reading (E10 3,281, E8 2,440, E9 604), so no public reading logged. No stop or target hit; all bets HOLD (hook in frame one 52.4% on 3 reels; tight 20–30 s 38.6% on 1; a line worth sending 3.2 per 1k on 3 of 4). vidIQ credits this week: 20.
- 2026-10-15 (nightly): Quiet. vidIQ owner insights unavailable for a seventh night ("Meta token is inactive"; the account list still says active); public counts only, no bets judged on public data. No reel posted on 10–15 Oct (six days off the one-a-day plan; 10 of 20 stage reels with 10 days left, so the strategy stop can only be judged on 25 Oct with a reel every day from tomorrow). Every reel within 0–6 plays of the last reading (E10 3,282, E8 2,442, E9 604), so no public reading logged. No stop or target hit; all bets HOLD (hook in frame one 52.4% on 3 reels; tight 20–30 s 38.6% on 1; a line worth sending 3.2 per 1k on 3 of 4). vidIQ credits this week: 25.
- 2026-10-16 (nightly): Quiet. vidIQ owner insights unavailable for an eighth night ("Meta token is inactive"; the account list still says active); public counts only, no bets judged on public data. No reel posted on 10–16 Oct (seven days off the one-a-day plan; 10 of 20 stage reels with 9 days left, so the strategy stop can no longer reach 20 reels by 25 Oct even at one a day; the 25 Oct review judges it on what is posted). Every reel within 0–3 plays of the last reading (E10 3,284, E8 2,445, E9 605), so no public reading logged. No stop or target hit; all bets HOLD (hook in frame one 52.4% on 3 reels; tight 20–30 s 38.6% on 1; a line worth sending 3.2 per 1k on 3 of 4). vidIQ credits this week: 30.
- 2026-10-17 (nightly): Quiet. vidIQ owner insights unavailable for a ninth night ("Meta token is inactive"; the account list still says active); public counts only, no bets judged on public data. No reel posted on 10–17 Oct (eight days off the one-a-day plan; 10 of 20 stage reels with 8 days left; the desk drafted the WhatsApp stock-tip story today). Every reel within 0–5 plays of the last reading (E10 3,289, E8 2,445, E9 610), so no public reading logged. No stop or target hit; all bets HOLD (hook in frame one 52.4% on 3 reels; tight 20–30 s 38.6% on 1; a line worth sending 3.2 per 1k on 3 of 4). vidIQ credits this week: 35.
- 2026-10-18 (weekly review):
  - vidIQ owner insights unavailable for a tenth night ("Meta token is inactive"; the account list still says active); public counts only, no bets judged on public data. Every reel within 0–2 plays of last night (E10 3,291), so no public reading logged. No stop or target hit; all bets HOLD (hook in frame one 52.4% on 3 reels; tight 20–30 s 38.6% on 1; a line worth sending 3.2 per 1k on 3 of 4).
  - The week: no reel posted (the last was E10 on 9 Oct), about 230 plays on the back catalogue (public counts), followers 291 (+0), 0 episode credits. Ten script drafts in scripts/drafts/ since 10 Oct, none approved; the drafts aim at 30–40 s, over the 30 s rule.
  - Weakest stage: still the stop (skip 55.9% against 45%), but the binding constraint is volume: no bet can move without reels. Book unchanged (full at 3; no stop, target or time stop). No new bet.
  - Evidence (one outlier scan, 5 credits): the Jio IPO (opens 21 Oct) was 6 of 10 Instagram outliers (@growwithyuvraj.20 15.5M, @therawfeed.ig 6.6M, @thekiranyadavv 4.7M, @abhishekkarofficial 2.4M, @rehan.talkss 1.9M, @the_unchaptered 985K); IDBI's sale to Fairfax (@cryptowalaindia 1.9M) and UPI MDR postponed (@legitfinancials 866K) were stories the desk also carried. Pattern (8 of 10): split screen, real footage on top, presenter below.
  - Put to Akhilesh: the Jio IPO reel before Tuesday; scripts held to 30 s; Stage 1 to run to 20 reels or 8 Nov; reconnect Instagram in vidIQ.
  - Platform: no change found to Instagram ranking, YouTube Shorts (beyond the 1 Oct originality update), SEBI's finfluencer rules or MeitY's AI labels.
  - vidIQ credits this week: 45 (35 nightly cross-checks, 5 tonight's cross-check, 5 outliers).
- 2026-10-19 (nightly): First reel in ten days: E11 (Starlink vs Jio, creator format, 59 s, carries only the famous-name watch item) posted about 18:10 (time read from the shortcode) and linked to DerRj-MyNeO; 237 public plays, 7 likes at 3.5 h, in line with E7's early follower burst (204 at 4 h), so not taking off yet; judge it tomorrow at about a day old against E10's 1,768. vidIQ owner insights unavailable for an eleventh night ("Meta token is inactive"; the account list still says active), so public counts only and no bets judged. Followers 286 (public profile, -5 on the week). Every older reel within 0–26 plays of its last reading (E10 3,297), so only E11 logged. No stop or target hit; all bets HOLD (hook in frame one 52.4% on 3 reels; tight 20–30 s 38.6% on 1; a line worth sending 3.2 per 1k on 3 of 4). 11 of 20 stage reels with 6 days left. Shortcode times put E10's posting at about 01:14 on 10 Oct, not 22:00 on 9 Oct; its readings' ages are about 3 h too high (not changed). vidIQ credits this week: 10.
- 2026-10-20 (nightly): Starlink vs Jio (E11) is taking off, just over the line: 661 public plays and 34 likes at 27.5 h, against a line of about 650 (3× the ~216 median of the last 10 reels at about a day old); well below Snapdeal (2,242) and Nana Patekar (1,768) at that age. Ride-now line added to docs/learnings.md: a 20–30 s Jio IPO reel for tomorrow, the day it opens. vidIQ owner insights unavailable for a twelfth night ("Meta token is inactive"; the account list still says active), so public counts only and no bets judged. Followers not read tonight (286 last night). Every older reel within 0–20 plays of its last reading, so only E11 logged. No stop or target hit; all bets HOLD (hook in frame one 52.4% on 3 reels; tight 20–30 s 38.6% on 1; a line worth sending 3.2 per 1k on 3 of 4). 11 of 20 stage reels with 5 days left. vidIQ credits this week: 15.
- 2026-10-21 (nightly): Starlink vs Jio (E11) is now our biggest reel: 4,055 public plays and 232 likes at about 52 h (661 last night), past Nana Patekar (3,319) before its 72 h reading; most of the jump came on Jio IPO opening day. Ride-now line updated: a 20–30 s Jio reel tomorrow while the issue is open, then listing day. No new reel posted today (11 of 20 stage reels, 4 days left). vidIQ owner insights unavailable for a thirteenth night ("Meta token is inactive"; the account list still says active), so public counts only and no bets judged. Followers not read tonight (286 on 19 Oct). Every older reel within 0–35 plays of its last reading, so only E11 logged. No stop or target hit; all bets HOLD (hook in frame one 52.4% on 3 reels; tight 20–30 s 38.6% on 1; a line worth sending 3.2 per 1k on 3 of 4). vidIQ credits this week: 20.
- 2026-10-22 (nightly): Salman Khan: maafi ya ₹5 crore (E12, Naveen's Sahayata Kendra voice-over reel, 70 s, carries hook in frame one and a line worth sending) is taking off: 6,009 public plays and 93 likes at 21 h (posted 00:45 IST, time read from the shortcode), our biggest reel and about 28× the ~216 median at a day old. Linked to DexIwnEyUZW. Ride-now line added to docs/learnings.md: another famous-name money story told the same way. Starlink vs Jio (E11) at 4,091 public plays at 75.6 h (its 72 h reading). vidIQ owner insights unavailable for a fourteenth night ("Meta token is inactive"; the account list still says active), so public counts only and no bets judged; E12's skip, watched and sends stay unknown until it returns. Followers not read tonight (286 on 19 Oct). Every older reel within 0–40 plays of its last reading, so only E11 and E12 logged. No stop or target hit; all bets HOLD (hook in frame one 52.4% on 3 judged reels; tight 20–30 s 38.6% on 1; a line worth sending 3.2 per 1k on 3 of 4). 12 of 20 stage reels with 3 days left; median plays at 72 h 242. vidIQ credits this week: 25.
- 2026-10-25 (weekly review):
  - vidIQ owner insights unavailable for a 17th night ("Meta token is inactive"; the account list says active); public counts only, no bets judged. Silver (E14, posted 08:15 today, linked to De5qk8SSBLc) is taking off: 2,065 public plays at 13.4 h, against 876 for eMudhra at 12.5 h. Ride-now line added. Public readings logged for E14, E13 (5,865 at 60 h), E12 (6,709), E10 and E9. Followers 467 (public profile), +176 on the week.
  - The week: 4 reels (E11 Starlink vs Jio, E12 Salman Khan, E13 eMudhra, E14 silver), all on that day's news, all four over the taking-off line; about 18,900 plays (about 80× the week before). Episode credits 256 on E11, E12 and E14 (about 20 per 1,000 plays); E13's credits are not logged.
  - Stage 1 ends today: best reel (6,709) and followers (467) hit; median plays at 72 h 420 against 500, missed; skip (56%) and watched (29%) unknown since 9 Oct. Strategy stop not hit (14 of 20 reels, median 420 above 300). Last week's question (run to 20 reels or 8 Nov) had no recorded answer; put again with Stage 2's start and a follower target of 1,000 (we are at 467 against Stage 2's written 500).
  - Book unchanged: no stop, target or time stop; no bet can be judged without the owner feed. Hook in frame one carried by E12 and E14 (unmeasured). Tight 20–30 s got no reel for a second week (the four breakouts ran 59–92 s): retiring it, and opening a split-screen-opener bet on median plays at 72 h in its slot, put to Akhilesh.
  - Weakest stage: the stop by the last numbers (skip 56% against 45%), but the binding problem is data: 17 nights without the owner feed. Asked Akhilesh to reconnect vidIQ or send Insights screenshots for E11–E14.
  - Evidence (one outlier scan, 5 credits): the Jio IPO was 9 of 10 Indian money outliers on Instagram (up to 3.8M, @tazakhabhar.in, 414×; @samjho.exe allotment-lottery explainer 3.7M, 359×); split screen in 6 of 10. Platform: no Instagram ranking, Shorts, SEBI or MeitY change found.
  - vidIQ credits this week: 50 of 60 (nightly cross-checks 40, profile 5, outliers 5).
