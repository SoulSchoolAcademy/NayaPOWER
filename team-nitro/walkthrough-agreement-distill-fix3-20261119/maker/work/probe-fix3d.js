#!/usr/bin/env node
// probe-fix3d.js — is the lowercase alias fill pre-existing base behavior?
// Fetch BASE identity, run it in the harness DOM with the three URLs, read the input.
// Also print every aliasInput.value assignment with context. No writes.
const https = require('https');
const H1 = require('./dom-harness3-dom.js');
const STAGE = 'naya-walk-beginning-staging.nayapower.workers.dev';
function get(p) {
  return new Promise((res, rej) => {
    const req = https.get({ hostname: STAGE, path: p, headers: { 'User-Agent': 'Mozilla/5.0' } }, (r) => {
      const b = []; r.on('data', (c) => b.push(c));
      r.on('end', () => res(Buffer.concat(b).toString('utf8')));
      r.on('error', rej);
    });
    req.setTimeout(60000, () => req.destroy(new Error('timeout')));
    req.on('error', rej);
  });
}
function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }
(async () => {
  const I0 = await get('/identity.html?name=Distill%20Eye%20Walk');
  console.log('base identity bytes: ' + Buffer.byteLength(I0));
  // every aliasInput.value assignment
  let i = -1, n = 0;
  while ((i = I0.indexOf('aliasInput.value', i + 1)) !== -1) {
    n++;
    console.log('--- aliasInput.value #' + n + ' @' + i + ' ---');
    console.log(I0.slice(Math.max(0, i - 350), i + 250).replace(/\n/g, ' ').slice(0, 600));
  }
  // passedAlias uses
  let j = -1;
  while ((j = I0.indexOf('passedAlias', j + 1)) !== -1) {
    console.log('--- passedAlias @' + j + ' ---');
    console.log(I0.slice(Math.max(0, j - 150), j + 250).replace(/\n/g, ' ').slice(0, 400));
  }
  // run BASE bytes in the harness with each URL
  for (const url of ['?name=Distill%20Eye%20Walk&alias=Distill', '?alias=Distill', '?name=Distill%20Eye%20Walk']) {
    const e = H1.makeEnv(I0, url);
    await sleep(50);
    const inputs = H1.qa(e.document, 'input');
    let input = null;
    for (const inp of inputs) { const ph = inp.getAttribute('placeholder') || ''; if (ph.indexOf('lias') !== -1) { input = inp; break; } }
    const nm = e.document.querySelector('#displayName');
    console.log('BASE ' + url + ' -> input=' + JSON.stringify(input ? input.value : null) +
      ' hero text=' + JSON.stringify(nm ? nm.textContent : null) +
      ' hero hidden=' + (nm ? nm.hidden : null) +
      ' data-text=' + JSON.stringify(nm ? nm.getAttribute('data-text') : null) +
      ' errors=' + e.errors.length);
  }
  process.exit(0);
})().catch((e) => { console.error('FATAL', e); process.exit(1); });
