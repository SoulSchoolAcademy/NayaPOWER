// Fetch fix-5 base blob bytes from the GitHub API (in memory only).
const { execFileSync } = require('child_process');
const crypto = require('crypto');
const path = require('path');
const BLOB = 'dedf0b19057b4396572d8b1963352f0744c32439';
const EXPECT_SHA256 = '8585244daa53fd8b7ad00fe5da0c4ee79ec02c3c4a146c55b9b64140936752b9';
const EXPECT_SIZE = 10453371;
function fetchBase() {
  const out = execFileSync('python3', [path.join('/home/hatch/workspace/team-nitro', 'gh-direct.py'), 'GET', `/repos/SoulSchoolAcademy/NayaPOWER/git/blobs/${BLOB}`], { maxBuffer: 64 * 1024 * 1024 }).toString();
  const body = JSON.parse(out.slice(out.indexOf('\n') + 1));
  const buf = Buffer.from(body.content.replace(/\s/g, ''), 'base64');
  const sha = crypto.createHash('sha256').update(buf).digest('hex');
  if (sha !== EXPECT_SHA256) throw new Error('base sha mismatch ' + sha);
  if (buf.length !== EXPECT_SIZE) throw new Error('base size mismatch ' + buf.length);
  return buf.toString('latin1');
}
function count(s, sub) { return s.split(sub).length - 1; }
function ctx(s, sub, before = 200, after = 400) {
  const i = s.indexOf(sub);
  if (i < 0) return null;
  return { index: i, line: s.slice(0, i).split('\n').length, text: s.slice(Math.max(0, i - before), i + sub.length + after) };
}
module.exports = { fetchBase, count, ctx };
