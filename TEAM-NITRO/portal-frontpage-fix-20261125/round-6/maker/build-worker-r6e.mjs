// Build the R6e staging worker from the lane files. Same pattern as
// build-worker-r6.mjs, with two changes:
//   (1) /identity.html now embeds identity.html — the NEW certificate
//       (315,409 B, sha 0c11fdb8…), NOT identity-consolidated.html (the old
//       313,224 B cert). The new cert goes live at nayanet.app/identity.html
//       as part of this round's live step.
//   (2) /agreement now serves the fixed v25 agreement file from KV
//       (key agreement-v25-r6.html, ~23 MB — too big to embed in the worker
//       script). The file opens on the welcome player (no preview intro);
//       LET'S GO starts slide 1 "The Old Way". The portal's own /agreement
//       boot (letter view) is a fallback that never fires while this route
//       serves the file.
//   /agreement-landing stays as R6 (302 to the onboarding landing; the front
//   page no longer uses it). Deck assets stay on WELCOME_ASSETS KV.
import {readFileSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const sha = b => createHash('sha256').update(b).digest('hex');
const LANE = new URL('./', import.meta.url).pathname;
const portal = readFileSync(LANE + 'portal.html', 'utf8');
const identity = readFileSync(LANE + 'identity.html', 'utf8');
const sw = readFileSync(LANE + 'sw.js', 'utf8');
const main = `// portal-frontpage-fix-20261125-r6-staging — STAGED ONLY. Round-6e portal:
//   CORRECTION (Shawn 2026-11-26 09:14 MST, supersedes the little-N/nutshell
//   decision): ONE entry — the red N orb dead center at the top, a real live
//   object with energy flowing around it, upright N — click goes STRAIGHT to
//   https://nayanet.app/agreement. NO bottom agreement button (0). The
//   corner Ns are plain home links, not entries. The (i) stays as R5.
//   /agreement serves the fixed v25 agreement file from KV: it opens on the
//   welcome player (the preview intro is GONE — removed whole), LET'S GO
//   starts slide 1 "The Old Way", all 27 slides in order, end slide = the
//   verbatim deed text + Agree at the very bottom (flashing) above the
//   arrows, the eight links on a bar BELOW the page. Agree returns to the
//   portal name entry and sets nayanet_agreement_done — the agreement does
//   not come up again. Certificate: the NEW 315,409 B fixed cert.
//   R6 carried forward: three-boards-at-a-time letter, end-slide agree
//   wording, story from inside only, hover-only menu, 78s ring, 27-slide
//   story, returning view. Live untouched.
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
    if (u.pathname === '/agreement') {
      const v = await env.WELCOME_ASSETS.get('agreement-v25-r6.html', 'arrayBuffer');
      if (v === null) return new Response('Agreement not staged', {status: 404});
      return new Response(v, {headers: H});
    }
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
console.log('identity.html (NEW cert)', identity.length, 'B sha256', sha(Buffer.from(identity)));
console.log('sw.js', sw.length, 'B sha256', sha(Buffer.from(sw)));
