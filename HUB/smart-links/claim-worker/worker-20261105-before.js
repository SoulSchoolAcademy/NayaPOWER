// naya-smartlinks-claim — Smart Link CLAIM endpoint (Page Elevation Program, 2026-10-23)
// Serves ONLY: POST https://nayanet.live/api/smart-links/claim
// Dedicated worker (NOT the redirect worker): the redirect worker
// (naya-smartlinks) stays byte-untouched, so claiming can never break
// redirecting. This worker validates, checks reserved/taken, INSERTs via
// the Supabase service role, then waits until the new short address
// answers with the real 302 (routes are minted by the VM-side route
// reconciler, which holds the Cloudflare credential — see record) and
// only then reports success. Any failure after insert rolls the row back.
// Every error string is written for a first-time user: what happened +
// what to do next. The page shows it verbatim.

const SB_URL = 'https://dahisasgpfvziswqvmvm.supabase.co';
const NAME_RE = /^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$/;
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36';

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Access-Control-Max-Age': '86400'
};

function json(status, body) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store', ...CORS }
  });
}
const err = (status, error) => json(status, { error });

async function sb(env, method, path, body) {
  const res = await fetch(SB_URL + '/rest/v1/' + path, {
    method,
    headers: {
      apikey: env.SUPABASE_SERVICE_ROLE_KEY,
      Authorization: 'Bearer ' + env.SUPABASE_SERVICE_ROLE_KEY,
      'Content-Type': 'application/json',
      Prefer: method === 'POST' ? 'return=representation' : 'return=minimal'
    },
    body: body ? JSON.stringify(body) : undefined
  });
  const text = await res.text();
  let data = null;
  try { data = text ? JSON.parse(text) : null; } catch (e) { data = null; }
  return { ok: res.ok, status: res.status, data };
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Verify through the off-zone probe worker: a Worker on the nayanet.live
// zone cannot fetch nayanet.live itself (same-zone subrequests hang —
// proven live 2026-10-23). The probe (workers.dev) fetches the link like
// any outside visitor and reports the real status + Location.
const PROBE = 'https://naya-link-probe.nayapower.workers.dev/?u=';
async function waitForRedirect(name, target) {
  const deadline = Date.now() + 50000;
  const link = 'https://nayanet.live/' + name;
  while (Date.now() < deadline) {
    try {
      const res = await fetch(PROBE + encodeURIComponent(link), {
        headers: { 'User-Agent': UA },
        signal: AbortSignal.timeout(12000)
      });
      const data = await res.json();
      if (data && data.status === 302 && data.location === target) return true;
    } catch (e) { /* not live yet — keep waiting */ }
    await sleep(2000);
  }
  return false;
}

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });
    if (request.method !== 'POST') {
      return err(405, 'This address only takes claim requests — open your NayaNET page and use the Claim button there.');
    }
    if (!env.SUPABASE_SERVICE_ROLE_KEY) {
      return err(500, 'The claim service is not fully switched on yet — nothing was claimed. Please try again later.');
    }

    let body = null;
    try { body = await request.json(); } catch (e) { body = null; }
    if (!body || typeof body !== 'object') {
      return err(400, 'We could not read that claim — please go back, check the link and the name, and try again.');
    }

    const owner = typeof body.owner_alias === 'string' ? body.owner_alias.trim() : '';
    const name = typeof body.name === 'string' ? body.name.trim().toLowerCase() : '';
    const target = typeof body.target_url === 'string' ? body.target_url.trim() : '';

    if (!owner) {
      return err(400, 'Your page name was missing from that claim — reload your page and try claiming again.');
    }
    if (!NAME_RE.test(name)) {
      return err(400, 'That name cannot be used — a name can only use lowercase letters, numbers and dashes, it must start and end with a letter or number, and it can be up to 63 characters long. Try a simpler name and claim again.');
    }
    if (!/^https?:\/\//i.test(target)) {
      return err(400, 'That link does not look complete — it needs to start with https:// so copy the full link from your browser address bar, paste it in, and try again.');
    }

    // Reserved check (the database trigger is the backstop).
    const reserved = await sb(env, 'GET', 'smart_link_reserved_names?name=eq.' + encodeURIComponent(name) + '&select=name');
    if (reserved.ok && Array.isArray(reserved.data) && reserved.data.length) {
      return err(409, 'nayanet.live/' + name + ' is a name NayaNET keeps for its own pages, so it cannot be claimed — pick a different name and try again.');
    }
    // Taken check (the unique constraint is the backstop).
    const taken = await sb(env, 'GET', 'smart_links?name=eq.' + encodeURIComponent(name) + '&select=name');
    if (taken.ok && Array.isArray(taken.data) && taken.data.length) {
      return err(409, 'That name was just claimed by someone else — names go to whoever claims them first. Try another name — adding a word or your initials often works.');
    }

    // Guarded insert (DB guards fire here: unique, reserved trigger, shape checks).
    const ins = await sb(env, 'POST', 'smart_links', { owner_alias: owner, name, target_url: target });
    if (!ins.ok) {
      const msg = (ins.data && (ins.data.message || ins.data.details || '')) + '';
      if (ins.status === 409 || /duplicate|unique/i.test(msg)) {
        return err(409, 'That name was just claimed by someone else — names go to whoever claims them first. Try another name — adding a word or your initials often works.');
      }
      if (/reserved/i.test(msg)) {
        return err(409, 'nayanet.live/' + name + ' is a name NayaNET keeps for its own pages, so it cannot be claimed — pick a different name and try again.');
      }
      if (/check constraint|shape/i.test(msg)) {
        return err(400, 'That name or link was not accepted — check the name uses only lowercase letters, numbers and dashes, and that the link starts with https://, then try again.');
      }
      return err(500, 'Something went wrong on our side while saving that claim — nothing was claimed. Please try again in a moment.');
    }

    // Wait until the short address really redirects (route minted by the reconciler).
    const live = await waitForRedirect(name, target);
    if (!live) {
      // Roll back the row so the name is free again.
      await sb(env, 'DELETE', 'smart_links?name=eq.' + encodeURIComponent(name) + '&owner_alias=eq.' + encodeURIComponent(owner));
      return err(503, 'Your link was saved but its short address did not switch on in time, so nothing was claimed and the name is free again — please wait a few seconds and claim it once more.');
    }

    return json(200, { name });
  }
};