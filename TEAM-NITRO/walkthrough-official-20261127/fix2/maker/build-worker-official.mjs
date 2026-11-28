// Build the OFFICIAL walkthrough staging worker from the lane files.
// Worker name: official-walkthrough-staging (no earlier worker overwritten).
// HTML embedded via JSON.stringify (safe for any content). Node only.
// Routes mirror the v1 phone worker:
//   / + /index.html -> consolidated portal (v2)
//   /identity.html  -> consolidated certificate (official: no Jump back in, no Install App, live digit-tile date/time)
//   /agreement-landing -> 302 onboarding agreement landing
//   /agreement -> 302 live agreement
//   /agmt-*.jpg|png + /naya-emblem-cut.png -> WELCOME_ASSETS KV
//   /sw.js -> the live self-retiring service worker
// No /api/welcome/* proxy: the staged portal calls the walkthrough-15
// staging worker directly (it serves CORS, OPTIONS -> 204).
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const sha = b => createHash('sha256').update(b).digest('hex');
const LANE = new URL('./', import.meta.url).pathname;
const portal = readFileSync(LANE + 'portal.html', 'utf8');
const identity = readFileSync(LANE + 'identity-consolidated.html', 'utf8');
const sw = readFileSync(LANE + 'sw.js', 'utf8');
const main = `// official-walkthrough-staging — STAGED ONLY. The OFFICIAL walkthrough on
//   the R5 portal: portal -> certificate (no Jump back in, no Install App,
//   raised name, live digit-tile date/time, ENTER -> /?walk=1 same host) ->
//   23 phone frames in 8 trios (live, age+language, gender, favorites,
//   industry+skills+connect+categories, video, motto, vision, goal,
//   mission, love, don't love, thing, promise, gift, benefit, unique,
//   connect, work, education, experience, achievements, values+stand).
//   NO Skip anywhere, no name screen, gender no default. Pictures
//   harvested verbatim from workspace/user/media_library/image/ (locked
//   map: Vision->3 Nanoverse, Mission->4 How Naya Works, Goal->1 The
//   Vault, Thing->7 Auto Organizer, Promise->5 Smart Vault, Connect->6
//   Smart Match, Benefit->2 How Current Works; Values->the five pillars).
//   Video: the direct 9:16 file, ONE spot mid-flow, from KV.
//   Base: v1 phone portal (13,900,396 B, sha b7ee02d6...), itself on the R5
//   base (13,883,771 B, sha d4bb2102...).
//   (R5) hover-only top menu, dotted hero ring 78s, 27-slide story, nine
//   destinations, certificate link — all untouched.
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
    if (u.pathname === '/naya-video.mp4') {
      const v = await env.WELCOME_ASSETS.get('naya-welcome-video', 'arrayBuffer');
      if (v === null) return new Response('Not found', {status: 404});
      return new Response(v, {headers: {'content-type': 'video/mp4', 'cache-control': 'public, max-age=86400'}});
    }
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
console.log('WORKER BUILD DONE');
