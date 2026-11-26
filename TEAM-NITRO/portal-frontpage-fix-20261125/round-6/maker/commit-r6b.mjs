// Follow-up commit on branch portal-frontpage-fix-20261125-r6: the little-N
// amendment (Shawn's LOCKED decision) on top of commit 7d5fc23b. Blobs ->
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
  'verify-r6.mjs', 'commit-r6.mjs', 'commit-r6b.mjs'];
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
  const bodyFile = LANE + 'evidence/.blob-r6b-' + f.replace(/[^a-z0-9]/gi, '_') + '.json';
  writeFileSync(bodyFile, JSON.stringify({content: buf.toString('base64'), encoding: 'base64'}));
  const blob = api('POST', `/repos/${REPO}/git/blobs`, bodyFile);
  console.log('blob', f, buf.length, 'B ->', blob.sha);
  treeEntries.push({path: DIR + f, mode: '100644', type: 'blob', sha: blob.sha});
}
const treeFile = LANE + 'evidence/.tree-r6b.json';
writeFileSync(treeFile, JSON.stringify({base_tree: headCommit.tree.sha, tree: treeEntries}));
const tree = api('POST', `/repos/${REPO}/git/trees`, treeFile);
console.log('tree:', tree.sha);
const commitFile = LANE + 'evidence/.commit-r6b.json';
writeFileSync(commitFile, JSON.stringify({
  message: 'Portal front-page fix ROUND 6 follow-up 2026-11-26 (the little N — Shawn\'s LOCKED decision, on commit 7d5fc23b)\n\nThe little info-i at the end of the deed text inside the circle is REPLACED by a little N — dead center where the (i) was, upright, static, never spinning. In the R5 base the deed text itself was gone (the deed-sentence <p> held only the red ball), so the front-page wording returns verbatim with the little N inline at its end, and the red ball stays after it on its own centred line. Click the little N and the agreement pops up IN A NUTSHELL carrying that same wording verbatim; Close, backdrop, or Esc shuts it and the page underneath is unchanged. The little N is a different element from the red-orb N: 26px obsidian circle, white Marcellus N, purple glow, NO animation anywhere. The three (i) glyphs left in the file were in comments only — removed, so the file-wide audit reads 0.\n\nBuild: 30/30 assertions in build-fix-r6.mjs; portal 13,890,340 B, sha 6f417f6a... (+3,673 B vs 7d5fc23b, deed only — diff evidence/portal-diff-r6.txt). Certificate byte-identical (sha 57bdd387...). Nothing live, nothing to Shawn.',
  tree: tree.sha, parents: [headSha],
}));
const commit = api('POST', `/repos/${REPO}/git/commits`, commitFile);
console.log('commit:', commit.sha);
const refFile = LANE + 'evidence/.ref-r6b.json';
writeFileSync(refFile, JSON.stringify({sha: commit.sha, force: false}));
const ref = api('PATCH', `/repos/${REPO}/git/refs/heads/${BRANCH}`, refFile);
console.log('ref now:', ref.object.sha);
console.log('COMMIT DONE', commit.sha);
