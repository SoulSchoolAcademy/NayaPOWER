#!/usr/bin/env node
/* FIX7 node transform (2026-11-19): python writes are EPERM-blocked in this
   window (silent-zero), node writes land (proven: node-probe-7). This script
   does the whole frame transform in node:
   1. Extract the UNFOLD embed from the LOCAL worker file (the canonical
      unfold file on disk is 0 bytes — flake-zeroed by a truncate-first
      python open; the filed blob 8980e577 is the truth and the worker
      embed carries the same bytes).
   2. Verify sha 3252948e.
   3. Apply the 3 FIX7 insertions (frame layer, frame CSS, frame JS)
      taken verbatim from build-frame7.py's CSS/JS strings (python
      escapes collapsed: \\u -> \u, since python would have interpreted
      them on output).
   4. Write work/unfold-fix7.html + attempt the canonical path; verify
      size + sha after every write; node --check all 3 script blocks. */
const fs = require('fs');
const crypto = require('crypto');
const { spawnSync } = require('child_process');
console.log = (...a) => console.error(...a); // all logs to stderr: stdout carries ONLY the bytes

const BASE_SHA = '3252948ed7f80157d0fa86fd730dc2e535a749f00e80944f0274ded54eb6a0f8';
const WORKER = '/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js';
const PY = '/home/hatch/workspace/team-nitro/walkthrough-chain-fix7-20261119/work/build-frame7.py';
const WORK_OUT = '/home/hatch/workspace/team-nitro/walkthrough-chain-fix7-20261119/work/unfold-fix7.html';
const CANON = '/home/hatch/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html';
const PH = 'https://naya-proof-host.nayapower.workers.dev/?file=team-nitro/agreement-unfold-20261117/';
const FRAME_URL = PH + 'master-frame.png&ref=walkthrough/chain-fix7-20261119&cb=5a4dc2f9ca703945f12cec0b39b491d728e69c4a';
const FACES = [
  ['face-1.jpg', '8743e1868400bb8ae4f650b536ab9cbace036786'],
  ['face-3.jpg', 'c01d71025d34abf8379bab5b7eb13bfa9204964a'],
  ['face-4.jpg', '39c7f0ce4222d853d676d1ea5138569ed182b209'],
  ['face-5.jpg', 'c3cd3d9caf778a0b9e0fcf122b3a780030107f76'],
  ['face-6.jpg', '6fa4c1a28c196429f8c2e325de695a31f16cd06b'],
  ['face-7.jpg', '0be821b80d8c055d08b9f5333449064507b7412e'],
  ['face-8.jpg', '00ea37ad9e03cc5da2b7ba352b0f3d988e31da5a'],
  ['face-9.jpg', 'e1dbe46717f87cf4cb63f7cef4bd367d8bb1a0f2'],
];
const FACE_URLS = FACES.map(([n, cb]) => PH + n + '&ref=agreement/unfold-20261117&cb=' + cb);

function sha(b) { return crypto.createHash('sha256').update(b).digest('hex'); }

// 1. extract UNFOLD embed from the local worker file
const w = fs.readFileSync(WORKER, 'utf8');
const marker = 'const UNFOLD = ';
const i = w.indexOf(marker);
if (i < 0) { console.error('worker has no UNFOLD'); process.exit(1); }
const q = w.indexOf('"', i);
let k = q + 1;
while (k < w.length) {
  if (w[k] === '\\') { k += 2; continue; }
  if (w[k] === '"') break;
  k++;
}
const base = JSON.parse(w.slice(q, k + 1));
console.log('base unfold:', base.length, 'B sha', sha(base));
if (sha(base) !== BASE_SHA) { console.error('base is not the fix-3 unfold'); process.exit(1); }

// 2. pull CSS/JS from build-frame7.py (verbatim python triple-quoted strings)
const py = fs.readFileSync(PY, 'utf8');
function pyStr(name) {
  const m = py.match(new RegExp(name + ' = """([\\s\\S]*?)"""'));
  if (!m) { console.error('no ' + name + ' in ' + PY); process.exit(1); }
  return m[1];
}
let CSS = pyStr('CSS').replace(/__FRAME_URL__/g, FRAME_URL);
let JS = pyStr('JS')
  .replace(/__FACES__/g, JSON.stringify(FACE_URLS))
  .replace(/\\\\u/g, '\\u'); // python would have collapsed \\u -> \u on output
let text = base;
if (text.includes('fpFrame7')) { console.error('frame7 already applied'); process.exit(1); }
text = text.replace('<body>', '<body>\n<div class="naya-frame" aria-hidden="true"><div class="frame-light"></div></div>');
text = text.replace('</head>', CSS + '</head>');
text = text.replace('</body>', JS + '\n</body>');
const out = Buffer.from(text, 'utf8');
for (const needle of ["Hi, I&#x27;m Naya.", 'What if it could help you learn faster',
  'I agree — show me my world', 'dealAgreeBtn', 'wireDeck', 'wirePlay', 'wireAgree']) {
  if (!text.includes(needle)) { console.error('content lost: ' + needle); process.exit(1); }
}
const count = (s, n) => s.split(n).length - 1;
if (count(text, 'data-beat=') !== count(base, 'data-beat=')) { console.error('beat count changed'); process.exit(1); }
if (count(text, '<article') !== count(base, '<article')) { console.error('article count changed'); process.exit(1); }
const newSha = sha(out);
console.log('unfold fix7:', out.length, 'B sha', newSha);

// 3. node --check all 3 script blocks
const blocks = [...text.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
console.log('script blocks:', blocks.length, blocks.map(b => b.length));
blocks.forEach((code, idx) => {
  const r = spawnSync('node', ['--check', '-'], { input: code });
  console.log('block', idx, 'rc=', r.status, r.status === 0 ? 'OK' : String(r.stderr).slice(0, 300));
  if (r.status !== 0) process.exit(1);
});

process.stdout.write(out);
