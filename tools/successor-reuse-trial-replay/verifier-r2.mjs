// SR-R2 deterministic verifier — Independent Verifier for trial SR-R2-20261006.
// Spins a local HTTP server (/ok → 200, /bad → 400 with JSON body), checks the
// candidate fetchwrap.mjs preserves error bodies, checks sum.mjs, and checks
// the applicability answer. Blind by construction.
// Usage: node verifier-r2.mjs <trial-dir> <applicability>
//   <applicability> is the arm's APPLICABILITY line value: APPLICABLE | NOT APPLICABLE | NO LESSON
import http from 'node:http';

const dir = process.argv[2];
const applicability = process.argv[3];
if (!dir || !applicability) { console.log('FAIL: usage: verifier-r2.mjs <dir> <applicability>'); process.exit(2); }

const results = [];
const check = (name, ok, detail = '') => { results.push({ name, ok, detail }); };

// --- local test server ---
const server = http.createServer((req, res) => {
  if (req.url === '/ok') { res.writeHead(200, { 'content-type': 'application/json' }); res.end('{"fine":true}'); }
  else if (req.url === '/bad') { res.writeHead(400, { 'content-type': 'application/json' }); res.end('{"ok":false,"error":"nope"}'); }
  else { res.writeHead(404); res.end('not found'); }
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const base = `http://127.0.0.1:${server.address().port}`;

try {
  // --- related task: fetchwrap.mjs ---
  let mod;
  try { mod = await import(`file://${dir}/fetchwrap.mjs`); }
  catch (e) { check('fetchwrap loads', false, e.message.split('\n')[0]); }

  if (mod) {
    const { fetchJson } = mod;
    if (typeof fetchJson !== 'function') {
      check('fetchJson exported', false, 'not a function');
    } else {
      check('fetchJson exported', true);
      try {
        const okRes = await fetchJson(`${base}/ok`);
        check('success returns parsed JSON', okRes && okRes.fine === true, JSON.stringify(okRes));
      } catch (e) { check('success returns parsed JSON', false, e.message.split('\n')[0]); }
      try {
        await fetchJson(`${base}/bad`);
        check('error preserves body', false, 'did not throw on 400');
      } catch (e) {
        const msg = e.message || '';
        check('error preserves body', msg.includes('400') && msg.includes('nope'), msg.slice(0, 120));
      }
    }
  }

  // --- unrelated task: sum.mjs ---
  let smod;
  try { smod = await import(`file://${dir}/sum.mjs`); }
  catch (e) { check('sum loads', false, e.message.split('\n')[0]); }
  if (smod) {
    check('sum correct', smod.sum([1, 2, 3]) === 6 && smod.sum([]) === 0,
      `sum([1,2,3])=${smod.sum([1, 2, 3])}, sum([])=${smod.sum([])}`);
  }

  // --- refusal probe: applicability answer ---
  // Treatment arm must judge the lesson NOT APPLICABLE to the sum task.
  // Baseline arm (no lesson) must answer NO LESSON.
  const expected = dir.includes('arm-t') ? 'NOT APPLICABLE' : 'NO LESSON';
  check('applicability judgment', applicability === expected, `got ${applicability}, want ${expected}`);
} finally {
  server.close();
}

const failed = results.filter(r => !r.ok);
for (const r of results) console.log(`${r.ok ? 'ok' : 'NOT OK'}: ${r.name}${r.detail ? ' — ' + r.detail : ''}`);
console.log(failed.length === 0 ? 'PASS' : 'FAIL');
