// INDEPENDENT CHECKER — fix-6 byte verification. Fetches base + fixed blobs
// via gh-direct.py (blob API), hashes, diffs lines, checks mechanism claims.
// Writes NOTHING except stdout (report written separately via file tool).
const { execFileSync } = require('child_process');
const crypto = require('crypto');
const path = require('path');
const GH = '/home/hatch/workspace/team-nitro/gh-direct.py';
const REPO = 'SoulSchoolAcademy/NayaPOWER';
const BASE_BLOB = 'dedf0b19057b4396572d8b1963352f0744c32439';
const FIX_BLOB = '8fbec9580c078b97d0881f7aa20d8c92ce41d9d6';
const BASE_EXPECT = { size: 10453371, sha256: '8585244daa53fd8b7ad00fe5da0c4ee79ec02c3c4a146c55b9b64140936752b9' };
const FIX_EXPECT = { size: 10454283, sha256: '3dabcd80ade63f664fb2daabef3a2b2c34f1360fb0f31177739e1d7280c66522' };

function fetchBlob(sha) {
  const out = execFileSync('python3', [GH, 'GET', `/repos/${REPO}/git/blobs/${sha}`], { maxBuffer: 128 * 1024 * 1024 }).toString();
  const body = JSON.parse(out.slice(out.indexOf('\n') + 1));
  if (body.encoding !== 'base64') throw new Error('unexpected encoding ' + body.encoding);
  return Buffer.from(body.content.replace(/\s/g, ''), 'base64');
}
function sha256(buf) { return crypto.createHash('sha256').update(buf).digest('hex'); }
function count(s, sub) { return s.split(sub).length - 1; }
function lineNo(s, idx) { return s.slice(0, idx).split('\n').length; }

const baseBuf = fetchBlob(BASE_BLOB);
const fixBuf = fetchBlob(FIX_BLOB);
console.log('BASE size', baseBuf.length, 'sha', sha256(baseBuf), 'expect', BASE_EXPECT.size, BASE_EXPECT.sha256, 'MATCH', baseBuf.length === BASE_EXPECT.size && sha256(baseBuf) === BASE_EXPECT.sha256);
console.log('FIX  size', fixBuf.length, 'sha', sha256(fixBuf), 'expect', FIX_EXPECT.size, FIX_EXPECT.sha256, 'MATCH', fixBuf.length === FIX_EXPECT.size && sha256(fixBuf) === FIX_EXPECT.sha256);
console.log('SIZE DELTA', fixBuf.length - baseBuf.length);

const base = baseBuf.toString('latin1');
const fix = fixBuf.toString('latin1');
const bLines = base.split('\n');
const fLines = fix.split('\n');
console.log('BASE lines', bLines.length, 'FIX lines', fLines.length, 'DELTA', fLines.length - bLines.length);

// common prefix / suffix
let pre = 0;
while (pre < bLines.length && pre < fLines.length && bLines[pre] === fLines[pre]) pre++;
let suf = 0;
while (suf < bLines.length - pre && suf < fLines.length - pre && bLines[bLines.length - 1 - suf] === fLines[fLines.length - 1 - suf]) suf++;
console.log('COMMON PREFIX lines', pre, '(0-based idx', pre, ')');
console.log('COMMON SUFFIX lines', suf);
console.log('BASE removed lines', bLines.length - pre - suf);
console.log('FIX added lines', fLines.length - pre - suf);
console.log('--- ADDED LINES (1-based fixed line numbers) ---');
for (let i = pre; i < fLines.length - suf; i++) console.log((i + 1) + ': ' + fLines[i]);
console.log('--- BASE lines around insertion (1-based) ---');
for (let i = pre - 3; i < pre + 3 && i < bLines.length; i++) console.log((i + 1) + ': ' + bLines[i]);

// Mechanism checks in BASE bytes
console.log('=== MECHANISM (base) ===');
// 1. render() hub/:room parametric match
const ri = base.indexOf("routes['hub/:room']");
console.log("routes['hub/:room'] in base:", ri >= 0, ri >= 0 ? 'line ' + lineNo(base, ri) : '');
const starI = base.indexOf("routes['*']");
console.log("routes['*'] in base:", starI >= 0, starI >= 0 ? 'line ' + lineNo(base, starI) : '');
// order: which appears first in render()? find render function region
const renderI = base.indexOf('function render()');
console.log('render() at line', renderI >= 0 ? lineNo(base, renderI) : 'NOT FOUND');
// print render region lines 11012-11044 approx (find by searching "hub/:room" context)
if (ri >= 0) console.log('hub/:room context:', JSON.stringify(base.slice(ri - 300, ri + 300)));
// 2. popstate handler base
const ps = base.indexOf("addEventListener('popstate'");
console.log('popstate handler base line', ps >= 0 ? lineNo(base, ps) : 'NOT FOUND');
if (ps >= 0) console.log('popstate context:', JSON.stringify(base.slice(ps - 100, ps + 400)));
// 3. showView F3 yield
const f3 = base.indexOf("navigate('/hub/feed')");
console.log("navigate('/hub/feed') occurrences base:", count(base, "navigate('/hub/feed')"));
const sv = base.indexOf('showView');
console.log('first showView line', sv >= 0 ? lineNo(base, sv) : '');
// 4. askBtn navigate
const ask = base.indexOf("navigate('/hub/ask')");
console.log("navigate('/hub/ask') occurrences base:", count(base, "navigate('/hub/ask')"), 'first line', ask >= 0 ? lineNo(base, ask) : '');
const askBtn = base.indexOf('askBtn');
console.log('askBtn occurrences base:', count(base, 'askBtn'));
// 5. fallback line 17440 region
console.log('base line 17440:', JSON.stringify(bLines[17439]));
console.log('fix  line 17440:', JSON.stringify(fLines[17439]));
// 6. recoverFeedAfterBack counts
console.log('recoverFeedAfterBack base:', count(base, 'recoverFeedAfterBack'), 'fix:', count(fix, 'recoverFeedAfterBack'));
// 7. Academy destination
console.log('groovepages academy base:', count(base, 'nayanet.groovepages.com/academy'), 'fix:', count(fix, 'nayanet.groovepages.com/academy'));
// 8. guard presence in fix
console.log('FRAME-FIX6 marker fix:', count(fix, 'FRAME-FIX6'), 'base:', count(base, 'FRAME-FIX6'));
console.log('guard first-seg test fix:', count(fix, "if (_h==='hub'"));
// 9. script parse check (all inline scripts parse)
const vm = require('vm');
function scriptsParse(s) {
  const re = /<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script\s*>/gi;
  let m, n = 0, fail = 0;
  while ((m = re.exec(s))) { n++; try { new vm.Script(m[1]); } catch (e) { fail++; console.log('  PARSE FAIL script#' + n + ': ' + e.message.slice(0, 200)); } }
  return { n, fail };
}
console.log('base scripts:', JSON.stringify(scriptsParse(base)));
console.log('fix scripts:', JSON.stringify(scriptsParse(fix)));
// 10. VIEWS definition + showView home yield region in fix
const f3f = fix.indexOf("navigate('/hub/feed')");
console.log('fix navigate hub/feed first line', f3f >= 0 ? lineNo(fix, f3f) : '');
// 11. welcome banner marker — check a stable string present identically in both
const wb = base.indexOf('Welcome');
console.log('welcome-banner region check: base has "naya-install-overlay":', base.includes('naya-install-overlay'), 'fix:', fix.includes('naya-install-overlay'));
// 12. fallback allow-list: find the '*' fallback block text in base
const fb = base.indexOf("routes['*']");
if (fb >= 0) console.log('fallback context:', JSON.stringify(base.slice(fb - 200, fb + 800)));
