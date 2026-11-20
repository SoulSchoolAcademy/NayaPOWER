#!/usr/bin/env node
// Fix-5 maker: verify the filed branch by FRESH git API reads.
// Checks branch tip, parent, commit message, and the six files + report
// (blob sha + size) against the local values. Writes verify-filed.json.
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const HERE = __dirname;
const GH = '/home/hatch/workspace/team-nitro/gh-direct.py';
const REPO = 'SoulSchoolAcademy/NayaPOWER';
const BRANCH = 'walkthrough/agreement-distill-fix5-20261119';
const EXPECT_TIP = 'b048f00269f61c821812f06ffe6bd8e96cf29d4b';
const EXPECT_PARENT = 'd5003b2fd5c59e352b84169294b2773263876e01';
function gh(p) {
  const out = execFileSync('python3', [GH, 'GET', p], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024, timeout: 180000 });
  return JSON.parse(out.slice(out.indexOf('{')));
}
const WANT = {
  'team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html': ['1f0b04747e3315be6f1b619c1411e5e14fbdc1bb', 142532],
  'team-nitro/walk-v23-assembly-20261114/welcome-staged.html': ['00082c3d65801997f1dcb035bea6ee51bf600737', 1930947],
  'team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html': ['2f7a5e3ef599e00cb39c1e577bcb42563cd7ed81', 4363683],
  'team-nitro/walk-v23-assembly-20261114/identity-fixed.html': ['b3e5af088ef1d516079d96eeaa61d811d7889b8e', 404147],
  'team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js': ['0413500982bc14dfbe5534cbe82cd9c75a68696a', 8463055],
  'team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py': ['2299b99155e442257ca46eeb2c777ad4816ff6b0', 96371],
  'team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/MAKER-REPORT.md': ['e173efd76cf2f2dc94e15341d759220d9d00a3be', 19425],
};
const res = { branch: BRANCH, files: {}, allOk: true };
const ref = gh(`/repos/${REPO}/git/ref/heads/${BRANCH}`);
res.tip = ref.object.sha;
res.tipMatch = res.tip === EXPECT_TIP;
const commit = gh(`/repos/${REPO}/git/commits/${res.tip}`);
res.commitMessage = commit.message;
res.parent = commit.parents.map(p => p.sha);
res.parentMatch = res.parent.includes(EXPECT_PARENT);
res.treeSha = commit.tree.sha;
const tree = gh(`/repos/${REPO}/git/trees/${commit.tree.sha}?recursive=1`);
const byPath = {};
for (const e of tree.tree) byPath[e.path] = e;
for (const [p, [sha, size]] of Object.entries(WANT)) {
  const e = byPath[p];
  const ok = !!e && e.sha === sha && e.size === size;
  res.files[p] = { treeBlob: e ? e.sha : null, treeSize: e ? e.size : null, expectedBlob: sha, expectedSize: size, ok };
  if (!ok) res.allOk = false;
}
res.fix5RoundPaths = Object.keys(byPath).filter(p => p.includes('agreement-distill-fix5-20261119')).length;
res.allOk = res.allOk && res.tipMatch && res.parentMatch;
fs.writeFileSync(path.join(HERE, 'verify-filed.json'), JSON.stringify(res, null, 2));
console.log(JSON.stringify(res, null, 1));
