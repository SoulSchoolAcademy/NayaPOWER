#!/usr/bin/env node
// probe-fix3.js — fetch identity + walk base, print contexts around the F9 code. No writes.
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
function ctx(s, needle, before, after, label) {
  const i = s.indexOf(needle);
  if (i < 0) { console.log('NOT FOUND: ' + label + ' :: ' + JSON.stringify(needle.slice(0, 80))); return; }
  console.log('=== ' + label + ' @' + i + ' ===');
  console.log(s.slice(Math.max(0, i - (before || 400)), i + needle.length + (after || 800)));
  console.log('=== end ' + label + ' ===');
}
function allidx(s, needle, label) {
  const out = []; let i = -1;
  while ((i = s.indexOf(needle, i + 1)) !== -1) out.push(i);
  console.log(label + ': ' + out.length + 'x @ ' + out.join(','));
}
(async () => {
  const I = await get('/identity.html?name=Distill%20Eye%20Walk');
  const WK = await get('/welcome');
  console.log('identity bytes: ' + Buffer.byteLength(I) + ' walk bytes: ' + Buffer.byteLength(WK));
  // IDENTITY
  ctx(I, 'passedName', 300, 600, 'I passedName def');
  ctx(I, 'currentDisplayName', 300, 900, 'I currentDisplayName');
  ctx(I, 'paintHeroName', 200, 700, 'I paintHeroName def');
  allidx(I, 'paintHeroName(', 'I paintHeroName( calls');
  allidx(I, "aliasInput.value = ''", 'I FIX3 clear');
  ctx(I, "aliasInput.value = ''", 700, 500, 'I FIX3 clear ctx');
  allidx(I, 'urlParams', 'I urlParams');
  ctx(I, 'displayName', 200, 400, 'I displayName first');
  allidx(I, 'cert-name', 'I cert-name');
  ctx(I, 'cert-name::before', 100, 300, 'I cert-name::before CSS');
  // WALK
  allidx(WK, 'gateDone6', 'WK gateDone6');
  ctx(WK, 'gateDone6', 600, 600, 'WK claim-gate timer ctx');
  allidx(WK, 'step-door', 'WK step-door');
  ctx(WK, 'showDoor', 200, 500, 'WK showDoor');
  allidx(WK, 'proceed()', 'WK proceed() calls');
  ctx(WK, 'function proceed', 300, 700, 'WK proceed def');
  ctx(WK, 'step-door', 300, 900, 'WK door HTML');
})().catch((e) => { console.error('FATAL', e); process.exit(1); });
