// Bridge step 1 (see SKILL.md "Saving files"). Run in the SOURCE tab (Gemini, ChatGPT, ...) with
// javascript_tool. Returns a short line "m1|o|..." (the WebRTC offer). Give it to: bridge.sh answer 'LINE'
if (window.__mjlPc) { try { window.__mjlPc.close(); } catch (e) {} }
const pc = new RTCPeerConnection(), ch = pc.createDataChannel('mjl');
ch.binaryType = 'arraybuffer'; window.__mjlPc = pc; window.__mjlCh = ch;
await pc.setLocalDescription(await pc.createOffer());
await new Promise(r => { if (pc.iceGatheringState === 'complete') return r(); pc.onicegatheringstatechange = () => pc.iceGatheringState === 'complete' && r(); setTimeout(r, 5000); });
const s = pc.localDescription.sdp, g = k => (s.match(new RegExp('a=' + k + ':([^\\r\\n]+)')) || [])[1];
const cands = (s.match(/a=candidate:[^\r\n]+/g) || []).map(c => c.split(' ')).filter(p => p[2].toLowerCase() === 'udp').map(p => p[4] + ',' + p[5]);
['m1', 'o', g('ice-ufrag'), g('ice-pwd'), g('fingerprint').split(' ')[1].replace(/:/g, ''), g('setup'), cands.join(';')].join('|');
