# Story tracker

_Written 2026-10-12 by `pipeline/story_tracker.py md`. Data: registry/story_tracker.json._

Every story the desk has sent stays here until it leaves the news cycle (COLD on two checks running, or past its window). Each morning `story_tracker.py check` measures them all again.

Label history reads oldest to newest: H hot, R rising, F flat, C cold.

| Story | Status | Now | Direction | Day | History | News today/week | YouTube views this week | Best views/hr | Desk score | Window |
|---|---|---|---|---|---|---|---|---|---|---|
| Jio Platforms IPO (`jio-ipo`) | active | FLAT | steady | 5 | H R F F F | -/100 | 403,318 | 1,612 | 7 | 2026-10-31 |
| Ramayana producer's Prime Focus searched by Income Tax (`prime-focus-ramayana`) | active | COLD | fading | 5 | H H H H C | 0/0 | 1,050,808 | 9,372 | 8 | 2026-11-10 |
| International ETFs trading far above NAV (NSE warning) (`intl-etf-premium`) | active | COLD | rising | 5 | C C C C C | 0/0 | 67,347 | 267 | 6 | 2026-10-22 |
| Sensex -1,045 on 8 Oct: ₹10.23 lakh crore wiped off (`market-crash-oct8`) | active | COLD | fading | 4 | H H C | 0/4 | 1,777,684 | 6,888 | 9 | 2026-10-12 |
| TCS: profit +15%, share -35% in 2026 (`tcs-q2-profit-share`) | active | FLAT | fading | 4 | H F F | 2/40 | 190,558 | 1,055 | 8 | 2026-10-14 |
| SC orders panel on pharma freebies to doctors (`pharma-freebies-sc`) | active | COLD | steady | 4 | C C C | 0/1 | 68,795 | 497 | 6 | 2026-10-23 |
| UPI merchant fee (0.4% MDR) may be deferred to 1 Jan (`upi-mdr-deferral`) | active | FLAT | fading | 3 | H F | 3/43 | 302,336 | 2,119 | 7 | 2026-10-16 |
| Inox Clean: revenue 43X, debt 45X, IPO on hold (`inox-clean-ipo`) | active | COLD | steady | 3 | C C | 0/2 | 358,262 | 2,330 | 6 | 2026-10-24 |
| Musk calls Ambani 'Prime Minister Ambani' over Starlink (`musk-ambani-starlink`) | active | HOT | new | 2 | H | 3/38 | 1,667,305 | 7,599 | 9 | 2026-10-21 |
| US suspends TCS, Infosys, Wipro from green-card PERM; IT shares rise (`us-perm-indian-it`) | active | HOT | new | 2 | H | 0/1 | 1,310,342 | 5,567 | 8 | 2026-10-17 |
| SC on hospital drug markups: Rs 2,700 drug sold at Rs 27,000 (`hospital-drug-markup-sc`) | active | COLD | new | 2 | C | 0/0 | 6,689 | 46 | 6 | 2026-10-25 |
| HDFC Bank's new CEO ₹35.9 cr vs SBI chairman ₹43 lakh (`hdfc-ceo-pay-sbi`) | active | - | new | 1 |  | -/- | 0 | 0 | 9 | 2026-10-27 |
| Gauahar Khan's Versova duplex: 88% in 12 years (`gauahar-khan-flat`) | active | - | new | 1 |  | -/- | 0 | 0 | 6 | 2026-10-26 |
| EPF wage ceiling raised to ₹25,000 (`epf-wage-ceiling`) | retired: COLD on 2 checks running | COLD | fading | 5 | F F C C | 0/7 | 20,051 | 152 | - | - |
| Snapdeal (AceVector) after listing (`snapdeal-acevector`) | retired (E8): COLD on 2 checks running | COLD | steady | 5 | C C | 0/1 | 100,780 | 770 | - | - |
| Nana Patekar dies; the Rs 1.5 crore car he gave up for farmers (`nana-patekar`) | retired (E10): past its window | HOT | rising | 5 | R H H H | 100/100 | 27,305,534 | 110,559 | 7 | 2026-10-11 |

## Latest notes
- **Jio Platforms IPO:** 2026-10-10: 2026-10-10: Bloomberg band ₹1,065-1,119, ~₹30,213 cr, valuation ~07 bn; RHP expected Mon 12 Oct
- **Jio Platforms IPO:** 2026-10-11: 11 Oct: no RHP yet; documents expected week of 12 Oct; Musk-Ambani row (story musk-ambani-starlink) is its newest turn
- **Ramayana producer's Prime Focus searched by Income Tax:** First sent 8 Oct. I-T searches 7 Oct, shares about -8%. Film releases 5 Nov: the story can return at release.
- **International ETFs trading far above NAV (NSE warning):** First sent 8 Oct (deep lane). NSE caution 7 Oct; BSE 25 Sep.
- **Sensex -1,045 on 8 Oct: ₹10.23 lakh crore wiped off:** First sent 9 Oct. Sensex 32-month low, Nifty 52-week low, Brent $104, FII selling 9 sessions.
- **TCS: profit +15%, share -35% in 2026:** First sent 9 Oct. Q2 profit ₹13,884 cr; +4,258 staff; AI $3.1 bn.
- **SC orders panel on pharma freebies to doctors:** First sent 9 Oct (deep lane). Order 8 Oct; panel reports in ~2 months; hearing 29 Jan 2027.
- **UPI merchant fee (0.4% MDR) may be deferred to 1 Jan:** First sent 10 Oct. Fee due 15 Oct; deferral to 1 Jan 2027 under consideration, decision in days.
- **UPI merchant fee (0.4% MDR) may be deferred to 1 Jan:** 2026-10-11: 11 Oct: steering committee meeting of 9 Oct not held; 15 Oct still officially stands
- **Inox Clean: revenue 43X, debt 45X, IPO on hold:** First sent 10 Oct (via The Ken, 9 Oct). SEBI observations in abeyance.
- **Musk calls Ambani 'Prime Minister Ambani' over Starlink:** First sent 11 Oct. Musk posts 8-10 Oct; govt: same stage for all three satcom operators; Jio 1,600-satellite plan; ties to Jio IPO 21 Oct.
- **Musk calls Ambani 'Prime Minister Ambani' over Starlink:** 2026-10-12: Musk promises affordable Starlink (Sat 10 Oct); Jio targets $106 bn
- **US suspends TCS, Infosys, Wipro from green-card PERM; IT shares rise:** First sent 11 Oct. Suspension 8 Oct; Nifty IT +1,000 pts at one stage 9 Oct; The Ken: Infosys 0 certifications since 2023.
- **SC on hospital drug markups: Rs 2,700 drug sold at Rs 27,000:** First sent 11 Oct. Hearings 22 and 29 Sep; 16% uniform margin suggested; Centre's reply due at the 12 Oct hearing.
- **HDFC Bank's new CEO ₹35.9 cr vs SBI chairman ₹43 lakh:** Bagchi package via postal ballot; desk 12 Oct
- **Gauahar Khan's Versova duplex: 88% in 12 years:** creator-format option; desk 12 Oct
