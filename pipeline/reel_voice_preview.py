#!/usr/bin/env python3
"""Render ONE gate-checked draft preview with the existing voice_cut tool; never approves or freezes it.
Usage: reel_voice_preview.py SLUG [--retake LINE_ID]
The performance agent supplies audio/<script-stem>/lines.json with unchanged script_text per spoken line,
voice-ready text, format, name, script_sha256 and story_digest. All checks below precede any network call.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

from reel_script_gate import ROOT, digest, folder, local, relative, status


def words(text):
    return re.findall(r'[\w]+', text.casefold(), flags=re.UNICODE)


def script_words(text):
    spoken = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        match = re.match(r'\*\*([A-Z][A-Z0-9_]*)\*\*:\s*(.*)', line)
        if match:
            if match[1] == 'BILLU':
                continue
            line = match[2]
        line = re.sub(r'\[[^\]]*\]', '', line)
        spoken.append(line)
    return words(' '.join(spoken))


def prepare(slug):
    current = status(slug)
    if current['status'] != 'ready_for_voice':
        raise ValueError(f"Voice cannot run at {current['status']}")
    base = folder(slug)
    script = local(base, current['script'])
    out = (ROOT / current['voice_dir']).resolve()
    plan = local(base, relative(out / 'lines.json'))
    spec = json.loads(plan.read_text())
    if (spec.get('name') != out.name or spec.get('script_sha256') != current['script_sha256']
            or spec.get('story_digest') != current['story_digest']
            or spec.get('format') != current['brief']['format']):
        raise ValueError('Voice plan is not bound to the checked script, story and format')
    lines = spec.get('lines', [])
    if not lines or any(not isinstance(l, dict) or not l.get('text') or not l.get('script_text')
                        or l.get('speaker') not in current['brief']['cast'] for l in lines):
        raise ValueError('Missing voice lines, source words or selected cast member')
    if words(' '.join(l['script_text'] for l in lines)) != script_words(script.read_text()):
        raise ValueError('Voice plan adds, drops, reorders or changes manuscript words')
    voices = json.loads((ROOT / 'registry' / 'assets.json').read_text()).get('voices', {})
    for line in lines:
        if spec['format'] == 'sahayata_kendra' and line['speaker'] == 'caller':
            if not spec.get('caller_voice'):
                raise ValueError('Kendra caller voice is not configured')
        elif not (voices.get(line['speaker']) or {}).get('elevenlabs_voice_id'):
            raise ValueError(f"No configured ElevenLabs voice for {line['speaker']}")
    return current, out, plan


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('slug')
    parser.add_argument('--retake', action='append', default=[])
    args = parser.parse_args()
    current, out, plan = prepare(args.slug)
    if any(not re.fullmatch(r'[A-Za-z0-9-]+', line) for line in args.retake):
        raise ValueError('Invalid retake line id')
    command = [sys.executable, str(ROOT / 'pipeline' / 'voice_cut.py'), relative(plan), relative(out)]
    for line in args.retake:
        command += ['--retake', line]
    result = subprocess.run(command, cwd=ROOT)
    if result.returncode:
        return result.returncode
    # Recheck after rendering: a concurrent edit must not get a clean voice-review record.
    now = status(args.slug)
    if (now.get('script_sha256') != current['script_sha256']
            or now.get('story_digest') != current['story_digest'] or now['status'] != 'ready_for_voice'):
        raise ValueError('Reviewed inputs changed while rendering; do not present this take as current')
    cut = json.loads((out / 'cut.json').read_text())
    if cut.get('failed') or cut.get('cut_transcript_match', 0) < 0.85:
        raise ValueError('Generated preview did not pass its transcript/tail checks')
    audio = {k: relative(out / (f"{plan.parent.name}_voice_cut.{k}" if k != 'report' else 'report.md'))
             for k in ('mp3', 'wav', 'report')}
    hashes = {k: digest(local(folder(args.slug), p).read_bytes()) for k, p in audio.items()}
    record = {**audio, 'audio_sha256': hashes, 'script_sha256': current['script_sha256'],
              'story_digest': current['story_digest'], 'transcript_verified': True,
              'voice_attempt': current['voice_attempt'], 'duration_s': cut['cut_s'], 'human_listened': False}
    (folder(args.slug) / 'voice-review.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(status(args.slug)))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f'Voice preview blocked: {exc}', file=sys.stderr)
        sys.exit(2)
