// Build the portal-alignment R1 staging worker from the lane files.
// Routes mirror the proven R5 worker: / -> R1 portal, /identity.html -> the
// NEW certificate (byte-identical, sha 57bdd387), /sw.js, /agreement-landing,
// /agreement -> 302 live agreement, /agmt-* + emblem from WELCOME_ASSETS KV.
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const sha = b => createHash('sha256').update(b).digest('hex');
const LANE = new URL('./', import.meta.url).pathname;
const portal = readFileSync(LANE + 'portal.html', 'utf8');
const identity = readFileSync(LANE + 'identity.html', 'utf8');
const sw = readFileSync(LANE + 'sw.js', 'utf8');
const main = `// portal-alignment-r1-staging — STAGED ONLY. Alignment round 1 on the R5 base
// (portal sha d4bb2102...): (1) nav labels always visible under each ball —
// desktop one row of 9 cells, phone 3x3 grid, first-tap-hold JS deleted;
// (2) one light top-left — button sheen 105deg -> 135deg, ambient glow
// re-enabled as a top-left wash; (3) walkthrough strip under the name entry:
// 1 Portal -> 2 Certificate (/identity.html, same host) -> 3 iPhones
// (v3 phone walkthrough staging worker, linked not duplicated).
// Certificate byte-identical to R2 (sha 57bdd387). Nothing live.
const PORTAL = ${JSON.stringify(portal)};
const IDENTITY = ${JSON.stringify(identity)};
const SW = ${JSON.stringify(sw)};
const LANDING_URL = 'https://naya-onboarding-landing-20261124-staging.nayapower.workers.dev/';
const H = {'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store'};
const ASSET_CT = {'.jpg': 'image/jpeg', '.png': 'image/png'};
export default {
  async fetch(req, env) {
    const u = new URL(req.url);
    if (u.pathname === '/' || u.pathname === '/index.html')
      return new Response(PORTAL, {headers: H});
    if (u.pathname === '/identity.html')
      return new Response(IDENTITY, {headers: H});
    if (u.pathname === '/sw.js')
      return new Response(SW, {headers: {'content-type': 'application/javascript; charset=utf-8', 'cache-control': 'no-store'}});
    if (u.pathname === '/agreement-landing')
      return Response.redirect(LANDING_URL, 302);
    if (u.pathname === '/agreement')
      return Response.redirect('https://nayanet.app/agreement', 302);
    const m = u.pathname.match(/^\\/(agmt-[a-z0-9-]+\\.(?:jpg|png)|naya-emblem-cut\\.png)$/);
    if (m) {
      const key = 'wbf-' + m[1];
      const ext = m[1].slice(m[1].lastIndexOf('.'));
      const v = await env.WELCOME_ASSETS.get(key, 'arrayBuffer');
      if (v === null) return new Response('Not found', {status: 404});
      return new Response(v, {headers: {'content-type': ASSET_CT[ext], 'cache-control': 'public, max-age=86400'}});
    }
    return new Response('Not found', {status: 404});
  }
};
`;
writeFileSync(LANE + 'worker-consolidated.js', main);
writeFileSync(LANE + 'worker-meta.json', JSON.stringify({main_module: 'worker.js', bindings: [{type: 'kv_namespace', name: 'WELCOME_ASSETS', namespace_id: '1cf80db6183245d19dd5296645a12bd0'}]}, null, 2) + '\n');
const b = readFileSync(LANE + 'worker-consolidated.js');
console.log('worker-consolidated.js', b.length, 'B sha256', sha(b));
console.log('portal.html', portal.length, 'B sha256', sha(Buffer.from(portal)));
console.log('identity.html', identity.length, 'B sha256', sha(Buffer.from(identity)));
