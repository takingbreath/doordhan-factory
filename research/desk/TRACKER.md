# Story tracker

_Written 2026-10-16 by `pipeline/story_tracker.py md`. Data: registry/story_tracker.json._

Every story the desk has sent stays here until it leaves the news cycle (COLD on two checks running, or past its window). Each morning `story_tracker.py check` measures them all again.

Label history reads oldest to newest: H hot, R rising, F flat, C cold.

| Story | Status | Now | Direction | Day | History | News today/week | YouTube views this week | Best views/hr | Desk score | Window |
|---|---|---|---|---|---|---|---|---|---|---|
| Jio Platforms IPO (`jio-ipo`) | active | HOT | rising | 9 | F F F R F R H | 100/100 | 453,792 | 9,525 | 7 | 2026-10-31 |
| International ETFs trading far above NAV (NSE warning) (`intl-etf-premium`) | active | COLD | fading | 9 | C C C C C C C | 0/0 | 12,809 | 51 | 6 | 2026-10-22 |
| SC orders panel on pharma freebies to doctors (`pharma-freebies-sc`) | active | COLD | rising | 8 | C C C C C C C | 0/0 | 24,896 | 183 | 6 | 2026-10-23 |
| UPI merchant fee (0.4% MDR) may be deferred to 1 Jan (`upi-mdr-deferral`) | active | HOT | rising | 7 | H F H H H H | 2/40 | 628,548 | 8,129 | 6 | 2026-10-16 |
| Inox Clean: revenue 43X, debt 45X, IPO on hold (`inox-clean-ipo`) | active | COLD | steady | 7 | C C C C C C | 0/2 | 64,449 | 352 | 6 | 2026-10-24 |
| Musk calls Ambani 'Prime Minister Ambani' over Starlink (`musk-ambani-starlink`) | active | FLAT | fading | 6 | H H H F F | 1/24 | 8,751,103 | 52,173 | 6 | 2026-10-21 |
| SC on hospital drug markups: Rs 2,700 drug sold at Rs 27,000 (`hospital-drug-markup-sc`) | active | COLD | steady | 6 | C C C C C | 0/0 | 193,252 | 1,318 | 6 | 2026-10-25 |
| Gauahar Khan's Versova duplex: 88% in 12 years (`gauahar-khan-flat`) | active | COLD | fading | 5 | C C C C | 0/0 | 127,347 | 1,047 | 6 | 2026-10-26 |
| Rupee near ₹97: RBI hike, then four emergency measures (`rbi-rupee-rescue`) | active | HOT | rising | 4 | H H H | 0/9 | 1,180,761 | 20,121 | 7 | 2026-10-20 |
| Zoho freezes pay rises over AI and server costs (`zoho-pay-freeze`) | active | COLD | fading | 3 | H C | 0/2 | 217,500 | 2,590 | 9 | 2026-10-20 |
| Sensex +1,109 partly on FM's LTCG remark (`ltcg-remark-rally`) | active | HOT | rising | 3 | H H | 0/1 | 1,866,439 | 22,635 | 8 | 2026-10-20 |
| Gold ₹3,600 cheaper in four sessions on a stronger rupee (`gold-slide-rupee`) | active | HOT | new | 2 | H | 52/80 | 252,012 | 3,242 | 8 | 2026-10-19 |
| Airtel Money lists in London at $7 bn (via The Ken) (`airtel-money-london`) | active | HOT | new | 2 | H | 13/100 | 398,769 | 7,287 | 6 | 2026-10-29 |
| Yes Bank -14.5% after SC voids AT-1 write-off (`yes-bank-at1-sc`) | active | - | new | 1 |  | -/- | 0 | 0 | 9 | 2026-10-20 |
| Mutual funds halt new gold FoF SIPs and bulk gold ETF buys (`gold-fund-halt`) | active | - | new | 1 |  | -/- | 0 | 0 | 8 | 2026-11-08 |
| Zetwerk IPO: 54% of Q1 revenue from metal sales (`zetwerk-ipo-metals`) | active | - | new | 1 |  | -/- | 0 | 0 | 7 | 2026-10-23 |
| Ramayana producer's Prime Focus searched by Income Tax (`prime-focus-ramayana`) | retired: COLD on 2 checks running | COLD | steady | 9 | H H H H C C | 0/0 | 1,056,196 | 7,548 | 8 | 2026-11-10 |
| EPF wage ceiling raised to ₹25,000 (`epf-wage-ceiling`) | retired: COLD on 2 checks running | COLD | fading | 9 | F F C C | 0/7 | 20,051 | 152 | - | - |
| Snapdeal (AceVector) after listing (`snapdeal-acevector`) | retired (E8): COLD on 2 checks running | COLD | steady | 9 | C C | 0/1 | 100,780 | 770 | - | - |
| Nana Patekar dies; the Rs 1.5 crore car he gave up for farmers (`nana-patekar`) | retired (E10): past its window | HOT | rising | 9 | R H H H | 100/100 | 27,305,534 | 110,559 | 7 | 2026-10-11 |
| Sensex -1,045 on 8 Oct: ₹10.23 lakh crore wiped off (`market-crash-oct8`) | retired: past its window | HOT | rising | 8 | H H C H | 9/17 | 3,239,882 | 14,656 | 9 | 2026-10-12 |
| TCS: profit +15%, share -35% in 2026 (`tcs-q2-profit-share`) | retired: past its window | HOT | rising | 8 | H F F F F H | 7/48 | 464,093 | 10,346 | 8 | 2026-10-14 |
| US suspends TCS, Infosys, Wipro from green-card PERM; IT shares rise (`us-perm-indian-it`) | retired: COLD on 2 checks running | COLD | steady | 6 | H C C | 0/1 | 1,195,114 | 3,721 | 8 | 2026-10-17 |
| HDFC Bank's new CEO ₹35.9 cr vs SBI chairman ₹43 lakh (`hdfc-ceo-pay-sbi`) | retired: COLD on 2 checks running | COLD | fading | 5 | C C | 0/1 | 8,051 | 55 | 9 | 2026-10-27 |
| Kohli and Anushka's ₹44 crore: three Versova flats, ready 2031 (`kohli-anushka-versova-flats`) | retired: COLD on 2 checks running | COLD | fading | 4 | C C | 0/0 | 598 | 25 | 8 | 2026-10-20 |

## Latest notes
- **Jio Platforms IPO:** 2026-10-14: 13 Oct: >$20 bn bids reported (ET/Mint headlines); band 1,065-1,119 reported; no RHP yet
- **Jio Platforms IPO:** 2026-10-15: 15 Oct: dates official (PTI): opens 21 Oct, lists 28 Oct; ₹2,500 cr quota for Reliance holders as of 14 Oct; ₹500 cr employees
- **International ETFs trading far above NAV (NSE warning):** First sent 8 Oct (deep lane). NSE caution 7 Oct; BSE 25 Sep.
- **SC orders panel on pharma freebies to doctors:** First sent 9 Oct (deep lane). Order 8 Oct; panel reports in ~2 months; hearing 29 Jan 2027.
- **UPI merchant fee (0.4% MDR) may be deferred to 1 Jan:** 2026-10-13: 13 Oct: no decision yet, 15 Oct stands; IIT-Bombay study says 0.08% (PTI, 11 Oct)
- **UPI merchant fee (0.4% MDR) may be deferred to 1 Jan:** 2026-10-14: 13 Oct: NPCI deferred MDR to 'immediately after Diwali', date to be notified; rates unchanged
- **Inox Clean: revenue 43X, debt 45X, IPO on hold:** First sent 10 Oct (via The Ken, 9 Oct). SEBI observations in abeyance.
- **Musk calls Ambani 'Prime Minister Ambani' over Starlink:** 2026-10-12: Musk promises affordable Starlink (Sat 10 Oct); Jio targets $106 bn
- **Musk calls Ambani 'Prime Minister Ambani' over Starlink:** 2026-10-14: 13 Oct: RSS affiliate urges Starlink licence denial (Reuters)
- **SC on hospital drug markups: Rs 2,700 drug sold at Rs 27,000:** First sent 11 Oct. Hearings 22 and 29 Sep; 16% uniform margin suggested; Centre's reply due at the 12 Oct hearing.
- **Gauahar Khan's Versova duplex: 88% in 12 years:** creator-format option; desk 12 Oct
- **Rupee near ₹97: RBI hike, then four emergency measures:** First sent 13 Oct. Repo 5.50% (7 Oct); ₹96.73 → ₹95.76 on 12 Oct; 99% daily CRR from 16 Oct.
- **Zoho freezes pay rises over AI and server costs:** First sent 14 Oct. Vembu X post 13 Oct: no usual pay increase, server prices 4x, headcount flat 18 months, 'pray for us'.
- **Sensex +1,109 partly on FM's LTCG remark:** First sent 14 Oct. FM: debate healthy, 'not the best time to say what I will consider'; Sensex +1,109 to 73,033.78 on 13 Oct.
- **Gold ₹3,600 cheaper in four sessions on a stronger rupee:** First sent 15 Oct. ₹1,50,800/10 g on 14 Oct (−₹1,800; −₹3,600 since 9 Oct); rupee 95.17, 4th gain.
- **Airtel Money lists in London at $7 bn (via The Ken):** First sent 15 Oct. £1.96, £5.3 bn; 270m shares; flat debut 9 Oct; admission 14 Oct.
- **Yes Bank -14.5% after SC voids AT-1 write-off:** results 17 Oct
- **Zetwerk IPO: 54% of Q1 revenue from metal sales:** via The Ken
