// File MAKER-REPORT.md (+ this script + commit-r2.mjs) as the head commit on
// the round-2 fix branch. Blobs -> tree (base = branch head tree) -> commit -> ref.
// gh-app-api only. Node only; prints every sha. No raw credential anywhere.
import {readFileSync, writeFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
const GH = '/home/hatch/workspace/custom-connectors/custom.legacy-github/bin/gh-app-api';
const REPO = 'SoulSchoolAcademy/NayaPOWER';
const BRANCH = 'portal-frontpage-fix-20261125-r2';
const LANE = new URL('./', import.meta.url).pathname;
const DIR = 'TEAM-NITRO/portal-frontpage-fix-20261125/round-2/maker/';
const FILES = ['MAKER-REPORT.md', 'commit-r2.mjs', 'commit-report-r2.mjs'];
const api = (method, path, bodyFile) => {
  const args = [method, path];
  if (bodyFile) args.push('@' + bodyFile);
  const out = execFileSync(GH, args, {encoding: 'utf8', maxBuffer: 64 * 1024 * 1024});
  return JSON.parse(out);
};
const head = api('GET', `/repos/${REPO}/git/ref/heads/${BRANCH}`);
const headSha = head.object.sha;
console.log('head:', headSha);
const headCommit = api('GET', `/repos/${REPO}/git/commits/${headSha}`);
const treeEntries = [];
for (const f of FILES) {
  const buf = readFileSync(LANE + f);
  const bodyFile = LANE + 'evidence/.blob-r2r-' + f.replace(/[^a-z0-9]/gi, '_') + '.json';
  writeFileSync(bodyFile, JSON.stringify({content: buf.toString('base64'), encoding: 'base64'}));
  const blob = api('POST', `/repos/${REPO}/git/blobs`, bodyFile);
  console.log('blob', f, buf.length, 'B ->', blob.sha);
  treeEntries.push({path: DIR + f, mode: '100644', type: 'blob', sha: blob.sha});
}
const treeFile = LANE + 'evidence/.tree-r2r.json';
writeFileSync(treeFile, JSON.stringify({base_tree: headCommit.tree.sha, tree: treeEntries}));
const tree = api('POST', `/repos/${REPO}/git/trees`, treeFile);
console.log('tree:', tree.sha);
const commitFile = LANE + 'evidence/.commit-r2r.json';
writeFileSync(commitFile, JSON.stringify({
  message: 'Portal front-page fix ROUND 2 — maker report\n\nStaged portal 1,907,038 B sha 66664c07... / identity 313,224 B sha\n57bdd387... (unchanged) / worker deployment 05f3e980...\nCode commit 4b194f93... on this branch. F1 spin proven by timed captures;\nF2 heading clear at 573x355 fresh + returning. Nothing live, nothing to Shawn.',
  tree: tree.sha, parents: [headSha],
}));
const commit = api('POST', `/repos/${REPO}/git/commits`, commitFile);
console.log('commit:', commit.sha);
const refFile = LANE + 'evidence/.ref-r2r.json';
writeFileSync(refFile, JSON.stringify({sha: commit.sha, force: false}));
const ref = api('PATCH', `/repos/${REPO}/git/refs/heads/${BRANCH}`, refFile);
console.log('ref now:', ref.object.sha);
console.log('COMMIT DONE', commit.sha);
