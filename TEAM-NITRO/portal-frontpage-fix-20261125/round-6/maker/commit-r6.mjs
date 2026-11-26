// File the round-6 portal fix to NEW branch portal-frontpage-fix-20261125-r6,
// created FROM the round-5 branch head (not main), via the git-data API
// (gh-app-api only). Blobs -> tree (base = R5 head tree) -> commit -> ref.
// Files >1 MB go through the blob API (base64). Node only; prints every sha.
// No raw credential anywhere.
import {readFileSync, writeFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
const GH = '/home/hatch/workspace/custom-connectors/custom.legacy-github/bin/gh-app-api';
const REPO = 'SoulSchoolAcademy/NayaPOWER';
const BASE_BRANCH = 'portal-frontpage-fix-20261125-r5';
const BRANCH = 'portal-frontpage-fix-20261125-r6';
const LANE = new URL('./', import.meta.url).pathname;
const DIR = 'TEAM-NITRO/portal-frontpage-fix-20261125/round-6/maker/';
const FILES = ['portal.html', 'identity.html', 'identity-consolidated.html',
  'worker-consolidated.js', 'worker-meta.json', 'sw.js',
  'build-fix-r6.mjs', 'build-worker-r6.mjs', 'verify-r6.mjs',
  'commit-r6.mjs', 'portal-r5.html'];
const api = (method, path, bodyFile) => {
  const args = [method, path];
  if (bodyFile) args.push('@' + bodyFile);
  const out = execFileSync(GH, args, {encoding: 'utf8', maxBuffer: 64 * 1024 * 1024});
  return JSON.parse(out);
};
const baseRef = api('GET', `/repos/${REPO}/git/ref/heads/${BASE_BRANCH}`);
const baseSha = baseRef.object.sha;
console.log('R5 branch head:', baseSha);
const baseCommit = api('GET', `/repos/${REPO}/git/commits/${baseSha}`);
console.log('R4 tree:', baseCommit.tree.sha);
const refBody = LANE + 'evidence/.newref-r6.json';
writeFileSync(refBody, JSON.stringify({ref: 'refs/heads/' + BRANCH, sha: baseSha}));
const created = api('POST', `/repos/${REPO}/git/refs`, refBody);
console.log('branch created:', created.ref, created.object.sha);
const treeEntries = [];
for (const f of FILES) {
  const buf = readFileSync(LANE + f);
  const bodyFile = LANE + 'evidence/.blob-r6-' + f.replace(/[^a-z0-9]/gi, '_') + '.json';
  writeFileSync(bodyFile, JSON.stringify({content: buf.toString('base64'), encoding: 'base64'}));
  const blob = api('POST', `/repos/${REPO}/git/blobs`, bodyFile);
  console.log('blob', f, buf.length, 'B ->', blob.sha);
  treeEntries.push({path: DIR + f, mode: '100644', type: 'blob', sha: blob.sha});
}
const treeFile = LANE + 'evidence/.tree-r6.json';
writeFileSync(treeFile, JSON.stringify({base_tree: baseCommit.tree.sha, tree: treeEntries}));
const tree = api('POST', `/repos/${REPO}/git/trees`, treeFile);
console.log('tree:', tree.sha);
const commitFile = LANE + 'evidence/.commit-r6.json';
writeFileSync(commitFile, JSON.stringify({
  message: "Portal front-page fix ROUND 6 2026-11-26 (the real collective agreement on the portal, on the Round 5 base; Shawn: \"Put the real collective agreement on the portal. Make it. And make it live.\" + eye additions 1-3)\n\nTHE REAL AGREEMENT, ALREADY IN THE FILE: the v7 text is already in this portal verbatim as the distilled letter (#dealUnfold / #letterBody): 208/223 v7 sentences by machine diff (the 15 misses are the source file header/metadata + heading/stage-direction artefacts). This round is an ENTRY + PRESENTATION fix, not a text harvest: no v7 sentence reworded, added, or removed.\n\nENTRIES — DIRECT, IN PLACE, EXACT URL: the four front-page entries (circle N, black corner N, red corner N, footer \"Read the agreement\") called openStory(0) — the story, not the agreement. They now call openAgreementDirect(): stage on, letter view, beat 0, first group visible, plus history.pushState to /agreement (the exact agreement URL, https://nayanet.app/agreement on live). The other three \"Read the agreement\" buttons (choice, bridge-final, intro nextBtn2) already navigate to /agreement (relative) — unchanged. The worker /agreement route now SERVES this portal (was a 302 to live); a load on /agreement boots straight into the letter view — no preview intro, no bridge choice, no \"Begin the visual story\" as an entry step. The preview page is gone from both paths. The live /agreement file (v25, 22,953,906 B, sha 2c88513f) is a separate deployment — the live step puts this build on the exact URL.\n\nTHREE BOARDS AT A TIME: the letter view stepped one beat at a time; wireLetterUnfold now reveals the next THREE beats per Keep reading, render() shows the current group of three (letter + letterPage), derive() syncs to the group start, jewel counts groups (19 beats -> 7 groups). Deck untouched.\n\nAGREE WORDING: every \"I agree ◆\" is now \"I agree — show me my world ◆\" (letter, letterPage, agree setNext sites + #letterPageAgree + #dealAgreeBtn). Story end slide already carried it.\n\nSTORY FROM INSIDE ONLY: in the letter/letterPage views the second button reads \"Begin the visual story\" and opens the 27-slide story overlay — inside the agreement view only, never as an entry step. Story untouched.\n\nN UPRIGHT (eye: red-orb gold N sideways ~90 deg): the IMAGE carried eco-spin 90s (R5 checker: corner red N +138.3 deg over ~34.6s — the spin, not a static tilt). The spin is OFF both red-N imgs (circle + corner-right); it stays on the decorative rings (::before conic sheen, 90s — the circle button gains the mirrored ring so it stays alive). Black left N untouched (upright).\n\nBuild: 26/26 assertions in build-fix-r6.mjs; portal 13,886,667 B, sha 0c0b2b7a... (+2,896 B vs R5 — diff evidence/portal-diff-r6.txt). Certificate byte-identical (sha 57bdd387...). Nothing live, nothing to Shawn.",
  tree: tree.sha, parents: [baseSha],
}));
const commit = api('POST', `/repos/${REPO}/git/commits`, commitFile);
console.log('commit:', commit.sha);
const refFile = LANE + 'evidence/.ref-r6.json';
writeFileSync(refFile, JSON.stringify({sha: commit.sha, force: false}));
const ref = api('PATCH', `/repos/${REPO}/git/refs/heads/${BRANCH}`, refFile);
console.log('ref now:', ref.object.sha);
console.log('COMMIT DONE', commit.sha);
