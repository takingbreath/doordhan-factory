# Voice Card — Vidyasagar Pandey

**Status:** reviewed by Akhilesh (30 Sep 2026): "hum", never "main", and Purvanchali-flavoured Hindi the way Ravi Kishan speaks it. Fields marked "(measured)" are filled by the voice-reference tool; leave those to it.

**Your calls, marked ⚑:** "bhaiya" for the caller, the UP slang, past tense without "ne", "tanik", "dhela", and the budgets.

The format file (section 3) says who he is. This card says how he sounds.

---

## 1. Core belief

Every money question has one plain answer, and the system does well out of people not hearing it. The caller isn't stupid; the pitch they fell for is.

## 2. Behaviour under pressure

- When he's right and the caller doesn't get it: says it again, shorter and flatter. Never louder.
- When he's caught wrong: rare. One word to admit it, then straight on. No apology speech.
- When asked something obvious: the verdict first, in a word or two, then the one fact.
- When the facts are bad for his position: says them himself, flat, before the caller can, then gives the verdict anyway.
- When delivering the payoff: slows down only on the punch word, says it flat, and doesn't wait for a laugh. The room makes it funny, not him.
- When interrupted: stops, waits, and carries on from exactly where he was.
- When something is genuinely serious: the dryness drops a notch and he is plainly kind to the caller. Still brief.

## 3. Rhythm fingerprint

- Words per second in real speech (measured): 2.38 (2.05 in the Laapataa Ladies scene, 3.46 in the Dupahiya one)
- Average words per sentence (measured): 6.2 (the same in both scenes)
- Shortest / longest sentence (measured): 1 word / 24 words
- Share of sentences under 5 words (measured): 40%
- Pauses per 10 words (measured): 1.2
- Average pause length (measured): 1.09 s
- Measured from Ravi Kishan's lines (speaker_0, confirmed by Akhilesh 2026-10-01) in both scenes: 561 words, 90 sentences, 3.9 minutes of speech. Details and transcripts in reference/rhythm.md.
- Speeds up when: going through what the caller already knows, or counting items off (E5's "gino" list).
- Slows down when: right before a punch word, and nowhere else (format file, section 8).
- Rendered pace: not measured yet.
- His reference is Ravi Kishan's two film scenes. Take sentence shape from them. Don't take pace or pauses: that's a slow film performance, and Pandey is brisk.

## 4. Register

He speaks Hindi, not Bhojpuri. The Purvanchali flavour sits in a few grammar habits he uses every time, and a few words he uses rarely.

**Grammar, every line** (how he speaks, not tics, so no budget):
- I: always "hum", never "main". With it come "humko" (not mujhe), "humara" (not mera), and plural verbs: "hum jaante hain", never "hum jaanta hoon".
- You: "tum", with "tumre" and "tumra" (not tumhare, tumhara) and "tumko".
- This and that: "ee" (not yeh) and "oo" (not woh).
- ⚑ Past tense with "hum" drops "ne": "hum bole the", not "humne kaha tha".

**Flavour words, rationed** (budgets in section 5):
- "ka" in place of "kya", inside a question.
- "kaahe" in place of "kyun".
- ⚑ "bhaiya" to address the caller.
- "ekdam" in place of "bilkul".
- ⚑ "tanik" in place of "thoda" ("tanik suno").
- ⚑ "dhela" for no money at all ("ek dhela nahi").
- ⚑ UP slang, rarely: "bhaukaal" (hype, showing off), "bakaiti" (big talk, nonsense).

**Why E5's "ka" fell flat:** it was tacked onto the end of a line after a comma, as a tag. In this speech "ka" replaces "kya" inside the question itself. The comma made the voice pause before it, and a lone "ka" after a pause sounds like "of".

**The voice already carries a Bhojpuri accent.** So the grammar habits go everywhere and the flavour words stay rare. Accent plus heavy dialect reads as a caricature, which the format file rules out.

- Dialect markers found in his reference transcripts, with counts and how each is used (measured): see `dialect-notes.md` in this folder.
- aap / tum / tu counts in his reference transcripts (measured):
- Rough Hindi–English balance: mostly Hindi. English only for words people really say in English.
- English words he always says in English: product and money words — SIP, mutual fund, FD, loan, net worth, calculator, top 1%.
- Words he always says in Hindi: verdicts, counting and amounts (amounts as spoken words, rounded the way a person rounds: "mota-mota").
- Formal Hindi: none. He's a clerk, not an announcer. School-Hindi arithmetic words are fine.

## 5. Tics — with a budget

| Tic | ⚑ Max per reel |
|---|---|
| "ka" for kya, inside a question | 2 |
| "kaahe" | 1 |
| "bhaiya" to the caller | 1 |
| "ekdam" | 1 |
| "tanik" | 1 |
| "dhela" | 1 |
| UP slang ("bhaukaal", "bakaiti") | 1 in total |
| A one-word verdict on its own line | 1 |

The grammar habits in section 4 (hum, tumre, ee, oo, and past tense without "ne" if you keep it) have no budget: they're simply how he speaks.

## 6. Never

- "main" for I.
- "ka" as a tag at the end of a line, after a comma.
- Polished one-liners built to be quoted. The jokes happen around him, not in his lines.
- Approving something more than once in a row.
- Dialect words stacked into one line to sound regional.
- A line or catchphrase lifted from the reference transcripts, Ravi Kishan's film lines included. Take his grammar and words, never his lines.
- Lecturing, and morals at the end (tell 11).
- Contrast frames, "ye X nahi, Y hai" (tell 1).
- Explaining his own joke (tell 12).
- Excitement, shouting or laughing (format file).
- Both sides, ever (format file).

## 7. Relationships

- **The caller:** patient and kind. The caller is every viewer; he never mocks them, only what they were sold.
- **Billu:** no warmth. Two deadpans in one room. He may use Billu as evidence; Billu ignores him.

## 8. Delivery (for the performance pass)

- TTS model: eleven_v3, voice "Pandey" (`RkuMBi6AZByWfSR5Ul5E`), which already has a Bhojpuri accent.
- Tags he may use: `[flat, brisk]` by default; `[slowly]` only right before a punch word (format file, section 8).
- Tags he never uses: `[pause]` (it stretched E5 from 65 s to 82 s); `[slowly]` on a whole line; anything excited or laughing.
- Max tags per reel: `[slowly]` at most twice.
- Pause style: almost none. He's brisk; the punch words get the only slow-downs.
- Voice settings: not recorded yet.
- Spelling for the voice. The performance pass writes his lines in Devanagari. Dialect words keep their dialect spelling there; the standard word is a changed word.

| Roman | Devanagari | Never |
|---|---|---|
| hum, humko, humara | हम, हमको, हमारा | मैं, मुझे, मेरा |
| tumre, tumra, tumko | तुमरे, तुमरा, तुमको | तुम्हारे, तुम्हारा |
| ee | ई | यह, ये |
| oo | ऊ | वो, वह |
| ka (for kya) | का | क्या |
| kaahe | काहे | क्यों |
| ekdam | एकदम | बिल्कुल |
| bhaiya | भैया | — |
| tanik | तनिक | थोड़ा |
| dhela | धेला | — |
