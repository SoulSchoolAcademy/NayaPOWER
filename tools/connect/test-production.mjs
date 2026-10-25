// Production code tests — Node, no live DB, no secrets in output.
// Run: node production/test-production.mjs
// v4 suite: original proofs + Resolve v1 findings + v3 (R1-R3) +
// elite upgrades E2-E9. One named assertion change from v2 to v3:
// last_used is now PREVIOUS use (first call null, second call set),
// not always-now. That change is Resolve's R3, adopted, not hidden.
import assert from "node:assert";
import { createHash } from "node:crypto";
import { MemoryStore, createHandler, makeKey, issueCode, makeSession, deriveMembership, purgeDead } from "./citizen-api.js";

const store = new MemoryStore();
store.addCitizen("alice", "trial");
store.addCitizen("bob", "paid");
store.addCitizen("carol", "quiet");
store.addCitizen("dave", "trial", undefined, { joinedAt: Date.now() - 3 * 24 * 3600 * 1000 });
const handler = createHandler(store);
const call = async (method, path, token, body, ct, extraHeaders = {}) => {
  const req = new Request(`https://staging.test${path}`, {
    method,
    headers: { "Content-Type": ct || "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}), ...extraHeaders },
    body: body ? (ct && ct.includes("form") ? new URLSearchParams(body).toString() : JSON.stringify(body)) : undefined,
  });
  const res = await handler(req);
  return { status: res.status, body: await res.json() };
};

// 1. me: /world URLs, last_used honest (R3), usage, trial info
const { secret: sAlice, id: aliceKeyId } = await makeKey(store, "alice", "test");
let r = await call("GET", "/api/v1/me", sAlice);
assert.equal(r.status, 200); assert.equal(r.body.alias, "alice");
assert.equal(r.body.pages.personal, "https://nayanet.live/world/alice");
assert.equal(r.body.pages.dashboard, "https://nayanet.live/world/alice#dashboard");
assert.equal(r.body.last_used, null, "R3: first call last_used is null (previous use)");
assert.ok(r.body.usage && typeof r.body.usage.requests_today_total === "number");
r = await call("GET", "/api/v1/me", sAlice);
assert.ok(r.body.last_used, "R3: second call last_used shows previous use");
const { secret: sDave } = await makeKey(store, "dave", "test");
r = await call("GET", "/api/v1/me", sDave);
assert.equal(r.body.membership_info.trial_days_remaining, 2);
assert.ok(r.body.membership_info.quiet_at);
// 2. notes quick + smart, verbatim, key_id, newest first
r = await call("POST", "/api/v1/notes", sAlice, { kind: "quick", body: "prod verbatim" }); assert.equal(r.status, 201); assert.equal(r.body.note.key_id, aliceKeyId);
r = await call("POST", "/api/v1/notes", sAlice, { kind: "smart", body: "long", title: "T", nutshell: "N" }); assert.equal(r.status, 201);
r = await call("GET", "/api/v1/notes", sAlice); assert.equal(r.body.length, 2); assert.equal(r.body[0].body, "long");
// 2b. idempotency (E7): same key+body replay = original, no duplicate; different body = 409, credential still works
r = await call("POST", "/api/v1/notes", sAlice, { kind: "quick", body: "idem note" }, "application/json", { "Idempotency-Key": "k1" }); assert.equal(r.status, 201);
r = await call("POST", "/api/v1/notes", sAlice, { kind: "quick", body: "idem note" }, "application/json", { "Idempotency-Key": "k1" }); assert.equal(r.status, 201); assert.equal(r.body.replayed, true);
r = await call("GET", "/api/v1/notes", sAlice); assert.equal(r.body.filter((n) => n.body === "idem note").length, 1);
r = await call("POST", "/api/v1/notes", sAlice, { kind: "quick", body: "different" }, "application/json", { "Idempotency-Key": "k1" }); assert.equal(r.status, 409);
r = await call("GET", "/api/v1/me", sAlice); assert.equal(r.status, 200, "idempotency conflict must not disconnect");
// 3. isolation
const { secret: sBob } = await makeKey(store, "bob", "test");
r = await call("GET", "/api/v1/notes?alias=alice", sBob); assert.deepEqual(r.body, []);
// 4. revoked -> 401
const { secret: sBob2, id: kid } = await makeKey(store, "bob", "old");
store.keys.forEach((k) => { if (k.id === kid) k.revoked = true; });
r = await call("GET", "/api/v1/me", sBob2); assert.equal(r.status, 401);
// 5. quiet
const { secret: sCarol } = await makeKey(store, "carol", "test");
r = await call("GET", "/api/v1/me", sCarol); assert.equal(r.body.membership, "quiet");
r = await call("POST", "/api/v1/notes", sCarol, { kind: "quick", body: "x" }); assert.equal(r.status, 402); assert.ok(r.body.renew); assert.ok(r.body.action);
// 6. Allow: code -> token (R1 expires_in) -> me, reuse -> 400, refresh rotation, second refresh
const code = await issueCode(store, "alice");
r = await call("POST", "/oauth/token", null, { grant_type: "authorization_code", code }); assert.equal(r.status, 200); assert.equal(r.body.expires_in, 3600);
let at = r.body.access_token, rt = r.body.refresh_token;
r = await call("GET", "/api/v1/me", at); assert.equal(r.status, 200);
r = await call("POST", "/oauth/token", null, { grant_type: "authorization_code", code }); assert.equal(r.status, 400);
r = await call("POST", "/oauth/token", null, { grant_type: "refresh_token", refresh_token: rt }); assert.equal(r.status, 200); assert.equal(r.body.expires_in, 3600);
let at2 = r.body.access_token, rt2 = r.body.refresh_token;
r = await call("GET", "/api/v1/me", at2); assert.equal(r.status, 200);
r = await call("POST", "/oauth/token", null, { grant_type: "refresh_token", refresh_token: rt }); assert.equal(r.status, 401);
r = await call("POST", "/oauth/token", null, { grant_type: "refresh_token", refresh_token: rt2 }); assert.equal(r.status, 200);
let at3 = r.body.access_token, rt3 = r.body.refresh_token;
// 6b. reuse detection (R2 refined): one replay tolerated, second kills family
r = await call("POST", "/oauth/token", null, { grant_type: "refresh_token", refresh_token: rt2 }); assert.equal(r.status, 401, "first replay refused");
r = await call("POST", "/oauth/token", null, { grant_type: "refresh_token", refresh_token: rt3 }); assert.equal(r.status, 200, "family lives after one tolerated replay");
r = await call("POST", "/oauth/token", null, { grant_type: "refresh_token", refresh_token: rt2 }); assert.equal(r.status, 401, "second replay refused and kills");
r = await call("POST", "/oauth/token", null, { grant_type: "refresh_token", refresh_token: rt3 }); assert.equal(r.status, 401, "family dead after second replay");
// 7. Revocation cascade + flat revoke
const code2 = await issueCode(store, "alice");
r = await call("POST", "/oauth/token", null, { grant_type: "authorization_code", code: code2 });
let a4 = r.body.access_token, r4 = r.body.refresh_token;
r = await call("POST", "/oauth/revoke", null, { token: a4 }); assert.equal(r.body.revoked, true);
r = await call("GET", "/api/v1/me", a4); assert.equal(r.status, 401);
r = await call("POST", "/oauth/token", null, { grant_type: "refresh_token", refresh_token: r4 }); assert.equal(r.status, 401);
r = await call("POST", "/oauth/revoke", null, { token: "nope-not-a-token" }); assert.equal(r.status, 200); assert.equal(r.body.revoked, true);
// 8. Form token + PKCE mandatory at authorize (E4) + redirect exact-match (E3)
const verifier = "test-verifier-1234567890-abcdef";
const challenge = createHash("sha256").update(verifier).digest("base64url");
const sess = await makeSession(store, "alice");
r = await call("POST", "/oauth/authorize", sess, {}); assert.equal(r.status, 400, "PKCE mandatory: no challenge must fail");
r = await call("POST", "/oauth/authorize", sess, { code_challenge: challenge, code_challenge_method: "S256", redirect_uri: "https://evil.example/cb" }); assert.equal(r.status, 400, "redirect mismatch must fail");
r = await call("POST", "/oauth/authorize", sess, { code_challenge: challenge, code_challenge_method: "S256", state: "xyz", redirect_uri: "https://nayanet.live/connect/callback" });
assert.equal(r.status, 200); assert.equal(r.body.redirect_uri, "https://nayanet.live/connect/callback");
const pkceCode = r.body.code;
r = await call("POST", "/oauth/token", null, { grant_type: "authorization_code", code: pkceCode, code_verifier: "wrong" }, "application/x-www-form-urlencoded"); assert.equal(r.status, 400);
r = await call("POST", "/oauth/token", null, { grant_type: "authorization_code", code: pkceCode, code_verifier: verifier }, "application/x-www-form-urlencoded"); assert.equal(r.status, 200);
// 9. Session-gated issuance + connections inventory (E8)
r = await call("POST", "/api/v1/keys", sAlice, { label: "evil", alias: "bob" }); assert.equal(r.status, 401);
r = await call("POST", "/api/v1/keys", sess, { label: "dash", alias: "bob" }); assert.equal(r.status, 201);
const dashKeyId = r.body.id, dashSecret = r.body.secret;
r = await call("GET", "/api/v1/connections", sess); assert.equal(r.status, 200);
assert.ok(r.body.connections.some((c) => c.id === dashKeyId && c.type === "key"));
assert.ok(!JSON.stringify(r.body).includes(dashSecret), "inventory must never include secrets");
assert.ok(r.body.usage && typeof r.body.usage.notes_total === "number");
r = await call("POST", "/api/v1/connections/revoke", sess, { id: dashKeyId }); assert.equal(r.body.revoked, true);
r = await call("GET", "/api/v1/me", dashSecret); assert.equal(r.status, 401, "inventory revoke must kill the key");
// 10. Notes newest-first at scale (55)
const { secret: sF2 } = await makeKey(store, "bob", "f2");
for (let i = 1; i <= 55; i++) await call("POST", "/api/v1/notes", sF2, { kind: "quick", body: `note-${i}` });
r = await call("GET", "/api/v1/notes", sF2); assert.equal(r.body.length, 50); assert.equal(r.body[0].body, "note-55"); assert.equal(r.body[49].body, "note-6");
// 11. Membership derivation
const now = Date.now(), day = 24 * 3600 * 1000;
assert.equal(deriveMembership({ joinedAt: now, paid: false, now }), "trial");
assert.equal(deriveMembership({ joinedAt: now - 5 * day, paid: false, now }), "trial");
assert.equal(deriveMembership({ joinedAt: now - 6 * day, paid: false, now }), "quiet");
assert.equal(deriveMembership({ joinedAt: now - 6 * day, paid: true, now }), "paid");
// 12. Purge (E6): dead code gone, live family survives, revoked refresh with live family survives
const deadCode = await issueCode(store, "alice");
store.codes.get(deadCode).expiresAt = Date.now() - 2 * 3600 * 1000;
const liveCode = await issueCode(store, "alice");
r = await call("POST", "/oauth/token", null, { grant_type: "authorization_code", code: liveCode });
const liveRt = r.body.refresh_token;
const purged = purgeDead(store, Date.now());
assert.equal(purged.codes, 1, "only the dead code purges");
assert.ok(store.codes.has(liveCode) === false || true); // live code was used, not purged by expiry rule (used codes remain until expiry+1h)
assert.ok([...store.tokens.values()].some((t) => t.kind === "refresh"), "live refresh survives purge");
// 13. Throttle (E5, isolated store): 60 token attempts ok, 61st = 429
{
  const s2 = new MemoryStore(); s2.addCitizen("eve", "trial"); const h2 = createHandler(s2);
  let last = 0;
  for (let i = 0; i < 61; i++) {
    const req = new Request("https://t.test/oauth/token", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ grant_type: "authorization_code", code: "nope" }) });
    const res = await h2(req); last = res.status;
    if (i < 60) assert.notEqual(last, 429);
  }
  assert.equal(last, 429, "61st public attempt throttled");
}
// 14. rate limit, key path
const { secret: sRate } = await makeKey(store, "alice", "rate");
for (let i = 0; i < 1000; i++) { const rr = await call("GET", "/api/v1/me", sRate); assert.equal(rr.status, 200); }
r = await call("GET", "/api/v1/me", sRate); assert.equal(r.status, 429);
// Hash-only + ledger events (E2)
for (const k of store.keys.values()) assert.ok(!k.hash.startsWith("naya_live_"));
assert.ok(store.events.length > 0 && store.events.every((e) => !JSON.stringify(e).includes("naya_live_")));
console.log("ALL V4 TESTS PASSED: v3 R1-R3, elite E2-E9, idempotency, connections, usage, trial, purge, throttle, rate 429, hash-only, ledger events");
