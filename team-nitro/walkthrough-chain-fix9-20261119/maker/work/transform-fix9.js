#!/usr/bin/env node
/* FIX9 node transform (2026-11-19): apply the FIX9 insertions to the fix-8
   unfold bytes.
   1. Extract the UNFOLD embed from the LOCAL worker file (fix-8 worker).
   2. Verify sha 11130770.
   3. Apply the FIX9 insertions (frame CSS9 + JS9) taken verbatim from
      build-frame9.py's CSS9/JS9 strings (literal UTF-8).
   4. Guards: fix-8 present, fix-9 absent, content needles intact, beat /
      article counts unchanged, no 'Welcome' button/pill introduced
      (F8), no forbidden media wired (F9 — no audio, no mp3, no m4a).
   5. node --check every script block. stdout carries ONLY the bytes. */
const fs = require('fs');
const crypto = require('crypto');
const { spawnSync } = require('child_process');
console.log = (...a) => console.error(...a); // all logs to stderr: stdout carries ONLY the bytes

const BASE_SHA = '11130770398575ba407da0f9acca254d946c03daa76852cfebc1763bd76bff32';
const WORKER = '/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js';
const PY = '/home/hatch/workspace/team-nitro/walkthrough-chain-fix9-20261119/maker/work/build-frame9.py';

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
console.log('base unfold:', base.length, 'chars sha', sha(Buffer.from(base, 'utf8')));
if (sha(Buffer.from(base, 'utf8')) !== BASE_SHA) { console.error('base is not the fix-8 unfold'); process.exit(1); }

// 2. pull CSS9/JS9 from build-frame9.py (verbatim python triple-quoted strings)
const py = fs.readFileSync(PY, 'utf8');
function pyStr(name) {
  const m = py.match(new RegExp(name + ' = """([\\s\\S]*?)"""'));
  if (!m) { console.error('no ' + name + ' in ' + PY); process.exit(1); }
  return m[1];
}
const CSS = pyStr('CSS9');
const JS = pyStr('JS9');
if (CSS.includes('__') || JS.includes('__')) { console.error('placeholder left'); process.exit(1); }

let text = base;
if (!text.includes('fpFrame8')) { console.error('base is not fix-8 (no fpFrame8)'); process.exit(1); }
if (text.includes('fpFrame9')) { console.error('frame9 already applied'); process.exit(1); }
text = text.replace('</head>', CSS + '</head>');
text = text.replace('</body>', JS + '\n</body>');
const out = Buffer.from(text, 'utf8');
for (const needle of ["Hi, I&#x27;m Naya.", 'What if it could help you learn faster',
  'I agree — show me my world', 'dealAgreeBtn', 'wireDeck', 'wirePlay', 'wireAgree',
  'fpFrame7', 'fpFrame8', 'fpFrame9', 'fpMediaFrame', 'fpAnthemVideoBtn', 'wireFrame9']) {
  if (!text.includes(needle)) { console.error('content lost: ' + needle); process.exit(1); }
}
const count = (s, n) => s.split(n).length - 1;
if (count(text, 'data-beat=') !== count(base, 'data-beat=')) { console.error('beat count changed'); process.exit(1); }
if (count(text, '<article') !== count(base, '<article')) { console.error('article count changed'); process.exit(1); }
// F8: no Welcome button/pill introduced — the added blocks must not contain
// a button whose label carries the word Welcome.
const added = CSS + JS;
if (/Welcome/i.test(added)) { console.error('F8 VIOLATION: added blocks mention Welcome'); process.exit(1); }
// F9: the wrong files must never be wired. The mp3 is not wired either
// (Shawn has NOT given the audio yet — the audio is cut from his captioned
// video, which has not arrived; nothing is substituted). Any reference to
// the mp3, the Oct-29 mp4, or the NotebookLM m4a files fails the build.
if (/Inside_the_NayaNET|b60233efb19466a0356330778ce38d5363d38cc77ca87435a64187d4c20eef19|agreement-naya-voice|62bf05e6|<audio/.test(text)) {
  console.error('F9 VIOLATION: forbidden media referenced'); process.exit(1);
}
const newSha = sha(out);
console.log('unfold fix9:', out.length, 'B sha', newSha);

// 3. node --check every script block
const blocks = [...text.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
console.log('script blocks:', blocks.length, blocks.map(b => b.length));
blocks.forEach((code, idx) => {
  const r = spawnSync('node', ['--check', '-'], { input: code });
  console.log('block', idx, 'rc=', r.status, r.status === 0 ? 'OK' : String(r.stderr).slice(0, 300));
  if (r.status !== 0) process.exit(1);
});

process.stdout.write(out);
