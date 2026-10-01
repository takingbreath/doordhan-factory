# Hook library: Hindi and Hinglish money reels that beat their channel's average

**vidIQ credits spent: 204** of the 400 budget (balance 1,630 → 1,426, 1 October 2026): outlier searches 50 (10 calls, 3 of them empty), YouTube transcripts 80 (16), short-form watches 74 (77 submitted, 3 refunded because the reel was deleted; vidIQ lists a watch at 10 credits but charged 1). **Rows with a known opening: 90 of 92** in `work/hooks/outliers.csv`; the other 2 have only their on-screen text (the reels were deleted before they could be watched).

Built from vidIQ data only. Every opening below is copied from vidIQ's transcript or short-form tools and cut at 15 words; nothing is rewritten.

## How the set was built

- **Instagram:** two `vidiq_instagram_tiktok_outlier_search` calls (posted after 2025-10-01, captions in Hindi or English, outlier score 3 or more, Indian salaried audience), one on SIPs, saving, salary, EMIs and stock basics and one on tax, insurance, credit cards and FDs. 91 reels came back. TikTok results were ignored.
- **YouTube Shorts:** `vidiq_outliers` (Shorts, last 12 months) by keyword (SIP and mutual funds, credit card, income tax and salary, saving) and by six Indian finance channels found in those results (three first attempts with an India filter came back empty: vidIQ leaves most Indian channels' country blank). vidIQ does not search Hindi titles for Shorts, so Latin-script titles were searched and the language was checked on each transcript. 16 candidates at 3× or more were transcribed; 14 were Hindi or Hinglish.
- **Opening:** for every talking reel, `vidiq_watch_shortform_content` was asked for the spoken language, the first complete spoken sentence and the on-screen text of the first 3 seconds; YouTube Shorts also have `vidiq_video_transcript`. Music-only reels take their on-screen text from the search's own first-3-seconds analysis. No video was downloaded, so `pipeline/voice_reference.py` was not needed.
- **Kept:** 92 (78 Instagram, 14 YouTube Shorts). **Left out:** 15, listed with the reason in `work/hooks/excluded.csv`: 3 off topic, 6 spoken in English or Telugu, 5 with no speech and English-only on-screen text, and 1 deleted reel whose language could not be confirmed.
- **Multiple:** Instagram is vidIQ's “x their median” (views over the creator's median); YouTube is vidIQ's `breakoutScore` (views over the channel's typical). Instagram views are vidIQ's rounded figures. Medians are used throughout because the multiples run from 3× to 3,849×.
- **Caveat:** this is the set vidIQ's search returned, not a random sample, and most types have fewer than 10 reels. Read the medians as directions, not laws. Median multiple of all 90 known openings: 41.7×.

## Hook types

Each reel has one type, taken from its first spoken sentence, or from its on-screen text when nothing is spoken. Only types that at least three outliers use are listed; every known opening fits one of them.

| Type | Definition | Outliers | Median multiple |
|---|---|---|---|
| What the rich do | Names a rich person, a celebrity, a wealthy community or the rich-vs-middle-class split, and the money move they make. | 17 | 45.2× |
| Story or scene | Opens inside one specific case: a client, a couple, a named person, a film, or an acted scene. | 13 | 42.1× |
| Verdict | A flat judgement or instruction about a money behaviour: not worth it, never do it, do it now. | 10 | 48.0× |
| Promise | Announces what the viewer will learn: these rules, these deductions, this one thing. | 9 | 62.3× |
| Question | Opens on a money question: the viewer’s own, one put to the viewer, or one overheard in a clip. | 9 | 30.1× |
| Warning | A cost about to hit the viewer: a dated rule change, a deadline, a penalty, a leak. | 8 | 42.1× |
| Surprising number | Leads with one specific figure as the news. | 5 | 112.0× |
| Relatable line | A one-line saying or lament the viewer recognises as their own. | 5 | 37.9× |
| Personal proof | The creator’s own money result, journey or regret, in the first person. | 5 | 34.2× |
| Formula on your number | Tells the viewer to do a sum with their own number. | 3 | 63.8× |
| Belief to bust | States what people believe or do, set up to be knocked down. | 3 | 48.0× |
| Secret | Promises something others hide or most people don’t know. | 3 | 28.9× |

### What the rich do

**17 outliers, median 45.2×.** Names a rich person, a celebrity, a wealthy community or the rich-vs-middle-class split, and the money move they make.

Structure: “Rich people / a celebrity / Marwaris do X” as the first line or the on-screen headline; six of the seventeen are text over music, five of them the same line (“अमीर लोग EMI ऐसे भरते हैं”) on different accounts.

- “अच्छा, अगर आप किसी मारवाड़ी बच्चे से पूछोगे कि ₹1 लाख का profit हुआ तो …” — 431.5×, [Instagram](https://www.instagram.com/reel/DbQTCgMtwzC/)
- “राकेश झुनझुनवाला ने अपनी पूरी ज़िन्दगी में सिर्फ़ एक ही बात बोली और सुनो उन्हीं …” — 336.5×, [Instagram](https://www.instagram.com/reel/DcZI21gySrD/)
- “मैं 50 लाख का plot खरीद रही हूँ।” — 305.4×, [Instagram](https://www.instagram.com/reel/DdjTiEdhDRh/)
- “Ambani family भी iPhone September में नहीं October में लेती है” — 105.1×, [Instagram](https://www.instagram.com/reel/DazxZFptxIT/)
- “अमीर लोग EMI ऐसे भरते हैं (Rich people pay EMIs like this)” (on-screen text, no speech) — 80.8×, [Instagram](https://www.instagram.com/reel/Dbk1REBty3B/)

### Story or scene

**13 outliers, median 42.1×.** Opens inside one specific case: a client, a couple, a named person, a film, or an acted scene.

Structure: A single person or scene in the first line (“a client came to me…”, “his salary was ₹70,000…”), the money lesson held back until later.

- “भाई ऐसे ऐसे client आते हैं ना” — 710.8×, [YouTube](https://www.youtube.com/shorts/8xVAZUPrPZE)
- “भाई 1 लाख की सैलरी वाले क्लाइंट ने 2 करोड़ की Defender खरीद ली।” — 190.5×, [YouTube](https://www.youtube.com/shorts/yOvQgMPtbys)
- “आशिकी फिल्म आई थी आपके और मेरे टाइम पे।” — 183.7×, [Instagram](https://www.instagram.com/reel/DcQ0ba8RQ5x/)
- “ये लो मैडम आपके chips का packet, पर 1 minute इसपे तो 2-2 MRP लिखे …” — 128.4×, [YouTube](https://www.youtube.com/shorts/g2RumJsX3eY)
- “Usaki salary 70,000 thi..” (on-screen text, no speech) — 71.3×, [Instagram](https://www.instagram.com/reel/Db0kk4Wimv4/)

### Verdict

**10 outliers, median 48.0×.** A flat judgement or instruction about a money behaviour: not worth it, never do it, do it now.

Structure: One declarative line, often an imperative (“मत करना”, “बंद कर दो”, “go file ITR”), stated before any reason.

- “10 lakh rupaye ki gadi mein invest karna is not worth it.” — 1,263.6×, [Instagram](https://www.instagram.com/reel/Db6bqFBTG9a/)
- “Income Tax Department आपको तब नहीं पकड़ता जब आपकी transactions गलत हो जाती हैं वो …” — 548.9×, [Instagram](https://www.instagram.com/reel/Dafrq_aS07x/)
- “अगर आप job करते हो तो आज से ही अपने घर वालों को पैसे देना …” — 240.4×, [YouTube](https://www.youtube.com/shorts/iTw7X_DbCDk)
- “तुम दुनिया की कोई भी गलती कर देना लेकिन EMI trap में फंसने की गलती …” — 137.5×, [Instagram](https://www.instagram.com/reel/DanrEoJpTuh/)
- “18 साल के होते ही go file ITR.” — 54.8×, [Instagram](https://www.instagram.com/reel/Da-aV95xuD2/)

### Promise

**9 outliers, median 62.3×.** Announces what the viewer will learn: these rules, these deductions, this one thing.

Structure: “If you are doing X, these N things will …” or “today you’ll understand all of this in one video”, usually with a list or chart on screen.

- “अगर आप new tax regime में filing कर रहे हैं तो इन deductions का use …” — 251.4×, [Instagram](https://www.instagram.com/reel/Da4Q-uFiMlZ/)
- “अगर आप health insurance policy लेने का सोच रहे हो तो अपनी policy में ये …” — 156.2×, [Instagram](https://www.instagram.com/reel/DbvP7aEvcCo/)
- “चलिए समझते हैं, अगर आप अपनी financial life बदलना चाहते हो तो ये सात rules …” — 147.4×, [Instagram](https://www.instagram.com/reel/DaStxnxKreh/)
- “पाँच ऐसी Indian schemes जो आपको FD से ज़्यादा रिटर्न देती है और हर महीने …” — 85.1×, [Instagram](https://www.instagram.com/reel/DbGcyWZpnps/)
- “गजेंद्र कोठारी इनसे SWP समझते हैं।” — 62.3×, [Instagram](https://www.instagram.com/reel/DcSXuX5MnFx/)

### Question

**9 outliers, median 30.1×.** Opens on a money question: the viewer’s own, one put to the viewer, or one overheard in a clip.

Structure: A single question as the first line (“…ये होता क्या है?”, “…बंद हो गई तो?”), answered in the body.

- “डैड, अगर 100 करोड़ फिक्स डिपाजिट होगा, तो इंटरेस्ट कितना आता होगा?” — 411.1×, [Instagram](https://www.instagram.com/reel/DcsVxBEzwN4/)
- “India में कितने पैसे में तुम एकदम बहुत comfortably freedom के साथ Richie Rich life …” — 385.3×, [Instagram](https://www.instagram.com/reel/DcBlKdfKGp0/)
- “Monica government ne to bola ki 12 lakh tak ki salary pe koyi tax nahi …” — 47.3×, [YouTube](https://www.youtube.com/shorts/_E1xmeFvkY0)
- “Certified financial planner ये होता क्या है?” — 32.3×, [Instagram](https://www.instagram.com/reel/Dac_UF2BLdV/)
- “Wait, tax तो सब भरते हैं लेकिन tax की language समझते कितने हैं?” — 30.1×, [Instagram](https://www.instagram.com/reel/DbklXkMNyUO/)

### Warning

**8 outliers, median 42.1×.** A cost about to hit the viewer: a dated rule change, a deadline, a penalty, a leak.

Structure: A date or a trigger plus the loss (“15 December se pehle… warna penalty”, “in-hand salary drops by ₹2,400”).

- “15th December के पहले income tax portal पे यह काम जरूर करना, वरना आपको penalty …” — 720.0×, [YouTube](https://www.youtube.com/shorts/nKCFFidUBZo)
- “अब इन hand salary भी कम आने वाली है ₹2400 से।” — 220.8×, [Instagram](https://www.instagram.com/reel/DdYNQiIy1zJ/)
- “अगर आपके पैसे FD में इन्वेस्टेड हैं तो इस reel को मिस मत करना क्योंकि …” — 81.5×, [Instagram](https://www.instagram.com/reel/DcJz3cYSf9f/)
- “Government है ना फिर से ला रही है टैक्स लगाने के लिए” — 56.0×, [Instagram](https://www.instagram.com/reel/DdW3KLnMGm4/)
- “1 October से FD करने वालों के लिए banking system के सारे rules बदलने वाले …” — 28.3×, [Instagram](https://www.instagram.com/reel/DcFsNXvPaZf/)

### Surprising number

**5 outliers, median 112.0×.** Leads with one specific figure as the news.

Structure: A number or a chart in the first line (“500 Cr+ earners: only 966 people”, “₹100 a month: SIP ₹2.3 lakh, FD ₹46,000”).

- “So guys ये photo देख लो, India में जितने भी non-life insurance के claim है, …” — 473.2×, [Instagram](https://www.instagram.com/reel/DbOCts9tRGm/)
- “India में 500 Cr+ कमाने वाले सिर्फ 966 लोग हैं।” — 343.4×, [Instagram](https://www.instagram.com/reel/Dcs-8Apo_VL/)
- “अगर आप ₹100 हर महीने invest करते हो तो SIP में बनेंगे roughly around ₹2.3 …” — 112.0×, [Instagram](https://www.instagram.com/reel/Dc5WiZpxsU0/)
- “10,000 की SIP सिर्फ 6 साल के लिए, और आपके बच्चे का कॉर्पस 1 करोड़ …” — 31.1×, [Instagram](https://www.instagram.com/reel/DbsH46jzVld/)
- “सिर्फ ₹2000 की investment से आप अपने बच्चों को ₹1 करोड़ उपहार कर पाओगे जब …” — 4.1×, [Instagram](https://www.instagram.com/reel/DbPmhn4gafJ/)

### Relatable line

**5 outliers, median 37.9×.** A one-line saying or lament the viewer recognises as their own.

Structure: Text over music in four of the five: a confession or proverb about saving (“Paisa bachana seekha nahi tha”).

- “मुझे सिखाया गया है जहा किसी ओर के पैसे खर्च हो रहे हो” (on-screen text, no speech) — 1,244.0×, [Instagram](https://www.instagram.com/reel/DdwcYBJRCRd/)
- “Paisa bachana seekha nahi tha.” (on-screen text, no speech) — 82.3×, [Instagram](https://www.instagram.com/reel/DbxcrmNy-As/)
- “Salary bhi mil rahi hai, Paise bhi kama raha hu, Lekin ye Paise ja kaha …” (on-screen text, no speech) — 37.9×, [Instagram](https://www.instagram.com/reel/DbPaPC2J67Z/)
- “Paisa kehta hai, bhale hi main tere saath upar nahi jaunga, par jab tak tu …” (on-screen text, no speech) — 15.6×, [Instagram](https://www.instagram.com/reel/DbA8bWrB_46/)
- “Pehle lagta tha Paisa kamana mushkil Hai Ab lagta Hai Paisa Bachana usse bhi Jyada …” (on-screen text; the audio starts mid-sentence) — 9.2×, [Instagram](https://www.instagram.com/reel/DbdhoyMtjln/)

### Personal proof

**5 outliers, median 34.2×.** The creator’s own money result, journey or regret, in the first person.

Structure: “I have done X for N years / I cut my EMI from ₹48,000 to ₹31,000 / I wish someone had told me at 22”, often with a screenshot of the portfolio or the statement.

- “मैं पिछले आठ साल से SIP कर रहा हूँ लेकिन इस एक SIP में मुझे …” — 77.9×, [Instagram](https://www.instagram.com/reel/DaqCWKPJ3N8/)
- “मैंने अपनी होम लोन की EMI ₹48,000 से सीधा ₹31,000 कर दी है बैंक को …” — 49.9×, [Instagram](https://www.instagram.com/reel/DcqrTORSE_x/)
- “टोटल ₹2,64,000 इन्वेस्ट कर पाया” — 34.2×, [Instagram](https://www.instagram.com/reel/DbrXHWihaYK/)
- “काश ये छह चीज़ों के बारे में मुझे 22 साल की उम्र में किसी ने …” — 23.0×, [Instagram](https://www.instagram.com/reel/DaXzONyiGOx/)
- “मेरे पहले 1 करोड़ कमाने की जर्नी” — 3.8×, [Instagram](https://www.instagram.com/reel/Dbr6xDvKqzb/)

### Formula on your number

**3 outliers, median 63.8×.** Tells the viewer to do a sum with their own number.

Structure: “Take your monthly income and multiply it by 300” spoken, with the sum written as a numbered list (“1. 50000 x 300”) that fills in as it goes.

- “अपनी monthly income लो और उसे 300 से multiply करो” — 3,849.4×, [Instagram](https://www.instagram.com/reel/DbvaLNnv4z8/)
- “सैलरी आ गई 0.2 से multiply करो।” — 63.8×, [Instagram](https://www.instagram.com/reel/Dcc8kMQTc7j/)
- “अपनी मंथली सैलरी को 0.25 से मल्टीप्लाई करो और इतना पैसा तुम हर महीने इन्वेस्ट …” — 42.1×, [Instagram](https://www.instagram.com/reel/DcAs9Njzte2/)

### Belief to bust

**3 outliers, median 48.0×.** States what people believe or do, set up to be knocked down.

Structure: “People are happy that…”, “sounds like the perfect plan, right? Let’s do the maths”, then the correction.

- “तो लोग खुश होते हैं ना कि मैंने प्लॉट में डाला 30 साल में 30 …” — 200.7×, [YouTube](https://www.youtube.com/shorts/KBlM2Z5Mf1A)
- “१ करोड़ की FD महीने का ₹58,333 सैलरी जितना बिना काम किए परफेक्ट प्लान लगता …” — 48.0×, [Instagram](https://www.instagram.com/reel/DcvdROzzM39/)
- “ज़िंदगी ना मिलेगी दोबारा देखके लोग बहुत ज़्यादा पागल हो चुके हैं।” — 40.3×, [Instagram](https://www.instagram.com/reel/DcZOdECT60u/)

### Secret

**3 outliers, median 28.9×.** Promises something others hide or most people don’t know.

Structure: “Banks will never tell you this”, “most people don’t know you can make this tax zero”; two of the three are the same text over music.

- “बहुत से लोगों को यह नहीं पता कि वो अपने stocks, mutual funds, gold या …” — 33.0×, [Instagram](https://www.instagram.com/reel/Dbu9WDYRf7k/)
- “बैंक वाले ये बात आपको कभी नहीं बताएंगे! 😲” (on-screen text, no speech) — 28.9×, [Instagram](https://www.instagram.com/reel/DbLBCENRu5i/)
- “बैंक वाले ये बात आपको कभी नहीं बताएंगे (Banks will never tell you this)” (on-screen text, no speech), same text on another account — 4.3×, [Instagram](https://www.instagram.com/reel/DcFUxhOCOdr/)

## What the strongest openings share

“Strongest” is the top quarter by multiple: 22 of the 90 known openings (137.5× and up); for spoken openings only, the top 17 of 71 (190.5× and up).

1. **They are spoken.** Openings with speech have a median of 47.3× (71 reels); text over music has 28.9× (19). Only 1 of the top 22 is a music-only reel.
2. **Their first spoken line runs past 8 words.** Spoken openings of 8 words or fewer have a median of 33.2× (14 reels); longer ones 48.8× (57). Only 2 of the top 17 spoken openings are 8 words or fewer. Past that, length makes little difference: the top 17 have a median of 16 words, the rest 18.

   Re-cut by length (Claude, 2026-10-01): 8 words or fewer 33.2× (14 reels); 9–12 words 183.7× (11); 13–16 words 31.7× (10); 17 or more 49.3× (36). The medians jump around instead of rising with length. Read this point as “length doesn't decide”, not “longer is better”.
3. **They talk to the viewer.** Spoken openings that say आप / तुम / अपनी / you have a median of 64.2× (33 reels); the others 43.7× (38). The share at the very top is the same as below it (8 of 17 against 25 of 54), so this lifts the typical reel more than it makes the outliers.
4. **A specific number helps a little.** Spoken openings with a figure have a median of 48.4× (38); without, 40.3× (33). 10 of the top 17 carry one, against 28 of the other 54. The Surprising number type has the highest median of any type (112.0×, 5 reels).
5. **No type owns the top.** The top 22 span 10 of the 12 types, and the four biggest types (What the rich do, Story or scene, Verdict, Promise) all sit between 42.1× and 62.3×. Points 1 to 4 separate strong from weak openings more than the type does.

## Sahayata Kendra's two openings

`formats/sahayata_kendra.md` section 0: Pandey's first line, on screen from the first frame, is either the reel's question (**question headline**) or his flat verdict (**verdict**), in 8 words at most.

- **Question headline** matches the **Question** type (9 outliers, median 30.1×), plus reels of other types whose on-screen headline is the reel's question. The two strongest are both about how much money a big sum makes or how much is enough, and in both the question is spoken in a clip, not by the creator (vidIQ marks both as clips; one is a celebrity's voice).
- **Verdict** matches the **Verdict** type (10 outliers, median 48.0×).
- **Against the 8-word limit:** 2 of the top 17 spoken openings are 8 words or fewer (point 2 above). In the tables below, four of the ten put a headline of 8 words or fewer on screen over a longer spoken first line (“How Much Money Is Enough in India?” over a 30-word question; “10 Lakh Ki Gadi Lena It's Not Worth It” over 12 words), and one, “18 साल के होते ही go file ITR.”, is 8 words spoken. Word counts are given for each.

**Question headline: the 5 best**

| Multiple | First spoken sentence | Words | On-screen text, first 3 s | Link |
|---|---|---|---|---|
| 411.1× | “डैड, अगर 100 करोड़ फिक्स डिपाजिट होगा, तो इंटरेस्ट कितना आता होगा?” | 12 | Dad, if he has a 100-crore fixed deposit, what's the interest he makes? YOUR FD … | [Instagram](https://www.instagram.com/reel/DcsVxBEzwN4/) |
| 385.3× | “India में कितने पैसे में तुम एकदम बहुत comfortably freedom के साथ Richie Rich life …” | 30 | How Much Money Is Enough in India? INDIA MEIN KITNE PAISE MEIN TUM TUM EKDUM … | [Instagram](https://www.instagram.com/reel/DcBlKdfKGp0/) |
| 48.0× | “१ करोड़ की FD महीने का ₹58,333 सैलरी जितना बिना काम किए परफेक्ट प्लान लगता …” | 23 | ₹1 CRORE -> FD -> ?/MAHINA ₹58,333/MAHINA 1 CRONE -> FD -> ?/MAHINA | [Instagram](https://www.instagram.com/reel/DcvdROzzM39/) |
| 47.3× | “Monica government ne to bola ki 12 lakh tak ki salary pe koyi tax nahi …” | 36 | Monica government ne to bola ki ₹12 lakh tak ki salary pe koyi tax nahi … | [YouTube](https://www.youtube.com/shorts/_E1xmeFvkY0) |
| 35.3× | “घर में बेटी हुई है, तो सुकन्या समृद्धि योजना में इन्वेस्टमेंट अभी से शुरू कर …” | 16 | Sukanya Samriddhi Yojana Vs Mutual Fund Which One is Better ? | [Instagram](https://www.instagram.com/reel/DcbhJSOP_oP/) |

**Verdict: the 5 best**

| Multiple | First spoken sentence | Words | On-screen text, first 3 s | Link |
|---|---|---|---|---|
| 1,263.6× | “10 lakh rupaye ki gadi mein invest karna is not worth it.” | 12 | "10 Lakh Ki Gadi Lena It's Not Worth It 👎" | [Instagram](https://www.instagram.com/reel/Db6bqFBTG9a/) |
| 548.9× | “Income Tax Department आपको तब नहीं पकड़ता जब आपकी transactions गलत हो जाती हैं वो …” | 27 | These Transactions Can Trigger Income Tax Reporting | [Instagram](https://www.instagram.com/reel/Dafrq_aS07x/) |
| 240.4× | “अगर आप job करते हो तो आज से ही अपने घर वालों को पैसे देना …” | 18 | Agar aap JOB aaj se hi apne gharwaalo | [YouTube](https://www.youtube.com/shorts/iTw7X_DbCDk) |
| 137.5× | “तुम दुनिया की कोई भी गलती कर देना लेकिन EMI trap में फंसने की गलती …” | 18 | तुम दुनिया की कोई भी गलती कर देना लेकिन EMI ट्रैप में फंसने की गलती … | [Instagram](https://www.instagram.com/reel/DanrEoJpTuh/) |
| 54.8× | “18 साल के होते ही go file ITR.” | 8 | Why rich kids start filings at 18 | [Instagram](https://www.instagram.com/reel/Da-aV95xuD2/) |

## Our reference set, typed the same way

The 18 reels in `docs/voices/general/reference/` (Samay Raina and Anupam Mittal left out). They are other creators' reels kept as voice references, not Doordhan episodes, and they have no multiples, so they are typed only.

| Reel | First spoken sentence | Type |
|---|---|---|
| 100x-stock-kaise-khoje | “multi baggers कैसे खोजें?” | Question |
| 3-6-charts | “भाई जेफ्रीज की एक बड़ी जबरदस्त report आई है जिसमें कहा गया है कि छह …” | Promise |
| 3-things-not-to-do-with-credit-card-llashorts-76 | “भैया credit card से जो करना है करो।” | Verdict |
| 5-ranges-11 | “Nifty क्यों इस range में फंस गई है?” | Question |
| 52-weeks-high-low-shorts | “देखिए यूं तो ये किस्सा काफी पुराना है, लेकिन मुझे ऐसा लगता है मानो कल …” | Story or scene |
| banknifty-1-lot-25000-shorts | “बात सुनिए जरा।” | none of the types (an attention call, no claim) |
| best-business-idea-for-2023-pkbola | “हम सब चाहते हैं ना कोई ऐसा business plan जिससे हम साल का एक करोड़ …” | Relatable line |
| ekdum-800-share-stockexchange-investinginstocks | “इस शख्स को तो आप जानते ही होंगे।” | Story or scene |
| intraday-chart-candle-shorts | “तो क्या आप भी पहली 15 मिनट की candle देखकर के intraday trade लेते हैं?” | Question |
| iphone-vs-apple-shares-price-zyada-par-growth-kitni-ankur-warikoo-shorts | “जब भारत में पहली बार iPhone launch हुआ था, पता है कितने का था?” | Question |
| kaunse-prime-minister-ne-best-stock-market-return-di-hain-ankur-warikoo-shorts | “भारत के कौन से प्रधानमंत्री ने सबसे बढ़िया stock market return दी है?” | Question |
| long-short-pcr-shorts | “जनता पैसा खोएगी, संस्था पैसा कमाएगी।” | Verdict |
| parle-g-is-a-million-dollar-biscuit-llashorts-336 | “इस पाँच रुपए के biscuit ने हजारों लोगों की jobs बचाई है।” | Surprising number |
| rs-20l-ya-rs-100-kisme-hain-zyada-returns-ankur-warikoo-shorts | “इनमें से क्या choose करेंगे?” | Question |
| the-easiest-way-to-make-money-on-youtube-ankur-warikoo | “YouTube पर आप कैसे और कितने पैसे कमा सकते हैं?” | Question |
| why-hotels-have-12-pm-checkout-why-not-24-hours | “यह hotels पर ना मुझे बहुत गुस्सा आता है यार।” | Relatable line |
| why-no-pockets-for-girls-clothing-llashorts-198 | “लड़कियों के कपड़ों में या तो pockets होते ही नहीं है या होती है तो …” | Relatable line |
| ye-hai-modern-zamana-llashorts-890 | “69,400 इतना cash लेकर एक couple अपने दो छोटे बच्चों के साथ छुट्टियां मनाने गए …” | Story or scene |

Question is 7 of our 18 (39%) against 9 of the 90 outliers (10%), and has the lowest median of any outlier type with five or more reels. What the rich do, the most common outlier type (17 of 90), is 0 of our 18.

Data: `work/hooks/outliers.csv` (one row per outlier), `work/hooks/excluded.csv`, raw vidIQ output in `work/hooks/raw/`, `watch.json`, `yt_watch.json`; built by `work/hooks/build.py` and `write_outputs.py`.
