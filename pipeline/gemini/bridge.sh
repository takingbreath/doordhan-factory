#!/bin/bash
# Page-to-disk bridge helper (see SKILL.md "Saving files"). No download, so no Mac Save panel.
#   bridge.sh start OUT_DIR    start the receiver server; prints the receiver tab address
#   bridge.sh answer 'LINE'    pass the offer line from bridge_offer.js; prints the answer line
#   bridge.sh stop             stop the server (it also stops itself after 15 idle minutes)
set -euo pipefail
STATE="${TMPDIR:-/tmp}/mjl-bridge.json"
DIR="$(cd "$(dirname "$0")" && pwd)"
field() { python3 -I -c "import json,sys; print(json.load(open(sys.argv[1]))[sys.argv[2]])" "$STATE" "$1"; }
case "${1:-}" in
  start)
    OUT="${2:?usage: bridge.sh start OUT_DIR}"
    if [ -f "$STATE" ]; then kill "$(field pid)" 2>/dev/null || true; rm -f "$STATE"; fi
    for PORT in 8761 8762 8763 8764 8765; do
      lsof -nP -iTCP:$PORT -sTCP:LISTEN >/dev/null 2>&1 && continue
      LOG="$(mktemp)"
      nohup python3 -I "$DIR/bridge_server.py" "$OUT" --port $PORT > "$LOG" 2>&1 &
      PID=$!
      for _ in $(seq 1 50); do [ -s "$LOG" ] && break; sleep 0.1; done
      if head -1 "$LOG" | grep -q '"token"'; then
        head -1 "$LOG" | python3 -I -c "import json,sys; d=json.loads(sys.stdin.read()); d['pid']=$PID; d['log']='$LOG'; print(json.dumps(d))" > "$STATE"
        echo "receiver tab address: $(field receiver)"
        echo "files go to: $(field out)"
        exit 0
      fi
      kill $PID 2>/dev/null || true
    done
    echo "bridge: could not start a server on ports 8761-8765" >&2; exit 1 ;;
  answer)
    LINE="${2:?usage: bridge.sh answer 'm1|o|...'}"
    BASE="http://127.0.0.1:$(field port)"; T="$(field token)"
    curl -sf -X POST --data-binary "$LINE" "$BASE/offer/$T" >/dev/null
    ANS="$(curl -sf "$BASE/answer/$T?wait=40" || true)"
    if [ -z "$ANS" ]; then echo "bridge: no answer in 40 s. Is the receiver tab open at $(field receiver) ?" >&2; exit 1; fi
    echo "$ANS" ;;
  stop)
    if [ -f "$STATE" ]; then kill "$(field pid)" 2>/dev/null || true; tail -n +2 "$(field log)" 2>/dev/null || true; rm -f "$STATE"; fi
    echo "bridge stopped" ;;
  *) sed -n '2,6p' "$0"; exit 2 ;;
esac
