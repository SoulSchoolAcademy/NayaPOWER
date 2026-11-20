#!/usr/bin/env node
// check-base-equiv.js — in-memory only. Does the live staging BASE unfold contain
// the Nov-18 FIX1 deck-beat-9 logic that the stale disk unfold has?
// (Decides whether base is a true superset or a divergent lineage.)
const https = require('https');
const crypto = require('crypto');
const fs = require('fs');
const STAGE = 'naya-walk-beginning-staging.nayapower.workers.dev';
function get(p) {
  return new Promise((res, rej) => {
    const req = https.get({ hostname: STAGE, path: p, headers: { 'User-Agent': 'Mozilla/5.0' } }, (r) => {
      const b = []; r.on('data', (c) => b.push(c)); r.on('end', () => res(Buffer.concat(b).toString('utf8'))); r.on('error', rej);
    });
    req.setTimeout(60000, () => req.destroy(new Error('timeout')));
    req.on('error', rej);
  });
}
function sha(s) { return crypto.createHash('sha256').update(s, 'utf8').digest('hex'); }
function count(s, n) { let c = 0, i = -1; while ((i = s.indexOf(n, i + 1)) !== -1) c++; return c; }
(async () => {
  const U0 = await get('/agreement');
  const W0 = await get('/?stage=deck');
  console.log('base unfold sha ' + sha(U0).slice(0, 16) + ' expect 5fe1a3ec -> ' + (sha(U0).startsWith('5fe1a3ec') ? 'MATCH' : 'MISMATCH'));
  console.log('base welcome sha ' + sha(W0).slice(0, 16) + ' expect c3c750b7 -> ' + (sha(W0).startsWith('c3c750b7') ? 'MATCH' : 'MISMATCH'));
  const staleU = fs.readFileSync('/home/hatch/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html', 'utf8');
  const staleW = fs.readFileSync('/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/welcome-staged.html', 'utf8');
  const probes = [
    ['currentBeatEl', 'Nov-18 FIX1 deck-beat-9 helper'],
    ['fp-smart-visual', 'Nov-18 FIX1 visual-phase class'],
    ['deck beat 9 HAS a showcase', 'Nov-18 FIX1 comment'],
    ['EYE FOLLOW-ON #2 F4', 'eye follow-on comment'],
    ['__fpDeckEndReturn', 'deck-end return flag'],
    ['Nine pictures', 'F8 phrase (should be 0 in base)'],
    ['1 / 86', 'old 86-count jewel (should be 0 in base)'],
    ['fpLinkLetterAll', 'read-it-all link id'],
  ];
  for (const [needle, label] of probes) {
    console.log(label + ' :: base-unfold ' + count(U0, needle) + 'x | stale-unfold ' + count(staleU, needle) + 'x | base-welcome ' + count(W0, needle) + 'x | stale-welcome ' + count(staleW, needle) + 'x');
  }
})().catch((e) => { console.error('FATAL: ' + (e && e.stack || e)); process.exit(1); });
