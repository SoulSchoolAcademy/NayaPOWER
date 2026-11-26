// File the round-5 portal fix to NEW branch portal-frontpage-fix-20261125-r5,
// created FROM the round-4 branch head (not main), via the git-data API
// (gh-app-api only). Blobs -> tree (base = R4 head tree) -> commit -> ref.
// Files >1 MB go through the blob API (base64). Node only; prints every sha.
// No raw credential anywhere.
import {readFileSync, writeFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
const GH = '/home/hatch/workspace/custom-connectors/custom.legacy-github/bin/gh-app-api';
const REPO = 'SoulSchoolAcademy/NayaPOWER';
const BASE_BRANCH = 'portal-frontpage-fix-20261125-r4';
const BRANCH = 'portal-frontpage-fix-20261125-r5';
const LANE = new URL('./', import.meta.url).pathname;
const DIR = 'TEAM-NITRO/portal-frontpage-fix-20261125/round-5/maker/';
const FILES = ['portal.html', 'identity.html', 'identity-consolidated.html',
  'worker-consolidated.js', 'worker-meta.json', 'sw.js',
  'build-fix-r5.mjs', 'build-worker-r5.mjs', 'verify-r5.mjs',
  'commit-r5.mjs', 'portal-r4.html'];
const api = (method, path, bodyFile) => {
  const args = [method, path];
  if (bodyFile) args.push('@' + bodyFile);
  const out = execFileSync(GH, args, {encoding: 'utf8', maxBuffer: 64 * 1024 * 1024});
  return JSON.parse(out);
};
const baseRef = api('GET', `/repos/${REPO}/git/ref/heads/${BASE_BRANCH}`);
const baseSha = baseRef.object.sha;
console.log('R4 branch head:', baseSha);
const baseCommit = api('GET', `/repos/${REPO}/git/commits/${baseSha}`);
console.log('R4 tree:', baseCommit.tree.sha);
const refBody = LANE + 'evidence/.newref-r5.json';
writeFileSync(refBody, JSON.stringify({ref: 'refs/heads/' + BRANCH, sha: baseSha}));
const created = api('POST', `/repos/${REPO}/git/refs`, refBody);
console.log('branch created:', created.ref, created.object.sha);
const treeEntries = [];
for (const f of FILES) {
  const buf = readFileSync(LANE + f);
  const bodyFile = LANE + 'evidence/.blob-r5-' + f.replace(/[^a-z0-9]/gi, '_') + '.json';
  writeFileSync(bodyFile, JSON.stringify({content: buf.toString('base64'), encoding: 'base64'}));
  const blob = api('POST', `/repos/${REPO}/git/blobs`, bodyFile);
  console.log('blob', f, buf.length, 'B ->', blob.sha);
  treeEntries.push({path: DIR + f, mode: '100644', type: 'blob', sha: blob.sha});
}
const treeFile = LANE + 'evidence/.tree-r5.json';
writeFileSync(treeFile, JSON.stringify({base_tree: baseCommit.tree.sha, tree: treeEntries}));
const tree = api('POST', `/repos/${REPO}/git/trees`, treeFile);
console.log('tree:', tree.sha);
const commitFile = LANE + 'evidence/.commit-r5.json';
writeFileSync(commitFile, JSON.stringify({
  message: "Portal front-page fix ROUND 5 2026-11-25 (two-defect round on the Round 4 base; captain's eye: menu shows words at rest + dotted ring static)\n\nDEFECT 1 — TOP MENU SHOWS WORDS AT REST: FIXED. The hover-only menu is folded in verbatim from the proven hover-fix build (blob 15267a2c, sha 5750da64; checker PASS + eye PASS; Shawn: 'one of the nicest buttons I've seen'): the whole menu CSS region replaced byte-for-byte (eco-tip pills on hover/focus/first-tap, D3 focus ring, single nowrap row at phone, 3x3 grid gone, 1240px wrap guard deleted); the nine nav anchors keep their R4 hrefs/glyphs/colours byte-for-byte — only the label spans became tip spans (12 Elements tip reads '12 Elements of Naya', as harvested); the tip script (clamp + first-tap, 2600ms auto-hide) inserted verbatim. Both menu candidates were rendered with REAL hovers at 390x844 and 1440x900 before choosing: BOTH prove hover-only (rest: all tips opacity 0, single row; hover 9/9: tip opacity 1, gone on mouse-away, each in its own colour). His Nov 24th pick (b) was NOT folded verbatim because it is a different nine (no Skills, no Grand Mission; About Us + Life with Naya; Home is an in-page #entryForm anchor) in bright off-palette colours — folding it would delete two destinations. (a) IS (b)'s hover treatment (tip rules byte-identical to (b), selector renamed .eco-dot -> .eco-item, per the hover-fix checker), applied to the portal's own nine in the deep palette.\n\nDEFECT 2 — DOTTED RING DOES NOT MOVE: NOT REPRODUCED, no ring code changed. On the R4 base the jewel ring (108 .naya-jewel dots, .naya-color-orbit, nayaSpectrum 78s) moves -116 deg over 25s at BOTH widths (phone + desktop), and the tight-annulus pixel change is 48.08% (phone) / 43.55% (desktop) — two independent methods, same answer. The eye's 'zero changed pixels' does not reproduce in Chromium renders of this build; changing a working 78s orbit would be an unasked change to working code. The checker re-proves with the same method.\n\nBuild: 21/21 assertions in build-fix-r5.mjs; portal 13,883,771 B, sha d4bb2102... (+2,989 B vs R4, menu only — diff evidence/portal-diff-r5.txt). Certificate byte-identical (sha 57bdd387...). Design laws: run after staging; the transplant swaps one 17px label rule for one 17px tip rule. Nothing live, nothing to Shawn.",
  tree: tree.sha, parents: [baseSha],
}));
const commit = api('POST', `/repos/${REPO}/git/commits`, commitFile);
console.log('commit:', commit.sha);
const refFile = LANE + 'evidence/.ref-r5.json';
writeFileSync(refFile, JSON.stringify({sha: commit.sha, force: false}));
const ref = api('PATCH', `/repos/${REPO}/git/refs/heads/${BRANCH}`, refFile);
console.log('ref now:', ref.object.sha);
console.log('COMMIT DONE', commit.sha);
