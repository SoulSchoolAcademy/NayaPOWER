#!/usr/bin/env node
// probe-fix3b.js — deeper contexts. No writes.
const https = require('https');
const STAGE = 'naya-walk-beginning-staging.nayapower.workers.dev';
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
function ctxAt(s, idx, before, after, label) {
  console.log('=== ' + label + ' @' + idx + ' ===');
  console.log(s.slice(Math.max(0, idx - before), idx + after));
  console.log('=== end ===');
}
function allidx(s, needle, label) {
  const out = []; let i = -1;
  while ((i = s.indexOf(needle, i + 1)) !== -1) out.push(i);
  console.log(label + ': ' + out.length + 'x @ ' + out.join(','));
  return out;
}
(async () => {
  const I = await get('/identity.html?name=Distill%20Eye%20Walk');
  const WK = await get('/welcome');
  // identity: currentDisplayName full body
  const cdi = I.indexOf('currentDisplayName');
  ctxAt(I, cdi, 100, 1400, 'I currentDisplayName body');
  // paintHeroName call sites
  for (const idx of allidx(I, 'paintHeroName(', 'I paintHeroName calls')) {
    ctxAt(I, idx, 500, 300, 'I paintHeroName call @' + idx);
  }
  // second aliasInput clear
  ctxAt(I, 355311, 800, 600, 'I second aliasInput.value clear');
  // where is rawName used after? 
  allidx(I, 'rawName', 'I rawName uses');
  // updateSmartCredentials — input handler?
  const usc = I.indexOf('function updateSmartCredentials');
  if (usc > -1) ctxAt(I, usc, 100, 900, 'I updateSmartCredentials');
  // WALK: proceed definition
  const pr = WK.indexOf('proceed =');
  console.log('WK proceed = @' + pr);
  if (pr > -1) ctxAt(WK, pr, 400, 900, 'WK proceed def');
  allidx(WK, 'showDoor()', 'WK showDoor() calls');
  // where does boot decide door vs questionnaire?
  const boot = WK.indexOf('showDoor');
  // find the claim-gate enclosing function name
  const g = WK.indexOf('gateDone6');
  ctxAt(WK, g, 1500, 200, 'WK claim-gate enclosing fn');
  // door dismiss: any click handler on step-door or data-back cert?
  allidx(WK, "data-back", 'WK data-back');
  ctxAt(WK, WK.indexOf('certUrl'), 200, 600, 'WK certUrl def');
  // what sets DOORSEC visible at boot? search DOORSEC
  allidx(WK, 'DOORSEC', 'WK DOORSEC');
  const d = WK.indexOf('DOORSEC =');
  if (d > -1) ctxAt(WK, d, 200, 400, 'WK DOORSEC def');
})().catch((e) => { console.error('FATAL', e); process.exit(1); });
