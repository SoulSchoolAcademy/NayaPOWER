// Checker follow-up: F3 yield region, branch tip, staged-bytes hash.
// Stdout only; no disk writes except the log redirect by the caller.
const { execFileSync } = require('child_process');
const crypto = require('crypto');
const https = require('https');
const GH = '/home/hatch/workspace/team-nitro/gh-direct.py';
const REPO = 'SoulSchoolAcademy/NayaPOWER';

function gh(path) {
  const out = execFileSync('python3', [GH, 'GET', path], { maxBuffer: 128 * 1024 * 1024 }).toString();
  return JSON.parse(out.slice(out.indexOf('\n') + 1));
}
function fetchBlob(sha) {
  const body = gh(`/repos/${REPO}/git/blobs/${sha}`);
  return Buffer.from(body.content.replace(/\s/g, ''), 'base64');
}
const base = fetchBlob('dedf0b19057b4396572d8b1963352f0744c32439').toString('latin1');
const bLines = base.split('\n');
console.log('--- base showView region lines 23560-23595 (1-based) ---');
for (let i = 23559; i < 23595; i++) console.log((i + 1) + ': ' + bLines[i]);
// _roomOpen definition
const ri = base.indexOf('_roomOpen');
console.log('_roomOpen first occurrence line:', ri >= 0 ? base.slice(0, ri).split('\n').length : 'NOT FOUND');
let idx = -1, n = 0;
while ((idx = base.indexOf('_roomOpen', idx + 1)) >= 0 && n < 8) { n++; console.log('  _roomOpen #' + n + ' line ' + base.slice(0, idx).split('\n').length + ': ' + JSON.stringify(base.slice(Math.max(0, idx - 120), idx + 200))); }
// VIEWS list
const vi = base.indexOf('VIEWS');
console.log('VIEWS first line:', vi >= 0 ? base.slice(0, vi).split('\n').length : 'NOT FOUND');
if (vi >= 0) console.log('VIEWS context:', JSON.stringify(base.slice(vi, vi + 400)));
// Branch tip + parent
const br = gh(`/repos/${REPO}/branches/personal/frame-round-fix6-20261119`);
console.log('BRANCH tip:', br.commit && br.commit.sha);
const cm = gh(`/repos/${REPO}/git/commits/8056efc3a7699b83d3f55294215482dee956156b`);
console.log('COMMIT sha:', cm.sha, 'parents:', (cm.parents || []).map(p => p.sha).join(','), 'tree:', cm.tree && cm.tree.sha);
console.log('COMMIT message:', JSON.stringify(cm.message));
// Staged bytes
const STAGED = 'https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/frame-round-fix6-20261119&cb=8fbec9580c078b97d0881f7aa20d8c92ce41d9d6&owner=flagship-personal';
https.get(STAGED, { headers: { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36' } }, res => {
  const chunks = [];
  res.on('data', c => chunks.push(c));
  res.on('end', () => {
    const buf = Buffer.concat(chunks);
    console.log('STAGED status', res.statusCode, 'size', buf.length, 'sha256', crypto.createHash('sha256').update(buf).digest('hex'));
    console.log('STAGED MATCH fixed blob:', buf.length === 10454283 && crypto.createHash('sha256').update(buf).digest('hex') === '3dabcd80ade63f664fb2daabef3a2b2c34f1360fb0f31177739e1d7280c66522');
  });
}).on('error', e => console.log('STAGED fetch ERROR', e.message));
