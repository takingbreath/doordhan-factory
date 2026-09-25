#!/usr/bin/env python3
"""Compare a generated clip's audio with the track we gave it. Wan 2.7 should keep it (>=95%). Low = re-voiced.
Usage: check_match.py CLIP.mp4 TRACK.mp3"""
import sys
from common import envelope
a, b = envelope(sys.argv[1]), envelope(sys.argv[2])
n = min(len(a), len(b))
match = 100.0 * ((a[:n] > -38) == (b[:n] > -38)).mean() if n else 0.0
print(f"{'PASS' if match >= 95 else 'FAIL'}  speech pattern match {match:.0f}%  ({sys.argv[1]} vs {sys.argv[2]})")
