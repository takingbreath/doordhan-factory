# Story tracker

_Written 2026-10-13 by `pipeline/story_tracker.py md`. Data: registry/story_tracker.json._

Every story the desk has sent stays here until it leaves the news cycle (COLD on two checks running, or past its window). Each morning `story_tracker.py check` measures them all again.

Label history reads oldest to newest: H hot, R rising, F flat, C cold.

| Story | Status | Now | Direction | Day | History | News today/week | YouTube views this week | Best views/hr | Desk score | Window |
|---|---|---|---|---|---|---|---|---|---|---|
| Jio Platforms IPO (`jio-ipo`) | active | RISING | rising | 6 | H R F F F R | 36/100 | 197,159 | 2,337 | 7 | 2026-10-31 |
| International ETFs trading far above NAV (NSE warning) (`intl-etf-premium`) | active | COLD | rising | 6 | C C C C C C | 0/0 | 111,096 | 1,859 | 6 | 2026-10-22 |
| TCS: profit +15%, share -35% in 2026 (`tcs-q2-profit-share`) | active | FLAT | steady | 5 | H F F F | 4/41 | 206,469 | 801 | 8 | 2026-10-14 |
| SC orders panel on pharma freebies to doctors (`pharma-freebies-sc`) | active | COLD | steady | 5 | C C C C | 0/1 | 56,143 | 398 | 6 | 2026-10-23 |
| UPI merchant fee (0.4% MDR) may be deferred to 1 Jan (`upi-mdr-deferral`) | active | HOT | rising | 4 | H F H | 5/41 | 907,121 | 6,495 | 8 | 2026-10-16 |
| Inox Clean: revenue 43X, debt 45X, IPO on hold (`inox-clean-ipo`) | active | COLD | steady | 4 | C C C | 0/2 | 352,154 | 1,948 | 6 | 2026-10-24 |
| Musk calls Ambani 'Prime Minister Ambani' over Starlink (`musk-ambani-starlink`) | active | HOT | rising | 3 | H H | 2/43 | 6,750,511 | 109,241 | 9 | 2026-10-21 |
| US suspends TCS, Infosys, Wipro from green-card PERM; IT shares rise (`us-perm-indian-it`) | active | COLD | fading | 3 | H C | 0/1 | 1,305,201 | 4,441 | 8 | 2026-10-17 |
| SC on hospital drug markups: Rs 2,700 drug sold at Rs 27,000 (`hospital-drug-markup-sc`) | active | COLD | steady | 3 | C C | 0/0 | 6,395 | 39 | 6 | 2026-10-25 |
| HDFC Bank's new CEO ₹35.9 cr vs SBI chairman ₹43 lakh (`hdfc-ceo-pay-sbi`) | active | COLD | new | 2 | C | 0/1 | 90,898 | 796 | 9 | 2026-10-27 |
| Gauahar Khan's Versova duplex: 88% in 12 years (`gauahar-khan-flat`) | active | COLD | new | 2 | C | 0/0 | 2,119,627 | 21,490 | 6 | 2026-10-26 |
| Kohli and Anushka's ₹44 crore: three Versova flats, ready 2031 (`kohli-anushka-versova-flats`) | active | - | new | 1 |  | -/- | 0 | 0 | 8 | 2026-10-20 |
| Rupee near ₹97: RBI hike, then four emergency measures (`rbi-rupee-rescue`) | active | - | new | 1 |  | -/- | 0 | 0 | 7 | 2026-10-20 |
| Ramayana producer's Prime Focus searched by Income Tax (`prime-focus-ramayana`) | retired: COLD on 2 checks running | COLD | steady | 6 | H H H H C C | 0/0 | 1,056,196 | 7,548 | 8 | 2026-11-10 |
| EPF wage ceiling raised to ₹25,000 (`epf-wage-ceiling`) | retired: COLD on 2 checks running | COLD | fading | 6 | F F C C | 0/7 | 20,051 | 152 | - | - |
| Snapdeal (AceVector) after listing (`snapdeal-acevector`) | retired (E8): COLD on 2 checks running | COLD | steady | 6 | C C | 0/1 | 100,780 | 770 | - | - |
| Nana Patekar dies; the Rs 1.5 crore car he gave up for farmers (`nana-patekar`) | retired (E10): past its window | HOT | rising | 6 | R H H H | 100/100 | 27,305,534 | 110,559 | 7 | 2026-10-11 |
| Sensex -1,045 on 8 Oct: ₹10.23 lakh crore wiped off (`market-crash-oct8`) | retired: past its window | HOT | rising | 5 | H H C H | 9/17 | 3,239,882 | 14,656 | 9 | 2026-10-12 |

## Latest notes
- **Jio Platforms IPO:** 2026-10-10: 2026-10-10: Bloomberg band ₹1,065-1,119, ~₹30,213 cr, valuation ~07 bn; RHP expected Mon 12 Oct
- **Jio Platforms IPO:** 2026-10-11: 11 Oct: no RHP yet; documents expected week of 12 Oct; Musk-Ambani row (story musk-ambani-starlink) is its newest turn
- **International ETFs trading far above NAV (NSE warning):** First sent 8 Oct (deep lane). NSE caution 7 Oct; BSE 25 Sep.
- **TCS: profit +15%, share -35% in 2026:** First sent 9 Oct. Q2 profit ₹13,884 cr; +4,258 staff; AI $3.1 bn.
- **SC orders panel on pharma freebies to doctors:** First sent 9 Oct (deep lane). Order 8 Oct; panel reports in ~2 months; hearing 29 Jan 2027.
- **UPI merchant fee (0.4% MDR) may be deferred to 1 Jan:** 2026-10-13: 13 Oct: no decision yet, 15 Oct stands; IIT-Bombay study says 0.08% (PTI, 11 Oct)
- **UPI merchant fee (0.4% MDR) may be deferred to 1 Jan:** 2026-10-13: 13 Oct: no decision yet, 15 Oct stands; IIT-Bombay study says 0.08% (PTI, 11 Oct)
- **Inox Clean: revenue 43X, debt 45X, IPO on hold:** First sent 10 Oct (via The Ken, 9 Oct). SEBI observations in abeyance.
- **Musk calls Ambani 'Prime Minister Ambani' over Starlink:** First sent 11 Oct. Musk posts 8-10 Oct; govt: same stage for all three satcom operators; Jio 1,600-satellite plan; ties to Jio IPO 21 Oct.
- **Musk calls Ambani 'Prime Minister Ambani' over Starlink:** 2026-10-12: Musk promises affordable Starlink (Sat 10 Oct); Jio targets $106 bn
- **US suspends TCS, Infosys, Wipro from green-card PERM; IT shares rise:** First sent 11 Oct. Suspension 8 Oct; Nifty IT +1,000 pts at one stage 9 Oct; The Ken: Infosys 0 certifications since 2023.
- **SC on hospital drug markups: Rs 2,700 drug sold at Rs 27,000:** First sent 11 Oct. Hearings 22 and 29 Sep; 16% uniform margin suggested; Centre's reply due at the 12 Oct hearing.
- **HDFC Bank's new CEO ₹35.9 cr vs SBI chairman ₹43 lakh:** Bagchi package via postal ballot; desk 12 Oct
- **Gauahar Khan's Versova duplex: 88% in 12 years:** creator-format option; desk 12 Oct
- **Kohli and Anushka's ₹44 crore: three Versova flats, ready 2031:** First sent 13 Oct. Godrej Skyshore, 3 flats ₹44 cr, stamp duty ~₹2.49 cr, possession 30 Jun 2031.
- **Rupee near ₹97: RBI hike, then four emergency measures:** First sent 13 Oct. Repo 5.50% (7 Oct); ₹96.73 → ₹95.76 on 12 Oct; 99% daily CRR from 16 Oct.
