#!/usr/bin/env python3
"""Real speech as a writing reference: ElevenLabs Scribe on every clip in work/voices/audio/<name>/, one transcript per
clip in docs/voices/<name>/reference/ (file names in lowercase ASCII and hyphens), and the rhythm numbers that a voice
card's "(measured)" fields ask for.
Usage: voice_reference.py NAME [--full PART ... | --full-all] [--rhythm PART[=speaker_0,speaker_1] ...]
                               [--language hi] [--refresh]
  text-only (the default): the plain transcript, one sentence per line.
  full (--full PART: the clips whose file name contains PART; --full-all: every clip): Scribe also labels the speakers.
    Each line starts with its speaker label. A gap of 0.25 s or more between two words by one speaker is a pause,
    written with its length, like (0.4 s). A new line starts at a gap of 0.6 s or more and at a change of speaker.
  --rhythm: write reference/rhythm.md from these full-mode clips, every speaker or only the labels after "=".
    Given without --full or --full-all, it writes rhythm.md alone from the answers already kept.
Scribe's words are kept exactly as returned: nothing is corrected, standardised or translated.
Scribe's answers are kept in work/voices/scribe/<name>/ (git-ignored), so a second run, or a rhythm.md for other
speakers, costs no new call; --refresh asks again. Transcription is the only ElevenLabs call, and the audio stays in
work/, out of git."""
import argparse, json, os, re, subprocess, sys, tempfile, unicodedata, uuid
from common import FFMPEG
from elevenlabs_api import ROOT, STT_MODEL, request, error_text

AUDIO = (".mp3", ".m4a", ".wav", ".mp4", ".mov", ".aac", ".ogg", ".opus", ".flac", ".webm", ".mkv")
PAUSE, LINE_GAP = 0.25, 0.6                     # seconds between two words: a marked pause; a new line
END = re.compile(r"[।.?!…][\"'”’)\]]*$")        # a sentence ends at one of these

spk = lambda w: w.get("speaker_id") or "speaker_?"
gap = lambda a, b: round(b["start"] - a["end"], 3)
mark = lambda g: f"({g:.1f} s)"
spoken = lambda r: [w for w in r.get("words", []) if w.get("type") == "word"]
fold = lambda s: unicodedata.normalize("NFC", s).casefold()


def slug(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "clip"


def scribe(path, language, diarize):
    """One Scribe call, made the way transcribe.py makes it; diarize asks for speaker labels as well."""
    with tempfile.TemporaryDirectory() as tmp:
        mp3 = os.path.join(tmp, "a.mp3")
        subprocess.run([FFMPEG, "-y", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", "16000", "-b:a", "64k",
                        mp3], check=True)
        audio = open(mp3, "rb").read()
    boundary = uuid.uuid4().hex
    fields = {"model_id": STT_MODEL, "language_code": language, "timestamps_granularity": "word",
              "tag_audio_events": "false"}
    if diarize:
        fields["diarize"] = "true"
    body = b"".join(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
                    for k, v in fields.items())
    body += (f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="a.mp3"\r\n'
             f"Content-Type: audio/mpeg\r\n\r\n").encode() + audio + f"\r\n--{boundary}--\r\n".encode()
    st, raw = request("/v1/speech-to-text", data=body, method="POST", timeout=900,
                      headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    if st != 200:
        sys.exit(error_text(st, raw))
    return json.loads(raw)


def sentences(tokens):
    """Scribe's tokens, in order -> sentences (lists of tokens). A sentence ends at । . ? ! or …"""
    out, cur = [], []
    for t in tokens:
        cur.append(t)
        if t.get("type") == "word" and END.search(t["text"]):
            out.append(cur); cur = []
    if any(t.get("type") == "word" for t in cur):
        out.append(cur)
    return out


def text_lines(r):
    """Text-only mode: Scribe's text as it came, one sentence per line."""
    return ["".join(t["text"] for t in s).strip() for s in sentences(r.get("words", []))]


def lines_of(ws):
    """Words -> lines (lists of words): a new line at a gap of LINE_GAP or more and at a change of speaker."""
    out = []
    for w in ws:
        if out and spk(w) == spk(out[-1][-1]) and gap(out[-1][-1], w) < LINE_GAP:
            out[-1].append(w)
        else:
            out.append([w])
    return out


def full_lines(ws):
    """Full mode: 'speaker_0: words (0.4 s) more words'. A pause that also breaks the line is marked at the end of
    the line it follows."""
    lines, out = lines_of(ws), []
    for i, ln in enumerate(lines):
        parts = [ln[0]["text"]]
        for a, b in zip(ln, ln[1:]):
            if gap(a, b) >= PAUSE:
                parts.append(mark(gap(a, b)))
            parts.append(b["text"])
        nxt = lines[i + 1][0] if i + 1 < len(lines) else None
        if nxt and spk(nxt) == spk(ln[0]):
            parts.append(mark(gap(ln[-1], nxt)))
        out.append(f"{spk(ln[0])}: " + " ".join(parts))
    return out


def rhythm(picks):
    """picks: [(clip file name, Scribe's answer with speaker labels, the labels to count or None for every speaker)].
    Returns the text of rhythm.md. Sentences are counted inside each speaker's own words."""
    n, secs, pauses, sents, head = 0, 0.0, [], [], []
    for clip, r, labels in picks:
        ws = spoken(r)
        every = sorted({spk(w) for w in ws})
        if labels and set(labels) - set(every):
            sys.exit(f"{clip}: no speaker {', '.join(sorted(set(labels) - set(every)))} (it has {', '.join(every)})")
        use = sorted(labels) if labels else every
        for ln in lines_of(ws):
            if spk(ln[0]) in use:
                n += len(ln); secs += ln[-1]["end"] - ln[0]["start"]
        pauses += [gap(a, b) for a, b in zip(ws, ws[1:]) if spk(a) == spk(b) and spk(a) in use and gap(a, b) >= PAUSE]
        for s in use:
            sents += sentences([w for w in ws if spk(w) == s])
        head.append(f"{clip} ({'only ' if labels else 'all speakers: '}{', '.join(use)})")
    if not sents or not secs:
        sys.exit("rhythm: no words from the chosen clips and speakers")
    say = lambda s: " ".join(w["text"] for w in s)
    lo, hi = min(sents, key=len), max(sents, key=len)
    short = sum(len(s) < 5 for s in sents)
    return "\n".join([
        f"Rhythm measured from: {'; '.join(head)}.",
        "",
        "Scribe's words and timings, counted by pipeline/voice_reference.py. A line runs until a gap of "
        f"{LINE_GAP} s or a change of speaker; a pause is a gap of {PAUSE} s or more between two words by one speaker.",
        "",
        f"- Words per second: {n / secs:.2f} ({n} words over {secs:.0f} s of lines, each line timed from its first "
        "word to its last)",
        f"- Average words per sentence: {n / len(sents):.1f}",
        f"- Shortest sentence: {len(lo)} word{'s' if len(lo) != 1 else ''} (\"{say(lo)}\")",
        f"- Longest sentence: {len(hi)} words (\"{say(hi)}\")",
        f"- Share of sentences under 5 words: {100 * short / len(sents):.0f}% ({short} of {len(sents)})",
        f"- Pauses per 10 words: {10 * len(pauses) / n:.1f} ({len(pauses)} pauses)",
        "- Average pause length: " + (f"{sum(pauses) / len(pauses):.2f} s" if pauses else "no pauses"),
        f"- Covers: {secs / 60:.1f} minutes of speech (the lines' time), {len(sents)} sentences",
    ]) + "\n"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("name")
    p.add_argument("--full", action="append", default=[], metavar="PART")
    p.add_argument("--full-all", action="store_true")
    p.add_argument("--rhythm", action="append", default=[], metavar="PART[=LABELS]")
    p.add_argument("--language", default="hi"); p.add_argument("--refresh", action="store_true")
    a = p.parse_args()

    src = os.path.join(ROOT, "work", "voices", "audio", a.name)
    out = os.path.join(ROOT, "docs", "voices", a.name, "reference")
    kept = os.path.join(ROOT, "work", "voices", "scribe", a.name)
    clips = sorted(f for f in os.listdir(src) if f.lower().endswith(AUDIO)) if os.path.isdir(src) else []
    if not clips:
        sys.exit(f"no audio files in {os.path.relpath(src, ROOT)}/")
    names = {}
    for c in clips:                                  # two clips that come to the same file name: -2, -3
        s = base = slug(os.path.splitext(c)[0]); i = 1
        while s in names.values():
            i += 1; s = f"{base}-{i}"
        names[c] = s

    def find(part):
        hits = [c for c in clips if fold(part) in fold(c)]
        if not hits:
            sys.exit(f"no clip in {os.path.relpath(src, ROOT)}/ has '{part}' in its name")
        return hits

    full = set(clips) if a.full_all else {c for part in a.full for c in find(part)}
    picks = {}                                       # clip -> labels, or None for every speaker
    for item in a.rhythm:
        part, _, labels = item.partition("=")
        for c in find(part):
            picks[c] = [l.strip() for l in labels.split(",") if l.strip()] or None
    transcripts = bool(a.full_all or a.full or not a.rhythm)
    cache = lambda c, mode: os.path.join(kept, f"{names[c]}.{mode}.json")
    for c in picks:
        if transcripts and c not in full:
            sys.exit(f"rhythm.md is measured from full-mode clips: add --full for '{c}'")
        if not transcripts and not os.path.exists(cache(c, "full")):
            sys.exit(f"no full-mode answer kept for '{c}': run it with --full first")

    def answer(c, mode):
        f, audio = cache(c, mode), os.path.join(src, c)
        if not a.refresh and os.path.exists(f) and os.path.getmtime(f) >= os.path.getmtime(audio):
            return json.load(open(f, encoding="utf-8")), "kept"
        r = scribe(audio, a.language, mode == "full")
        os.makedirs(kept, exist_ok=True)
        json.dump(r, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        return r, "new"

    if transcripts:
        os.makedirs(out, exist_ok=True)
        for c in clips:
            mode = "full" if c in full else "text"
            r, how = answer(c, mode)
            ws = spoken(r)
            lines = full_lines(ws) if mode == "full" else text_lines(r)
            open(os.path.join(out, names[c] + ".md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
            who = ""
            if mode == "full":
                who = "; " + ", ".join(f"{s} {sum(spk(w) == s for w in ws)} words" for s in sorted({spk(w) for w in ws}))
            print(f"{mode:4} {how:4} {names[c]}.md  <- {c}  ({len(lines)} lines, {len(ws)} words{who})")
    if picks:
        open(os.path.join(out, "rhythm.md"), "w", encoding="utf-8").write(
            rhythm([(c, json.load(open(cache(c, "full"), encoding="utf-8")), picks[c]) for c in clips if c in picks]))
        print("rhythm.md  <- " + "; ".join(f"{c} ({', '.join(picks[c] or ['all speakers'])})" for c in picks))
    print(f"written to {os.path.relpath(out, ROOT)}/")


if __name__ == "__main__":
    main()
