// Follow-up commit on branch portal-frontpage-fix-20261125-r6: the little-N
// amendment (Shawn's LOCKED decision) on top of commit b2ab86d4. Blobs ->
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
  'verify-r6.mjs', 'commit-r6.mjs', 'commit-r6c.mjs'];
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
  const bodyFile = LANE + 'evidence/.blob-r6c-' + f.replace(/[^a-z0-9]/gi, '_') + '.json';
  writeFileSync(bodyFile, JSON.stringify({content: buf.toString('base64'), encoding: 'base64'}));
  const blob = api('POST', `/repos/${REPO}/git/blobs`, bodyFile);
  console.log('blob', f, buf.length, 'B ->', blob.sha);
  treeEntries.push({path: DIR + f, mode: '100644', type: 'blob', sha: blob.sha});
}
const treeFile = LANE + 'evidence/.tree-r6c.json';
writeFileSync(treeFile, JSON.stringify({base_tree: headCommit.tree.sha, tree: treeEntries}));
const tree = api('POST', `/repos/${REPO}/git/trees`, treeFile);
console.log('tree:', tree.sha);
const commitFile = LANE + 'evidence/.commit-r6c.json';
writeFileSync(commitFile, JSON.stringify({
  message: 'Portal front-page fix ROUND 6 follow-up 2026-11-26 (probe fixes, on commit b2ab86d4)\n\nThe R6 probe caught two defects before anything reached the checker:\n(1) SYNTAX ERROR — the D5 keep-branch replacement ended with one stray "}" which closed the render() letter/letterPage branch early and orphaned the next "else if" — the whole stage IIFE failed to parse at runtime (pageerror "Unexpected token \'else\'" on every load; window.__fpStage undefined; the stage never opened). The stray brace is removed (letter + letterPage branches). (2) PHONE FRONT PAGE — place() is dead code in the R5 base: its guard requires #fpDeedReader, an element that no longer exists, so the deed sentence never moves out of the circle on phone; the restored deed text (373px) overflowed the 288px phone circle and pushed the heading, name field, and Enter button out of view. The guard drops the reader requirement and the two reader moves are null-guarded. The deed sentence is now a block (text centred, red ball on its own centred line below, little N alone at the text\'s end).\n\nBuild: 32/32 assertions in build-fix-r6.mjs, including a new vm.Script compile check on every inline script (string assertions could not see this class of break). Portal 13,890,488 B, sha c9c27f4c... (+148 B vs b2ab86d4). Certificate byte-identical (sha 57bdd387...). Nothing live, nothing to Shawn.',
  tree: tree.sha, parents: [headSha],
}));
const commit = api('POST', `/repos/${REPO}/git/commits`, commitFile);
console.log('commit:', commit.sha);
const refFile = LANE + 'evidence/.ref-r6c.json';
writeFileSync(refFile, JSON.stringify({sha: commit.sha, force: false}));
const ref = api('PATCH', `/repos/${REPO}/git/refs/heads/${BRANCH}`, refFile);
console.log('ref now:', ref.object.sha);
console.log('COMMIT DONE', commit.sha);
