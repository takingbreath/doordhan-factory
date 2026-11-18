# Nvidia extra week — primary verification and arithmetic

Status: DRAFT — SOURCE NOTES FOR UNAPPROVED HOOK/STORY. Checked 18 November 2026 IST. Writer verification only; independent review of the eventual Roman Hinglish script remains required.

## Newly released actuals and outlook

[NVIDIA Q3 FY2027 results release, 17 November 2026](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Third-Quarter-Fiscal-2027/default.aspx).

Opened the issuer's full HTML release. The quarter ended 25 October 2026. The financial table gives actual revenue of **$115,844 million**, rounded to $115.8 billion in the headline. The outlook explicitly includes an extra week and gives **$130 billion, plus/minus 3%** for Q4 FY27. No actual Q4 results have been reported here.

The current quarter's reported 103% year-on-year and 20% quarter-on-quarter growth are separate from our comparison of the next-quarter midpoint with current actuals. No profit or stock-return calculation enters the story.

## Confirm the calendar

[NVIDIA Q2 FY2027 Form 10-Q, quarter ended 26 July 2026](https://investor.nvidia.com/files/doc_financials/2027/NVDA-2027-Q2-10Q-Final-including-exhibits.pdf), Note 1, Fiscal Year, PDF page 9.

The issuer says FY2027 has 53 weeks and Q4 will have 14 weeks. It identifies the July quarter as 13 weeks. The current Q3 runs from 27 July through 25 October: 91 days / 7 = **13 weeks**, independently checked from the disclosed quarter-end dates. Thus the outlook compares 14 weeks with 13, not two equal-length quarters. The extra week was previously disclosed, not discovered as an omission.

## Our calculation

Inputs in billions: actual = 115.844; Q3 weeks = 13; Q4 guidance midpoint = 130; Q4 weeks = 14.

`Raw implied Q/Q growth = (130 / 115.844 - 1) * 100 = 12.2198819%`

`Average-per-week implied growth = ((130 / 14) / (115.844 / 13) - 1) * 100 = 4.2041761%`

Verified with Python Decimal and date arithmetic. Spoken rounding: roughly 12% quarterly; around 4% on an average-per-week basis at the midpoint. The same calculation at the guidance low/high implies approximately 1.08% / 7.33% per week; those endpoints are not in the proposed story but show why the midpoint qualifier matters.

Dividing total revenue by weeks gives a comparable average; it does not establish a uniform pattern of shipments, strip out seasonality, measure units/prices/customer demand separately, or predict that a hypothetical 13-week Q4 would have exactly proportional sales. Do not present the 4% as Nvidia's published organic-growth forecast or a realised outcome. No regression, causal estimate or earnings/trading prediction was performed.

## Chronology and excluded claims

The desk's overnight-results story is current. However, Q3 ended on 25 October, before the November CEO departure confirmed in [NVIDIA's 12 November transition release](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-CEO-Transition/default.aspx). A first earnings publication after his exit is not a full operating quarter without him. Do not infer founder dispensability from that timing or attribute all of the quarter's results to his successor.

No need to establish the latest board-return position, allegations, after-hours price move, Indian fund weight or Anthropic pricing in this one calendar story. None is included as an independently checked spoken claim. Earlier dated capacity-backstop figures require a fresh latest-filing check if that separate draft proceeds; this proposal does not update those contracts.

Search also surfaced third-party analyses discussing the extra week. They are not used as the factual authority or copied. Do not claim that nobody has noticed the calendar issue. The company release, prior company filing and our transparent arithmetic support the proposal.

## Intake and review state

LATEST matches research/desk/2026-11-18.md byte-for-byte. Full TRACKER, current COLLABORATION.md, story/prosody checkpoints, existing weekly strategy and approved jio01 were read. Research is current again after the 17 November missing-desk notice. Today's recommendation is Nvidia (the desk's second option); the existing Anthropic supplier-investor/accounting proposals remain pending without new human approval. Yes Bank requires primary legal checks before a separate proposal.

Research files remain read-only. Preserve tracked local collaboration edits and all pre-existing untracked manuscripts. Only these two dated Nvidia draft documents are to be committed/pushed.

Next checkpoint: human hook/story approval, then one Roman Hinglish script, independent editorial/final fact review of its actual words, and human voice review. No audio, measured duration, spending, script freeze, video, publishing or unsolicited cross-chat message is authorized here.
