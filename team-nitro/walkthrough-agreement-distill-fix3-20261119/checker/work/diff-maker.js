#!/usr/bin/env node
// diff-maker.js — CHECKER diagnostic: reproduce the MAKER's own transform by
// evaluating the transform constants straight out of run-fix3.js (no retyping),
// then byte-diff the maker's fixed walk against the checker's own fixed walk.
// Answers: does the maker's own script produce the maker's claimed sha
// b068d1da (4,363,239 B), or the checker's ef982267 (4,363,264 B) — and
// exactly which bytes differ (25 B)?
const fs = require('fs');
const crypto = require('crypto');
const runFix2 = require('/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix3-20261119/maker/work/run-fix2-export.js');
const checker = require('./check-fix3.js');
const sha = (s) => crypto.createHash('sha256').update(s, 'utf8').digest('hex');
const count = (s, n) => { let c = 0, i = -1; while ((i = s.indexOf(n, i + 1)) !== -1) c++; return c; };

(async () => {
  const src = fs.readFileSync('/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix3-20261119/maker/work/run-fix3.js', 'utf8');
  // Slice the transform block: from the first fix-3 const to the fixed-sizes print.
  const start = src.indexOf('  const I_ANCHOR =');
  const end = src.indexOf('  // ---- fixed sizes + shas ----');
  if (start < 0 || end < 0) throw new Error('transform block markers not found');
  const block = src.slice(start, end);
  console.log('maker transform block chars: ' + block.length);
  // Execute the block with the maker's own rep1 semantics (count-assert + split/join).
  function makerRep1(s, needle, repl, label) {
    const n = count(s, needle);
    if (n !== 1) throw new Error('MAKER REP ' + label + ': found ' + n);
    return s.split(needle).join(repl);
  }
  const fn = new Function('I', 'WK', 'rep1', block + '\nreturn { I: I, WK: WK };');
  const R = await runFix2();
  const F2 = { U: R.U, W: R.W, WK: R.WK, I: R.I };
  const M = fn(F2.I, F2.WK, makerRep1);
  console.log('MAKER-SCRIPT walk: ' + Buffer.byteLength(M.WK) + 'B sha256 ' + sha(M.WK));
  console.log('MAKER-SCRIPT identity: ' + Buffer.byteLength(M.I) + 'B sha256 ' + sha(M.I));
  console.log('maker claim walk: 4363239B sha256 b068d1da38403878eb0b4a552ea92efec2fe77724d6a12fdef04f98fb8f8089b');
  // Checker's own transform on the same fix-2 bytes.
  const C = checker.applyFix3(F2);
  console.log('CHECKER walk: ' + Buffer.byteLength(C.WK) + 'B sha256 ' + sha(C.WK));
  console.log('CHECKER identity: ' + Buffer.byteLength(C.I) + 'B sha256 ' + sha(C.I));
  console.log('identity identical maker-vs-checker: ' + (M.I === C.I));
  // Byte-diff maker walk vs checker walk.
  if (M.WK !== C.WK) {
    let a = 0;
    while (a < M.WK.length && a < C.WK.length && M.WK[a] === C.WK[a]) a++;
    let bM = M.WK.length, bC = C.WK.length;
    while (bM > a && bC > a && M.WK[bM - 1] === C.WK[bC - 1]) { bM--; bC--; }
    console.log('FIRST DIFF at offset ' + a + ' (maker len ' + M.WK.length + ', checker len ' + C.WK.length + ')');
    console.log('MAKER-only region (' + (bM - a) + ' chars): ' + JSON.stringify(M.WK.slice(a, bM)));
    console.log('CHECKER-only region (' + (bC - a) + ' chars): ' + JSON.stringify(C.WK.slice(a, bC)));
    console.log('maker context before: ' + JSON.stringify(M.WK.slice(Math.max(0, a - 200), a)));
    console.log('maker context after: ' + JSON.stringify(M.WK.slice(bM, bM + 200)));
  } else {
    console.log('walk identical maker-vs-checker');
  }
  // Also: byte-length of each maker insertion (for the 1018 vs 1043 arithmetic).
  const m = (s) => Buffer.byteLength(s, 'utf8');
  // Recompute insertion sizes from the evaluated consts by re-running with markers:
  // (simpler) print the lengths of the four maker insertion deltas via the diff above.
  process.exit(0);
})().catch((e) => { console.error('FATAL', e); process.exit(1); });
