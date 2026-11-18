import worker from '/tmp/pricing-worker-src.mjs';

const mustHave = JSON.parse(process.argv[2]);
const mustNot = JSON.parse(process.argv[3]);
const resp = await worker.fetch(new Request('https://nayanet.app/pricing'));
const text = await resp.text();
let ok = true;
for (const m of mustHave) {
  const found = text.includes(m);
  console.log('HAVE', JSON.stringify(m), found);
  if (!found) ok = false;
}
for (const m of mustNot) {
  const found = text.includes(m);
  console.log('NOT', JSON.stringify(m), !found);
  if (found) ok = false;
}
console.log('MARKERS:', ok ? 'PASS' : 'FAIL');
if (!ok) process.exit(1);
