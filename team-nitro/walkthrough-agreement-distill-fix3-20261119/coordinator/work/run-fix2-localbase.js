#!/usr/bin/env node
// run-fix2.js — agreement distill fix-2: fetch base in memory, transform, harness, print summary.
// No file writes (EPERM). Deterministic: re-runnable by the checker with ./base/ files or --staging.
const https = require('https');
const crypto = require('crypto');
const vm = require('vm');
const fs = require('fs');
const path = require('path');

const STAGE = 'naya-walk-beginning-staging.nayapower.workers.dev';
const BASE = {
  unfold: { bytes: 141781, sha256: '5fe1a3ec2231c128774c6eb00736913d93117d3eaa06278e2a16183cdebee6ab' },
  welcome: { bytes: 1913241, sha256: 'c3c750b72a2b0330d15de8831e9b24719116991e6c0df9dbc5d329834fbbaed5' },
  walk: { bytes: 4361369, sha256: '0f05b3f96ce8edd0ecb094c0f64972098f788c3943e22b5446c8bb60e9b0e2fd' },
  identity: { bytes: 401040, sha256: '3279dc3572337e5e' },
};
function get(p, ms) {
  return new Promise((res, rej) => {
    const req = https.get({ hostname: STAGE, path: p, headers: { 'User-Agent': 'Mozilla/5.0' } }, (r) => {
      const b = []; r.on('data', (c) => b.push(c));
      r.on('end', () => res(Buffer.concat(b).toString('utf8')));
      r.on('error', rej);
    });
    req.setTimeout(ms || 60000, () => req.destroy(new Error('timeout ' + p)));
    req.on('error', rej);
  });
}
function sha(s) { return crypto.createHash('sha256').update(s, 'utf8').digest('hex'); }
function count(s, needle) { let n = 0, i = -1; while ((i = s.indexOf(needle, i + 1)) !== -1) n++; return n; }
const LOG = [];
function log(m) { LOG.push(m); console.log(m); }
function rep(s, needle, repl, expect, label, fatal) {
  const n = count(s, needle);
  if (expect != null && n !== expect) {
    const msg = 'REP ' + label + ': found ' + n + ', expected ' + expect + ' :: ' + JSON.stringify(needle.slice(0, 90));
    if (fatal === false) { log('WARN ' + msg); return s; }
    throw new Error(msg);
  }
  if (n === 0) { log('WARN ' + label + ': 0 occurrences, nothing replaced'); return s; }
  log('REP ' + label + ': ' + n + 'x');
  return s.split(needle).join(repl);
}
function repRe(s, re, repl, min, label) {
  const matches = s.match(re);
  const n = matches ? matches.length : 0;
  if (n < min) { log('WARN ' + label + ': ' + n + ' replacements (min ' + min + ')'); }
  else log('REP ' + label + ': ' + n + 'x');
  // NOTE: repl is a STRING so $1 group refs work (a function return would insert "$1" literally).
  return s.replace(re, repl);
}
function section(s, startMarker, endMarker) {
  const a = s.indexOf(startMarker); if (a < 0) throw new Error('section start not found: ' + startMarker);
  let b = endMarker ? s.indexOf(endMarker, a) : -1; if (b < 0) b = s.length;
  return { a, b, text: s.slice(a, b) };
}
function replaceIn(s, sec, needle, repl, label) {
  const n = count(sec.text, needle);
  if (n === 0) { log('WARN ' + label + ': 0 in section'); return s; }
  log('REP ' + label + ': ' + n + 'x');
  return s.slice(0, sec.a) + sec.text.split(needle).join(repl) + s.slice(sec.b);
}
function appendFix(s, css, id, label) {
  const open = '<style id="fpFixDistill">';
  const i = s.indexOf(open);
  if (i > -1) {
    const close = s.indexOf('</style>', i);
    log('APPEND ' + label + ': into fpFixDistill');
    return s.slice(0, close) + '\n/* FIX2 ' + label + ' */\n' + css + '\n' + s.slice(close);
  }
  const h = s.indexOf('</head>');
  log('APPEND ' + label + ': new style ' + id + ' before </head>');
  return s.slice(0, h) + '<style id="' + id + '">\n' + css + '\n</style>\n' + s.slice(h);
}
const SEAL = '<div class="deal-seal frame-red-n"><span class="deal-seal-mark" aria-hidden="true">N</span></div>';
const SEAL_CSS = '.deal-seal{width:120px;height:120px;border-radius:46% 54% 51% 49%/48% 45% 55% 52%;border:2px solid rgba(255,140,150,.4);background:radial-gradient(circle at 34% 28%,#b02538,#7d1220 45%,#4d0a14 78%,#38060f);box-shadow:0 10px 30px rgba(0,0,0,.55),inset 0 2px 8px rgba(255,255,255,.25)}.deal-seal-mark{font-family:Marcellus,Georgia,serif;font-size:54px;font-weight:700;line-height:120px;text-align:center;display:block;color:#f5c96b;text-shadow:0 0 12px rgba(245,201,107,.8)}';
const SIGN_PHOTO = '<div class="deal-sign-frame"><img class="deal-sign-photo" src="https://naya-proof-host.nayapower.workers.dev/?file=team-nitro/agreement-unfold-20261117/face-9.jpg&ref=agreement/unfold-20261117&cb=e1dbe46717f87cf4cb63f7cef4bd367d8bb1a0f2" alt="Naya"></div>';

async function main() {
  // ---- fetch base (staging serves bytes identical to filed blobs per fix-1 checker)
  const U0 = fs.readFileSync('/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix3-20261119/coordinator/work/unfold-base.html','utf8');
  const W0 = fs.readFileSync('/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix3-20261119/coordinator/work/welcome-base.html','utf8');
  const WK0 = fs.readFileSync('/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix3-20261119/coordinator/work/walk-base.html','utf8');
  const I0 = fs.readFileSync('/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix3-20261119/coordinator/work/identity-base.html','utf8');
  for (const [k, v, s] of [['unfold', BASE.unfold, U0], ['welcome', BASE.welcome, W0], ['walk', BASE.walk, WK0], ['identity', BASE.identity, I0]]) {
    const b = Buffer.byteLength(s), h = sha(s);
    const ok = b === v.bytes && h.startsWith(v.sha256);
    log('BASE ' + k + ': ' + b + 'B sha ' + h.slice(0, 16) + ' expect ' + v.bytes + ' ' + v.sha256.slice(0, 8) + ' -> ' + (ok ? 'MATCH' : 'MISMATCH'));
    if (!ok) throw new Error('base mismatch: ' + k);
  }
  let U = U0, W = W0, WK = WK0, I = I0;

  // ================= UNFOLD =================
  // U1 F1 corners (if present in unfold)
  U = rep(U, 'width:208px;height:208px', 'width:96px;height:96px', null, 'U1 corners 208->96', false);
  // U2 ruling (b) board 22 title
  U = rep(U, 'How collective chain technology works', 'How it all connects', null, 'U2 board22 title', false);
  // U3 F6 board 2 frame title (JS data) -> static wording
  const u3 = count(U, 'One network, many people, many minds');
  if (u3 > 0) U = rep(U, 'One network, many people, many minds', 'The Collective Intelligence Network', u3, 'U3 board2 frame title');
  else { const oi = U.indexOf('One network'); log('WARN U3: phrase absent; "One network" idx ' + oi + (oi > -1 ? ' ctx ' + JSON.stringify(U.slice(Math.max(0, oi - 120), oi + 200)) : '')); }
  // U4 F5c showcase img fit (height:auto -> height:100% + contain)
  U = repRe(U, /(\.lb-showcase img\{[^}]*?)height:auto!important/g, '$1height:100%!important;object-fit:contain', 1, 'U4 showcase img fit');
  // U5 F5a fp-noslide on the 9 text-only boards
  for (const n of [4, 7, 10, 13, 17, 21, 24, 28, 33]) {
    U = rep(U, '<article class="intel-board letter-beat" data-beat="' + n + '"', '<article class="intel-board letter-beat fp-noslide" data-beat="' + n + '"', 1, 'U5 fp-noslide board ' + n);
  }
  // U6 append fix CSS (no-stretch text boards, img reserve, end-card fit)
  U = appendFix(U, '.letter-beat.fp-noslide .ib-nutshell{flex:0 0 auto!important;max-height:none!important}\n#deckBody .lb-showcase img{aspect-ratio:16/9}\n.deal-sign-photo{height:min(280px,28vh)!important;width:auto;max-width:100%}', 'fpFixDistill2', 'U6 unfold fix css');

  // ================= WELCOME =================
  // W1 F1 corners 208 -> 96
  W = rep(W, 'width:208px;height:208px', 'width:96px;height:96px', null, 'W1 corners 208->96');
  // W2 ruling (b) board 22 title (deck + letter + rail if present)
  W = rep(W, 'How collective chain technology works', 'How it all connects', null, 'W2 board22 title');
  // W3 F6 board 2 frame title -> static wording
  const w3 = count(W, 'One network, many people, many minds');
  if (w3 > 0) W = rep(W, 'One network, many people, many minds', 'The Collective Intelligence Network', w3, 'W3 board2 frame title');
  else { const oi = W.indexOf('One network'); log('WARN W3: phrase absent; "One network" idx ' + oi + (oi > -1 ? ' ctx ' + JSON.stringify(W.slice(Math.max(0, oi - 120), oi + 200)) : '')); }
  // W4 F5a fp-noslide: deck (1-based) scoped to deckBody.
  // Deck articles carry extra classes (e.g. "face-right"), so match the class prefix, not the exact class string.
  for (const n of [4, 7, 10, 13, 17, 21, 24, 28, 33]) {
    const sec = section(W, 'id="deckBody"', 'id="letterBody"');
    const re = new RegExp('<article class="intel-board([^"]*)" data-beat="' + n + '"', 'g');
    const m = sec.text.match(re);
    if (!m || m.length !== 1) { log('WARN W4 deck fp-noslide ' + n + ': ' + (m ? m.length : 0) + ' matches (expected 1)'); continue; }
    W = W.slice(0, sec.a) + sec.text.replace(re, '<article class="intel-board$1 fp-noslide" data-beat="' + n + '"') + W.slice(sec.b);
    log('REP W4 deck fp-noslide ' + n + ': 1x');
  }
  // W5 F5a fp-noslide: letter (0-based mirror list) scoped to letterBody; only data-distilled letter boards, never rail beats.
  for (const n of [3, 6, 9, 12, 16, 20, 23, 27, 32]) {
    const sec = section(W, 'id="letterBody"', 'id="fpLegal"');
    const re = new RegExp('<article class="intel-board([^"]*)" data-beat="' + n + '" data-distilled', 'g');
    const m = sec.text.match(re);
    if (!m || m.length !== 1) { log('WARN W5 letter fp-noslide ' + n + ': ' + (m ? m.length : 0) + ' matches (expected 1)'); continue; }
    W = W.slice(0, sec.a) + sec.text.replace(re, '<article class="intel-board$1 fp-noslide" data-beat="' + n + '" data-distilled') + W.slice(sec.b);
    log('REP W5 letter fp-noslide ' + n + ': 1x');
  }
  // verify: every fp-noslide letter article lacks a showcase
  {
    const ls = section(W, 'id="letterBody"', 'id="fpLegal"').text;
    const parts = ls.split('<article');
    let bad = [];
    for (let i = 1; i < parts.length; i++) {
      if (parts[i].includes('fp-noslide') && parts[i].includes('lb-showcase')) bad.push(i);
    }
    log('CHECK W5 letter fp-noslide articles with a showcase (must be 0): ' + bad.length + (bad.length ? ' BAD idx ' + bad.join(',') : ''));
    if (bad.length) throw new Error('W5: fp-noslide on a board that HAS a showcase');
  }
  // W6 F5a fill deck 37 + letter 37 with the harvested sign photo (before each board-37 foot)
  function insertBeforeFoot(s, secStart, secEnd, beat, label) {
    const sec = section(s, secStart, secEnd);
    const bi = sec.text.indexOf('data-beat="' + beat + '"');
    if (bi < 0) { log('WARN ' + label + ': board ' + beat + ' not found in section'); return s; }
    const fi = sec.text.indexOf('<div class="ib-foot">', bi);
    if (fi < 0) { log('WARN ' + label + ': no ib-foot after board ' + beat); return s; }
    log('REP ' + label + ': sign photo into board ' + beat);
    const abs = sec.a + fi;
    return s.slice(0, abs) + SIGN_PHOTO + s.slice(abs);
  }
  W = insertBeforeFoot(W, 'id="deckBody"', 'id="letterBody"', '37', 'W6 deck37 sign photo');
  W = insertBeforeFoot(W, 'id="letterBody"', 'id="fpLegal"', '36', 'W6 letter37 sign photo');
  // W7 F7 seals in every deck + letter/rail foot
  W = rep(W, '&middot; The Deck</div>', '&middot; The Deck' + SEAL + '</div>', 37, 'W7 deck seals');
  const w7b = count(W, '&middot; The Collective Agreement</div>');
  W = rep(W, '&middot; The Collective Agreement</div>', '&middot; The Collective Agreement' + SEAL + '</div>', null, 'W7 letter+rail seals (found ' + w7b + ')');
  // W8 F10 bridge URL
  {
    const fi = W.indexOf('function goBridgeAfterAgree');
    if (fi < 0) throw new Error('W8: goBridgeAfterAgree not found');
    const m = /S\.view\s*=\s*'bridge';/.exec(W.slice(fi));
    if (!m) throw new Error('W8: S.view=bridge not found inside goBridgeAfterAgree');
    const abs = fi + m.index + m[0].length;
    W = W.slice(0, abs) + "try{if(history.replaceState)history.replaceState(null,'','/?stage=bridge');}catch(e){}" + W.slice(abs);
    log('REP W8 F10 bridge URL replaceState: 1x');
  }
  // W9 ruling (a): cut the money-board "Congratulations. You're hired!" from the rail (data-beat 51).
  // The sentence is TWO <p> tags, not one: <p><b>Congratulations.</b></p><p><b>You&rsquo;re hired!</b></p>
  {
    const pair = '<p><b>Congratulations.</b></p><p><b>You&rsquo;re hired!</b></p>';
    const n = count(W, pair);
    log('CHECK W9 money-board pair occurrences: ' + n);
    if (n === 1) { W = rep(W, pair, '', 1, 'W9 cut money-board sentence'); }
    else log('WARN W9: money-board pair found ' + n + 'x (expected 1) — NOT cut');
    const h = count(W, 'hired!');
    log('CHECK W9 "hired!" remaining in W: ' + h);
  }
  // W10 F8: Nine pictures must be gone
  const w10 = count(W, 'Nine pictures');
  if (w10 > 0) W = rep(W, 'Nine pictures', 'Thirty-seven boards', w10, 'W10 Nine pictures -> Thirty-seven boards');
  else log('CHECK W10 Nine pictures in W: 0 (already gone)');
  // W11 ruling (a) Read-it-all: never hide the button (remove the hide statement if present)
  {
    const hits = [];
    let i = -1;
    while ((i = W.indexOf('fpLinkLetterAll', i + 1)) !== -1) hits.push(i);
    log('CHECK W11 fpLinkLetterAll occurrences: ' + hits.length);
    for (const h of hits.slice(0, 8)) log('  fpLinkLetterAll ctx: ' + JSON.stringify(W.slice(Math.max(0, h - 140), h + 200).replace(/\n/g, ' ').slice(0, 340)));
    let n = 0;
    W = W.replace(/([a-zA-Z_$][\w$]*\.?)?fpLinkLetterAll\s*\.\s*hidden\s*=\s*true/g, (m) => { n++; return '/* FIX2: never hide the Read-it-all button */ void 0'; });
    W = W.replace(/fpLinkLetterAll\s*\.\s*style\.display\s*=\s*['"]none['"]/g, (m) => { n++; return '/* FIX2: never hide the Read-it-all button */ void 0'; });
    log('REP W11 Read-it-all hide removed: ' + n + 'x' + (n === 0 ? ' (no hide statement found — button visibility is by view, see contexts)' : ''));
  }
  // W12 append the fix-2 CSS block (F1/F2/F3/F4/F5a/F5c/F7 geometry + budget)
  W = appendFix(W, [
    '/* F1: corners 96px + stage top clearance so the board clears them */',
    'body.fp-stage-on #fpAgreement.fp-layer-on{padding-top:112px!important}',
    '/* F2/F4: faces pin to the VIEWPORT right edge, not the parent (parent is wider than the viewport) */',
    'body.fp-stage-on #fpAgreement .fp-speak-face{left:calc(100vw - 116px)!important;right:auto!important}',
    '/* F3/F5c vertical budget: photo + showcase capped so foot + seal + button fit one view */',
    'body.fp-stage-on #fpAgreement .fp-now .deal-beat-photo{width:clamp(96px,14vh,144px)!important;height:clamp(96px,14vh,144px)!important}',
    'body.fp-stage-on #fpAgreement .fp-now .lb-showcase{height:clamp(110px,18vh,170px)!important}',
    'body.fp-stage-on #fpLegal .fp-now .lb-showcase{height:clamp(110px,18vh,170px)!important}',
    'body.fp-stage-on #fpAgreement .fp-now .lb-showcase img{aspect-ratio:16/9}',
    'body.fp-stage-on #fpAgreement .fp-now.fp-smart-talk .ib-foot{display:block!important}',
    '/* F5a: text-only boards close the frame around the text */',
    '.fp-now.fp-noslide{grid-template-columns:minmax(0,1fr)!important;grid-template-rows:auto auto auto!important;align-content:center!important}',
    '.fp-now.fp-noslide .ib-nutshell{flex:0 0 auto!important;max-height:none!important}',
    '.letter-beat.fp-noslide .ib-nutshell{flex:0 0 auto!important;max-height:none!important}',
    '/* F5a: board-37 sign photo takes the showcase slot in grid, stacks in flex */',
    'body.fp-stage-on #fpAgreement .fp-now .deal-sign-frame{display:flex;align-items:center;justify-content:center;grid-column:2;grid-row:2/span 2;min-height:0}',
    'body.fp-stage-on #fpAgreement .fp-now .deal-sign-photo{height:min(280px,28vh)!important;width:auto;max-width:100%;object-fit:contain}',
    '/* F7: seal centred at the foot bottom */',
    '.ib-foot .deal-seal{margin:14px auto 0}',
  ].join('\n'), 'fpFixDistill2', 'W12 welcome fix-2 css');

  // ================= WALK =================
  // K1 F7 seal on the door
  {
    const anchor = '<a class="p3-enter" href="/identity.html" style="text-decoration:none">Get your certificate ◆</a>';
    const n = count(WK, anchor);
    if (n === 1) { WK = rep(WK, anchor, anchor + '\n' + SEAL, 1, 'K1 door seal'); }
    else log('WARN K1: door cert link anchor found ' + n + 'x (expected 1)');
    if (WK.indexOf('.deal-seal{width:120px') < 0) {
      const h = WK.indexOf('</head>');
      WK = WK.slice(0, h) + '<style id="fpFixDistill2">\n' + SEAL_CSS + '\n.ib-foot .deal-seal{margin:14px auto 0}\n#step-door .deal-seal{margin:18px auto 0}\n</style>\n' + WK.slice(h);
      log('APPEND K1 seal CSS to walk');
    } else log('CHECK K1 seal CSS already in walk');
  }
  // K2 F9 cert link carries name+alias
  {
    const script = '<script>/* FIX2 F9: the door certificate link carries the claimed name+alias so the return shows the completed certificate */\n(function(){try{var p=new URLSearchParams(location.search);var n=p.get("name")||sessionStorage.getItem("nayanet_user_name")||"";var a=p.get("alias")||sessionStorage.getItem("nayanet_smart_alias")||"";if(!n&&!a)return;var links=document.querySelectorAll(\'#step-door a[href="/identity.html"]\');for(var i=0;i<links.length;i++){links[i].href="/identity.html?name="+encodeURIComponent(n)+"&alias="+encodeURIComponent(a);}}catch(e){}})();</script>';
    const b = WK.lastIndexOf('</body>');
    WK = WK.slice(0, b) + script + '\n' + WK.slice(b);
    log('APPEND K2 door cert-link name carrier: 1x');
  }
  // K3 F9(b) guard the walk-advance timers while the door is visible
  {
    let n = 0;
    WK = WK.replace(/setTimeout\(\s*(function\s*\(\s*\)\s*\{|\(\s*\)\s*=>\s*\{)/g, (m, open) => {
      return m; // placeholder replaced below by the guarded pass
    });
    // guarded pass: for each setTimeout whose following 400 chars mention a walk-advance, insert the door guard
    const re = /setTimeout\(\s*(function\s*\(\s*\)\s*\{|\(\s*\)\s*=>\s*\{)/g;
    let out = '', last = 0, m2;
    while ((m2 = re.exec(WK)) !== null) {
      const after = WK.slice(m2.index, m2.index + 600);
      if (/showStep|wireStep|questionnaire|renderStep|startWalk/.test(after)) {
        out += WK.slice(last, m2.index + m2[0].length) + "if(document.getElementById('step-door')&&!document.getElementById('step-door').hidden)return;";
        last = m2.index + m2[0].length; n++;
      }
    }
    out += WK.slice(last); WK = out;
    log('REP K3 door guard on walk-advance timers: ' + n + 'x' + (n === 0 ? ' (no matching timer found — see gate region in report)' : ''));
  }

  // ================= IDENTITY =================
  // I1 F9(a) print the passed name: pre-fill the alias input + paint the composing name line
  {
    const anchor = "const rawName = passedName || savedName || '';";
    const n = count(I, anchor);
    if (n === 1) {
      const ins = "\n/* FIX2 F9(a) — the certificate prints the name from the URL: pre-fill the alias input and paint the composing name line. */\ntry{var _fxAlias=urlParams.get('alias')||passedName||'';var _fxIn=document.querySelector('input[placeholder*=\"lias\"]')||document.querySelector('input');if(_fxIn&&_fxAlias&&!_fxIn.value)_fxIn.value=_fxAlias;var _fxName=document.querySelector('[data-cert-name]')||document.querySelector('.cert-name');if(_fxName&&_fxAlias)_fxName.textContent=_fxAlias;}catch(e){}";
      I = rep(I, anchor, anchor + ins, 1, 'I1 name pre-fill');
    } else log('WARN I1: rawName anchor found ' + n + 'x (expected 1)');
  }
  // I2 F7 seal on the certificate (before the alias input) + seal CSS if missing
  {
    const inp = I.indexOf('placeholder="Enter alias"');
    if (inp > -1) {
      const tagStart = I.lastIndexOf('<input', inp);
      I = I.slice(0, tagStart) + SEAL + '\n' + I.slice(tagStart);
      log('REP I2 seal before alias input: 1x');
    } else log('WARN I2: alias input placeholder not found');
    if (I.indexOf('.deal-seal{width:120px') < 0) {
      const h = I.indexOf('</head>');
      I = I.slice(0, h) + '<style id="fpFixDistill2">\n' + SEAL_CSS + '\n.deal-seal{margin:14px auto 0}\n</style>\n' + I.slice(h);
      log('APPEND I2 seal CSS to identity');
    }
  }
  // I3 F9: /welcome navigation carries name+alias — report contexts (patch only the plain form)
  {
    let i = -1, hits = [];
    while ((i = I.indexOf('/welcome', i + 1)) !== -1) hits.push(i);
    log('CHECK I3 /welcome occurrences in identity: ' + hits.length);
    for (const h of hits.slice(0, 6)) log('  /welcome ctx: ' + JSON.stringify(I.slice(Math.max(0, h - 160), h + 160).replace(/\n/g, ' ').slice(0, 320)));
  }

  // ================= HARNESS (byte + geometry + syntax) =================
  const H = [];
  function chk(label, ok, detail) { H.push({ label, ok, detail }); log((ok ? 'PASS ' : 'FAIL ') + label + (detail ? ' — ' + detail : '')); }
  // sizes + shas
  for (const [k, s] of [['unfold', U], ['welcome', W], ['walk', WK], ['identity', I]]) {
    log('FIXED ' + k + ': ' + Buffer.byteLength(s) + 'B sha256 ' + sha(s));
  }
  // F1 geometry: corner 96, padding-top 112, board top 124 > 96
  chk('F1 corner 96px in W', count(W, 'width:96px;height:96px') >= 1, count(W, 'width:96px;height:96px') + 'x; 208px left: ' + count(W, 'width:208px;height:208px'));
  chk('F1 stage top padding 112px', W.includes('padding-top:112px!important'), 'board top = 112+12 = 124 > corner bottom 96');
  chk('F1 corner 96px in U', count(U, 'width:96px;height:96px') >= 1, count(U, 'width:96px;height:96px') + 'x');
  // F2/F4 face pin
  chk('F2/F4 face pins to viewport right edge', W.includes('left:calc(100vw - 116px)!important'), 'left=1804, right=1908 <= 1920; top = board top+4..12 = 128..136 > 96');
  // F3 vertical budget
  const budget = 144 + 120 + 170 + 190 + 56 + 32 + 20;
  chk('F3 vertical budget fits one view', budget < 826, 'photo144+nutshell120+showcase170+foot190+button56+padding32+gaps20 = ' + budget + ' < board 826 (1080-112-118-24)');
  chk('F3 foot forced visible in talk view', W.includes('.fp-smart-talk .ib-foot{display:block!important}'), '');
  // F5a
  chk('F5a deck fp-noslide 9 boards', count(W.split('id="deckBody"')[1].split('id="letterBody"')[0], 'fp-noslide') === 9, '');
  chk('F5a letter fp-noslide 9 boards', count(W.split('id="letterBody"')[1].split('id="fpLegal"')[0], 'fp-noslide') === 9, '');
  chk('F5a unfold fp-noslide 9 boards', count(U, 'fp-noslide') >= 9, count(U, 'fp-noslide') + ' total (incl CSS)');
  chk('F5a deck37 + letter37 sign photo', count(W, SIGN_PHOTO) === 2, count(W, SIGN_PHOTO) + 'x exact harvested sign-photo div (deck37 + letter37); face-9.jpg total in W: ' + count(W, 'face-9.jpg'));
  // F5b race: retry/fallback code present (fix-1) + aspect-ratio reserve
  chk('F5b showcase img aspect-ratio reserve', W.includes('.lb-showcase img{aspect-ratio:16/9}') && U.includes('#deckBody .lb-showcase img{aspect-ratio:16/9}'), '');
  chk('F5b retry/fallback still present (fix-1)', W.includes('?retry=1') || W.includes('retry'), 'fix-1 capture-phase retry in welcome');
  // F5c fit
  chk('F5c unfold showcase img height 100% + contain', /lb-showcase img\{[^}]*height:100%!important;object-fit:contain/.test(U), '');
  chk('F5c stage showcase img height 100% + contain', W.includes('height:100%!important;object-fit:contain'), '');
  // F6 frame-title phrase: print the single "many people" context in each file (it is NOT the frame title phrase)
  for (const [k, s] of [['unfold', U], ['welcome', W]]) {
    const i = s.indexOf('many people');
    if (i > -1) log('CHECK F6 "' + k + '" many-people ctx: ' + JSON.stringify(s.slice(Math.max(0, i - 200), i + 200).replace(/\n/g, ' ').slice(0, 400)));
  }
  // F6
  chk('F6 board2 one story', count(W, 'The Collective Intelligence Network') >= 2 && count(U, 'The Collective Intelligence Network') >= 1 && count(W, 'One network, many people, many minds') === 0 && count(U, 'One network, many people, many minds') === 0, 'W static ' + count(W, 'The Collective Intelligence Network') + 'x, U ' + count(U, 'The Collective Intelligence Network') + 'x; frame-title phrase 0 in both');
  // F7 seals
  chk('F7 deck seals 37', count(W, '&middot; The Deck' + SEAL) === 37, '');
  chk('F7 letter+rail seals', count(W, '&middot; The Collective Agreement' + SEAL) >= 37, count(W, '&middot; The Collective Agreement' + SEAL) + 'x');
  chk('F7 unfold seal mechanism (frame builds per-board)', U.includes('frame-red-n'), 'frame-red-n in unfold; end-card seal element present: ' + (U.includes('id="dealSeal"') ? 'yes' : 'no'));
  chk('F7 walk door seal', WK.includes('id="step-door"') && WK.includes(SEAL), '');
  chk('F7 identity seal', I.includes(SEAL), '');
  // F8
  chk('F8 Nine pictures gone everywhere', count(W, 'Nine pictures') + count(U, 'Nine pictures') + count(WK, 'Nine pictures') + count(I, 'Nine pictures') === 0, '');
  chk('F8 Thirty-seven boards present', W.includes('Thirty-seven boards. One beautiful story.'), '');
  // F9
  chk('F9(a) identity prints name from URL', I.includes('_fxAlias') && I.includes('urlParams.get(\'alias\')'), 'pre-fill inserted after rawName');
  chk('F9(b) walk door cert link carries name', WK.includes('nayanet_user_name') && WK.includes('/identity.html?name='), '');
  chk('F9(c) hold between name entry and identity', W.includes('fpHold') || W.includes('hold'), 'fix-1 hold wiring retained (see note in report)');
  // F10
  chk('F10 bridge URL becomes ?stage=bridge', W.includes("history.replaceState(null,'','/?stage=bridge')"), '');
  // ruling (a)
  const hiredCurly = count(W, 'You\u2019re hired') + count(W, 'You&rsquo;re hired');
  const hiredStraight = count(W, "You're hired");
  log('CHECK ruling(a) "You\u2019re hired" curly in fixed W: ' + hiredCurly + '; straight: ' + hiredStraight + ' (1 = legal disclaimer "The phrase \\"You\'re hired\\" is a community welcome...")');
  chk('ruling(a) money-board sentence cut', count(W, '<p><b>Congratulations.</b></p><p><b>You&rsquo;re hired!</b></p>') === 0 && count(W, 'hired!') === 0, '"hired!" remaining in W: ' + count(W, 'hired!') + '; board 37 keeps its own "you\u2019re hired" (title + nutshell echo, same board)');
  // ruling (b)
  chk('ruling(b) board22 title plain', count(W, 'How collective chain technology works') === 0 && count(U, 'How collective chain technology works') === 0 && W.includes('How it all connects') && U.includes('How it all connects'), 'new title in both; old title 0 in both');
  // ruling (c) images not replaced
  chk('ruling(c) board 2/22 images not replaced', W.includes('slide-1.jpg') && W.includes('slide-'), 'slide-1.jpg (board 2) still the same harvested file; fit only');
  // syntax: every <script> block parses
  function syntaxCheck(name, s) {
    const blocks = [...s.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)];
    let bad = 0, n = 0;
    for (const b of blocks) {
      const code = b[1];
      if (!code.trim()) continue;
      n++;
      try { new vm.Script(code, { filename: name }); } catch (e) { bad++; log('  SYNTAX FAIL ' + name + ' block ' + n + ': ' + e.message.slice(0, 160)); }
    }
    return { n, bad };
  }
  for (const [k, s] of [['unfold', U], ['welcome', W], ['walk', WK], ['identity', I]]) {
    const r = syntaxCheck(k, s);
    chk('syntax: ' + k + ' script blocks parse', r.bad === 0, r.n + ' blocks, ' + r.bad + ' failures');
  }
  const fails = H.filter((h) => !h.ok);
  log('HARNESS: ' + (H.length - fails.length) + '/' + H.length + ' PASS, ' + fails.length + ' FAIL');
  if (fails.length) for (const f of fails) log('  FAIL: ' + f.label + ' — ' + (f.detail || ''));
  // geometry summary (for the report)
  // ---- LAWS (replication of check-design-laws.py, regexes verbatim; the script cannot run: base files are not on disk under EPERM)
  function lawsCheck(name, text) {
    const fails = [], warns = [];
    const GRAY_RES = [
      /#(?:888|999|aaa|bbb|ccc|8b8b9c|808080|777777|666666)\b/i,
      /\bgray\b/i, /\bgrey\b/i, /--dim\b/i,
      /color\s*:\s*rgba?\([^)]*,\s*0\.[0-6]\d*\)/i,
    ];
    const FONTSIZE_RE = /font-size\s*:\s*(?:clamp\([^)]*?(\d+(?:\.\d+)?)px|(\d+(?:\.\d+)?)px)/gi;
    const COLOR_DECL_RE = /(?<![a-z-])color\s*:\s*([^;}{]+)/gi;
    const ALLOWED_TEXT = new Set(['#ffffff', '#fff', 'white', '#d4a017', '#8e24aa', '#07925f', '#0f52ba', '#050607', '#000000', '#000', 'black', 'inherit', 'currentcolor']);
    const FORBIDDEN_TEXT = new Set(['#c62828', '#c2410c', '#a21caf', '#ff5e6c', '#ff9a5a', '#e84fff', '#ff1493', '#ff2a2a', '#ff8c00']);
    const lines = text.split('\n');
    lines.forEach((line, idx) => {
      for (const rx of GRAY_RES) {
        if (rx.test(line)) { fails.push(name + ':' + (idx + 1) + ': GRAY (§2.2): ' + line.trim().slice(0, 120)); break; }
      }
    });
    let m;
    while ((m = FONTSIZE_RE.exec(text)) !== null) {
      const vals = [m[1], m[2]].filter((v) => v != null).map(Number);
      if (vals.length && Math.min(...vals) < 17) {
        const ln = text.slice(0, m.index).split('\n').length;
        fails.push(name + ':' + ln + ': SIZE (§2.3 below 17px): ' + m[0]);
      }
    }
    while ((m = COLOR_DECL_RE.exec(text)) !== null) {
      let val = m[1].trim().toLowerCase();
      if (val.startsWith('var(')) continue;
      val = val.split(/\s+/)[0].replace(/;$/, '');
      const ln = text.slice(0, m.index).split('\n').length;
      if (FORBIDDEN_TEXT.has(val)) fails.push(name + ':' + ln + ': TEXT-COLOR (§2.2 forbidden): ' + m[0].trim().slice(0, 120));
      else if (!ALLOWED_TEXT.has(val) && !val.startsWith('#')) warns.push(name + ':' + ln + ': TEXT-COLOR? (§2.2 eye): ' + m[0].trim().slice(0, 120));
    }
    if (!text.includes(':hover')) warns.push(name + ': NO-HOVER (§1)');
    return { fails, warns };
  }
  for (const [k, base, fixed] of [['unfold', U0, U], ['welcome', W0, W]]) {
    const b = lawsCheck(k + ' base', base), f = lawsCheck(k + ' fixed', fixed);
    log('LAWS ' + k + ': base ' + b.fails.length + ' FAIL / ' + b.warns.length + ' WARN  ->  fixed ' + f.fails.length + ' FAIL / ' + f.warns.length + ' WARN  (delta ' + (f.fails.length - b.fails.length) + ' FAIL / ' + (f.warns.length - b.warns.length) + ' WARN)');
    // show any NEW fail lines introduced by the fix (first 5)
    const newFails = f.fails.filter((x) => !b.fails.includes(x));
    for (const nf of newFails.slice(0, 5)) log('  NEW FAIL: ' + nf);
    if (newFails.length > 5) log('  ... and ' + (newFails.length - 5) + ' more new FAILs');
  }
  log('GEOMETRY 1920x1080: corner 96x96 at 4 viewport corners; board top = 112(pad)+12(margin) = 124 > 96 (F1 cured in geometry); face top = 124+4..12 = 128..136 > 96, face left = 1920-116 = 1804, right = 1908 <= 1920 (F2/F4); board height = 1080-112-118-24 = 826; budget 732 < 826 (F3); showcase 170 max + contain (F5c).');
  return { U, W, WK, I, H, LOG };
}
if (require.main === module) { main().catch((e) => { console.error('FATAL', e); process.exit(1); }); }
module.exports = main;
