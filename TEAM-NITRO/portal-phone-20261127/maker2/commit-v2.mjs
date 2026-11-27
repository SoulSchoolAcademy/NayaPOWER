// File the Black Diamond phone v2 portal to NEW branch
// portal-frontpage-fix-20261125-r5-phone-v2, created FROM the v1 branch head,
// via the git-data API (gh-app-api only). Blobs -> tree (base = v1 head
// tree) -> commit -> ref. Files >1 MB go through the blob API (base64).
// Node only; prints every sha. No raw credential anywhere.
import {readFileSync, writeFileSync, mkdirSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
const GH = '/home/hatch/workspace/custom-connectors/custom.legacy-github/bin/gh-app-api';
const REPO = 'SoulSchoolAcademy/NayaPOWER';
const BASE_BRANCH = 'portal-frontpage-fix-20261125-r5-phone';
const BRANCH = 'portal-frontpage-fix-20261125-r5-phone-v2';
const LANE = new URL('./', import.meta.url).pathname;
const DIR = 'TEAM-NITRO/portal-phone-20261127/maker2/';
const FILES = ['portal.html', 'portal-v1.html', 'portal-r5-base.html', 'identity.html', 'identity-consolidated.html',
  'worker-consolidated.js', 'worker-meta.json', 'sw.js',
  'build-v2.mjs', 'build-worker-v2.mjs', 'verify-v2.mjs', 'commit-v2.mjs',
  'phone-section2.html', 'phone-style2.html', 'phone-script2.html',
  'steps.js', 'engine.js', 'MAKER-REPORT.md',
  'evidence/probe-v2.py', 'evidence/enable-subdomain-v2.py',
  'evidence/v2-390-reveal-q1.png', 'evidence/v2-390-reveal-vision.png',
  'evidence/v2-390-end.png', 'evidence/v2-1440-reveal.png'];
mkdirSync(LANE + 'evidence', {recursive: true});
const api = (method, path, bodyFile) => {
  const args = [method, path];
  if (bodyFile) args.push('@' + bodyFile);
  const out = execFileSync(GH, args, {encoding: 'utf8', maxBuffer: 64 * 1024 * 1024});
  return JSON.parse(out);
};
const baseRef = api('GET', `/repos/${REPO}/git/ref/heads/${BASE_BRANCH}`);
const baseSha = baseRef.object.sha;
console.log('v1 branch head:', baseSha);
const baseCommit = api('GET', `/repos/${REPO}/git/commits/${baseSha}`);
console.log('v1 tree:', baseCommit.tree.sha);
const refBody = LANE + 'evidence/.newref-v2.json';
writeFileSync(refBody, JSON.stringify({ref: 'refs/heads/' + BRANCH, sha: baseSha}));
const created = api('POST', `/repos/${REPO}/git/refs`, refBody);
console.log('branch created:', created.ref, created.object.sha);
const treeEntries = [];
for (const f of FILES) {
  const buf = readFileSync(LANE + f);
  const bodyFile = LANE + 'evidence/.blob-v2-' + f.replace(/[^a-z0-9]/gi, '_') + '.json';
  writeFileSync(bodyFile, JSON.stringify({content: buf.toString('base64'), encoding: 'base64'}));
  const blob = api('POST', `/repos/${REPO}/git/blobs`, bodyFile);
  console.log('blob', f, buf.length, 'B ->', blob.sha);
  treeEntries.push({path: DIR + f, mode: '100644', type: 'blob', sha: blob.sha});
}
const treeFile = LANE + 'evidence/.tree-v2.json';
writeFileSync(treeFile, JSON.stringify({base_tree: baseCommit.tree.sha, tree: treeEntries}));
const tree = api('POST', `/repos/${REPO}/git/trees`, treeFile);
console.log('tree:', tree.sha);
const commitFile = LANE + 'evidence/.commit-v2.json';
writeFileSync(commitFile, JSON.stringify({
  message: "Black Diamond phone v2 on the portal 2026-11-27 (collapsed walk + checker D1-D7 + eye fixes; staged only, nothing live)\n\nThe walkthrough rebuilt to Shawn's ~10:0x collapsed flow (MEMORY.md): 17 steps, personal first, deep stuff at the end, categories LAST, no Skip anywhere. One-box location (country/province/city), age+language box, gender dropdown with NO default, three favorites boxes, sports type+team, who-to-connect-with (picture 6 Smart Match), industry+skills check-off, resume, then model/vision/goal/mission/thing/values/promise/benefit with the locked picture map (Vision->3 Nanoverse, Mission->4 How Naya Works, Goal->1 The Vault, Thing->7 Auto Organizer, Promise->5 Smart Vault, Connect->6 Smart Match, Benefit->2 How Current Works; Values->the five pillars), pictures harvested verbatim from workspace/user/media_library/image/ and embedded. Ball IS Enter (reveals in place); only the arrows navigate. Answers save as you go (naya_welcome_right_v1); review screen copies every answer out.\n\nChecker D1-D7 fixed: finish() no longer hides the ball; end screen rebuilt as a tight 2-column grid that fits whole at 390; no Skip pill; jewel rebuilt as an SVG facet map; frame ring is 12 discrete 30-degree facets; phone fits the viewport (831.5px in 844 at 390); cards size to content. Eye fixes: phone viewport-capped at both widths (845.1px in 900 at 1440, XL returns on tall viewports); reveal card scrolled whole into the 9:16 stage (no clipped example); pictures render full-frame in the stage; the stray 1440 page error not reproduced (0 page errors at both widths, two full probe runs).\n\nBuild: 26/26 assertions in build-v2.mjs; portal 22,107,028 B, sha 523a6844... (+8,206,632 B vs v1 — the 8 harvested pictures). Certificate byte-identical (sha 57bdd387...). Staged worker portal-phone-v2-staging (worker 22,444,930 B, sha 29150ae5...). Verify 23/23; browser probe 60/60 PASS twice (390x844 + 1440x900, 0 page errors). Design laws: §11 in MAKER-REPORT.md — one carried exception (the reference's white screen card); one named deviation (desktop width viewport-capped, not XL 560, so the phone fits in 900px).\n\nOpen: Shawn's eye is the final gate; live-backend acceptance of the new answer keys unproven; the staging backend 404s uncertified aliases (complete() needs a certified alias); a NEWER order landed during this round (MEMORY.md 'WALKTHROUGH — THE 3D IPHONE', voice call ~12:17-13:24 MST — trios of iPhones, picture full-screen behind the input, motto/love/don't-love/unique/gift return) which needs a re-brief as the next round; no Naya video asset yet; skills list is thin (R3 harvested four).",
  tree: tree.sha, parents: [baseSha],
}));
const commit = api('POST', `/repos/${REPO}/git/commits`, commitFile);
console.log('commit:', commit.sha);
const refFile = LANE + 'evidence/.ref-v2.json';
writeFileSync(refFile, JSON.stringify({sha: commit.sha, force: false}));
const ref = api('PATCH', `/repos/${REPO}/git/refs/heads/${BRANCH}`, refFile);
console.log('ref now:', ref.object.sha);
console.log('COMMIT DONE', commit.sha);
