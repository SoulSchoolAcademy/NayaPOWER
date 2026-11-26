// Follow-up commit on branch portal-frontpage-fix-20261125-r6: the little-N
// amendment (Shawn's LOCKED decision) on top of commit f9e071c6. Blobs ->
// tree (base = r6 head tree) -> commit -> PATCH ref. No branch creation
// (the branch already exists). Node only; prints every sha.
import {readFileSync, writeFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
const GH = '/home/hatch/workspace/custom-connectors/custom.legacy-github/bin/gh-app-api';
const REPO = 'SoulSchoolAcademy/NayaPOWER';
const BRANCH = 'portal-frontpage-fix-20261125-r6';
const LANE = new URL('./', import.meta.url).pathname;
const DIR = 'TEAM-NITRO/portal-frontpage-fix-20261125/round-6/maker/';
const FILES = ['portal.html', 'worker-consolidated.js', 'build-fix-r6.mjs',
  'verify-r6.mjs', 'commit-r6.mjs', 'commit-r6d.mjs'];
const api = (method, path, bodyFile) => {
  const args = [method, path];
  if (bodyFile) args.push('@' + bodyFile);
  const out = execFileSync(GH, args, {encoding: 'utf8', maxBuffer: 64 * 1024 * 1024});
  return JSON.parse(out);
};
const headRef = api('GET', `/repos/${REPO}/git/ref/heads/${BRANCH}`);
const headSha = headRef.object.sha;
console.log('R6 branch head:', headSha);
const headCommit = api('GET', `/repos/${REPO}/git/commits/${headSha}`);
console.log('R6 tree:', headCommit.tree.sha);
const treeEntries = [];
for (const f of FILES) {
  const buf = readFileSync(LANE + f);
  const bodyFile = LANE + 'evidence/.blob-r6d-' + f.replace(/[^a-z0-9]/gi, '_') + '.json';
  writeFileSync(bodyFile, JSON.stringify({content: buf.toString('base64'), encoding: 'base64'}));
  const blob = api('POST', `/repos/${REPO}/git/blobs`, bodyFile);
  console.log('blob', f, buf.length, 'B ->', blob.sha);
  treeEntries.push({path: DIR + f, mode: '100644', type: 'blob', sha: blob.sha});
}
const treeFile = LANE + 'evidence/.tree-r6d.json';
writeFileSync(treeFile, JSON.stringify({base_tree: headCommit.tree.sha, tree: treeEntries}));
const tree = api('POST', `/repos/${REPO}/git/trees`, treeFile);
console.log('tree:', tree.sha);
const commitFile = LANE + 'evidence/.commit-r6d.json';
writeFileSync(commitFile, JSON.stringify({
  message: 'Portal front-page fix ROUND 6 follow-up 2026-11-26 (probe fix 2 — nutshell stacking, on commit f9e071c6)\n\nThe R6 probe caught a third defect: on phone, the nutshell pop-up sat inside .portal while place() moves the deed sentence (with the red ball) OUT of the portal into .stage — so the pop-up rendered UNDER the moved sentence and the red ball intercepted the Close tap (the button was untappable). The pop-up div + its script now live at the end of <body>, in the root stacking context, above everything. No other change: deed text, little N, and the repaired place() are as in f9e071c6.\n\nBuild: 32/32 assertions in build-fix-r6.mjs (vm.Script compile check on all 11 inline scripts). Portal 13,890,489 B, sha 272b6e3d... (+1 B vs f9e071c6 — the move only). Certificate byte-identical (sha 57bdd387...). Nothing live, nothing to Shawn.',
  tree: tree.sha, parents: [headSha],
}));
const commit = api('POST', `/repos/${REPO}/git/commits`, commitFile);
console.log('commit:', commit.sha);
const refFile = LANE + 'evidence/.ref-r6d.json';
writeFileSync(refFile, JSON.stringify({sha: commit.sha, force: false}));
const ref = api('PATCH', `/repos/${REPO}/git/refs/heads/${BRANCH}`, refFile);
console.log('ref now:', ref.object.sha);
console.log('COMMIT DONE', commit.sha);
