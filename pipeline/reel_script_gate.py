#!/usr/bin/env python3
"""Local checkpoints for /reel-script. No model, network, voice generation or production approval.

The coordinating chat records approvals only after the human explicitly gives them:
  reel_script_gate.py approve-story SLUG --by Akhilesh --quote '...' --expected-digest SHA
  reel_script_gate.py approve-voice SLUG --by Akhilesh --quote '...' --expected-digest SHA
`status SLUG` is read-only. Approval binds the actual reviewed files; edits invalidate it.
These records preserve human decisions; a name/quote is not independent identity authentication.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import sys

ROOT = Path(os.environ.get('DOORDHAN_ROOT') or Path(__file__).resolve().parents[1]).resolve()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True).encode()


def folder(slug):
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]*', slug):
        raise ValueError('Invalid run slug')
    path = (ROOT / 'work' / slug / 'loop').resolve()
    if not path.is_relative_to(ROOT / 'work'):
        raise ValueError('Run folder escapes work/')
    return path


def local(base, name):
    path = (ROOT / name).resolve()
    if not path.is_relative_to(base) or not path.is_file():
        raise ValueError(f'Missing or out-of-run file: {name}')
    return path


def relative(path):
    return path.relative_to(ROOT).as_posix()


def load(slug):
    base = folder(slug)
    state = json.loads((base / 'state.json').read_text())
    if state['brief']['slug'] != slug:
        raise ValueError('State slug does not match the requested run')
    brief = state['brief']
    if (not isinstance(brief.get('topic'), str) or not brief['topic'].strip()
            or not isinstance(brief.get('format'), str)
            or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', brief['format'])
            or type(brief.get('writers')) is not int or not 1 <= brief['writers'] <= 5
            or not isinstance(brief.get('cast'), list) or not brief['cast']
            or any(not isinstance(n, str) or not re.fullmatch(r'[a-z0-9][a-z0-9_-]*', n)
                   for n in brief['cast'])):
        raise ValueError('Invalid resolved brief; check topic, format, cast and writers (1–5)')
    return base, state


def save(base, state):
    path = base / 'state.json'
    temp = base / 'state.json.tmp'
    temp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
    temp.replace(path)


def latest_scripts(base):
    found = {}
    for path in base.glob('w*-v*.md'):
        match = re.fullmatch(r'w(\d+)-v(\d+)\.md', path.name)
        if match and path.stat().st_size:
            if not path.resolve().is_relative_to(base):
                raise ValueError('Candidate script escapes the run folder')
            writer, version = map(int, match.groups())
            if writer not in found or version > found[writer][0]:
                found[writer] = (version, path)
    return {str(w): {'path': relative(p), 'sha256': digest(p.read_bytes()), 'version': v}
            for w, (v, p) in sorted(found.items())}


def status(slug):
    base, state = load(slug)
    brief = state['brief']
    out = {'slug': slug, 'brief': brief, 'dir': relative(base), 'status': 'incomplete',
           'candidates': latest_scripts(base)}
    research, story = base / 's1-research.md', base / 's2-story.md'
    if not research.is_file() or not story.is_file() or not research.stat().st_size or not story.stat().st_size:
        return out
    material = {'brief': brief, 'input': state.get('input', ''),
                'research': digest(research.read_bytes()), 'story': digest(story.read_bytes())}
    if brief.get('research'):
        supplied = Path(brief['research'])
        supplied = supplied if supplied.is_absolute() else ROOT / supplied
        if not supplied.is_file():
            return {**out, 'status': 'blocked', 'reason': 'Supplied research file is missing'}
        material['supplied_research'] = digest(supplied.read_bytes())
    bundle = digest(encoded(material))
    out.update(story=relative(story), research=relative(research), story_digest=bundle)
    if (state.get('story_approval') or {}).get('digest') != bundle:
        return {**out, 'status': 'awaiting_story_approval'}
    if not out['candidates']:
        return {**out, 'status': 'ready_to_write'}
    review_path = base / 'review.json'
    if not review_path.is_file():
        return {**out, 'status': 'needs_editor'}
    review = json.loads(review_path.read_text())
    script = local(base, review.get('script', ''))
    script_sha = digest(script.read_bytes())
    newest = {x['path'] for x in out['candidates'].values()}
    out.update(script=relative(script), script_sha256=script_sha, review=relative(review_path))
    if (relative(script) not in newest or review.get('script_sha256') != script_sha
            or review.get('story_digest') != bundle):
        return {**out, 'status': 'needs_editor'}
    verdict = review.get('verdict')
    if verdict != 'pass':
        return {**out, 'status': {'revise': 'needs_revision', 'story_changed': 'needs_story_revision',
                                 'blocked': 'blocked'}.get(verdict, 'blocked'),
                'reason': review.get('summary', 'Editorial/factual review did not pass')}
    claims = review.get('claims')
    if (not isinstance(claims, list) or review.get('issues') != []
            or any(not isinstance(c, dict) or not c.get('claim') or not c.get('source')
                   or not c.get('checked_on') or c.get('status') not in ('verified', 'qualified')
                   or (c.get('status') == 'qualified' and not c.get('qualification')) for c in claims)):
        return {**out, 'status': 'blocked', 'reason': 'Final claims trace is incomplete or has unresolved issues'}
    feedback = state.get('voice_feedback') or {}
    attempt = (feedback.get('attempt', 0) if feedback.get('script_sha256') == script_sha
               and feedback.get('story_digest') == bundle else 0)
    voice_dir = base / 'audio' / (script.stem + (f'-take{attempt + 1}' if attempt else ''))
    out.update(voice_dir=relative(voice_dir), voice_attempt=attempt,
               voice_feedback=feedback.get('quote', '') if attempt else '')
    voice_path = base / 'voice-review.json'
    if not voice_path.is_file():
        return {**out, 'status': 'ready_for_voice'}
    voice = json.loads(voice_path.read_text())
    if (voice.get('script_sha256') != script_sha or voice.get('story_digest') != bundle
            or voice.get('voice_attempt', 0) != attempt):
        return {**out, 'status': 'ready_for_voice'}
    if voice.get('transcript_verified') is not True:
        return {**out, 'status': 'blocked', 'reason': 'Voice transcript has not passed'}
    audio = {k: local(base, voice.get(k, '')) for k in ('mp3', 'wav', 'report')}
    voice_digest = digest(encoded({'script': script_sha, 'story': bundle, 'attempt': attempt,
                                   **{k: digest(p.read_bytes()) for k, p in audio.items()}}))
    # Binding generated bytes also detects replacing a take after its transcript check.
    if voice.get('audio_sha256') != {k: digest(p.read_bytes()) for k, p in audio.items()}:
        return {**out, 'status': 'ready_for_voice'}
    approved = (state.get('voice_approval') or {}).get('digest') == voice_digest
    return {**out, 'status': 'voice_approved' if approved else 'awaiting_voice_review',
            'voice_digest': voice_digest, 'audio': {k: relative(p) for k, p in audio.items()}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init')
    init.add_argument('--payload', required=True)
    sub.add_parser('status').add_argument('slug')
    for command in ('approve-story', 'approve-voice', 'revise-voice'):
        approve = sub.add_parser(command)
        approve.add_argument('slug')
        approve.add_argument('--by', required=True, choices=('Akhilesh', 'Naveen'))
        approve.add_argument('--quote', required=True)
        approve.add_argument('--expected-digest', required=True)
    args = parser.parse_args()
    if args.command == 'init':
        state = json.loads(args.payload)
        brief = state['brief']
        base = folder(brief['slug'])
        if (base / 'state.json').exists():
            raise ValueError('Run already exists; continue it instead of overwriting it')
        base.mkdir(parents=True, exist_ok=True)
        if any(base.glob('w*-v*.md')) or (base / 's2-story.md').exists():
            raise ValueError('Existing creative work must be continued, not overwritten')
        save(base, {'brief': brief, 'input': state.get('input', ''), 'history': []})
        if not (base / 'brief.md').exists():
            (base / 'brief.md').write_text('# Human-supplied structured brief\n\n'
                                          + json.dumps(brief, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps({**status(brief['slug']), 'initialized': True}, ensure_ascii=False))
        return
    current = status(args.slug)
    if args.command == 'status':
        print(json.dumps(current, ensure_ascii=False))
        return
    key = 'story' if args.command == 'approve-story' else 'voice'
    eligible = (('awaiting_story_approval',) if key == 'story' else
                ('awaiting_voice_review', 'voice_approved') if args.command == 'revise-voice'
                else ('awaiting_voice_review',))
    if current['status'] not in eligible:
        raise ValueError(f"Cannot approve {key} at {current['status']}")
    if not args.quote.strip() or args.expected_digest != current[f'{key}_digest']:
        raise ValueError('Missing explicit human quote or the reviewed version has changed')
    base, state = load(args.slug)
    record = {'by': args.by, 'quote': args.quote.strip(), 'digest': args.expected_digest,
              'at': dt.datetime.now(dt.timezone.utc).isoformat()}
    if args.command == 'revise-voice':
        record.update(attempt=current['voice_attempt'] + 1, script_sha256=current['script_sha256'],
                      story_digest=current['story_digest'])
        state.setdefault('history', []).append({'gate': 'voice_feedback', **record})
        state['voice_feedback'] = record
    else:
        state.setdefault('history', []).append({'gate': key, **record})
        state[f'{key}_approval'] = record
    save(base, state)
    print(json.dumps(status(args.slug), ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError, TypeError, AttributeError) as exc:
        print(json.dumps({'status': 'blocked', 'reason': str(exc)}))
        sys.exit(1)
