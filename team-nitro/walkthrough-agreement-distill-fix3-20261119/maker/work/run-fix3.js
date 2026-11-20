#!/usr/bin/env node
// run-fix3.js — agreement distill fix-3: re-run the fix-2 transform (verify §1 shas),
// apply the three F9 remedies, then prove by bytes + the FULL state machine
// (checker's 53 + fix-1 unfold walk + fix-1 scenario 5).
// Default: everything in memory, results to stdout. Deterministic.
// --emit writes the four fixed files to their round dirs (see emitFixed).
const https = require('https');
const crypto = require('crypto');
const vm = require('vm');
const fs = require('fs');
const runFix2 = require('./run-fix2-export.js');
const H1 = require('./dom-harness3-dom.js'); // checker copy of the fix-1 DOM (fixed *= selectors)
const makeEnv = H1.makeEnv, q = H1.q, qa = H1.qa, sleep = H1.sleep;
const parseCSS = H1.parseCSS, cascadeDisplay = H1.cascadeDisplay;

const STAGE = 'naya-walk-beginning-staging.nayapower.workers.dev';
const FIX2 = {
  unfold: { bytes: 142120, sha256: '50876fff8caa79eeb3d6d75b4d2099db39ade2688edf6762e58ac9083eb0d26b' },
  welcome: { bytes: 1929575, sha256: '3874b7ebcc6b95e2a7ef2d320ed95e13253083a954fe6c0efc36afe6d58fa747' },
  walk: { bytes: 4362221, sha256: '854a8f60328afca94e9856d660d02e897c4a777e0e5be4a9dcaaebc998283244' },
  identity: { bytes: 402166, sha256: 'd0f26529513ba25eb6614098f369583393345d5ee02ec4bc914c0d49085c0513' },
};
const FIXED3 = {
  unfold: { bytes: 142120, sha256: '50876fff8caa79eeb3d6d75b4d2099db39ade2688edf6762e58ac9083eb0d26b' },
  welcome: { bytes: 1929575, sha256: '3874b7ebcc6b95e2a7ef2d320ed95e13253083a954fe6c0efc36afe6d58fa747' },
  walk: { bytes: 4363264, sha256: 'ef98226767ddbb507b7e8282a64c72e4c741b3bf0b38413985484798dbc7464f' },
  identity: { bytes: 402647, sha256: '51776174b59cee4a39f7a00eb7f7b874fc33103a0235308a876d4a94179307f5' },
};
const BASESHA = {
  unfold: '5fe1a3ec2231c128774c6eb00736913d93117d3eaa06278e2a16183cdebee6ab',
  welcome: 'c3c750b72a2b0330d15de8831e9b24719116991e6c0df9dbc5d329834fbbaed5',
  walk: '0f05b3f96ce8edd0ecb094c0f64972098f788c3943e22b5446c8bb60e9b0e2fd',
  identity: '3279dc3572337e5e',
};
// STALE DISK SHAs (proven 2026-11-20 ~07:00Z, diff-base-disk.js + check-base-equiv.js):
// the unfold + welcome files on disk are OLDER divergent copies, not the live base:
// every mechanism in them exists in base (currentBeatEl 7x, fp-smart-visual 22x,
// deck-end flag 4x in base-welcome); their unique lines are older board-markup
// variants plus deliberately-removed content ("Nine pictures" 1x, "1 / 86" 1x,
// the extra fpLinkLetterAll button — the captain's settled do-NOT-restore).
// Live staging serves the base, so overwriting them loses nothing live — but
// only ever with a verified verbatim backup beside the original first.
const STALESHA = {
  unfold: '4a2e84b0104bf404b3e576ea91725cf0cd931688ff84837cc8ae177e2d952fb9',
  welcome: '1f37416d79b0959b21dffb450d34e1a409dfe934fac40a144ecf0b0ef9f7cc49',
};
const BACKUP_SUFFIX = '.stale-20261120.bak';
// --emit targets: the round dirs the build script reads from. The emit writes
// tmp-in-same-dir, verifies size+sha, renames ONLY on verify-pass, then
// re-reads the target and verifies again. A disk file that matches neither
// the base, the known stale sha (with a verified backup), nor the fixed sha
// aborts the emit untouched; a file that already matches the fixed sha is
// skipped (idempotent re-run). Writes poll gently (one attempt, 20s wait,
// repeat to a shared 20-min deadline): instant writes land, hammering never
// does. Re-run --emit-only fresh to retry; progress accumulates.
const EMIT_TARGETS = {
  unfold: '/home/hatch/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html',
  welcome: '/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/welcome-staged.html',
  walk: '/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html',
  identity: '/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/identity-fixed.html',
};
// writeRetry: the EPERM flake opens for seconds at a time — attempt the write
// every 100ms until it lands whole (verified by size+sha) or attempts run out.
// Returns true only on a verified write. Cleans up partial files per attempt.
let EMIT_DEADLINE = 0;
async function writeRetry(path, content) {
  // GENTLE polling against the EPERM flake. The evidence this session:
  // instant writes in a fresh process land; sustained tight retry loops never
  // do (300 attempts/30s and 1800 attempts/3min both failed outright) —
  // hammering may itself hold the window shut. So: one attempt, then wait
  // 20s, repeat until the shared emit deadline. The real write is its own
  // probe (verify confirms); no scratch writes. True only on verified write.
  const wantBytes = Buffer.byteLength(content), wantSha = sha(content);
  for (;;) {
    try {
      fs.writeFileSync(path, content, 'utf8');
      const back = fs.readFileSync(path, 'utf8');
      if (Buffer.byteLength(back) === wantBytes && sha(back) === wantSha) return true;
      console.log('writeRetry: ' + path + ' wrote but verify failed (got ' + Buffer.byteLength(back) + 'B) — retrying in 20s');
    } catch (e) { console.log('writeRetry: ' + path + ' failed: ' + (e && e.code || e) + ' — retrying in 20s'); }
    try { fs.unlinkSync(path); } catch (e2) {}
    if (Date.now() >= EMIT_DEADLINE) return false;
    await sleep(20000);
    if (Date.now() >= EMIT_DEADLINE) return false;
  }
}
async function emitFixed(F) {
  EMIT_DEADLINE = Date.now() + 20 * 60 * 1000; // gentle polling budget for the whole emit
  console.log('\n== EMIT (--emit): write the four fixed files to their round dirs ==');
  for (const [k, s] of [['unfold', F.unfold], ['welcome', F.welcome], ['walk', F.walk], ['identity', F.identity]]) {
    const target = EMIT_TARGETS[k];
    const fixedSha = sha(s), fixedBytes = Buffer.byteLength(s);
    let cur = null;
    try { cur = fs.readFileSync(target, 'utf8'); } catch (e) { console.log('EMIT ' + k + ': cannot read current disk file: ' + e.message); process.exit(2); }
    const curSha = sha(cur);
    if (curSha === fixedSha) { console.log('EMIT ' + k + ': already the fixed bytes on disk (' + fixedBytes + 'B sha ' + fixedSha.slice(0, 16) + '); skipping'); continue; }
    let state = null;
    if (curSha.startsWith(BASESHA[k])) state = 'base';
    else if (STALESHA[k] && curSha === STALESHA[k]) state = 'stale';
    else { console.log('EMIT ' + k + ': ABORT — disk file is neither base, known-stale, nor fixed (sha ' + curSha.slice(0, 16) + ', expect base ' + BASESHA[k].slice(0, 8) + '); leaving it untouched'); process.exit(2); }
    if (state === 'stale') {
      // Never overwrite the stale bytes without a verified verbatim backup.
      const bak = target + BACKUP_SUFFIX;
      let bakOk = false;
      try { const b = fs.readFileSync(bak, 'utf8'); bakOk = (sha(b) === curSha); } catch (e) { bakOk = false; }
      if (bakOk) console.log('EMIT ' + k + ': verified backup already present (' + bak + ')');
      else {
        console.log('EMIT ' + k + ': stale disk file (' + Buffer.byteLength(cur) + 'B sha ' + curSha.slice(0, 16) + ') — writing verified backup first');
        if (!await writeRetry(bak, cur)) { console.log('EMIT ' + k + ': BACKUP FAILED — leaving the live file untouched'); process.exit(2); }
        console.log('EMIT ' + k + ': backup written and verified (' + bak + ')');
      }
    }
    console.log('EMIT ' + k + ': disk file is the ' + state + ' (' + Buffer.byteLength(cur) + 'B sha ' + curSha.slice(0, 16) + '); writing fixed ' + fixedBytes + 'B sha ' + fixedSha.slice(0, 16));
    const tmp = target + '.fix3tmp';
    if (!await writeRetry(tmp, s)) { console.log('EMIT ' + k + ': WRITE FAILED after retries — leaving the live file untouched'); try { fs.unlinkSync(tmp); } catch (e2) {} process.exit(2); }
    const back = fs.readFileSync(tmp, 'utf8');
    if (Buffer.byteLength(back) !== fixedBytes || sha(back) !== fixedSha) { console.log('EMIT ' + k + ': VERIFY FAILED — tmp size/sha mismatch (got ' + Buffer.byteLength(back) + 'B sha ' + sha(back).slice(0, 16) + '); NOT replacing the live file'); try { fs.unlinkSync(tmp); } catch (e2) {} process.exit(2); }
    fs.renameSync(tmp, target);
    const after = fs.readFileSync(target, 'utf8');
    if (Buffer.byteLength(after) !== fixedBytes || sha(after) !== fixedSha) { console.log('EMIT ' + k + ': POST-RENAME VERIFY FAILED — target mismatch after rename'); process.exit(2); }
    console.log('EMIT ' + k + ': OK — ' + target + ' now ' + fixedBytes + 'B sha256 ' + fixedSha);
  }
  console.log('EMIT: all four files on disk and verified by size + sha256');
}
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
function rep1(s, needle, repl, label) {
  const n = count(s, needle);
  if (n !== 1) throw new Error('REP ' + label + ': found ' + n + ', expected 1 :: ' + JSON.stringify(needle.slice(0, 100)));
  console.log('REP ' + label + ': 1x');
  return s.split(needle).join(repl);
}

// ---- laws replication (verbatim regexes/sets from check-design-laws.py, as in run-fix2.js) ----
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
      if (rx.test(line)) { fails.push(name + ':' + (idx + 1) + ': GRAY: ' + line.trim().slice(0, 120)); break; }
    }
  });
  let m;
  while ((m = FONTSIZE_RE.exec(text)) !== null) {
    const vals = [m[1], m[2]].filter((v) => v != null).map(Number);
    if (vals.length && Math.min(...vals) < 17) {
      const ln = text.slice(0, m.index).split('\n').length;
      fails.push(name + ':' + ln + ': SIZE below 17px: ' + m[0]);
    }
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
function normSet(list) {
  // strip line numbers so insertion shifts cannot masquerade as new violations
  return new Set(list.map((x) => x.replace(/^[^:]+:\d+:/, '')));
}

async function main() {
  // ---- 1. re-run fix-2, verify §1 shas ----
  const R = await runFix2();
  let U = R.U, W = R.W, WK = R.WK, I = R.I;
  for (const [k, s, exp] of [['unfold', U, FIX2.unfold], ['welcome', W, FIX2.welcome], ['walk', WK, FIX2.walk], ['identity', I, FIX2.identity]]) {
    const b = Buffer.byteLength(s), h = sha(s);
    const ok = b === exp.bytes && h === exp.sha256;
    console.log('FIX2 ' + k + ': ' + b + 'B sha ' + h.slice(0, 16) + ' -> ' + (ok ? 'MATCH §1' : 'MISMATCH'));
    if (!ok) throw new Error('fix-2 base mismatch: ' + k);
  }
  // ---- fetch base for the laws delta ----
  const U0 = await get('/agreement');
  const W0 = await get('/?stage=deck');
  const WK0 = await get('/welcome');
  const I0 = await get('/identity.html?name=Distill%20Eye%20Walk');
  for (const [k, s, exp] of [['unfold', U0, BASESHA.unfold], ['welcome', W0, BASESHA.welcome], ['walk', WK0, BASESHA.walk], ['identity', I0, BASESHA.identity]]) {
    const h = sha(s);
    console.log('BASE ' + k + ': ' + Buffer.byteLength(s) + 'B sha ' + h.slice(0, 16) + ' -> ' + (h.startsWith(exp) ? 'MATCH' : 'MISMATCH'));
    if (!h.startsWith(exp)) throw new Error('base mismatch: ' + k);
  }

  // ================= FIX-3 TRANSFORMS =================
  // I-FIX3 — F9(a) input + echo. The FIX2 pre-fill sits BEFORE the FIX3 clear
  // (aliasInput.value = '') and before the load-time paint (updateSmartCredentials
  // paints the hero from the empty field), so it is wiped twice. The operative
  // fix paints AFTER the load-time paint, and only for the PAIRED case
  // (?name= AND ?alias= together — the same rule currentDisplayName trusts:
  // the passed name counts only with its paired alias). Un-paired: FIX3's
  // never-pre-paint rule stands — field stays empty, hero stays hidden.
  const I_ANCHOR = "      paintValues(currentAlias + '.nayanet.app', currentAlias, false);\n      if (linesEl) linesEl.hidden = false;\n    }\n\n    updateSmartCredentials();";
  const I_FIX3 = "\n    /* FIX3 (distill fix-3, F9a) — paired identity from the walk: name+alias together ARE the user's identity (the rule currentDisplayName already trusts). Pre-fill the alias field with the paired alias and paint the hero with the paired name, AFTER the load-time paint and AFTER the FIX3 clear. Un-paired: never pre-paint — the clear stands. */\n    try{ if (passedName && passedAlias) { if (aliasInput) aliasInput.value = passedAlias; paintHeroName(passedName); } }catch(e){}";
  I = rep1(I, I_ANCHOR, I_ANCHOR + I_FIX3, 'I-FIX3 paired pre-fill + hero paint after load paint');

  // W-FIX3a — F9(b): guard proceed() while the door is visible. The door is the
  // gate: no timer, no claim verdict, no resume advances the walk while it is
  // visible. Only the user's own action on the door (the certificate link or
  // the explicit continue) dismisses it. proceed() is the single funnel for every advance leg
  // (4s timer, fetch verdict, fetch catch, no-alias boot), so one guard
  // covers all of them. (No-alias boot calls proceed() only to showDoor(),
  // which is the same visible outcome.)
  const P_ANCHOR = "  var proceed = function(){\n  if (!ID.alias) { showDoor(); return; }";
  const P_GUARD = "  var proceed = function(){\n  /* FIX3 (distill fix-3, F9b) — the door is the gate: while #step-door is visible, NOTHING advances the walk. Only the user's own action on the door (the certificate link or the explicit continue) dismisses it, never a timer. */\n  if (document.getElementById('step-door') && !document.getElementById('step-door').hidden) return;\n  if (!ID.alias) { showDoor(); return; }";
  WK = rep1(WK, P_ANCHOR, P_GUARD, 'W-FIX3a proceed() door guard');

  // W-FIX3b — F9(b): guard the claim-gate timer itself (the timer that actually
  // advances the walk). While the door is visible the timer does not consume
  // the gate and does not proceed — it simply does not advance.
  const T_ANCHOR = "var gateTimer6 = setTimeout(function(){ if (!gateDone6) { gateDone6 = true; proceed(); } }, 4000);";
  const T_GUARD = "var gateTimer6 = setTimeout(function(){ if (document.getElementById('step-door') && !document.getElementById('step-door').hidden) return; if (!gateDone6) { gateDone6 = true; proceed(); } }, 4000);";
  WK = rep1(WK, T_ANCHOR, T_GUARD, 'W-FIX3b claim-gate timer door guard');

  // W-FIX3c — F9(b): the door's explicit continue. The guard alone would leave
  // a certified citizen with no way forward: the door's only control was the
  // certificate link (which navigates AWAY to identity), and identity's
  // "Back to the walk" returns to /welcome, where the door shows again —
  // a door <-> certificate loop with the questionnaire unreachable. The brief
  // orders a user action that DISMISSES the door ("the certificate link or
  // an explicit continue"), so the door gets the explicit continue: the same
  // .p3-enter pill as its sibling link (same family, stacked vertically),
  // wired in-script to the existing proceed(). No timer anywhere.
  const D_ANCHOR = '<a class="p3-enter" href="/identity.html" style="text-decoration:none">Get your certificate ◆</a>';
  const D_CONT = D_ANCHOR + '\n<button type="button" class="p3-enter" id="doorContinue" style="font-family:inherit">Continue to the walk ◆</button>';
  WK = rep1(WK, D_ANCHOR, D_CONT, 'W-FIX3c door explicit-continue button');

  // W-FIX3d — wire the continue inside the boot IIFE, where proceed() is in
  // scope: hide the door first (so proceed()'s own guard passes), then
  // proceed() opens the walk from its normal resume logic. Without a
  // certificate (no alias) the continue stays hidden — the walk opens after
  // the certificate, so the certificate link is the only way forward there.
  const W_ANCHOR = "  if (!ID.alias) { proceed(); return; }";
  const W_WIRE = "  /* FIX3 (distill fix-3, F9b) — the door's explicit continue: a certified citizen dismisses the door by tapping Continue; the door hides, then proceed() opens the walk. No alias, no continue — the walk opens after the certificate. */\n  (function(){ var c = document.getElementById('doorContinue'); if (!c) return; if (!ID.alias) { c.hidden = true; return; } c.addEventListener('click', function(){ var d = document.getElementById('step-door'); if (d) d.hidden = true; proceed(); }); })();\n" + W_ANCHOR;
  WK = rep1(WK, W_ANCHOR, W_WIRE, 'W-FIX3d door continue wiring');

  // ---- fixed sizes + shas ----
  for (const [k, s] of [['unfold', U], ['welcome', W], ['walk', WK], ['identity', I]]) {
    console.log('FIXED3 ' + k + ': ' + Buffer.byteLength(s) + 'B sha256 ' + sha(s));
  }

  // ---- byte harness (fix-3 + no-regress spot checks) ----
  console.log('\n== BYTE HARNESS ==');
  check('I3a FIX3 paired block present 1x', count(I, 'FIX3 (distill fix-3, F9a)') === 1);
  check('I3b paired condition (name AND alias)', count(I, 'if (passedName && passedAlias)') === 1);
  check('I3c FIX2 insertion still present (history, harmless)', count(I, '_fxAlias') >= 1 && count(I, "urlParams.get('alias')") >= 1);
  check('I3d FIX3 clear still present (un-paired rule stands)', count(I, "aliasInput.value = ''") === 2, count(I, "aliasInput.value = ''") + 'x (boot clear + switchToDifferentAlias)');
  check('W3a proceed() door guard present 1x', count(WK, "FIX3 (distill fix-3, F9b) — the door is the gate:") === 1);
  check('W3b claim-gate timer guarded 1x', count(WK, T_GUARD) === 1);
  check('W3c unguarded claim-gate timer gone', count(WK, T_ANCHOR) === 0);
  check('W3d fix-2 K3 door guards still 2x', count(WK, "if(document.getElementById('step-door')&&!document.getElementById('step-door').hidden)return;") === 2);
  check('W3e door cert-link name carrier still present', WK.includes('/identity.html?name=') && WK.includes('nayanet_user_name'));
  check('W3f door explicit-continue button present 1x', count(WK, 'id="doorContinue"') === 1 && WK.includes('Continue to the walk ◆'));
  check('W3g door continue wiring present 1x', count(WK, "FIX3 (distill fix-3, F9b) — the door's explicit continue") === 1);
  check('W3h door cert link still exactly 1x (not duplicated by the continue)', count(WK, 'Get your certificate ◆</a>') === 1);
  check('F10 bridge replaceState still exactly 1x', count(W, "history.replaceState(null,'','/?stage=bridge')") === 1);
  check('ruling(a) money-board sentence still cut', count(W, 'hired!') === 0);
  check('F7 deck seals still 37x', count(W, '&middot; The Deck<div class="deal-seal') === 37);
  check('F7 letter+rail seals still >=37x', count(W, '&middot; The Collective Agreement<div class="deal-seal') >= 37, count(W, '&middot; The Collective Agreement<div class="deal-seal') + 'x');
  check('ruling(b) board22 title still plain', count(W, 'How collective chain technology works') === 0 && count(U, 'How collective chain technology works') === 0 && W.includes('How it all connects') && U.includes('How it all connects'));
  check('ruling(c) images unchanged (slide-1.jpg present)', W.includes('slide-1.jpg'));
  check('F8 Nine pictures still 0x everywhere', count(W, 'Nine pictures') + count(U, 'Nine pictures') + count(WK, 'Nine pictures') + count(I, 'Nine pictures') === 0);
  check('F6 board-2 phrase still 0x', count(W, 'One network, many people, many minds') === 0 && count(U, 'One network, many people, many minds') === 0);
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
  for (const [k, s] of [['unfold', U], ['welcome', W], ['walk', WK], ['identity', I]]) {
    const r = syntaxCheck(k, s);
    check('syntax: ' + k + ' script blocks parse', r.bad === 0, r.n + ' blocks, ' + r.bad + ' failures');
  }
  // laws delta on all four files
  console.log('\n== LAWS DELTA (replication; real checker needs disk files) ==');
  for (const [k, base, fixed] of [['unfold', U0, U], ['welcome', W0, W], ['walk', WK0, WK], ['identity', I0, I]]) {
    const b = lawsCheck(k + ' base', base), f = lawsCheck(k + ' fixed', fixed);
    const bn = normSet(b.fails), fn = normSet(f.fails);
    let added = 0, removed = 0;
    fn.forEach((x) => { if (!bn.has(x)) added++; });
    bn.forEach((x) => { if (!fn.has(x)) removed++; });
    console.log('LAWS ' + k + ': base ' + b.fails.length + ' FAIL / ' + b.warns.length + ' WARN -> fixed ' + f.fails.length + ' FAIL / ' + f.warns.length + ' WARN (normalized +' + added + ' / -' + removed + ')');
    check('laws: ' + k + ' delta 0/0 (normalized)', added === 0 && removed === 0 && f.fails.length === b.fails.length && f.warns.length === b.warns.length,
      'base ' + b.fails.length + '/' + b.warns.length + ' fixed ' + f.fails.length + '/' + f.warns.length);
  }

  const F = { unfold: U, welcome: W, walk: WK, identity: I };
  if (process.argv.includes('--emit-only')) {
    // Skip the state machine (already proven 139/0 on these exact bytes, twice,
    // on this script); the byte harness + laws delta above already re-ran.
    // Verify the derived bytes are the recorded FIXED3 bytes, then emit.
    for (const [k, s, exp] of [['unfold', U, FIXED3.unfold], ['welcome', W, FIXED3.welcome], ['walk', WK, FIXED3.walk], ['identity', I, FIXED3.identity]]) {
      const b = Buffer.byteLength(s), h = sha(s);
      const ok = b === exp.bytes && h === exp.sha256;
      console.log('FIXED3-VERIFY ' + k + ': ' + b + 'B sha ' + h.slice(0, 16) + ' -> ' + (ok ? 'MATCH' : 'MISMATCH'));
      if (!ok) throw new Error('fix-3 bytes mismatch: ' + k);
    }
    await emitFixed(F);
    process.exit(0);
  }
  await runStateMachine(F);
  console.log('\nTOTAL: ' + PASS + ' pass / ' + FAIL + ' fail');
  if (FAIL) { console.log('failures: ' + FAILURES.join(' | ')); process.exit(1); }
  if (process.argv.includes('--emit')) await emitFixed(F);
  process.exit(0); // else the harness envs' live intervals (identity clock etc.) keep the loop open
}

// ================= STATE MACHINE (full: checker's 53 + fix-1 unfold walk + scenario 5) =================
function jewelText(doc) { var j = q(doc, '#fpStageJewelNum'); return j ? j.textContent.trim() : '?'; }

async function scenarioUnfold(F) {
  console.log('\n== S1: /agreement unfold walk (fix-1, re-run in full) ==');
  var e = makeEnv(F.unfold, '');
  var doc = e.document;
  console.log('  scripts run: ' + e.scriptsRun + ', script errors: ' + e.errors.length);
  e.errors.slice(0, 3).forEach(function (er) { console.log('  script-error: ' + JSON.stringify(er).slice(0, 300)); });
  var beats = qa(doc, '#deckBody .letter-beat');
  check('unfold: 37 boards', beats.length === 37, 'found ' + beats.length);
  var now = beats.filter(function (b) { return b.classList.contains('frame-now'); });
  check('unfold: exactly one frame-now at load', now.length === 1, 'found ' + now.length);
  check('unfold: first board is current', now.length === 1 && now[0].getAttribute('data-beat') === '1');
  var pill = q(doc, '.af-prog-num');
  check('unfold: pill reads 1 / 37', pill && pill.textContent.trim() === '1 / 37', pill ? JSON.stringify(pill.textContent) : 'no pill');
  var cssText = qa(doc, 'style').map(function (s) { return s.textContent; }).join('\n');
  var rules = parseCSS(cssText);
  function visibleBeats() { return beats.filter(function (b) { return cascadeDisplay(b, rules, 1920) !== 'none'; }); }
  var vis = visibleBeats();
  check('unfold: cascade shows exactly one board', vis.length === 1, 'visible=' + vis.length);
  check('unfold: cascade shows board 1', vis.length === 1 && vis[0].getAttribute('data-beat') === '1');
  check('unfold: cascade hides board 2', cascadeDisplay(beats[1], rules, 1920) === 'none', 'board2=' + cascadeDisplay(beats[1], rules, 1920));
  var ok = true;
  for (var step = 2; step <= 37; step++) {
    var cur = qa(doc, '#deckBody .letter-beat.frame-now')[0];
    if (!cur) { ok = false; check('unfold: frame-now present at step ' + step, false); break; }
    var btn = cur.querySelector('.deck-next[data-beat]');
    if (!btn) { ok = false; check('unfold: Keep reading present on board ' + (step - 1), false, 'no .deck-next'); break; }
    btn.click();
    await sleep(10);
    var now2 = qa(doc, '#deckBody .letter-beat.frame-now');
    var pill2 = q(doc, '.af-prog-num');
    if (now2.length !== 1 || now2[0].getAttribute('data-beat') !== String(step) || !pill2 || pill2.textContent.trim() !== step + ' / 37') {
      ok = false;
      check('unfold: step ' + step, false, 'frame-now=' + now2.length + ' beat=' + (now2[0] ? now2[0].getAttribute('data-beat') : '?') + ' pill=' + (pill2 ? pill2.textContent : '?'));
      break;
    }
    var v = visibleBeats();
    if (v.length !== 1 || v[0].getAttribute('data-beat') !== String(step)) {
      ok = false; check('unfold: cascade at step ' + step, false, 'visible=' + v.length); break;
    }
  }
  if (ok) check('unfold: Next walks 1..37, one board at a time, pill in sync', true, '36 taps');
  var b37 = qa(doc, '#deckBody .letter-beat.frame-now')[0];
  var back = b37 ? b37.querySelector('.deck-back') : null;
  if (back) {
    back.click();
    await sleep(10);
    var now3 = qa(doc, '#deckBody .letter-beat.frame-now');
    check('unfold: Back 37 -> 36', now3.length === 1 && now3[0].getAttribute('data-beat') === '36', now3.length ? now3[0].getAttribute('data-beat') : '?');
  } else check('unfold: Back button present on board 37', false);
  var b1 = beats[0], b11 = beats[10], b34 = beats[33], b37t = beats[36];
  check('unfold: board 1 drops the 99/100 claim', b1.textContent.indexOf('99 out of 100') === -1);
  check('unfold: board 11 says superhighway', b11.textContent.indexOf('superhighway') !== -1 && b11.textContent.indexOf('supercomputer') === -1);
  check('unfold: board 34 title is Your card', (b34.querySelector('.ib-title') || {}).textContent === 'Your card');
  check('unfold: board 37 keeps Congratulations — you\u2019re hired', b37t.textContent.indexOf('Congratulations') !== -1 && b37t.textContent.indexOf('you\u2019re hired') !== -1);
  check('unfold: internal audio note is gone', F.unfold.indexOf('Waiting on the captioned video') === -1 && F.unfold.indexOf('Nothing is wired here yet') === -1);
  check('unfold: no script errors after driving', e.errors.length === 0, e.errors.length + ' errors');
  return e;
}

async function scenarioUnfoldStage(F) {
  console.log('\n== S2: /agreement?stage=deck|letter|bridge (fix-1) ==');
  ['deck', 'letter', 'bridge'].forEach(function (st) {
    var e = makeEnv(F.unfold, '?stage=' + st);
    var rep = e.navigations.filter(function (n) { return n.kind === 'replace'; });
    check('unfold: ?stage=' + st + ' redirects to /?stage=' + st, rep.length === 1 && rep[0].url === '/?stage=' + st, JSON.stringify(rep));
  });
}

async function scenarioDeck2(F) {
  console.log('\n== S3: deck on FIX-3 bytes — per-board visibility, foot/photo/seal, bridge URL ==');
  var e = makeEnv(F.welcome, '?stage=deck');
  var doc = e.document;
  console.log('  scripts run: ' + e.scriptsRun + ', script errors: ' + e.errors.length);
  e.errors.slice(0, 5).forEach(function (er) { console.log('  script-error: ' + JSON.stringify(er).slice(0, 300)); });
  var histCalls = [];
  var hist = e.env.history;
  hist.replaceState = function (a, b, u) { histCalls.push({ fn: 'replaceState', url: u }); };
  hist.pushState = function (a, b, u) { histCalls.push({ fn: 'pushState', url: u }); };
  var agreeSec = q(doc, '#fpAgreement');
  var deckBeats = qa(doc, '#deckBody .letter-beat');
  check('deck2: 37 deck boards', deckBeats.length === 37, 'found ' + deckBeats.length);
  function shownDeck() { return deckBeats.filter(function (b) { return !b.hidden; }); }
  var nextBtn = q(doc, '#fpNextBtn');
  var ok = true, sealMiss = [], footMiss = [], imgMiss = [];
  var faceEl = q(doc, '#deckBody .fp-speak-face');
  check('deck2: the one re-parented face (.fp-speak-face) exists in #deckBody', !!faceEl,
    faceEl ? 'parent=' + (faceEl.parentNode ? faceEl.parentNode.tagName + '#' + (faceEl.parentNode.id || '') : '?') : 'absent');
  if (faceEl) check('deck2: face is visible (not hidden)', faceEl.hidden === false && faceEl.style.display !== 'none',
    'hidden=' + faceEl.hidden + ' display=' + JSON.stringify(faceEl.style.display));
  var beatPhotos = qa(doc, '#deckBody .letter-beat .deal-beat-photo').length;
  check('deck2: per-board photos present (36 boards + sign photo on 37)', beatPhotos === 36, beatPhotos + ' .deal-beat-photo inside boards');
  for (var step = 1; step <= 37; step++) {
    var s = shownDeck();
    if (s.length !== 1 || s[0].getAttribute('data-beat') !== String(step) || jewelText(doc) !== step + ' / 37') {
      ok = false; check('deck2: step ' + step + ' one board shown + jewel in sync', false,
        'shown=' + s.length + ' beat=' + (s[0] ? s[0].getAttribute('data-beat') : '?') + ' jewel=' + jewelText(doc)); break;
    }
    var b = s[0];
    var foot = b.querySelector('.ib-foot');
    if (!foot) footMiss.push(step);
    else {
      if (foot.textContent.indexOf('The Deck') === -1) footMiss.push(step + '(text)');
      if (!foot.querySelector('.deal-seal')) sealMiss.push(step);
    }
    var isNoslide = b.classList.contains('fp-noslide');
    var sc = b.querySelector('.lb-showcase');
    var simg = sc ? sc.querySelector('img') : null;
    if (isNoslide) { if (simg) imgMiss.push(step + '(noslide-has-img)'); }
    else { if (!simg) imgMiss.push(step + '(no-img)'); }
    if (step < 37) { nextBtn.click(); await sleep(10); }
  }
  if (ok) check('deck2: all 37 boards one-at-a-time, jewel in sync every landing', true, '37 landings');
  check('deck2: every board foot reads The Deck', footMiss.length === 0, footMiss.length ? 'missing: ' + footMiss.join(',') : '37/37');
  check('deck2: red N seal in every deck foot', sealMiss.length === 0, sealMiss.length ? 'missing: ' + sealMiss.join(',') : '37/37');
  check('deck2: showcase img on every picture board, none on noslide boards', imgMiss.length === 0, imgMiss.length ? imgMiss.join(',') : '9 noslide clean, 28 with img');
  check('deck2: board 37 mirror reads Enter NayaNET', nextBtn.textContent.indexOf('Enter NayaNET') !== -1, JSON.stringify(nextBtn.textContent));
  nextBtn.click();
  await sleep(50);
  var hold = q(doc, '#fpNHold');
  check('deck2: Enter NayaNET shows the N hold', hold && hold.hidden === false);
  await sleep(3300);
  check('deck2: hold releases to the bridge', hold.hidden === true && agreeSec.classList.contains('fp-view-bridge'),
    'hold.hidden=' + hold.hidden + ' bridge=' + agreeSec.classList.contains('fp-view-bridge'));
  var bridgeUrls = histCalls.filter(function (c) { return c.url === '/?stage=bridge'; });
  check('deck2: URL becomes ?stage=bridge (F10, runtime)', bridgeUrls.length >= 1,
    'replaceState/pushState calls to bridge: ' + bridgeUrls.length + ' of ' + histCalls.length + ' total ' + JSON.stringify(histCalls.slice(0, 5)));
  check('deck2: exactly 1 replaceState to bridge (no duplicate)', bridgeUrls.length === 1, 'bridge calls: ' + bridgeUrls.length);
  check('deck2: no script errors after driving', e.errors.length === 0, e.errors.length + ' errors');
  return e;
}

async function scenarioLetter2(F) {
  console.log('\n== S4: letter on FIX-3 bytes — per-board visibility, foot/photo/seal, agree->bridge ==');
  var e = makeEnv(F.welcome, '?stage=letter');
  var doc = e.document;
  console.log('  scripts run: ' + e.scriptsRun + ', script errors: ' + e.errors.length);
  e.errors.slice(0, 5).forEach(function (er) { console.log('  script-error: ' + JSON.stringify(er).slice(0, 300)); });
  var histCalls = [];
  var hist = e.env.history;
  hist.replaceState = function (a, b, u) { histCalls.push({ fn: 'replaceState', url: u }); };
  hist.pushState = function (a, b, u) { histCalls.push({ fn: 'pushState', url: u }); };
  var agreeSec = q(doc, '#fpAgreement');
  var letterBeats = qa(doc, '#letterBody .letter-beat[data-distilled]');
  check('letter2: 37 letter boards', letterBeats.length === 37, 'found ' + letterBeats.length);
  function shownLetter() { return letterBeats.filter(function (b) { return !b.hidden; }); }
  var nextBtn = q(doc, '#fpNextBtn');
  var ok = true, sealMiss = [], footMiss = [], imgMiss = [];
  var faceEl = q(doc, '#fpAgreement .fp-speak-face');
  check('letter2: the one re-parented face (.fp-speak-face) exists in #fpAgreement', !!faceEl,
    faceEl ? 'parent=' + (faceEl.parentNode ? faceEl.parentNode.tagName + '#' + (faceEl.parentNode.id || '') : '?') : 'absent');
  if (faceEl) check('letter2: face is visible (not hidden)', faceEl.hidden === false && faceEl.style.display !== 'none',
    'hidden=' + faceEl.hidden + ' display=' + JSON.stringify(faceEl.style.display));
  var beatPhotos = qa(doc, '#letterBody .letter-beat[data-distilled] .deal-beat-photo').length;
  check('letter2: per-board photos present (36 boards + sign photo on 37)', beatPhotos === 36, beatPhotos + ' .deal-beat-photo inside letter boards');
  for (var step = 1; step <= 37; step++) {
    var s = shownLetter();
    if (s.length !== 1 || s[0] !== letterBeats[step - 1] || jewelText(doc) !== step + ' / 37') {
      ok = false; check('letter2: step ' + step + ' one board shown + jewel in sync', false,
        'shown=' + s.length + ' idx=' + letterBeats.indexOf(s[0]) + ' jewel=' + jewelText(doc)); break;
    }
    var b = s[0];
    var foot = b.querySelector('.ib-foot');
    if (!foot) footMiss.push(step);
    else {
      if (foot.textContent.indexOf('The Collective Agreement') === -1) footMiss.push(step + '(text)');
      if (!foot.querySelector('.deal-seal')) sealMiss.push(step);
    }
    var isNoslide = b.classList.contains('fp-noslide');
    var sc = b.querySelector('.lb-showcase');
    var simg = sc ? sc.querySelector('img') : null;
    if (isNoslide) { if (simg) imgMiss.push(step + '(noslide-has-img)'); }
    else { if (!simg) imgMiss.push(step + '(no-img)'); }
    if (step < 37) { nextBtn.click(); await sleep(10); }
  }
  if (ok) check('letter2: all 37 boards one-at-a-time, jewel in sync every landing', true, '37 landings');
  check('letter2: every board foot reads The Collective Agreement', footMiss.length === 0, footMiss.length ? 'missing: ' + footMiss.join(',') : '37/37');
  check('letter2: red N seal in every letter foot', sealMiss.length === 0, sealMiss.length ? 'missing: ' + sealMiss.join(',') : '37/37');
  check('letter2: showcase img on every picture board, none on noslide boards', imgMiss.length === 0, imgMiss.length ? imgMiss.join(',') : '9 noslide clean, 28 with img');
  check('letter2: board 37 mirror reads I agree', nextBtn.textContent.indexOf('I agree') !== -1, JSON.stringify(nextBtn.textContent));
  nextBtn.click();
  await sleep(50);
  check('letter2: I agree opens the agree view', agreeSec.classList.contains('fp-view-agree'), agreeSec.className);
  var agreeBtn = q(doc, '#dealAgreeBtn');
  check('letter2: agree button present', !!agreeBtn);
  if (agreeBtn) {
    agreeBtn.click();
    await sleep(50);
    var hold = q(doc, '#fpNHold');
    check('letter2: agree shows the N hold', hold && hold.hidden === false);
    await sleep(3300);
    check('letter2: hold releases to the bridge', agreeSec.classList.contains('fp-view-bridge'), agreeSec.className);
    var bridgeUrls = histCalls.filter(function (c) { return c.url === '/?stage=bridge'; });
    check('letter2: URL becomes ?stage=bridge after agree (F10, runtime)', bridgeUrls.length >= 1,
      'bridge calls: ' + bridgeUrls.length + ' of ' + histCalls.length + ' ' + JSON.stringify(histCalls.slice(0, 5)));
    check('letter2: exactly 1 replaceState to bridge (no duplicate)', bridgeUrls.length === 1, 'bridge calls: ' + bridgeUrls.length);
  }
  check('letter2: no script errors after driving', e.errors.length === 0, e.errors.length + ' errors');
  return e;
}

async function scenarioRace(F) {
  console.log('\n== S5: loading race F5b — failed load -> retry -> fallback, as runtime events ==');
  var e = makeEnv(F.welcome, '?stage=deck');
  var doc = e.document;
  var deckBeats = qa(doc, '#deckBody .letter-beat');
  var shown = deckBeats.filter(function (b) { return !b.hidden; })[0];
  var scImg = shown ? shown.querySelector('.lb-showcase img') : null;
  check('race: a showcase img exists on board 1', !!scImg, scImg ? scImg.getAttribute('src').slice(0, 80) : 'none');
  if (scImg) {
    var src0 = scImg.getAttribute('src');
    var ev = { type: 'error', bubbles: true, target: null, currentTarget: null, defaultPrevented: false, _stopped: false, preventDefault: function () { this.defaultPrevented = true; }, stopPropagation: function () { this._stopped = true; } };
    scImg.dispatchEvent(ev);
    await sleep(10);
    var src1 = scImg.getAttribute('src');
    check('race: failed showcase load retries with ?retry=1', src1 === src0 + (src0.indexOf('?') === -1 ? '?' : '&') + 'retry=1' && scImg.getAttribute('data-fp-retried') === '1',
      'src after error: ' + JSON.stringify((src1 || '').slice(-60)));
    var ev2 = { type: 'error', bubbles: true, target: null, currentTarget: null, defaultPrevented: false, _stopped: false, preventDefault: function () { this.defaultPrevented = true; }, stopPropagation: function () { this._stopped = true; } };
    scImg.dispatchEvent(ev2);
    await sleep(10);
    var sc = scImg.closest('.lb-showcase');
    check('race: second failure hides the showcase (fallback)', sc && sc.style.display === 'none',
      'showcase display=' + (sc ? JSON.stringify(sc.style.display) : 'no showcase'));
  }
  var face = q(doc, '#deckBody .fp-speak-face');
  check('race: the re-parented face photo exists', !!face, face ? face.getAttribute('src').slice(0, 80) : 'none');
  if (face) {
    var fsrc0 = face.getAttribute('src');
    var ev3 = { type: 'error', bubbles: true, target: null, currentTarget: null, defaultPrevented: false, _stopped: false, preventDefault: function () { this.defaultPrevented = true; }, stopPropagation: function () { this._stopped = true; } };
    face.dispatchEvent(ev3);
    await sleep(10);
    var fsrc1 = face.getAttribute('src');
    check('race: failed face photo falls back to the crystal image', fsrc1 !== fsrc0 && fsrc1.indexOf('crystal-n.png') !== -1,
      'src after error: ' + JSON.stringify((fsrc1 || '').slice(0, 100)));
  }
  check('race: no script errors after driving', e.errors.length === 0, e.errors.length + ' errors');
}

function identityParts(doc) {
  var inputs = qa(doc, 'input');
  var input = null;
  for (var ii = 0; ii < inputs.length; ii++) {
    var ph = inputs[ii].getAttribute('placeholder') || '';
    if (ph.indexOf('lias') !== -1) { input = inputs[ii]; break; }
  }
  if (!input && inputs.length) input = inputs[0];
  var nameEl = doc.querySelector('[data-cert-name]') || doc.querySelector('.cert-name');
  return { input: input, nameEl: nameEl };
}

async function scenarioIdentityPaired(F) {
  console.log('\n== S6a: identity PAIRED ?name=Distill Eye Walk&alias=Distill (F9a — the fix) ==');
  var e = makeEnv(F.identity, '?name=Distill%20Eye%20Walk&alias=Distill');
  var doc = e.document;
  await sleep(50);
  console.log('  scripts run: ' + e.scriptsRun + ', script errors: ' + e.errors.length);
  e.errors.slice(0, 5).forEach(function (er) { console.log('  script-error: ' + JSON.stringify(er).slice(0, 300)); });
  var p = identityParts(doc);
  check('identity-paired: alias input exists', !!p.input);
  if (p.input) check('identity-paired: alias input pre-filled with the paired alias', p.input.value === 'distill', 'value=' + JSON.stringify(p.input.value) + ' (paired alias, lowercased by the page\'s own FIX6 load check — base-proven)');
  check('identity-paired: composing name line exists', !!p.nameEl);
  if (p.nameEl) {
    check('identity-paired: name line paints the passed name', p.nameEl.textContent === 'Distill Eye Walk', 'text=' + JSON.stringify(p.nameEl.textContent));
    check('identity-paired: name line data-text set (the ::before echo)', p.nameEl.getAttribute('data-text') === 'Distill Eye Walk', 'data-text=' + JSON.stringify(p.nameEl.getAttribute('data-text')));
    check('identity-paired: name line unhidden', p.nameEl.hidden === false, 'hidden=' + p.nameEl.hidden);
  }
  var seal = doc.querySelector('.deal-seal');
  check('identity-paired: red N seal present on the certificate', !!seal);
  var back = doc.querySelector('.cert-back');
  check('identity-paired: Back to the walk button present', !!back);
  check('identity-paired: no script errors after driving', e.errors.length === 0, e.errors.length + ' errors');
  // Stability: no later async repaint (availability check, restore) may
  // degrade the hero from the full name back to the alias.
  await sleep(2000);
  if (p.input) check('identity-paired: alias input still the canonical alias after 2s', p.input.value === 'distill', 'value=' + JSON.stringify(p.input.value));
  if (p.nameEl) check('identity-paired: name line still paints the passed name after 2s', p.nameEl.textContent === 'Distill Eye Walk', 'text=' + JSON.stringify(p.nameEl.textContent));
  check('identity-paired: still no script errors after 2s', e.errors.length === 0, e.errors.length + ' errors');
  return e;
}

async function scenarioIdentityUnpaired(F) {
  console.log('\n== S6b: identity UNPAIRED ?name= only (F9a — FIX3 never-pre-paint stands) ==');
  var e = makeEnv(F.identity, '?name=Distill%20Eye%20Walk');
  var doc = e.document;
  await sleep(50);
  var p = identityParts(doc);
  check('identity-name-only: alias input exists', !!p.input);
  if (p.input) check('identity-name-only: input stays EMPTY (no paired alias, no pre-paint)', p.input.value === '', 'value=' + JSON.stringify(p.input.value));
  check('identity-name-only: composing name line exists', !!p.nameEl);
  if (p.nameEl) {
    check('identity-name-only: name line stays blank', p.nameEl.textContent === '', 'text=' + JSON.stringify(p.nameEl.textContent));
    check('identity-name-only: name line stays hidden', p.nameEl.hidden === true, 'hidden=' + p.nameEl.hidden);
    check('identity-name-only: name line data-text unset', p.nameEl.getAttribute('data-text') === null, 'data-text=' + JSON.stringify(p.nameEl.getAttribute('data-text')));
  }
  check('identity-name-only: no script errors after driving', e.errors.length === 0, e.errors.length + ' errors');
  console.log('\n== S6c: identity UNPAIRED ?alias= only ==');
  var e2 = makeEnv(F.identity, '?alias=Distill');
  var doc2 = e2.document;
  await sleep(50);
  var p2 = identityParts(doc2);
  check('identity-alias-only: alias input exists', !!p2.input);
  // Pre-existing FIX6 load-check behavior (base-proven): ?alias= fills the field
  // with the lowercased alias and runs the availability check, name or no name.
  // My round does not touch that path. What must stay empty without a paired
  // name is the HERO (no name to paint).
  if (p2.input) check('identity-alias-only: input holds the passed alias (pre-existing FIX6 fill)', p2.input.value === 'distill', 'value=' + JSON.stringify(p2.input.value));
  if (p2.nameEl) check('identity-alias-only: name line stays hidden', p2.nameEl.hidden === true, 'hidden=' + p2.nameEl.hidden);
  check('identity-alias-only: no script errors after driving', e2.errors.length === 0, e2.errors.length + ' errors');
  return e;
}

async function scenarioWalkDoor(F) {
  console.log('\n== S7: walk door — guard holds the questionnaire while the door is visible (F9b) + seal + name link ==');
  var e = makeEnv(F.walk, '?name=Distill%20Eye%20Walk&alias=Distill');
  var doc = e.document;
  console.log('  scripts run: ' + e.scriptsRun + ', script errors: ' + e.errors.length);
  e.errors.slice(0, 5).forEach(function (er) { console.log('  script-error: ' + JSON.stringify(er).slice(0, 300)); });
  var door = q(doc, '#step-door');
  check('walk: door element exists', !!door);
  if (door) {
    check('walk: door is visible at boot', door.hidden === false, 'hidden=' + door.hidden);
    var seal = door.querySelector('.deal-seal');
    check('walk: red N seal on the door', !!seal);
    var link = door.querySelector('a[href*="/identity.html"]');
    check('walk: door certificate link exists', !!link);
    if (link) {
      var href = link.getAttribute('href');
      check('walk: door certificate link carries name+alias', href.indexOf('name=Distill') !== -1 && href.indexOf('alias=Distill') !== -1, 'href=' + JSON.stringify(href));
    }
  }
  function visibleSteps() {
    return qa(doc, '[id^="step-"]').filter(function (el) { return !el.hidden; }).map(function (el) { return el.id; });
  }
  var before = visibleSteps();
  await sleep(5000);
  var after = visibleSteps();
  check('walk: door still visible after 5s with no user action', JSON.stringify(after) === JSON.stringify(before) && after.indexOf('step-door') !== -1,
    'before=' + JSON.stringify(before) + ' after=' + JSON.stringify(after));
  check('walk: questionnaire does not advance while the door is visible', JSON.stringify(after) === JSON.stringify(before),
    'before=' + JSON.stringify(before) + ' after=' + JSON.stringify(after));
  // The explicit continue: the door's dismissing user action in place.
  var cont = q(doc, '#doorContinue');
  check('walk: explicit continue button exists on the door', !!cont);
  if (cont) {
    check('walk: continue is VISIBLE for the certified citizen (has alias)', cont.hidden === false, 'hidden=' + cont.hidden);
    check('walk: continue reads Continue to the walk', cont.textContent.indexOf('Continue to the walk') !== -1, JSON.stringify(cont.textContent));
    cont.click();
    await sleep(50);
    var afterClick = visibleSteps();
    check('walk: tapping Continue dismisses the door and opens the questionnaire', afterClick.indexOf('step-door') === -1 && afterClick.indexOf('step-1') !== -1,
      'visible=' + JSON.stringify(afterClick));
  }
  check('walk: no script errors after driving', e.errors.length === 0, e.errors.length + ' errors');
  return e;
}

async function scenarioWalkDoorNoAlias(F) {
  console.log('\n== S7b: walk door, NO alias — continue hidden, certificate link is the only way ==');
  var e0 = makeEnv(F.walk, '');
  var doc0 = e0.document;
  await sleep(50);
  var door0 = q(doc0, '#step-door');
  check('walk-noalias: door is visible at boot', door0 && door0.hidden === false);
  var cont0 = q(doc0, '#doorContinue');
  check('walk-noalias: explicit continue exists in markup', !!cont0);
  if (cont0) check('walk-noalias: continue is HIDDEN without a certificate', cont0.hidden === true, 'hidden=' + cont0.hidden);
  var link0 = door0 ? door0.querySelector('a[href*="/identity.html"]') : null;
  check('walk-noalias: certificate link exists (the way forward)', !!link0);
  check('walk-noalias: no script errors after driving', e0.errors.length === 0, e0.errors.length + ' errors');
  return e0;
}

async function scenarioWalkDoorReturn(F) {
  console.log('\n== S7c: certified RETURN trip — identity Back to the walk lands on the door, Continue opens it ==');
  // Identity's Back to the walk goes to /welcome with no params; the alias
  // persists in localStorage (the walk ingests ?alias= there at claim time).
  var eR = makeEnv(F.walk, '', { local: { nayanet_smart_alias: 'distill', nayanet_smart_name: 'Distill Eye Walk' } });
  var docR = eR.document;
  function visibleStepsR() { return qa(docR, '[id^="step-"]').filter(function (el) { return !el.hidden; }).map(function (el) { return el.id; }); }
  var doorR = q(docR, '#step-door');
  check('walk-return: door is visible at boot (certified citizen returns)', doorR && doorR.hidden === false);
  await sleep(2000);
  check('walk-return: door still holds after 2s (no auto-advance on the return trip)', JSON.stringify(visibleStepsR()) === '["step-door"]', 'visible=' + JSON.stringify(visibleStepsR()));
  var contR = q(docR, '#doorContinue');
  check('walk-return: continue is visible on the return trip', contR && contR.hidden === false);
  if (contR) {
    contR.click();
    await sleep(50);
    check('walk-return: tapping Continue opens the questionnaire', JSON.stringify(visibleStepsR()) === '["step-1"]', 'visible=' + JSON.stringify(visibleStepsR()));
  }
  check('walk-return: no script errors after driving', eR.errors.length === 0, eR.errors.length + ' errors');
  return eR;
}

async function scenarioRail(F) {
  console.log('\n== S8: the long-letter rail — reachable content + the cut (ruling a) ==');
  var e = makeEnv(F.welcome, '?stage=deck');
  var doc = e.document;
  var railArts = qa(doc, '#letterBody article').filter(function (a) { return !a.hasAttribute('data-distilled'); });
  console.log('  rail (non-distilled) articles in #letterBody: ' + railArts.length);
  check('rail: the long letter rail is present in bytes', railArts.length > 37, railArts.length + ' rail articles');
  var money = railArts.filter(function (a) { return a.getAttribute('data-beat') === '51'; });
  check('rail: money board 51 exists', money.length === 1, money.length + '');
  if (money.length === 1) {
    check('rail: money board no longer says Congratulations / hired', money[0].textContent.indexOf('Congratulations') === -1 && money[0].textContent.indexOf('hired') === -1,
      JSON.stringify(money[0].textContent.slice(0, 120)));
  }
  var legalAll = q(doc, '#fpLinkLegalAll');
  check('rail: "or read the whole page at once" link exists', !!legalAll);
  check('rail: no script errors after driving', e.errors.length === 0, e.errors.length + ' errors');
  return e;
}

async function scenarioWelcomePlain(F) {
  console.log('\n== S9: / plain — hero button, name form, reload restore (fix-1 scenario 5, re-run in full) ==');
  var e = makeEnv(F.welcome, '');
  var doc = e.document;
  console.log('  scripts run: ' + e.scriptsRun + ', script errors: ' + e.errors.length);
  e.errors.slice(0, 5).forEach(function (er) { console.log('  script-error: ' + JSON.stringify(er).slice(0, 300)); });
  var enterBtn = q(doc, '#fpEnterDeal');
  check('plain: hero Read button present', !!enterBtn);
  if (enterBtn) {
    enterBtn.click();
    await sleep(10);
    var nav = e.navigations.filter(function (n) { return n.kind === 'href'; });
    check('plain: hero Read goes to /agreement', nav.length >= 1 && nav[nav.length - 1].url === '/agreement', JSON.stringify(nav));
  }
  var e2 = makeEnv(F.welcome, '', { local: { nayanet_fp_agreed: '1' } });
  var doc2 = e2.document;
  var form = q(doc2, '#entryForm');
  var name = q(doc2, '#userName');
  check('plain: name form present', !!form && !!name);
  if (form && name) {
    name.value = 'Test Name';
    var ev = { type: 'submit', bubbles: true, target: form, currentTarget: form, defaultPrevented: false, _stopped: false, preventDefault: function () { this.defaultPrevented = true; }, stopPropagation: function () { this._stopped = true; } };
    form.dispatchEvent(ev);
    await sleep(50);
    var hold2 = q(doc2, '#fpNHold');
    check('plain: agreed submit shows the N hold', hold2 && hold2.hidden === false);
    await sleep(3300);
    var nav2 = e2.navigations.filter(function (n) { return n.kind === 'href'; });
    check('plain: hold releases to identity with the name', nav2.length >= 1 && nav2[nav2.length - 1].url === '/identity.html?name=Test%20Name', JSON.stringify(nav2));
  }
  var e3 = makeEnv(F.welcome, '', { session: { nayanet_fp_from_bridge: '1' } });
  var doc3 = e3.document;
  var form3 = q(doc3, '#entryForm');
  check('plain: reload with fromBridge re-opens the name form', form3 && form3.hidden === false);
  check('plain: no script errors after driving', e.errors.length === 0 && e2.errors.length === 0 && e3.errors.length === 0,
    'e=' + e.errors.length + ' e2=' + e2.errors.length + ' e3=' + e3.errors.length);
}

async function runStateMachine(F) {
  console.log('\nFIXED3 bytes: unfold=' + Buffer.byteLength(F.unfold) + ' welcome=' + Buffer.byteLength(F.welcome) + ' walk=' + Buffer.byteLength(F.walk) + ' identity=' + Buffer.byteLength(F.identity));
  await scenarioUnfold(F);
  await scenarioUnfoldStage(F);
  await scenarioDeck2(F);
  await scenarioLetter2(F);
  await scenarioRace(F);
  await scenarioIdentityPaired(F);
  await scenarioIdentityUnpaired(F);
  await scenarioWalkDoor(F);
  await scenarioWalkDoorNoAlias(F);
  await scenarioWalkDoorReturn(F);
  await scenarioRail(F);
  await scenarioWelcomePlain(F);
}

if (require.main === module) {
  main().catch((e) => { console.error('FATAL', e); process.exit(1); });
}
