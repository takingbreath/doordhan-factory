# Story tracker

_Written 2026-10-21 by `pipeline/story_tracker.py md`. Data: registry/story_tracker.json._

Every story the desk has sent stays here until it leaves the news cycle (COLD on two checks running, or past its window). Each morning `story_tracker.py check` measures them all again.

Label history reads oldest to newest: H hot, R rising, F flat, C cold.

| Story | Status | Now | Direction | Day | History | News today/week | YouTube views this week | Best views/hr | Desk score | Window |
|---|---|---|---|---|---|---|---|---|---|---|
| Jio Platforms IPO (`jio-ipo`) | active | HOT | rising | 14 | R H H H H R H | 54/100 | 2,233,094 | 27,799 | 9 | 2026-10-31 |
| International ETFs trading far above NAV (NSE warning) (`intl-etf-premium`) | active | HOT | steady | 14 | C C C C C H H | 0/0 | 445,080 | 7,445 | 6 | 2026-10-22 |
| SC orders panel on pharma freebies to doctors (`pharma-freebies-sc`) | active | COLD | fading | 13 | C C H H H H C | 0/0 | 1,012,061 | 2,414 | 6 | 2026-10-23 |
| Inox Clean: revenue 43X, debt 45X, IPO on hold (`inox-clean-ipo`) | active | COLD | rising | 12 | C C H H H C C | 0/2 | 651,053 | 5,206 | 6 | 2026-10-24 |
| Musk calls Ambani 'Prime Minister Ambani' over Starlink (`musk-ambani-starlink`) | active | HOT | steady | 11 | F F F H H H H | 0/13 | 6,585,909 | 22,409 | 8 | 2026-10-21 |
| SC on hospital drug markups: Rs 2,700 drug sold at Rs 27,000 (`hospital-drug-markup-sc`) | active | COLD | fading | 11 | C C C C C H C | 0/0 | 426,475 | 3,896 | 6 | 2026-10-25 |
| Gauahar Khan's Versova duplex: 88% in 12 years (`gauahar-khan-flat`) | active | COLD | fading | 10 | C C C C C C C | 0/0 | 14,701 | 131 | 6 | 2026-10-26 |
| Airtel Money lists in London at $7 bn (via The Ken) (`airtel-money-london`) | active | FLAT | steady | 7 | H H F F F F | 4/56 | 3,038,994 | 10,337 | 6 | 2026-10-29 |
| Mutual funds halt new gold FoF SIPs and bulk gold ETF buys (`gold-fund-halt`) | active | FLAT | fading | 6 | R H H H F | 8/65 | 1,126,196 | 2,442 | 8 | 2026-11-08 |
| Zetwerk IPO: 54% of Q1 revenue from metal sales (`zetwerk-ipo-metals`) | active | FLAT | fading | 6 | F F F R F | 10/48 | 292,983 | 1,127 | 7 | 2026-10-23 |
| IDBI Bank sold to Fairfax at ₹81 vs ₹90 market (`idbi-fairfax-sale`) | active | FLAT | fading | 5 | H H H F | 0/33 | 601,861 | 1,363 | 9 | 2026-10-24 |
| Insurance mis-selling complaints +14%; IRDAI crackdown may slip (via The Ken) (`insurance-misselling-ken`) | active | COLD | steady | 5 | C C C C | 0/1 | 22,082 | 92 | 6 | 2026-10-31 |
| Green-card freeze 'bloodbath' reels, then Indian IT's best week since 2008 (`it-rally-green-card`) | active | COLD | fading | 4 | C H C | 0/2 | 273,530 | 2,135 | 9 | to about Wed 21 Oct |
| Groww's F&O share of revenue falls to 45%; turns to IPOs and wealth (via The Arc) (`groww-derivatives-arc`) | active | COLD | steady | 4 | C C C | 0/0 | 143,690 | 844 | 6 | to about Fri 23 Oct |
| Axis Bank: profit +38%, shares -5% (base effect of last year's ₹1,231 cr provision) (`axis-bank-q2-fall`) | active | RISING | new | 2 | R | 13/19 | 106,895 | 576 | 8 | 2026-10-23 |
| Air India FY26 loss ₹22,238 cr (~₹61 cr a day); SIA as saviour (via The Ken) (`air-india-loss-ken`) | active | COLD | new | 2 | C | 0/0 | 875,467 | 5,967 | 6 | 2026-11-02 |
| Silver -46% from January record (₹3,84,632 → ₹2,08,380/kg) before Dhanteras (`silver-crash-46`) | active | - | new | 1 |  | -/- | 0 | 0 | 8 | 2026-11-08 |
| Urban Company loss triples on InstaHelp: ₹114 booking, ₹279 loss (via The Morning Context) (`urban-company-instahelp`) | active | - | new | 1 |  | -/- | 0 | 0 | 7 | 2026-11-03 |
| Ramayana producer's Prime Focus searched by Income Tax (`prime-focus-ramayana`) | retired: COLD on 2 checks running | COLD | steady | 14 | H H H H C C | 0/0 | 1,056,196 | 7,548 | 8 | 2026-11-10 |
| EPF wage ceiling raised to ₹25,000 (`epf-wage-ceiling`) | retired: COLD on 2 checks running | COLD | fading | 14 | F F C C | 0/7 | 20,051 | 152 | - | - |
| Snapdeal (AceVector) after listing (`snapdeal-acevector`) | retired (E8): COLD on 2 checks running | COLD | steady | 14 | C C | 0/1 | 100,780 | 770 | - | - |
| Nana Patekar dies; the Rs 1.5 crore car he gave up for farmers (`nana-patekar`) | retired (E10): past its window | HOT | rising | 14 | R H H H | 100/100 | 27,305,534 | 110,559 | 7 | 2026-10-11 |
| Sensex -1,045 on 8 Oct: ₹10.23 lakh crore wiped off (`market-crash-oct8`) | retired: past its window | HOT | rising | 13 | H H C H | 9/17 | 3,239,882 | 14,656 | 9 | 2026-10-12 |
| TCS: profit +15%, share -35% in 2026 (`tcs-q2-profit-share`) | retired: past its window | HOT | rising | 13 | H F F F F H | 7/48 | 464,093 | 10,346 | 8 | 2026-10-14 |
| UPI merchant fee (0.4% MDR) may be deferred to 1 Jan (`upi-mdr-deferral`) | retired: past its window | HOT | rising | 12 | H F H H H H H | 2/41 | 910,815 | 4,784 | 6 | 2026-10-16 |
| US suspends TCS, Infosys, Wipro from green-card PERM; IT shares rise (`us-perm-indian-it`) | retired: COLD on 2 checks running | COLD | steady | 11 | H C C | 0/1 | 1,195,114 | 3,721 | 8 | 2026-10-17 |
| HDFC Bank's new CEO ₹35.9 cr vs SBI chairman ₹43 lakh (`hdfc-ceo-pay-sbi`) | retired: COLD on 2 checks running | COLD | fading | 10 | C C | 0/1 | 8,051 | 55 | 9 | 2026-10-27 |
| Kohli and Anushka's ₹44 crore: three Versova flats, ready 2031 (`kohli-anushka-versova-flats`) | retired: COLD on 2 checks running | COLD | fading | 9 | C C | 0/0 | 598 | 25 | 8 | 2026-10-20 |
| Rupee near ₹97: RBI hike, then four emergency measures (`rbi-rupee-rescue`) | retired: COLD on 2 checks running | COLD | rising | 9 | H H H C C | 0/9 | 1,516,191 | 14,931 | 7 | 2026-10-20 |
| Zoho freezes pay rises over AI and server costs (`zoho-pay-freeze`) | retired: COLD on 2 checks running | COLD | rising | 8 | H C C | 0/2 | 287,736 | 1,847 | 9 | 2026-10-20 |
| Sensex +1,109 partly on FM's LTCG remark (`ltcg-remark-rally`) | retired: COLD on 2 checks running | COLD | fading | 8 | H H H H C C | 0/1 | 1,266,936 | 3,079 | 8 | 2026-10-20 |
| Gold ₹3,600 cheaper in four sessions on a stronger rupee (`gold-slide-rupee`) | retired: past its window | RISING | rising | 7 | H R R F R | 31/85 | 175,924 | 2,637 | 8 | 2026-10-19 |
| Yes Bank -14.5% after SC voids AT-1 write-off (`yes-bank-at1-sc`) | retired: past its window | FLAT | steady | 6 | R H F F F | 2/36 | 452,328 | 1,618 | 8 | 2026-10-20 |
| ED raids WhatsApp 'Multibagger' pump-and-dump (RM Drip, R&B Denims) (`ed-whatsapp-multibagger`) | retired: COLD on 2 checks running | COLD | rising | 5 | C C | 0/3 | 230 | 5 | 7 | 2026-10-22 |
| Expired food allegedly back on sale: FIR names Reliance, Blinkit directors (`expired-food-reliance-blinkit`) | retired: COLD on 2 checks running | COLD | rising | 4 | C C | 0/0 | 27,744 | 247 | 8 | to about Tue 20 Oct |

## Latest notes
- **Jio Platforms IPO:** 2026-10-20: anchor book ₹2.5 lakh cr bids for ₹8,110 cr, 30x
- **Jio Platforms IPO:** 2026-10-21: 21 Oct: opens today; Reliance paid 4 lakh+ staff ~15 days early, helped open share accounts (Reuters)
- **International ETFs trading far above NAV (NSE warning):** First sent 8 Oct (deep lane). NSE caution 7 Oct; BSE 25 Sep.
- **SC orders panel on pharma freebies to doctors:** First sent 9 Oct (deep lane). Order 8 Oct; panel reports in ~2 months; hearing 29 Jan 2027.
- **Inox Clean: revenue 43X, debt 45X, IPO on hold:** First sent 10 Oct (via The Ken, 9 Oct). SEBI observations in abeyance.
- **Musk calls Ambani 'Prime Minister Ambani' over Starlink:** 2026-10-18: crowded; Reliance responded 16 Oct
- **Musk calls Ambani 'Prime Minister Ambani' over Starlink:** 2026-10-18: picked 18 Oct: link with Jio IPO
- **SC on hospital drug markups: Rs 2,700 drug sold at Rs 27,000:** First sent 11 Oct. Hearings 22 and 29 Sep; 16% uniform margin suggested; Centre's reply due at the 12 Oct hearing.
- **SC on hospital drug markups: Rs 2,700 drug sold at Rs 27,000:** 2026-10-19: NPPA caps trade margins at 30% on 137 cancer drugs from 9 Nov; up to 70% cheaper (Moneylife)
- **Gauahar Khan's Versova duplex: 88% in 12 years:** creator-format option; desk 12 Oct
- **Airtel Money lists in London at $7 bn (via The Ken):** First sent 15 Oct. £1.96, £5.3 bn; 270m shares; flat debut 9 Oct; admission 14 Oct.
- **Zetwerk IPO: 54% of Q1 revenue from metal sales:** via The Ken
- **IDBI Bank sold to Fairfax at ₹81 vs ₹90 market:** First sent 17 Oct. ₹52,878 cr for 60.72% (govt 30.48, LIC 30.24); ₹81 vs ₹90.40 close; −7% on 15 Oct
- **Insurance mis-selling complaints +14%; IRDAI crackdown may slip (via The Ken):** First sent 17 Oct. Comments due 25 Oct
- **Axis Bank: profit +38%, shares -5% (base effect of last year's ₹1,231 cr provision):** sent 20 Oct
- **Air India FY26 loss ₹22,238 cr (~₹61 cr a day); SIA as saviour (via The Ken):** sent 20 Oct
- **Silver -46% from January record (₹3,84,632 → ₹2,08,380/kg) before Dhanteras:** sent 21 Oct
- **Urban Company loss triples on InstaHelp: ₹114 booking, ₹279 loss (via The Morning Context):** sent 21 Oct
