#!/usr/bin/env python3
"""Print where speech starts, ends and pauses in each file (audio or video). Choose cut points from this.
Usage: speech_map.py FILE [FILE ...]"""
import sys, json
from common import speech_map
for f in sys.argv[1:]:
    print(f, json.dumps(speech_map(f)))
