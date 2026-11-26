// File the round-2 portal fix to NEW branch portal-frontpage-fix-20261125-r2,
// created FROM the round-1 branch head (not main), via the git-data API
// (gh-app-api only). Blobs -> tree (base = R1 head tree) -> commit -> ref.
// Files >1 MB go through the blob API (base64). Node only; prints every sha.
// No raw credential anywhere.
import {readFileSync, writeFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
const GH = '/home/hatch/workspace/custom-connectors/custom.legacy-github/bin/gh-app-api';
const REPO = 'SoulSchoolAcademy/NayaPOWER';
const BASE_BRANCH = 'portal-frontpage-fix-20261125';
const BRANCH = 'portal-frontpage-fix-20261125-r2';
const LANE = new URL('./', import.meta.url).pathname;
const DIR = 'TEAM-NITRO/portal-frontpage-fix-20261125/round-2/maker/';
const FILES = ['portal.html', 'identity.html', 'identity-consolidated.html',
  'worker-consolidated.js', 'worker-meta.json', 'sw.js',
  'build-fix-r2.mjs', 'build-worker-r2.mjs', 'verify-r2.mjs',
  'portal-r1.html'];
const api = (method, path, bodyFile) => {
  const args = [method, path];
  if (bodyFile) args.push('@' + bodyFile);
  const out = execFileSync(GH, args, {encoding: 'utf8', maxBuffer: 64 * 1024 * 1024});
  return JSON.parse(out);
};
const baseRef = api('GET', `/repos/${REPO}/git/ref/heads/${BASE_BRANCH}`);
const baseSha = baseRef.object.sha;
console.log('R1 branch head:', baseSha);
const baseCommit = api('GET', `/repos/${REPO}/git/commits/${baseSha}`);
console.log('R1 tree:', baseCommit.tree.sha);
const refBody = LANE + 'evidence/.newref-r2.json';
writeFileSync(refBody, JSON.stringify({ref: 'refs/heads/' + BRANCH, sha: baseSha}));
const created = api('POST', `/repos/${REPO}/git/refs`, refBody);
console.log('branch created:', created.ref, created.object.sha);
const treeEntries = [];
for (const f of FILES) {
  const buf = readFileSync(LANE + f);
  const bodyFile = LANE + 'evidence/.blob-r2-' + f.replace(/[^a-z0-9]/gi, '_') + '.json';
  writeFileSync(bodyFile, JSON.stringify({content: buf.toString('base64'), encoding: 'base64'}));
  const blob = api('POST', `/repos/${REPO}/git/blobs`, bodyFile);
  console.log('blob', f, buf.length, 'B ->', blob.sha);
  treeEntries.push({path: DIR + f, mode: '100644', type: 'blob', sha: blob.sha});
}
const treeFile = LANE + 'evidence/.tree-r2.json';
writeFileSync(treeFile, JSON.stringify({base_tree: baseCommit.tree.sha, tree: treeEntries}));
const tree = api('POST', `/repos/${REPO}/git/trees`, treeFile);
console.log('tree:', tree.sha);
const commitFile = LANE + 'evidence/.commit-r2.json';
writeFileSync(commitFile, JSON.stringify({
  message: 'Portal front-page fix ROUND 2 2026-11-25 (captain\'s eye findings)\n\nF1: the red N did NOT spin. Diagnosis: the live agreement v25 ball never\nrotates (floaty 5.5s bob only + orbit-spin ring sweep — no rotation to\nharvest); the portal corner img had animation:none (measured t0/t25) while\nonly the thin symmetric ring turned, reading as static. Fix: the portal\'s\nown eco-spin 90s keyframes on the right-corner IMG itself, so the gold N\nturns (80 deg per 20 s, proven by timed captures at 390x844 + 1440x900).\nGloss stays fixed above the ball (light top-left). Asset/alt/size/position/\ndestination unchanged; left N untouched.\n\nF2: at 573px wide the heading wrapped to two lines and "YOU" collided with\nthe top rim ("Welcome back," tight against it). Reproduced at 573x355: the\nportal shrinks to its 250px floor, content narrows to 187px, the heading\'s\ntop line is wider than the circle\'s chord at its height, so the rim slices\nthe word. Fix, narrow+short only (max-width:640px AND max-height:700px):\nheading stays one line (nowrap, tracking 0 — no font-size change, law\ncounts unmoved) and the stack compresses so the heading sits in the wide\nband. Desktop, 390x844, 573x844 untouched.\n\n(a): orbit jewel-dot ring fades while the inner reader is open, so it no\nlonger crosses the reader card\'s text on phone.\n\nDiff vs R1 staged portal: exactly 6 hunks. Design laws: portal 81 + 4\nwarnings, identity 3 — identical to the R2 baseline, zero new. Certificate\nbyte-identical to R2 (sha 57bdd387...). Staged: portal 1,907,038 B sha\n66664c07... / worker deployment 05f3e980... Nothing live, nothing to Shawn.',
  tree: tree.sha, parents: [baseSha],
}));
const commit = api('POST', `/repos/${REPO}/git/commits`, commitFile);
console.log('commit:', commit.sha);
const refFile = LANE + 'evidence/.ref-r2.json';
writeFileSync(refFile, JSON.stringify({sha: commit.sha, force: false}));
const ref = api('PATCH', `/repos/${REPO}/git/refs/heads/${BRANCH}`, refFile);
console.log('ref now:', ref.object.sha);
console.log('COMMIT DONE', commit.sha);
