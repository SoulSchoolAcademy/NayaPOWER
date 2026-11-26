// Build the portal-consolidated staging worker from the lane files.
// HTML embedded via JSON.stringify (safe for any content). Node only.
// Routes mirror the proven portal-login-mobile worker:
//   / + /index.html -> consolidated portal
//   /identity.html  -> consolidated certificate
//   /agreement-landing -> 302 onboarding agreement landing (proven route)
//   /agreement -> 302 live agreement (sha 2c88513f, verified byte-exact)
//   /agmt-*.jpg|png + /naya-emblem-cut.png -> WELCOME_ASSETS KV (fix
//     2026-11-25, defect 1: the 16 deck assets 404'd on the worker. The
//     bytes live in KV as wbf-<name> — 22/23 size-matched live nayanet.app
//     byte-for-byte, the emblem a real PNG 2,592,251 B; live fakes the
//     emblem with its SPA shell, so KV is the harvested source. Binding
//     WELCOME_ASSETS, namespace 1cf80db6183245d19dd5296645a12bd0; the deploy
//     metadata in worker-meta.json declares it.)
//   /sw.js -> the live self-retiring service worker, harvested byte-for-byte
//     (567 B, sha abac2ab5…): identity.html registers it, and the worker
//     404'd it — a console error on every certificate load.
// No /api/welcome/* proxy: the staged portal calls the walkthrough-15
// staging worker directly (it serves CORS, OPTIONS -> 204).
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const sha = b => createHash('sha256').update(b).digest('hex');
const LANE = new URL('./', import.meta.url).pathname;
const portal = readFileSync(LANE + 'portal.html', 'utf8');
const identity = readFileSync(LANE + 'identity-consolidated.html', 'utf8');
const sw = readFileSync(LANE + 'sw.js', 'utf8');
const main = `// portal-frontpage-fix-20261125-r4-staging — STAGED ONLY. Round-4 portal:
//   ROUND 4 (from the round-3 staged portal, sha d46c4409...):
//   (R4) F2 fixed at 390 (<=480px stack tightening, heading back toward
//   the R2 clearance); desktop end-slide red N orb whole (last-slide-only
//   trim); "Our Vow" answer opens at its head. Circle N untouched (56px,
//   eco-spin 90s), story untouched, F1 kept. R3 carried forward: the red
//   ACTIVE N in the circle; every N + "Read the agreement" open the visual
//   story IN PLACE at slide 1 ("The Old Way"); the 13-paragraph pop-up
//   reader is gone; the end slide carries the agree button at the very
//   bottom + the eight links in a bar across the bottom + the franchise
//   text box.
// One current portal:
// returning-v2 (login-mobile fixes + premium greeting) + top-menu final nine
// (no logo on top, black N left / red N right in the botbar) + walk Skip +
// "See my world" -> created world + certificate retitled. Live untouched.
// FIX 2026-11-25: deck assets served from WELCOME_ASSETS KV (wbf-<name>);
// claim + complete verify before declaring success (see the pages).
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
console.log('identity-consolidated.html', identity.length, 'B sha256', sha(Buffer.from(identity)));
