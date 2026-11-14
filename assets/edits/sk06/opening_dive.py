#!/usr/bin/env python3
"""sk06 opening v4 (Akhilesh on v3, 2026-11-14: "so much better"; text in the scene, e.g. LONG-TERM in yellow on the
red bus roof; one colour grade so it reads as one video). v3's timing, plus:
  - the Wan 2.7 dive and glide graded to the Wan 3.0 look (grade_match.py -> S1_wan27_g, T1g_g);
  - LONG-TERM painted on the roof, tracked as a plane (roof_text.py -> S1_wan27_gt);
  - the first real cut (5.62 s, the pause before "doosra") is a 1.2x punch-in on T1w3, scaled about his eyes, so the
    cut reads as a move in, not as a jump between two near-identical framings.
Run from the repository root."""
import subprocess, sys
sys.path.insert(0, "pipeline")
from common import FFMPEG  # noqa: E402
W = "work/sk06"
VOICE_AT, SEAM, END = 0.12, 1.60, 7.30
DIVE_T = 2.5
SLOW_C, SLOW_R = 0.38, 0.54
CUT = 5.62
PUNCH, FX, FY = 1.2, 0.509, 0.475          # scale, the face point (eyes) as fractions of the frame
g_c = lambda r: r - SEAM - 0.16
c_3 = lambda r: r - VOICE_AT - (1.85 - 0.5) - 0.22
cw, chh = 720 / PUNCH, 1280 / PUNCH
cx0, cy0 = FX * 720 * (1 - 1 / PUNCH), FY * 1280 * (1 - 1 / PUNCH)
fc = (f"[0:v]trim=0:{DIVE_T},setpts=(PTS-STARTPTS)*{SEAM / DIVE_T:.5f},fps=30,scale=720:1280:flags=lanczos,setsar=1[d];"
      f"[1:v]trim=0:{SLOW_C},setpts=(PTS-STARTPTS)*{SLOW_R / SLOW_C:.5f},fps=30,scale=720:1280:flags=lanczos,setsar=1[g1];"
      f"[1:v]trim={SLOW_C}:{g_c(CUT):.3f},setpts=PTS-STARTPTS,fps=30,scale=720:1280:flags=lanczos,setsar=1[g2];"
      f"[2:v]trim={c_3(CUT):.3f}:{c_3(END):.3f},setpts=PTS-STARTPTS,fps=30,scale=720:1280:flags=lanczos,"
      f"crop={cw:.0f}:{chh:.0f}:{cx0:.0f}:{cy0:.0f},scale=720:1280:flags=lanczos,setsar=1[t];"
      f"[d][g1][g2][t]concat=n=4:v=1:a=0[v];"
      f"[3:a]atrim=0:{END - VOICE_AT},asetpts=PTS-STARTPTS,adelay={int(VOICE_AT * 1000)}:all=1[vo];"
      f"[4:a]atrim=25.98:{25.98 + END},asetpts=PTS-STARTPTS,volume='if(lt(t,0.3),0.55,if(lt(t,1.6),0.55-0.5*(t-0.3)/1.3,0.05))':eval=frame[so];"
      f"[5:a]atrim=0:{END},asetpts=PTS-STARTPTS,volume='if(lt(t,1.5),0.15,min(1,0.15+0.85*(t-1.5)/0.6))*0.35':eval=frame[bd];"
      f"[vo][so][bd]amix=inputs=3:duration=longest:normalize=0,atrim=0:{END},loudnorm=I=-14:TP=-1.5[a]")
out = f"{W}/vid/opening_v4.mp4"
subprocess.run([FFMPEG, "-v", "error", "-y", "-i", f"{W}/vid/S1_wan27_gt.mp4", "-i", f"{W}/vid/T1g_g.mp4",
                "-i", f"{W}/vid/T1w3.mp4", "-i", f"{W}/voice2/sk06_voice_v2.wav", "-i", f"{W}/music/zindagi.mp3",
                "-i", f"{W}/sfx/bus_bed_a.mp3", "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", str(END), out],
               check=True)
print(out)
