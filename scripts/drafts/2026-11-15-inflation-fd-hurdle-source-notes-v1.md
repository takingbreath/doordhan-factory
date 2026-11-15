# Inflation / FD hurdle — primary sources and arithmetic

Status: DRAFT — SOURCE NOTES FOR UNAPPROVED HOOK/STORY. Checked 15 November 2026 IST. Writer verification only, not independent final review of a Roman Hinglish script.

## Headline inflation: official release

[MoSPI / PIB, October 2026 CPI release, 12 November 2026](https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=2335416&lang=2&reg=48).

The official release gives provisional all-India combined CPI inflation of **6.09%**, October 2026 versus October 2025, on the 2024 base. It is year-on-year, not October's one-month price change. The next year's inflation and an individual household's spending basket may differ. Keep the past-data/future-example distinction in the actual script.

The story uses the headline CPI only. CFPI and food-and-beverages are distinct groupings and do not need to be mixed into this calculation. No monetary-policy prediction or claim about formal inflation-target failure is made.

## FD card rate: verify the bank, not the aggregator

[SBI retail domestic term-deposit rate table](https://sbi.bank.in/web/interest-rates/deposit-rates/retail-domestic-term-deposits?inheritRedirect=true).

Opened the official page and read the below-Rs-3-crore table: the general-public 1-year-to-under-2-year band is **6.25% p.a.**, with the rate column effective **15 December 2025**. The page is marked last updated 19 October 2026. The separately labelled non-callable 1-year rate is 6.40%; senior rates and special-tenor schemes also differ. Do not substitute them or claim the 6.25% was newly raised in October/November.

The source is now the bank's own table, resolving the desk's reliance on an old aggregator card for this claim. This remains a posted rate checked today, not a live customer quote or a reconstruction of effective yield under a particular payout/compounding option. Recheck before voice if the story is delayed.

## Independent arithmetic, with explicit assumptions

One-year illustrative cash flow, no fees: assumed annual price growth p = 0.0609; assumed effective tax on interest t = 0.30. Let r be the gross one-year return, and assume the interest tax is paid from the example's interest over that horizon.

For unchanged purchasing power:

`(1 + r * (1 - t)) / (1 + p) = 1`

Therefore `r = p / (1 - t) = 0.0609 / 0.70 = 0.087`, or **8.7%**. After the assumed tax, `8.7% * 70% = 6.09%`. The resulting real gain is zero, not 8.7% and not 6.09%.

Verified with Python Decimal. Diagnostic only: for a separately assumed simple gross annual return of 6.25%, net nominal return is 4.375% and exact real return is about -1.6166% under the same assumptions. These diagnostic numbers are not in the proposed story; do not call this a precise calculation of an actual SBI maturity value. Card-rate compounding and tax timing can change the effective result.

Thirty percent is a modelling input, not legal guidance, not a claim about all viewers and not shorthand for an actual statutory slab including cess/surcharge. If adding a real person's tax position or a legal tax claim, independently verify the applicable rules and exemptions. No product or asset-class recommendation follows from the hurdle.

## Intake and preservation

LATEST matches research/desk/2026-11-15.md byte-for-byte. Read full TRACKER, current collaboration notes, prosody/story checkpoints and approved jio01. Today's recommendation comes from the desk's second option; story/hook suggestions in the research are not instructions. The Nvidia contract story remains pending, and the new petition count does not change its underlying mechanism. No new human approval of these daily proposals was found.

Research files are read-only. Existing tracked collaboration edits and all pre-existing untracked eMudhra, FD/loan, silver and space/semiconductor manuscripts are preserved. Only the two dated 15 November draft documents are to be staged/pushed.

Next: human hook/story approval, one Roman Hinglish script, independent editorial/final fact review of the actual words, then human voice review. The 30–40-second target is for that subsequent script; no recording or measured duration exists. No audio, spending, script freeze, video generation, public publishing or unsolicited external message is authorized here.
