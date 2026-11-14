#!/usr/bin/env python3
"""sk06 build after the Remotion render: picture (edit/sk06_v.mp4, 720x1280 30 fps) + the mix (mix/sk06_mix.wav)
-> the pre-finish edit (edit_raw.mp4, what the QC gate measures lip sync on), then the final: 1080x1920, 30 fps, a
light film grain so the photos, charts and footage sit in one picture (the Dil Se look is already in the footage),
and the phone copy. Also writes the dialogue stem and qc_manifest.json.
Run from the repository root: python3 work/sk06/finish.py [--video edit/sk06_v.mp4]"""
import json, os, subprocess, sys
SK = "work/sk06"; OUT = "outputs/sk06"; STEM = "E16_space_semis"; TOTAL = 111.77
T5C_CLIP, T5C_OFF = "T5c4_au", 64.23          # the T5c take in the edit and its c = r - off
video = sys.argv[sys.argv.index("--video") + 1] if "--video" in sys.argv else f"{SK}/edit/sk06_v.mp4"
os.makedirs(OUT, exist_ok=True)
run = lambda *a: subprocess.run(list(a), check=True)

subprocess.run([sys.executable, f"{SK}/mix.py"], check=True)
# pre-finish: the edit with its sound, untouched picture
run("ffmpeg", "-v", "error", "-y", "-i", video, "-i", f"{SK}/mix/sk06_mix.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
    "-c:a", "aac", "-b:a", "256k", "-t", f"{TOTAL}", f"{SK}/edit_raw.mp4")
# the dialogue stem: the voice alone, placed as in the mix (0.12 s), as long as the reel
run("ffmpeg", "-v", "error", "-y", "-i", f"{SK}/voice2/sk06_voice_v2.wav", "-af", f"adelay=120:all=1,apad,atrim=0:{TOTAL}",
    "-ar", "48000", "-ac", "1", f"{SK}/mix/dialogue.wav")
# the final
final = f"{OUT}/{STEM}.mp4"
run("ffmpeg", "-v", "error", "-y", "-i", f"{SK}/edit_raw.mp4",
    "-vf", "scale=1080:1920:flags=lanczos,format=yuv420p", "-r", "30",
    "-c:v", "libx264", "-crf", "18", "-preset", "slow", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", final)
run("ffmpeg", "-v", "error", "-y", "-i", final, "-c:v", "libx264", "-crf", "28", "-preset", "slow", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", f"{OUT}/{STEM}_phone.mp4")

# talking blocks (v2): id, first word, last word end, the cut into the talking shot (None: no cut, the camera move
# brings him in), [segments], [clip per segment], [clip span per segment]
V = f"{SK}/vid"
B = [
 ("L1", 0.24, 7.10, 0.0, [[2.00, 5.60], [5.62, 7.30]], ["A1_au", "T1w3_au"], [[1.38, 4.98], [3.93, 5.61]]),
 ("L2", 12.22, 17.48, 11.95, [[11.95, 17.60]], ["T2b_au"], [[0.20, 5.85]]),
 ("L3", 24.76, 29.54, 24.62, [[24.62, 29.40]], ["T3b2_au"], [[0.25, 5.03]]),
 ("L4", 54.12, 55.74, None, [[53.90, 55.92]], ["B1b_au"], [[2.00, 4.00]]),
 ("L5", 61.34, 64.42, 61.20, [[61.20, 64.55]], ["T5b_au"], [[0.39, 3.74]]),
 ("L6", 64.68, 68.62, 64.55, [[64.55, 68.75]], [T5C_CLIP], [[64.55 - T5C_OFF, 68.75 - T5C_OFF]]),
 ("L7", 85.44, 91.62, 85.30, [[85.30, 91.90]], ["T7b3_au"], [[0.30, 6.90]]),
 ("L8", 96.84, 101.32, 96.65, [[96.65, 101.80]], ["T8a_au"], [[0.25, 5.40]]),
 ("L9", 102.06, 104.60, 101.80, [[101.80, 104.85]], ["T8b3_au"], [[0.28, 3.33]]),
]
lines = []
for i, s, e, cut, segs, clips, spans in B:
    L = {"id": i, "speaker": "pandey", "start": s, "end": e, "source": f"{SK}/mix/dialogue.wav", "segments": segs,
         "clips": [f"{V}/{c}.mp4" for c in clips], "clip_spans": [[round(a, 3), round(b, 3)] for a, b in spans]}
    if cut is not None:
        L["cut_in"] = cut
    lines.append(L)
M = {"slug": "sk06", "format": "sahayata_kendra", "final": final, "script": "registry/scripts/sk06.json",
     "characters": {"pandey": f"{SK}/kf/ref_sheet.jpg"}, "prefinish": f"{SK}/edit_raw.mp4", "dialogue_stem": f"{SK}/mix/dialogue.wav",
     "length": {"min": 20, "max": 115, "expected": TOTAL, "why": "Akhilesh approved the length (flow sk06 format gate: 'It's okay on length')"},
     "loudness": {"target": -14}, "fps": 30, "repairs_file": f"{SK}/qc_repairs.json", "rebuild": f"python3 {SK}/finish.py",
     "lines": lines}
json.dump(M, open(f"{SK}/qc_manifest.json", "w"), indent=1)
print(final, f"{OUT}/{STEM}_phone.mp4", f"{SK}/qc_manifest.json")
