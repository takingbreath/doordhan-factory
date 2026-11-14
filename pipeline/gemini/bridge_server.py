#!/usr/bin/env python3
"""Page-to-disk bridge for Claude's built-in browser: saves a file that a web page holds,
with NO download (so no Mac Save panel). Tested 2026-10-16 (Gemini video, ChatGPT picture).

Why: every download in the built-in browser opens a macOS Save panel (the app never sets a save
path). When the browser pane is hidden, that panel is off-screen: nobody sees it and the run
waits forever (2026-10-15/16: up to 10 panels were left waiting). curl works only for addresses
that need no login (Gemini pictures: fetch_full.sh). Everything else uses this bridge.

How: a receiver tab on 127.0.0.1 (this server) and the source tab (Gemini, ChatGPT, ...) open a
WebRTC data channel. The source page reads the file with its own login and sends it; the receiver
page posts it to this server, which writes it into OUT_DIR. The 1 KB offer and answer travel
through this server (bridge.sh relays them with curl), so no tool has to act on the receiver tab.

The other direction (bridge_get.js, 2026-10-28): the page asks for a file that is in OUT_DIR and
receives it over the same channel, for example to paste a reference picture into Gemini when the
pane is hidden and the Drive picker cannot be seen.

Usage: bridge_server.py OUT_DIR [--port 8761] [--idle 900]
Prints one JSON line {"port", "token", "out", "receiver"}, then one JSON line per saved file.
Stops by itself after --idle seconds without a request. Binds 127.0.0.1 only; every path needs
the random token; files go only into OUT_DIR (base name only, never overwritten).
"""
import argparse, json, os, re, secrets, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

MAX_BYTES = 600 * 1024 * 1024

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("--port", type=int, default=8761)
ap.add_argument("--idle", type=int, default=900)
a = ap.parse_args()
OUT = os.path.realpath(os.path.expanduser(a.out))
os.makedirs(OUT, exist_ok=True)
TOKEN = secrets.token_urlsafe(18)
last = [time.time()]
box = {"offer": None, "answer": None}
cond = threading.Condition()

RECEIVER = r"""<!doctype html><meta charset="utf-8"><title>Manjulika bridge</title>
<body style="font:14px system-ui;margin:24px;background:#fff;color:#222">
<p>Manjulika file bridge (receiver). Leave this tab open while a run saves files.</p><pre id="s"></pre>
<script>
const T = %s, s = document.getElementById('s');
const say = t => { s.textContent = (new Date().toTimeString().slice(0, 8) + ' ' + t + '\n' + s.textContent).slice(0, 4000); };
async function waitOffer() {
  for (;;) {
    try {
      const r = await fetch('/offer/' + T + '?wait=25', {cache: 'no-store'});
      if (r.status === 200) return await r.text();
    } catch (e) { await new Promise(r => setTimeout(r, 1000)); }
  }
}
// The offer and answer travel as one short line "m1|o|ufrag|pwd|fingerprint|setup|host,port;..."
// (about 200 characters, easy to copy without a mistake); these two functions convert it.
function unpack(line) {
  const [, ty, uf, pw, fp, setup, cs] = line.trim().split('|');
  let sdp = 'v=0\r\no=- 1 2 IN IP4 127.0.0.1\r\ns=-\r\nt=0 0\r\na=group:BUNDLE 0\r\na=msid-semantic: WMS\r\n' +
    'm=application 9 UDP/DTLS/SCTP webrtc-datachannel\r\nc=IN IP4 0.0.0.0\r\na=ice-ufrag:' + uf + '\r\na=ice-pwd:' + pw +
    '\r\na=fingerprint:sha-256 ' + fp.match(/../g).join(':').toUpperCase() + '\r\na=setup:' + setup +
    '\r\na=mid:0\r\na=sctp-port:5000\r\na=max-message-size:262144\r\n';
  (cs || '').split(';').filter(Boolean).forEach((c, i) => { const [ip, port] = c.split(','); sdp += 'a=candidate:' + (i + 1) + ' 1 udp ' + (2113937151 - i) + ' ' + ip + ' ' + port + ' typ host generation 0\r\n'; });
  return {type: ty === 'o' ? 'offer' : 'answer', sdp};
}
function pack(d) {
  const s = d.sdp, g = k => (s.match(new RegExp('a=' + k + ':([^\\r\\n]+)')) || [])[1];
  const cands = (s.match(/a=candidate:[^\r\n]+/g) || []).map(c => c.split(' ')).filter(p => p[2].toLowerCase() === 'udp').map(p => p[4] + ',' + p[5]);
  return ['m1', d.type[0], g('ice-ufrag'), g('ice-pwd'), g('fingerprint').split(' ')[1].replace(/:/g, ''), g('setup'), cands.join(';')].join('|');
}
async function serve(offer) {
  const pc = new RTCPeerConnection();
  pc.ondatachannel = e => {
    const ch = e.channel; ch.binaryType = 'arraybuffer';
    let head = null, parts = [], got = 0;
    ch.onmessage = async m => {
      if (typeof m.data === 'string') {
        const msg = JSON.parse(m.data);
        if (msg.op === 'get') {   // the other direction (bridge_get.js): send a file from OUT_DIR to the page
          try {
            const r = await fetch('/get/' + T + '?name=' + encodeURIComponent(msg.name), {cache: 'no-store'});
            if (!r.ok) throw new Error('HTTP ' + r.status + ' for ' + msg.name);
            const blob = await r.blob();
            ch.send(JSON.stringify({op: 'head', id: msg.id, name: msg.name, size: blob.size, type: blob.type}));
            ch.bufferedAmountLowThreshold = 1 << 20;
            for (let o = 0; o < blob.size; o += 65536) {
              if (ch.bufferedAmount > (4 << 20)) await new Promise(r => { ch.onbufferedamountlow = r; });
              ch.send(await blob.slice(o, o + 65536).arrayBuffer());
            }
            ch.send(JSON.stringify({op: 'end', id: msg.id})); say('sent ' + msg.name + ' (' + blob.size + ' bytes)');
          } catch (err) { ch.send(JSON.stringify({op: 'error', id: msg.id, error: String(err)})); say('error ' + err); }
          return;
        }
        if (msg.op === 'head') { head = msg; parts = []; got = 0; say('receiving ' + msg.name + ' (' + msg.size + ' bytes)'); }
        else if (msg.op === 'end') {
          const blob = new Blob(parts, {type: head.type || 'application/octet-stream'}); parts = [];
          let reply;
          try {
            const r = await fetch('/put/' + T + '?name=' + encodeURIComponent(head.name), {method: 'POST', body: blob});
            reply = Object.assign({op: 'saved', id: head.id, ok: r.ok && got === head.size, got}, await r.json());
          } catch (err) { reply = {op: 'saved', id: head.id, ok: false, error: String(err)}; }
          say(JSON.stringify(reply)); ch.send(JSON.stringify(reply));
        }
      } else { parts.push(m.data); got += m.data.byteLength; }
    };
  };
  await pc.setRemoteDescription(unpack(offer));
  await pc.setLocalDescription(await pc.createAnswer());
  await new Promise(r => { if (pc.iceGatheringState === 'complete') return r(); pc.onicegatheringstatechange = () => pc.iceGatheringState === 'complete' && r(); setTimeout(r, 5000); });
  await fetch('/answer/' + T, {method: 'POST', body: pack(pc.localDescription)});
  say('answer sent');
}
(async () => { say('ready'); for (;;) { const o = await waitOffer(); say('offer received'); try { await serve(o); } catch (e) { say('error ' + e); } } })();
</script>"""


def safe_name(name):
    name = os.path.basename(name or "file.bin").strip()
    name = re.sub(r"[^A-Za-z0-9._ -]", "_", name).lstrip(".") or "file.bin"
    base, ext = os.path.splitext(name)
    path, n = os.path.join(OUT, name), 1
    while os.path.exists(path) or os.path.exists(path + ".part"):
        path, n = os.path.join(OUT, f"{base}-{n}{ext}"), n + 1
    return path


class H(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, code, body, ctype="application/json"):
        data = body.encode() if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def body(self, limit):
        size = int(self.headers.get("Content-Length") or 0)
        if size <= 0 or size > limit:
            return None
        return self.rfile.read(size)

    def wait_for(self, key, seconds):
        # Long poll: a fetch that waits is not slowed down in a hidden tab, a timer loop is.
        with cond:
            cond.wait_for(lambda: box[key] is not None, timeout=seconds)
            value, box[key] = box[key], None
        return value

    def do_GET(self):
        last[0] = time.time()
        u = urlparse(self.path)
        q = parse_qs(u.query)
        wait = min(float(q.get("wait", ["0"])[0] or 0), 60)
        if u.path == f"/r/{TOKEN}":
            return self.send(200, RECEIVER % json.dumps(TOKEN), "text/html; charset=utf-8")
        if u.path == f"/get/{TOKEN}":
            # only a file directly inside OUT_DIR, by base name (bridge_get.js sends it to the page)
            name = os.path.basename(q.get("name", [""])[0])
            path = os.path.join(OUT, name)
            if not name or name.startswith(".") or not os.path.isfile(path):
                return self.send(404, '{"error":"no such file in OUT_DIR"}')
            ext = os.path.splitext(name)[1].lower()
            ctype = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp",
                     ".mp4": "video/mp4", ".pdf": "application/pdf"}.get(ext, "application/octet-stream")
            return self.send(200, open(path, "rb").read(), ctype)
        for key in ("offer", "answer"):
            if u.path == f"/{key}/{TOKEN}":
                value = self.wait_for(key, wait)
                return self.send(200, value, "text/plain") if value else self.send(204, b"")
        self.send(404, '{"error":"not found"}')

    def do_POST(self):
        last[0] = time.time()
        u = urlparse(self.path)
        for key in ("offer", "answer"):
            if u.path == f"/{key}/{TOKEN}":
                data = self.body(64 * 1024)
                if data is None:
                    return self.send(400, '{"error":"bad sdp"}')
                with cond:
                    box[key] = data.decode(errors="replace")
                    cond.notify_all()
                return self.send(200, '{"ok":true}')
        if u.path != f"/put/{TOKEN}":
            return self.send(404, '{"error":"not found"}')
        size = int(self.headers.get("Content-Length") or 0)
        if size <= 0 or size > MAX_BYTES:
            return self.send(413, json.dumps({"error": f"bad size {size}"}))
        path = safe_name(parse_qs(u.query).get("name", ["file.bin"])[0])
        tmp, left = path + ".part", size
        with open(tmp, "wb") as f:
            while left:
                chunk = self.rfile.read(min(left, 1 << 20))
                if not chunk:
                    break
                f.write(chunk)
                left -= len(chunk)
        if left:
            os.remove(tmp)
            return self.send(400, json.dumps({"error": "short body"}))
        os.replace(tmp, path)
        last[0] = time.time()
        print(json.dumps({"saved": path, "bytes": size}), flush=True)
        self.send(200, json.dumps({"saved": path, "bytes": size}))


srv = ThreadingHTTPServer(("127.0.0.1", a.port), H)
srv.daemon_threads = True


def idle_stop():
    while time.time() - last[0] < a.idle:
        time.sleep(5)
    srv.shutdown()


threading.Thread(target=idle_stop, daemon=True).start()
print(json.dumps({"port": a.port, "token": TOKEN, "out": OUT,
                  "receiver": f"http://127.0.0.1:{a.port}/r/{TOKEN}"}), flush=True)
srv.serve_forever()
