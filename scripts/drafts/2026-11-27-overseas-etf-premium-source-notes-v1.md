# Overseas ETF premiums — primary sources and hypothetical arithmetic

Status: DRAFT — SUPPORTS AN UNAPPROVED HOOK/STORY. Writer verification on 27 November 2026 IST. Independent final checks remain required for the actual later manuscript.

## Exchange warning read directly

[NSE, Trading in International Exchange Traded Funds, 25 September 2026](https://nsearchives.nseindia.com//web/pressrelease/2026-09/PR_cc_25092026_20260925122830.pdf).

Opened and read the complete one-page primary PDF, found through a circular index's source link. NSE described certain international ETFs trading above NAV while underlying NAVs remained broadly stable, tied restricted unit creation to exhausted overseas headroom, and warned of traded-price falls unrelated to the underlying. This supports the mechanism, not a fresh 27 November quote. The date on this PDF is September 25; do not mislabel it as a new warning issued today or as a directly read October 7 notice.

The release also discusses a future price-band reference change. The story does not predict an April price fall or claim that a price band guarantees a maximum premium. No unverified current premium is needed for the hypothetical example.

## Current primary cap definitions

[SEBI Master Circular for Mutual Funds, 20 March 2026](https://www.sebi.gov.in/sebi_data/attachdocs/mar-2026/1774024028162.pdf), paragraph 13.11.2, PDF page 211. Read the limit table and context: overseas securities have a $7 billion industry ceiling and $1 billion per-mutual-fund ceiling; investment in overseas ETFs has a $1 billion industry ceiling and $300 million per-mutual-fund ceiling.

The $1 billion overseas-ETF ceiling is not a blanket limit on all India-listed ETFs tracking foreign stocks. The cap must be matched to what the scheme invests in. Do not infer that a scheme has no creation headroom today solely from these maximum limits. The spoken version simply says investment limits can restrict creation.

[Motilal Oswal Nasdaq 100 ETF SID, 29 May 2026](https://www.motilaloswalmf.com/content/dam/motilal-mf/downloads/mf/sid/2026/may/SID_Motilal%20Oswal%20Nasdaq%20100%20ETF.pdf). Read the investment objective on PDF page 1 and risk discussion on pages 35 and 38. The objective is investment in Nasdaq-100 constituent securities. The risk section identifies supply/demand-driven premiums/discounts and regulatory effects on market makers' ability to arbitrage. This corroborates the general distinction and avoids assigning the wrong cap simply from the ETF label. No current trading price or NAV is taken from the SID.

## Hypothetical calculation — checked with Python Decimal

Assume one unit has ₹100 of net assets, is purchased for ₹125, retains ₹100 rupee NAV, and later trades at ₹100 when its premium becomes zero. These assumptions belong in the actual spoken version, not only a caption.

`Initial premium = (125 / 100 - 1) × 100 = 25%`

`Price return = (100 / 125 - 1) × 100 = -20%`

This is an illustrative price return before investor charges/taxes. It is not a claim about MON100, Q50, a named holder, an observed loss, current valuation or a future target. ₹25 lost out of ₹125 paid is 20%, not 25%. The underlying rupee NAV, including the currency effect, is held constant; a flat dollar index alone would not be sufficient. Other risks still exist and the final two-part payoff is not an exhaustive list of ETF risks.

## Research lead and scope

The desk cites The Ken's 26 November headline “A $1 billion limit is making Indian investors overpay for US stocks”. Credit **via The Ken** for discovery. No paywalled body was read or reproduced. The independent source basis above supports the chosen example without treating that headline as universally applicable to every India-listed overseas ETF.

No live market price/NAV pair was independently checked for this proposal, so the desk's 32%, 86% and 235% figures are excluded. A later named-fund version needs aligned primary price/NAV observations, valuation date/time and currency treatment. No buy/sell instruction, alternate-product recommendation, beneficiary identity or market-rigging allegation is added.

## Intake and handoff

Checked local work before fetch; incoming changes did not overlap. Pulled main fast-forward only to c336bd2. LATEST matches the dated 27 November research byte-for-byte. Consulted today's three options, tracker, older October ETF research for context, collaboration instructions, repo rules, story/prosody guidance, strategy delta and approved jio01's actual words/approval record. Strategy changes are observational metrics, not permission to bypass human approval. No new hook/story approval was found.

Research remains read-only. Stage/push only this note and its paired story; preserve all earlier proposals, the modified collaboration file and pre-existing untracked work. No paid call, workflow invocation, audio, registry freeze, production, public posting or unsolicited message. Recheck any real quote or implementation claim before a later production handoff.
