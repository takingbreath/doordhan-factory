// Bridge, other direction (see SKILL.md "Putting a file INTO the page"). Run in the SOURCE tab (Gemini, ...) with
// javascript_tool after bridge_offer.js, with this line FIRST in the same text:
//   window.MJL = {answer: 'm1|a|...', get: ['ref.png'], paste: true};
// Each name must be a file directly inside the bridge's OUT_DIR. The page receives it over the data channel and keeps it
// as a File in window.__mjlGot[name]. With paste: true it also dispatches a paste event with all the files on the
// prompt box (Gemini attaches them as if pasted). No file dialog, no Drive picker, works with the pane hidden.
const M = window.MJL, pc = window.__mjlPc, ch = window.__mjlCh;
if (!M || !pc || !ch) throw new Error('run bridge_offer.js first, then set window.MJL');
const [, , uf, pw, fp, setup, cs] = M.answer.trim().split('|');
let sdp = 'v=0\r\no=- 1 2 IN IP4 127.0.0.1\r\ns=-\r\nt=0 0\r\na=group:BUNDLE 0\r\na=msid-semantic: WMS\r\n' +
  'm=application 9 UDP/DTLS/SCTP webrtc-datachannel\r\nc=IN IP4 0.0.0.0\r\na=ice-ufrag:' + uf + '\r\na=ice-pwd:' + pw +
  '\r\na=fingerprint:sha-256 ' + fp.match(/../g).join(':').toUpperCase() + '\r\na=setup:' + setup +
  '\r\na=mid:0\r\na=sctp-port:5000\r\na=max-message-size:262144\r\n';
(cs || '').split(';').filter(Boolean).forEach((c, i) => { const [ip, port] = c.split(','); sdp += 'a=candidate:' + (i + 1) + ' 1 udp ' + (2113937151 - i) + ' ' + ip + ' ' + port + ' typ host generation 0\r\n'; });
if (pc.signalingState === 'have-local-offer') await pc.setRemoteDescription({type: 'answer', sdp});
await new Promise((r, j) => { if (ch.readyState === 'open') return r(); ch.onopen = r; setTimeout(() => j(new Error('channel did not open: ' + pc.connectionState + '. Start again from bridge_offer.js')), 20000); });
const got = window.__mjlGot = window.__mjlGot || {}, out = [];
for (const name of M.get || []) {
  const id = Math.random().toString(36).slice(2);
  const file = await new Promise((res, rej) => {
    let head = null, parts = [], n = 0;
    const t = setTimeout(() => rej(new Error('no file from the receiver tab in 60 s')), 60000);
    ch.onmessage = m => {
      if (typeof m.data !== 'string') { parts.push(m.data); n += m.data.byteLength; return; }
      const d = JSON.parse(m.data);
      if (d.id !== id) return;
      if (d.op === 'error') { clearTimeout(t); rej(new Error(d.error)); }
      else if (d.op === 'head') { head = d; parts = []; n = 0; }
      else if (d.op === 'end') { clearTimeout(t); if (n !== head.size) rej(new Error('got ' + n + ' of ' + head.size + ' bytes')); else res(new File(parts, name, {type: head.type})); }
    };
    ch.send(JSON.stringify({op: 'get', id, name}));
  }).catch(e => ({error: String(e.message || e)}));
  if (file instanceof File) { got[name] = file; out.push({name, ok: true, bytes: file.size, type: file.type}); }
  else out.push({name, ok: false, error: file.error});
}
if (M.paste) {
  const files = (M.get || []).map(n => got[n]).filter(Boolean);
  const box = document.querySelector('rich-textarea .ql-editor, div[contenteditable="true"], textarea');
  if (!box) out.push({paste: false, error: 'no prompt box found'});
  else if (files.length) {
    const dt = new DataTransfer(); files.forEach(f => dt.items.add(f));
    box.focus();
    box.dispatchEvent(new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true}));
    out.push({paste: true, files: files.length});
  }
}
out;
