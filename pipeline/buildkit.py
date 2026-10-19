#!/usr/bin/env python3
"""Speed for the episode edit scripts (assets/edits/*_build.py), with the same output (jio01, 2026-10-19).

- render_all: renders every shot in parallel and skips a shot whose output is still current. A shot is current when
  its signature matches: the shot's own arguments, the source code of the functions that render it, and the size and
  mtime of every input file it names. Change one shot and only that shot renders again. Each shot is still rendered
  to its own exact frame count by the same ffmpeg command, so the files are the same as a serial build's.
- encode_finals: the 1080x1920 final and the phone copy, both from the burned 720 master, at the same time (preset
  slow, as before). DRAFT=1 in the environment writes only <stem>_draft.mp4 with x264 veryfast (about 4x faster, same
  CRF) for looking at between fixes; the build that goes to the QC gate is a normal one, so the stamped final is
  unchanged in quality.
Measured on the cloud machine (4 vCPU): a full jio01 build was 279 s, of which the two slow encodes were 175 s and
the 12 shots 63 s.
"""
import hashlib, inspect, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor


def workers():
    return max(1, min(8, (os.cpu_count() or 2) // 2))


def _files_in(obj):
    """paths of existing files named anywhere in a shot's arguments"""
    out = []
    if isinstance(obj, dict):
        for v in obj.values():
            out += _files_in(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            out += _files_in(v)
    elif isinstance(obj, str) and os.path.isfile(obj):
        out.append(obj)
    return out


def signature(shot, funcs, extra=None):
    h = hashlib.sha256()
    h.update(repr(shot).encode())
    for f in funcs:
        h.update(inspect.getsource(f).encode())
    for p in sorted(set(_files_in(shot) + list(extra or []))):
        st = os.stat(p); h.update(f"{p}:{st.st_size}:{st.st_mtime_ns}".encode())
    return h.hexdigest()


def render_all(shots, render, out_path, funcs, extra_inputs=None, jobs=None):
    """render(i, shot) -> path for every shot, in parallel; skip shots whose output and signature are current.
    out_path(i, shot) must return the path render() writes. Returns the list of paths in shot order."""
    funcs = [render] + list(funcs)

    def one(i):
        shot = shots[i]; out = out_path(i, shot); sig_file = out + ".sig"
        sig = signature(shot, funcs, (extra_inputs or {}).get(i))
        if os.path.exists(out) and os.path.exists(sig_file) and open(sig_file).read() == sig:
            return out, False
        if os.path.exists(sig_file):
            os.remove(sig_file)
        path = render(i, shot)
        open(sig_file, "w").write(sig)
        return path, True

    with ThreadPoolExecutor(max_workers=jobs or workers()) as ex:
        res = list(ex.map(one, range(len(shots))))
    done = sum(1 for _, r in res if r)
    print(f"  shots: {done} rendered, {len(res) - done} unchanged (cached), {jobs or workers()} at a time")
    return [p for p, _ in res]


def encode_finals(burned, mix, out, phone, fps, scale="1080:1920"):
    """the final and its phone copy from the same master, at the same time (preset slow). DRAFT=1: only a veryfast
    <stem>_draft.mp4 for looking at, never the final's path, so a draft can't reach the QC gate. Returns the paths."""
    common = ["-i", burned, "-i", mix, "-map", "0:v", "-map", "1:a", "-vf", f"scale={scale}:flags=lanczos", "-r", str(fps),
              "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-shortest"]
    if os.environ.get("DRAFT"):
        draft = out.replace(".mp4", "_draft.mp4")
        cmds = [["ffmpeg", "-v", "error", "-y"] + common + ["-c:v", "libx264", "-crf", "17", "-preset", "veryfast",
                                                         "-c:a", "aac", "-b:a", "192k", draft]]
    else:
        cmds = [["ffmpeg", "-v", "error", "-y"] + common + ["-c:v", "libx264", "-crf", "17", "-preset", "slow",
                                                         "-c:a", "aac", "-b:a", "192k", out],
                ["ffmpeg", "-v", "error", "-y"] + common + ["-c:v", "libx264", "-crf", "26", "-preset", "slow",
                                                         "-c:a", "aac", "-b:a", "128k", phone]]
    procs = [subprocess.Popen(c, stderr=subprocess.PIPE, text=True) for c in cmds]
    for c, p in zip(cmds, procs):
        _, err = p.communicate()
        if p.returncode:
            sys.exit(f"FAILED: {' '.join(c)[:300]}\n{err[-1500:]}")
    paths = [c[-1] for c in cmds]
    print("  encoded " + " and ".join(os.path.basename(x) for x in paths) +
          (" (DRAFT, veryfast: for looking only; the QC gate needs a normal build)" if os.environ.get("DRAFT") else " (slow)"))
    return paths
