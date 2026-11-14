# sk06: voice direction v2 (Pandey in a Mumbai bus)

Akhilesh (2026-11-14) on cut v1: remove the breath sounds ("He's in a bus, not a studio"), apply the pause and
emphasis lessons from the Rashmi reels (docs/voices/directing-tts.md, work/anthropic01/voice/direction_v2.md), and
keep the slower pace (he preferred the slowest-take cut, 97.9 s). The words do not change: only punctuation and tags.

## Spec
- Affect: a mid-30s office commuter, dry and knowing, speaking to the person standing next to him. Low and close
  (the camera is very near), not projecting over the bus.
- Tone: calm, matter-of-fact, a little confidential. Never a newsreader, never a salesman.
- Pacing: unhurried, about 2.4 words a second; quicker inside a list, slower before each name.
- Arc: direct question (hook) -> dry aside (startups unlisted) -> calm walk through four names -> the brake, a reset
  ("Ab semiconductors par aaiye") -> quietly firm payoff (charts before entry).
- Pauses: put in the edit, not by ellipses (unreliable): after the hook; before each company name; the brake before
  "Ab semiconductors"; before "Ab ee chaaron"; a short beat before "Entry ke waqt".
- Emphasis: one focus word per thought group, marked with a dash before it.
- Breaths: removed after generation (debreath pass), the bus ambience fills the gaps.

## Beats
| Line | Intention | Focus | Tag |
|---|---|---|---|
| P1 | ask the viewer directly, then the two sectors | ignore; space / semiconductors | [direct, conversational] |
| P2 | name the startups, then the catch | listed nahi | [dry, matter-of-fact] |
| P3 | first name, why it matters, what to check | Centum Electronics; breakout | [calm, unhurried] |
| P4 | second name, what it makes, the chart note | MTAR Technologies; range | [calm, unhurried] |
| P5 | after the brake: reset to chips | unlisted; watchlist | [calm, matter-of-fact] |
| P6 | third name, quick | CG Power | [calm, unhurried] |
| P7 | fourth name, then the point | Kaynes Technology; radar | [calm, unhurried] |
| P8 | the payoff | chart ka setup | [quietly firm] |
