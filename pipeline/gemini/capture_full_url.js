// Run in the Gemini tab with javascript_tool. Returns the full-size URL of the newest picture,
// and keeps the picture itself in the page as window.__fullBlob (for bridge_send.js).
// Optional: set window.__pick = N (0-based) before running to pick another picture.
//
// NO DOWNLOAD (v3, tested 2026-10-16): the click on Gemini's "Download full-sized image" button
// makes the page fetch the picture and hand it to a sandboxed helper frame, which starts a
// download. Every download opens a Mac Save panel; with the browser pane hidden the panel is
// off-screen, nobody can press it, and it leaves a hidden 6-8 MB file in ~/Downloads (v2 of this
// script left one per picture). v3 lets Gemini's address chain run, notes the final picture
// address, and gives the page an error instead of the picture: the helper gets nothing, so no
// download starts. Gemini may show "Something went wrong"; that is expected.
// The URL expires fast (a 1-minute-old URL gave HTTP 403): run fetch_full.sh at once.
window.__full = null; window.__fullBlob = null;
if (!window.__holdHooked) {
  const of = window.fetch;
  window.fetch = async function (...a) {
    const url = String(a[0] && (a[0].url || a[0]));
    const r = await of.apply(this, a);
    if (window.__armed && /^https:\/\/lh3\.google(usercontent)?\.com\/(rd-)?gg(-dl)?\//.test(url)
        && /^image\//.test(r.headers.get('content-type') || '') && /=s0|=d|-d-|\/rd-gg-dl\//.test(url)) {
      window.__armed = false; const b = await r.blob(); window.__fullBlob = b; window.__full = url;
      throw new TypeError('picture kept for the run (no download)');
    }
    return r;
  };
  window.__holdHooked = true;
}
const btns = [...document.querySelectorAll('button')].filter(x => /Download full-sized image/.test(x.getAttribute('aria-label') || ''));
if (!btns.length) throw new Error('no picture with a download button on this page');
window.__armed = true;
btns[window.__pick ?? btns.length - 1].click();
for (let i = 0; i < 80 && !window.__full; i++) await new Promise(r => setTimeout(r, 500));
window.__armed = false;
window.__full ? window.__full : 'none: Gemini did not fetch the picture in 40 s. Wait, then run again.';
