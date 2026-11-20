#!/usr/bin/env node
// mech-probe.js — CHECKER mechanism probe on BASE bytes (no transform):
// (1) exact byte-length of each fix-3 insertion delta (maker constants vs checker);
// (2) full text of the walk's /api/claim fetch verdict handler (.then/.catch);
// (3) full text of identity's checkAliasAvailability (can its verdict repaint the hero?).
const https = require('https');
const crypto = require('crypto');
const fs = require('fs');
const runFix2 = require('/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix3-20261119/maker/work/run-fix2-export.js');
const checker = require('./check-fix3.js');
const sha = (s) => crypto.createHash('sha256').update(s, 'utf8').digest('hex');
function get(p) {
  return new Promise((res, rej) => {
    const req = https.get({ hostname: 'naya-walk-beginning-staging.nayapower.workers.dev', path: p, headers: { 'User-Agent': 'Mozilla/5.0' } }, (r) => {
      const b = []; r.on('data', (c) => b.push(c));
      r.on('end', () => res(Buffer.concat(b).toString('utf8')));
      r.on('error', rej);
    });
    req.setTimeout(60000, () => req.destroy(new Error('timeout')));
    req.on('error', rej);
  });
}
(async () => {
  // (1) insertion delta lengths — from the checker's own constants (proven identical to the maker's by diff-maker.js).
  const src = fs.readFileSync('./check-fix3.js', 'utf8');
  // Grab each const statement whole (some are concatenations) and eval it in a
  // scope where the anchor consts are already defined.
  const stmt = (name) => {
    const i = src.indexOf('const ' + name + ' = ');
    if (i < 0) throw new Error('const not found: ' + name);
    const semi = src.indexOf(';\n', i);
    return src.slice(i + ('const ' + name + ' = ').length, semi);
  };
  const ev = (expr, scope) => new Function(...Object.keys(scope), 'return (' + expr + ');')(...Object.values(scope));
  const I_ANCHOR = ev(stmt('I_ANCHOR'), {});
  const I_FIX3 = ev(stmt('I_FIX3'), {});
  const P_ANCHOR = ev(stmt('P_ANCHOR'), {});
  const P_GUARD = ev(stmt('P_GUARD'), {});
  const T_ANCHOR = ev(stmt('T_ANCHOR'), {});
  const T_GUARD = ev(stmt('T_GUARD'), {});
  const D_ANCHOR = ev(stmt('D_ANCHOR'), {});
  const D_CONT = ev(stmt('D_CONT'), { D_ANCHOR });
  const W_ANCHOR = ev(stmt('W_ANCHOR'), {});
  const W_WIRE = ev(stmt('W_WIRE'), { W_ANCHOR });
  const pairs = [
    ['I_FIX3', null, I_FIX3],
    ['P_GUARD vs P_ANCHOR', P_ANCHOR, P_GUARD],
    ['T_GUARD vs T_ANCHOR', T_ANCHOR, T_GUARD],
    ['D_CONT vs D_ANCHOR', D_ANCHOR, D_CONT],
    ['W_WIRE vs W_ANCHOR', W_ANCHOR, W_WIRE],
  ];
  let walkTotal = 0;
  for (const [label, a, b] of pairs) {
    if (a === null) { console.log(label + ': +' + Buffer.byteLength(b) + 'B'); continue; }
    const d = Buffer.byteLength(b) - Buffer.byteLength(a);
    console.log(label + ': +' + d + 'B');
    if (label !== 'I_FIX3') walkTotal += d;
  }
  console.log('WALK INSERTION TOTAL: +' + walkTotal + 'B (maker §2 claims +1018B; diff ' + (walkTotal - 1018) + 'B)');
  console.log('IDENTITY INSERTION TOTAL: +481B (maker §2 claims +481B)');

  // (2) walk claim-verdict handler, base bytes.
  const WK0 = await get('/welcome');
  const fi = WK0.indexOf("fetch('/api/claim?alias='");
  console.log('\n--- WALK /api/claim handler, base bytes @' + fi + ' ---');
  console.log(WK0.slice(fi, fi + 1400));
  console.log('--- end handler ---');
  // The resume/proceed function full text (for the "single funnel" claim).
  const pi = WK0.indexOf('var proceed = function(){');
  console.log('\n--- proceed() full text, base bytes ---');
  console.log(WK0.slice(pi, pi + 1800));
  console.log('--- end proceed ---');
  // showDoor call sites that run at boot (not inside functions).
  console.log('\n--- showDoor(); boot call context ---');
  const si = WK0.indexOf('showDoor();', WK0.indexOf('FIX6 (2026-11-19)'));
  console.log(JSON.stringify(WK0.slice(Math.max(0, si - 300), si + 200)));

  // (3) identity checkAliasAvailability full text, base bytes.
  const I0 = await get('/identity.html?name=Distill%20Eye%20Walk');
  const ci = I0.indexOf('function checkAliasAvailability(alias, silent)');
  console.log('\n--- checkAliasAvailability full text, base bytes ---');
  console.log(I0.slice(ci, ci + 2600));
  console.log('--- end checkAliasAvailability ---');
  // Does anything after the I-FIX3 insertion point repaint the hero? List every
  // paintHeroName call AFTER the updateSmartCredentials() anchor in base identity.
  const anchor = I0.indexOf('updateSmartCredentials();', I0.indexOf('paintValues(currentAlias'));
  let j = anchor, n = 0;
  console.log('\n--- paintHeroName calls AFTER the load-paint anchor (base identity) ---');
  while ((j = I0.indexOf('paintHeroName(', j + 1)) !== -1) {
    n++;
    console.log('#' + n + ' @' + j + ': ' + JSON.stringify(I0.slice(Math.max(0, j - 160), j + 160).replace(/\n/g, ' ')));
  }
  if (!n) console.log('none — nothing after the anchor repaints the hero at load time');
  process.exit(0);
})().catch((e) => { console.error('FATAL', e); process.exit(1); });
