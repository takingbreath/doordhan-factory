# Reliance earnings bridge — verification, 3 November 2026

Status: SOURCE NOTES FOR AN UNAPPROVED HOOK/STORY. Writer verification only; final independent review remains pending. Research files and existing local work remain untouched.

## Company evidence inspected

Opened [Reliance's financial-reporting page and Q2 FY27 management transcript](https://www.ril.com/investors/financial-reporting). Management describes O2C EBITDA up about 68%, stronger transportation-fuel cracks and chemical margins, cost headwinds, flexible crude sourcing and high utilisation. Diesel alone does not explain the full segment: the Q&A explicitly describes a combined refining/petrochemical/operational contribution. These are company explanations, not independently measured effects of each factor.

Opened the company's signed 30 October [media release reproduced by FinancialFilings](https://financialfilings.com/filings/reliance-industries-ltd/earnings-release/2026/75111477/) and its [23-page PDF copy](https://cdn.financialreports.eu/financialreports/media/filings/58986/2026/RNS/58986_rns_2026-10-30_029abb55-2c00-4622-9b26-f0f30d5b0059.pdf). The copy includes the exchange cover letter, so printed page 1 is PDF page 2. Read the parsed consolidated and O2C tables; a screenshot request for the O2C page failed with a cache miss, so no complete visual-table verification is claimed.

## Reproducible calculation

All amounts are ₹ crore. Both columns compare Q2 FY27, quarter ended September 2026, with Q2 FY26. Do not mix this with sequential growth or a half-year comparison.

| Reported measure | Q2 FY27 | Q2 FY26 | Increase |
| --- | ---: | ---: | ---: |
| Consolidated EBITDA — printed p1 | 62,409 | 50,367 | 12,042 |
| O2C segment EBITDA — printed p13 | 25,203 | 15,008 | 10,195 |

Writer's calculation, checked in Python:

`(25,203 − 15,008) / (62,409 − 50,367) × 100 = 84.6620%`, rounded to roughly **85% of the year-on-year EBITDA increase**.

This is an arithmetic comparison, not a separately reported company metric or a causal allocation of the stock rally. The segment was about 40.4% of total current-quarter EBITDA, so “85% of Reliance's EBITDA/profit came from oil” would be false. Net group growth can include offsetting changes in other businesses and consolidation effects. Do not describe the ratio as a gross share of all positive segment increases, or multiply it by the share-price move.

## Market-event check

Opened [Upstox's 2 November closing market report](https://upstox.com/news/market-news/stocks/market-wrap-nov-2-sensex-zooms-1-233-pts-nifty-50-ends-at-23-441-as-crude-oil-prices-ease-reliance-industries-soars-12/article-202833/): RIL closed up 11.6% following results, with O2C highlighted. [Moneycontrol's 2 November report](https://www.moneycontrol.com/news/business/markets/reliance-industries-shares-jump-over-4-after-record-q2-results-top-nifty-gainer-biggest-index-contributor-14065973.html) surfaced in fresh search, corroborating nearly 12%; not used as a substitute for the primary financial tables. The Yahoo/Bloomberg link returned 429. Omit its record/$19bn/80%-discount claims from this proposal rather than implying that article was inspected.

## Final-version boundaries

- EBITDA is the consistent metric for the bridge. Do not replace it with PAT, profit attributable to owners, cash earnings or free cash flow. The release and news use several different profit/revenue definitions; none is needed here.
- O2C includes refining and chemicals. Stronger cracks are product-versus-crude spreads, not Reliance's final net refining profit after every cost. Freight, insurance, crude premiums, export levies and domestic fuel under-recoveries were headwinds, according to the company.
- The period explains a reported quarter. It does not establish that high oil prices always help refiners, that war automatically raises their profits, or that these margins persist. No forecast, buy/sell/hold instruction, analyst rating, share-price level or target.
- No Ambani wealth increase, universal SIP exposure, Jio stake valuation or claim that all investors bought for the same reason. Preserve the difference between the operating explanation and the market's full reaction.
- Put detailed source/calculation credits in visuals or caption. Caption convention: “Not investment advice”. No fabricated executive quotations or photos generated as real people.

## Handoff

Push this explicitly unapproved proposal/source pair only. Research files stay read-only. Human hook/story approval, scripting, independent final checks and human voice review remain pending. Do not freeze, spend on production, publicly publish or message another task.
