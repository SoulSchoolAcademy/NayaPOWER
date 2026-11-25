// File the front-page fix round to NEW branch portal-frontpage-fix-20261125
// via the git-data API (gh-app-api only). Create branch from main, then
// blobs -> tree (base = main head tree) -> commit -> ref update.
// Files >1 MB go through the blob API (base64). Node only; prints every sha.
// No raw credential anywhere.
import {readFileSync, writeFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
const GH = '/home/hatch/workspace/custom-connectors/custom.legacy-github/bin/gh-app-api';
const REPO = 'SoulSchoolAcademy/NayaPOWER';
const BRANCH = 'portal-frontpage-fix-20261125';
const LANE = new URL('./', import.meta.url).pathname;
const DIR = 'TEAM-NITRO/portal-frontpage-fix-20261125/maker/';
const FILES = ['portal.html', 'identity.html', 'identity-consolidated.html',
  'worker-consolidated.js', 'worker-meta.json', 'sw.js',
  'build-fix.mjs', 'build-worker.mjs', 'verify-fix.mjs'];
const api = (method, path, bodyFile) => {
  const args = [method, path];
  if (bodyFile) args.push('@' + bodyFile);
  const out = execFileSync(GH, args, {encoding: 'utf8', maxBuffer: 64 * 1024 * 1024});
  return JSON.parse(out);
};
const mainRef = api('GET', `/repos/${REPO}/git/ref/heads/main`);
const mainSha = mainRef.object.sha;
console.log('main head:', mainSha);
const mainCommit = api('GET', `/repos/${REPO}/git/commits/${mainSha}`);
console.log('main tree:', mainCommit.tree.sha);
const refBody = LANE + 'evidence/.newref.json';
writeFileSync(refBody, JSON.stringify({ref: 'refs/heads/' + BRANCH, sha: mainSha}));
const created = api('POST', `/repos/${REPO}/git/refs`, refBody);
console.log('branch created:', created.ref, created.object.sha);
const treeEntries = [];
for (const f of FILES) {
  const buf = readFileSync(LANE + f);
  const bodyFile = LANE + 'evidence/.blob-' + f.replace(/[^a-z0-9]/gi, '_') + '.json';
  writeFileSync(bodyFile, JSON.stringify({content: buf.toString('base64'), encoding: 'base64'}));
  const blob = api('POST', `/repos/${REPO}/git/blobs`, bodyFile);
  console.log('blob', f, buf.length, 'B ->', blob.sha);
  treeEntries.push({path: DIR + f, mode: '100644', type: 'blob', sha: blob.sha});
}
const treeFile = LANE + 'evidence/.tree.json';
writeFileSync(treeFile, JSON.stringify({base_tree: mainCommit.tree.sha, tree: treeEntries}));
const tree = api('POST', `/repos/${REPO}/git/trees`, treeFile);
console.log('tree:', tree.sha);
const commitFile = LANE + 'evidence/.commit.json';
writeFileSync(commitFile, JSON.stringify({
  message: 'Portal front-page fix 2026-11-25 (Shawn\'s eye, voice call ~15:51-15:52 MST)\n\nDefect 1: the wall of text under the name input is off the new-user front\npage. The agreement sentence now lives verbatim as PARAS[0] of the inner\nagreement reader behind the info trigger; the front page is just the\ngreeting + name input + Enter button + the info trigger, centred.\n\nDefect 2: the wrong red N bottom-right (small static PNG disc, 13,790 B)\nis replaced by the official red N harvested byte-for-byte from live\nagreement v25 (EMBED.ball, WEBP 182,452 B, 1600x1600, sha 2a4b10fd...),\nalt text harvested verbatim, jewel-gloss highlight from agreement v25\nverbatim (selector renamed only). It lights up (red hover glow) and spins\n(orbit ring, eco-spin 90s). Black N bottom-left untouched (EMBED.logo).\n\nNothing else changed: diff vs R2 staged portal is exactly 5 hunks.\nStaged: portal 1,904,285 B sha 737fca6b... / identity 313,224 B sha\n57bdd387... (unchanged) / worker deployment 3e2a3c64... Nothing live,\nnothing to Shawn.',
  tree: tree.sha, parents: [mainSha],
}));
const commit = api('POST', `/repos/${REPO}/git/commits`, commitFile);
console.log('commit:', commit.sha);
const refFile = LANE + 'evidence/.ref.json';
writeFileSync(refFile, JSON.stringify({sha: commit.sha, force: false}));
const ref = api('PATCH', `/repos/${REPO}/git/refs/heads/${BRANCH}`, refFile);
console.log('ref now:', ref.object.sha);
console.log('COMMIT DONE', commit.sha);
