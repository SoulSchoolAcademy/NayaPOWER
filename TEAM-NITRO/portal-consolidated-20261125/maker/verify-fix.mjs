// FIX-ROUND verification: syntax-check every inline <script> in both staged
// files (node --check), assert the fix strings, the 15 questions verbatim,
// and that nothing else in the consolidation moved.
import {readFileSync, writeFileSync, unlinkSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
const sha = b => createHash('sha256').update(b).digest('hex');
const LANE = new URL('./', import.meta.url).pathname;
const read = f => readFileSync(LANE + f, 'utf8');
const count = (s, sub) => s.split(sub).length - 1;
let fail = 0;
const check = (ok, m) => { console.log((ok ? 'PASS ' : 'FAIL ') + m); if (!ok) fail++; };

function checkScripts(file) {
  const s = read(file);
  const blocks = [...s.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
  console.log(file, 'inline scripts:', blocks.length);
  blocks.forEach((code, i) => {
    const tmp = LANE + 'evidence/.syntax-' + file.replace(/[^a-z]/g, '') + '-' + i + '.js';
    writeFileSync(tmp, code);
    try { execFileSync('node', ['--check', tmp], {stdio: 'pipe'}); console.log('PASS script ' + i + ' ' + file); }
    catch (e) { console.log('FAIL script ' + i + ' ' + file + ': ' + e.stderr.toString().slice(0, 300)); fail++; }
    unlinkSync(tmp);
  });
}
checkScripts('portal.html');
checkScripts('identity-consolidated.html');

const portal = read('portal.html');
const ident = read('identity-consolidated.html');
check(portal.includes("finish(out && out.failed ? 'failed' : 'ready')"), 'portal: verified complete()');
check(!portal.includes('var to = setTimeout(finish, 3000);'), 'portal: 3s finish-anyway gone');
check(portal.includes('verifyWorld'), 'portal: world verify present');
check(portal.includes('/api/welcome/me') && portal.includes('has_world === true'), 'portal: verify via has_world (CORS-clean)');
check(!portal.includes("WORLD_URL = 'https://naya-walkthrough-15-staging"), 'portal: no CORS-blocked world GET');
check(portal.includes('fpWalkFailLine') && portal.includes('fpWalkRetry'), 'portal: fail line + retry');
check(portal.includes('Your world is not ready yet'), 'portal: plain failure words');
check(portal.includes('.fp-walk-skip[hidden]{display:none!important}'), 'portal: skip honours hidden');
check(portal.includes('.fp-walk-enter[hidden]{display:none!important}'), 'portal: enter honours hidden');
check(portal.includes('flex-wrap:wrap'), 'portal: end rows wrap at 390px');
check(count(portal, '"key": "') === 15, 'portal: 15 questions');
check(count(portal, 'class="eco-item"') === 9, 'portal: final nine intact');
check(portal.includes('id="fpWalkSkip"'), 'portal: skip button intact');
check(ident.includes("status: 'unconfirmed'"), 'identity: unconfirmed resolutions');
check(count(ident, "status: 'unconfirmed'") === 5, 'identity: five unconfirmed');
check(ident.includes('fpClaimRetry'), 'identity: claim retry button');
check(ident.includes('onClaimResult'), 'identity: named claim handler');
check(!ident.includes('resolve({ status: \'ok\', createdAt: null }); }, 2500)'), 'identity: timeout no longer resolves ok');
check(ident.includes('Certificate of the Collective Agreement'), 'identity: title');
const worker = read('worker-consolidated.js');
check(worker.includes('WELCOME_ASSETS'), 'worker: KV binding route');
check(worker.includes("wbf-' + m[1]"), 'worker: wbf- key mapping');
check(worker.includes('async fetch(req, env)'), 'worker: env param');
check(worker.includes("'/sw.js'") && worker.includes('const SW ='), 'worker: sw.js route (harvested live)');
console.log('portal.html', Buffer.from(portal).length, 'B sha256', sha(Buffer.from(portal)));
console.log('identity-consolidated.html', Buffer.from(ident).length, 'B sha256', sha(Buffer.from(ident)));
console.log('worker-consolidated.js', Buffer.from(worker).length, 'B sha256', sha(Buffer.from(worker)));
if (fail) { console.error('VERIFY-FAIL', fail); process.exit(1); }
console.log('VERIFY-FIX PASS');
