# Silver ETF flows — primary tables and calculation

Status: DRAFT — SUPPORTS AN UNAPPROVED HOOK/STORY. Writer verification on 23 November 2026 IST. Independent final checks still apply to the eventual manuscript.

## Primary inputs

Read page 1, section VII, row v “Silver ETF”, including the column headings, in AMFI's [September 2026 report](https://portal.amfiindia.com/spages/amsep2026repo.pdf) and [October 2026 report](https://portal.amfiindia.com/spages/amoct2026repo.pdf). Amounts below are INR crore.

| Month | Funds mobilised | Repurchase/redemption | Published net inflow |
|---|---:|---:|---:|
| September 2026 | 7,308.79 | 5,334.48 | 1,974.32 |
| October 2026 | 6,406.78 | 3,314.56 | 3,092.22 |

The money columns are distinct from folios, AUM and average AUM. Neither report measures all exchange purchases and sales. Do not add domestic fund-of-funds data to the ETF row; that would risk counting underlying investment twice.

## Calculation checked with Python Decimal

- Published net inflow growth: `(3092.22 / 1974.32 - 1) × 100 = 56.622027%`, rounded 57%.
- Funds mobilised change: `(6406.78 / 7308.79 - 1) × 100 = -12.341441%`.
- Redemptions change: `(3314.56 / 5334.48 - 1) × 100 = -37.865359%`.
- Gross mobilisation fell ₹902.01 crore; redemptions fell ₹2,019.92 crore. This explains the higher net amount. Published net increase is ₹1,117.90 crore.

The displayed September components subtract to ₹1,974.31 crore, one hundredth below the published net. The change calculated from displayed components is correspondingly ₹1,117.91 crore. Preserve the published net totals and note the small precision discrepancy rather than silently altering them. It does not affect rounded percentages or the argument. Spoken whole-crore amounts are 7,309 / 6,407 and 5,334 / 3,315.

“More money arriving” is the apparent gross-flow reading being tested; more money did enter on a net basis. Never claim the net increase itself is false. Lower rupee redemption amounts do not establish lower selling in units, fewer sellers or a motive to hold; prices can affect rupee flows. No claim about investor returns or price causation follows from these tables.

## Reporting and freshness

[Kotak Neo's 11 November AMFI report](https://www.kotakneo.com/news/mutual-funds/gold-silver-etf-inflows-october-2026/) supplies the desk's headline lead. The primary tables, rather than headline wording, establish the flow distinction.

[Upstox, 20 November, updated 13:20 IST](https://upstox.com/news/market-news/commodities/gold-silver-prices-crash-mcx-gold-nears-1-21-lakh-silver-plunges-10-614-kg-here-s-why/article-203760/) was opened and read for the current silver-selloff context. Its ₹1,46,868/kg quote is a Friday intraday MCX low, not a closing or live Monday price. The proposed words contain no price level, target, exact peak comparison or causal market forecast.

The desk's 23 November BusinessToday closing-price link was inaccessible to the browsing tool. Do not claim that body or its ₹1,47,813 close was independently read. It is not used in the story. No current November ETF totals are inferred from October data. Technical commodity-price explanations and buy/sell suggestions are unnecessary here.

## Intake and handoff

Checked dirty work before fetching; incoming files did not overlap with it. Pulled main fast-forward only to c8439cf. LATEST matches the dated 23 November research byte-for-byte. Consulted today's three options, tracker, collaboration instructions, repo rules, story/prosody guidance, current strategy/learning/platform changes and the approved jio01 script and actual approval record. No fresh human approval was found.

Research files remain read-only. Stage only this source note and the paired new story proposal. Preserve yesterday's IndusInd proposal, previous drafts, the modified collaboration document and all untracked human work. No paid call, audio, registry freeze, video, public publishing or cross-chat message. Approval of the hook/story is the next checkpoint.
