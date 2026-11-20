// Personal Frame FIX-6: Ask Naya button opens the room.
// ROOT CAUSE (proven live, fix-6 repro6b stack trace + repro6c popstate log):
//   The Hub-bar Ask Naya button calls NayaRouter.navigate('/hub/ask') (line
//   12254). In Firefox, assigning location.hash fires a `popstate` event.
//   The Personal frame's popstate handler (lines 23592-23595) mapped EVERY
//   non-Personal hash to showView('home'), and showView('home') runs the
//   fix-4 F3 yield: with the hash now '#/hub/ask' the room counts as open,
//   so it navigates straight back to '/hub/feed' — 6 ms after the ask click,
//   before any hashchange render runs. The Router '*' fallback (line 17440)
//   NEVER runs in this path: render()'s parametric branch matches hub/:room
//   first, so the eye's byte-level mechanism (fallback eats #/hub/ask) is
//   refuted. The fallback is left untouched.
// FIX: the popstate handler returns early when the current hash names a
//   Hub/note route (hub, smart-notes, notes, note) — those belong to the
//   Router's hashchange render. Personal views (and empty hash) still route
//   through showView, so Back to a Personal view still yields an open room.
// Edit is Buffer-safe (latin1 round-trip, byte-exact) like fix-5.
const { fetchBase } = require('./fetchBase6.js');

const OLD = [
  "  window.addEventListener('popstate', function(e){",
  "    var v=(e.state && e.state.osView) || (location.hash||'').replace('#','');",
  "    showView(VIEWS.indexOf(v)>=0?v:'home', true);",
  "  });",
].join('\n');

const NEW = [
  "  window.addEventListener('popstate', function(e){",
  "    /* FRAME-FIX6 2026-11-19 (F6): a Hub-room hash is NOT a Personal-view popstate.",
  "       Firefox fires popstate when location.hash is assigned, so the Hub-bar",
  "       Ask Naya button's navigate('/hub/ask') used to land here, showView('home')",
  "       ran, and its fix-4 F3 yield forced the room straight back to '/hub/feed'",
  "       (proven by live stack trace + popstate log, fix-6 repro6b/6c — the",
  "       Router '*' fallback at 17440 never runs for hub routes: hub/:room",
  "       matches first, so it was not the eater). Hub/note hashes belong to the",
  "       Router's hashchange render — leave them alone. Personal views (and an",
  "       empty hash) still route here, so Back to a Personal view still yields",
  "       an open room through showView('home'). */",
  "    var _h=(location.hash||'').replace(/^#\\/?/,'').split('?')[0].split('/')[0];",
  "    if (_h==='hub' || _h==='smart-notes' || _h==='notes' || _h==='note') return;",
  "    var v=(e.state && e.state.osView) || (location.hash||'').replace('#','');",
  "    showView(VIEWS.indexOf(v)>=0?v:'home', true);",
  "  });",
].join('\n');

function transform(base) {
  const parts = base.split(OLD);
  if (parts.length !== 2) throw new Error('OLD anchor occurrences: ' + (parts.length - 1) + ' (expected exactly 1)');
  return parts[0] + NEW + parts[1];
}

if (require.main === module) {
  const base = fetchBase();
  const out = transform(base);
  const crypto = require('crypto');
  const bBuf = Buffer.from(base, 'latin1');
  const oBuf = Buffer.from(out, 'latin1');
  console.log(JSON.stringify({
    baseLines: base.split('\n').length,
    outLines: out.split('\n').length,
    baseSize: bBuf.length,
    outSize: oBuf.length,
    delta: oBuf.length - bBuf.length,
    outSha256: crypto.createHash('sha256').update(oBuf).digest('hex'),
    outGitBlobSha1: crypto.createHash('sha1').update(`blob ${oBuf.length}\0`).update(oBuf).digest('hex'),
  }, null, 2));
  // Diff hunk check: common prefix / suffix lines
  const bl = base.split('\n'), ol = out.split('\n');
  let pre = 0; while (pre < bl.length && pre < ol.length && bl[pre] === ol[pre]) pre++;
  let suf = 0; while (suf < bl.length - pre && suf < ol.length - pre && bl[bl.length - 1 - suf] === ol[ol.length - 1 - suf]) suf++;
  console.log(JSON.stringify({ commonPrefixLines: pre, commonSuffixLines: suf, baseChangedLines: bl.length - pre - suf, outChangedLines: ol.length - pre - suf }));
  console.log('--- base changed region ---');
  for (let i = pre; i < bl.length - suf; i++) console.log((i + 1) + ': ' + bl[i]);
  console.log('--- fixed changed region ---');
  for (let i = pre; i < ol.length - suf; i++) console.log((i + 1) + ': ' + ol[i]);
}
module.exports = { transform, fetchBase };
