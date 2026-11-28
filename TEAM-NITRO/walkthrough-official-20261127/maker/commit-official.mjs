// File the OFFICIAL walkthrough (small files) to NEW branch
// walkthrough-official-20261127, created FROM the v3 branch head,
// via the git-data API (gh-app-api only). Blobs -> tree (base = v3 head
// tree) -> commit -> ref. The two 47 MB files (portal.html,
// worker-consolidated.js) and the 13.9 MB v1 base are NOT filed here —
// the blobs API 422s payloads that size (v3 precedent); they are staged
// and verified, with shas in MAKER-REPORT.md. Node only; prints every sha.
import {readFileSync, writeFileSync, mkdirSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
const GH = '/home/hatch/workspace/custom-connectors/custom.legacy-github/bin/gh-app-api';
const REPO = 'SoulSchoolAcademy/NayaPOWER';
const BASE_BRANCH = 'portal-frontpage-fix-20261125-r5-phone-v3';
const BRANCH = 'walkthrough-official-20261127';
const LANE = new URL('./', import.meta.url).pathname;
const DIR = 'TEAM-NITRO/walkthrough-official-20261127/maker/';
const FILES = ['identity.html', 'identity-consolidated.html',
  'worker-meta.json', 'sw.js',
  'build-official.mjs', 'build-worker-official.mjs', 'fix-cert.mjs', 'commit-official.mjs',
  'phone-section3.html', 'phone-style3.html', 'phone-script3.html',
  'steps.js', 'engine.js', 'MAKER-REPORT.md',
  'kv-put-video.py', 'enable-subdomain-official.py',
  'evidence/probe-official.py', 'evidence/probe-official.log',
  'evidence/official-390-end.png', 'evidence/official-390-trio-g1.png',
  'evidence/official-1440-end.png', 'evidence/official-1440-trio.png'];
mkdirSync(LANE + 'evidence', {recursive: true});
const api = (method, path, bodyFile) => {
  const args = [method, path];
  if (bodyFile) args.push('@' + bodyFile);
  const out = execFileSync(GH, args, {encoding: 'utf8', maxBuffer: 64 * 1024 * 1024});
  return JSON.parse(out);
};
const baseRef = api('GET', `/repos/${REPO}/git/ref/heads/${BASE_BRANCH}`);
const baseSha = baseRef.object.sha;
console.log('v3 branch head:', baseSha);
const baseCommit = api('GET', `/repos/${REPO}/git/commits/${baseSha}`);
console.log('v3 tree:', baseCommit.tree.sha);
const refBody = LANE + 'evidence/.newref-official.json';
writeFileSync(refBody, JSON.stringify({ref: 'refs/heads/' + BRANCH, sha: baseSha}));
const created = api('POST', `/repos/${REPO}/git/refs`, refBody);
console.log('branch created:', created.ref, created.object.sha);
const treeEntries = [];
for (const f of FILES) {
  const buf = readFileSync(LANE + f);
  const bodyFile = LANE + 'evidence/.blob-official-' + f.replace(/[^a-z0-9]/gi, '_') + '.json';
  writeFileSync(bodyFile, JSON.stringify({content: buf.toString('base64'), encoding: 'base64'}));
  const blob = api('POST', `/repos/${REPO}/git/blobs`, bodyFile);
  console.log('blob', f, buf.length, 'B ->', blob.sha);
  treeEntries.push({path: DIR + f, mode: '100644', type: 'blob', sha: blob.sha});
}
const treeFile = LANE + 'evidence/.tree-official.json';
writeFileSync(treeFile, JSON.stringify({base_tree: baseCommit.tree.sha, tree: treeEntries}));
const tree = api('POST', `/repos/${REPO}/git/trees`, treeFile);
console.log('tree:', tree.sha);
const commitFile = LANE + 'evidence/.commit-official.json';
writeFileSync(commitFile, JSON.stringify({
  message: "Official walkthrough on the R5 portal 2026-11-27 (staged only, nothing live)\n\nPortal R5 -> certificate (no Jump back in, no Install App, raised name, live digit-tile date/time, ENTER -> /?walk=1 same host) -> 23 Black Diamond phone frames in 8 trios: live, age+language, gender+faith+ethnicity, favorites, industry+skills+connect+categories, video, motto, vision, goal, mission, love, don't love, thing, promise, gift, benefit, unique, connect, work, education, experience, achievements, values+stand for. End: answers -> Hub -> pricing. NO Skip anywhere, no name screen, gender no default, no church question, no Spotify. Pictures harvested verbatim (locked map: Vision->3 Nanoverse, Mission->4 How Naya Works, Goal->1 The Vault, Thing->7 Auto Organizer, Promise->5 Smart Vault, Connect->6 Smart Match, Benefit->2 How Current Works; Values->the five pillars). Video: the direct 9:16 file, ONE spot mid-flow, from KV (/naya-video.mp4).\n\nStaged: https://official-walkthrough-staging.nayapower.workers.dev/ — portal 47,430,066 B sha 1677214b..., certificate 316,048 B sha f1f69cc9..., worker deployment 12b9905f..., all three routes curl-verified byte-identical. Build 36/36 assertions; probe 123 PASS at 390x844 (full walk, real taps, 0 real page errors) + 1440x900 end screen whole, 0 page errors.\n\nOpen: '28-frame' vs 23 phones (brief's own list yields 23); pricing is a button not an auto-popup; complete() still posts to the walkthrough-15 staging backend (accepted certified alias shawn at both widths — new answer keys unproven as a real citizen claim); About/Skills pages not built here (the walkthrough collects their material); Shawn's eye is the final gate.\n\nNOTE: portal.html (47,430,066 B) and worker-consolidated.js (47,772,462 B) are NOT in this commit — the blobs API 422s payloads that size (v3 precedent). They are staged, byte-verified, and recorded with shas in MAKER-REPORT.md in this lane.",
  tree: tree.sha, parents: [baseSha],
}));
const commit = api('POST', `/repos/${REPO}/git/commits`, commitFile);
console.log('commit:', commit.sha);
const refFile = LANE + 'evidence/.ref-official.json';
writeFileSync(refFile, JSON.stringify({sha: commit.sha, force: false}));
const ref = api('PATCH', `/repos/${REPO}/git/refs/heads/${BRANCH}`, refFile);
console.log('ref now:', ref.object.sha);
console.log('COMMIT DONE', commit.sha);
