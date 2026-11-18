// Static-route check for the free-entry staging worker (F4).
// Usage: node check-free-route.mjs <free-entry.html> <walk-free.html> <free-index.html>
// Calls the worker's real fetch handler (no env — so only the static
// routes; the /api/* routes need the KV binding and are covered by the
// HTTP checks in stage-free-route.py against the staged worker).
import fs from 'node:fs';
import crypto from 'node:crypto';
import worker from '/tmp/free-worker-src.mjs';

const [entryFile, walkFile, indexFile] = process.argv.slice(2);
const cases = [
  ['/free', entryFile],
  ['/free/walk', walkFile],
  ['/', indexFile],
];
let ok = true;
for (const [path, file] of cases) {
  const resp = await worker.fetch(new Request('https://naya-pricing-free-staging.nayapower.workers.dev' + path));
  const text = await resp.text();
  const expected = fs.readFileSync(file, 'utf-8');
  const match = Buffer.from(text, 'utf-8').equals(Buffer.from(expected, 'utf-8'));
  console.log(path, 'status', resp.status, 'bytes', text.length, 'sha256',
    crypto.createHash('sha256').update(text).digest('hex').slice(0, 12) + '…', 'MATCH:', match);
  if (!match || resp.status !== 200) ok = false;
}
const hub = await worker.fetch(new Request('https://naya-pricing-free-staging.nayapower.workers.dev/free/hub'));
console.log('/free/hub status', hub.status, 'Location:', hub.headers.get('location'));
if (hub.status !== 302 || hub.headers.get('location') !== 'https://nayanet.app/') ok = false;
console.log('FREE STATIC ROUTES:', ok ? 'PASS' : 'FAIL');
if (!ok) process.exit(1);
