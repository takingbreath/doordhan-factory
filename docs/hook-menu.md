# Hook menu

The moves an opening can make (Claude, 2026-10-01). Every example is the opening of a Hindi or Hinglish money reel that did well, grouped by the move it makes. There are no view counts here, on purpose: pick the move that fits this story, not the example that did best.

- **A hook is one reason a reel works, never the only one.** These reels also had their topic, their timing, their creator's following and everything after the first line. No example here is a formula.
- **Take the move, never the words.** These are creators talking to camera. Pandey and the caller are not creators: the voice card and the format file decide how a move sounds in their mouths.
- **The format's contract decides which moves an opening may use.** For Sahayata Kendra: Pandey's first line is a verdict or a question headline, then one ring, then the caller's first line, which adds their own stake.
- **No agent in loop v0.3 reads this menu** (`docs/script-playbook.md`, 3 Oct 2026). In the v3.x loop the blueprint stage read it and named the move and the intent, and the writer never saw these examples. Whether v0.3's writers should get it is open with Akhilesh. The evidence behind them (`docs/hooks.md`: multiples, links and the analysis) is for Akhilesh, and no agent reads it. The § numbers below are the archived v3.5 spec's (`prompts/archive/script-writer-v3.5.md`).

## Sahayata Kendra: Pandey's first line

### Verdict shapes

**Plain verdict.** A flat ruling on something people commonly do, before any reason. The viewer stays to find out why.
Fits when the answer is a clear yes or no on a common choice.
- "10 lakh rupaye ki gadi mein invest karna is not worth it." (on screen: "10 Lakh Ki Gadi Lena It's Not Worth It")
- "18 साल के होते ही go file ITR."

**A verdict the viewer wants to argue with.** The ruling goes against what the viewer was raised to do, so they stay to push back.
Fits when the stance overturns a habit the viewer's family treats as obviously right.
- "अगर आप job करते हो तो आज से ही अपने घर वालों को पैसे देना बंद कर दो।"

**A sum on your own number.** The ruling arrives as a sum the viewer does on their own salary or amount.
Fits when the answer turns on an amount the viewer already knows. The line has to make sense without doing the sum (spec §5); doing it is why they stay.
- "अपनी monthly income लो और उसे 300 से multiply करो" (on screen: "50000 x 300 / 1.5 Cr")
- "सैलरी आ गई 0.2 से multiply करो।"

**Your money, side by side.** Two outcomes for the same small amount, so the gap does the arguing.
Fits when the story compares two places for the same money.
- "अगर आप ₹100 हर महीने invest करते हो तो SIP में बनेंगे roughly around ₹2.3 लाख और FD में…"

**A warning, only with a real date or a real loss.** What to do before a date, or the money the viewer is about to lose.
Fits only when there is an actual deadline or cost. Without one, it's fake edge (spec §3).
- "15th December के पहले income tax portal पे यह काम जरूर करना, वरना आपको penalty लगेगी।"
- "अब इन hand salary भी कम आने वाली है ₹2400 से।"

### Question headline shapes

**The viewer's own question.** Asked plainly, the way a person says it out loud. It hooks because the viewer has asked it too.
Fits when the answer isn't obvious and the viewer has wondered.
- "Mutual Fund कम्पनी बंद हो गयी तो?"
- "India में कितने पैसे में तुम … Richie Rich life जी सकते हो…?" (on screen, shorter: "How Much Money Is Enough in India?")

**A what-if with a big number.** A concrete, slightly absurd sum, so the viewer guesses before the answer comes.
Fits when the answer is a number the viewer will get wrong.
- "डैड, अगर 100 करोड़ फिक्स डिपाजिट होगा, तो इंटरेस्ट कितना आता होगा?"

**The promise, said back.** The pitch the viewer has heard (a calculator, an ad, the common belief), repeated plainly, so the viewer waits for the check.
Fits when the story checks a pitch the viewer believes.
- "१ करोड़ की FD महीने का ₹58,333 सैलरी जितना बिना काम किए परफेक्ट प्लान लगता है ना…" (on screen: "₹1 CRORE -> FD -> ?/MAHINA")
- "तो लोग खुश होते हैं ना कि मैंने प्लॉट में डाला 30 साल में 30 गुना हो गया…"

**What people with money do.** How the rich handle the same thing the viewer handles.
Fits when the answer is a habit the viewer can copy, not a product.
- "अमीर लोग EMI ऐसे भरते हैं" (on-screen text over music)
- "Celebrities apni gold jewellery naa ghar pe rakhte hain aur naa hi bank ke locker me…"

## Sahayata Kendra: the caller's first line

The contract: it adds the caller's own stake (their amount, their situation) and never repeats Pandey's line. The caller rings once and is gone, so this one line carries all of them.

**Their situation, in one specific line.** Who they are and what they did or are about to do, with their number. The question can stay implied.
- "सर मुझे 12 लाख की FD करानी थी।"
- "मैं 50 लाख का plot खरीद रही हूँ।"

**What they were told.** The claim they heard, who said it, and the doubt it left.
- "Monica government ne to bola ki 12 lakh tak ki salary pe koyi tax nahi hai to fir … ye sab kya hai?"

**The complaint everyone has.** A small, true frustration the viewer says to themselves.
- "Salary bhi mil rahi hai, Paise bhi kama raha hu, Lekin ye Paise ja kahan rahe hain" (on-screen text)
- "Paisa bachana seekha nahi tha." (on-screen text)

## Not used for Sahayata Kendra

- **Secret** ("बैंक वाले ये बात आपको कभी नहीं बताएंगे"): it announces a secret instead of telling it. The spec bans that as fake edge (§3).
- **Promise** ("चलिए समझते हैं…", "सिर्फ इस एक video में"): a creator talking to camera (§4 tells). Pandey answers a call; he doesn't sell the next minute.
- **Personal proof** (a creator's own portfolio): Pandey has none to show. A caller's own result goes under "Their situation".
- **Stats about other people** ("India में 500 Cr+ कमाने वाले सिर्फ 966 लोग हैं।"): research voice (§4, tell 13), unless the number changes what this viewer does.
- **Community stereotypes** (what "Marwaris" or "Gujaratis" do): the joke lands on a group of people, not on a pitch.
