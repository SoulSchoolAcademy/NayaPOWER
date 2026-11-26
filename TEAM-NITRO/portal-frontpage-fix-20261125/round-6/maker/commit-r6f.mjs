// File the R6f fix round to the EXISTING branch
// portal-frontpage-fix-20261125-r6 (HEAD 7700f1bb...), as a new commit on
// top — git-data API via gh-app-api. Blobs -> tree (base = R6 head tree)
// -> commit -> ref PATCH. Files >1 MB go through the blob API; the 23 MB
// agreement file is piped (base64 -> jq -> gh-app-api, no intermediate
// file). Node only; prints every sha. No raw credential anywhere.
import {readFileSync, writeFileSync} from 'node:fs';
import {execFileSync, execSync} from 'node:child_process';
const GH = '/home/hatch/workspace/custom-connectors/custom.legacy-github/bin/gh-app-api';
const REPO = 'SoulSchoolAcademy/NayaPOWER';
const BRANCH = 'portal-frontpage-fix-20261125-r6';
const LANE = new URL('./', import.meta.url).pathname;
const DIR = 'TEAM-NITRO/portal-frontpage-fix-20261125/round-6/maker/';
const FILES = ['portal.html', 'agreement-v25-fixed-r6f.html', 'identity.html',
  'worker-consolidated.js', 'worker-meta.json', 'sw.js',
  'build-fix-r6f.mjs', 'build-agreement-r6f.mjs', 'build-worker-r6f.mjs',
  'verify-r6f.mjs', 'commit-r6f.mjs',
  'evidence/kv-put-r6f.py', 'evidence/design-laws-r6f-portal.txt',
  'evidence/design-laws-r6f-agreement.txt'];
const api = (method, path, bodyFile) => {
  const args = [method, path];
  if (bodyFile) args.push('@' + bodyFile);
  const out = execFileSync(GH, args, {encoding: 'utf8', maxBuffer: 64 * 1024 * 1024});
  return JSON.parse(out);
};
const apiPipe = (method, path, file) => {
  const cmd = `${GH} ${method} ${path} @<(base64 -w0 ${JSON.stringify(file)} | jq -Rs '{content: ., encoding: "base64"}')`;
  const out = execSync(`bash -c ${JSON.stringify(cmd)}`, {encoding: 'utf8', maxBuffer: 64 * 1024 * 1024});
  return JSON.parse(out);
};
const headRef = api('GET', `/repos/${REPO}/git/ref/heads/${BRANCH}`);
const headSha = headRef.object.sha;
console.log('R6 branch head:', headSha);
if (headSha !== '7700f1bb41b05a505b1d972293fc9c0be9deb3a1')
  throw new Error('R6 branch head moved since the round started: ' + headSha);
const headCommit = api('GET', `/repos/${REPO}/git/commits/${headSha}`);
console.log('head tree:', headCommit.tree.sha);
const treeEntries = [];
for (const f of FILES) {
  const buf = readFileSync(LANE + f);
  const blob = buf.length > 1024 * 1024
    ? apiPipe('POST', `/repos/${REPO}/git/blobs`, LANE + f)
    : api('POST', `/repos/${REPO}/git/blobs`, (() => {
        const bodyFile = LANE + 'evidence/.blob-r6f-' + f.replace(/[^a-z0-9]/gi, '_') + '.json';
        writeFileSync(bodyFile, JSON.stringify({content: buf.toString('base64'), encoding: 'base64'}));
        return bodyFile;
      })());
  console.log('blob', f, buf.length, 'B ->', blob.sha);
  treeEntries.push({path: DIR + f, mode: '100644', type: 'blob', sha: blob.sha});
}
const treeFile = LANE + 'evidence/.tree-r6f.json';
writeFileSync(treeFile, JSON.stringify({base_tree: headCommit.tree.sha, tree: treeEntries}));
const tree = api('POST', `/repos/${REPO}/git/trees`, treeFile);
console.log('tree:', tree.sha);
const commitFile = LANE + 'evidence/.commit-r6f.json';
writeFileSync(commitFile, JSON.stringify({
  message: "Portal front-page fix ROUND 6f 2026-11-26 (fix round on the R6e build, fb721c5d — the captain's decision: repoint, do not amend the brief)\n\nD1 — REPOINT, 4 of 4 agreement entries on the exact URL: the three stage handlers #fpChoiceLetter, #fpBridgeLetter, #fpNextBtn2 (4 relative '/agreement' navigations) now go to https://nayanet.app/agreement, exactly like the orb (#fpCircleN, untouched). Zero relative '/agreement' navigations left in the portal. Proven by real taps at 390x844 + 1440x900: choiceLetter x2, nextBtn2 intro x1, bridgeLetter x2, nextBtn2 deck-end x1 (deck beat 8 of 9) — every one to the exact URL.\n\nD2 — ZERO 'Read the agreement' in the build: the three handlers are RELABELLED, not deleted — 'The agreement ◆' (HTML 3 + JS 2; the deck-end 'Read the full agreement' text is relabelled too). The buttons keep working: they still open the agreement at the exact URL, and #fpNextBtn2 keeps its other function (opening the in-place story in letter views). The two dated comments quoting the old label are reworded; the string count is 0. #fpEnterDeal stays gone.\n\nD3 — WALKTHROUGH WIRING: NOT WIRED, open and blocked-on-walkthrough. /?walk=1 still serves the OLD built-in 15-question walk. The fix3 build is NOT verified: no checker verdict exists for fix3; its branch HEAD has moved past the maker's reported tip (6f0cd84e -> 050f4dee); and its staged bytes (26,139,281 B, sha 3483b790...) do NOT match its filed blob (26,123,858 B, sha 46267e50..., blob 40a91177 — verified by blob-API decode). No wiring was invented or faked.\n\nD5 — (a) phone cover: compact rules at <=640px only, two passes — frame 120px, saying 17px, cover-N 32px, orb-wraps 60px, side padding 8px, gaps 8/6px — LET'S GO bottom 985 -> ~831, inside the 844 viewport, proven by probe. (Pass 1 used a bare `saying` selector that matched nothing; caught by the probe and fixed.) (b) deck total stable: tDur is written ONLY by the audio loadedmetadata handler (the actual recording, 4:18) — paintDeckTime no longer overwrites it with the video duration (4:19); tDur series 4:18 x4 at both widths. (c) OPEN, named: the end-slide body text + franchise image are NOT visible on arrival at phone — the deck is clipped by its .panel-body window (~122px) under the pinned deed row; they ARE reachable by scrolling that inner panel (proven by probe). A clean fix needs the 700px screen/chrome restructured — out of this round's scope, not faked. At desk the board's last line is half-cut the same way. (d) portal story-end: on the last slide the board scrolls just enough that the deed box is whole on arrival at desk. (e) ticker: unchanged — a scrolling marquee clips mid-scroll by definition; named, not changed.\n\nBuilds: build-fix-r6f.mjs 25/25 assertions (portal 13,887,753 B, sha 486a5bbb..., +551 B vs R6e); build-agreement-r6f.mjs 16/16 (agreement 22,936,614 B, sha cae1cf03..., +1,571 B vs R6e); verify-r6f.mjs 48 PASS, zero fails (staged == lane == blob on every route); §11 zero new (portal 81 + 4, agreement 27 + 0, normalized FAIL sets identical to R6e). Staged worker portal-frontpage-fix-20261125-r6-staging: / = 486a5bbb..., /identity.html = 0c11fdb8... (NEW cert, unchanged), /agreement = cae1cf03... (KV agreement-v25-r6f.html, verified MATCH). Nothing live, nothing to Shawn. The round ran over its one-hour max — stated plainly in the maker report.",
  tree: tree.sha, parents: [headSha],
}));
const commit = api('POST', `/repos/${REPO}/git/commits`, commitFile);
console.log('commit:', commit.sha);
const refFile = LANE + 'evidence/.ref-r6f.json';
writeFileSync(refFile, JSON.stringify({sha: commit.sha, force: false}));
const ref = api('PATCH', `/repos/${REPO}/git/refs/heads/${BRANCH}`, refFile);
console.log('ref now:', ref.object.sha);
console.log('COMMIT DONE', commit.sha);
