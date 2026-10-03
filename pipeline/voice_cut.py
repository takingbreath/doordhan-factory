#!/usr/bin/env python3
"""One draft voice cut of a Sahayata Kendra script, made the way work/cheat1/audio V6b was (3 Oct 2026, Akhilesh's
pick): Pandey's opening line, one ring, the pick-up, the caller on the landline chain (format §6), the clack, the
monologue as one take, then a silence for Billu's beat. Run from the repository root.

Usage: voice_cut.py LINES.json OUT_DIR [--retake ID ...] [--monologue-takes 2]
LINES.json:
  {"name": "w1-1", "caller_voice": "<ElevenLabs voice id>", "billu_s": 1.5,
   "lines": [{"id": "P1", "speaker": "pandey", "text": "[flat, brisk] Dollar का rate कोई तय नहीं करता।"},
             {"id": "C1", "speaker": "caller", "text": "[curious] Hello, ..."},
             {"id": "P2", "speaker": "pandey", "text": "[flat, brisk] तुमको लगता है ...", "monologue": true}]}
  Lines in script order, Billu's silent beat left out (billu_s is its silence). Text is what the voice gets: Devanagari
  with English words in Latin, delivery tags in square brackets.

The recipe, from V6b:
  - Every take gets " [exhales]" after its text, so eleven_v3 doesn't stop the file mid-word (looptest5's fix); the
    breath is trimmed off after the last word.
  - A line marked "monologue" gets --monologue-takes takes (default 2), and the cut uses the slowest one that
    passes: V6b was the slower, more spaced of two clean takes of the same text.
  - Every other line gets one take, and another only if it fails.
  - A take passes when Scribe's transcript matches its line (word skeletons across scripts, at least 85%) and
    verify_line finds the last word intact and not hard-cut. A line that fails gets new takes, up to 3 in all.
  - Each take is trimmed 40 ms after its last word with a 30 ms fade; the caller then gets the landline chain.
  - Ring, pick-up click and cradle clack are synthesised (the looptest6 sounds); gaps 0.35 s, 0.75 s after the clack.
  - The cut is levelled to -16 LUFS, then Scribe transcribes the whole cut against the script.

Writes into OUT_DIR: lines/ (text sent per take), raw/, prep/, check/ (transcripts, verify results), takes.json,
<name>_voice_cut.wav and .mp3, cut.json, report.md. Takes already on disk are reused; --retake ID drops a line's takes
and makes new ones. Exit 0 when every line has a passing take and the cut's transcript matches; 1 when not (report.md
says which); 2 on bad input or when a line has no usable take at all. ElevenLabs allows 3 requests at once: run one voice_cut at a time."""
import argparse, difflib, json, os, re, subprocess, sys, wave
from concurrent.futures import ThreadPoolExecutor
import numpy as np

here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from verify_line import skeleton, tokens  # noqa: E402
from common import FFMPEG  # noqa: E402

SR = 48000
PY = sys.executable
EXHALE = " [exhales]"
PASS_SIM = 0.85
MAX_TAKES = 3
GAP, AFTER_CLACK = 0.35, 0.75
# §6 caller landline chain: band-limit, 8 kHz with a 10-bit log crush, +7 dB at 1.6 kHz, -4 dB at 500 Hz, 6:1
# compression, then pink-noise line hiss band-limited to 400-3000 Hz and loudnorm -17.
PHONE = ("highpass=f=380,lowpass=f=3000,aresample=8000,acrusher=bits=10:mode=log,aresample=48000,"
         "equalizer=f=1600:t=q:w=1:g=7,equalizer=f=500:t=q:w=1:g=-4,"
         "acompressor=threshold=0.1:ratio=6:attack=5:release=80:makeup=2")


def plain(text):
    return re.sub(r"\s+", " ", re.sub(r"\s*\[[^\]]*\]\s*", " ", text)).strip()


def skel_words(text):
    return [s for s in (skeleton(w) for w in tokens(plain(text))) if s]


def similarity(expect, heard):
    """word-skeleton match, so 'dollar' and 'डॉलर' count as the same word"""
    a, b = skel_words(expect), skel_words(heard)
    return difflib.SequenceMatcher(None, a, b).ratio() if a and b else 0.0


def differences(expect, heard):
    """script words Scribe heard differently or not at all, as (script words, heard words)"""
    ew, hw = tokens(plain(expect)), tokens(plain(heard))
    es, hs = [skeleton(w) for w in ew], [skeleton(w) for w in hw]
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, es, hs, autojunk=False).get_opcodes():
        if op != "equal":
            out.append((" ".join(ew[i1:i2]) or "(nothing)", " ".join(hw[j1:j2]) or "(nothing)"))
    return out


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def load(f):
    raw = subprocess.run([FFMPEG, "-v", "error", "-i", f, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def write(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


# ---------------------------------------------------------------- phone sounds (looptest6)
rng = np.random.default_rng(7)


def peak(x, db):
    return x * (10 ** (db / 20) / (np.abs(x).max() + 1e-9))


def strike(freqs, decay, n):
    t = np.arange(n) / SR
    return sum(a * np.sin(2 * np.pi * f * t + rng.uniform(0, 6.28)) * np.exp(-t / (decay * k))
               for (f, a), k in zip(freqs, (1.0, 0.8, 0.6, 0.45)))


GONG_A = [(1175, 1.0), (1590, 0.5), (2410, 0.35), (3320, 0.2)]
GONG_B = [(1240, 1.0), (1660, 0.5), (2520, 0.35), (3460, 0.2)]


def bell(on_s):
    n = int((on_s + 0.35) * SR); x = np.zeros(n, np.float32)
    for k, i in enumerate(range(0, int(on_s * SR), int(SR / 40))):   # 20 Hz clapper on two gongs
        x[i:] += strike(GONG_A if k % 2 else GONG_B, 0.09, n - i) * rng.uniform(0.85, 1.0)
    return x


def ring():   # one ring, Indian cadence: 0.4 s on, 0.2 off, 0.4 on
    a = bell(0.4); b = bell(0.4)
    x = np.zeros(int(1.4 * SR), np.float32)
    x[: len(a)] += a; i = int(0.6 * SR); x[i:i + len(b)] += b[: len(x) - i]
    return x


def transient(lp_hz, decay, n_s, thump_hz=0.0, thump_amp=0.0, n=None):
    n = n or int(n_s * SR); t = np.arange(n) / SR
    noise = rng.standard_normal(n).astype(np.float32)
    a = np.exp(-2 * np.pi * lp_hz / SR); y = np.zeros(n, np.float32); acc = 0.0
    for i in range(n):
        acc = (1 - a) * noise[i] + a * acc; y[i] = acc
    y *= np.exp(-t / decay)
    if thump_hz:
        y += thump_amp * np.sin(2 * np.pi * thump_hz * t) * np.exp(-t / (decay * 1.8))
    return y


def click():   # receiver lifted off the hook
    x = transient(4000, 0.006, 0.12, 140, 0.25)
    j = int(0.035 * SR); x[j:] += 0.5 * transient(3000, 0.005, 0, n=len(x) - j)
    return x


def clack():   # handset dropped into the cradle, with the bell's faint sympathetic ting
    x = transient(1800, 0.02, 0.4, 170, 0.6)
    j = int(0.028 * SR); x[j:] += 0.6 * transient(2200, 0.015, 0, 120, 0.4, n=len(x) - j)
    return x + strike(GONG_A, 0.12, len(x)) * 0.05


def room(x, wet=0.12):   # a small office, so the synthetic sounds sit in a space
    ir_n = int(0.3 * SR); t = np.arange(ir_n) / SR
    ir = rng.standard_normal(ir_n).astype(np.float32) * np.exp(-t / 0.06); ir[0] = 0
    w = np.convolve(x, ir)[: len(x) + ir_n]
    out = np.zeros(len(w), np.float32); out[: len(x)] += x
    return out + wet * w / (np.abs(w).max() + 1e-9) * np.abs(x).max()


# ---------------------------------------------------------------- takes
class Cut:
    def __init__(self, spec, out):
        self.spec, self.out = spec, out
        self.lines = spec["lines"]
        self.by_id = {l["id"]: l for l in self.lines}
        for d in ("lines", "raw", "prep", "check"):
            os.makedirs(os.path.join(out, d), exist_ok=True)
        self.takes_file = os.path.join(out, "takes.json")
        self.takes = json.load(open(self.takes_file)) if os.path.exists(self.takes_file) else {}

    def p(self, *parts):
        return os.path.join(self.out, *parts)

    def save(self):
        json.dump(self.takes, open(self.takes_file, "w"), indent=1, ensure_ascii=False)

    def line_of(self, take):
        return self.by_id[take.rsplit("_t", 1)[0]]

    def is_caller(self, take):
        return self.line_of(take)["speaker"] == "caller"

    def prepped(self, take):
        return self.p("prep", f"{take}_phone.wav" if self.is_caller(take) else f"{take}.wav")

    def new_takes(self, lid, n):
        have = self.takes.setdefault(lid, [])
        start = max([int(t.rsplit("_t", 1)[1]) for t in have] or [0]) + 1
        names = [f"{lid}_t{k}" for k in range(start, start + n)]
        have.extend(names); self.save()
        return names

    def gen(self, takes):
        def one(t):
            line = self.line_of(t)
            src = self.p("lines", f"{t}.txt")
            open(src, "w", encoding="utf-8").write(line["text"].strip() + EXHALE + "\n")
            voice = ["--voice-id", self.spec["caller_voice"]] if line["speaker"] == "caller" else ["--voice", "pandey"]
            r = run([PY, os.path.join(here, "tts_elevenlabs.py"), *voice, "--text-file", src,
                     "--out", self.p("raw", f"{t}.mp3")])
            open(self.p("check", f"{t}.tts.log"), "w").write(r.stdout + r.stderr)
            return t, r.returncode
        with ThreadPoolExecutor(3) as ex:
            for t, rc in ex.map(one, takes):
                print(f"  take {t}: {'made' if rc == 0 else f'FAILED (see check/{t}.tts.log)'}")

    def check(self, take):
        """Scribe, prep (and the landline chain for the caller), verify_line; returns the take's result"""
        line = self.line_of(take); raw = self.p("raw", f"{take}.mp3")
        res = {"take": take, "ok": False}
        if not os.path.exists(raw):
            res["why"] = "no audio (TTS failed)"; return res
        sj = self.p("check", f"{take}.scribe.json")
        r = run([PY, os.path.join(here, "transcribe.py"), raw, "--json", sj])
        if r.returncode != 0 or not os.path.exists(sj):
            res["why"] = "Scribe failed: " + (r.stdout + r.stderr).strip()[-200:]; return res
        heard = json.load(open(sj))["text"]
        r = run([PY, os.path.join(here, "prep_line.py"), raw, self.p("prep", f"{take}.wav")])
        if r.returncode != 0:
            res["why"] = "prep_line failed: " + (r.stdout + r.stderr).strip()[-200:]; return res
        if line["speaker"] == "caller":
            fc = (f"[0:a]{PHONE}[v];"
                  "anoisesrc=color=pink:amplitude=1:sample_rate=48000,highpass=f=400,lowpass=f=3000,volume=-44dB[n];"
                  "[v][n]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-17:TP=-1.5:LRA=11,aresample=48000")
            subprocess.run([FFMPEG, "-v", "error", "-y", "-i", self.p("prep", f"{take}.wav"), "-filter_complex", fc,
                            "-ac", "1", self.prepped(take)], check=True)
        vj = self.p("check", f"{take}.verify.json")
        run([PY, os.path.join(here, "verify_line.py"), self.prepped(take), "--script", line["text"],
             "--transcript", heard, "--cap", "0", "--json", vj])
        if not os.path.exists(vj):
            res["why"] = "verify_line wrote nothing"; return res
        c = json.load(open(vj))["checks"]
        sim = similarity(line["text"], heard)
        lead, end = c["lead"]["lead_s"], c["tail"]["speech_end"]
        res.update(heard=heard, sim=round(sim, 3), lead=lead, speech_end=end, speech_s=round(end - lead, 2),
                   last_word=c["last_word"]["ok"], end_cut=c["end_cut"]["ok"])
        why = []
        if sim < PASS_SIM:
            why.append(f"transcript matches {sim:.0%} (needs {PASS_SIM:.0%})")
        if not c["last_word"]["ok"]:
            why.append(f"last word heard as '{c['last_word'].get('heard')}', not '{c['last_word'].get('script')}'")
        if not c["end_cut"]["ok"]:
            why.append("hard cut at the end")
        res["ok"] = not why
        res["why"] = "; ".join(why)
        return res

    def audio(self, res):
        """the prepped take, cut 40 ms after its last word with a 30 ms fade"""
        x = load(self.prepped(res["take"]))
        n = min(len(x), int((res["speech_end"] + 0.04) * SR)); x = x[:n].copy()
        f = int(0.03 * SR); x[-f:] *= np.linspace(1, 0, f)
        return x


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lines"); ap.add_argument("out")
    ap.add_argument("--retake", action="append", default=[], help="line id whose takes are dropped and remade")
    ap.add_argument("--monologue-takes", type=int, default=2)
    a = ap.parse_args()
    try:
        spec = json.load(open(a.lines, encoding="utf-8"))
        assert re.fullmatch(r"[A-Za-z0-9_.-]+", spec["name"]), "name: letters, digits, . _ - only"
        assert spec["lines"], "no lines"
        for l in spec["lines"]:
            assert re.fullmatch(r"[A-Za-z0-9-]+", l["id"]), f"bad id {l.get('id')!r}"
            assert l["speaker"] in ("pandey", "caller"), f"{l['id']}: speaker must be pandey or caller"
            assert plain(l["text"]), f"{l['id']}: no words"
        assert len({l["id"] for l in spec["lines"]}) == len(spec["lines"]), "line ids repeat"
        if any(l["speaker"] == "caller" for l in spec["lines"]):
            assert spec.get("caller_voice"), "caller_voice missing"
    except (OSError, ValueError, KeyError, AssertionError) as e:
        sys.exit(f"bad lines file {a.lines}: {e}")  # a message exit becomes code 2 (see the bottom)
    cut = Cut(spec, a.out)
    for lid in a.retake:
        for t in cut.takes.pop(lid, []):
            for f in (cut.p("raw", f"{t}.mp3"), cut.p("prep", f"{t}.wav"), cut.p("prep", f"{t}_phone.wav")):
                if os.path.exists(f):
                    os.remove(f)
    cut.save()

    # 1. planned takes, then a retake for every line with no passing take, up to MAX_TAKES per line
    want = {l["id"]: (a.monologue_takes if l.get("monologue") else 1) for l in spec["lines"]}
    todo = [t for l in spec["lines"] for t in cut.new_takes(l["id"], max(0, want[l["id"]] - len(cut.takes.get(l["id"], []))))]
    results = {}
    while True:
        missing = [t for lid in cut.takes for t in cut.takes[lid] if not os.path.exists(cut.p("raw", f"{t}.mp3"))]
        if todo or missing:
            print(f"making {len(set(todo + missing))} take(s)")
            cut.gen(sorted(set(todo + missing)))
        for lid, ts in cut.takes.items():
            for t in ts:
                if t not in results:
                    results[t] = cut.check(t)
                    r = results[t]
                    print(f"  {t}: {'pass' if r['ok'] else 'fail'}"
                          + (f", {r['speech_s']} s, transcript {r['sim']:.0%}" if 'sim' in r else "")
                          + (f" ({r['why']})" if r["why"] else ""))
        todo = []
        for l in spec["lines"]:
            ts = cut.takes[l["id"]]
            if not any(results[t]["ok"] for t in ts) and len(ts) < MAX_TAKES:
                todo += cut.new_takes(l["id"], 1)
        if not todo:
            break

    # 2. the take per line: the slowest passing take for a monologue (V6b), else the first that passes
    chosen, failed = {}, []
    for l in spec["lines"]:
        rs = [results[t] for t in cut.takes[l["id"]]]
        ok = [r for r in rs if r["ok"]]
        if ok:
            chosen[l["id"]] = max(ok, key=lambda r: r["speech_s"]) if l.get("monologue") else ok[0]
        else:
            usable = [r for r in rs if "speech_end" in r]
            if not usable:
                sys.exit(f"{l['id']}: no usable take ({'; '.join(r['why'] for r in rs)}); nothing to cut")
            chosen[l["id"]] = max(usable, key=lambda r: r["sim"])
            failed.append(f"{l['id']}: no take passed; using {chosen[l['id']]['take']} ({chosen[l['id']]['why']})")

    # 3. the cut
    ring_x = room(peak(ring(), -9)); click_x = room(peak(click(), -12)); clack_x = room(peak(clack(), -7))
    ids = [l["id"] for l in spec["lines"]]
    audio = {i: cut.audio(chosen[i]) for i in ids}
    callers = [i for i in ids if cut.by_id[i]["speaker"] == "caller"]
    S, t = {}, 0.0
    for k, i in enumerate(ids):
        if callers and i == callers[0]:                       # one ring, the pick-up, then the caller
            S["ring"] = t + 0.25; S["click"] = S["ring"] + 1.2; t = S["click"] + 0.33
        elif k and cut.by_id[ids[k - 1]]["speaker"] == "caller":   # he hangs up after the caller, before he speaks
            S["clack"] = t + 0.6; t = S["clack"] + AFTER_CLACK
        elif k:
            t += GAP
        S[i] = t; t += len(audio[i]) / SR
    S["billu"] = t
    total = t + float(spec.get("billu_s", 1.5))
    n = int(total * SR); bus = np.zeros(n, np.float32)

    def put(x, at):
        j0 = int(at * SR); j1 = min(n, j0 + len(x)); bus[j0:j1] += x[: j1 - j0]
    for i in ids:
        put(audio[i], S[i])
    if "ring" in S:
        put(ring_x, S["ring"]); put(click_x, S["click"])
    if "clack" in S:
        put(clack_x, S["clack"] - 0.02)
    base = cut.p(f"{spec['name']}_voice_cut")
    write(base + "_tmp.wav", bus)
    subprocess.run([FFMPEG, "-v", "error", "-y", "-i", base + "_tmp.wav", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                    "-ar", str(SR), base + ".wav"], check=True)
    subprocess.run([FFMPEG, "-v", "error", "-y", "-i", base + ".wav", "-codec:a", "libmp3lame", "-b:a", "192k",
                    base + ".mp3"], check=True)
    os.remove(base + "_tmp.wav")

    # 4. Scribe on the whole cut, against the script
    expect = " ".join(plain(cut.by_id[i]["text"]) for i in ids)
    open(cut.p("check", "cut.expect"), "w", encoding="utf-8").write(expect + "\n")
    sj = cut.p("check", "cut.scribe.json")
    r = run([PY, os.path.join(here, "transcribe.py"), base + ".mp3", "--expect-file", cut.p("check", "cut.expect"),
             "--json", sj])
    open(cut.p("check", "cut.scribe.log"), "w").write(r.stdout + r.stderr)
    heard = json.load(open(sj))["text"] if os.path.exists(sj) else ""
    sim = similarity(expect, heard)
    scribe_line = next((ln for ln in (r.stdout + r.stderr).splitlines() if "similarity" in ln), "no Scribe result")
    if sim < PASS_SIM:
        failed.append(f"whole cut: transcript matches {sim:.0%} (needs {PASS_SIM:.0%})")
    diffs = differences(expect, heard)

    report = {"name": spec["name"], "cut_s": round(total, 2), "with_card_s": round(total + 4.8, 2),
              "timeline_s": {k: round(v, 2) for k, v in S.items()},
              "takes": {i: {k: chosen[i][k] for k in ("take", "sim", "speech_s")} for i in ids},
              "cut_transcript_match": round(sim, 3), "scribe": scribe_line, "failed": failed}
    json.dump(report, open(cut.p("cut.json"), "w"), indent=1, ensure_ascii=False)
    md = [f"# Voice cut: {spec['name']}", "",
          f"- File: {base}.mp3",
          f"- Length: {total:.1f} s; with the 4.8 s closing card, {total + 4.8:.1f} s",
          f"- Whole-cut transcript against the script: {sim:.0%} word match (Scribe's own score: {scribe_line.strip()})",
          f"- Result: {'PASS' if not failed else 'FAIL'}", ""]
    if failed:
        md += ["## What failed", ""] + [f"- {f}" for f in failed] + [""]
    md += ["## Takes", "", "| Line | Take used | Takes made | Speech | Transcript |", "|---|---|---|---|---|"]
    for i in ids:
        c = chosen[i]
        md.append(f"| {i}{' (monologue)' if cut.by_id[i].get('monologue') else ''} | {c['take']} | "
                  f"{len(cut.takes[i])} | {c['speech_s']} s | {c['sim']:.0%} |")
    md += ["", "## Words Scribe heard differently", "",
           "Scribe writes dialect in standard spelling (ई as ये, ऊ as वो, तुमरा as तुम्हारा) and English words in "
           "either script, so most of these are spelling. Listen at the others.", ""]
    md += [f"- script \"{e}\" → heard \"{h}\"" for e, h in diffs] or ["- None"]
    md += ["", "## Whole-cut transcript", "", heard or "(none)", ""]
    open(cut.p("report.md"), "w", encoding="utf-8").write("\n".join(md))
    print(f"{spec['name']}: {total:.1f} s ({total + 4.8:.1f} s with the card), transcript {sim:.0%}, "
          f"{'PASS' if not failed else 'FAIL: ' + '; '.join(failed)}")
    print(f"wrote {base}.mp3 and {cut.p('report.md')}")
    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        if isinstance(e.code, str):
            print(e.code, file=sys.stderr); sys.exit(2)
        raise
