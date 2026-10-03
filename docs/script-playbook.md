# Script playbook, v0.3 (3 Oct 2026)

How a Sahayata Kendra script gets written. One page. The agents in the loop read this file and nothing longer. The 8,700-word spec it replaces is in `prompts/archive/` for reference; it produced worse scripts.

## What a good script is

Someone curious asks a money question; Pandey explains it to a beginner, out loud, in one go, so the person on the phone gets it. That's the whole job. A good one:

- is one continuous piece of talk, where each sentence picks up from the one before (dekho, ab, toh, matlab, kaahe, isi liye are how people join thoughts; use them);
- can be said aloud without stumbling, and followed on one listen by someone who knows nothing;
- has the why in it, not just the what;
- leaves the viewer with one line they could repeat to a friend, and feeling a little smarter;
- sounds like Pandey: dry, kind to the caller, unimpressed by the system, with his words (hum, tumra, ee, oo, ka, kaahe) and no excitement;
- gets its laugh from the situation, in passing, never from a line built to be quoted;
- never ends on a moral, a lesson or an ask.

The example: `docs/examples/sahayata-kendra-dollar-rate.md`. Read it for the shape and the voice. Don't reuse its lines.

## The loop (v0.3, agreed 3 Oct 2026)

1. **Research. One agent.** Facts with sources and dates; every number computed in code; how people phrase the question (search suggestions, titles, comments); what popular creators say; and five to eight reels on the topic, chosen by views, with transcripts (vidIQ search, transcript and watch tools only). It flags gaps; it doesn't pick a take.
2. **Writers. Three agents, independent, the same package each.** The package: the research handoff, the reels, this file's "What a good script is", the brief below, and the example. Nothing else. Each writer picks the question a normal person would ask, says in a few lines why, and writes two complete scripts, each as one continuous piece of talk. The question and the answer come from one mind; that is the point. If a writer needs a number the research doesn't have, it looks that one thing up, cites it in its note, and the judge checks it.
3. **Judge. One agent.** Reads all six scripts whole and compares them against "What a good script is" and the example. Picks three, from different writers where it can. For each pick: traces every claim and number to the research (or the writer's cited lookup), attaches the lint's voice report, and writes four or five lines on why it works and what Akhilesh should listen for. It changes no words.
4. **The judge's note.** For a pick, the judge may send one note back to the writer who wrote it: a claim it can't trace, or one observation about the whole script. The writer answers once: keep, revise, or offer its other draft. The writer has the last word on the words.
5. **Readers. Three per pick, cold.** "You heard this once; tell a friend what it said, in three sentences." Their retells go to Akhilesh under each script, as information. They send nothing back to anyone; their lack of context is the point.
6. **Voice.** The three picks, rendered the way V6b was: Devanagari from the voice card's spelling table, the monologue as one take, the slower spaced delivery, a Scribe transcript of each cut against its script.
7. **Hand-off.** Three scripts in full, three cuts, each writer's question and reasons, the claims trace, the retells, the lint reports, compliance notes. Akhilesh picks one, or none. A rejection is a new brief with a sentence from him.

Paths back, and no others: the judge's one note to a pick's own writer; a writer's one lookup for a missing number. No rewrite loop. No line-by-line critic. The lint reports; it stops nothing.

## The brief (what a writer gets)

Fill the three bracketed parts. Keep the rest word for word.

> Write a 60-second Instagram reel script in Hinglish.
>
> The setup: a 1980s government helpline, "Doordhan Sahayata Kendra". Vidyasagar Pandey, the clerk, answers one money question per call. A caller rings and asks, and Pandey explains. Billu, the office cat, sits on the desk and does one silent thing at the end.
>
> The question: [the viewer's question].
>
> What Pandey explains, the way a beginner needs it: [one answer paragraph from step 2, four to six sentences, with the why; any return or inflation figure marked to be said as an assumption].
>
> How Pandey talks: deadpan, dry, unhurried, kind to the caller and unimpressed by the system. Purvanchali-flavoured Hindi: "hum", never "main"; "tumra", "tumko"; "ee" and "oo" for yeh and woh; now and then "ka" for kya and "kaahe" for kyun. English words where people say English: [the topic's English words]. Numbers in Hindi words up to twenty and the round tens, in English otherwise ("twenty seven hazaar"). He never ends with a moral.
>
> Shape: Pandey's first line is the hook, said to camera: the question itself, or his flat verdict, 8 words or fewer. Then one ring. Then the caller asks the question the way a curious person would. Then Pandey explains in one go, as one continuous piece of talk, the way he'd say it on the phone. Not a list of points. End on Billu's one silent beat, in square brackets.
>
> Roman Hinglish, the way people type in chats. Label the lines PANDEY, CALLER and BILLU.

Plus the example file, with "read this for the shape and the voice; don't reuse its lines".

## What this replaced, and why

looptest3 to looptest6 and cheat1 V1–V3 came from a 13-agent loop with 18,400 words of rules. Their scripts were lists of true sentences with the joins removed, because the loop wrote, judged and rewrote line by line, and its rules banned the joining words. `work/cheat1/v6.md` came from the brief above in one pass. The research agent, the fact check, the voice pipeline and its transcript checks, the voice card's spelling table and the hook library were right every run and stay.
