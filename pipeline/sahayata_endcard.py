#!/usr/bin/env python3
"""The Doordhan Sahayata Kendra closing card, built once and reused on every episode.
Sound: the call cuts (three short 400 Hz beeps, an Indian landline's disconnect), then the Kendra's hold music:
Für Elise (Beethoven, public domain) on a thin, cheap 90s keyboard, down a phone line.
Picture: a flicker of TV snow, then the card snaps in and creeps forward; the broadcast look is applied last.
  sahayata_endcard.py [--out assets/clips/sahayata_endcard.mp4] [--seconds 4.8]"""
import argparse, os, subprocess, tempfile, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "assets", "fonts")
W, H, SR = 1080, 1920, 44100


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size, layout_engine=ImageFont.Layout.RAQM)


def centered(d, y, text, f, fill, shadow=(0, 0, 0), off=6, stroke=0, stroke_fill=None):
    w = d.textlength(text, font=f)
    x = (W - w) / 2
    d.text((x + off, y + off), text, font=f, fill=shadow)
    d.text((x, y), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)


def card(path):
    # Deep Doordarshan blue with a soft vertical gradient and a faint sunburst behind the text.
    y = np.linspace(0, 1, H)[:, None]
    top, bot = np.array([18, 40, 110]), np.array([6, 14, 52])
    bg = (top * (1 - y) + bot * y)[:, None, :].repeat(W, 1).reshape(H, W, 3)
    img = Image.fromarray(bg.astype(np.uint8))
    rays = Image.new("L", (W, H), 0)
    rd = ImageDraw.Draw(rays)
    cx, cy = W / 2, H * 0.47
    for k in range(24):
        a0, a1 = np.radians(k * 15), np.radians(k * 15 + 6)
        rd.polygon([(cx, cy), (cx + 2000 * np.cos(a0), cy + 2000 * np.sin(a0)),
                    (cx + 2000 * np.cos(a1), cy + 2000 * np.sin(a1))], fill=26)
    img = Image.composite(Image.new("RGB", (W, H), (70, 110, 200)), img, rays.filter(ImageFilter.GaussianBlur(6)))
    d = ImageDraw.Draw(img)
    # Header strip
    d.rectangle([0, 250, W, 400], fill=(232, 176, 28))
    centered(d, 268, "DOORDHAN", font("Bungee.ttf", 70), (20, 30, 80), shadow=(160, 110, 10), off=4)
    centered(d, 338, "SAHAYATA KENDRA", font("Bungee.ttf", 44), (20, 30, 80), shadow=(160, 110, 10), off=3)
    # Logo, if present
    logo = os.path.join(ROOT, "assets", "logos", "doordhan_logo.png")
    if os.path.exists(logo):
        lg = Image.open(logo).convert("RGBA")
        lg.thumbnail((190, 190))
        img.paste(lg, ((W - lg.width) // 2, 470), lg)
    # The line itself, in Roman Hinglish (Akhilesh: on-screen text is Hinglish, never Devanagari), big and chunky
    big = font("Baloo2-Latin-ExtraBold.ttf", 132)
    for i, line in enumerate(["AAPKI CALL", "HAMARE LIYE", "MAHATVAPURN", "THI."]):
        centered(d, 730 + i * 150, line, big, (255, 250, 235), shadow=(0, 0, 0), off=8, stroke=3,
                 stroke_fill=(10, 20, 60))
    centered(d, 1370, "(Your call was important to us.)", font("Baloo2-Latin-ExtraBold.ttf", 46),
             (232, 176, 28), off=3)
    # Footer: the in-world phone number and a thin rule
    d.rectangle([140, 1520, W - 140, 1526], fill=(232, 176, 28))
    centered(d, 1560, "DAYA KARKE LINE PAR BANE RAHEIN", font("Bungee.ttf", 40), (200, 210, 240), off=3)
    img.save(path)


def tone(freqs, dur, amp=0.35):
    t = np.arange(int(SR * dur)) / SR
    x = sum(np.sin(2 * np.pi * f * t) for f in freqs) / len(freqs)
    env = np.minimum(1, np.minimum(t / 0.005, (dur - t) / 0.005))
    return amp * x * env


def hold_music(seconds):
    # Für Elise, opening phrase: (note, eighths)
    E5, Ds5, D5, C5, B4, A4, Gs4, E4, C4, A3 = 659.3, 622.3, 587.3, 523.3, 493.9, 440.0, 415.3, 329.6, 261.6, 220.0
    tune = [(E5, 1), (Ds5, 1), (E5, 1), (Ds5, 1), (E5, 1), (B4, 1), (D5, 1), (C5, 1), (A4, 2),
            (C4, 1), (E4, 1), (A4, 1), (B4, 2), (E4, 1), (Gs4, 1), (B4, 1), (C5, 2), (E4, 1),
            (E5, 1), (Ds5, 1), (E5, 1), (Ds5, 1), (E5, 1), (B4, 1), (D5, 1), (C5, 1), (A4, 2)]
    eighth, out = 0.2, []
    for f, n in tune:
        dur = eighth * n
        t = np.arange(int(SR * dur)) / SR
        # thin cheap-keyboard voice: square-ish (odd harmonics) with a fast decay and a little vibrato
        vib = 1 + 0.004 * np.sin(2 * np.pi * 5.5 * t)
        x = sum(np.sin(2 * np.pi * f * k * vib * t) / k for k in (1, 3, 5))
        env = np.exp(-t * 4.0) * np.minimum(1, t / 0.01)
        out.append(0.28 * x * env)
    x = np.concatenate(out)
    return x[: int(SR * seconds)] if len(x) > SR * seconds else np.pad(x, (0, int(SR * seconds) - len(x)))


def audio(path, seconds):
    beep, gap = tone([400], 0.18), np.zeros(int(SR * 0.14))
    cut = np.concatenate([np.zeros(int(SR * 0.1)), beep, gap, beep, gap, beep, np.zeros(int(SR * 0.25))])
    music = hold_music(seconds - len(cut) / SR)
    fade = np.minimum(1, np.linspace(0, len(music) / SR, len(music)) / 0.15)
    music = music * fade
    music[-int(SR * 0.4):] *= np.linspace(1, 0, int(SR * 0.4))
    x = np.concatenate([cut, music])
    pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "assets", "clips", "sahayata_endcard.mp4"))
    ap.add_argument("--seconds", type=float, default=4.8)
    a = ap.parse_args()
    tmp = tempfile.mkdtemp()
    png, wav, raw = (os.path.join(tmp, n) for n in ("card.png", "end.wav", "raw.mp4"))
    card(png)
    audio(wav, a.seconds)
    snow = 0.25  # a flicker of TV snow, then the card snaps in and creeps forward
    fc = (f"color=c=black:s={W}x{H}:d={snow}:r=25,noise=alls=100:allf=t+u,format=yuv420p[s];"
          f"[0:v]scale={W * 2}:{H * 2},zoompan=z='1+0.0006*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
          f"d={int((a.seconds - snow) * 25)}:s={W}x{H}:fps=25,format=yuv420p[c];[s][c]concat=n=2:v=1:a=0[v];"
          f"[1:a]highpass=f=300,lowpass=f=3400,aformat=channel_layouts=mono[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", png, "-i", wav, "-filter_complex", fc,
                    "-map", "[v]", "-map", "[a]", "-t", str(a.seconds), "-c:v", "libx264", "-crf", "16",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", raw], check=True)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    subprocess.run(["python3", os.path.join(ROOT, "pipeline", "look.py"), raw, a.out], check=True)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
