import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { stripTypeScriptTypes } from "node:module";
import { test } from "node:test";
import vm from "node:vm";

// Firing proofs for nayanet-github-dispatch.
//
// This is the highest-blast-radius surface left. It is the only remaining function that
// causes an EXTERNAL, VISIBLE, HARD-TO-REVERSE effect: it commits to main on GitHub.
// Every guard below is loaded into a VM sandbox with stubbed Deno / supabase / GitHub, so
// the real request path executes offline. Nothing here greps source.
//
// The point of closing these in order: `EXPLICIT_APPROVAL_REQUIRED` is the last gate
// before an irreversible public write, and until now nothing had ever watched it fire.

const source = readFileSync(
  new URL("../supabase/functions/nayanet-github-dispatch/index.ts", import.meta.url),
  "utf8"
);
const code = stripTypeScriptTypes(source.replace(/^import .*;\r?\n/gm, ""));

const USER = "11111111-1111-4111-8111-111111111111";
const OTHER = "22222222-2222-4222-8222-222222222222";
const TX = "aaaaaaaa-1111-4111-8111-111111111111";
const GRANT = "grant-1";
const IB = "IB-000123";

const validBody = {
  operation: "project_smart_note",
  transaction_id: TX,
  authority_grant_id: GRANT,
  approval: "EXPLICIT_APPROVAL_GRANTED",
  idempotency_key: "idem-1",
};

const validGrant = {
  grant_id: GRANT,
  status: "ACTIVE",
  expires_at: null,
  actions: ["smart_note_github_projection"],
  scope: { target: TX },
  issuer_id: USER,
  subject_id: USER,
};

const validTx = {
  id: TX,
  user_id: USER,
  created_at: "2026-10-06T00:00:00Z",
  intelligent_block: {
    identity: { intelligent_block_id: IB },
    metadata: { projection_category: "system", projection_topic: "smart-note" },
    content: { lesson: "hello" },
  },
};

/**
 * Drive the real handler with stubbed externals.
 *
 * `failAt` selects which GitHub call fails, so the post-write guards can be reached.
 * `commitShaSeen` controls what the read-back returns, which is how PROJECTION_UNVERIFIED
 * is provoked.
 */
function runtime({
  user = { id: USER },
  body = validBody,
  grant = validGrant,
  tx = validTx,
  credentialError = null,
  headStatus = 404,
  putOk = true,
  putBody = { content: { sha: "commit-1" } },
  verifySha = "commit-1",
  claims = null,
} = {}) {
  let handler;
  const githubCalls = [];

  const receipts = {
    inserted: [],
    updated: [],
    selectResult: claims,
    insert(row) {
      receipts.inserted.push(row);
      // A pre-existing completed claim must be returned by the INSERT for the replay
      // branch to be reachable. Returning a fresh "processing" row always made
      // `replayed` undefined and the idempotency guarantee untestable.
      const existing = receipts.selectResult ?? { id: "receipt-1", status: "processing" };
      const chain = {
        select() { return chain; },
        maybeSingle: async () => ({ data: existing, error: null }),
      };
      return chain;
    },
    update(row) {
      receipts.updated.push(row);
      const chain = {
        eq() { return chain; },
        // The final completion write is .update().eq().select().single(). Getting the
        // chain shape wrong twice in a row is the lesson here: a stub that is merely
        // close produces a 500 and looks like a product defect.
        select() { return chain; },
        single: async () => ({ data: { id: "receipt-1" }, error: null }),
        maybeSingle: async () => ({ data: { id: "receipt-1" }, error: null }),
        then: async (r) => r({ data: null, error: null }),
      };
      return chain;
    },
    select() {
      const chain = {
        eq() { return chain; },
        maybeSingle: async () => ({ data: receipts.selectResult, error: null }),
      };
      return chain;
    },
  };

  const userClient = {
    auth: {
      getUser: async () => (user ? { data: { user }, error: null } : { data: { user: null }, error: {} }),
    },
    from(table) {
      if (table === "nayanet_authority_grants") {
        const chain = {
          select() { return chain; },
          eq() { return chain; },
          maybeSingle: async () => ({ data: grant, error: null }),
        };
        return chain;
      }
      if (table === "v7_smart_note_transactions") {
        const chain = {
          select() { return chain; },
          eq() { return chain; },
          maybeSingle: async () => ({ data: tx, error: null }),
        };
        return chain;
      }
      return receipts;
    },
  };

  // PRODUCTION REPAIR (2026-10-07): the transaction row is read through the
  // service-role client (the user-scoped read is invisible under the live RLS
  // contract), so the admin mock serves the tx table the same as the user mock.
  const adminClient = {
    from(table) {
      if (table === "v7_smart_note_transactions") {
        const chain = {
          select() { return chain; },
          eq() { return chain; },
          maybeSingle: async () => ({ data: tx, error: null }),
        };
        return chain;
      }
      return receipts;
    },
  };

  const fetchStub = async (url, opts = {}) => {
    const method = opts.method ?? "GET";
    githubCalls.push({ url: String(url), method });
    if (String(url).includes("contents/")) {
      if (method === "GET") {
        // The handler GETs twice: once to read the existing blob head, once to verify the
        // commit it just made. A stateless stub returning 404 for both made the verify read
        // fail on the HAPPY path. Track committed state so the second GET reflects reality.
        if (receipts.committed || headStatus === 200) {
          return { ok: true, status: 200, json: async () => ({ sha: verifySha }) };
        }
        return { ok: false, status: headStatus, json: async () => ({}) };
      }
      if (method === "PUT") {
        receipts.committed = true;
        return { ok: putOk, status: putOk ? 201 : 422, json: async () => putBody };
      }
    }
    return { ok: true, status: 200, json: async () => ({}) };
  };

  // The handler calls resolveGitHubCredential(); stub at the crypto boundary so the
  // credential guard is reachable without configuring anything.
  const SignJWT = async () => "jwt";
  const importPKCS8 = async () => "key";

  vm.runInNewContext(code, {
    URL, Request, Response, console, Date, TextEncoder, TextDecoder, Uint8Array, crypto,
    atob, btoa,
    fetch: fetchStub,
    Deno: {
      env: {
        // Every key the handler reads must be answered explicitly. An earlier draft
        // returned `credentialError` for unknown keys, which made resolveGitHubCredential
        // fail on the HAPPY path too and masked the four post-write guards behind a
        // credential error. A stub that lies about the environment lies about the system.
        get: (k) =>
          ({
            SUPABASE_URL: "https://offline.invalid",
            SUPABASE_ANON_KEY: "anon",
            SUPABASE_SERVICE_ROLE_KEY: "service",
            GITHUB_TOKEN: credentialError === "GITHUB_CREDENTIAL_NOT_CONFIGURED" ? "" : "ghs_test",
          })[k] ?? "",
      },
      serve: (cb) => { handler = cb; },
    },
    createClient: (url, key) => (key === "service" ? adminClient : userClient),
    createRemoteJWKSet: () => ({}),
    jwtVerify: async () => ({ payload: { repository: "SoulSchoolAcademy/NayaPOWER" } }),
    SignJWT,
    importPKCS8,
  });

  return {
    githubCalls,
    receipts,
    invoke: (overrideBody = body, headers = {}, method = "POST") =>
      handler(new Request("https://offline.invalid", {
        method,
        headers: { "content-type": "application/json", authorization: "Bearer t", ...headers },
        body: method === "GET" || method === "HEAD" ? undefined : JSON.stringify(overrideBody ?? {}),
      })),
  };
}

// ── The last gate before an irreversible public write ──────────────────────────

test("GUARD -- EXPLICIT_APPROVAL_REQUIRED fires without explicit approval", async () => {
  const rt = runtime();
  const res = await rt.invoke({ ...validBody, approval: undefined });
  assert.equal(res.status, 403);
  assert.equal((await res.json()).error, "EXPLICIT_APPROVAL_REQUIRED");
  assert.equal(rt.githubCalls.length, 0, "no GitHub call may happen before approval");
  assert.equal(rt.receipts.inserted.length, 0, "no receipt claim may happen before approval");
});

test("GUARD -- approval must be the exact token, not merely present", async () => {
  for (const approval of ["yes", "approved", "EXPLICIT_APPROVAL", "explicit_approval_granted", "true"]) {
    const rt = runtime();
    const res = await rt.invoke({ ...validBody, approval });
    assert.equal(res.status, 403, `approval="${approval}" must not pass`);
    assert.equal((await res.json()).error, "EXPLICIT_APPROVAL_REQUIRED");
    assert.equal(rt.githubCalls.length, 0);
  }
});

test("GUARD -- AUTHORITY_GRANT_REQUIRED fires when no grant is presented", async () => {
  const rt = runtime();
  const res = await rt.invoke({ ...validBody, authority_grant_id: undefined });
  assert.equal(res.status, 400);
  assert.equal((await res.json()).error, "AUTHORITY_GRANT_REQUIRED");
  assert.equal(rt.githubCalls.length, 0);
});

test("GUARD -- PROJECTION_AUTHORITY_REFUSED fires for an inactive grant", async () => {
  const rt = runtime({ grant: { ...validGrant, status: "REVOKED" } });
  const res = await rt.invoke();
  assert.equal(res.status, 403);
  const body = await res.json();
  assert.equal(body.error, "PROJECTION_AUTHORITY_REFUSED");
  assert.equal(rt.githubCalls.length, 0);
});

test("GUARD -- PROJECTION_AUTHORITY_REFUSED fires for a cross-owner grant", async () => {
  // The single most consequential guard here: someone else's grant must never authorize
  // a write to this owner's repo.
  const rt = runtime({ grant: { ...validGrant, subject_id: OTHER } });
  const res = await rt.invoke();
  assert.equal(res.status, 403);
  assert.equal((await res.json()).error, "PROJECTION_AUTHORITY_REFUSED");
  assert.equal(rt.githubCalls.length, 0);
});

test("GUARD -- PROJECTION_AUTHORITY_REFUSED fires when the grant scope is another transaction", async () => {
  // Grant scope is per-transaction. A live, owned grant aimed elsewhere must not write.
  const rt = runtime({ grant: { ...validGrant, scope: { target: "some-other-transaction" } } });
  const res = await rt.invoke();
  assert.equal(res.status, 403);
  assert.equal((await res.json()).error, "PROJECTION_AUTHORITY_REFUSED");
  assert.equal(rt.githubCalls.length, 0);
});

test("GUARD -- PROJECTION_AUTHORITY_REFUSED fires for an expired grant", async () => {
  const rt = runtime({ grant: { ...validGrant, expires_at: "2020-01-01T00:00:00Z" } });
  const res = await rt.invoke();
  assert.equal(res.status, 403);
  assert.equal((await res.json()).error, "PROJECTION_AUTHORITY_REFUSED");
  assert.equal(rt.githubCalls.length, 0);
});

test("GUARD -- PROJECTION_AUTHORITY_REFUSED fires when the grant omits the projection action", async () => {
  const rt = runtime({ grant: { ...validGrant, actions: ["read_only"] } });
  const res = await rt.invoke();
  assert.equal(res.status, 403);
  assert.equal((await res.json()).error, "PROJECTION_AUTHORITY_REFUSED");
  assert.equal(rt.githubCalls.length, 0);
});

// ── Transaction ownership ────────────────────────────────────────────────────

test("GUARD -- TRANSACTION_NOT_FOUND fires for another owner's transaction", async () => {
  const rt = runtime({ tx: { ...validTx, user_id: OTHER } });
  const res = await rt.invoke();
  assert.equal(res.status, 404);
  assert.equal((await res.json()).error, "TRANSACTION_NOT_FOUND");
  assert.equal(rt.githubCalls.length, 0);
});

test("GUARD -- INTELLIGENT_BLOCK_ID_INVALID fires for a malformed block identity", async () => {
  // The smart-link contract requires /IB-\d{6}/. A malformed id would produce a link
  // that looks plausible and is not in the canonical tree.
  for (const bad of ["not-an-ib", "IB-123", "IB-0001234", "IB-00012X", ""]) {
    const rt = runtime({
      tx: { ...validTx, intelligent_block: { ...validTx.intelligent_block, identity: { intelligent_block_id: bad } } },
    });
    const res = await rt.invoke();
    assert.ok(res.status >= 400, `id="${bad}" must be refused, got ${res.status}`);
    assert.equal((await res.json()).error, "INTELLIGENT_BLOCK_ID_INVALID", `id="${bad}"`);
    assert.equal(rt.githubCalls.length, 0, `id="${bad}" reached GitHub`);
  }
});

// ── Request preconditions ────────────────────────────────────────────────────

test("GUARD -- UNKNOWN_OPERATION fires for any other operation", async () => {
  for (const operation of ["delete_smart_note", "force_push", "", "PROJECT_SMART_NOTE"]) {
    const rt = runtime();
    const res = await rt.invoke({ ...validBody, operation });
    assert.equal(res.status, 400, `operation="${operation}"`);
    assert.equal((await res.json()).error, "UNKNOWN_OPERATION");
    assert.equal(rt.githubCalls.length, 0);
  }
});

test("GUARD -- TRANSACTION_ID_REQUIRED fires without a transaction", async () => {
  const rt = runtime();
  const res = await rt.invoke({ ...validBody, transaction_id: undefined });
  assert.equal(res.status, 400);
  assert.equal((await res.json()).error, "TRANSACTION_ID_REQUIRED");
});

test("GUARD -- IDEMPOTENCY_KEY_REQUIRED fires without a key", async () => {
  // Idempotency is what makes a replay safe. Without it, a retry is a duplicate commit.
  const rt = runtime();
  const res = await rt.invoke({ ...validBody, idempotency_key: undefined });
  assert.equal(res.status, 400);
  assert.equal((await res.json()).error, "IDEMPOTENCY_KEY_REQUIRED");
  assert.equal(rt.githubCalls.length, 0);
});

test("GUARD -- IDEMPOTENCY_KEY_REQUIRED fires when only a blank key is supplied", async () => {
  const rt = runtime();
  const res = await rt.invoke({ ...validBody, idempotency_key: "   " });
  assert.equal(res.status, 400);
  assert.equal((await res.json()).error, "IDEMPOTENCY_KEY_REQUIRED");
});

// ── Authentication ───────────────────────────────────────────────────────────

test("GUARD -- AUTHORIZATION_REQUIRED fires with no Authorization header", async () => {
  const rt = runtime();
  const res = await rt.invoke(validBody, { authorization: "" });
  assert.equal(res.status, 401);
  assert.equal((await res.json()).error, "AUTHORIZATION_REQUIRED");
});

test("GUARD -- AUTHENTICATED_USER_REQUIRED fires for a token with no resolved user", async () => {
  const rt = runtime({ user: null });
  const res = await rt.invoke();
  assert.equal(res.status, 401);
  assert.equal((await res.json()).error, "AUTHENTICATED_USER_REQUIRED");
  assert.equal(rt.githubCalls.length, 0);
});

test("GUARD -- METHOD_NOT_ALLOWED fires for a non-POST request", async () => {
  const rt = runtime();
  const res = await rt.invoke(validBody, {}, "GET");
  assert.equal(res.status, 405);
  assert.equal((await res.json()).error, "METHOD_NOT_ALLOWED");
});

// ── Post-write guards. Reaching these requires passing every gate above. ──────

test("GUARD -- GITHUB_CREDENTIAL_NOT_CONFIGURED blocks rather than guessing a link", async () => {
  // SN-0465/SN-0466: an absent credential must never produce a fabricated smart link.
  const rt = runtime({ credentialError: "GITHUB_CREDENTIAL_NOT_CONFIGURED" });
  const res = await rt.invoke();
  const body = await res.json();
  assert.equal(body.ok, false);
  assert.equal(body.pipeline, "PROJECTION_BLOCKED");
  assert.equal(body.error, "GITHUB_CREDENTIAL_NOT_CONFIGURED");
  assert.equal(body.smart_link, undefined, "a blocked projection must not report a link");
});

test("GUARD -- GITHUB_READ_FAILED fires on a non-404, non-200 read", async () => {
  const rt = runtime({ headStatus: 500 });
  const res = await rt.invoke();
  const body = await res.json();
  assert.equal(body.error, "GITHUB_READ_FAILED");
  assert.equal(body.status, 500);
});

test("GUARD -- GITHUB_COMMIT_FAILED fires when the PUT yields no commit sha", async () => {
  // A 2xx with no sha is still a failure. Trusting the status alone would report a
  // projection that never happened.
  const rt = runtime({ putOk: true, putBody: { message: "ok but no sha" } });
  const res = await rt.invoke();
  const body = await res.json();
  assert.equal(body.error, "GITHUB_COMMIT_FAILED");
  assert.equal(body.smart_link, undefined, "a failed commit must not report a link");
});

test("GUARD -- PROJECTION_UNVERIFIED fires when read-back does not match the commit", async () => {
  // SN-0477: the deploy stamp is not the proof. This reads the blob back and compares.
  const rt = runtime({ verifySha: "a-different-sha" });
  const res = await rt.invoke();
  const body = await res.json();
  assert.equal(body.error, "PROJECTION_UNVERIFIED");
  assert.equal(body.pipeline, "PROJECTION_FAILED");
});

// ── Positive control. Without this the suite could pass by refusing everything. ──

test("CONTROL -- a fully authorized request commits and returns a verified link", async () => {
  const rt = runtime();
  const res = await rt.invoke();
  const body = await res.json();
  assert.equal(res.status, 200, JSON.stringify(body));
  assert.equal(body.ok, true);
  assert.equal(body.pipeline, "PROJECTION_VERIFIED");
  assert.match(body.smart_link, /^https:\/\/github\.com\/SoulSchoolAcademy\/NayaPOWER\/blob\/main\/.+\/IB-000123\/smart-note\.md$/);
  assert.equal(body.projection_verification.commit_sha, "commit-1");
  assert.equal(rt.githubCalls.some((c) => c.method === "PUT"), true, "a real commit must have been attempted");
});

test("CONTROL -- a completed claim replays without a duplicate commit", async () => {
  // The idempotency guarantee, executed: same key, already completed -> no PUT.
  const rt = runtime({
    claims: { id: "receipt-1", status: "completed", smart_link: "https://github.com/x/IB-000123/smart-note.md", commit_sha: "commit-0", completed_at: "2026-10-06T00:00:00Z" },
  });
  const res = await rt.invoke();
  const body = await res.json();
  assert.equal(body.ok, true);
  assert.equal(body.replayed, true);
  assert.equal(rt.githubCalls.some((c) => c.method === "PUT"), false, "a replay must not commit again");
});
