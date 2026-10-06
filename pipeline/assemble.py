#!/usr/bin/env python3
"""Assemble the final reel from an edit list, apply the old-TV look (look.py), loudness, and 1080x1920 output.
Usage: assemble.py work/<ep>/edit.json
edit.json:
{ "out": "outputs/<ep>/final.mp4",
  "parts": [ {"file": "work/<ep>/A.mp4", "start": 0, "end": 4.06, "audio_shift_ms": 160},
             {"file": "work/<ep>/montage.mkv", "lufs": -17},
             {"file": "work/<ep>/C.mp4", "start": 0.1, "end": 13.0} ],
  "target_lufs": -14, "look": "broadcast", "tv_audio": true }
"look": broadcast (default) | vhs | kendra (Sahayata Kendra: clearer, brighter) | clean (the Sept 2026 finish) | none. "finish": false still means no look.
"tv_audio": mono, 90 Hz-10 kHz, like a TV speaker (default true; the loudness target is measured after it).
Cut points must come from speech_map.py on each generated clip. Never cut before the last word.
Each part with sound is levelled to its "lufs" (default -16, the line level) before joining: video models change
the level of the track we give them (Wan raised one by 3 dB), which undoes the per-line levelling. "lufs": null skips it.
Finish defaults (2026-09-29, from the realism test, docs/lab/2026-09-29-reads-as-ai.md):
  "voice_room": true   every part with sound goes through voice_room.py (120 Hz-7 kHz, light tape saturation, a small
                       office room; no hiss). Mark music, stings, montage, a phone caller, or a mix already treated in
                       its own build with "room": false on the part.
  "ambience": "office" recorded CC0 room ambience (ambience.py: fan + distant road) under the whole reel at
                       "ambience_db" (default -36) relative to the programme; null for none (a build with its own bed).
  "vhs_motion": 0.65   the tape's movement (vhs_motion.py: line jitter, colour bleed, streak noise, dropouts) at this
                       strength, applied to the edit before the look; the look keeps its own colour. 0 turns it off.
Also writes <out>_prefinish.mkv: the joined edit before the VHS pass and the look, with the final sound's timing.
qc_gate.py runs the lip-sync check on it (the finish lowers SyncNet's confidence and can fake a lag)."""
import json, os, shutil, subprocess, sys, tempfile, wave
import numpy as np
from common import FFMPEG, FFPROBE, W, H, FPS, run, duration, loudness
from look import PRESETS, filtergraph, scanline_mask
import ambience, vhs_motion, voice_room

spec = json.load(open(sys.argv[1]))
tmp = tempfile.mkdtemp()
parts, bounds, t = [], [], 0.0
for i, p in enumerate(spec["parts"]):
    f = p["file"]
    start = float(p.get("start", 0)); end = float(p.get("end", duration(f)))
    L = end - start
    has_audio = bool(subprocess.run([FFPROBE, "-v", "error", "-select_streams", "a", "-show_entries",
                                     "stream=index", "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip())
    out = os.path.join(tmp, f"p{i:02d}.mkv")
    # 25 fps by blending neighbouring frames, not dropping one in six (Wan delivers 30 fps): dropping left a regular
    # judder (every 5th step 30% larger); blending evened it (0.90-1.08) with no edge doubling and unchanged lip sync
    # (2026-09-29, docs/lab/2026-09-29-continuity-and-finish.md). A 25 fps source passes through unchanged.
    vf = f"scale={W}:{H}:flags=lanczos,framerate=fps={FPS},format=yuv420p,setsar=1"
    af = f"aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.03,afade=t=out:st={max(0, L-0.05):.3f}:d=0.05"
    # lip-sync repair (lipsync_lag.py "constant" pattern): + delays this part's audio, - pulls it earlier; length kept
    shift = float(p.get("audio_shift_ms", 0)) / 1000
    if shift > 0:
        af = f"adelay={int(shift * 1000)}:all=1," + af
    elif shift < 0:
        af = f"atrim=start={-shift:.3f},asetpts=PTS-STARTPTS," + af
    # pad every part's audio to its picture length: a part whose audio ran 20-70 ms short made the concat slide
    # every later line earlier (DTB3, 2026-10-06: 0.3 s ahead of the lips by 48 s)
    af = af.replace("afade=t=in", "apad,afade=t=in", 1)
    cmd = [FFMPEG, "-y", "-v", "error", "-ss", f"{start:.3f}", "-i", f]
    if has_audio:
        cmd += ["-t", f"{L:.3f}", "-vf", vf, "-af", af]
    else:
        cmd += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{L:.3f}", "-vf", vf,
                "-map", "0:v", "-map", "1:a"]
    cmd += ["-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-pix_fmt", "yuv420p",
            "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", out]
    run(cmd)
    if has_audio and spec.get("voice_room", True) and p.get("room", True):
        roomed = out + ".room.mkv"; voice_room.treat_file(out, roomed); shutil.move(roomed, out)
    target = p.get("lufs", -16)
    if has_audio and target is not None:
        I0, _ = loudness(out)
        if I0 is not None and I0 > -60 and abs(target - I0) > 0.3:
            pre = out + ".pre.mkv"; shutil.move(out, pre)
            run([FFMPEG, "-y", "-v", "error", "-i", pre, "-c:v", "copy", "-af",
                 f"volume={target - I0:.2f}dB,alimiter=limit=0.84:level=false", "-c:a", "pcm_s16le", out])
            print(f"part {i}: levelled {I0} -> {target} LUFS")
    parts.append(out); t += duration(out); bounds.append(t)
lst = os.path.join(tmp, "list.txt")
open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
joined = os.path.join(tmp, "joined.mkv")
run([FFMPEG, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-crf", "16",
     "-preset", "veryfast", "-c:a", "pcm_s16le", joined])
# Sound: a TV speaker (mono, no deep bass, no air) unless "tv_audio": false; loudness is measured after it.
audio = os.path.join(tmp, "audio.wav")
tv = "pan=mono|c0=0.5*c0+0.5*c1,highpass=f=90,lowpass=f=10000,pan=stereo|c0=c0|c1=c0" if spec.get("tv_audio", True) \
    else "anull"
pack = spec.get("ambience", "office")
if pack:
    raw = os.path.join(tmp, "raw.wav")
    run([FFMPEG, "-y", "-v", "error", "-i", joined, "-vn", "-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le", raw])
    w = wave.open(raw); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32) / 32768
    I0, _ = loudness(raw)
    b = ambience.bed(len(x) / 48000 + 0.01, pack)[: len(x)]
    rel_db = float(spec.get("ambience_db", ambience.DEFAULT_DB))
    b *= 10 ** (((I0 if I0 is not None and I0 > -60 else -16) + rel_db - ambience.rms_db(b)) / 20)
    x = x + b[:, None]
    bedded = os.path.join(tmp, "bedded.wav")
    w = wave.open(bedded, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(48000)
    w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    print(f"ambience '{pack}' at {rel_db:+.0f} dB relative to the programme")
    run([FFMPEG, "-y", "-v", "error", "-i", bedded, "-af", tv, "-c:a", "pcm_s16le", audio])
else:
    run([FFMPEG, "-y", "-v", "error", "-i", joined, "-vn", "-af", tv, "-c:a", "pcm_s16le", audio])
I, _ = loudness(audio)
prefinish = os.path.splitext(spec["out"])[0] + "_prefinish.mkv"
os.makedirs(os.path.dirname(os.path.abspath(spec["out"])), exist_ok=True)
run([FFMPEG, "-y", "-v", "error", "-i", joined, "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
     "-c:a", "pcm_s16le", "-shortest", prefinish])
strength = float(spec.get("vhs_motion", vhs_motion.DEFAULT_STRENGTH))
if strength > 0 and spec.get("finish", True):
    moved = os.path.join(tmp, "joined_vhs.mkv")
    # As its own process, not vhs_motion.run(): its worker pool re-imports the main script on macOS (spawn), and this
    # script has no __main__ guard, so every worker re-ran the whole assembly and the pool never finished.
    run([sys.executable, vhs_motion.__file__, joined, moved, "--strength", str(strength)])
    joined = moved
    print(f"vhs motion at {strength:.2f}")
gain = spec.get("target_lufs", -14) - I
look = spec.get("look", "broadcast") if spec.get("finish", True) else "none"
if look == "none":
    graph = "[0:v]scale=1080:1920:flags=lanczos,format=yuv420p[v]"
else:
    graph = filtergraph(look, mask="[2:v]")
mask = scanline_mask(os.path.join(tmp, "scan.png"), (PRESETS.get(look) or {}).get("scan", 0))
os.makedirs(os.path.dirname(os.path.abspath(spec["out"])), exist_ok=True)
run([FFMPEG, "-y", "-v", "error", "-i", joined, "-i", audio, "-loop", "1", "-i", mask,
     "-filter_complex", graph, "-map", "[v]", "-map", "1:a",
     "-af", f"volume={gain:.2f}dB,alimiter=limit=0.84:level=false", "-shortest",
     "-c:v", "libx264", "-crf", "19", "-preset", "veryfast", "-profile:v", "high", "-pix_fmt", "yuv420p",
     "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", spec["out"]])
L = duration(spec["out"]); I2, P2 = loudness(spec["out"])
print(f"{spec['out']}: {L:.1f}s  loudness {I2} LUFS  peak {P2} dBFS  look {look}")
print("joins at:", [round(b, 2) for b in bounds[:-1]])
times = [x for b in bounds[:-1] for x in (max(0, b - 0.15), b + 0.15)] + [max(0, L - 0.2)]
sheet = os.path.splitext(spec["out"])[0] + "_joins.png"
here = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, os.path.join(here, "contact_sheet.py"), spec["out"], sheet, "--times",
                *[f"{x:.2f}" for x in times]], check=True, capture_output=True)
print("joins sheet:", sheet)
