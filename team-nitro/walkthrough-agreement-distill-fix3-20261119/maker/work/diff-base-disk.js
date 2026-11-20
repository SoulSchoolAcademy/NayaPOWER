#!/usr/bin/env node
// diff-base-disk.js — fix-3 landing probe: fetch base from staging IN MEMORY,
// compare against the disk files the build script reads, WITHOUT writing large
// files (EPERM flake: large writes land 0 bytes right now).
// Question: do the stale disk files (unfold, welcome) contain anything the
// live staging base lacks? If base is a superset, overwriting them with the
// fix-3 bytes loses nothing live. Prints only a summary + the stale-only lines.
const https = require('https');
const crypto = require('crypto');
const fs = require('fs');

const STAGE = 'naya-walk-beginning-staging.nayapower.workers.dev';
const BASE = {
  unfold: { bytes: 141781, sha256: '5fe1a3ec2231c128774c6eb00736913d93117d3eaa06278e2a16183cdebee6ab' },
  welcome: { bytes: 1913241, sha256: 'c3c750b72a2b0330d15de8831e9b24719116991e6c0df9dbc5d329834fbbaed5' },
  walk: { bytes: 4361369, sha256: '0f05b3f96ce8edd0ecb094c0f64972098f788c3943e22b5446c8bb60e9b0e2fd' },
  identity: { bytes: 401040, sha256: '3279dc3572337e5e' },
};
const DISK = {
  unfold: '/home/hatch/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html',
  welcome: '/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/welcome-staged.html',
  walk: '/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html',
  identity: '/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/identity-fixed.html',
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

async function main() {
  const U0 = await get('/agreement');
  const W0 = await get('/?stage=deck');
  const WK0 = await get('/welcome');
  const I0 = await get('/identity.html?name=Distill%20Eye%20Walk');
  const fetched = { unfold: U0, welcome: W0, walk: WK0, identity: I0 };
  for (const k of Object.keys(BASE)) {
    const s = fetched[k], b = Buffer.byteLength(s), h = sha(s);
    const ok = b === BASE[k].bytes && h.startsWith(BASE[k].sha256);
    console.log('BASE ' + k + ': ' + b + 'B sha ' + h.slice(0, 16) + ' -> ' + (ok ? 'MATCH' : 'MISMATCH'));
    if (!ok) throw new Error('base mismatch: ' + k);
  }
  for (const k of Object.keys(BASE)) {
    const disk = fs.readFileSync(DISK[k], 'utf8');
    const db = Buffer.byteLength(disk), dh = sha(disk);
    console.log('\n--- ' + k + ' ---');
    console.log('disk: ' + db + 'B sha ' + dh.slice(0, 16) + ' vs base ' + BASE[k].bytes + 'B sha ' + BASE[k].sha256.slice(0, 8));
    if (dh.startsWith(BASE[k].sha256)) { console.log('VERDICT: disk IS the base (identical).'); continue; }
    // Set-diff on lines: what does the stale disk file have that base lacks?
    const baseLines = fetched[k].split('\n');
    const diskLines = disk.split('\n');
    const baseSet = new Set(baseLines);
    const diskSet = new Set(diskLines);
    const removed = []; const removedSeen = new Set();
    for (const ln of diskLines) if (!baseSet.has(ln) && !removedSeen.has(ln)) { removedSeen.add(ln); removed.push(ln); }
    let added = 0; const addedSeen = new Set();
    for (const ln of baseLines) if (!diskSet.has(ln) && !addedSeen.has(ln)) { addedSeen.add(ln); added++; }
    console.log('lines: disk ' + diskLines.length + ' / base ' + baseLines.length);
    console.log('UNIQUE-TO-DISK lines: ' + removed.length + ' | UNIQUE-TO-BASE lines: ' + added);
    if (removed.length === 0) {
      console.log('VERDICT: STALE-IS-SUBSET — every distinct disk line is present in base. Overwriting loses no distinct line.');
    } else {
      console.log('VERDICT: STALE-HAS-UNIQUE — the disk file has content base lacks. DO NOT overwrite blindly.');
      console.log('--- stale-only lines (first 120, full text) ---');
      removed.slice(0, 120).forEach((ln, i) => console.log('[' + i + '] ' + JSON.stringify(ln.slice(0, 600))));
      if (removed.length > 120) console.log('... and ' + (removed.length - 120) + ' more stale-only lines');
    }
  }
}
main().catch((e) => { console.error('FATAL: ' + (e && e.stack || e)); process.exit(1); });
