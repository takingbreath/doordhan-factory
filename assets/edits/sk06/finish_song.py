#!/usr/bin/env python3
"""sk06 SONG PREVIEW build (review only, never posted): the final's picture with mix/sk06_mix_song.wav, at 1080x1920,
plus its phone copy and its own QC manifest (qc_manifest_song.json: the same lines; the gate stamps each file).
Run after finish.py: python3 work/sk06/finish_song.py"""
import json, subprocess, sys
SK = "work/sk06"; OUT = "outputs/sk06"; STEM = "E16_space_semis_SONG_PREVIEW"
subprocess.run([sys.executable, f"{SK}/mix_song.py"], check=True)
M = json.load(open(f"{SK}/qc_manifest.json")); TOTAL = M["length"]["expected"]
run = lambda *a: subprocess.run(list(a), check=True)
run("ffmpeg", "-v", "error", "-y", "-i", M["final"], "-i", f"{SK}/mix/sk06_mix_song.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
    "-c:a", "aac", "-b:a", "256k", "-t", f"{TOTAL}", "-movflags", "+faststart", f"{OUT}/{STEM}.mp4")
run("ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/{STEM}.mp4", "-c:v", "libx264", "-crf", "28", "-preset", "slow", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", f"{OUT}/{STEM}_phone.mp4")
M["final"] = f"{OUT}/{STEM}.mp4"; M["rebuild"] = f"python3 {SK}/finish_song.py"; M["note"] = "song preview for Akhilesh's review only; the posted file has no song"
json.dump(M, open(f"{SK}/qc_manifest_song.json", "w"), indent=1)
print(f"{OUT}/{STEM}.mp4", f"{OUT}/{STEM}_phone.mp4", f"{SK}/qc_manifest_song.json")
