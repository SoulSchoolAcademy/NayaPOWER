// File the Black Diamond phone portal to NEW branch
// portal-frontpage-fix-20261125-r5-phone, created FROM the R5 branch head,
// via the git-data API (gh-app-api only). Blobs -> tree (base = R5 head
// tree) -> commit -> ref. Files >1 MB go through the blob API (base64).
// Node only; prints every sha. No raw credential anywhere.
import {readFileSync, writeFileSync, mkdirSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
const GH = '/home/hatch/workspace/custom-connectors/custom.legacy-github/bin/gh-app-api';
const REPO = 'SoulSchoolAcademy/NayaPOWER';
const BASE_BRANCH = 'portal-frontpage-fix-20261125-r5';
const BRANCH = 'portal-frontpage-fix-20261125-r5-phone';
const LANE = new URL('./', import.meta.url).pathname;
const DIR = 'TEAM-NITRO/portal-phone-20261127/maker/';
const FILES = ['portal.html', 'portal-r5-base.html', 'identity.html', 'identity-consolidated.html',
  'worker-consolidated.js', 'worker-meta.json', 'sw.js',
  'build-phone.mjs', 'build-worker-phone.mjs', 'verify-phone.mjs',
  'commit-phone.mjs', 'phone-section.html', 'phone-style.html', 'phone-script.html',
  'MAKER-REPORT.md'];
mkdirSync(LANE + 'evidence', {recursive: true});
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
console.log('R5 tree:', baseCommit.tree.sha);
const refBody = LANE + 'evidence/.newref-phone.json';
writeFileSync(refBody, JSON.stringify({ref: 'refs/heads/' + BRANCH, sha: baseSha}));
const created = api('POST', `/repos/${REPO}/git/refs`, refBody);
console.log('branch created:', created.ref, created.object.sha);
const treeEntries = [];
for (const f of FILES) {
  const buf = readFileSync(LANE + f);
  const bodyFile = LANE + 'evidence/.blob-phone-' + f.replace(/[^a-z0-9]/gi, '_') + '.json';
  writeFileSync(bodyFile, JSON.stringify({content: buf.toString('base64'), encoding: 'base64'}));
  const blob = api('POST', `/repos/${REPO}/git/blobs`, bodyFile);
  console.log('blob', f, buf.length, 'B ->', blob.sha);
  treeEntries.push({path: DIR + f, mode: '100644', type: 'blob', sha: blob.sha});
}
const treeFile = LANE + 'evidence/.tree-phone.json';
writeFileSync(treeFile, JSON.stringify({base_tree: baseCommit.tree.sha, tree: treeEntries}));
const tree = api('POST', `/repos/${REPO}/git/trees`, treeFile);
console.log('tree:', tree.sha);
const commitFile = LANE + 'evidence/.commit-phone.json';
writeFileSync(commitFile, JSON.stringify({
  message: "Black Diamond phone on the portal 2026-11-27 (phone round on the R5 base; staged only, nothing live)\n\nThe walkthrough is now the Black Diamond phone, real on the portal page: faceted diamond chrome frame, carbon-fiber chin, brushed aluminum, obsidian 9:16 screen, live ticking clock + 5G + battery in the status bar, and one big elevated purple obsidian jewel ball with the Naya N in a chrome bezel — the ball IS Enter (ENTER under it, no separate Enter button, no end disc). Front and center, XL width, dead forward, edge-to-edge on mobile.\n\nFLOW: no real-name screen (the portal has it), no alias screen (the certificate has it). First phone screen: country, then province/state, then city — one board each — then the 15 harvested R5 walk questions verbatim, in order (motto..start). Per screen: question + input full-frame on the white-light card, or the reveal full-frame after the ball tap — never both squished. Type your answer -> tap the ball -> it reveals in place (unfold + ball spin) with your answer and our full example -> Next arrow moves on, Back arrow goes back. The ball never navigates on its own. Answers save as you go (same key naya_welcome_right_v1); review screen copies every answer out (Copy my answers). No server save is faked: the walk's own complete() POST + verify-before-declare to the walkthrough-15 staging worker is untouched, and the backend integration is the named open item.\n\nHARVEST: R5 portal whole — name entry, Collective Agreement, Royal Unfolding, certificate link, menu, dotted ring — untouched except the walk section transplant (one <section> swapped, one <style> + one <script> added) and 9 small walk-JS patches (QUESTIONS prepend, placeholder, showInput, ball-reveal, next-arrow, finish-showEnd). Build: 18/18 assertions in build-phone.mjs; portal 13,900,189 B, sha 3b489c5a... (+16,418 B vs R5). Certificate byte-identical (sha 57bdd387...). Staged worker portal-frontpage-fix-20261125-r5phone-staging (worker 14,237,881 B, sha 2360ee86...). Design laws: §11 in MAKER-REPORT.md — one brief-ordered exception named (the reference's white screen card, black Marcellus text, never gray).\n\nOpen: backend integration for the phone answers (in-page state + copy-out only); the brief's parenthetical walk list (age/language, gender/faith, favorites, industry, education, achievements...) names questions that do not exist in the harvested R5 walk — the 15 harvested questions were kept verbatim instead of inventing new ones.",
  tree: tree.sha, parents: [baseSha],
}));
const commit = api('POST', `/repos/${REPO}/git/commits`, commitFile);
console.log('commit:', commit.sha);
const refFile = LANE + 'evidence/.ref-phone.json';
writeFileSync(refFile, JSON.stringify({sha: commit.sha, force: false}));
const ref = api('PATCH', `/repos/${REPO}/git/refs/heads/${BRANCH}`, refFile);
console.log('ref now:', ref.object.sha);
console.log('COMMIT DONE', commit.sha);
