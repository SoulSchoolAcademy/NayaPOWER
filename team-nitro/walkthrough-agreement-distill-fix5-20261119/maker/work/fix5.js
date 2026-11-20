#!/usr/bin/env node
/* FIX-5 maker transform — defect F only (footer links unreachable at 390).
   Operates on base-welcome-staged.html (fix-4b bytes, verified); writes
   fix5-welcome-staged.html.
   Change: `justify-content:center` -> `justify-content:safe center` on the
   TWO nowrap .fp-legal-links rules (intro + bridge). Nothing else.
   Why safe center: the centred 1064px row in a 374px viewport pushes the
   row start left of the scroll origin, so links 1-5 sit at negative x at
   every scrollLeft and can never be reached. `safe center` centres only
   when the row fits; on overflow it aligns to the start (the scroll
   origin), so every link enters the viewport at some scrollLeft. Desktop
   is unchanged: at 1920 the row fits, so it still centres exactly as
   before. Fallback is graceful: a browser that does not understand `safe`
   drops the declaration, leaving justify-content:normal -> flex-start
   behaviour for a flex row — still reachable.
   Each anchor must occur exactly once; the script refuses otherwise. */
const fs = require('fs');
const crypto = require('crypto');
const HERE = __dirname;
function sha(b) { return crypto.createHash('sha256').update(b).digest('hex'); }
function rep(s, anchor, insert, label) {
  const n = s.split(anchor).length - 1;
  if (n !== 1) throw new Error(`${label}: anchor occurs ${n}x (want 1)`);
  return s.replace(anchor, insert);
}
let s = fs.readFileSync(`${HERE}/base-welcome-staged.html`, 'utf8');
const before = { bytes: Buffer.byteLength(s), sha: sha(s) };
s = rep(s,
  'html.fp-locked body.fp-stage-on.fp-intro #fpLegal .fp-legal-links{display:flex;flex-wrap:nowrap;overflow-x:auto;justify-content:center;',
  'html.fp-locked body.fp-stage-on.fp-intro #fpLegal .fp-legal-links{display:flex;flex-wrap:nowrap;overflow-x:auto;justify-content:safe center;',
  'F-intro-rule');
s = rep(s,
  'html.fp-locked body.fp-stage-on.fp-bridge #fpLegal .fp-legal-links{display:flex;flex-wrap:nowrap;overflow-x:auto;justify-content:center;',
  'html.fp-locked body.fp-stage-on.fp-bridge #fpLegal .fp-legal-links{display:flex;flex-wrap:nowrap;overflow-x:auto;justify-content:safe center;',
  'F-bridge-rule');
fs.writeFileSync(`${HERE}/fix5-welcome-staged.html`, s);
const after = { bytes: Buffer.byteLength(s), sha: sha(s) };
console.log('BEFORE', JSON.stringify(before));
console.log('AFTER ', JSON.stringify(after));
console.log('DELTA BYTES', after.bytes - before.bytes, '(expect +10: "safe " x2)');
// Reconstruction proof: undo the two values -> must be byte-identical to base.
const back = s
  .replace('fp-intro #fpLegal .fp-legal-links{display:flex;flex-wrap:nowrap;overflow-x:auto;justify-content:safe center;',
           'fp-intro #fpLegal .fp-legal-links{display:flex;flex-wrap:nowrap;overflow-x:auto;justify-content:center;')
  .replace('fp-bridge #fpLegal .fp-legal-links{display:flex;flex-wrap:nowrap;overflow-x:auto;justify-content:safe center;',
           'fp-bridge #fpLegal .fp-legal-links{display:flex;flex-wrap:nowrap;overflow-x:auto;justify-content:center;');
const base = fs.readFileSync(`${HERE}/base-welcome-staged.html`, 'utf8');
console.log('RECONSTRUCTION byte-identical to base:', back === base);
if (back !== base) throw new Error('reconstruction mismatch');
// Count occurrences of the new value and confirm no other justify changed.
console.log('safe center occurrences:', s.split('justify-content:safe center').length - 1);
console.log('remaining nowrap justify-content:center occurrences:',
  (s.match(/flex-wrap:nowrap;overflow-x:auto;justify-content:center/g) || []).length);
