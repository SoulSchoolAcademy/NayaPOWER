import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { stripTypeScriptTypes } from "node:module";
import { test } from "node:test";
import vm from "node:vm";

// EXECUTED coverage for nayanet-causal-verify.
//
// This function is the causal-verification gate. Until now it had ZERO executed
// tests -- only source-text greps in tests/test_cvo_runtime_identity_contract.py,
// which assert the code looks right, not that it runs. That is the same blind spot
// that let nayanet-prove-runtime ship an un-imported identifier as an opaque HTTP 400
// (live-prove-proof run 37384065800) while 13/13 tests were green.
//
// The handler is loaded into a VM sandbox with stubbed Deno / jose / supabase, so the
// real request-handling path executes here exactly as it does in Deno.

const source = readFileSync(
  new URL("../supabase/functions/nayanet-causal-verify/index.ts", import.meta.url),
  "utf8"
);
const code = stripTypeScriptTypes(source.replace(/^import .*;\r?\n/gm, ""));

const OWNER_ID = "adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const NAYA_ID = "NAYA-NODE-0001";
const MISSION_ID = "NAYA-NODE-0001-CONTINUITY";
const TREATMENT_ID = "6aee287d-c47d-4667-86ed-6b53be8bd384";
const CONTROL_ID = "b00ed556-d7b7-4e5e-90a0-4620b9aaef67";
const BLOCK_ID = "IB-NAYA-NODE-0001-0001";

const claims = {
  repository: "SoulSchoolAcademy/NayaPOWER",
  ref: "refs/heads/main",
  workflow_ref: "SoulSchoolAcademy/NayaPOWER/.github/workflows/live-cvo-runtime-proof.yml@refs/heads/main",
  jti: "cvo-exec-jti",
  sub: "repo:SoulSchoolAcademy/NayaPOWER:ref:refs/heads/main",
};

function canonicalGrant() {
  return {
    grant_id: "grant-1",
    issuer_id: OWNER_ID,
    subject_id: OWNER_ID,
    mission_id: MISSION_ID,
    scope: { target: NAYA_ID },
    actions: ["naya_node_apply"],
    constraints: {},
    status: "ACTIVE",
    evidence: {},
  };
}

const treatmentOutcomeEvidence = {
  treatment_condition: true,
  intelligence_id: BLOCK_ID,
  provenance_present: true,
};
const controlOutcomeEvidence = {
  control_condition: true,
  provenance_present: false,
};

// An explicit `null` means "this row does not exist" and must be distinguishable from
// an omitted key, meaning "use the canonical fixture". `??` cannot tell them apart.
function pick(value, fallback) {
  return value === undefined ? fallback : value;
}

function receipts({ grantCount = 1, treatment, control, treatmentOutcome, controlOutcome } = {}) {
  return {
    treatment: pick(treatment, {
      id: TREATMENT_ID,
      action: "NAYA-NODE-0001-TREATMENT",
      status: "SUCCESS",
      observed_result: "TREATMENT_BEHAVIOR",
      evidence: [],
    }),
    control: pick(control, {
      id: CONTROL_ID,
      action: "NAYA-NODE-0001-BASELINE",
      status: "SUCCESS",
      observed_result: "CONTROL_BEHAVIOR",
      evidence: [],
    }),
    treatmentOutcome: pick(treatmentOutcome, {
      outcome_id: "outcome-treatment",
      receipt_id: TREATMENT_ID,
      experiment_case_id: "NAYA-NODE-0001-COLD-BEHAVIOR",
      verified: true,
      evidence: treatmentOutcomeEvidence,
    }),
    controlOutcome: pick(controlOutcome, {
      outcome_id: "outcome-control",
      receipt_id: CONTROL_ID,
      experiment_case_id: "NAYA-NODE-0001-COLD-BEHAVIOR",
      verified: true,
      evidence: controlOutcomeEvidence,
    }),
  };
}

function runtime(options = {}) {
  const { grantCount = 1, ...data } = options;
  const state = receipts(data);
  let handler;

  const grants = Array.from({ length: grantCount }, (_, i) => ({
    ...canonicalGrant(),
    grant_id: `grant-${i + 1}`,
  }));

  function query(table) {
    const filters = {};
    const builder = {
      select() { return builder; },
      eq(key, value) { filters[key] = value; return builder; },
      in() { return builder; },
      order() { return builder; },
      limit() { return builder; },
      insert() { return builder; },
      update() { return builder; },
      async single() {
        // The only single() in this handler is the causal_verification write-back.
        if (table === "nayanet_execution_receipts") {
          return { data: { id: filters.id, action: "NAYA-NODE-0001-TREATMENT", status: "SUCCESS", evidence: state.treatment.evidence }, error: null };
        }
        throw new Error("unexpected single table: " + table);
      },
      async maybeSingle() {
        if (table === "nayanet_authority_grants") return { data: grants[0] ?? null, error: null };
        if (table === "nayanet_execution_receipts") {
          const id = filters.id;
          if (id === TREATMENT_ID) return { data: state.treatment, error: null };
          if (id === CONTROL_ID) return { data: state.control, error: null };
          return { data: null, error: null };
        }
        if (table === "nayanet_execution_outcomes") {
          const receiptId = filters.receipt_id;
          if (receiptId === TREATMENT_ID) return { data: state.treatmentOutcome, error: null };
          if (receiptId === CONTROL_ID) return { data: state.controlOutcome, error: null };
          return { data: null, error: null };
        }
        throw new Error("unexpected maybeSingle table: " + table);
      },
      // The authority-binding read is the one list-shaped query in the verify path.
      // Awaiting the builder resolves it, exactly as supabase-js does.
      async then(resolve, reject) {
        if (table === "nayanet_authority_grants") return resolve({ data: grants, error: null });
        if (table === "nayanet_execution_outcomes") return resolve({ data: [], error: null });
        try { reject(new Error("unexpected list table: " + table)); } catch { /* noop */ }
        return undefined;
      },
    };
    return builder;
  }

  const admin = { from: query };

  vm.runInNewContext(code, {
    URL, Request, Response, console, Date, TextEncoder, Uint8Array, crypto,
    Deno: {
      env: { get: (k) => ({ SUPABASE_URL: "https://offline.invalid", SUPABASE_SERVICE_ROLE_KEY: "fake" })[k] },
      serve: (cb) => { handler = cb; },
    },
    createRemoteJWKSet: () => ({}),
    jwtVerify: async () => ({ payload: claims }),
    createClient: () => admin,
  });

  return (body) =>
    handler(new Request("https://offline.invalid", {
      method: "POST",
      headers: { authorization: "Bearer test", "content-type": "application/json" },
      body: JSON.stringify(body),
    }));
}

const base = { mode: "verify", treatment_receipt_id: TREATMENT_ID, control_receipt_id: CONTROL_ID };

test("causal-verify rejects an unsupported mode", async () => {
  const invoke = runtime();
  const res = await invoke({ ...base, mode: "not-a-mode" });
  assert.equal(res.status, 400);
  assert.equal((await res.json()).error, "UNSUPPORTED_MODE");
});

test("causal-verify fails closed when the durable authority binding is not exactly one grant", async () => {
  for (const grantCount of [0, 2]) {
    const invoke = runtime({ grantCount });
    const res = await invoke(base);
    assert.equal(res.status, 403);
    const body = await res.json();
    assert.equal(body.error, "DURABLE_NAYA_AUTHORIZATION_BINDING_INVALID");
    assert.equal(body.count, grantCount);
  }
});

test("causal-verify fails closed when a paired receipt is missing", async () => {
  const invoke = runtime({ treatment: null });
  const res = await invoke(base);
  assert.equal(res.status, 404);
  assert.equal((await res.json()).error, "PAIRED_ACTION_RECEIPTS_NOT_FOUND");
});

test("causal-verify fails closed when a paired outcome is missing", async () => {
  const invoke = runtime({ controlOutcome: null });
  const res = await invoke(base);
  assert.equal(res.status, 404);
  assert.equal((await res.json()).error, "PAIRED_ACTION_OUTCOMES_NOT_FOUND");
});

test("causal-verify fails closed when an outcome is not verified", async () => {
  const { controlOutcome } = receipts();
  const invoke = runtime({ controlOutcome: { ...controlOutcome, verified: false } });
  const res = await invoke(base);
  assert.equal(res.status, 409);
  assert.equal((await res.json()).error, "PAIRED_ACTION_OUTCOMES_NOT_VERIFIED");
});

test("causal-verify fails closed on the wrong experiment case", async () => {
  const { treatmentOutcome } = receipts();
  const invoke = runtime({ treatmentOutcome: { ...treatmentOutcome, experiment_case_id: "WRONG-CASE" } });
  const res = await invoke(base);
  assert.equal(res.status, 409);
  assert.equal((await res.json()).error, "PAIRED_ACTION_OUTCOME_CASE_INVALID");
});

test("causal-verify fails closed when treatment outcome evidence is invalid", async () => {
  // The direction of the treatment/control effect is the whole claim. A treatment arm
  // that does not carry provenance must never verify, or the causal verdict is forged.
  const { treatmentOutcome } = receipts();
  const invoke = runtime({
    treatmentOutcome: { ...treatmentOutcome, evidence: { ...treatmentOutcomeEvidence, provenance_present: false } },
  });
  const res = await invoke(base);
  assert.equal(res.status, 409);
  assert.equal((await res.json()).error, "TREATMENT_OUTCOME_EVIDENCE_INVALID");
});

test("causal-verify fails closed when control outcome evidence is invalid", async () => {
  const { controlOutcome } = receipts();
  const invoke = runtime({
    controlOutcome: { ...controlOutcome, evidence: { ...controlOutcomeEvidence, provenance_present: true } },
  });
  const res = await invoke(base);
  assert.equal(res.status, 409);
  assert.equal((await res.json()).error, "CONTROL_OUTCOME_EVIDENCE_INVALID");
});

test("causal-verify fails closed when treatment binds the wrong intelligent block", async () => {
  const { treatmentOutcome } = receipts();
  const invoke = runtime({
    treatmentOutcome: { ...treatmentOutcome, evidence: { ...treatmentOutcomeEvidence, intelligence_id: "IB-SOMEONE-ELSES" } },
  });
  const res = await invoke(base);
  assert.equal(res.status, 409);
  assert.equal((await res.json()).error, "TREATMENT_OUTCOME_EVIDENCE_INVALID");
});

test("causal-verify fails closed when receipt actions are not the paired treatment/baseline", async () => {
  const invoke = runtime({
    treatment: { id: TREATMENT_ID, action: "SOMETHING-ELSE", status: "SUCCESS", evidence: [] },
  });
  const res = await invoke(base);
  assert.equal(res.status, 409);
  assert.equal((await res.json()).error, "PAIRED_ACTION_RECEIPTS_INVALID");
});

test("causal-verify fails closed when a paired receipt is not SUCCESS", async () => {
  const invoke = runtime({
    control: { id: CONTROL_ID, action: "NAYA-NODE-0001-BASELINE", status: "FAILED", evidence: [] },
  });
  const res = await invoke(base);
  assert.equal(res.status, 409);
  assert.equal((await res.json()).error, "PAIRED_ACTION_OUTCOME_NOT_SUCCESS");
});

test("verify mode fails closed when no causal_verification was persisted", async () => {
  const invoke = runtime();
  const res = await invoke(base);
  assert.equal(res.status, 409);
  assert.equal((await res.json()).error, "CVO_NOT_PERSISTED");
});

function persistedCausal(overrides = {}) {
  return {
    causal_verification: {
      schema: "NAYANET_CAUSAL_VERIFICATION_V1",
      receipt_id: TREATMENT_ID,
      comparison_receipt_id: CONTROL_ID,
      causal_method: "CONTROLLED_INTERVENTION",
      causal_assessment: "CAUSAL_SUPPORTED",
      verification_status: "OUTCOME_VERIFIED",
      production_action_executed: true,
      observed_change: "TREATMENT_BEHAVIOR",
      evidence: {
        refs: [TREATMENT_ID, CONTROL_ID, BLOCK_ID],
        control: { outcome_id: "outcome-control", evidence: { provenance_present: false } },
        treatment: { outcome_id: "outcome-treatment", evidence: { provenance_present: true } },
      },
      ...overrides,
    },
  };
}

function verifyWithCausal(causalOverrides) {
  const { treatment, treatmentOutcome } = receipts();
  return runtime({
    treatment: { ...treatment, evidence: [persistedCausal(causalOverrides)] },
    treatmentOutcome,
  });
}

test("verify mode accepts a faithfully persisted causal verification", async () => {
  const res = await verifyWithCausal()(base);
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.equal(body.ok, true);
  // The verdict is carried inside verification.independent_verification; the envelope
  // does not duplicate it at the top level.
  assert.equal(body.verification.independent_verification, true);
  assert.equal(body.verification.receipt_id, TREATMENT_ID);
  assert.equal(body.verification.comparison_receipt_id, CONTROL_ID);
  assert.equal(body.verification.active_authorization_grant_id, "grant-1");
});

test("verify mode rejects a persisted claim whose treatment outcome_id is forged", async () => {
  const res = await verifyWithCausal({
    evidence: {
      refs: [TREATMENT_ID, CONTROL_ID, BLOCK_ID],
      control: { outcome_id: "outcome-control", evidence: { provenance_present: false } },
      treatment: { outcome_id: "outcome-not-actually-observed", evidence: { provenance_present: true } },
    },
  })(base);
  assert.equal(res.status, 409);
  const body = await res.json();
  assert.equal(body.ok, false);
  assert.equal(body.status, undefined);
});

test("verify mode rejects a persisted claim that inverts the provenance contrast", async () => {
  // The single most important negative: a record claiming CAUSAL_SUPPORTED while its
  // own evidence shows control had provenance and treatment did not is a forged proof.
  const res = await verifyWithCausal({
    evidence: {
      refs: [TREATMENT_ID, CONTROL_ID, BLOCK_ID],
      control: { outcome_id: "outcome-control", evidence: { provenance_present: true } },
      treatment: { outcome_id: "outcome-treatment", evidence: { provenance_present: false } },
    },
  })(base);
  assert.equal(res.status, 409);
  assert.equal((await res.json()).ok, false);
});

test("verify mode rejects a causal record missing its evidence arms entirely", async () => {
  // Regression anchor for the untyped-JSONB read: before the explicit narrowing, a
  // record with no evidence object silently compared `undefined` and could pass on
  // the strength of the other fields alone.
  const res = await verifyWithCausal({ evidence: undefined })(base);
  assert.equal(res.status, 409);
  assert.equal((await res.json()).ok, false);
});

test("verify mode rejects a downgraded causal assessment persisted as supported", async () => {
  const res = await verifyWithCausal({ causal_assessment: "CAUSAL_UNSUPPORTED" })(base);
  assert.equal(res.status, 409);
  assert.equal((await res.json()).ok, false);
});

test("verify mode rejects a causal record pointing at the wrong paired receipt", async () => {
  const res = await verifyWithCausal({ comparison_receipt_id: "some-other-receipt" })(base);
  assert.equal(res.status, 409);
  assert.equal((await res.json()).ok, false);
});

test("cvo mode never executes a governed action; it only observes and records", async () => {
  // Causal verification observes an already-completed governed action. Whatever a
  // caller asks for, this runtime must not gain the ability to perform one.
  const { treatment, treatmentOutcome } = receipts();
  const invoke = runtime({
    treatment: { ...treatment, evidence: [persistedCausal()] },
    treatmentOutcome,
  });
  const res = await invoke({ mode: "cvo", treatment_receipt_id: TREATMENT_ID, control_receipt_id: CONTROL_ID });
  const body = await res.json();

  assert.equal(body.ok, true);
  assert.equal(body.schema, "NAYANET_CAUSAL_VERIFY_RUNTIME_V1");
  // It asserts the action WAS executed (observed), and grants nothing itself.
  assert.equal(body.causal_verification.production_action_executed, true);
  assert.match(body.causal_verification.permission.basis, /does not grant execution authority/);
  // No authority token is minted by verification.
  assert.equal(body.causal_verification.authority.status, "AUTHORIZED");
  assert.equal(body.causal_verification.authority.grant_id, "grant-1");
  // And no execution outcome is created by this runtime.
  assert.equal(body.receipt.action, "NAYA-NODE-0001-TREATMENT");
});

test("recover-learning-outcomes refuses a pair whose arms disagree on task", async () => {
  const { treatment, control, treatmentOutcome, controlOutcome } = receipts();
  const baseEvidence = (condition, extra) => ({
    task_input: { task_id: "NAYA-0001-PROVENANCE-HELDOUT-001" },
    learning_id: "learning-1",
    source_event_id: "event-1",
    condition,
    behavior: "X",
    ...extra,
  });
  const invoke = runtime({
    treatment: {
      ...treatment,
      action: "NAYA-NODE-0001-TREATMENT-1",
      observed_result: "X",
      evidence: [baseEvidence("TREATMENT", {
        retained_intelligence_used: true,
        intelligence_id: BLOCK_ID,
        outcome: { task_completed: true, provenance_preserved: true, intelligent_block_bound: BLOCK_ID },
      })],
    },
    control: {
      ...control,
      action: "NAYA-NODE-0001-CONTROL-1",
      observed_result: "X",
      evidence: [baseEvidence("CONTROL", {
        retained_intelligence_used: false,
        // Deliberately a DIFFERENT task: the arms are not comparable.
        task_input: { task_id: "SOME-OTHER-TASK" },
        outcome: { task_completed: true, provenance_preserved: false },
      })],
    },
    treatmentOutcome,
    controlOutcome,
  });
  const res = await invoke({ mode: "recover-learning-outcomes", treatment_receipt_id: TREATMENT_ID, control_receipt_id: CONTROL_ID });
  assert.equal(res.status, 409);
  const body = await res.json();
  assert.equal(body.error, "LEARNING_OUTCOME_RECOVERY_PAIR_INVALID");
  assert.equal(body.recomputed.same_task, false);
});
