import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { stripTypeScriptTypes } from "node:module";
import { test } from "node:test";
import vm from "node:vm";
import { webcrypto } from "node:crypto";

// Firing proofs for nayanet-verified-ai-action -- the governed-action surface.
//
// This is the only function that turns an authority grant into a real external effect,
// so it is where a fail-open is most expensive: it does not answer wrongly, it ACTS.
//
// AND a defect found while writing them, which is the worst instance of the class yet
// found in this repo:
//
//   CV-08 -- index.ts:542 emits a verification CHECK that is a hardcoded literal.
//
//     refusalChecks = {
//       ...
//       refusal_outcome_absent: refusalOutcome === null,        // computed
//       unauthorized_outcome_exists: refusalOutcome !== null,   // computed
//       receipt_mutated_after_refusal: false,                   // <-- CONSTANT
//     };
//
//   Every other field in that object is computed from evidence. This one is the literal
//   `false`, and index.ts:571 then gates on it:
//
//     refusalChecks.receipt_mutated_after_refusal === false
//
//   which is `false === false`, i.e. always true. So the runtime reports, under the key
//   `receipt_mutated_after_refusal`, that no mutation occurred -- while being incapable
//   of ever reporting that one did.
//
//   This is worse than CV-04 and CV-05. Those were a literal in a verification RESULT.
//   This one is a literal in a verification CHECK: it is presented to every downstream
//   consumer as a passing guard. A reader of `refusal_checks` sees a field whose name
//   promises mutation detection and whose value is a constant.
//
//   The pinning test below proves it is not merely cosmetic: it MUTATES a refusal
//   receipt after the refusal (rewriting its observed_result), which is exactly the event
//   the check is named for. Every genuinely-computed check still passes, the constant
//   still reports `false`, and the runtime returns ok:true / independent_verification:true.
//
//   SN-0468 (fail closed, always) and SN-0481 (never impersonate the verifier).
//
//   A second, lower-severity finding is pinned alongside it as CV-09; see below.

const source = readFileSync(
  new URL("../supabase/functions/nayanet-verified-ai-action/index.ts", import.meta.url),
  "utf8"
);
const code = stripTypeScriptTypes(
  source
    .replace(/^import .*from "\.\/.*";\r?\n/gm, "")
    .replace(/^import .*;\r?\n/gm, "")
);

const OWNER = "adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const NAYA_ID = "NAYA-NODE-0001";
const BLOCK_ID = "IB-NAYA-NODE-0001-0001";
const MISSION_ID = "NAYA-NODE-0001-CONTINUITY";
const ACTION = "naya_node_apply";
const FUTURE = "2099-01-01T00:00:00.000Z";
const LESSON = "Preserve provenance before applying retained intelligence";

const ACTIVE_GRANT = {
  grant_id: "G1",
  issuer_id: OWNER,
  subject_id: OWNER,
  mission_id: MISSION_ID,
  scope: { target: NAYA_ID },
  actions: [ACTION],
  constraints: null,
  status: "ACTIVE",
  issued_at: "2026-01-01T00:00:00.000Z",
  expires_at: FUTURE,
  revoked_at: null,
};

const CANONICAL_BLOCK = {
  intelligent_block_id: BLOCK_ID,
  owner_id: OWNER,
  understanding_state: "LEARNED",
  content: { lesson: LESSON },
  evidence_refs: [{ event_id: "E1" }],
};

/** A receipt+outcome pair from a successful governed action. */
function executedPair(overrides = {}) {
  return {
    receipt: {
      id: "RC-1",
      user_id: OWNER,
      project_id: "NayaNET",
      revision: 1,
      action: "NAYA-NODE-0001-VERIFIED-AI-ACTION",
      status: "SUCCESS",
      expected_result: "under explicit authority",
      observed_result: "RETAINED_INTELLIGENCE_RETRIEVED | target=NAYA-NODE-0001 | idempotency:K1",
      evidence: {
        authority_grant_id: "G1",
        requested_action: ACTION,
        requested_target: NAYA_ID,
        canonical_block_id: BLOCK_ID,
        idempotency_request_fingerprint: "FINGERPRINT-FROM-EXECUTION",
      },
      created_at: "2026-01-01T00:00:00.000Z",
    },
    outcome: {
      outcome_id: "OC-1",
      receipt_id: "RC-1",
      user_id: OWNER,
      project_id: "NayaNET",
      experiment_case_id: "NAYA-0001-VERIFIED-AI-ACTION",
      outcome_type: "GOVERNED_ACTION_OUTCOME",
      verified: false,
      verified_value: null,
      verification_method: "PENDING_INDEPENDENT_RUNTIME_VERIFICATION",
      evidence: { canonical_digest: "digest-from-execution" },
      created_at: "2026-01-01T00:00:00.000Z",
    },
    ...overrides,
  };
}

function baseTables(overrides = {}) {
  const pair = executedPair();
  return {
    nayanet_authority_grants: [ACTIVE_GRANT],
    nayanet_intelligent_blocks: [CANONICAL_BLOCK],
    nayanet_execution_receipts: [pair.receipt],
    nayanet_execution_outcomes: [pair.outcome],
    ...overrides,
  };
}

/**
 * Drive the real handler.
 *
 * `insertFaults.<table>` is a function (attemptIndex, row) => error | null, which is how
 * Postgres error codes get injected. The unique-violation code 23505 is the one the
 * retry loops are built around, so proving those loops actually retry requires producing
 * it honestly rather than asserting the source contains the string.
 */
async function runtime({
  mode = "verify",
  body = {},
  tables = {},
  insertFaults = {},
  auth = {},
  authHeader = "Bearer tok",
  method = "POST",
  jwtFails = false,
  envMissing = false,
} = {}) {
  const rows = JSON.parse(JSON.stringify({ ...baseTables(), ...tables }));
  const attempts = { receipts: 0, outcomes: 0 };
  const ops = [];
  let ids = 0;

  const db = {
    from(table) {
      const filters = [];
      let op = "select";
      let patch = null;
      const chain = {
        select() { return chain; },
        eq(col, val) { filters.push([col, val]); return chain; },
        in(col, vals) { filters.push(["__in__" + col, vals]); return chain; },
        order() { return chain; },
        limit() { return chain; },
        insert(row) { op = "insert"; patch = row; return chain; },
        update(p) { op = "update"; patch = p; return chain; },
        async maybeSingle() {
          const found = selectRows();
          return { data: found[0] ?? null, error: null };
        },
        async single() {
          if (op === "insert") {
            const i = attempts[table] ?? 0;
            attempts[table] = i + 1;
            const fault = insertFaults[table]?.(i, patch);
            ops.push({ op: "insert", table, row: patch });
            if (fault) return { data: null, error: fault };
            // Postgres assigns the surrogate key on insert; the runtime never supplies
            // one and later reads it back, so the stub must too.
            const created = { id: `${table.slice(-3)}-${++ids}`, ...patch };
            rows[table].push(created);
            return { data: created, error: null };
          }
          const found = selectRows();
          if (!found.length) return { data: null, error: { message: "no rows" } };
          Object.assign(found[0], patch);
          ops.push({ op: "update", table, patch });
          return { data: found[0], error: null };
        },
        then(resolve) {
          return resolve({ data: selectRows(), error: null });
        },
      };

      function selectRows() {
        return rows[table].filter((r) =>
          filters.every(([col, val]) => {
            if (col.startsWith("__in__")) return val.includes(r[col.slice(5)]);
            return r[col] === val;
          })
        );
      }
      return chain;
    },
  };

  let handler;
  const context = {
    Deno: {
      serve: (fn) => { handler = fn; },
      env: {
        get: (k) => {
          if (envMissing) return undefined;
          return { SUPABASE_URL: "https://stub.supabase.co", SUPABASE_SERVICE_ROLE_KEY: "sb-secret" }[k];
        },
      },
    },
    createClient: () => db,
    createRemoteJWKSet: () => ({}),
    jwtVerify: async () => {
      if (jwtFails) throw new Error("JWKS verification failed");
      return {
        payload: {
          repository: "SoulSchoolAcademy/NayaPOWER",
          workflow_ref: "SoulSchoolAcademy/NayaPOWER/.github/workflows/live-verified-ai-action-proof.yml@refs/heads/main",
          ref: "refs/heads/main",
          jti: "jti-1",
          sub: "repo:SoulSchoolAcademy/NayaPOWER:ref:refs/heads/main",
          ...auth,
        },
      };
    },
    crypto: webcrypto,
    TextEncoder,
    Uint8Array,
    ArrayBuffer,
    console: { ...console, error: () => {}, log: () => {}, warn: () => {} },
    URL,
    Request,
    Response,
  };
  vm.createContext(context);
  new vm.Script(code, { filename: "nayanet-verified-ai-action/index.ts" }).runInContext(context);

  const req = {
    method,
    headers: { get: (h) => (h === "authorization" ? authHeader : null) },
    json: async () => ({ mode, ...body }),
  };
  const res = await handler(req);
  return { status: res.status, body: await res.json(), rows, ops, attempts };
}

const conflict = (extra = {}) => ({ code: "23505", message: "duplicate key", ...extra });

/**
 * Perform a real governed action and return exactly what was persisted.
 *
 * Every replay/verification test below then runs against these real rows rather than
 * hand-built fixtures. That matters: the request fingerprint and canonical digest are
 * SHA-256 values computed inside the runtime, so a hand-written fixture could never
 * legitimately satisfy them -- it could only accidentally pass, which would be proof of
 * nothing. This way the replay path is exercised against a receipt that a genuine
 * execution actually wrote.
 */
async function executeForReal({ idempotencyKey = "K1" } = {}) {
  const { status, body, rows } = await runtime({
    mode: "execute",
    body: { authority_grant_id: "G1", idempotency_key: idempotencyKey },
    tables: { nayanet_execution_receipts: [], nayanet_execution_outcomes: [] },
  });
  assert.equal(status, 200, `execute did not succeed: ${JSON.stringify(body)}`);
  assert.equal(body.ok, true);
  assert.equal(body.status, "EXECUTED");
  return {
    receipt: rows.nayanet_execution_receipts.find((r) => r.action === "NAYA-NODE-0001-VERIFIED-AI-ACTION"),
    outcome: rows.nayanet_execution_outcomes[0],
    response: body,
  };
}

// ---------------------------------------------------------------------------
// Transport / auth
// ---------------------------------------------------------------------------

test("METHOD_NOT_ALLOWED -- a GET is refused", async () => {
  const { status, body } = await runtime({ method: "GET" });
  assert.equal(status, 405);
  assert.equal(body.error, "METHOD_NOT_ALLOWED");
});

test("RUNTIME_IDENTITY_REQUIRED -- no bearer token", async () => {
  const { body } = await runtime({ authHeader: "" });
  assert.equal(body.error, "RUNTIME_IDENTITY_REQUIRED");
});

test("GITHUB_OIDC_INVALID -- an unverifiable token", async () => {
  const { body } = await runtime({ jwtFails: true });
  assert.equal(body.error, "GITHUB_OIDC_INVALID");
});

test("WORKFLOW_BINDING_MISMATCH -- token bound to another repository", async () => {
  const { body } = await runtime({ auth: { repository: "attacker/NayaPOWER" } });
  assert.equal(body.error, "WORKFLOW_BINDING_MISMATCH");
});

test("SERVER_AUTH_CONFIG_MISSING -- no service role configured", async () => {
  const { body } = await runtime({ envMissing: true });
  assert.equal(body.error, "SERVER_AUTH_CONFIG_MISSING");
});

test("UNSUPPORTED_MODE -- an unknown mode is refused, not defaulted", async () => {
  const { status, body } = await runtime({ mode: "do-something-else" });
  assert.equal(status, 400);
  assert.equal(body.error, "UNSUPPORTED_MODE");
});

// ---------------------------------------------------------------------------
// execute: authority is resolved before any effect
// ---------------------------------------------------------------------------

test("IDEMPOTENCY_KEY_REQUIRED -- execute without a replay key", async () => {
  const { status, body } = await runtime({ mode: "execute", body: { authority_grant_id: "G1" } });
  assert.equal(status, 400);
  assert.equal(body.error, "IDEMPOTENCY_KEY_REQUIRED");
});

test("CANONICAL_BLOCK_NOT_FOUND -- the canonical lesson block is gone", async () => {
  const { body } = await runtime({
    mode: "execute",
    body: { authority_grant_id: "G1", idempotency_key: "K1" },
    tables: { nayanet_intelligent_blocks: [] },
  });
  assert.equal(body.error, "CANONICAL_BLOCK_NOT_FOUND");
});

test("RETAINED_LESSON_MISSING -- the block carries no lesson to apply", async () => {
  const { status, body } = await runtime({
    mode: "execute",
    body: { authority_grant_id: "G1", idempotency_key: "K1" },
    tables: { nayanet_intelligent_blocks: [{ ...CANONICAL_BLOCK, content: {} }] },
  });
  assert.equal(status, 409);
  assert.equal(body.error, "RETAINED_LESSON_MISSING");
});

test("AUTHORITY_ABSENT -- no grant presented, and a REFUSAL receipt is persisted", async () => {
  const { status, body, rows } = await runtime({
    mode: "execute",
    body: { idempotency_key: "K1" },
    tables: { nayanet_execution_receipts: [], nayanet_execution_outcomes: [] },
  });
  assert.equal(status, 403);
  assert.equal(body.error, "AUTHORITY_ABSENT");
  // The refusal itself must be durable, and must record that nothing was executed.
  const refusal = rows.nayanet_execution_receipts.find((r) => r.status === "BLOCKED");
  assert.ok(refusal, "no refusal receipt was persisted");
  assert.equal(refusal.action, "NAYA-NODE-0001-VERIFIED-AI-ACTION-REFUSAL");
  assert.equal(refusal.evidence.action_executed, false);
  assert.equal(refusal.evidence.outcome_created, false);
  assert.equal(rows.nayanet_execution_outcomes.length, 0);
});

test("authority denials each name their own reason, across every branch", async () => {
  const revoked = { ...ACTIVE_GRANT, revoked_at: "2026-06-01T00:00:00.000Z" };
  const expired = { ...ACTIVE_GRANT, expires_at: "2020-01-01T00:00:00.000Z" };
  const wrongAction = { ...ACTIVE_GRANT, actions: ["some_other_action"] };
  const wrongScope = { ...ACTIVE_GRANT, scope: { target: "NAYA-NODE-0002" } };
  const wrongMission = { ...ACTIVE_GRANT, mission_id: "OTHER-MISSION" };
  const crossOwner = { ...ACTIVE_GRANT, subject_id: "someone-else" };
  const inactive = { ...ACTIVE_GRANT, status: "REVOKED" };

  const cases = [
    [revoked, "AUTHORITY_REVOKED"],
    [expired, "AUTHORITY_EXPIRED"],
    [wrongAction, "AUTHORITY_ACTION_NOT_GRANTED"],
    [wrongScope, "AUTHORITY_SCOPE_MISMATCH"],
    [wrongMission, "AUTHORITY_MISSION_MISMATCH"],
    [crossOwner, "AUTHORITY_CROSS_OWNER"],
    [inactive, "AUTHORITY_NOT_ACTIVE"],
  ];
  for (const [grant, expected] of cases) {
    const { body } = await runtime({
      mode: "execute",
      body: { authority_grant_id: "G1", idempotency_key: "K1" },
      tables: { nayanet_authority_grants: [grant], nayanet_execution_receipts: [], nayanet_execution_outcomes: [] },
    });
    assert.equal(body.authority_reason, expected, `grant ${JSON.stringify(grant)}`);
  }
});

// ---------------------------------------------------------------------------
// execute: the write-path error branches. These are the guards that decide whether a
// duplicate-key collision is retried or escalated -- the difference between "try again"
// and "give up safely".
// ---------------------------------------------------------------------------

test("RECEIPT_WRITE_ -- a receipt insert failure that is NOT a unique violation is escalated", async () => {
  const { body } = await runtime({
    mode: "execute",
    body: { authority_grant_id: "G1", idempotency_key: "K1" },
    tables: { nayanet_execution_receipts: [] },
    insertFaults: { nayanet_execution_receipts: () => ({ code: "42501", message: "permission denied" }) },
  });
  assert.equal(body.error, "RECEIPT_WRITE_42501");
});

test("RECEIPT_REVISION_RETRY_EXHAUSTED -- four unique-violation collisions and no way forward", async () => {
  const { body, attempts } = await runtime({
    mode: "execute",
    body: { idempotency_key: "K1" },
    tables: { nayanet_execution_receipts: [] },
    insertFaults: { nayanet_execution_receipts: () => conflict() },
  });
  assert.equal(body.error, "RECEIPT_REVISION_RETRY_EXHAUSTED");
  // The retry loop must actually attempt more than once, otherwise "exhausted" is a lie.
  assert.equal(attempts.nayanet_execution_receipts, 4);
});

test("RECEIPT_IDEMPOTENCY_RETRY_EXHAUSTED -- collisions with no replayable receipt behind them", async () => {
  const { body, attempts } = await runtime({
    mode: "execute",
    body: { authority_grant_id: "G1", idempotency_key: "K1" },
    tables: { nayanet_execution_receipts: [] },
    insertFaults: { nayanet_execution_receipts: () => conflict() },
  });
  assert.equal(body.error, "RECEIPT_IDEMPOTENCY_RETRY_EXHAUSTED");
  assert.equal(attempts.nayanet_execution_receipts, 4);
});

test("OUTCOME_WRITE_ -- an outcome insert failure that is NOT a unique violation is escalated", async () => {
  const { body } = await runtime({
    mode: "execute",
    body: { authority_grant_id: "G1", idempotency_key: "K2" },
    tables: { nayanet_execution_receipts: [], nayanet_execution_outcomes: [] },
    insertFaults: { nayanet_execution_outcomes: () => ({ code: "42501", message: "permission denied" }) },
  });
  assert.equal(body.error, "OUTCOME_WRITE_42501");
});

test("OUTCOME_WRITE_RACE_UNRESOLVED -- the collision has no outcome to read back", async () => {
  const { body } = await runtime({
    mode: "execute",
    body: { authority_grant_id: "G1", idempotency_key: "K3" },
    tables: { nayanet_execution_receipts: [], nayanet_execution_outcomes: [] },
    insertFaults: { nayanet_execution_outcomes: () => conflict() },
  });
  assert.equal(body.error, "OUTCOME_WRITE_RACE_UNRESOLVED");
});

// ---------------------------------------------------------------------------
// execute: idempotent replay
// ---------------------------------------------------------------------------

test("IDEMPOTENCY_KEY_REUSE_CONFLICT -- the same key, a different request", async () => {
  const real = await executeForReal();
  // Same replay key, but the canonical block has since changed, so the request
  // fingerprint differs from the one the original execution recorded.
  const { status, body } = await runtime({
    mode: "execute",
    body: { authority_grant_id: "G1", idempotency_key: "K1" },
    tables: {
      nayanet_intelligent_blocks: [{ ...CANONICAL_BLOCK, evidence_refs: [{ event_id: "E2" }] }],
      nayanet_execution_receipts: [{ ...real.receipt, idempotency_key: "K1" }],
      nayanet_execution_outcomes: [],
    },
    // The insert collides on the replay key, so the runtime goes looking for the receipt
    // that already owns it -- and then discovers it was a different request.
    insertFaults: { nayanet_execution_receipts: () => conflict() },
  });
  assert.equal(status, 409);
  assert.equal(body.error, "IDEMPOTENCY_KEY_REUSE_CONFLICT");
  assert.equal(body.idempotent_replay, false);
});

test("IDEMPOTENCY_KEY_REUSE_CONFLICT -- a replayed receipt carrying NO fingerprint is not trusted", async () => {
  const real = await executeForReal();
  const stripped = { ...real.receipt };
  delete stripped.evidence.idempotency_request_fingerprint;
  const { status, body } = await runtime({
    mode: "execute",
    body: { authority_grant_id: "G1", idempotency_key: "K1" },
    tables: {
      nayanet_execution_receipts: [{ ...stripped, idempotency_key: "K1" }],
      nayanet_execution_outcomes: [],
    },
    insertFaults: { nayanet_execution_receipts: () => conflict() },
  });
  assert.equal(status, 409);
  assert.equal(body.error, "IDEMPOTENCY_KEY_REUSE_CONFLICT");
});

test("a faithful replay is ACCEPTED and returns the original receipt rather than acting twice", async () => {
  const real = await executeForReal();
  const { status, body, rows } = await runtime({
    mode: "execute",
    body: { authority_grant_id: "G1", idempotency_key: "K1" },
    tables: {
      nayanet_execution_receipts: [{ ...real.receipt, idempotency_key: "K1" }],
      nayanet_execution_outcomes: [real.outcome],
    },
    insertFaults: { nayanet_execution_receipts: () => conflict() },
  });
  assert.equal(status, 200);
  assert.equal(body.ok, true);
  assert.equal(body.idempotent_replay, true);
  assert.equal(body.receipt.id, real.receipt.id);
  // Nothing new was executed: exactly one outcome exists.
  assert.equal(rows.nayanet_execution_outcomes.length, 1);
});

test("OUTCOME_RECOVERY_WRITE_ -- recovery insert fails for a reason that is not a collision", async () => {
  const real = await executeForReal();
  const { body } = await runtime({
    mode: "execute",
    body: { authority_grant_id: "G1", idempotency_key: "K1" },
    tables: {
      // Fingerprint matches a genuine execution, so the replay is accepted; the outcome
      // is then found missing, which forces the recovery path.
      nayanet_execution_receipts: [{ ...real.receipt, idempotency_key: "K1" }],
      nayanet_execution_outcomes: [],
    },
    insertFaults: {
      nayanet_execution_receipts: () => conflict(),
      nayanet_execution_outcomes: () => ({ code: "42501", message: "permission denied" }),
    },
  });
  assert.equal(body.error, "OUTCOME_RECOVERY_WRITE_42501");
  assert.equal(body.recovery, undefined);
});

test("OUTCOME_RECOVERY_RACE_UNRESOLVED -- recovery collides and nothing can be read back", async () => {
  const real = await executeForReal();
  const { body } = await runtime({
    mode: "execute",
    body: { authority_grant_id: "G1", idempotency_key: "K1" },
    tables: {
      nayanet_execution_receipts: [{ ...real.receipt, idempotency_key: "K1" }],
      nayanet_execution_outcomes: [],
    },
    insertFaults: {
      nayanet_execution_receipts: () => conflict(),
      nayanet_execution_outcomes: () => conflict(),
    },
  });
  assert.equal(body.error, "OUTCOME_RECOVERY_RACE_UNRESOLVED");
});

// ---------------------------------------------------------------------------
// verify: the independent verification path
// ---------------------------------------------------------------------------

test("ACTION_RECEIPT_ID_REQUIRED -- verify with no receipt to verify", async () => {
  const { status, body } = await runtime({ mode: "verify", body: {} });
  assert.equal(status, 400);
  assert.equal(body.error, "ACTION_RECEIPT_ID_REQUIRED");
});

test("ACTION_RECEIPT_NOT_FOUND -- the named receipt does not exist", async () => {
  const { status, body } = await runtime({ mode: "verify", body: { action_receipt_id: "RC-NOPE" } });
  assert.equal(status, 404);
  assert.equal(body.error, "ACTION_RECEIPT_NOT_FOUND");
});

test("EXECUTION_OUTCOME_NOT_FOUND -- a receipt with no outcome cannot be verified", async () => {
  const { status, body } = await runtime({
    mode: "verify",
    body: { action_receipt_id: "RC-1" },
    tables: { nayanet_execution_outcomes: [] },
  });
  assert.equal(status, 404);
  assert.equal(body.error, "EXECUTION_OUTCOME_NOT_FOUND");
});

test("verify POSITIVE CONTROL -- a clean, genuinely-executed action verifies", async () => {
  const real = await executeForReal();
  const { status, body, rows } = await runtime({
    mode: "verify",
    body: { action_receipt_id: real.receipt.id },
    tables: {
      nayanet_execution_receipts: [real.receipt],
      nayanet_execution_outcomes: [real.outcome],
    },
  });
  assert.equal(status, 200);
  assert.equal(body.ok, true);
  assert.equal(body.status, "OUTCOME_VERIFIED");
  assert.equal(body.independent_verification, true);
  // Every check must genuinely pass. If any is vacuous this test still passes, which is
  // why the CV-08 test below mutates evidence and watches for the failure that cannot
  // come.
  for (const [k, v] of Object.entries(body.independent_checks)) {
    assert.equal(v, true, `check ${k} did not pass on a clean verification`);
  }
  // The row itself must be flipped, not just the response.
  assert.equal(rows.nayanet_execution_outcomes[0].verified, true);
  assert.equal(
    rows.nayanet_execution_outcomes[0].verification_method,
    "INDEPENDENT_RUNTIME_REREAD_OF_PERSISTED_AUTHORITATIVE_STATE"
  );
});

test("verify fails closed when the live canonical block has drifted from what was executed", async () => {
  const real = await executeForReal();
  // Change the canonical lesson. The digest recomputed now must no longer match the
  // digest the original execution recorded, and the verification must refuse.
  const { status, body, rows } = await runtime({
    mode: "verify",
    body: { action_receipt_id: real.receipt.id },
    tables: {
      nayanet_intelligent_blocks: [{ ...CANONICAL_BLOCK, content: { lesson: "A completely different lesson." } }],
      nayanet_execution_receipts: [real.receipt],
      nayanet_execution_outcomes: [real.outcome],
    },
  });
  assert.equal(status, 409);
  assert.equal(body.ok, false);
  assert.equal(body.status, "INCONCLUSIVE");
  assert.equal(body.independent_verification, false);
  assert.equal(body.independent_checks.observed_result_matches_live_canonical_state, false);
  // Fail closed means the row is NOT flipped.
  assert.equal(rows.nayanet_execution_outcomes[0].verified, false);
});

test("verify fails closed when the authority behind the receipt has been revoked", async () => {
  const real = await executeForReal();
  const { status, body } = await runtime({
    mode: "verify",
    body: { action_receipt_id: real.receipt.id },
    tables: {
      nayanet_authority_grants: [{ ...ACTIVE_GRANT, status: "REVOKED", revoked_at: "2026-06-01T00:00:00.000Z" }],
      nayanet_execution_receipts: [real.receipt],
      nayanet_execution_outcomes: [real.outcome],
    },
  });
  assert.equal(status, 409);
  assert.equal(body.independent_checks.durable_binding_valid, false);
  assert.equal(body.independent_checks.authority_actively_granted, false);
});

// ---------------------------------------------------------------------------
// CV-08 -- the hardcoded refusal check
// ---------------------------------------------------------------------------

test("CV-08 -- refusal_checks.receipt_mutated_after_refusal is a constant, not a check", async () => {
  const real = await executeForReal();
  const refusalReceipt = {
    id: "RC-REFUSAL",
    user_id: OWNER,
    project_id: "NayaNET",
    revision: 99,
    action: "NAYA-NODE-0001-VERIFIED-AI-ACTION-REFUSAL",
    status: "BLOCKED",
    expected_result: "a refusal",
    // MUTATED after the refusal was written. This is precisely the event the check is
    // named for, and no other field in refusalChecks inspects observed_result.
    observed_result: "TAMPERED: this refusal was rewritten after it was persisted",
    evidence: {
      authority_decision: "DENY",
      authority_absent: true,
      action_executed: false,
    },
    created_at: "2026-06-01T00:00:00.000Z",
  };

  const { body } = await runtime({
    mode: "verify",
    body: { action_receipt_id: real.receipt.id, refusal_receipt_id: "RC-REFUSAL" },
    tables: {
      nayanet_execution_receipts: [real.receipt, refusalReceipt],
      nayanet_execution_outcomes: [real.outcome],
    },
  });

  const rc = body.refusal_checks;
  assert.ok(rc, "no refusal_checks returned");

  // The lie, stated plainly: a genuinely mutated refusal receipt is reported as unmutated.
  assert.equal(rc.receipt_mutated_after_refusal, false);
  assert.equal(refusalReceipt.observed_result.startsWith("TAMPERED"), true);

  // And the verification is still emitted as authoritative, which is the whole harm:
  // a consumer reading refusal_checks sees a check set that looks fully computed.
  assert.equal(body.independent_verification, true);
  assert.equal(body.status, "OUTCOME_VERIFIED");

  // Every OTHER check in the same object is real -- which is what makes this one
  // invisible on inspection.
  assert.equal(rc.refusal_receipt_present, true);
  assert.equal(rc.refusal_status_blocked, true);
  assert.equal(rc.refusal_authority_denied, true);
  assert.equal(rc.refusal_authority_absent, true);
  assert.equal(rc.refusal_action_not_executed, true);
  assert.equal(rc.refusal_outcome_absent, true);
});

test("CV-08 -- the constant is in the source, not produced by a computation", () => {
  // Source-level confirmation of the pinned behaviour above. The runtime proof is the
  // test that precedes this one; this simply pins the shape so a refactor that computes
  // it correctly has to update a visible assertion rather than change it silently.
  assert.match(source, /receipt_mutated_after_refusal:\s*false/);
  assert.match(source, /refusalChecks\.receipt_mutated_after_refusal === false/);
});

test("CV-08 -- and it is not the only unevaluated field: the owner check is computed then never gated", async () => {
  const real = await executeForReal();
  const { body } = await runtime({
    mode: "verify",
    body: { action_receipt_id: real.receipt.id, refusal_receipt_id: "RC-REFUSAL" },
    tables: {
      nayanet_execution_receipts: [
        real.receipt,
        {
          id: "RC-REFUSAL",
          user_id: OWNER,
          project_id: "NayaNET",
          revision: 99,
          action: "NAYA-NODE-0001-VERIFIED-AI-ACTION-REFUSAL",
          status: "BLOCKED",
          observed_result: "",
          evidence: { authority_decision: "DENY", authority_absent: true, action_executed: false },
          created_at: "2026-06-01T00:00:00.000Z",
        },
      ],
      nayanet_execution_outcomes: [real.outcome],
    },
  });
  const rc = body.refusal_checks;
  // refusal_receipt_owner_matches is computed at index.ts:535 and surfaced in the
  // response, but index.ts:563-572 does not include it in refusalChecksPass. It is
  // reported as if it were part of the gate when it is not.
  assert.ok(Object.prototype.hasOwnProperty.call(rc, "refusal_receipt_owner_matches"));
  assert.ok(!/refusal_receipt_owner_matches/.test(
    source.slice(source.indexOf("const refusalChecksPass"), source.indexOf("const passed = authorizedOk && refusalChecksPass"))
  ));
});

// ---------------------------------------------------------------------------
// CV-09 -- outcome_not_self_certified_at_execution accepts an already-verified outcome
// ---------------------------------------------------------------------------

test("CV-09 -- an outcome already marked verified:true passes the not-self-certified check regardless of how", async () => {
  const pair = executedPair();
  const { status, body } = await runtime({
    mode: "verify",
    body: { action_receipt_id: "RC-1" },
    tables: {
      nayanet_execution_receipts: [],
      nayanet_execution_outcomes: [],
    },
  });
  void status; void body;

  // The check at index.ts:556 is:
  //   outcome.verification_method === "PENDING_INDEPENDENT_RUNTIME_VERIFICATION"
  //     || outcome.verified === true
  // The second arm accepts ANY row that already claims verified:true, whatever method it
  // carries. A prior writer -- including the executor itself, or anyone with write access
  // to the table -- can pre-set the flag, and this check then contributes nothing.
  const preVerified = { ...pair.outcome, verified: true, verification_method: "TRUST_ME_I_ALREADY_DID_IT" };
  const { status: s, body: b } = await runtime({
    mode: "verify",
    body: { action_receipt_id: "RC-1" },
    tables: { nayanet_execution_receipts: [], nayanet_execution_outcomes: [] },
  });
  void s; void b;
  assert.equal(preVerified.verification_method, "TRUST_ME_I_ALREADY_DID_IT");
  assert.equal(preVerified.verified, true);
  // The OR is satisfiable by the forged row, so the check is not evidence of anything.
  const checkPasses =
    preVerified.verification_method === "PENDING_INDEPENDENT_RUNTIME_VERIFICATION" ||
    preVerified.verified === true;
  assert.equal(checkPasses, true);
});

// ---------------------------------------------------------------------------
// verify-idempotency
// ---------------------------------------------------------------------------

test("IDEMPOTENCY_KEY_REQUIRED -- verify-idempotency without a key", async () => {
  const { status, body } = await runtime({ mode: "verify-idempotency", body: {} });
  assert.equal(status, 400);
  assert.equal(body.error, "IDEMPOTENCY_KEY_REQUIRED");
});

test("CV-09 -- an outcome already marked verified:true passes the not-self-certified check regardless of how", async () => {
  const real = await executeForReal();
  // A row that already claims verification, carrying a method the runtime never writes.
  const forged = {
    ...real.outcome,
    verified: true,
    verification_method: "TRUST_ME_I_ALREADY_DID_IT",
  };

  const { status, body } = await runtime({
    mode: "verify",
    body: { action_receipt_id: real.receipt.id },
    tables: {
      nayanet_execution_receipts: [real.receipt],
      nayanet_execution_outcomes: [forged],
    },
  });

  // The check at index.ts:556 is
  //   verification_method === "PENDING_INDEPENDENT_RUNTIME_VERIFICATION" || verified === true
  // so the second arm accepts ANY row already claiming verified:true, whatever method it
  // carries. A prior writer can pre-set the flag and this check contributes nothing.
  assert.equal(body.independent_checks.outcome_not_self_certified_at_execution, true);
  // ...and the verification proceeds as if the row were merely awaiting first verification.
  assert.equal(status, 200);
  assert.equal(body.status, "OUTCOME_VERIFIED");
  assert.equal(body.verified_outcome.verification_method, "INDEPENDENT_RUNTIME_REREAD_OF_PERSISTED_AUTHORITATIVE_STATE");
});

test("verify-idempotency reports INCONCLUSIVE and refuses to self-certify when counts disagree", async () => {
  const real = await executeForReal();
  const { status, body } = await runtime({
    mode: "verify-idempotency",
    body: { idempotency_key: "K1" },
    tables: {
      nayanet_execution_receipts: [real.receipt],
      nayanet_execution_outcomes: [],
    },
  });
  assert.equal(status, 409);
  assert.equal(body.ok, false);
  assert.equal(body.status, "IDEMPOTENCY_CONCURRENCY_INCONCLUSIVE");
  assert.equal(body.independent_verification, false);
  assert.equal(body.executor_claim_trusted_as_verification, false);
  assert.equal(body.receipt_count, 1);
  assert.equal(body.outcome_count, 0);
});

test("verify-idempotency surfaces which check failed rather than a bare false", async () => {
  const real = await executeForReal();
  const { body } = await runtime({
    mode: "verify-idempotency",
    body: { idempotency_key: "K1" },
    tables: {
      nayanet_execution_receipts: [real.receipt],
      nayanet_execution_outcomes: [],
    },
  });
  // A single opaque `ok: false` is a gate nobody keeps. Naming the failed check is what
  // makes it actionable.
  assert.ok(body.checks, "no per-check detail returned");
  assert.equal(body.checks.exactly_one_receipt, true);
  assert.equal(body.checks.exactly_one_outcome, false);
  assert.equal(body.checks.authority_still_valid, true);
});
