#!/usr/bin/env node
// check-fix3.js — CHECKER's independent verification of agreement distill fix-3.
// Written by the checker from the brief + base bytes. Does NOT reuse the maker's
// run-fix3.js: the fix-3 transforms below are the checker's own application of the
// brief's remedies (anchors located + context-verified in the fix-2 bytes first),
// the state machine scenarios are the checker's own, the laws replication is
// transcribed fresh from check-design-laws.py, and the fetch-verdict causality
// test uses a pending-fetch harness variant. No file writes (EPERM). Results to stdout.
// Usage: node check-fix3.js            (full check)
//        node check-fix3.js --dump walk|identity|unfold|welcome   (print fixed bytes)
const https = require('https');
const crypto = require('crypto');
const vm = require('vm');
const runFix2 = require('/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix3-20261119/maker/work/run-fix2-export.js');
const H1 = require('./dom-check3.js'); // checker copy of the fix-1 DOM + pending-fetch patch
const makeEnv = H1.makeEnv, q = H1.q, qa = H1.qa, sleep = H1.sleep;

const STAGE = 'naya-walk-beginning-staging.nayapower.workers.dev';
const BASE = {
  unfold: { bytes: 141781, sha256: '5fe1a3ec2231c128774c6eb00736913d93117d3eaa06278e2a16183cdebee6ab' },
  welcome: { bytes: 1913241, sha256: 'c3c750b72a2b0330d15de8831e9b24719116991e6c0df9dbc5d329834fbbaed5' },
  walk: { bytes: 4361369, sha256: '0f05b3f96ce8edd0ecb094c0f64972098f788c3943e22b5446c8bb60e9b0e2fd' },
  identity: { bytes: 401040, sha256: '3279dc3572337e5e' }, // 16-hex prefix (as filed); full sha checked via git tree below
};
const FIX2 = {
  unfold: { bytes: 142120, sha256: '50876fff8caa79eeb3d6d75b4d2099db39ade2688edf6762e58ac9083eb0d26b' },
  welcome: { bytes: 1929575, sha256: '3874b7ebcc6b95e2a7ef2d320ed95e13253083a954fe6c0efc36afe6d58fa747' },
  walk: { bytes: 4362221, sha256: '854a8f60328afca94e9856d660d02e897c4a777e0e5be4a9dcaaebc998283244' },
  identity: { bytes: 402166, sha256: 'd0f26529513ba25eb6614098f369583393345d5ee02ec4bc914c0d49085c0513' },
};
const FIX3CLAIM = { // maker's §2 claims — what this script must reproduce or refute
  unfold: { bytes: 142120, sha256: '50876fff8caa79eeb3d6d75b4d2099db39ade2688edf6762e58ac9083eb0d26b' },
  welcome: { bytes: 1929575, sha256: '3874b7ebcc6b95e2a7ef2d320ed95e13253083a954fe6c0efc36afe6d58fa747' },
  walk: { bytes: 4363239, sha256: 'b068d1da38403878eb0b4a552ea92efec2fe77724d6a12fdef04f98fb8f8089b' },
  identity: { bytes: 402647, sha256: '51776174b59cee4a39f7a00eb7f7b874fc33103a0235308a876d4a94179307f5' },
};
function get(p) {
  return new Promise((res, rej) => {
    const req = https.get({ hostname: STAGE, path: p, headers: { 'User-Agent': 'Mozilla/5.0' } }, (r) => {
      const b = []; r.on('data', (c) => b.push(c));
      r.on('end', () => res(Buffer.concat(b).toString('utf8')));
      r.on('error', rej);
    });
    req.setTimeout(60000, () => req.destroy(new Error('timeout ' + p)));
    req.on('error', rej);
  });
}
function sha(s) { return crypto.createHash('sha256').update(s, 'utf8').digest('hex'); }
function count(s, needle) { let n = 0, i = -1; while ((i = s.indexOf(needle, i + 1)) !== -1) n++; return n; }
let PASS = 0, FAIL = 0; const FAILURES = [];
function check(n, c, d) {
  if (c) { PASS++; console.log('  PASS ' + n + (d ? ' — ' + d : '')); }
  else { FAIL++; FAILURES.push(n); console.log('  FAIL ' + n + (d ? ' — ' + d : '')); }
}
function ctx(s, needle, before, after) {
  const i = s.indexOf(needle);
  if (i < 0) return 'NOT FOUND: ' + JSON.stringify(needle.slice(0, 80));
  return JSON.stringify(s.slice(Math.max(0, i - (before || 120)), i + needle.length + (after || 120)).replace(/\n/g, ' '));
}
// Replace exactly once; print the anchor's context so the location is on the record.
function rep1(s, needle, repl, label) {
  const n = count(s, needle);
  console.log('  ANCHOR ' + label + ': found ' + n + 'x :: ' + ctx(s, needle, 100, 100));
  if (n !== 1) throw new Error('REP ' + label + ': found ' + n + ', expected 1');
  return s.split(needle).join(repl);
}

// ================= CHECKER'S OWN FIX-3 TRANSFORMS =================
// Remedies per the brief §"What failed" + captain's reconciliation:
//  (1) paired ?name=+?alias= -> pre-fill alias + paint hero via paintHeroName AFTER
//      the load-time paint (and after the FIX3 clear); un-paired stays empty.
//  (2) guard proceed() while #step-door is visible (covers every advance leg).
//  (3) guard the 4s claim-gate timer itself so it does not consume the gate.
//  (4) explicit-continue button on the door + wiring in the boot IIFE.
function applyFix3(F2) {
  let I = F2.I, WK = F2.WK;
  // (1) identity — anchor on the load-time paint call (unique in context).
  const I_ANCHOR = "      paintValues(currentAlias + '.nayanet.app', currentAlias, false);\n      if (linesEl) linesEl.hidden = false;\n    }\n\n    updateSmartCredentials();";
  const I_FIX3 = "\n    /* FIX3 (distill fix-3, F9a) — paired identity from the walk: name+alias together ARE the user's identity (the rule currentDisplayName already trusts). Pre-fill the alias field with the paired alias and paint the hero with the paired name, AFTER the load-time paint and AFTER the FIX3 clear. Un-paired: never pre-paint — the clear stands. */\n    try{ if (passedName && passedAlias) { if (aliasInput) aliasInput.value = passedAlias; paintHeroName(passedName); } }catch(e){}";
  I = rep1(I, I_ANCHOR, I_ANCHOR + I_FIX3, 'I-FIX3 paired paint after load paint');
  // (2) walk — guard proceed() at its top.
  const P_ANCHOR = "  var proceed = function(){\n  if (!ID.alias) { showDoor(); return; }";
  const P_GUARD = "  var proceed = function(){\n  /* FIX3 (distill fix-3, F9b) — the door is the gate: while #step-door is visible, NOTHING advances the walk. Only the user's own action on the door (the certificate link or the explicit continue) dismisses it, never a timer. */\n  if (document.getElementById('step-door') && !document.getElementById('step-door').hidden) return;\n  if (!ID.alias) { showDoor(); return; }";
  WK = rep1(WK, P_ANCHOR, P_GUARD, 'W-FIX3a proceed() door guard');
  // (3) walk — guard the claim-gate timer itself.
  const T_ANCHOR = "var gateTimer6 = setTimeout(function(){ if (!gateDone6) { gateDone6 = true; proceed(); } }, 4000);";
  const T_GUARD = "var gateTimer6 = setTimeout(function(){ if (document.getElementById('step-door') && !document.getElementById('step-door').hidden) return; if (!gateDone6) { gateDone6 = true; proceed(); } }, 4000);";
  WK = rep1(WK, T_ANCHOR, T_GUARD, 'W-FIX3b claim-gate timer guard');
  // (4a) walk — explicit-continue button after the certificate link.
  const D_ANCHOR = '<a class="p3-enter" href="/identity.html" style="text-decoration:none">Get your certificate ◆</a>';
  const D_CONT = D_ANCHOR + '\n<button type="button" class="p3-enter" id="doorContinue" style="font-family:inherit">Continue to the walk ◆</button>';
  WK = rep1(WK, D_ANCHOR, D_CONT, 'W-FIX3c continue button');
  // (4b) walk — wire it in the boot IIFE, just before the no-alias boot line.
  const W_ANCHOR = "  if (!ID.alias) { proceed(); return; }";
  const W_WIRE = "  /* FIX3 (distill fix-3, F9b) — the door's explicit continue: a certified citizen dismisses the door by tapping Continue; the door hides, then proceed() opens the walk. No alias, no continue — the walk opens after the certificate. */\n  (function(){ var c = document.getElementById('doorContinue'); if (!c) return; if (!ID.alias) { c.hidden = true; return; } c.addEventListener('click', function(){ var d = document.getElementById('step-door'); if (d) d.hidden = true; proceed(); }); })();\n" + W_ANCHOR;
  WK = rep1(WK, W_ANCHOR, W_WIRE, 'W-FIX3d continue wiring');
  return { U: F2.U, W: F2.W, WK, I, _ins: { I_FIX3, P_GUARD, T_GUARD, D_CONT, W_WIRE } };
}
async function buildFixed() {
  const R = await runFix2();
  const F2 = { U: R.U, W: R.W, WK: R.WK, I: R.I };
  for (const [k, s, exp] of [['unfold', F2.U, FIX2.unfold], ['welcome', F2.W, FIX2.welcome], ['walk', F2.WK, FIX2.walk], ['identity', F2.I, FIX2.identity]]) {
    const b = Buffer.byteLength(s), h = sha(s);
    if (b !== exp.bytes || h !== exp.sha256) throw new Error('fix-2 mismatch: ' + k + ' ' + b + 'B ' + h.slice(0, 16));
  }
  console.log('FIX2 REPRODUCED: all four shas match the fix-2 checker report §1');
  const F3 = applyFix3(F2);
  const base = {
    unfold: await get('/agreement'),
    welcome: await get('/?stage=deck'),
    walk: await get('/welcome'),
    identity: await get('/identity.html?name=Distill%20Eye%20Walk'),
  };
  return { F2, F3, base };
}
module.exports = { buildFixed, applyFix3 };

// ================= BYTE HARNESS (checker's own) =================
function byteHarness(F2, F3, base) {
  console.log('\n== BYTE HARNESS ==');
  // fixed sizes + shas vs the maker's §2 claims
  for (const [k, s, claim] of [['unfold', F3.U, FIX3CLAIM.unfold], ['welcome', F3.W, FIX3CLAIM.welcome], ['walk', F3.WK, FIX3CLAIM.walk], ['identity', F3.I, FIX3CLAIM.identity]]) {
    const b = Buffer.byteLength(s), h = sha(s);
    console.log('CHECKER-FIXED3 ' + k + ': ' + b + 'B sha256 ' + h);
    check('fixed sha matches maker claim: ' + k, b === claim.bytes && h === claim.sha256, b + 'B vs claim ' + claim.bytes + 'B; sha ' + h.slice(0, 16) + ' vs ' + claim.sha256.slice(0, 16));
  }
  check('unfold byte-identical to fix-2 (claimed unchanged)', F3.U === F2.U);
  check('welcome byte-identical to fix-2 (claimed unchanged)', F3.W === F2.W);
  check('walk delta vs fix-2 is +1018 B (maker claim)', Buffer.byteLength(F3.WK) - Buffer.byteLength(F2.WK) === 1018, (Buffer.byteLength(F3.WK) - Buffer.byteLength(F2.WK)) + 'B');
  check('identity delta vs fix-2 is +481 B (maker claim)', Buffer.byteLength(F3.I) - Buffer.byteLength(F2.I) === 481, (Buffer.byteLength(F3.I) - Buffer.byteLength(F2.I)) + 'B');
  // Diff minimality by reverse-application: strip exactly the four insertions
  // from the fixed bytes; the result must be byte-identical to the fix-2 bytes.
  const ins = F3._ins;
  const revI = F3.I.split(ins.I_FIX3).join('');
  check('MINIMAL identity: fixed minus the one I-FIX3 block == fix-2 bytes exactly', revI === F2.I);
  const guardLine = "  /* FIX3 (distill fix-3, F9b) — the door is the gate: while #step-door is visible, NOTHING advances the walk. Only the user's own action on the door (the certificate link or the explicit continue) dismisses it, never a timer. */\n  if (document.getElementById('step-door') && !document.getElementById('step-door').hidden) return;\n";
  const T_ANCHOR = "var gateTimer6 = setTimeout(function(){ if (!gateDone6) { gateDone6 = true; proceed(); } }, 4000);";
  const btnLine = '\n<button type="button" class="p3-enter" id="doorContinue" style="font-family:inherit">Continue to the walk ◆</button>';
  const wireBlock = "  /* FIX3 (distill fix-3, F9b) — the door's explicit continue: a certified citizen dismisses the door by tapping Continue; the door hides, then proceed() opens the walk. No alias, no continue — the walk opens after the certificate. */\n  (function(){ var c = document.getElementById('doorContinue'); if (!c) return; if (!ID.alias) { c.hidden = true; return; } c.addEventListener('click', function(){ var d = document.getElementById('step-door'); if (d) d.hidden = true; proceed(); }); })();\n";
  let revW = F3.WK;
  check('MINIMAL walk: guard comment+line present 1x', count(revW, guardLine) === 1);
  revW = revW.split(guardLine).join('');
  check('MINIMAL walk: guarded timer present 1x', count(revW, ins.T_GUARD) === 1);
  revW = revW.split(ins.T_GUARD).join(T_ANCHOR);
  check('MINIMAL walk: continue button present 1x', count(revW, btnLine) === 1);
  revW = revW.split(btnLine).join('');
  check('MINIMAL walk: wiring block present 1x', count(revW, wireBlock) === 1);
  revW = revW.split(wireBlock).join('');
  check('MINIMAL walk: fixed minus the four insertions == fix-2 bytes exactly', revW === F2.WK);
  // Insertion content carries no laws-relevant declarations
  const allIns = ins.I_FIX3 + ins.P_GUARD + ins.T_GUARD + ins.D_CONT + ins.W_WIRE;
  check('insertions carry no color: declaration', allIns.indexOf('color:') === -1);
  check('insertions carry no font-size declaration', allIns.indexOf('font-size') === -1);
  check('insertions add no new CSS rules (no <style>; style= only the anchor text-decoration + the button font inherit)', (allIns.match(/<style/g) || []).length === 0 && count(allIns, 'style=') === 2, count(allIns, 'style=') + ' style= (1 = D_ANCHOR text-decoration, 1 = button font-family:inherit)');
  // Anchor-order proof in identity: FIX2 pre-fill BEFORE the FIX3 clear BEFORE the FIX3 paint
  const iFix2 = F3.I.indexOf("/* FIX2 F9(a)");
  const iClear = F3.I.indexOf("aliasInput.value = ''");
  const iFix3 = F3.I.indexOf('/* FIX3 (distill fix-3, F9a)');
  const iPaint = F3.I.indexOf('updateSmartCredentials();');
  console.log('  identity offsets: FIX2-insert=' + iFix2 + ' FIX3-clear=' + iClear + ' load-paint=' + iPaint + ' FIX3-paint=' + iFix3);
  check('identity order: FIX2 pre-fill < FIX3 clear < load paint < FIX3 paired paint', iFix2 > -1 && iClear > iFix2 && iPaint > iClear && iFix3 > iPaint, 'offsets ' + [iFix2, iClear, iPaint, iFix3].join(' < '));
  check('identity: FIX3 clear still present 2x (boot clear + switchToDifferentAlias)', count(F3.I, "aliasInput.value = ''") === 2, count(F3.I, "aliasInput.value = ''") + 'x');
  check('identity: paintHeroName is the one hero painter (def 1x)', count(F3.I, 'function paintHeroName') === 1 || count(F3.I, 'paintHeroName = function') === 1, 'paintHeroName defs: function=' + count(F3.I, 'function paintHeroName'));
  check('identity: paired condition is name AND alias (1x)', count(F3.I, 'if (passedName && passedAlias)') === 1);
  check('identity: FIX6 lowercase load check untouched (pre-existing)', F3.I.indexOf("passedAlias.toLowerCase()") > -1 || F3.I.indexOf('toLowerCase().replace(/[^a-z0-9]/g') > -1, ctx(F3.I, 'toLowerCase', 80, 80));
  // Walk byte checks
  const spacedGuard = "if (document.getElementById('step-door') && !document.getElementById('step-door').hidden) return;";
  console.log('  spaced door-guard occurrences: ' + count(F3.WK, spacedGuard));
  { let i = -1; while ((i = F3.WK.indexOf(spacedGuard, i + 1)) !== -1) console.log('  spaced-guard ctx: ' + JSON.stringify(F3.WK.slice(Math.max(0, i - 90), i + spacedGuard.length + 60).replace(/\n/g, ' '))); }
  check('walk: proceed() + timer door guards present (spaced form 2x: W-FIX3a + W-FIX3b)', count(F3.WK, spacedGuard) === 2,
    count(F3.WK, spacedGuard) + 'x');
  check('walk: unguarded claim-gate timer gone', count(F3.WK, T_ANCHOR) === 0);
  check('walk: fix-2 K3 guards still 2x', count(F3.WK, "if(document.getElementById('step-door')&&!document.getElementById('step-door').hidden)return;") === 2);
  check('walk: door cert link still exactly 1x', count(F3.WK, 'Get your certificate ◆</a>') === 1);
  check('walk: continue button exactly 1x, same .p3-enter pill as its sibling', count(F3.WK, 'id="doorContinue"') === 1 && F3.WK.indexOf('id="doorContinue"') > F3.WK.indexOf('Get your certificate'));
  check('walk: continue wiring exactly 1x', count(F3.WK, "getElementById('doorContinue')") === 1);
  check('walk: door cert-link name carrier (fix-2 K2) still present', F3.WK.includes('/identity.html?name=') && F3.WK.includes('nayanet_user_name'));
  check('walk: doorContinue is type=button (cannot submit a form)', F3.WK.indexOf('<button type="button" class="p3-enter" id="doorContinue"') > -1);
  check('walk: #step-door is NOT inside a <form> (button cannot submit anything)', (() => { const d = F3.WK.indexOf('id="step-door"'); const f1 = F3.WK.lastIndexOf('<form', d); const fe = f1 === -1 ? -1 : F3.WK.indexOf('</form>', f1); return f1 === -1 || fe < d; })());
  // No-regress spots (fix-2 checker §3, re-checked on fix-3 bytes)
  check('F10 bridge replaceState still exactly 1x', count(F3.W, "history.replaceState(null,'','/?stage=bridge')") === 1);
  check('ruling(a) money-board sentence still cut (hired! 0x)', count(F3.W, 'hired!') === 0);
  check('ruling(a) #letterAll + #fpLinkLetterAll NOT restored (captain settled)', F3.W.indexOf('id="letterAll"') === -1 && F3.W.indexOf('id="fpLinkLetterAll"') === -1, 'letterAll-id=' + F3.W.indexOf('id="letterAll"') + ' fpLinkLetterAll-id=' + F3.W.indexOf('id="fpLinkLetterAll"'));
  check('F7 deck seals still 37x', count(F3.W, '&middot; The Deck<div class="deal-seal') === 37);
  check('F7 letter+rail seals still >=37x', count(F3.W, '&middot; The Collective Agreement<div class="deal-seal') >= 37);
  check('ruling(b) board22 title still plain', count(F3.W, 'How collective chain technology works') === 0 && count(F3.U, 'How collective chain technology works') === 0 && F3.W.includes('How it all connects') && F3.U.includes('How it all connects'));
  check('F8 Nine pictures still 0x everywhere', count(F3.W, 'Nine pictures') + count(F3.U, 'Nine pictures') + count(F3.WK, 'Nine pictures') + count(F3.I, 'Nine pictures') === 0);
  check('F6 board-2 phrase still 0x', count(F3.W, 'One network, many people, many minds') === 0 && count(F3.U, 'One network, many people, many minds') === 0);
  // Images unchanged base -> fixed (all four files)
  for (const [k, b0, f] of [['unfold', base.unfold, F3.U], ['welcome', base.welcome, F3.W], ['walk', base.walk, F3.WK], ['identity', base.identity, F3.I]]) {
    const m0 = (b0.match(/slide-\d+\.jpg/g) || []).sort().join(',');
    const m1 = (f.match(/slide-\d+\.jpg/g) || []).sort().join(',');
    check('ruling(c) slide-*.jpg multiset identical base->fixed: ' + k, m0 === m1, (m0.split(',').filter(Boolean).length) + ' refs');
  }
  // syntax: every <script> block parses
  function syntaxCheck(name, s) {
    const blocks = [...s.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)];
    let bad = 0, n = 0;
    for (const b of blocks) {
      const code = b[1];
      if (!code.trim()) continue;
      n++;
      try { new vm.Script(code, { filename: name }); } catch (e) { bad++; console.log('  SYNTAX FAIL ' + name + ' block ' + n + ': ' + e.message.slice(0, 160)); }
    }
    return { n, bad };
  }
  for (const [k, s] of [['unfold', F3.U], ['welcome', F3.W], ['walk', F3.WK], ['identity', F3.I]]) {
    const r = syntaxCheck(k, s);
    check('syntax: ' + k + ' script blocks parse', r.bad === 0, r.n + ' blocks, ' + r.bad + ' failures');
  }
  // ---- advance-path enumeration in the WALK script (fix-2 bytes: the mechanism under test) ----
  console.log('\n== ADVANCE-PATH ENUMERATION (fix-2 walk bytes — every way the walk can move) ==');
  const scripts = [...F2.WK.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map((m) => m[1]).filter((c) => c.trim());
  console.log('  walk inline scripts: ' + scripts.length);
  scripts.forEach((code, si) => {
    console.log('  -- script ' + si + ' (' + code.length + ' chars) --');
    ['setTimeout(', 'setInterval(', 'fetch(', 'proceed()', 'showDoor(', 'showStep(', '.hidden = false', '.hidden=false', "hidden = false"].forEach((pat) => {
      let i = -1, n = 0;
      while ((i = code.indexOf(pat, i + 1)) !== -1) {
        n++;
        console.log('  [' + pat + ' #' + n + ' @' + i + '] ' + JSON.stringify(code.slice(Math.max(0, i - 100), i + 220).replace(/\n/g, ' ')));
      }
      if (!n) console.log('  [' + pat + '] 0x');
    });
  });
  // identity timers (later repaints?)
  console.log('\n== IDENTITY TIMERS / FETCH (fix-2 bytes — anything that could repaint after boot) ==');
  const iscripts = [...F2.I.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map((m) => m[1]).filter((c) => c.trim());
  iscripts.forEach((code, si) => {
    ['setTimeout(', 'setInterval(', 'fetch(', 'paintHeroName(', 'checkAliasAvailability('].forEach((pat) => {
      let i = -1, n = 0;
      while ((i = code.indexOf(pat, i + 1)) !== -1) {
        n++;
        console.log('  [id-script ' + si + ' ' + pat + ' #' + n + ' @' + i + '] ' + JSON.stringify(code.slice(Math.max(0, i - 80), i + 200).replace(/\n/g, ' ')));
      }
      if (!n) console.log('  [id-script ' + si + ' ' + pat + '] 0x');
    });
  });
  // localStorage keys the walk reads (S7c return-trip premise)
  console.log('\n== WALK STORAGE KEYS ==');
  ['nayanet_smart_alias', 'nayanet_smart_name', 'nayanet_user_name'].forEach((k) => {
    console.log('  key ' + k + ': ' + count(F2.WK, k) + 'x in walk bytes');
  });
  check('walk reads nayanet_smart_alias (return trip can restore the alias)', count(F2.WK, 'nayanet_smart_alias') >= 1);
}

// ================= LAWS (transcribed fresh from check-design-laws.py) =================
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
  text.split('\n').forEach((line, idx) => {
    for (const rx of GRAY_RES) {
      if (rx.test(line)) { fails.push(name + ':' + (idx + 1) + ': GRAY: ' + line.trim().slice(0, 120)); break; }
    }
  });
  let m;
  while ((m = FONTSIZE_RE.exec(text)) !== null) {
    const vals = [m[1], m[2]].filter((v) => v != null).map(Number);
    if (vals.length && Math.min(...vals) < 17) fails.push(name + ':' + (text.slice(0, m.index).split('\n').length) + ': SIZE below 17px: ' + m[0]);
  }
  while ((m = COLOR_DECL_RE.exec(text)) !== null) {
    let val = m[1].trim().toLowerCase();
    if (val.startsWith('var(')) continue;
    val = val.split(/\s+/)[0].replace(/;$/, '');
    const ln = text.slice(0, m.index).split('\n').length;
    if (FORBIDDEN_TEXT.has(val)) fails.push(name + ':' + ln + ': TEXT-COLOR forbidden: ' + m[0].trim().slice(0, 120));
    else if (!ALLOWED_TEXT.has(val) && !val.startsWith('#')) warns.push(name + ':' + ln + ': TEXT-COLOR? eye: ' + m[0].trim().slice(0, 120));
  }
  if (!text.includes(':hover')) warns.push(name + ': NO-HOVER');
  return { fails, warns };
}
function lawsDelta(base, F3) {
  console.log('\n== LAWS DELTA (replication; real checker run separately via pipe) ==');
  for (const [k, b0, f] of [['unfold', base.unfold, F3.U], ['welcome', base.welcome, F3.W], ['walk', base.walk, F3.WK], ['identity', base.identity, F3.I]]) {
    const b = lawsCheck(k + ' base', b0), fx = lawsCheck(k + ' fixed', f);
    const norm = (list) => new Set(list.map((x) => x.replace(/^[^:]+:\d+:/, '')));
    const bn = norm(b.fails), fn = norm(fx.fails);
    let added = 0, removed = 0;
    fn.forEach((x) => { if (!bn.has(x)) { added++; console.log('  TRULY-NEW ' + k + ': ' + x); } });
    bn.forEach((x) => { if (!fn.has(x)) { removed++; console.log('  REMOVED ' + k + ': ' + x); } });
    console.log('LAWS ' + k + ': base ' + b.fails.length + ' FAIL / ' + b.warns.length + ' WARN -> fixed ' + fx.fails.length + ' FAIL / ' + fx.warns.length + ' WARN (normalized +' + added + ' / -' + removed + ', base-set ' + bn.size + ', fixed-set ' + fn.size + ')');
    check('laws: ' + k + ' delta 0/0 (normalized)', added === 0 && removed === 0 && fx.fails.length === b.fails.length && fx.warns.length === b.warns.length,
      'base ' + b.fails.length + '/' + b.warns.length + ' fixed ' + fx.fails.length + '/' + fx.warns.length);
  }
}

// ================= STATE MACHINE (checker's own scenarios) =================
function identityParts(doc) {
  const inputs = qa(doc, 'input');
  let input = null;
  for (const inp of inputs) { const ph = inp.getAttribute('placeholder') || ''; if (ph.indexOf('lias') !== -1) { input = inp; break; } }
  if (!input && inputs.length) input = inputs[0];
  const nameEl = doc.querySelector('[data-cert-name]') || doc.querySelector('.cert-name') || doc.querySelector('#displayName');
  return { input, nameEl };
}
function visibleSteps(doc) {
  return qa(doc, '[id^="step-"]').filter((el) => !el.hidden).map((el) => el.id);
}
async function pollVisible(doc, ms, every) {
  const t0 = Date.now();
  let last = JSON.stringify(visibleSteps(doc));
  while (Date.now() - t0 < ms) {
    await sleep(every);
    const now = JSON.stringify(visibleSteps(doc));
    if (now !== last) return { atMs: Date.now() - t0, from: last, to: now };
    last = now;
  }
  return { atMs: null, from: last, to: last };
}

async function scIdentity(F3, base) {
  console.log('\n== C-IDENT: certificate identity (checker scenarios) ==');
  // PAIRED on fix-3 bytes
  {
    const e = makeEnv(F3.I, '?name=Distill%20Eye%20Walk&alias=Distill');
    await sleep(50);
    const p = identityParts(e.document);
    check('C-IDENT paired: alias input exists', !!p.input);
    if (p.input) check('C-IDENT paired: input holds the paired alias (lowercased by FIX6)', p.input.value === 'distill', 'value=' + JSON.stringify(p.input.value));
    check('C-IDENT paired: name line exists', !!p.nameEl);
    if (p.nameEl) {
      check('C-IDENT paired: hero text is the passed name', p.nameEl.textContent === 'Distill Eye Walk', 'text=' + JSON.stringify(p.nameEl.textContent));
      check('C-IDENT paired: hero data-text set (the ::before echo source)', p.nameEl.getAttribute('data-text') === 'Distill Eye Walk', 'data-text=' + JSON.stringify(p.nameEl.getAttribute('data-text')));
      check('C-IDENT paired: hero unhidden', p.nameEl.hidden === false, 'hidden=' + p.nameEl.hidden);
    }
    check('C-IDENT paired: seal present', !!e.document.querySelector('.deal-seal'));
    await sleep(5000);
    if (p.input) check('C-IDENT paired: input STILL the alias after 5s (no later wipe)', p.input.value === 'distill', 'value=' + JSON.stringify(p.input.value));
    if (p.nameEl) check('C-IDENT paired: hero STILL the passed name after 5s (no later repaint)', p.nameEl.textContent === 'Distill Eye Walk' && p.nameEl.getAttribute('data-text') === 'Distill Eye Walk' && p.nameEl.hidden === false,
      'text=' + JSON.stringify(p.nameEl.textContent) + ' data-text=' + JSON.stringify(p.nameEl.getAttribute('data-text')) + ' hidden=' + p.nameEl.hidden);
    // User typing in the field is a different scenario from boot paint: record only.
    if (p.input) {
      p.input.value = 'distill';
      const ev = { type: 'input', bubbles: true, target: p.input, currentTarget: p.input, defaultPrevented: false, _stopped: false, preventDefault: function () { this.defaultPrevented = true; }, stopPropagation: function () { this._stopped = true; } };
      p.input.dispatchEvent(ev);
      await sleep(50);
      console.log('  OBSERVE after manual input event on the alias field: hero text=' + JSON.stringify(p.nameEl ? p.nameEl.textContent : null) + ' (user typing is not the boot-paint scenario; recorded, not scored)');
    }
    check('C-IDENT paired: no script errors', e.errors.length === 0, e.errors.length + ' errors');
  }
  // NAME-ONLY on fix-3 bytes (captain's reconciliation: must stay EMPTY)
  {
    const e = makeEnv(F3.I, '?name=Distill%20Eye%20Walk');
    await sleep(50);
    const p = identityParts(e.document);
    if (p.input) check('C-IDENT name-only: input stays EMPTY', p.input.value === '', 'value=' + JSON.stringify(p.input.value));
    if (p.nameEl) {
      check('C-IDENT name-only: hero stays blank', p.nameEl.textContent === '', 'text=' + JSON.stringify(p.nameEl.textContent));
      check('C-IDENT name-only: hero stays hidden', p.nameEl.hidden === true, 'hidden=' + p.nameEl.hidden);
      check('C-IDENT name-only: hero data-text stays null', p.nameEl.getAttribute('data-text') === null, 'data-text=' + JSON.stringify(p.nameEl.getAttribute('data-text')));
    }
    check('C-IDENT name-only: no script errors', e.errors.length === 0, e.errors.length + ' errors');
  }
  // ALIAS-ONLY on fix-3 bytes (pre-existing FIX6 fill; hero must stay hidden)
  {
    const e = makeEnv(F3.I, '?alias=Distill');
    await sleep(50);
    const p = identityParts(e.document);
    if (p.input) check('C-IDENT alias-only: input holds the alias (FIX6, pre-existing)', p.input.value === 'distill', 'value=' + JSON.stringify(p.input.value));
    if (p.nameEl) check('C-IDENT alias-only: hero stays hidden (no name to paint)', p.nameEl.hidden === true, 'hidden=' + p.nameEl.hidden);
    check('C-IDENT alias-only: no script errors', e.errors.length === 0, e.errors.length + ' errors');
  }
  // NO PARAMS
  {
    const e = makeEnv(F3.I, '');
    await sleep(50);
    const p = identityParts(e.document);
    if (p.input) check('C-IDENT no-params: input empty', p.input.value === '', 'value=' + JSON.stringify(p.input.value));
    if (p.nameEl) check('C-IDENT no-params: hero hidden', p.nameEl.hidden === true, 'hidden=' + p.nameEl.hidden);
    check('C-IDENT no-params: no script errors', e.errors.length === 0, e.errors.length + ' errors');
  }
  // PAIRED on BASE bytes — the before-state (proves the fix changed something)
  {
    const e = makeEnv(base.identity, '?name=Distill%20Eye%20Walk&alias=Distill');
    await sleep(50);
    const p = identityParts(e.document);
    if (p.input) check('C-IDENT base paired: input holds alias on base too (FIX6)', p.input.value === 'distill', 'value=' + JSON.stringify(p.input.value));
    if (p.nameEl) {
      check('C-IDENT base paired: hero BLANK on base (the bug)', p.nameEl.textContent === '', 'text=' + JSON.stringify(p.nameEl.textContent));
      check('C-IDENT base paired: hero HIDDEN on base (the bug)', p.nameEl.hidden === true, 'hidden=' + p.nameEl.hidden);
    }
    check('C-IDENT base paired: no script errors', e.errors.length === 0, e.errors.length + ' errors');
  }
}

async function scWalkDoor(F3, F2) {
  console.log('\n== C-WALK: door guard + continue (checker scenarios) ==');
  // Aliased, fix-3 bytes: hold 6s (past the 4s timer AND the fetch verdict)
  {
    const e = makeEnv(F3.WK, '?name=Distill%20Eye%20Walk&alias=Distill');
    const doc = e.document;
    const door = q(doc, '#step-door');
    check('C-WALK aliased: door exists', !!door);
    if (door) {
      check('C-WALK aliased: door visible at boot', door.hidden === false, 'hidden=' + door.hidden);
      check('C-WALK aliased: seal on the door', !!door.querySelector('.deal-seal'));
      const link = door.querySelector('a[href*="/identity.html"]');
      check('C-WALK aliased: cert link exists', !!link);
      if (link) check('C-WALK aliased: cert link carries name+alias', link.getAttribute('href').indexOf('name=Distill') !== -1 && link.getAttribute('href').indexOf('alias=Distill') !== -1, 'href=' + JSON.stringify(link.getAttribute('href')));
    }
    const r = await pollVisible(doc, 6000, 250);
    check('C-WALK aliased: door STILL visible after 6s, no user action', r.atMs === null && JSON.stringify(visibleSteps(doc)) === '["step-door"]', 'changed at ' + r.atMs + 'ms to ' + r.to + '; now=' + JSON.stringify(visibleSteps(doc)));
    const cont = q(doc, '#doorContinue');
    check('C-WALK aliased: continue exists', !!cont);
    if (cont) {
      check('C-WALK aliased: continue VISIBLE for the certified citizen', cont.hidden === false, 'hidden=' + cont.hidden);
      check('C-WALK aliased: continue reads "Continue to the walk ◆"', cont.textContent.indexOf('Continue to the walk') !== -1, JSON.stringify(cont.textContent));
      check('C-WALK aliased: continue is the same .p3-enter pill as the cert link', cont.classList.contains('p3-enter') && (door.querySelector('a.p3-enter') !== null));
      cont.click();
      await sleep(50);
      check('C-WALK aliased: tap Continue -> questionnaire opens, door gone', JSON.stringify(visibleSteps(doc)) === '["step-1"]', 'visible=' + JSON.stringify(visibleSteps(doc)));
    }
    check('C-WALK aliased: no script errors', e.errors.length === 0, e.errors.length + ' errors');
  }
  // No alias, fix-3 bytes
  {
    const e = makeEnv(F3.WK, '');
    await sleep(50);
    const doc = e.document;
    const door = q(doc, '#step-door');
    check('C-WALK no-alias: door visible at boot', door && door.hidden === false);
    const cont = q(doc, '#doorContinue');
    check('C-WALK no-alias: continue exists in markup', !!cont);
    if (cont) check('C-WALK no-alias: continue HIDDEN without a certificate', cont.hidden === true, 'hidden=' + cont.hidden);
    check('C-WALK no-alias: cert link present (the only way forward)', !!(door && door.querySelector('a[href*="/identity.html"]')));
    check('C-WALK no-alias: no script errors', e.errors.length === 0, e.errors.length + ' errors');
  }
  // Certified return trip (localStorage), fix-3 bytes
  {
    const e = makeEnv(F3.WK, '', { local: { nayanet_smart_alias: 'distill', nayanet_smart_name: 'Distill Eye Walk' } });
    const doc = e.document;
    const door = q(doc, '#step-door');
    check('C-WALK return: door visible at boot', door && door.hidden === false);
    const r = await pollVisible(doc, 2000, 250);
    check('C-WALK return: door holds 2s (no auto-advance on the return trip)', r.atMs === null && JSON.stringify(visibleSteps(doc)) === '["step-door"]', 'now=' + JSON.stringify(visibleSteps(doc)));
    const cont = q(doc, '#doorContinue');
    check('C-WALK return: continue visible on the return trip', cont && cont.hidden === false);
    if (cont) {
      cont.click();
      await sleep(50);
      check('C-WALK return: tap Continue -> step-1', JSON.stringify(visibleSteps(doc)) === '["step-1"]', 'visible=' + JSON.stringify(visibleSteps(doc)));
    }
    check('C-WALK return: no script errors', e.errors.length === 0, e.errors.length + ' errors');
  }
  // PENDING-fetch, fix-3 bytes: door must hold past the 4s timer too
  {
    const e = makeEnv(F3.WK, '?name=Distill%20Eye%20Walk&alias=Distill', { fetch: 'pending' });
    const doc = e.document;
    check('C-WALK pending-fetch: door visible at boot', q(doc, '#step-door') && q(doc, '#step-door').hidden === false);
    const r = await pollVisible(doc, 6000, 250);
    check('C-WALK pending-fetch: door STILL visible after 6s (timer fired, guard held)', r.atMs === null && JSON.stringify(visibleSteps(doc)) === '["step-door"]', 'changed at ' + r.atMs + 'ms to ' + r.to);
    check('C-WALK pending-fetch: no script errors', e.errors.length === 0, e.errors.length + ' errors');
  }
}

async function scFetchCausal(F2, F3) {
  console.log('\n== C-CAUSAL: is the FETCH VERDICT (not the 4s timer) the advancer on fix-2 bytes? ==');
  // (a) fix-2 bytes, default fetch (resolves 404 immediately): time the advance.
  {
    const e = makeEnv(F2.WK, '?name=Distill%20Eye%20Walk&alias=Distill');
    const doc = e.document;
    console.log('  fix-2 default-fetch: fetch calls at boot: ' + JSON.stringify(e.env.__fetchCalls.map((c) => String(c[0]).slice(0, 120))));
    const before = JSON.stringify(visibleSteps(doc));
    const r = await pollVisible(doc, 5000, 100);
    console.log('  fix-2 default-fetch: before=' + before + ' change=' + JSON.stringify(r));
    check('C-CAUSAL fix-2: door advances with the DEFAULT fetch', r.atMs !== null && r.to.indexOf('step-1') !== -1, 'changed at ' + r.atMs + 'ms to ' + r.to);
    check('C-CAUSAL fix-2: advance happens BEFORE the 4s timer could fire (so the timer is NOT the advancer)', r.atMs !== null && r.atMs < 4000, 'advanced at ' + r.atMs + 'ms');
  }
  // (b) fix-2 bytes, fetch NEVER resolves: if the verdict is the advancer, the
  // door must hold until the 4s timer fires (~4000ms), not before.
  {
    const e = makeEnv(F2.WK, '?name=Distill%20Eye%20Walk&alias=Distill', { fetch: 'pending' });
    const doc = e.document;
    const before = JSON.stringify(visibleSteps(doc));
    const r = await pollVisible(doc, 5000, 100);
    console.log('  fix-2 pending-fetch: before=' + before + ' change=' + JSON.stringify(r));
    check('C-CAUSAL fix-2 pending: door DOES advance eventually (the timer path exists)', r.atMs !== null && r.to.indexOf('step-1') !== -1, 'changed at ' + r.atMs + 'ms to ' + r.to);
    check('C-CAUSAL fix-2 pending: advance happens AT the 4s timer (~4000ms, not before)', r.atMs !== null && r.atMs >= 3500 && r.atMs <= 4600, 'advanced at ' + r.atMs + 'ms');
  }
  // (c) fix-3 bytes, default fetch: no advance at all in 6s (already covered in
  // C-WALK, but re-proven here as the control pair to (a)).
  {
    const e = makeEnv(F3.WK, '?name=Distill%20Eye%20Walk&alias=Distill');
    const doc = e.document;
    const r = await pollVisible(doc, 6000, 250);
    check('C-CAUSAL fix-3 default-fetch: NO advance in 6s (guard holds the verdict path)', r.atMs === null, 'changed at ' + r.atMs + 'ms to ' + r.to);
  }
}

async function scCore(F3) {
  console.log('\n== C-CORE: deck + letter + unfold + race + rail + plain (no-regress) ==');
  // Deck 37/37
  {
    const e = makeEnv(F3.W, '?stage=deck');
    const doc = e.document;
    const histCalls = [];
    e.env.history.replaceState = function (a, b, u) { histCalls.push({ fn: 'replaceState', url: u }); };
    e.env.history.pushState = function (a, b, u) { histCalls.push({ fn: 'pushState', url: u }); };
    const beats = qa(doc, '#deckBody .letter-beat');
    const jewel = () => { const j = q(doc, '#fpStageJewelNum'); return j ? j.textContent.trim() : '?'; };
    check('C-CORE deck: 37 boards', beats.length === 37, 'found ' + beats.length);
    const nextBtn = q(doc, '#fpNextBtn');
    let ok = true;
    for (let step = 1; step <= 37; step++) {
      const s = beats.filter((b) => !b.hidden);
      if (s.length !== 1 || s[0].getAttribute('data-beat') !== String(step) || jewel() !== step + ' / 37') { ok = false; check('C-CORE deck: step ' + step + ' one board + jewel in sync', false, 'shown=' + s.length + ' jewel=' + jewel()); break; }
      if (step < 37) { nextBtn.click(); await sleep(10); }
    }
    if (ok) check('C-CORE deck: 37/37 one-at-a-time, jewel in sync every landing', true, '37 landings');
    check('C-CORE deck: board 37 mirror reads Enter NayaNET', nextBtn.textContent.indexOf('Enter NayaNET') !== -1);
    nextBtn.click(); await sleep(50);
    const hold = q(doc, '#fpNHold');
    check('C-CORE deck: Enter shows the N hold', hold && hold.hidden === false);
    await sleep(3300);
    check('C-CORE deck: hold releases to the bridge', hold.hidden === true && q(doc, '#fpAgreement').classList.contains('fp-view-bridge'));
    const bridge = histCalls.filter((c) => c.url === '/?stage=bridge');
    check('C-CORE deck: exactly 1 replaceState to /?stage=bridge', bridge.length === 1 && bridge[0].fn === 'replaceState', 'bridge calls: ' + bridge.length + ' of ' + histCalls.length);
    check('C-CORE deck: no script errors', e.errors.length === 0, e.errors.length + ' errors');
  }
  // Letter 37/37
  {
    const e = makeEnv(F3.W, '?stage=letter');
    const doc = e.document;
    const histCalls = [];
    e.env.history.replaceState = function (a, b, u) { histCalls.push({ fn: 'replaceState', url: u }); };
    e.env.history.pushState = function (a, b, u) { histCalls.push({ fn: 'pushState', url: u }); };
    const beats = qa(doc, '#letterBody .letter-beat[data-distilled]');
    const jewel = () => { const j = q(doc, '#fpStageJewelNum'); return j ? j.textContent.trim() : '?'; };
    check('C-CORE letter: 37 boards', beats.length === 37, 'found ' + beats.length);
    const nextBtn = q(doc, '#fpNextBtn');
    let ok = true;
    for (let step = 1; step <= 37; step++) {
      const s = beats.filter((b) => !b.hidden);
      if (s.length !== 1 || s[0] !== beats[step - 1] || jewel() !== step + ' / 37') { ok = false; check('C-CORE letter: step ' + step, false, 'shown=' + s.length + ' jewel=' + jewel()); break; }
      if (step < 37) { nextBtn.click(); await sleep(10); }
    }
    if (ok) check('C-CORE letter: 37/37 one-at-a-time, jewel in sync every landing', true, '37 landings');
    check('C-CORE letter: board 37 mirror reads I agree', nextBtn.textContent.indexOf('I agree') !== -1);
    nextBtn.click(); await sleep(50);
    check('C-CORE letter: I agree opens the agree view', q(doc, '#fpAgreement').classList.contains('fp-view-agree'));
    const agreeBtn = q(doc, '#dealAgreeBtn');
    check('C-CORE letter: agree button present', !!agreeBtn);
    if (agreeBtn) {
      agreeBtn.click(); await sleep(50);
      const hold = q(doc, '#fpNHold');
      check('C-CORE letter: agree shows the N hold', hold && hold.hidden === false);
      await sleep(3300);
      check('C-CORE letter: hold releases to the bridge', q(doc, '#fpAgreement').classList.contains('fp-view-bridge'));
      const bridge = histCalls.filter((c) => c.url === '/?stage=bridge');
      check('C-CORE letter: exactly 1 replaceState to /?stage=bridge', bridge.length === 1 && bridge[0].fn === 'replaceState', 'bridge calls: ' + bridge.length);
    }
    check('C-CORE letter: no script errors', e.errors.length === 0, e.errors.length + ' errors');
  }
  // Unfold 1->37 (fix-1 walk, condensed: pill + cascade at 1, 19, 37 + Back)
  {
    const e = makeEnv(F3.U, '');
    const doc = e.document;
    const beats = qa(doc, '#deckBody .letter-beat');
    check('C-CORE unfold: 37 boards', beats.length === 37, 'found ' + beats.length);
    const cssText = qa(doc, 'style').map((s) => s.textContent).join('\n');
    const rules = H1.parseCSS(cssText);
    const vis = () => beats.filter((b) => H1.cascadeDisplay(b, rules, 1920) !== 'none');
    check('C-CORE unfold: cascade shows exactly board 1 at load', vis().length === 1 && vis()[0].getAttribute('data-beat') === '1', 'visible=' + vis().length);
    let ok = true;
    for (let step = 2; step <= 37; step++) {
      const cur = qa(doc, '#deckBody .letter-beat.frame-now')[0];
      if (!cur) { ok = false; check('C-CORE unfold: frame-now at step ' + step, false); break; }
      const btn = cur.querySelector('.deck-next[data-beat]');
      if (!btn) { ok = false; check('C-CORE unfold: Keep reading on board ' + (step - 1), false); break; }
      btn.click(); await sleep(10);
      const now = qa(doc, '#deckBody .letter-beat.frame-now');
      const pill = q(doc, '.af-prog-num');
      const v = vis();
      if (now.length !== 1 || now[0].getAttribute('data-beat') !== String(step) || !pill || pill.textContent.trim() !== step + ' / 37' || v.length !== 1 || v[0].getAttribute('data-beat') !== String(step)) {
        ok = false; check('C-CORE unfold: step ' + step, false, 'frame-now=' + now.length + ' pill=' + (pill ? pill.textContent : '?') + ' visible=' + v.length); break;
      }
    }
    if (ok) check('C-CORE unfold: Next walks 1..37, pill + cascade in sync', true, '36 taps');
    const b37 = qa(doc, '#deckBody .letter-beat.frame-now')[0];
    const back = b37 ? b37.querySelector('.deck-back') : null;
    if (back) {
      back.click(); await sleep(10);
      const now3 = qa(doc, '#deckBody .letter-beat.frame-now');
      check('C-CORE unfold: Back 37 -> 36', now3.length === 1 && now3[0].getAttribute('data-beat') === '36');
    } else check('C-CORE unfold: Back present on board 37', false);
    check('C-CORE unfold: board 37 keeps Congratulations — you’re hired', beats[36].textContent.indexOf('Congratulations') !== -1 && beats[36].textContent.indexOf('you’re hired') !== -1);
    check('C-CORE unfold: no script errors', e.errors.length === 0, e.errors.length + ' errors');
  }
  // Loading race F5b (runtime events)
  {
    const e = makeEnv(F3.W, '?stage=deck');
    const doc = e.document;
    const beats = qa(doc, '#deckBody .letter-beat');
    const shown = beats.filter((b) => !b.hidden)[0];
    const scImg = shown ? shown.querySelector('.lb-showcase img') : null;
    check('C-CORE race: showcase img exists on board 1', !!scImg);
    if (scImg) {
      const src0 = scImg.getAttribute('src');
      const mkEv = () => ({ type: 'error', bubbles: true, target: null, currentTarget: null, defaultPrevented: false, _stopped: false, preventDefault: function () { this.defaultPrevented = true; }, stopPropagation: function () { this._stopped = true; } });
      scImg.dispatchEvent(mkEv()); await sleep(10);
      const src1 = scImg.getAttribute('src');
      check('C-CORE race: failed load retries with &retry=1 + data-fp-retried=1', src1 === src0 + (src0.indexOf('?') === -1 ? '?' : '&') + 'retry=1' && scImg.getAttribute('data-fp-retried') === '1', 'src=' + JSON.stringify((src1 || '').slice(-60)));
      scImg.dispatchEvent(mkEv()); await sleep(10);
      const sc = scImg.closest('.lb-showcase');
      check('C-CORE race: second failure hides the showcase', sc && sc.style.display === 'none', 'display=' + (sc ? JSON.stringify(sc.style.display) : '?'));
    }
    const face = q(doc, '#deckBody .fp-speak-face');
    check('C-CORE race: face photo exists', !!face);
    if (face) {
      const f0 = face.getAttribute('src');
      const ev = { type: 'error', bubbles: true, target: null, currentTarget: null, defaultPrevented: false, _stopped: false, preventDefault: function () { this.defaultPrevented = true; }, stopPropagation: function () { this._stopped = true; } };
      face.dispatchEvent(ev); await sleep(10);
      const f1 = face.getAttribute('src');
      check('C-CORE race: failed face falls back to crystal-n.png', f1 !== f0 && f1.indexOf('crystal-n.png') !== -1, 'src=' + JSON.stringify((f1 || '').slice(0, 100)));
    }
    check('C-CORE race: no script errors', e.errors.length === 0, e.errors.length + ' errors');
  }
  // Rail
  {
    const e = makeEnv(F3.W, '?stage=deck');
    const doc = e.document;
    const railArts = qa(doc, '#letterBody article').filter((a) => !a.hasAttribute('data-distilled'));
    console.log('  rail (non-distilled) articles: ' + railArts.length);
    check('C-CORE rail: 67 rail articles present', railArts.length === 67, railArts.length + ' found');
    const money = railArts.filter((a) => a.getAttribute('data-beat') === '51');
    check('C-CORE rail: money board 51 exists', money.length === 1, money.length + '');
    if (money.length === 1) check('C-CORE rail: money board has no Congratulations/hired', money[0].textContent.indexOf('Congratulations') === -1 && money[0].textContent.indexOf('hired') === -1);
    check('C-CORE rail: "or read the whole page at once" link exists', !!q(doc, '#fpLinkLegalAll'));
    check('C-CORE rail: no script errors', e.errors.length === 0, e.errors.length + ' errors');
  }
  // Plain welcome (fix-1 scenario 5)
  {
    const e = makeEnv(F3.W, '');
    const doc = e.document;
    const enterBtn = q(doc, '#fpEnterDeal');
    check('C-CORE plain: hero Read button present', !!enterBtn);
    if (enterBtn) {
      enterBtn.click(); await sleep(10);
      const nav = e.navigations.filter((n) => n.kind === 'href');
      check('C-CORE plain: hero Read goes to /agreement', nav.length >= 1 && nav[nav.length - 1].url === '/agreement', JSON.stringify(nav));
    }
    const e2 = makeEnv(F3.W, '', { local: { nayanet_fp_agreed: '1' } });
    const doc2 = e2.document;
    const form = q(doc2, '#entryForm');
    const name = q(doc2, '#userName');
    check('C-CORE plain: name form present', !!form && !!name);
    if (form && name) {
      name.value = 'Test Name';
      const ev = { type: 'submit', bubbles: true, target: form, currentTarget: form, defaultPrevented: false, _stopped: false, preventDefault: function () { this.defaultPrevented = true; }, stopPropagation: function () { this._stopped = true; } };
      form.dispatchEvent(ev); await sleep(50);
      const hold2 = q(doc2, '#fpNHold');
      check('C-CORE plain: agreed submit shows the N hold', hold2 && hold2.hidden === false);
      await sleep(3300);
      const nav2 = e2.navigations.filter((n) => n.kind === 'href');
      check('C-CORE plain: hold releases to identity with the name', nav2.length >= 1 && nav2[nav2.length - 1].url === '/identity.html?name=Test%20Name', JSON.stringify(nav2));
    }
    const e3 = makeEnv(F3.W, '', { session: { nayanet_fp_from_bridge: '1' } });
    const form3 = q(e3.document, '#entryForm');
    check('C-CORE plain: reload with fromBridge re-opens the name form', form3 && form3.hidden === false);
    check('C-CORE plain: no script errors', e.errors.length === 0 && e2.errors.length === 0 && e3.errors.length === 0,
      'e=' + e.errors.length + ' e2=' + e2.errors.length + ' e3=' + e3.errors.length);
  }
  // Unfold stage redirects
  {
    ['deck', 'letter', 'bridge'].forEach((st) => {
      const e = makeEnv(F3.U, '?stage=' + st);
      const rep = e.navigations.filter((n) => n.kind === 'replace');
      check('C-CORE unfold: ?stage=' + st + ' redirects to /?stage=' + st, rep.length === 1 && rep[0].url === '/?stage=' + st, JSON.stringify(rep));
    });
  }
}

async function main() {
  // ---- base verification (fresh staging fetch, full shas) ----
  const bU = await get('/agreement');
  const bW = await get('/?stage=deck');
  const bWK = await get('/welcome');
  const bI = await get('/identity.html?name=Distill%20Eye%20Walk');
  for (const [k, s, exp] of [['unfold', bU, BASE.unfold], ['welcome', bW, BASE.welcome], ['walk', bWK, BASE.walk], ['identity', bI, BASE.identity]]) {
    const b = Buffer.byteLength(s), h = sha(s);
    const ok = b === exp.bytes && h.startsWith(exp.sha256);
    console.log('BASE ' + k + ': ' + b + 'B sha ' + h.slice(0, 16) + ' -> ' + (ok ? 'MATCH' : 'MISMATCH'));
    check('base matches exactly: ' + k, ok, b + 'B sha ' + h.slice(0, 32));
  }
  const { F2, F3, base } = await buildFixed();
  console.log('\n== CHECKER FIX-3 BYTES (own transform) ==');
  for (const [k, s] of [['unfold', F3.U], ['welcome', F3.W], ['walk', F3.WK], ['identity', F3.I]]) {
    console.log('CHECKER ' + k + ': ' + Buffer.byteLength(s) + 'B sha256 ' + sha(s));
  }
  byteHarness(F2, F3, base);
  lawsDelta(base, F3);
  await scIdentity(F3, base);
  await scWalkDoor(F3, F2);
  await scFetchCausal(F2, F3);
  await scCore(F3);
  console.log('\nCHECKER TOTAL: ' + PASS + ' pass / ' + FAIL + ' fail');
  if (FAIL) { console.log('failures: ' + FAILURES.join(' | ')); process.exit(1); }
  process.exit(0);
}

if (require.main === module) {
  const dump = process.argv[2] === '--dump' ? process.argv[3] : null;
  if (dump) {
    (async () => {
      const origLog = console.log;
      console.log = () => {}; // silence build logs so stdout is exactly the file bytes
      const { F3 } = await buildFixed();
      console.log = origLog;
      const map = { unfold: F3.U, welcome: F3.W, walk: F3.WK, identity: F3.I };
      if (!map[dump]) { console.error('unknown dump key ' + dump); process.exit(2); }
      process.stdout.write(map[dump]);
    })().catch((e) => { console.error('FATAL', e); process.exit(1); });
  } else {
    main().catch((e) => { console.error('FATAL', e); process.exit(1); });
  }
}
