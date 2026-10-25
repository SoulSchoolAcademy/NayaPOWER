// Citizen API v1 — production-ready logic, worker-agnostic.
// Web-standard: Request/Response, crypto.subtle. No platform imports.
// Store is pluggable: in-memory store is used by tests; production
// wires the same interface to Supabase (see production/supabase-adapter-NOTES.md).
// Secrets: NEVER logged, NEVER stored in clear. Only SHA-256 hashes.
// Decisions (see DECISIONS.md): D1 new Supabase Edge Function host,
// D2 quiet writes 402, D3 simple membership field, D4 naya_live_ prefix,
// D5 no Projects in v1, D6 consent list below.
// NO mail operations. NO Smart Mail privacy claims.
// NOT DEPLOYED. Ready to make live only when: deploy hold clears,
// Nitro rendered review passes, phone check passes, fork isolation
// passes or row C stays limited, merchant keys + payout terms land
// (for checkout, not for this API itself).
//
// v3 — Resolve's return patch, ADOPTED verbatim as the base for v4
// (2026-10-25): R1 expires_in, R2 reuse detection (refined: one
// replay of the immediate predecessor tolerated, second replay or
// older generation resurfacing kills the family), R3 last_used =
// PREVIOUS use, null on first call. Power re-ran her suite against
// v3: exactly one assertion failed, the old always-now last_used
// assertion, named by Resolve — adjusted here to the honest
// semantics (first call null, second call shows the previous use).
//
// v4 — Elite upgrades (Resolve's 10x list items 2-9, plus Power's
// reflection items that are code-feasible). Item 1 was adopt v3.
// Item 10 (land in repo) is PREPARED, not pushed — see repo-packet
// manifest; a push needs a PR with different-seat review at the
// exact head, which is Resolve's own rule for item 10.
// E2 ledger events: every connection event is emitted to
//    store.events (adapter writes to ledger_entries) — never secrets.
// E3 redirect exact-match: ONE allowed redirect, named here,
//    PROPOSED, must be confirmed before the authorize page is built.
//    No wildcards, no prefix matching, mismatch = 400.
// E4 PKCE MANDATORY at authorize: challenge required, S256 only.
//    Exchange still enforces a challenge when one was stored.
// E5 throttle public endpoints: 60/min per endpoint+IP (harness
//    only — adapter must use real IP + distributed store).
// E6 purgeDead(): codes 1h after expiry, tokens 30 days after
//    expiry, NEVER purge a revoked refresh before its whole family
//    expires. Scheduled by the adapter, never automatic on requests.
// E7 idempotency on POST /v1/notes: Idempotency-Key, alias-scoped,
//    same body replay returns the original, different body = 409,
//    never a disconnect, never a family kill.
// E8 "Your connections" inventory: GET /api/v1/connections
//    (session) + POST /api/v1/connections/revoke (session, id/family).
// E9 aggregate usage on /v1/me + connections: ONE true total across
//    credentials, plus trial info when joinedAt is known.
// Plain-words actions on 401/402/429 so a citizen hears what to tap.

export const RATE_LIMIT = 1000;
export const THROTTLE_LIMIT = 60;
export const THROTTLE_WINDOW_MS = 60 * 1000;
// E3: PROPOSED single redirect. Confirm with Nitro/Hub before the
// authorize page is built. This value is the allowlist, not a guess
// at runtime — any other redirect_uri is refused.
export const ALLOWED_REDIRECT_URI = "https://nayanet.live/connect/callback";
export const CONSENT_LIST = [
  "Read your identity and your four pages.",
  "Read your own notes and pages.",
  "Create notes for you, quick or smart.",
  "See when your Muse last used the connection.",
  "Nothing else. No mail.",
  "You can revoke any time from your dashboard card, and revocation cuts access immediately.",
];

function json(status, obj) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}
function err(status, message, extra = {}) {
  const out = { error: status, message, ...extra };
  if (status === 402) { out.renew = "Your connection is quiet until paid."; out.action = "Renew to keep creating."; }
  if (status === 401) out.action = "Reconnect from your dashboard.";
  if (status === 429) out.action = "Wait and retry. The limit resets daily.";
  return json(status, out);
}
async function sha256Hex(s) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}
async function sha256B64Url(s) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  const bytes = new Uint8Array(buf);
  let bin = "";
  for (const b of bytes) bin += String.fromCharCode(b);
  return btoa(bin).replace(/\+/g, "-").replace(/\//g, "_").replace(/=/g, "");
}
function randomToken(prefix) {
  const bytes = new Uint8Array(24);
  crypto.getRandomValues(bytes);
  let b64;
  if (typeof Buffer !== "undefined") {
    b64 = Buffer.from(bytes).toString("base64url");
  } else {
    let bin = "";
    for (const b of bytes) bin += String.fromCharCode(b);
    b64 = btoa(bin).replace(/\+/g, "-").replace(/\//g, "_").replace(/=/g, "");
  }
  return prefix + b64;
}
function todayStr() { return new Date().toISOString().slice(0, 10); }

export function deriveMembership({ joinedAt, paid, now = Date.now() } = {}) {
  if (paid) return "paid";
  if (!joinedAt) return "trial";
  const joined = typeof joinedAt === "number" ? joinedAt : Date.parse(joinedAt);
  if (Number.isNaN(joined)) return "trial";
  const days = (now - joined) / (24 * 3600 * 1000);
  return days <= 5 ? "trial" : "quiet";
}

export class MemoryStore {
  constructor() {
    this.citizens = new Map();
    this.keys = new Map();
    this.tokens = new Map();
    this.codes = new Map();
    this.notes = new Map();
    this.sessions = new Map();
    this.events = [];
    this.idempotency = new Map();
    this.throttle = new Map();
    this.allowedRedirectUri = ALLOWED_REDIRECT_URI;
    this.seq = 0;
  }
  addCitizen(alias, membership, pages, opts = {}) {
    this.citizens.set(alias, { alias, membership, joinedAt: opts.joinedAt || null, paid: !!opts.paid, pages: pages || {
      personal: `https://nayanet.live/world/${alias}`,
      business: `https://nayanet.live/world/${alias}/business`,
      space: `https://nayanet.live/world/${alias}/space`,
      dashboard: `https://nayanet.live/world/${alias}#dashboard`,
    }});
    if (!this.notes.has(alias)) this.notes.set(alias, []);
  }
}

export function revokeTokenFamily(store, family) {
  if (!family) return;
  for (const tok of store.tokens.values()) {
    if (tok.family === family && !tok.revoked) { tok.revoked = true; tok.revokeReason = "family"; }
  }
}

// E2: ledger event. Adapter writes store.events to ledger_entries.
// Never secrets, never hashes, never bodies — alias, credential id,
// operation, time only.
export function emit(store, event) {
  const e = { at: new Date().toISOString(), ...event };
  store.events.push(e);
  console.log(JSON.stringify(e));
  return e;
}

export function aggregateUsage(store, alias) {
  const today = todayStr();
  let requests_today_total = 0;
  for (const k of store.keys.values()) if (k.alias === alias && k.day === today) requests_today_total += k.requestsToday || 0;
  for (const t of store.tokens.values()) if (t.alias === alias && t.day === today) requests_today_total += t.requestsToday || 0;
  const keys_active = [...store.keys.values()].filter((k) => k.alias === alias && !k.revoked).length;
  const families = new Set();
  for (const t of store.tokens.values()) {
    if (t.alias === alias && !t.revoked && Date.now() <= t.expiresAt) families.add(t.family);
  }
  return { requests_today_total, notes_total: (store.notes.get(alias) || []).length, keys_active, families_active: families.size };
}

// E6: purge dead state. Scheduled by adapter, never on requests.
// Codes: 1h after expiry. Tokens: 30 days after expiry, AND for
// refresh tokens only when the whole family is fully expired.
export function purgeDead(store, now = Date.now()) {
  let codes = 0, tokens = 0;
  for (const [code, rec] of [...store.codes.entries()]) {
    if (rec.expiresAt + 3600 * 1000 < now) { store.codes.delete(code); codes += 1; }
  }
  for (const [hash, tok] of [...store.tokens.entries()]) {
    if (tok.expiresAt + 30 * 24 * 3600 * 1000 < now) {
      if (tok.kind === "refresh") {
        const famMax = Math.max(...[...store.tokens.values()].filter((t) => t.family === tok.family).map((t) => t.expiresAt));
        if (famMax >= now) continue;
      }
      store.tokens.delete(hash); tokens += 1;
    }
  }
  return { codes, tokens };
}

export function createHandler(store) {
  async function checkRate(rec) {
    const today = todayStr();
    if (rec.day !== today) { rec.day = today; rec.requestsToday = 0; }
    rec.requestsToday += 1;
    if (rec.requestsToday > RATE_LIMIT) throw { status: 429, message: "rate limit exceeded" };
  }
  function checkThrottle(req, endpoint) {
    const fwd = req.headers.get("X-Forwarded-For") || "";
    const ip = fwd ? fwd.split(",")[0].trim() : "unknown";
    const key = `${endpoint}|${ip}`;
    const now = Date.now();
    const rec = store.throttle.get(key) || { count: 0, start: now };
    if (now - rec.start >= THROTTLE_WINDOW_MS) { rec.count = 0; rec.start = now; }
    rec.count += 1;
    store.throttle.set(key, rec);
    if (rec.count > THROTTLE_LIMIT) throw { status: 429, message: "too many attempts" };
  }
  async function auth(req) {
    const h = req.headers.get("Authorization") || "";
    if (!h.startsWith("Bearer ")) throw { status: 401, message: "unauthorized: Bearer key required" };
    const secret = h.slice(7);
    const hash = await sha256Hex(secret);
    const key = store.keys.get(hash);
    if (key && !key.revoked) {
      await checkRate(key);
      const prevUsed = key.lastUsed;
      key.lastUsed = Date.now();
      return { alias: key.alias, cred: key, prevUsed };
    }
    const tok = store.tokens.get(hash);
    const now = Date.now();
    if (tok && !tok.revoked && tok.kind === "access" && now <= tok.expiresAt) {
      await checkRate(tok);
      const prevUsed = tok.lastUsed;
      tok.lastUsed = now;
      return { alias: tok.alias, cred: tok, prevUsed };
    }
    throw { status: 401, message: "unauthorized" };
  }
  async function sessionAuth(req) {
    const h = req.headers.get("Authorization") || "";
    if (!h.startsWith("Bearer ")) throw { status: 401, message: "unauthorized: dashboard session required" };
    const hash = await sha256Hex(h.slice(7));
    const alias = store.sessions.get(hash);
    if (!alias) throw { status: 401, message: "unauthorized: dashboard session required" };
    return alias;
  }
  async function me(alias, cred, prevUsed) {
    const c = store.citizens.get(alias);
    if (!c) throw { status: 404, message: "citizen not found" };
    let membership_info = null;
    if (c.joinedAt) {
      const joined = typeof c.joinedAt === "number" ? c.joinedAt : Date.parse(c.joinedAt);
      if (!Number.isNaN(joined)) {
        membership_info = {
          paid: !!c.paid,
          trial_days_remaining: c.paid ? null : Math.max(0, Math.ceil((joined + 5 * 24 * 3600 * 1000 - Date.now()) / (24 * 3600 * 1000))),
          quiet_at: new Date(joined + 5 * 24 * 3600 * 1000).toISOString(),
        };
      }
    }
    return {
      alias: c.alias,
      membership: c.membership,
      pages: c.pages,
      last_used: prevUsed ? new Date(prevUsed).toISOString() : null,
      membership_info,
      usage: aggregateUsage(store, alias),
    };
  }
  async function parseBody(req) {
    const ct = (req.headers.get("Content-Type") || "").toLowerCase();
    if (ct.includes("application/x-www-form-urlencoded")) {
      const text = await req.text();
      const params = new URLSearchParams(text);
      const out = {};
      for (const [k, v] of params.entries()) out[k] = v;
      return out;
    }
    return req.json().catch(() => ({}));
  }
  async function issueTokenPair(alias, family) {
    store.seq += 1;
    const fam = family || `fam-${store.seq}`;
    let gen = 1;
    for (const t of store.tokens.values()) if (t.family === fam && (t.gen || 0) >= gen) gen = (t.gen || 0) + 1;
    const access = randomToken("naya_at_");
    const refresh = randomToken("naya_rt_");
    const now = Date.now();
    store.tokens.set(await sha256Hex(access), { id: `tok-${store.seq}`, alias, kind: "access", family: fam, gen, expiresAt: now + 3600 * 1000, revoked: false, revokeReason: null, replays: 0, requestsToday: 0, day: "", lastUsed: null, createdAt: now });
    store.tokens.set(await sha256Hex(refresh), { id: `tok-${store.seq}r`, alias, kind: "refresh", family: fam, gen, expiresAt: now + 30 * 24 * 3600 * 1000, revoked: false, revokeReason: null, replays: 0, requestsToday: 0, day: "", lastUsed: null, createdAt: now });
    return { access, refresh, family: fam };
  }
  return async function handler(req) {
    try {
      const url = new URL(req.url);
      const path = url.pathname;
      if (req.method === "GET" && path === "/api/v1/me") {
        const { alias, cred, prevUsed } = await auth(req);
        return json(200, await me(alias, cred, prevUsed));
      }
      if (req.method === "GET" && path === "/api/v1/pages") {
        const { alias, cred, prevUsed } = await auth(req);
        return json(200, (await me(alias, cred, prevUsed)).pages);
      }
      if (req.method === "GET" && path === "/api/v1/notes") {
        const { alias } = await auth(req);
        const limit = Math.max(1, Math.min(100, parseInt(url.searchParams.get("limit") || "50", 10) || 50));
        const all = store.notes.get(alias) || [];
        return json(200, [...all].reverse().slice(0, limit));
      }
      if (req.method === "POST" && path === "/api/v1/notes") {
        const { alias, cred } = await auth(req);
        const c = store.citizens.get(alias);
        if (!c) throw { status: 404, message: "citizen not found" };
        if (c.membership === "quiet") throw { status: 402, message: "renew to keep creating — your connection is quiet until paid" };
        const body = await parseBody(req);
        if (body.kind !== "quick" && body.kind !== "smart") throw { status: 400, message: "kind must be quick or smart" };
        if (typeof body.body !== "string" || !body.body.trim() || body.body.length > 20000) throw { status: 400, message: "body must be non-empty text, max 20000 chars" };
        if (body.title && String(body.title).length > 200) throw { status: 400, message: "title max 200 chars" };
        // E7 idempotency: alias-scoped, same body replay = original,
        // different body = 409, never a disconnect or family kill.
        const idemKey = req.headers.get("Idempotency-Key");
        if (idemKey) {
          const ikey = `${alias}\0${idemKey}`;
          const bodySig = JSON.stringify({ kind: body.kind, body: body.body, title: body.title || null, nutshell: body.nutshell || null });
          const prev = store.idempotency.get(ikey);
          if (prev) {
            if (prev.bodySig !== bodySig) throw { status: 409, message: "idempotency key reused with different body" };
            return json(201, { created: true, replayed: true, note: prev.note });
          }
          const note = { kind: body.kind, body: body.body, title: body.title || null, nutshell: body.nutshell || null, key_id: cred.id };
          store.notes.get(alias).push(note);
          store.idempotency.set(ikey, { bodySig, note });
          emit(store, { alias, key_id: cred.id, operation: "notes.create", kind: body.kind });
          return json(201, { created: true, note });
        }
        const note = { kind: body.kind, body: body.body, title: body.title || null, nutshell: body.nutshell || null, key_id: cred.id };
        store.notes.get(alias).push(note);
        emit(store, { alias, key_id: cred.id, operation: "notes.create", kind: body.kind });
        return json(201, { created: true, note });
      }
      if (req.method === "POST" && path === "/api/v1/keys") {
        const alias = await sessionAuth(req);
        const body = await parseBody(req);
        const made = await makeKey(store, alias, typeof body.label === "string" && body.label ? body.label.slice(0, 100) : "dashboard");
        emit(store, { alias, key_id: made.id, operation: "keys.create" });
        return json(201, made);
      }
      // E8 inventory: session only, no secrets, no hashes.
      if (req.method === "GET" && path === "/api/v1/connections") {
        const alias = await sessionAuth(req);
        const keys = [...store.keys.values()].filter((k) => k.alias === alias).map((k) => ({ type: "key", id: k.id, label: k.label, last4: k.last4, created_at: k.createdAt ? new Date(k.createdAt).toISOString() : null, last_used: k.lastUsed ? new Date(k.lastUsed).toISOString() : null, revoked: !!k.revoked }));
        const famMap = new Map();
        for (const t of store.tokens.values()) {
          if (t.alias !== alias) continue;
          if (!famMap.has(t.family)) famMap.set(t.family, { type: "token_family", family: t.family, gen: t.gen || 1, created_at: t.createdAt ? new Date(t.createdAt).toISOString() : null, last_used: null, revoked: true });
          const f = famMap.get(t.family);
          if (t.createdAt && (!f.created_at || t.createdAt < Date.parse(f.created_at))) f.created_at = new Date(t.createdAt).toISOString();
          if (t.lastUsed && (!f.last_used || t.lastUsed > Date.parse(f.last_used))) f.last_used = new Date(t.lastUsed).toISOString();
          if (!t.revoked && Date.now() <= t.expiresAt) f.revoked = false;
          if ((t.gen || 1) > f.gen) f.gen = t.gen;
        }
        return json(200, { connections: [...keys, ...famMap.values()], usage: aggregateUsage(store, alias) });
      }
      if (req.method === "POST" && path === "/api/v1/connections/revoke") {
        const alias = await sessionAuth(req);
        const body = await parseBody(req);
        if (body.family) {
          const found = [...store.tokens.values()].some((t) => t.alias === alias && t.family === body.family);
          if (!found) throw { status: 404, message: "connection not found" };
          revokeTokenFamily(store, body.family);
          emit(store, { alias, family: body.family, operation: "oauth.revoke" });
          return json(200, { revoked: true, family: body.family });
        }
        if (body.id) {
          const key = [...store.keys.values()].find((k) => k.alias === alias && k.id === body.id);
          if (key) { key.revoked = true; emit(store, { alias, key_id: key.id, operation: "keys.revoke" }); return json(200, { revoked: true, id: key.id }); }
          const tok = [...store.tokens.values()].find((t) => t.alias === alias && t.id === body.id);
          if (tok) { revokeTokenFamily(store, tok.family); emit(store, { alias, family: tok.family, operation: "oauth.revoke" }); return json(200, { revoked: true, family: tok.family }); }
          throw { status: 404, message: "connection not found" };
        }
        throw { status: 400, message: "id or family required" };
      }
      if (req.method === "POST" && path === "/oauth/authorize") {
        checkThrottle(req, "oauth.authorize");
        const alias = await sessionAuth(req);
        const body = await parseBody(req);
        // E4 PKCE mandatory, E3 redirect exact-match.
        if (!body.code_challenge) throw { status: 400, message: "code_challenge required (PKCE S256 mandatory)" };
        if (body.code_challenge_method && body.code_challenge_method !== "S256") throw { status: 400, message: "code_challenge_method must be S256" };
        const allowed = store.allowedRedirectUri || ALLOWED_REDIRECT_URI;
        if (body.redirect_uri && body.redirect_uri !== allowed) throw { status: 400, message: "redirect_uri not allowed" };
        const code = await issueCode(store, alias, {
          code_challenge: body.code_challenge,
          code_challenge_method: "S256",
        });
        emit(store, { alias, operation: "oauth.authorize" });
        return json(200, { code, state: body.state || null, redirect_uri: allowed, consent: CONSENT_LIST });
      }
      if (req.method === "POST" && path === "/oauth/token") {
        checkThrottle(req, "oauth.token");
        const body = await parseBody(req);
        if (body.grant_type === "authorization_code") {
          const rec = store.codes.get(body.code || "");
          if (!rec) throw { status: 400, message: "invalid authorization code" };
          if (rec.used) throw { status: 400, message: "authorization code already used" };
          if (Date.now() > rec.expiresAt) throw { status: 400, message: "authorization code expired" };
          if (rec.code_challenge) {
            if (!body.code_verifier) throw { status: 400, message: "code_verifier required" };
            const calc = await sha256B64Url(body.code_verifier);
            if (calc !== rec.code_challenge) throw { status: 400, message: "invalid code_verifier" };
          }
          rec.used = true;
          const pair = await issueTokenPair(rec.alias, rec.family);
          emit(store, { alias: rec.alias, family: pair.family, operation: "oauth.token" });
          return json(200, { access_token: pair.access, refresh_token: pair.refresh, token_type: "Bearer", expires_in: 3600 });
        }
        if (body.grant_type === "refresh_token") {
          const hash = await sha256Hex(body.refresh_token || "");
          const tok = store.tokens.get(hash);
          let killedFamily = null;
          if (tok && tok.kind === "refresh" && tok.revoked && tok.revokeReason === "rotation") {
            tok.replays = (tok.replays || 0) + 1;
            const olderGeneration = [...store.tokens.values()].some((t) => t.family === tok.family && t.kind === "refresh" && t.revokeReason === "rotation" && (t.gen || 0) > (tok.gen || 0));
            if (tok.replays > 1 || olderGeneration) { revokeTokenFamily(store, tok.family); killedFamily = tok.family; }
          }
          if (killedFamily) emit(store, { alias: tok.alias, family: killedFamily, operation: "oauth.reuse_kill" });
          if (!tok || tok.revoked || tok.kind !== "refresh" || Date.now() > tok.expiresAt) throw { status: 401, message: "unauthorized" };
          tok.revoked = true; tok.revokeReason = "rotation";
          const pair = await issueTokenPair(tok.alias, tok.family);
          emit(store, { alias: tok.alias, family: pair.family, operation: "oauth.refresh" });
          return json(200, { access_token: pair.access, refresh_token: pair.refresh, token_type: "Bearer", expires_in: 3600 });
        }
        throw { status: 400, message: "unsupported grant_type" };
      }
      if (req.method === "POST" && path === "/oauth/revoke") {
        checkThrottle(req, "oauth.revoke");
        const body = await parseBody(req);
        if (body.token) {
          const hash = await sha256Hex(body.token);
          const tok = store.tokens.get(hash);
          if (tok) { revokeTokenFamily(store, tok.family); emit(store, { alias: tok.alias, family: tok.family, operation: "oauth.revoke" }); }
          const key = store.keys.get(hash);
          if (key) { key.revoked = true; emit(store, { alias: key.alias, key_id: key.id, operation: "keys.revoke" }); }
        }
        return json(200, { revoked: true });
      }
      return err(404, "not found");
    } catch (e) {
      if (e && typeof e.status === "number") return err(e.status, e.message);
      return err(500, "internal error");
    }
  };
}

export async function makeKey(store, alias, label) {
  if (!store.citizens.has(alias)) throw new Error("citizen not found");
  const secret = randomToken("naya_live_");
  const hash = await sha256Hex(secret);
  store.seq += 1;
  const rec = { id: `key-${store.seq}`, alias, label, hash, last4: secret.slice(-4), revoked: false, requestsToday: 0, day: "", lastUsed: null, createdAt: Date.now() };
  store.keys.set(hash, rec);
  return { secret, id: rec.id, last4: rec.last4 };
}
export async function issueCode(store, alias, opts = {}) {
  const code = randomToken("auth_");
  store.seq += 1;
  store.codes.set(code, {
    alias,
    expiresAt: Date.now() + 600 * 1000,
    used: false,
    code_challenge: opts.code_challenge || null,
    code_challenge_method: opts.code_challenge_method || null,
    family: `fam-${store.seq}`,
  });
  return code;
}
export async function makeSession(store, alias) {
  if (!store.citizens.has(alias)) throw new Error("citizen not found");
  const token = randomToken("naya_session_");
  store.sessions.set(await sha256Hex(token), alias);
  return token;
}
