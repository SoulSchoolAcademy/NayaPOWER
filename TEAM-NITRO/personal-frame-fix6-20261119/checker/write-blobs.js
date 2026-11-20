// Checker: write base + fixed bytes to checker dir (Node writes), for the laws checker.
const { execFileSync } = require('child_process');
const fs = require('fs');
const GH = '/home/hatch/workspace/team-nitro/gh-direct.py';
const REPO = 'SoulSchoolAcademy/NayaPOWER';
function fetchBlob(sha) {
  const out = execFileSync('python3', [GH, 'GET', `/repos/${REPO}/git/blobs/${sha}`], { maxBuffer: 128 * 1024 * 1024 }).toString();
  const body = JSON.parse(out.slice(out.indexOf('\n') + 1));
  return Buffer.from(body.content.replace(/\s/g, ''), 'base64');
}
const base = fetchBlob('dedf0b19057b4396572d8b1963352f0744c32439');
const fix = fetchBlob('8fbec9580c078b97d0881f7aa20d8c92ce41d9d6');
fs.writeFileSync('/home/hatch/workspace/team-nitro/personal-frame-fix6-20261119/checker/base.html', base);
fs.writeFileSync('/home/hatch/workspace/team-nitro/personal-frame-fix6-20261119/checker/fixed.html', fix);
console.log('wrote base', base.length, 'fix', fix.length);
