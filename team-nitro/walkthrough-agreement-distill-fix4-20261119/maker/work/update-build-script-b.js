#!/usr/bin/env node
/* FIX-4b: point the v23 staging build script at the fix-4b input shas
   (identity/unfold/welcome move; walk is byte-identical to fix-4). */
const fs = require('fs');
const crypto = require('crypto');
const P = '/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py';
let s = fs.readFileSync(P, 'utf8');
function rep(anchor, insert, label) {
  const n = s.split(anchor).length - 1;
  if (n !== 1) throw new Error(`${label}: anchor occurs ${n}x (want 1)`);
  s = s.replace(anchor, insert);
}
rep('assert ident_sha.startswith("642013c7"), "identity sha is not the AGREEMENT-DISTILL-FIX4 identity sha (2026-11-20: fix-3 eye A + C — hero name + taken-note clearance at <=480px)"',
  '# AGREEMENT-DISTILL-FIX4b (2026-11-20): the identity sha moves 642013c7 -> fef65d2c\n# (403,714 B -> 404,147 B, +433 B): fix-4 verification found the hero still\n# covered "This certifies that" (2356 px2, taken state) — the line hides at\n# <=480px while the hero shows (taken / is-certified / has-name).\nassert ident_sha.startswith("fef65d2c"), "identity sha is not the AGREEMENT-DISTILL-FIX4b identity sha (2026-11-20: fix-4 verify — certifies line hides while the hero shows, <=480px)"',
  'ident-assert');
rep('assert welcome_sha.startswith("c3cda417"), "welcome sha is not the AGREEMENT-DISTILL-FIX4 welcome sha (2026-11-20: fix-3 eye D + E — 22px title + sign-frame margin at <=480px)"',
  '# AGREEMENT-DISTILL-FIX4b (2026-11-20): the welcome sha moves c3cda417 -> 237af4d4\n# (1,930,495 B -> 1,930,937 B, +442 B): fix-4 verification found the first D\n# rule lost to body.af-deck-on #deckBody .ib-title{25px!important} — the\n# board-37 rule now wins at (1,3,2)!important on deck AND letter.\nassert welcome_sha.startswith("237af4d4"), "welcome sha is not the AGREEMENT-DISTILL-FIX4b welcome sha (2026-11-20: fix-4 verify — board-37 title beats the af-deck !important rule)"',
  'welcome-assert');
rep('assert unfold_sha.startswith("cde8b890"), "unfold sha is not the AGREEMENT-DISTILL-FIX4 unfold sha (2026-11-20: fix-3 eye D — 22px board title at <=480px)"',
  '# AGREEMENT-DISTILL-FIX4b (2026-11-20): the unfold sha moves cde8b890 -> a3b3907f\n# (142,491 B -> 142,532 B, +41 B): fix-4 verification found board 37\'s title\n# is .frame-title, not .ib-title (the first D rule never matched) — the\n# board-37 .frame-title rule now wins at (0,2,1)!important.\nassert unfold_sha.startswith("a3b3907f"), "unfold sha is not the AGREEMENT-DISTILL-FIX4b unfold sha (2026-11-20: fix-4 verify — board-37 .frame-title at 22px)"',
  'unfold-assert');
fs.writeFileSync(P, s);
console.log('build script updated; new sha256:', crypto.createHash('sha256').update(s).digest('hex'), 'bytes:', Buffer.byteLength(s));
