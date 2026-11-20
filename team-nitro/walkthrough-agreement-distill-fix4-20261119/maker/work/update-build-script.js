#!/usr/bin/env node
/* FIX-4: point the v23 staging build script at the fix-4 input shas.
   Reads ~/workspace/team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py,
   updates the four input asserts (walk/identity/welcome/unfold) from the
   fix-3 shas to the fix-4 shas, each asserted exactly once. Writes the
   script back in place (same dir, verified by sha after). */
const fs = require('fs');
const P = '/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py';
let s = fs.readFileSync(P, 'utf8');
function rep(anchor, insert, label) {
  const n = s.split(anchor).length - 1;
  if (n !== 1) throw new Error(`${label}: anchor occurs ${n}x (want 1)`);
  s = s.replace(anchor, insert);
}
rep('assert walk_sha.startswith("ef982267"), "walk sha is not the AGREEMENT-DISTILL-FIX3 walk sha (2026-11-20: F9b door guard — proceed() + claim-gate timer hold while the door is visible; explicit continue dismisses it)"',
  '# AGREEMENT-DISTILL-FIX4 (2026-11-20): the walk sha moves ef982267 -> 856d392c\n# (4,363,264 B -> 4,363,683 B, +419 B): fix-3 eye B — the door heading gets\n# 80px side padding at <=480px so its first/last letters clear the corner jewels.\nassert walk_sha.startswith("856d392c"), "walk sha is not the AGREEMENT-DISTILL-FIX4 walk sha (2026-11-20: fix-3 eye B — door heading side padding at <=480px)"',
  'walk-assert');
rep('assert ident_sha.startswith("51776174"), "identity sha is not the AGREEMENT-DISTILL-FIX3 identity sha (2026-11-20: F9a paired pre-fill + hero paint after load paint)"',
  '# AGREEMENT-DISTILL-FIX4 (2026-11-20): the identity sha moves 51776174 -> 642013c7\n# (402,647 B -> 403,714 B, +1,067 B): fix-3 eye A + C — hero name 52px -> 28px\n# + 16px zone margin at <=480px (clears the certificate title); the taken-note\n# banner gets 76px side padding and the bottom-center frame stone hides while\n# the taken note shows (taken state only, <=480px).\nassert ident_sha.startswith("642013c7"), "identity sha is not the AGREEMENT-DISTILL-FIX4 identity sha (2026-11-20: fix-3 eye A + C — hero name + taken-note clearance at <=480px)"',
  'ident-assert');
rep('assert welcome_sha.startswith("3874b7eb"), "welcome sha is not the AGREEMENT-DISTILL-FIX3 welcome sha (2026-11-20: fix-2 bytes carried forward; welcome unchanged in fix-3)"',
  '# AGREEMENT-DISTILL-FIX4 (2026-11-20): the welcome sha moves 3874b7eb -> c3cda417\n# (1,929,575 B -> 1,930,495 B, +920 B): fix-3 eye D + E — board title 25px ->\n# 22px at <=480px (clears the top-right photo on the final board) and the\n# deck/letter sign frame gains 64px top margin at <=480px (photo below the\n# text box). Footer links strip unchanged (proven scrollable).\nassert welcome_sha.startswith("c3cda417"), "welcome sha is not the AGREEMENT-DISTILL-FIX4 welcome sha (2026-11-20: fix-3 eye D + E — 22px title + sign-frame margin at <=480px)"',
  'welcome-assert');
rep('assert unfold_sha.startswith("50876fff"), "unfold sha is not the AGREEMENT-DISTILL-FIX3 unfold sha (2026-11-20: fix-2 bytes carried forward; unfold unchanged in fix-3)"',
  '# AGREEMENT-DISTILL-FIX4 (2026-11-20): the unfold sha moves 50876fff -> cde8b890\n# (142,120 B -> 142,491 B, +371 B): fix-3 eye D — board title 25px -> 22px at\n# <=480px so "Congratulations" clears the top-right diamond orb + avatar.\nassert unfold_sha.startswith("cde8b890"), "unfold sha is not the AGREEMENT-DISTILL-FIX4 unfold sha (2026-11-20: fix-3 eye D — 22px board title at <=480px)"',
  'unfold-assert');
fs.writeFileSync(P, s);
const crypto = require('crypto');
console.log('build script updated; new sha256:', crypto.createHash('sha256').update(s).digest('hex'), 'bytes:', Buffer.byteLength(s));
