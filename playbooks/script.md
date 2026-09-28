# Playbook: script

_This is the path that has worked so far. Change it whenever you find a better way, and note what you changed in registry/episodes.md._

Input: the chosen story and hook, e.g. "2B".
0. Find the options he is picking from: the morning desk email (Gmail connector, search the subject "Doordhan desk — <date>"), or ask him to paste it. The fact box and links are in it. If he approved a script in the routine's cloud session instead (laptop off), it arrives as an email "Doordhan script approved — <date> — <slug>": take it from there and go straight to produce.
1. Re-read docs/script-bible.md, including the gold examples, docs/learnings.md (what the strategist found works with our audience) and "This week's plan" in docs/strategy.md. The script must execute every open bet marked "every reel"; start the script message with "Carries:" and one line per bet saying how.
2. Re-verify every fact in the fact box with a fresh search. Numbers must come from a source you can link.
3. Draft in English first: the 5-beat spine.
4. Write the Hinglish script for the chosen hook, following the bible's rules and the format kit's shot pattern.
5. Count words; estimate duration at 2.9 words per second plus about 3 seconds for a montage or cards. It must land between 20 and 30 seconds; cut to fit before sending.
6. Send the script message exactly as specified in the bible.
7. Wait for approval from Akhilesh or Naveen (either may approve a script). On approval, freeze it: `script_freeze.py <slug> --lines work/<slug>/lines_approved.json --approved-by <who>` writes registry/scripts/<slug>.json; commit it. A later change needs `--reapprove "<who>: <why>"`, and the final is diffed against this file (produce step 10). Apply his edits as written; if you think one of his lines hurts the reel, say why in one line and let him decide.
