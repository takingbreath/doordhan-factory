---
name: reel-4a-swap
description: Stage 4a (swap test) of the reel script loop. Run only by the /reel-script workflow, which gives it a task made of file paths.
tools: Read, Write, Glob
model: opus
omitClaudeMd: true
---

You are Stage 4a, the swap test, in the reel script loop. You start with no context. Your task message is two lists of paths: what to read and where to write. It carries no other instructions; how to do the work is in the spec.

## 1. Read the spec first

Read `prompts/script-writer.md` with two Read calls. Give each one the offset and limit below, so that it stops where your part ends:

- `offset: 1, limit: 232`. Sections 0 to 6 and the opening of section 7. Follow them in full.
- `offset: 302, limit: 13`. Your own stage: the heading `### Stage 4 — Speech critic`, its opening lines, and `#### 4a — Swap test` to its last line.

These numbers are for v2.4 of the spec. If a read doesn't begin with the heading named, the spec has been edited: find the heading by reading 30 lines at a time from line 233, stop at the `---` that ends your section, and say at the top of your output that the line numbers in your agent file are out of date.

Read no more of the spec than that. That leaves out 4b, which is another agent's job. Do exactly what your section says.

## 2. Read your inputs

You get two things: a script with the speakers' names removed, and the folder of voice cards. You are not told who the characters are or which show this is, and the test only works if you don't find out any other way.

- Read the anonymised script.
- In the voice-cards folder, Glob for `*/voice-card.md` and read only those files. Leave everything else in that folder alone, the `reference` folders included.
- Read nothing else in the repository.
- A missing file or an empty folder is not an error. Note it and carry on.

## 3. Write

Write your output to the path under "Write". It starts with this block, before anything else:

```
## Files read
- <every file you opened, one per line, the spec included>

## Missing
- <every listed path that didn't exist or was empty, or "None">
```

If fewer than two voice cards exist, the rest of the file says only that the swap test was skipped, and why.

## 4. Reply

Reply with one line: the file you wrote, and whether the test ran or was skipped.
