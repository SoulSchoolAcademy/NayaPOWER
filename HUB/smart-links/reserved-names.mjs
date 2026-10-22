// reserved-names.mjs — the ONE reserved-name list for Smart Links.
//
// A Smart Link name becomes nayanet.live/<name>. Any name that collides with
// a real route, room, file, or system path on the live site would shadow it —
// so these names can never be minted as links. This module is the single
// source: the redirect worker refuses them, the database seed in
// supabase/migrations/20261022201500_smart_links_v1.sql mirrors them (a pytest
// contract test asserts the two never drift), and the future creation UI
// validates against validateLinkName() before a link exists.
//
// Provenance of the list:
//  - The Smart Links spec, via the Best-of-Best application map (element #3):
//    /rooms/*, /s/*, /identity.html are named there verbatim.
//  - Live route inventory of nayanet.live from this repo: the Hub worker's
//    SPA + rooms (HUB/app/index.html ROOMS), the naya-share worker routes
//    (/s/*, /share-img/*), the sync heartbeat file, the Welcome door and the
//    identity certificate (DESIGN-LANGUAGE SS9.2/SS9.4).
//  - The minted Smart Note link prefix /sn/<id> (feature_smart_notes.py).
//  - Ordinary web infrastructure names no short-link system may take.

export const RESERVED_NAMES = Object.freeze([
  // — named in the spec / application map —
  'rooms', 's', 'identity', 'identity.html',
  // — Hub rooms and shell routes (HUB/app/index.html) —
  'hub', 'feed', 'today', 'reports', 'library', 'connect', 'ledger',
  'connections', 'lists', 'mail', 'spaces', 'settings', 'start', 'start-here',
  // — live workers, files, and minted prefixes —
  'sn', 'share-img', 'sync-heartbeat', 'sync-heartbeat.json',
  'index', 'index.html', 'favicon.ico', 'robots.txt', 'sitemap.xml',
  'manifest.webmanifest', 'well-known',
  // — product doors (ONE universal app, many front doors) —
  'welcome', 'join', 'invite', 'invites', 'signup', 'login', 'signin',
  'dashboard', 'booking', 'product', 'events', 'community', 'profile',
  'menu', 'factory', 'growth',
  // — infrastructure / generic —
  'api', 'app', 'assets', 'static', 'public', 'admin', 'support', 'help',
  'about', 'privacy', 'terms', 'www', 'naya', 'nayanet',
]);

const RESERVED_SET = new Set(RESERVED_NAMES);

// Link names are single path segments: lowercase letters, digits, hyphens,
// 2–63 chars, never starting with a hyphen. No dots — so a link name can
// never impersonate a file (the dotted entries above are belt-and-braces
// for callers that hand us a raw path segment).
export const LINK_NAME_PATTERN = /^[a-z0-9][a-z0-9-]{1,62}$/;

export function normalizeLinkName(raw) {
  return String(raw ?? '').trim().toLowerCase();
}

export function isReservedName(raw) {
  return RESERVED_SET.has(normalizeLinkName(raw));
}

// Returns { ok: true, name } or { ok: false, reason } — reason is
// machine-readable: 'empty' | 'bad_shape' | 'reserved'.
export function validateLinkName(raw) {
  const name = normalizeLinkName(raw);
  if (!name) return { ok: false, reason: 'empty' };
  if (!LINK_NAME_PATTERN.test(name)) return { ok: false, reason: 'bad_shape' };
  if (RESERVED_SET.has(name)) return { ok: false, reason: 'reserved' };
  return { ok: true, name };
}
