// File the R6e correction to the EXISTING branch
// portal-frontpage-fix-20261125-r6 (HEAD 2c4bf149...), as a new commit on
// top — git-data API via gh-app-api. Blobs -> tree (base = R6 head tree)
// -> commit -> ref PATCH. Files >1 MB go through the blob API; the 23 MB
// agreement file is piped (base64 -> jq -> gh-app-api via bash process
// substitution), never staged to disk (EPERM flake rule). Node only;
// prints every sha. No raw credential anywhere.
import {readFileSync, writeFileSync, statSync} from 'node:fs';
import {execFileSync, execSync} from 'node:child_process';
const GH = '/home/hatch/workspace/custom-connectors/custom.legacy-github/bin/gh-app-api';
const REPO = 'SoulSchoolAcademy/NayaPOWER';
const BRANCH = 'portal-frontpage-fix-20261125-r6';
const LANE = new URL('./', import.meta.url).pathname;
const DIR = 'TEAM-NITRO/portal-frontpage-fix-20261125/round-6/maker/';
const FILES = ['portal.html', 'agreement-v25-fixed-r6.html', 'identity.html',
  'worker-consolidated.js', 'worker-meta.json', 'sw.js',
  'build-fix-r6e.mjs', 'build-agreement-v26.mjs', 'build-worker-r6e.mjs',
  'evidence/kv-put-r6e.py', 'evidence/portal-diff-r6e-readable.txt'];
const api = (method, path, bodyFile) => {
  const args = [method, path];
  if (bodyFile) args.push('@' + bodyFile);
  const out = execFileSync(GH, args, {encoding: 'utf8', maxBuffer: 64 * 1024 * 1024});
  return JSON.parse(out);
};
const apiPipe = (method, path, file) => {
  // Large file: base64 -> jq -> gh-app-api, no intermediate file.
  const cmd = `${GH} ${method} ${path} @<(base64 -w0 ${JSON.stringify(file)} | jq -Rs '{content: ., encoding: "base64"}')`;
  const out = execSync(`bash -c ${JSON.stringify(cmd)}`, {encoding: 'utf8', maxBuffer: 64 * 1024 * 1024});
  return JSON.parse(out);
};
const headRef = api('GET', `/repos/${REPO}/git/ref/heads/${BRANCH}`);
const headSha = headRef.object.sha;
console.log('R6 branch head:', headSha);
const headCommit = api('GET', `/repos/${REPO}/git/commits/${headSha}`);
console.log('head tree:', headCommit.tree.sha);
const treeEntries = [];
for (const f of FILES) {
  const buf = readFileSync(LANE + f);
  const blob = buf.length > 1024 * 1024
    ? apiPipe('POST', `/repos/${REPO}/git/blobs`, LANE + f)
    : api('POST', `/repos/${REPO}/git/blobs`, (() => {
        const bodyFile = LANE + 'evidence/.blob-r6e-' + f.replace(/[^a-z0-9]/gi, '_') + '.json';
        writeFileSync(bodyFile, JSON.stringify({content: buf.toString('base64'), encoding: 'base64'}));
        return bodyFile;
      })());
  console.log('blob', f, buf.length, 'B ->', blob.sha);
  treeEntries.push({path: DIR + f, mode: '100644', type: 'blob', sha: blob.sha});
}
const treeFile = LANE + 'evidence/.tree-r6e.json';
writeFileSync(treeFile, JSON.stringify({base_tree: headCommit.tree.sha, tree: treeEntries}));
const tree = api('POST', `/repos/${REPO}/git/trees`, treeFile);
console.log('tree:', tree.sha);
const commitFile = LANE + 'evidence/.commit-r6e.json';
writeFileSync(commitFile, JSON.stringify({
  message: "Portal front-page fix ROUND 6e 2026-11-26 (Shawn's correction 09:14 MST — supersedes the little-N/nutshell decision; the settled loop)\n\nTHE LOOP: red orb dead center at the top (real live object, energy flowing around it) -> click -> straight to https://nayanet.app/agreement -> go through the agreement -> Agree at the end -> back to put their name in. The agreement does not come up again.\n\nONE ENTRY: the red orb (#fpCircleN) is the only agreement entry — click navigates DIRECTLY to https://nayanet.app/agreement (exact URL). The bottom \"Read the agreement\" button is GONE (0 occurrences of the element; the dead query + one dated ROUND 3 comment mention remain). The corner Ns are plain home links now (red corner retargeted to https://nayanet.app/). The (i) stays exactly as R5. The orb's gold N reads upright: eco-spin is off the N imgs (kept on the rings), plus a bright energy ring (conic arc, 12s orbit) + breathing halo so the orb reads as a real live object.\n\nTHE PREVIEW IS GONE (agreement-v25-fixed-r6.html, 22,935,043 B, sha 410078e1…): the whole #screen-choice intro (\"Begin the visual story\" / \"Read the agreement\" / \"Welcome. Let's begin with trust.\") is removed — section, choice CSS (17 rules), choice wiring IIFE, screens.choice, show() choice branch. The file opens on the welcome player (cover active); LET'S GO starts slide 1 \"The Old Way\"; all 27 slides in exact order; end slide = the verbatim deed text + \"I agree ◆\" Agree at the very bottom above the arrows (flashing), the eight links on a bar BELOW the page. The duplicate lower player bar is out (audio element stays, hidden, no controls); the main play button sits BELOW the visual (the poster is object-fit:contain, whole + centered); phone fit hides the cover caption strip + dead arrows. Completion flag nayanet_agreement_done is set in goToPortal() and on both portal Agree paths. SLIDES, legal pages (12), FP_FINAL texts, portraits, audio data untouched. The captain's live step R2-PUTs this file to key agreement-v25.html (R2 bucket nayanet-covers).\n\nCERTIFICATE: the staged portal now serves the NEW 315,409 B fixed cert (sha 0c11fdb8…), linked at its live address https://nayanet.app/identity.html. WALKTHROUGH GAP (named, not silent): the fix2 walkthrough file has NO ?walk=1 entry, so the portal cannot serve the updated 15-question walkthrough at /?walk=1 in this round — the portal's built-in walk stays as R5 proved it; an auto-open/transplant is a separate build.\n\nBuild: build-fix-r6e.mjs 36/36 assertions; portal 13,887,202 B, sha 01051a8f… (+3,431 B vs R5; data URIs byte-identical to R5, sha c16946cd…); build-agreement-v26.mjs all V assertions pass, both scripts compile. Staged worker portal-frontpage-fix-20261125-r6-staging: / = 01051a8f…, /identity.html = 0c11fdb8…, /agreement = 410078e1… (KV agreement-v25-r6.html, verified MATCH). Nothing live, nothing to Shawn.",
  tree: tree.sha, parents: [headSha],
}));
const commit = api('POST', `/repos/${REPO}/git/commits`, commitFile);
console.log('commit:', commit.sha);
const refFile = LANE + 'evidence/.ref-r6e.json';
writeFileSync(refFile, JSON.stringify({sha: commit.sha, force: false}));
const ref = api('PATCH', `/repos/${REPO}/git/refs/heads/${BRANCH}`, refFile);
console.log('ref now:', ref.object.sha);
console.log('COMMIT DONE', commit.sha);
