# Story tracker

_Written 2026-10-28 by `pipeline/story_tracker.py md`. Data: registry/story_tracker.json._

Every story the desk has sent stays here until it leaves the news cycle (COLD on two checks running, or past its window). Each morning `story_tracker.py check` measures them all again.

Label history reads oldest to newest: H hot, R rising, F flat, C cold.

| Story | Status | Now | Direction | Day | History | News today/week | YouTube views this week | Best views/hr | Desk score | Window |
|---|---|---|---|---|---|---|---|---|---|---|
| Jio Platforms IPO (`jio-ipo`) | active | HOT | rising | 21 | H H H H H R H | 48/100 | 309,764 | 7,233 | 9 | 2026-10-31 |
| Airtel Money lists in London at $7 bn (via The Ken) (`airtel-money-london`) | active | FLAT | fading | 14 | F F F F F R F | 9/33 | 269,249 | 2,715 | 6 | 2026-10-29 |
| Mutual funds halt new gold FoF SIPs and bulk gold ETF buys (`gold-fund-halt`) | active | RISING | rising | 13 | F F F F F F R | 14/18 | 150,692 | 725 | 9 | 2026-11-08 |
| Insurance mis-selling complaints +14%; IRDAI crackdown may slip (via The Ken) (`insurance-misselling-ken`) | active | HOT | rising | 12 | C C C C C C H | 0/0 | 188,207 | 3,651 | 6 | 2026-10-31 |
| Groww's F&O share of revenue falls to 45%; turns to IPOs and wealth (via The Arc) (`groww-derivatives-arc`) | active | COLD | rising | 11 | C C C C C C C | 0/0 | 93,148 | 566 | 7 | to about Fri 23 Oct |
| Air India FY26 loss ₹22,238 cr (~₹61 cr a day); SIA as saviour (via The Ken) (`air-india-loss-ken`) | active | COLD | rising | 9 | C C C H C C C | 0/0 | 39,289 | 1,300 | 6 | 2026-11-02 |
| Silver -46% from January record (₹3,84,632 → ₹2,08,380/kg) before Dhanteras (`silver-crash-46`) | active | HOT | rising | 8 | H H H H H H H | 4/9 | 848,017 | 2,713 | 7 | 2026-11-08 |
| Urban Company loss triples on InstaHelp: ₹114 booking, ₹279 loss (via The Morning Context) (`urban-company-instahelp`) | active | COLD | rising | 8 | C C C C C C C | 1/2 | 143,169 | 1,229 | 7 | 2026-11-03 |
| Oil at $112: shares, gold and silver fell the same day (`oil-slide-everything`) | active | HOT | steady | 6 | H H H H H | 0/2 | 1,959,203 | 25,081 | 8 | 2026-10-29 |
| SEBI final order: Avadhut Sathe ₹546 cr refund (`avadhut-sathe-refund`) | active | HOT | rising | 5 | R F H H | 1/25 | 372,703 | 6,555 | 6 | 2026-10-30 |
| NSE unlisted buyers below IPO price (The Ken) (`nse-unlisted-regret-ken`) | active | HOT | rising | 5 | H C C H | 1/5 | 584,971 | 7,057 | 7 | 2026-11-07 |
| Swiggy record low, less than half its IPO price; Instamart loss ₹895 cr (`swiggy-record-low`) | active | FLAT | fading | 4 | F F F | 0/32 | 175,462 | 780 | 9 | 2026-10-28 |
| Jio's prepaid (77% of revenue) sold only via Reliance Retail (via The Ken) (`jio-reliance-retail-ken`) | active | HOT | rising | 4 | C C H | 0/0 | 566,475 | 6,214 | 8 | 2026-11-04 |
| Gold ₹38,000 below January peak, ₹5,560/10g down in 3 days, before Dhanteras (`gold-dhanteras-fall`) | active | HOT | steady | 3 | H H | 0/3 | 1,233,073 | 7,325 | 7 | 2026-11-06 |
| HDFC Bank's first outside CEO starts; share ~30% down in a year (via The Morning Context) (`hdfc-bank-bagchi`) | active | FLAT | new | 2 | F | 4/19 | 145,847 | 980 | 8 | 2026-11-03 |
| Jewellery makers' IPO wave: money goes to gold and debt (via The Ken) (`jewellery-ipo-ken`) | active | - | new | 1 |  | -/- | 0 | 0 | 5 | 2026-11-06 |
| Ramayana producer's Prime Focus searched by Income Tax (`prime-focus-ramayana`) | retired: COLD on 2 checks running | COLD | steady | 21 | H H H H C C | 0/0 | 1,056,196 | 7,548 | 8 | 2026-11-10 |
| International ETFs trading far above NAV (NSE warning) (`intl-etf-premium`) | retired: past its window | COLD | fading | 21 | C C C H H H C | 0/- | 438,146 | 4,086 | 6 | 2026-10-22 |
| EPF wage ceiling raised to ₹25,000 (`epf-wage-ceiling`) | retired: COLD on 2 checks running | COLD | fading | 21 | F F C C | 0/7 | 20,051 | 152 | - | - |
| Snapdeal (AceVector) after listing (`snapdeal-acevector`) | retired (E8): COLD on 2 checks running | COLD | steady | 21 | C C | 0/1 | 100,780 | 770 | - | - |
| Nana Patekar dies; the Rs 1.5 crore car he gave up for farmers (`nana-patekar`) | retired (E10): past its window | HOT | rising | 21 | R H H H | 100/100 | 27,305,534 | 110,559 | 7 | 2026-10-11 |
| Sensex -1,045 on 8 Oct: ₹10.23 lakh crore wiped off (`market-crash-oct8`) | retired: past its window | HOT | rising | 20 | H H C H | 9/17 | 3,239,882 | 14,656 | 9 | 2026-10-12 |
| TCS: profit +15%, share -35% in 2026 (`tcs-q2-profit-share`) | retired: past its window | HOT | rising | 20 | H F F F F H | 7/48 | 464,093 | 10,346 | 8 | 2026-10-14 |
| SC orders panel on pharma freebies to doctors (`pharma-freebies-sc`) | retired: past its window | COLD | fading | 20 | H H H C C C C | 0/0 | 445,730 | 1,054 | 6 | 2026-10-23 |
| UPI merchant fee (0.4% MDR) may be deferred to 1 Jan (`upi-mdr-deferral`) | retired: past its window | HOT | rising | 19 | H F H H H H H | 2/41 | 910,815 | 4,784 | 6 | 2026-10-16 |
| Inox Clean: revenue 43X, debt 45X, IPO on hold (`inox-clean-ipo`) | retired: past its window | COLD | fading | 19 | H C C C C C C | 0/0 | 29,731 | 131 | 6 | 2026-10-24 |
| Musk calls Ambani 'Prime Minister Ambani' over Starlink (`musk-ambani-starlink`) | retired: past its window | FLAT | fading | 18 | F F H H H H F | 1/10 | 4,347,306 | 14,666 | 8 | 2026-10-21 |
| US suspends TCS, Infosys, Wipro from green-card PERM; IT shares rise (`us-perm-indian-it`) | retired: COLD on 2 checks running | COLD | steady | 18 | H C C | 0/1 | 1,195,114 | 3,721 | 8 | 2026-10-17 |
| SC on hospital drug markups: Rs 2,700 drug sold at Rs 27,000 (`hospital-drug-markup-sc`) | retired: past its window | HOT | rising | 18 | H C C C C C H | 0/0 | 168,581 | 6,896 | 6 | 2026-10-25 |
| HDFC Bank's new CEO ₹35.9 cr vs SBI chairman ₹43 lakh (`hdfc-ceo-pay-sbi`) | retired: COLD on 2 checks running | COLD | fading | 17 | C C | 0/1 | 8,051 | 55 | 9 | 2026-10-27 |
| Gauahar Khan's Versova duplex: 88% in 12 years (`gauahar-khan-flat`) | retired: past its window | COLD | fading | 17 | C C H C C C C | 0/0 | 0 | 0 | 6 | 2026-10-26 |
| Kohli and Anushka's ₹44 crore: three Versova flats, ready 2031 (`kohli-anushka-versova-flats`) | retired: COLD on 2 checks running | COLD | fading | 16 | C C | 0/0 | 598 | 25 | 8 | 2026-10-20 |
| Rupee near ₹97: RBI hike, then four emergency measures (`rbi-rupee-rescue`) | retired: COLD on 2 checks running | COLD | rising | 16 | H H H C C | 0/9 | 1,516,191 | 14,931 | 7 | 2026-10-20 |
| Zoho freezes pay rises over AI and server costs (`zoho-pay-freeze`) | retired: COLD on 2 checks running | COLD | rising | 15 | H C C | 0/2 | 287,736 | 1,847 | 9 | 2026-10-20 |
| Sensex +1,109 partly on FM's LTCG remark (`ltcg-remark-rally`) | retired: COLD on 2 checks running | COLD | fading | 15 | H H H H C C | 0/1 | 1,266,936 | 3,079 | 8 | 2026-10-20 |
| Gold ₹3,600 cheaper in four sessions on a stronger rupee (`gold-slide-rupee`) | retired: past its window | RISING | rising | 14 | H R R F R | 31/85 | 175,924 | 2,637 | 8 | 2026-10-19 |
| Yes Bank -14.5% after SC voids AT-1 write-off (`yes-bank-at1-sc`) | retired: past its window | FLAT | steady | 13 | R H F F F | 2/36 | 452,328 | 1,618 | 8 | 2026-10-20 |
| Zetwerk IPO: 54% of Q1 revenue from metal sales (`zetwerk-ipo-metals`) | retired: past its window | FLAT | rising | 13 | F F R F F C F | 7/31 | 159,682 | 735 | 7 | 2026-10-23 |
| IDBI Bank sold to Fairfax at ₹81 vs ₹90 market (`idbi-fairfax-sale`) | retired: COLD on 2 checks running | COLD | fading | 12 | H H H F H C C | 1/4 | 255,768 | 1,751 | 9 | 2026-10-24 |
| ED raids WhatsApp 'Multibagger' pump-and-dump (RM Drip, R&B Denims) (`ed-whatsapp-multibagger`) | retired: COLD on 2 checks running | COLD | rising | 12 | C C | 0/3 | 230 | 5 | 7 | 2026-10-22 |
| Green-card freeze 'bloodbath' reels, then Indian IT's best week since 2008 (`it-rally-green-card`) | retired: COLD on 2 checks running | COLD | steady | 11 | C H C C | 1/3 | 38,873 | 1,467 | 9 | to about Wed 21 Oct |
| Expired food allegedly back on sale: FIR names Reliance, Blinkit directors (`expired-food-reliance-blinkit`) | retired: COLD on 2 checks running | COLD | rising | 11 | C C | 0/0 | 27,744 | 247 | 8 | to about Tue 20 Oct |
| Axis Bank: profit +38%, shares -5% (base effect of last year's ₹1,231 cr provision) (`axis-bank-q2-fall`) | retired: past its window | RISING | rising | 9 | R R R R | 38/66 | 300,690 | 1,158 | 8 | 2026-10-23 |
| eMudhra -20% lower circuit after its certificate keys turned out to be tiny numbers (one was 4) (`emudhra-key-4`) | retired: past its window | FLAT | rising | 7 | H H F F F F | 0/12 | 191,204 | 552 | 9 | 2026-10-27 |
| RBI Governor: upper-layer CICs like Tata Sons must list (`tata-sons-listing`) | retired: COLD on 2 checks running | COLD | steady | 4 | C C | 0/2 | 135,201 | 1,538 | 8 | 2026-11-08 |

## Latest notes
- **Jio Platforms IPO:** 2026-10-27: 27 Oct: refunds today, listing Wed 28 Oct; ₹10.3 lakh cr at issue vs HDFC Bank ₹10.62 lakh cr
- **Jio Platforms IPO:** 2026-10-28: 28 Oct: listing day; record passes from Reliance Power 2008 (closed -17% day one)
- **Airtel Money lists in London at $7 bn (via The Ken):** First sent 15 Oct. £1.96, £5.3 bn; 270m shares; flat debut 9 Oct; admission 14 Oct.
- **Mutual funds halt new gold FoF SIPs and bulk gold ETF buys:** 2026-10-23: 23 Oct: The Core: eighth rupee-defence step, 2013 parallel
- **Mutual funds halt new gold FoF SIPs and bulk gold ETF buys:** 2026-10-28: 28 Oct: digital gold +83% y/y to Rs 2,590 cr (Sep) despite SEBI warning; FoF still shut
- **Insurance mis-selling complaints +14%; IRDAI crackdown may slip (via The Ken):** First sent 17 Oct. Comments due 25 Oct
- **Groww's F&O share of revenue falls to 45%; turns to IPOs and wealth (via The Arc):** 2026-10-22: 22 Oct: The Ken 'hostage to options'; Groww PAT ₹725 cr, F&O 44.8% of revenue; SEBI FY26 87.7% lose
- **Air India FY26 loss ₹22,238 cr (~₹61 cr a day); SIA as saviour (via The Ken):** sent 20 Oct
- **Silver -46% from January record (₹3,84,632 → ₹2,08,380/kg) before Dhanteras:** sent 21 Oct
- **Silver -46% from January record (₹3,84,632 → ₹2,08,380/kg) before Dhanteras:** 2026-10-22: 22 Oct: no new turn; still HOT on YouTube
- **Urban Company loss triples on InstaHelp: ₹114 booking, ₹279 loss (via The Morning Context):** sent 21 Oct
- **Oil at $112: shares, gold and silver fell the same day:** sent 23 Oct
- **SEBI final order: Avadhut Sathe ₹546 cr refund:** final order 23 Oct; refund 546.17 cr + 67.87 cr interest
- **SEBI final order: Avadhut Sathe ₹546 cr refund:** 2026-10-27: 27 Oct: on the wire, not sent as a slot
- **NSE unlisted buyers below IPO price (The Ken):** via The Ken 23 Oct
- **Swiggy record low, less than half its IPO price; Instamart loss ₹895 cr:** Q2 FY27; fell as much as 17% on 23 Oct
- **Jio's prepaid (77% of revenue) sold only via Reliance Retail (via The Ken):** The Ken 22 Oct; RHP figures via Fortune India 15 Oct
- **Jio's prepaid (77% of revenue) sold only via Reliance Retail (via The Ken):** 2026-10-26: carried for Wed listing
- **Gold ₹38,000 below January peak, ₹5,560/10g down in 3 days, before Dhanteras:** sent 26 Oct
- **Gold ₹38,000 below January peak, ₹5,560/10g down in 3 days, before Dhanteras:** 2026-10-27: 27 Oct: flat at ₹1,42,760/10g Mumbai; no new turn
- **HDFC Bank's first outside CEO starts; share ~30% down in a year (via The Morning Context):** sent 27 Oct; Bagchi from 27 Oct; ₹688.05 close 26 Oct, 52w low ₹681.90
- **Jewellery makers' IPO wave: money goes to gold and debt (via The Ken):** sent 28 Oct; 8 mainboard IPOs in 2026; Deepa 86% of fresh issue to inventory
