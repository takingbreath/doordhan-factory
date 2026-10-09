#!/usr/bin/env python3
"""Download the film/TV/web clips an episode needs, on Akhilesh's laptop, and hand them to the cloud sessions.

Why local: YouTube and Instagram refuse downloads from cloud machines ("sign in to confirm you're not a bot", tested
2026-10-09 with yt-dlp, Piped, Invidious and cobalt). From a home connection yt-dlp works.

  python3 pipeline/fetch_clips.py registry/clip_requests/<slug>.json          download, trim, write clips/<slug>/
  python3 pipeline/fetch_clips.py registry/clip_requests/<slug>.json --push   ...then commit them to the `clips` branch
  ... --cookies-from-browser chrome                                            when YouTube asks to sign in

The manifest (written by the cloud session) is a list of clips:
  [{"name": "atc2_open", "url": "https://youtube.com/shorts/...", "start": "0:03", "end": "0:09", "note": "..."}]
`start`/`end` are optional: without them the whole video is kept, capped at --max-seconds (default 180).
Output: clips/<slug>/<name>.mp4 (H.264, at most 1080 px tall, CRF 23, AAC) plus clips/<slug>/manifest.done.json
with each file's duration and source. Clips live on the `clips` branch, never on main, so main stays small.
Needs: yt-dlp (`pip install -U yt-dlp`) and ffmpeg on PATH.
"""
import argparse, json, os, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run(cmd, **kw):
    print("+", " ".join(cmd))
    return subprocess.run(cmd, check=True, **kw)


def secs(t):
    if t is None or t == "":
        return None
    parts = [float(p) for p in str(t).split(":")]
    v = 0.0
    for p in parts:
        v = v * 60 + p
    return v


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout.strip()
    return round(float(out or 0), 2)


def fetch(clip, out_dir, args):
    with tempfile.TemporaryDirectory() as tmp:
        cmd = [sys.executable, "-m", "yt_dlp", "-f", "bv*[height<=1080]+ba/b[height<=1080]/b",
               "--merge-output-format", "mp4", "--no-playlist", "-o", os.path.join(tmp, "src.%(ext)s")]
        if args.cookies_from_browser:
            cmd += ["--cookies-from-browser", args.cookies_from_browser]
        if args.cookies:
            cmd += ["--cookies", args.cookies]
        run(cmd + [clip["url"]])
        src = next(os.path.join(tmp, f) for f in os.listdir(tmp) if f.startswith("src."))
        start, end = secs(clip.get("start")), secs(clip.get("end"))
        length = (end - start) if (start is not None and end is not None) else args.max_seconds
        dst = os.path.join(out_dir, f"{clip['name']}.mp4")
        ff = ["ffmpeg", "-y", "-loglevel", "error"]
        if start is not None:
            ff += ["-ss", str(start)]
        ff += ["-i", src, "-t", str(length), "-vf", "scale=-2:'min(1080,ih)'", "-c:v", "libx264", "-crf", "23",
               "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", dst]
        run(ff)
        return {**clip, "file": os.path.relpath(dst, ROOT), "duration_s": duration(dst)}


def push(slug, files):
    """Commit the clips to the `clips` branch (a worktree, so the user's checkout is untouched) and push."""
    wt = os.path.join(ROOT, ".clips-worktree")
    subprocess.run(["git", "-C", ROOT, "fetch", "origin", "clips"], capture_output=True)
    if not os.path.exists(wt):
        has_remote = subprocess.run(["git", "-C", ROOT, "rev-parse", "--verify", "origin/clips"],
                                    capture_output=True).returncode == 0
        if has_remote:
            run(["git", "-C", ROOT, "worktree", "add", "-B", "clips", wt, "origin/clips"])
        else:
            run(["git", "-C", ROOT, "worktree", "add", "--detach", wt])
            run(["git", "-C", wt, "checkout", "--orphan", "clips"])
            run(["git", "-C", wt, "rm", "-rf", "--quiet", "."])
    else:
        run(["git", "-C", wt, "pull", "--ff-only", "origin", "clips"])
    dest = os.path.join(wt, "clips", slug)
    os.makedirs(dest, exist_ok=True)
    for f in files:
        shutil.copy2(os.path.join(ROOT, f), dest)
    run(["git", "-C", wt, "add", "clips"])
    run(["git", "-C", wt, "commit", "-m", f"clips: {slug}"])
    run(["git", "-C", wt, "push", "-u", "origin", "clips"])


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("manifest")
    p.add_argument("--push", action="store_true", help="commit to the clips branch and push")
    p.add_argument("--cookies-from-browser", help="e.g. chrome, firefox, safari: use your logged-in browser")
    p.add_argument("--cookies", help="a cookies.txt file")
    p.add_argument("--max-seconds", type=float, default=180)
    a = p.parse_args()
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg is not on PATH (macOS: brew install ffmpeg)")
    slug = os.path.splitext(os.path.basename(a.manifest))[0]
    with open(a.manifest) as f:
        clips = json.load(f)
    out_dir = os.path.join(ROOT, "clips", slug)
    os.makedirs(out_dir, exist_ok=True)
    done, failed = [], []
    for c in clips:
        try:
            done.append(fetch(c, out_dir, a))
        except Exception as e:  # keep going; report at the end
            failed.append({**c, "error": str(e)})
    with open(os.path.join(out_dir, "manifest.done.json"), "w") as f:
        json.dump({"done": done, "failed": failed}, f, indent=1, ensure_ascii=False)
    for d in done:
        print(f"OK   {d['name']:<20} {d['duration_s']:>6} s  {d['file']}")
    for d in failed:
        print(f"FAIL {d['name']:<20} {d['error'][:120]}")
    if a.push and done:
        push(slug, [d["file"] for d in done] + [os.path.relpath(os.path.join(out_dir, "manifest.done.json"), ROOT)])


if __name__ == "__main__":
    main()
