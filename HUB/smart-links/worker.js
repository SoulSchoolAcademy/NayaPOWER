// worker.js — the Smart Links redirect worker for nayanet.live/<name>.
//
// STATUS: code only. Deployment is a human-gated act (see README.md); this
// file ships in the repo and is exercised by tests, it is not live.
//
// Behavior contract (Best-of-Best application map, element #3):
//   - GET /<name> for a live Smart Link -> 302 to the link's target URL.
//   - The click is counted FIRST in intent but NEVER blocks the visitor:
//     the count is handed to ctx.waitUntil and the redirect returns
//     immediately. A dead database can lose a count; it can never stall
//     or break a visitor's redirect.
//   - Reserved names (reserved-names.mjs) and unknown names are NOT links:
//     they answer 404 and record nothing, so this worker can never shadow
//     /rooms/*, /s/*, /identity.html, or any other real route.
//   - Every redirect carries the join-attribution carrier (attribution.mjs):
//     an nl_attr cookie plus an nl_ref param on the target URL.
//
// Data access goes through an adapter: { lookupLink(name), recordClick(row) }.
// Production uses the Supabase adapter below (anon key; lookup rides the
// resolve_smart_link RPC so the links table itself is never listable by
// anon, and click inserts are append-only by RLS — see the migration
// supabase/migrations/20261022201500_smart_links_v1.sql). Tests inject
// fakes, so the handler logic is proven without a database.

import { isReservedName, normalizeLinkName, LINK_NAME_PATTERN } from './reserved-names.mjs';
import { ATTRIBUTION_PARAM, formatAttributionCookie } from './attribution.mjs';

const SOCIAL_HOSTS = [
  'facebook.com', 'instagram.com', 'threads.net', 'x.com', 'twitter.com',
  'tiktok.com', 'linkedin.com', 'youtube.com', 'youtu.be', 'reddit.com',
  'pinterest.com', 'snapchat.com', 'whatsapp.com',
];
const SEARCH_HOSTS = [
  'google.', 'bing.com', 'duckduckgo.com', 'search.yahoo.', 'ecosia.org',
  'brave.com', 'startpage.com', 'yandex.',
];
const EMAIL_HOSTS = [
  'mail.google.', 'outlook.live.', 'mail.yahoo.', 'proton.me', 'protonmail.',
];

function hostMatches(host, list) {
  return list.some((h) => {
    if (h.endsWith('.')) {
      // Stem entry like 'google.' or 'mail.google.' — the host must START
      // with the stem (google.com, www.google.co.uk, mail.google.com),
      // so a stem appearing mid-host never matches (notgoogle.com,
      // fake.mail.google.com.evil.example).
      return host.startsWith(h) || host.startsWith('www.' + h);
    }
    return host === h || host.endsWith('.' + h);
  });
}

// The click stores a referrer CLASS, never the raw referrer: classes are
// what the Dashboard/Reports surfaces chart, and raw referrers leak the
// visitor's exact path through third-party sites.
export function classifyReferrer(referer, selfHost) {
  if (!referer) return { referrer_class: 'direct', referrer_host: null };
  let host;
  try { host = new URL(referer).hostname.toLowerCase(); } catch {
    return { referrer_class: 'other', referrer_host: null };
  }
  if (selfHost && host === selfHost) return { referrer_class: 'internal', referrer_host: host };
  if (hostMatches(host, SOCIAL_HOSTS)) return { referrer_class: 'social', referrer_host: host };
  if (hostMatches(host, EMAIL_HOSTS)) return { referrer_class: 'email', referrer_host: host };
  if (hostMatches(host, SEARCH_HOSTS)) return { referrer_class: 'search', referrer_host: host };
  return { referrer_class: 'other', referrer_host: host };
}

export function buildRedirectTarget(targetUrl, linkName) {
  const u = new URL(targetUrl);
  if (!u.searchParams.has(ATTRIBUTION_PARAM)) {
    u.searchParams.set(ATTRIBUTION_PARAM, linkName);
  }
  return u.toString();
}

function notFound() {
  return new Response('Not Found', {
    status: 404,
    headers: { 'Content-Type': 'text/plain; charset=utf-8', 'X-Smart-Links': 'pass' },
  });
}

// env: { lookupLink(name) -> Promise<{id, target_url} | null>,
//        recordClick(row) -> Promise<void>,
//        selfHost?: string, newAttributionId?: () => string }
export async function handleRequest(request, env, ctx) {
  if (request.method !== 'GET' && request.method !== 'HEAD') return notFound();
  const url = new URL(request.url);
  const segments = url.pathname.split('/').filter(Boolean);
  if (segments.length !== 1) return notFound();

  let name;
  try { name = normalizeLinkName(decodeURIComponent(segments[0])); } catch { return notFound(); }
  if (!LINK_NAME_PATTERN.test(name) || isReservedName(name)) return notFound();

  const link = await env.lookupLink(name);
  if (!link || !link.target_url) return notFound();

  const attributionId = (env.newAttributionId || (() => crypto.randomUUID()))();
  const { referrer_class, referrer_host } = classifyReferrer(
    request.headers.get('Referer') || request.headers.get('Referrer'),
    env.selfHost || url.hostname,
  );
  const click = {
    link_id: link.id,
    referrer_class,
    referrer_host,
    attribution_id: attributionId,
  };
  // Count-then-redirect: the count is registered with waitUntil and never
  // awaited. Its failure is swallowed — analytics must not break visits.
  const counting = Promise.resolve()
    .then(() => env.recordClick(click))
    .catch(() => {});
  if (ctx && typeof ctx.waitUntil === 'function') ctx.waitUntil(counting);

  return new Response(null, {
    status: 302,
    headers: {
      Location: buildRedirectTarget(link.target_url, name),
      'Set-Cookie': formatAttributionCookie(name, attributionId),
      'Cache-Control': 'no-store',
      'X-Smart-Links': 'redirect',
    },
  });
}

// ——— Production adapter: Supabase PostgREST with the anon key ———
export function createSupabaseAdapter({ supabaseUrl, anonKey, fetchImpl }) {
  const doFetch = fetchImpl || fetch;
  const base = String(supabaseUrl).replace(/\/$/, '') + '/rest/v1';
  const headers = {
    apikey: anonKey,
    Authorization: 'Bearer ' + anonKey,
    'Content-Type': 'application/json',
  };
  return {
    async lookupLink(name) {
      const res = await doFetch(base + '/rpc/resolve_smart_link', {
        method: 'POST',
        headers,
        body: JSON.stringify({ p_name: name }),
      });
      if (!res.ok) return null;
      const rows = await res.json();
      const row = Array.isArray(rows) ? rows[0] : rows;
      if (!row || !row.target_url) return null;
      return { id: row.link_id, target_url: row.target_url };
    },
    async recordClick(row) {
      await doFetch(base + '/smart_link_clicks', {
        method: 'POST',
        headers: { ...headers, Prefer: 'return=minimal' },
        body: JSON.stringify(row),
      });
    },
  };
}

export default {
  async fetch(request, env, ctx) {
    const adapter = createSupabaseAdapter({
      supabaseUrl: env.SUPABASE_URL,
      anonKey: env.SUPABASE_ANON_KEY,
    });
    return handleRequest(request, { ...adapter, selfHost: 'nayanet.live' }, ctx);
  },
};
