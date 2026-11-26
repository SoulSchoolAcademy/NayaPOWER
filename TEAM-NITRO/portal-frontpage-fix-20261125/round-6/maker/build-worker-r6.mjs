// Build the portal-consolidated staging worker from the lane files.
// HTML embedded via JSON.stringify (safe for any content). Node only.
// Routes mirror the proven portal-login-mobile worker:
//   / + /index.html -> consolidated portal
//   /identity.html  -> consolidated certificate
//   /agreement-landing -> 302 onboarding agreement landing (proven route)
//   /agreement -> the PORTAL itself (ROUND 6: the exact agreement URL now
//     serves the real agreement directly — the stage boots straight into
//     the v7 letter view, no preview intro. Was a 302 to live
//     https://nayanet.app/agreement (v25 file, sha 2c88513f). Live
//     /agreement is a separate deployment; the live step puts this build
//     on the exact URL.)
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
const main = `// portal-frontpage-fix-20261125-r6-staging — STAGED ONLY. Round-6 portal:
//   ROUND 6 (from the round-5 staged portal, sha d4bb2102...):
//   The REAL collective agreement on the portal (Shawn: "Put the real
//   collective agreement on the portal. Make it. And make it live."):
//   every N + "Read the agreement" opens the v7 letter view DIRECTLY, in
//   place, first group visible — no preview intro, no story as a step —
//   and the URL becomes /agreement (the exact agreement URL). /agreement
//   itself serves this portal and boots straight into the letter. The
//   letter unfolds THREE boards at a time; the agree button reads "I
//   agree — show me my world ◆"; the 27-slide story stays, reachable only
//   from INSIDE the agreement view. The red-orb N sits upright: the 90s
//   spin is off the N images, kept on the rings. R5 carried forward:
//   hover-only menu, 78s ring, 27-slide story, end-slide agree + eight
//   links, certificate byte-identical. Live untouched.
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
      return new Response(PORTAL, {headers: H});
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
