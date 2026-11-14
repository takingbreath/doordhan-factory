// Bridge step 3 (see SKILL.md "Saving files"). Run in the SOURCE tab with javascript_tool, with this
// line FIRST in the same text (fill in the answer from bridge.sh and the files to send):
//   window.MJL = {answer: 'm1|a|...', items: [{name: 'clip.mp4', css: 'video'}]};
// Item kinds: {name, url} reads that address with the page's own login;
//   {name, css, pick} reads the currentSrc/src of the element (pick: index, default -1 = last);
//   {name, blobVar} sends a Blob the page already holds, e.g. '__fullBlob' from capture_full_url.js.
// It never clicks a download button, so no Save panel opens. Returns one result per item.
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
const replies = {};
ch.onmessage = m => { try { const d = JSON.parse(m.data); if (d.op === 'saved') replies[d.id] = d; } catch (e) {} };
ch.bufferedAmountLowThreshold = 1 << 20;
const out = [];
for (const it of M.items) {
  const id = Math.random().toString(36).slice(2);
  try {
    let url = it.url, blob = it.blobVar ? window[it.blobVar] : null;
    if (it.blobVar && !(blob instanceof Blob)) throw new Error('window.' + it.blobVar + ' holds no file');
    if (!blob) {
      if (!url && it.css) { const els = [...document.querySelectorAll(it.css)]; const el = els.at(it.pick ?? -1); if (!el) throw new Error('no element ' + it.css); url = el.currentSrc || el.src; }
      const r = await fetch(url, {credentials: 'include'});
      if (!r.ok) throw new Error('HTTP ' + r.status);
      blob = await r.blob();
    }
    ch.send(JSON.stringify({op: 'head', id, name: it.name, size: blob.size, type: blob.type}));
    for (let o = 0; o < blob.size; o += 65536) {
      if (ch.bufferedAmount > (4 << 20)) await new Promise(r => { ch.onbufferedamountlow = r; });
      ch.send(await blob.slice(o, o + 65536).arrayBuffer());
    }
    ch.send(JSON.stringify({op: 'end', id}));
    for (let i = 0; i < 240 && !replies[id]; i++) await new Promise(r => setTimeout(r, 250));
    out.push(Object.assign({name: it.name, sent: blob.size, type: blob.type}, replies[id] || {ok: false, error: 'no reply from the receiver tab'}));
  } catch (e) { out.push({name: it.name, ok: false, error: String(e.message || e)}); }
}
out;
