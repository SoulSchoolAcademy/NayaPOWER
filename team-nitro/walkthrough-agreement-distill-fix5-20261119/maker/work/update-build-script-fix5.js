#!/usr/bin/env node
/* FIX-5: point the v23 staging build script at the fix-5 input sha.
   Reads ~/workspace/team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py,
   updates the welcome assert (237af4d4 -> 57ebe2d2), asserted exactly once.
   Writes the script back in place (same dir, verified by sha after) and
   copies it to this work dir as fix5-build-v23-staging-worker.py. */
const fs = require('fs');
const crypto = require('crypto');
const P = '/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py';
const HERE = __dirname;
let s = fs.readFileSync(P, 'utf8');
function rep(anchor, insert, label) {
  const n = s.split(anchor).length - 1;
  if (n !== 1) throw new Error(`${label}: anchor occurs ${n}x (want 1)`);
  s = s.replace(anchor, insert);
}
rep('assert welcome_sha.startswith("237af4d4"), "welcome sha is not the AGREEMENT-DISTILL-FIX4b welcome sha (2026-11-20: fix-4 verify — board-37 title beats the af-deck !important rule)"',
  '# AGREEMENT-DISTILL-FIX5 (2026-11-20): the welcome sha moves 237af4d4 -> 57ebe2d2\n# (1,930,937 B -> 1,930,947 B, +10 B): fix-4 checker F — the footer links\n# strip pushed its first five links left of the scroll origin at 390\n# (justify-content:center on a 1064px nowrap row in a 374px viewport).\n# Both nowrap .fp-legal-links rules (intro + bridge) now use\n# justify-content:safe center: centred where the row fits (desktop\n# unchanged), starting at the scroll origin on overflow, so all 12 links\n# enter the viewport at some scrollLeft. No other file changes.\nassert welcome_sha.startswith("57ebe2d2"), "welcome sha is not the AGREEMENT-DISTILL-FIX5 welcome sha (2026-11-20: fix-4 checker F — footer strip safe center at phone width)"',
  'welcome-assert');
fs.writeFileSync(P, s);
const out = `${HERE}/fix5-build-v23-staging-worker.py`;
fs.writeFileSync(out, s);
const a = fs.readFileSync(P), b = fs.readFileSync(out);
console.log('build script updated; new sha256:', crypto.createHash('sha256').update(a).digest('hex'), 'bytes:', a.length);
console.log('work copy identical:', a.equals(b));
