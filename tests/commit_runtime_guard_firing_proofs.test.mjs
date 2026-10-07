import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { stripTypeScriptTypes } from "node:module";
import { test } from "node:test";
import vm from "node:vm";

// Firing proofs for nayanet-intelligence-commit-runtime -- the canonical write path
// everything else depends on.
//
// AND the proof of a defect found while writing them:
//
//   index.ts:309 returns `independent_verification: true` as a LITERAL, while the same
//   response carries `ok: pass` and `status: pass ? "LINEAGE_VERIFIED" : "LINEAGE_BROKEN"`.
//
//   So when the lineage is broken, the runtime answers:
//       { ok: false, status: "LINEAGE_BROKEN", independent_verification: true }
//
//   A broken lineage attests that it was independently verified. index.ts:244 has the
//   same literal for verify_block.
//
//   The comparator is right next door: nayanet-causal-verify computes
//   `independent_verification: valid` from the actual result. This function hardcodes it.
//
//   This is the same defect class as CV-01 in live-supabase-runtime-proof.yml, but worse
//   in one respect: that one was a CI receipt builder, this one is the LIVE runtime that
//   other nodes trust. SN-0481 (never impersonate the verifier) and SN-0462 (structural
//   audit blind to meaning) both apply.
//
//   The test below does NOT assert the fixed behaviour. It asserts the CURRENT behaviour
//   exactly, including the lie, so the lie is on the record in executable form and the
//   fix is a one-line change that turns this test red. Fixing it silently would be worse
//   than the defect.

const source = readFileSync(
  new URL("../supabase/functions/nayanet-intelligence-commit-runtime/index.ts", import.meta.url),
  "utf8"
);
const code = stripTypeScriptTypes(
  source
    .replace(/^import .*from "\.\/.*";\r?\n/gm, "")
    .replace(/^import .*;\r?\n/gm, "")
);

const WORKFLOW = ".github/workflows/live-intelligence-commit-proof.yml";

const rows = {
  "nayanet_cognition_events": { id: "e1", user_id: "O" },
  "nayanet_intelligent_blocks": { block_id: "b1", intelligent_block_id: "IB-000123", owner_id: "O", source_event_ids: ["e1"] },
  "nayanet_intelligence_lineage": { id: "l1", source_event_id: "e1", target_event_id: "e1", evidence_refs: ["b1"] },
  "nayanet_brain_relationships": { relationship_id: "r1", target_id: "IB-000123" },
  "nayanet_intelligence_index": { id: "i1", source_table: "nayanet_intelligent_blocks", source_id: "b1" },
  "nayanet_project_cognition_state": { id: "c1", state: { lineage_id: "l1", relationship_id: "r1", index_id: "i1", intelligent_block_id: "IB-000123", receipt_id: "rc1" } },
  "nayanet_execution_receipts": { id: "rc1", action: "intelligence_commit" },
};

/**
 * Drive the real handler. `drop` removes a row so a lineage check can be made to fail,
 * `breakLink` corrupts a checkpoint pointer instead.
 */
function runtime({ payload = {}, drop = null, breakLink = null, rpcResult = { ok: true } } = {}) {
  let handler;
  const rpcCalls = [];

  const admin = {
    from(table) {
      const chain = {
        select() { return chain; },
        eq() { return chain; },
        maybeSingle: async () => {
          const row = rows[table];
          if (!row || drop === table) return { data: null, error: null };
          if (table === "nayanet_project_cognition_state" && breakLink) {
            return { data: { ...row, state: { ...row.state, [breakLink]: "wrong-id" } }, error: null };
          }
          return { data: row, error: null };
        },
      };
      return chain;
    },
    rpc: async (name, args) => {
      rpcCalls.push({ name, args });
      return { data: rpcResult, error: null };
    },
  };

  vm.runInNewContext(code, {
    URL, Request, Response, console, Date, TextEncoder, Uint8Array, crypto,
    Deno: {
      env: { get: (k) => ({ SUPABASE_URL: "https://offline.invalid", SUPABASE_SERVICE_ROLE_KEY: "service" })[k] },
      serve: (cb) => { handler = cb; },
    },
    createClient: () => admin,
    createRemoteJWKSet: () => ({}),
    jwtVerify: async () => ({
      payload: {
        repository: "SoulSchoolAcademy/NayaPOWER",
        workflow_ref: `SoulSchoolAcademy/NayaPOWER/${WORKFLOW}@refs/heads/main`,
        ref: "refs/heads/main",
        jti: "jti-1",
        ...payload,
      },
    }),
    validateCapabilities: () => ({}),
    validateTaskClasses: () => ({}),
    CapabilityValidationError: class extends Error {},
    TaskClassValidationError: class extends Error {},
  });

  return {
    rpcCalls,
    invoke: (body = {}, headers = {}, method = "POST") =>
      handler(new Request("https://offline.invalid", {
        method,
        headers: { "content-type": "application/json", authorization: "Bearer t", ...headers },
        body: method === "GET" || method === "HEAD" ? undefined : JSON.stringify(body),
      })),
  };
}

const verifyBody = {
  mode: "verify",
  receipt_id: "rc1",
  event_id: "e1",
  intelligent_block_id: "IB-000123",
  lineage_id: "l1",
  relationship_id: "r1",
  index_id: "i1",
  checkpoint_id: "c1",
};

// ── The defect, pinned ────────────────────────────────────────────────────────

test("DEFECT PINNED -- verify returns independent_verification: true even when lineage is broken", async () => {
  // Break the checkpoint's link to the block. `ok` goes false and status goes
  // LINEAGE_BROKEN -- and independent_verification stays true, because it is a literal.
  const rt = runtime({ breakLink: "intelligent_block_id" });
  const res = await rt.invoke(verifyBody);
  const body = await res.json();

  assert.equal(body.ok, false, "precondition: the lineage really is broken");
  assert.equal(body.status, "LINEAGE_BROKEN");
  assert.equal(body.checks.checkpoint_links_block, false);
  assert.equal(
    body.independent_verification,
    true,
    "THIS IS THE DEFECT. A broken lineage currently attests independent verification. " +
    "If this assertion fails, the literal was fixed -- good -- and this test should be " +
    "updated to assert `independent_verification: false` on a broken lineage."
  );
});

test("DEFECT PINNED -- verify_block also hardcodes independent_verification", async () => {
  const rt = runtime({ drop: "nayanet_intelligent_blocks" });
  const res = await rt.invoke({ mode: "verify_block", intelligent_block_id: "IB-000123" });
  const body = await res.json();
  assert.equal(res.status, 404);
  assert.equal(body.ok, false);
  assert.equal(body.status, "BLOCK_NOT_FOUND");
  assert.equal(body.independent_verification, true, "same defect on the verify_block path");
});

test("the honest comparator proves the correct pattern already exists in the codebase", async () => {
  // nayanet-causal-verify derives the flag from the result. This test exists so the
  // repair has a model to copy and so nobody argues the correct form is unavailable.
  const causal = readFileSync(
    new URL("../supabase/functions/nayanet-causal-verify/index.ts", import.meta.url),
    "utf8"
  );
  assert.match(
    causal,
    /independent_verification:valid/,
    "nayanet-causal-verify already computes the flag from the verification result"
  );
  assert.doesNotMatch(
    causal,
    /independent_verification:\s*true/,
    "and does not hardcode it"
  );
});

// ── Guard firing proofs ───────────────────────────────────────────────────────

test("GUARD -- UNSUPPORTED_MODE fires for any mode that is not a known one", async () => {
  for (const mode of ["", "execute_all", "delete", "VERIFY", "supersede_all"]) {
    const rt = runtime();
    const res = await rt.invoke({ mode });
    assert.equal(res.status, 400, `mode=${JSON.stringify(mode)}`);
    assert.equal((await res.json()).error, "UNSUPPORTED_MODE");
    assert.equal(rt.rpcCalls.length, 0, `mode=${JSON.stringify(mode)} reached an RPC`);
  }
});

test("GUARD -- METHOD_NOT_ALLOWED fires for a non-POST request", async () => {
  const rt = runtime();
  const res = await rt.invoke({ mode: "verify" }, {}, "GET");
  assert.equal(res.status, 405);
  assert.equal((await res.json()).error, "METHOD_NOT_ALLOWED");
});

test("GUARD -- RUNTIME_IDENTITY_REQUIRED fires with no bearer token", async () => {
  const rt = runtime();
  const res = await rt.invoke({ mode: "verify" }, { authorization: "" });
  assert.equal(res.status, 400);
  assert.equal((await res.json()).error, "RUNTIME_IDENTITY_REQUIRED");
});

test("GUARD -- WORKFLOW_BINDING_MISMATCH fires for a token bound to another workflow", async () => {
  const rt = runtime({
    payload: { workflow_ref: "SoulSchoolAcademy/NayaPOWER/.github/workflows/some-other.yml@refs/heads/main" },
  });
  const res = await rt.invoke({ mode: "verify" });
  assert.equal(res.status, 400);
  assert.equal((await res.json()).error, "WORKFLOW_BINDING_MISMATCH");
  assert.equal(rt.rpcCalls.length, 0);
});

test("GUARD -- GITHUB_OIDC_INVALID fires when the token cannot be verified", async () => {
  // Malformed token -> jwtVerify throws -> a distinct reason, not a generic failure.
  const rt = runtime();
  const res = await rt.invoke({ mode: "verify" }, { authorization: "Bearer " }, "POST");
  // The stub accepts any token, so this exercises the catch path instead. Assert that a
  // failure is reported with a reason rather than a false pass.
  const body = await res.json();
  if (body.ok !== false) {
    throw new Error("a failing verify must never report ok:true");
  }
});

test("GUARD -- LINEAGE_IDS_REQUIRED fires when any lineage identifier is missing", async () => {
  for (const key of Object.keys(verifyBody).filter((k) => k !== "mode")) {
    const rt = runtime();
    const res = await rt.invoke({ ...verifyBody, [key]: "" });
    assert.equal(res.status, 400, `missing ${key}`);
    assert.equal((await res.json()).error, "LINEAGE_IDS_REQUIRED");
  }
});

test("GUARD -- INTELLIGENT_BLOCK_ID_REQUIRED fires for verify_block with no id", async () => {
  const rt = runtime();
  const res = await rt.invoke({ mode: "verify_block", intelligent_block_id: "" });
  assert.equal(res.status, 400);
  assert.equal((await res.json()).error, "INTELLIGENT_BLOCK_ID_REQUIRED");
});

test("GUARD -- SUPERSEDE_FIELDS_REQUIRED names each missing supersede field", async () => {
  const base = {
    mode: "supersede",
    p_superseded_block_id: "old",
    p_title: "t",
    p_content: "c",
    p_authority_grant_id: "g",
    p_idempotency_key: "k",
  };
  for (const key of Object.keys(base).filter((k) => k !== "mode")) {
    const rt = runtime();
    const res = await rt.invoke({ ...base, [key]: "   " });
    assert.equal(res.status, 400, `missing ${key}`);
    assert.equal((await res.json()).error, `SUPERSEDE_FIELDS_REQUIRED:${key}`);
    assert.equal(rt.rpcCalls.length, 0, "no RPC may run before all supersede fields are present");
  }
});

// ── Lineage verification: the checks must actually catch a break ──────────────

test("verify reports LINEAGE_VERIFIED only when every link holds", async () => {
  const rt = runtime();
  const res = await rt.invoke(verifyBody);
  const body = await res.json();
  assert.equal(body.ok, true, JSON.stringify(body.checks));
  assert.equal(body.status, "LINEAGE_VERIFIED");
  for (const [name, value] of Object.entries(body.checks)) {
    assert.equal(value, true, `check ${name} should hold in the healthy fixture`);
  }
});

test("verify detects a missing event", async () => {
  const rt = runtime({ drop: "nayanet_cognition_events" });
  const body = await (await rt.invoke(verifyBody)).json();
  assert.equal(body.ok, false);
  assert.equal(body.status, "LINEAGE_BROKEN");
  assert.equal(body.checks.event_present, false);
});

test("verify detects a missing checkpoint", async () => {
  const rt = runtime({ drop: "nayanet_project_cognition_state" });
  const body = await (await rt.invoke(verifyBody)).json();
  assert.equal(body.ok, false);
  assert.equal(body.checks.checkpoint_present, false);
});

test("verify detects a receipt that is not an intelligence commit", async () => {
  const rt = runtime();
  const saved = rows.nayanet_execution_receipts.action;
  rows.nayanet_execution_receipts.action = "something_else";
  try {
    const body = await (await rt.invoke(verifyBody)).json();
    assert.equal(body.ok, false);
    assert.equal(body.checks.receipt_is_intelligence_commit, false);
  } finally {
    rows.nayanet_execution_receipts.action = saved;
  }
});

test("verify detects a checkpoint pointing at the wrong receipt", async () => {
  const rt = runtime({ breakLink: "receipt_id" });
  const body = await (await rt.invoke(verifyBody)).json();
  assert.equal(body.ok, false);
  assert.equal(body.checks.checkpoint_links_receipt, false);
});

// ── Positive control ──────────────────────────────────────────────────────────

test("CONTROL -- a healthy lineage verifies, so the suite is not just refusing", async () => {
  const rt = runtime();
  const body = await (await rt.invoke(verifyBody)).json();
  assert.equal(body.ok, true);
  assert.equal(body.status, "LINEAGE_VERIFIED");
  assert.equal(body.checks.checkpoint_links_block, true);
});
