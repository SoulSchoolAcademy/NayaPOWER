// File the Black Diamond phone v2 portal to NEW branch
// portal-frontpage-fix-20261125-r5-phone-v3, created FROM the v1 branch head,
// via the git-data API (gh-app-api only). Blobs -> tree (base = v1 head
// tree) -> commit -> ref. Files >1 MB go through the blob API (base64).
// Node only; prints every sha. No raw credential anywhere.
import {readFileSync, writeFileSync, mkdirSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
const GH = '/home/hatch/workspace/custom-connectors/custom.legacy-github/bin/gh-app-api';
const REPO = 'SoulSchoolAcademy/NayaPOWER';
const BASE_BRANCH = 'portal-frontpage-fix-20261125-r5-phone-v2';
const BRANCH = 'portal-frontpage-fix-20261125-r5-phone-v3';
const LANE = new URL('./', import.meta.url).pathname;
const DIR = 'TEAM-NITRO/portal-phone-20261127/maker3/';
const FILES = ['portal.html', 'portal-v1.html', 'portal-r5-base.html', 'identity.html', 'identity-consolidated.html',
  'worker-consolidated.js', 'worker-meta.json', 'sw.js',
  'build-v3.mjs', 'build-worker-v3.mjs', 'verify-v3.mjs', 'commit-v3.mjs',
  'phone-section3.html', 'phone-style3.html', 'phone-script3.html',
  'steps.js', 'engine.js', 'MAKER-REPORT.md',
  'evidence/probe-v3.py', 'evidence/enable-subdomain-v3.py', 'kv-put-video.py',
  'evidence/v3-390-end.png', 'evidence/v3-390-trio-g1.png',
  'evidence/v3-1440-end.png', 'evidence/v3-1440-trio.png'];
mkdirSync(LANE + 'evidence', {recursive: true});
const api = (method, path, bodyFile) => {
  const args = [method, path];
  if (bodyFile) args.push('@' + bodyFile);
  const out = execFileSync(GH, args, {encoding: 'utf8', maxBuffer: 64 * 1024 * 1024});
  return JSON.parse(out);
};
const baseRef = api('GET', `/repos/${REPO}/git/ref/heads/${BASE_BRANCH}`);
const baseSha = baseRef.object.sha;
console.log('v2 branch head:', baseSha);
const baseCommit = api('GET', `/repos/${REPO}/git/commits/${baseSha}`);
console.log('v1 tree:', baseCommit.tree.sha);
const refBody = LANE + 'evidence/.newref-v3.json';
writeFileSync(refBody, JSON.stringify({ref: 'refs/heads/' + BRANCH, sha: baseSha}));
const created = api('POST', `/repos/${REPO}/git/refs`, refBody);
console.log('branch created:', created.ref, created.object.sha);
const treeEntries = [];
for (const f of FILES) {
  const buf = readFileSync(LANE + f);
  const bodyFile = LANE + 'evidence/.blob-v3-' + f.replace(/[^a-z0-9]/gi, '_') + '.json';
  writeFileSync(bodyFile, JSON.stringify({content: buf.toString('base64'), encoding: 'base64'}));
  const blob = api('POST', `/repos/${REPO}/git/blobs`, bodyFile);
  console.log('blob', f, buf.length, 'B ->', blob.sha);
  treeEntries.push({path: DIR + f, mode: '100644', type: 'blob', sha: blob.sha});
}
const treeFile = LANE + 'evidence/.tree-v3.json';
writeFileSync(treeFile, JSON.stringify({base_tree: baseCommit.tree.sha, tree: treeEntries}));
const tree = api('POST', `/repos/${REPO}/git/trees`, treeFile);
console.log('tree:', tree.sha);
const commitFile = LANE + 'evidence/.commit-v3.json';
writeFileSync(commitFile, JSON.stringify({
  message: "Walkthrough phone TRIO rebuild v3 on the portal 2026-11-27 (staged only, nothing live)\n\nThree iPhones per group, 21 steps in 7 groups of three: side by side on laptop, stacked scrolling on phone. V2's 17 steps are the spine in relative order; motto, love, don't-love, unique and gift return; age+language and gender merged into one iPhone; values sits ONCE in achievements/values/where-you-stand; categories LAST. NO name screen, NO Skip anywhere. Back/forward arrows below the trio move between groups. Answers save as you go in localStorage key naya_welcome_right_v1 (47 keys). Picture/answer separation law: the picture is a full-bleed 9:16 layer BEHIND the input; the input card shows whole at rest covering the stage; the ball (Enter) transitions the card away and reveals the picture full-screen in place. The ball IS Enter (purple obsidian, SVG facet-map jewel harvested from v2, 12 discrete facets, N upright, orbit ring 120s). Black Diamond series, not rose gold. 14 pictures as base64 (v2's 8 verbatim + 6 new from the locked picture map: motto, love, don't-love, unique, gift, work). Full example on every step, using us as the example.\n\nVIDEO - one spot only, mid-flow, direct file (Shawn's rule, voice call ~14:12 MST): after industry + subcategories, before motto. Direct file workspace/user/media_library/video/c8/c86da39ed1360b79f5109f2c0706f8345059259b2574753b39cdf89af95d037c.mp4 - ffprobe-verified 576x1024 = exactly 9:16, h264, 30fps, 204.3s, 7,368,202 B, sha c86da39e... The video fills the phone's 9:16 screen above the ball; the ball plays/pauses it (preload=none, no native controls); tapping the video toggles too. YouTube (youtube.com/watch?v=XqZe1zdF1Tc) is a fallback link only, never the source. The pillars under the video are the video's OWN four: Smart Vault, Auto Organizer, Smart Match, Collective Intelligence. NO video at the end - end sequence is answers -> Hub -> pricing page. Serving note: embedding the video as base64 made the portal 57 MB and the worker returned 503 error 1102 on /; the video is served by the staging worker at /naya-video.mp4 from the WELCOME_ASSETS KV (key naya-welcome-video, 200, bytes == source file).\n\nF4/F5 closed: end screen whole inside the stage at 1440 (endBottom 685.77 < stageBottom 697.77), end grid now 2 columns with 'See my world' spanning both and the rest shortened per the brief, never clipped; chin label nowrap. Real bugs found by the probe and fixed: (1) picking a subcategory destroyed its own checkbox (change handler re-rendered the sub list before saving - now collects first, re-renders only on a CATEGORY change); (2) sub values never saved to localStorage (fieldValue queried subs inside [data-fid] but they live in the sibling .bd-subs host - a v2 carry-over the v2 checker missed by reading the DOM, not the saved value).\n\nBuild: 30/30 assertions in build-v3.mjs; portal 47,429,694 B, sha 83567578... (+33,529,298 B vs v1 - the 14 pictures). Certificate byte-identical (sha 57bdd387...). Staged worker portal-phone-v3-staging (worker 47,769,362 B, sha 8328f68f...). Verify 27/27; browser probe 129/129 PASS, 0 FAIL (390x844 + 1440x900, real taps, full walk, complete() 200 at both widths, 0 real page errors - cert artifact + transient agmt 503s retried 200 + video teardown abort excluded with proof). Design laws: section 11 in MAKER-REPORT.md - one carried exception (the reference's white screen card); one named deviation (desktop phones viewport-capped ~360px at 900h, not XL 560, so the trio fits; XL returns on tall viewports); video has no native controls (the ball is its control).\n\nOpen: Shawn's eye is the final gate; live-backend acceptance of the new answer keys unproven (backend seat); values placement still open for Shawn's word (also named in a 'values/promise/gift' trio); named trios vs rows (mission/goal/vision and unique/benefit/connect split across row boundaries); skills list is thin (R3 harvested four).\n\nThe walkthrough rebuilt to Shawn's ~10:0x collapsed flow (MEMORY.md): 17 steps, personal first, deep stuff at the end, categories LAST, no Skip anywhere. One-box location (country/province/city), age+language box, gender dropdown with NO default, three favorites boxes, sports type+team, who-to-connect-with (picture 6 Smart Match), industry+skills check-off, resume, then model/vision/goal/mission/thing/values/promise/benefit with the locked picture map (Vision->3 Nanoverse, Mission->4 How Naya Works, Goal->1 The Vault, Thing->7 Auto Organizer, Promise->5 Smart Vault, Connect->6 Smart Match, Benefit->2 How Current Works; Values->the five pillars), pictures harvested verbatim from workspace/user/media_library/image/ and embedded. Ball IS Enter (reveals in place); only the arrows navigate. Answers save as you go (naya_welcome_right_v1); review screen copies every answer out.\n\nChecker D1-D7 fixed: finish() no longer hides the ball; end screen rebuilt as a tight 2-column grid that fits whole at 390; no Skip pill; jewel rebuilt as an SVG facet map; frame ring is 12 discrete 30-degree facets; phone fits the viewport (831.5px in 844 at 390); cards size to content. Eye fixes: phone viewport-capped at both widths (845.1px in 900 at 1440, XL returns on tall viewports); reveal card scrolled whole into the 9:16 stage (no clipped example); pictures render full-frame in the stage; the stray 1440 page error not reproduced (0 page errors at both widths, two full probe runs).\n\nBuild: 26/26 assertions in build-v2.mjs; portal 22,107,028 B, sha 523a6844... (+8,206,632 B vs v1 — the 8 harvested pictures). Certificate byte-identical (sha 57bdd387...). Staged worker portal-phone-v2-staging (worker 22,444,930 B, sha 29150ae5...). Verify 23/23; browser probe 60/60 PASS twice (390x844 + 1440x900, 0 page errors). Design laws: §11 in MAKER-REPORT.md — one carried exception (the reference's white screen card); one named deviation (desktop width viewport-capped, not XL 560, so the phone fits in 900px).\n\nOpen: Shawn's eye is the final gate; live-backend acceptance of the new answer keys unproven; the staging backend 404s uncertified aliases (complete() needs a certified alias); a NEWER order landed during this round (MEMORY.md 'WALKTHROUGH — THE 3D IPHONE', voice call ~12:17-13:24 MST — trios of iPhones, picture full-screen behind the input, motto/love/don't-love/unique/gift return) which needs a re-brief as the next round; no Naya video asset yet; skills list is thin (R3 harvested four).",
  tree: tree.sha, parents: [baseSha],
}));
const commit = api('POST', `/repos/${REPO}/git/commits`, commitFile);
console.log('commit:', commit.sha);
const refFile = LANE + 'evidence/.ref-v3.json';
writeFileSync(refFile, JSON.stringify({sha: commit.sha, force: false}));
const ref = api('PATCH', `/repos/${REPO}/git/refs/heads/${BRANCH}`, refFile);
console.log('ref now:', ref.object.sha);
console.log('COMMIT DONE', commit.sha);
