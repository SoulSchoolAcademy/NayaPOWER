// attribution.mjs — the durable join-attribution carrier for Smart Links.
//
// The redirect worker (worker.js) stamps every click two ways:
//   1. a cookie  nl_attr=<link-name>.<attribution-id>  (30 days, Path=/)
//   2. a query param  nl_ref=<link-name>  appended to the redirect target
// Either one survives to the invite-join moment: the join page reads the
// carrier with readAttribution() and attaches { link_name, attribution_id }
// to the join, so the join credits the link — and the link's owner.
//
// This module is the reader half of the contract. It is pure and dependency
// free so the join surface (flagship app, Hub, or a future worker) can all
// consume the same code. The writer half lives in worker.js; the two are
// pinned to each other by tests/smart_links_worker.test.mjs.

export const ATTRIBUTION_COOKIE = 'nl_attr';
export const ATTRIBUTION_PARAM = 'nl_ref';
export const ATTRIBUTION_COOKIE_MAX_AGE = 2592000; // 30 days, seconds

export function formatAttributionCookie(linkName, attributionId) {
  return (
    ATTRIBUTION_COOKIE + '=' + encodeURIComponent(linkName) + '.' + attributionId +
    '; Max-Age=' + ATTRIBUTION_COOKIE_MAX_AGE +
    '; Path=/; SameSite=Lax; Secure'
  );
}

export function parseAttributionValue(raw) {
  if (!raw) return null;
  let value;
  try { value = decodeURIComponent(String(raw)); } catch { return null; }
  const dot = value.lastIndexOf('.');
  if (dot <= 0) return null;
  const link_name = value.slice(0, dot).trim().toLowerCase();
  const attribution_id = value.slice(dot + 1).trim();
  if (!link_name || !attribution_id) return null;
  return { link_name, attribution_id };
}

// Read the carrier from whichever surface the join moment has:
//   readAttribution({ cookieHeader, url })          — server / worker side
//   readAttribution({ cookieString, search })       — browser side
// Returns { link_name, attribution_id|null, source: 'cookie'|'param' } or
// null when no carrier is present. The param carries the link name only;
// the cookie is the durable half and wins when both exist.
export function readAttribution(input) {
  const { cookieHeader, cookieString, url, search } = input || {};
  const cookieRaw = cookieHeader ?? cookieString;
  if (cookieRaw) {
    for (const part of String(cookieRaw).split(';')) {
      const eq = part.indexOf('=');
      if (eq < 0) continue;
      if (part.slice(0, eq).trim() === ATTRIBUTION_COOKIE) {
        const parsed = parseAttributionValue(part.slice(eq + 1).trim());
        if (parsed) return { ...parsed, source: 'cookie' };
      }
    }
  }
  let paramRaw = null;
  if (url) {
    try { paramRaw = new URL(url).searchParams.get(ATTRIBUTION_PARAM); } catch { paramRaw = null; }
  }
  if (paramRaw === null && search) {
    try { paramRaw = new URLSearchParams(search).get(ATTRIBUTION_PARAM); } catch { paramRaw = null; }
  }
  if (paramRaw) {
    const link_name = String(paramRaw).trim().toLowerCase();
    if (link_name) return { link_name, attribution_id: null, source: 'param' };
  }
  return null;
}
