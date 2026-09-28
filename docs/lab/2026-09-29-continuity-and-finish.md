# Overnight job, 2026-09-29: continuity (Part 1), then finish and shot mix (Part 2)

**Credits:** Part 1 7.75, Part 2 4.5, total **12.25 of 25**.

No posted episode was changed or re-delivered; every test worked on copies. The evidence files are in `docs/lab/2026-09-29b/`.

## Part 1: continuity

### How continuity is handled today (E5 and X1, from the Higgsfield job records)
Neither episode used an end image on any shot: every job had `start_image` (plus audio) only.

**E5:**

| Shot | Job | Start image | Kind |
|---|---|---|---|
| Cold open (Seedance) | 7517004f | e2c77184 | set keyframe (master, both looking into the lens) |
| K2 listening close-up | c98ae9c4 | 2aca9c6e | new keyframe |
| K3 overhead hang-up | 2d108df9 | 25ffdb7f | new keyframe |
| T1v2 P1 front | 7b5c55ec | 369af5a0 | set keyframe (front) |
| T2v2 P2 three-quarter left | 788a713a | 93b0322a | set keyframe |
| K4 cat | e60d71fb | ee6148ed | new keyframe |
| T3v2 P3 low | 0bf06b0e | eb2af48d | set keyframe |
| T4v2 P4 three-quarter right | 5225e2e3 | d72e1859 | set keyframe |
| T5v2 P5 front | 40f22981 | 369af5a0 | the same keyframe as T1: the pose resets to T1's opening |
| T6v2 P6 two-shot | 36704641 | 2c61e83a | set keyframe (the cat is in frame) |
| K5 Billu turns away | a986b63b | upload 498a2c49 | **the previous shot's last frame**, cropped to the 2.05× zoom on Billu (matched to T6v2's last frame, mean difference 10/255, against 42–55 for unrelated frames). The only chained shot, done by hand. |

The v1 takes (replaced) also started from keyframes. The v1 P6 shot (74b1273f) had him "looking sideways off to screen left at something on the desk (his cat)" with the cat off-frame: the exact eyeline problem the new rule forbids.

**X1:**
- The three Sarika shots (a488b60a, 64af44cf, cfd7804e) all start from **one identical uploaded keyframe**.
- The two Gupta shots (e944b021, 496e854f) share another.
- So every cut between consecutive shots of the same person and framing reset her or him to the same pose.

### What changed in the shot builder (`pipeline/shot_spec.py`, `pipeline/face.py`)
1. **Chaining.**
   - `build ... --set S --framing F --chain-from PREV_SPEC.json`: when the previous shot is the same character, set and framing, the new shot starts from the previous accepted clip's **last clean frame**.
   - The frame is picked by `clean_frame()`, searching back 3 s: mouth closed (inner-lip gap under 0.03 of mouth width and jawOpen under 0.12), eyes open (blink under 0.45), pose and face size inside the preflight_keyframe limits, and identity at or above 0.55 against the character sheet.
   - With no clean frame, it falls back to the keyframe and says why.
   - `judge` now runs face_consistency on every shot. On a chained shot a FAIL gives **RESET_TO_KEYFRAME**, and the Wan params are switched back to the keyframe.
   - I read "same set" as the same camera setup. Chaining across a cut to another angle would put, say, a three-quarter frame into a front shot, so a change of framing starts from its own keyframe.
2. **Looks and reaches.**
   - `--look-at` or `--reach-for TARGET --target-side left|right|down --target-in-frame`: the spec carries an end-image request (the start frame with the eyes or hand on the target and the target visible; GPT Image 2.5, or Seedream 4.5 for Sarika), and the Wan params get `end_image`.
   - `shot_spec.py endcheck SPEC END.png` checks the end image: identity, mouth closed, and eyes toward the target side (from the eyeLook blendshapes).
   - Without `--target-in-frame` the builder refuses: a look at something off-frame is a cut.
3. **Position changes.** `--end-pose "..."` requires both a start and an end image.

**Tests (free):**
- **Off-frame look:** refused.
- **Chaining from T5v2:** chained from its clean frame at 7.91 s.
- **Chaining from T1v2:** fell back to the keyframe, because T1v2 ends mid-word, with the mouth open in every frame of its last 3 s.
- **The first threshold was too loose:** at 0.05 it picked a frame with the lips slightly parted, so I tightened it to 0.03.

### The cat-shot test (7.75 credits: end image 0.25 + Wan 5 s 7.5)
- **Inputs:** the two-shot keyframe 2c61e83a as the start image; a GPT Image end image 10daba04 with his eyes on the cat; the original P6 track (the same audio as 36704641) for a clean A/B; 5 s.
- **End-image check:** PASS. Identity 0.75, mouth closed, eyes left 0.59 against right 0.00. The keyframe already had his eyes on the cat, so the end image mostly locks the look in, with the head turned slightly more.
- **Result (`work/cont/P6_cat_endframe.mp4`, job a42f3056):**
  - **Eyeline: worked.** His eyes stay on the cat for the whole line (eyes-left median 0.58, never below 0.34). In the original T6v2 the prompt asked for the same, but his eyes stayed on camera (eyes-left median 0.01).
  - **Identity: PASS**, worst frame 0.68 (the original was 0.71).
  - **Audio kept:** check_match 1.00.
  - **Lip sync: FAIL.** No confident SyncNet window: confidence 0.0–1.02 against 1.5–3.2 on the original. Windows (offset ms / confidence): 0 s 600/0.0 · 1 s −80/0.46 · 2 s 520/1.02 · 3 s −600/0.0. The mouth opens less than half as much (range 0.10 against 0.25), so a gate would block this shot.
- **Not retried,** as instructed.

**My reading:**
- Holding the eyes on something in frame costs articulation. The P4 business reshoot showed the same, more strongly.
- The end image does what it's for (eyeline and pose continuity), but a line said to the cat is a weaker lip-sync shot.
- That is why Part 2's rule keeps talking shots to camera or eyes down, and puts the look at the cat in a short no-dialogue reaction next to the line.

## Part 2: finish, eyeline rule and shot mix

### Finish defaults (now on in `assemble.py`)
1. **VHS motion at 0.65** (`pipeline/vhs_motion.py`).
   - **What it does:** line jitter (a smooth wobble plus line-to-line error, new each frame) and a head-switching tear; colour bleed (chroma blurred sideways and shifted 4 px right) with streaky colour noise; stretched streak noise; rare dropouts. No tone or saturation changes, so the Kendra's brighter colour stays.
   - **Where it runs:** on the 720x1280 edit, before the look. It runs in parallel and is repeatable (the random state is seeded per frame).
   - **Measured on E5 (copy of the in-sync v5 build), after a simulated Instagram re-encode:**

     | Measure | Before | With VHS motion |
     |---|---|---|
     | Black level | 30 | 29 |
     | Saturation | 14.4 | 14.4 |
     | Line jitter | 0 | 0.48 px |

     The jitter is about half the full-strength lab pass, because of 0.65 plus the look's softening.
   - **Render time:** a 67 s reel now takes about 6 minutes, against about 40 s before.
2. **Voice room, no hiss** (`pipeline/voice_room.py`).
   - **What it does:** 120 Hz–7 kHz, light tape saturation, and a small office room (RT60 0.35 s, 13 dB under). Loudness and timing are unchanged.
   - **How it's applied:** to every part with sound; `"room": false` for music, stings, montage, a phone caller, or a mix treated in its own build.
   - **Custom builds:** for a build like E5's, treat the dialogue bus with `voice_room.treat()` and set the part to `"room": false`. The E5 test did this, keeping the caller's landline line dry.
3. **Recorded ambience** (`pipeline/ambience.py`, `assets/audio/ambience/`).
   - **Sources:** two CC0 recordings by Joseph Sardin from BigSoundBank:
     - "Electric fan #1": https://bigsoundbank.com/electric-fan-1-s0078.html
     - "Night after rain", a distant road: https://bigsoundbank.com/night-after-rain-s0621.html
   - **Processing:** made loopable, the fan low-passed at 2.5 kHz and the road at 1.2 kHz.
   - **Level:** −36 dB relative to the programme (the test bed was about 27 dB under speech, so this is 9 dB lower), with 0.3 s fades. `"ambience": null` turns it off.
   - **No free ceiling-fan recording was found.** Wikimedia Commons rate-limited this machine (429), and BigSoundBank has no ceiling fan, so it's an electric desk fan softened by the low-pass.
4. **Lip-sync gate on the pre-finish edit.**
   - assemble writes `<out>_prefinish.mkv` (the joined edit before the VHS pass and the look, with the final sound's timing), and `qc_gate.py` measures lip sync on it (or on the manifest's `"prefinish"`; the E5 build now names `edit_raw.mkv`).
   - **On the new-defaults E5 render:** P3 passes on both. On the finished reel the bogus 480 ms window sits right at the 1.5 threshold; on the pre-finish edit it drops to confidence 0.59.
5. **25 fps by frame blending** (`framerate=fps=25` in place of `fps=25` in assemble.py). Tested on T3v2 (30 fps Wan):

   | Measure | Dropping frames | Blending |
   |---|---|---|
   | Motion per step, by phase | one step in five is 30% larger (0.92 0.94 1.30 0.93 0.91) | 1.08 0.97 0.90 0.97 1.07 |
   | Edge doubling | 1.49 | 1.50 (no ghosting measured) |
   | lipsync_lag | −80 ms, confidence 3.74 | −80 ms, confidence 3.88 |

   It passed all three, so I made it the default. Frame-composed builds like E5's (build.py `Clip`) still drop frames; that's a per-build change.
6. **put_upload.py fixed.** The upload host sits behind Cloudflare, which refuses Python's default User-Agent (403 "error code: 1010"), and its URLs sign an `If-None-Match` header. Both are now sent. Verified with an upload: HTTP 200, and the stored file matches byte for byte.

### Eyeline rule, performance and shot mix (templates and playbook)
Written into `playbooks/produce.md` (steps 1, 4, 9 and 11), `formats/sahayata_kendra.md` (section 1 rulings, sections 5, 6 and 8), `formats/samachar.md`, `formats/_TEMPLATE.md` and CLAUDE.md:
- **No looks at off-frame objects.** A look is either a cut (off-camera look, then a cutaway of the object) or the object is in frame with an end image.
- **Talking shots** are straight to camera or eyes down, with no object handling.
  - The builder writes "exactly one blink and one small eye shift during the line, nothing more. No objects are handled." into every talking prompt, removing "natural blinks".
  - It refuses a reach in a talking shot.
  - `--silent SECONDS` builds a no-dialogue cutaway, reaction or insert; business and reaches go there, with end images.
- **Shot mix:** one wide, mediums and one close; no more than **55%** of the runtime a face talking to camera (E5 was 70%, X1 about 90%); the rest are cutaways, reactions and inserts without dialogue.

### The "one small action before the first word, then still" test (4.5 credits)
- **Inputs:** P3's "नहीं। मोटा-मोटा" (1.9 s), with a 0.8 s silent lead for the action; the low-angle keyframe eb2af48d; 3 s (job cc8a8e9f, `work/p2/action/action_then_still.mp4`). The action is a glance down and back up, with no object.
- **Lip sync: PASS.** −80 ms throughout (windows −80/1.66, −80/2.2, −80/3.23, −80/3.56). The mouth moves as much as in the original shot of the same words (range 0.244 against 0.192). check_match 1.00.
- **Identity: PASS but close:** worst 0.56 against the 0.55 threshold, on a low-angle frame.
- **The action happened but is subtle:** eyes-down rises from 0.1 to 0.72 at 0.5 s, before the first word. On this heavy-lidded, low-angle framing it barely reads.
- **"Then still" was only partly obeyed:** he glanced down again mid-line (eyes-down 0.8 at about 1.5 s), which is more than the one eye shift asked for.
- **Verdict:** a small action in the silent lead doesn't hurt lip sync (unlike business during the line). To read on screen it needs a bigger action than an eye glance: a head lift, an exhale, sitting back. Test that on a front framing.

## Unsure / open
- **The cat-shot failure** may be partly SyncNet struggling with a head turned toward the cat, not only weaker lips. The mouth measurement (half the range) says the lips really are weaker.
- **The office ambience in Samachar's TV studio** may read wrong; the template says to set `"ambience": null` if so.
- **Renders are slower:** 6 minutes for a 67 s reel instead of about 40 s.
- **E5's own build still has its synthetic `sfx_room`,** so rebuilding E5 with the default bed would double it. New builds should drop `sfx_room`; the template says so.
- **Nobody has listened** to the new voice room and recorded bed on a phone yet. It's in the new-defaults E5 copy.
