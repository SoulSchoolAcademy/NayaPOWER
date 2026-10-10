import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { stripTypeScriptTypes } from "node:module";
import { test } from "node:test";
import vm from "node:vm";

// EXECUTED coverage for the WO4 verified-lesson → decision seam.
//
// Before ACT plans, the plan handler must consult verified learning
// (naya-decision-context, previously dead code with zero callers) and merge
// the ACTIVE lesson into the plan's learning context. Causal influence is
// measured by a CONTROLLED INTERVENTION — control plan (no lesson) vs
// treatment plan (lesson applied) — never by the mere presence of a lesson
// (PR #1733: availability ≠ influence). These tests execute the actual seam
// code: buildActPlan with/without a decision context, applyDecisionContextToPlan,
// measureLearningInfluence, and readDecisionContext against a stubbed client.

const DIR = new URL("../supabase/functions/", import.meta.url);
function load(rel) {
  const src = readFileSync(new URL(rel, DIR), "utf8");
  const noImports = src.replace(/^import[\s\S]*?;\r?\n/gm, "");
  const noTypes = stripTypeScriptTypes(noImports);
  let code = noTypes.replace(/^export\s+(default\s+)?/gm, "");
  if (rel.endsWith("nayanet-act-runtime/act.ts")) {
    // Test-harness only: act.ts re-declares the servable sets that know.ts
    // already defines with identical values; drop the duplicates so the
    // concatenated vm scope has one definition.
    code = code
      .replace(/^const SERVABLE_STATUS = new Set\(\["ACTIVE", "DURABLE", "RELEASED"\]\);\r?\n/gm, "")
      .replace(/^const SERVABLE_STATES = new Set\(\["VERIFIED", "DISTILLED", "APPLIED", "LEARNED"\]\);\r?\n/gm, "");
  }
  return code;
}

const sandbox = { console, Date, JSON, RegExp, Array, Object, String, Number, Boolean, Math };
for (const rel of [
  "_shared/connect_selector.ts",
  "nayanet-know-runtime/know.ts",
  "nayanet-act-runtime/decision-context.ts",
  "nayanet-act-runtime/act.ts",
]) {
  vm.runInNewContext(load(rel), sandbox, { filename: rel });
}
const {
  selectKnowContext, buildActPlan, canonicalEqual, measureLearningInfluence,
  applyDecisionContextToPlan, readDecisionContext,
} = sandbox;
// Top-level consts don't attach to the vm sandbox object; read them by evaluation.
const ACT_BASELINE_BEHAVIOR = vm.runInNewContext("ACT_BASELINE_BEHAVIOR", sandbox);
const ACT_PROVENANCE_BEHAVIOR = vm.runInNewContext("ACT_PROVENANCE_BEHAVIOR", sandbox);

const OWNER_ID = "adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const NAYA_ID = "NAYA-NODE-0001";
const GRANT_ID = "grant-wo4-1";
const LAW_RECEIPT_ID = "law-wo4-1";
const KNOW_RECEIPT_ID = "know-wo4-1";
const SELECTION_NOW = "2026-10-09T12:00:00.000Z";
const EVALUATED_AT = "2026-10-09T11:59:00.000Z";

const request = {
  owner_id: OWNER_ID,
  naya_id: NAYA_ID,
  law_receipt_id: LAW_RECEIPT_ID,
  action: "naya_node_apply",
  target: NAYA_ID,
  door_id: "DOOR-AI",
  operation: "apply_retained_intelligence",
};

const lawReceipt = {
  id: LAW_RECEIPT_ID,
  user_id: OWNER_ID,
  action: "law_authority_decision",
  status: "SUCCESS",
  evidence: {
    node_id: "NAYA-KERNEL-LAW",
    law_request: { action: "naya_node_apply", target: NAYA_ID },
    law_decision: {
      status: "AUTHORIZED",
      owner_id: OWNER_ID,
      naya_id: NAYA_ID,
      action: "naya_node_apply",
      target: NAYA_ID,
      evaluated_at: EVALUATED_AT,
      expires_at: null,
      authority_refs: [GRANT_ID],
    },
  },
};

const liveGrant = {
  grant_id: GRANT_ID,
  issuer_id: OWNER_ID,
  subject_id: OWNER_ID,
  actions: ["naya_node_apply"],
  scope: { target: NAYA_ID },
  status: "ACTIVE",
  revoked_at: null,
  expires_at: null,
};

const door = {
  door_id: "DOOR-AI",
  operation: "apply_retained_intelligence",
  authority_action: "naya_node_apply",
  target: NAYA_ID,
  consequential: true,
  max_law_age_seconds: 900,
};

// A KNOW receipt whose replay is honest: the recorded result IS the canonical
// selector output over the (empty) universe at the pinned selection time.
function knowReceipt() {
  const knowReq = {
    owner_id: OWNER_ID,
    naya_id: NAYA_ID,
    task_id: "task-wo4-1",
    task_class: "probe",
    required_capability: "provenance_preservation",
  };
  const result = selectKnowContext(knowReq, [], new Date(SELECTION_NOW));
  assert.equal(result.status, "MISS");
  return {
    id: KNOW_RECEIPT_ID,
    user_id: OWNER_ID,
    action: "know_context_retrieval",
    status: "SUCCESS",
    evidence: {
      schema: "naya.know.receipt.v1",
      node_id: "NAYA-KERNEL-KNOW",
      request: { task_id: "task-wo4-1", task_class: "probe", required_capability: "provenance_preservation" },
      result,
      selection_now: SELECTION_NOW,
      law_receipt_id: LAW_RECEIPT_ID,
      authority_refs: [GRANT_ID],
      caller_selected_block: false,
      retrieval_creates_authority: false,
    },
  };
}

function decisionContext(overrides = {}) {
  return {
    decision: "LEARNING_CONTEXT_AVAILABLE",
    target_id: NAYA_ID,
    learning_context_available: true,
    influenced: false,
    reason: "test",
    context: {
      evidence_id: "evidence-wo4-1",
      level: "E4_TRANSFER",
      claim: "Preserve provenance before applying retained intelligence.",
      source_event_id: "event-wo4-1",
      observed_value: "PROVENANCE_PRESERVED",
      verification_method: "CONTROLLED_INTERVENTION",
      provenance: "VERIFICATION",
    },
    authority: { changed: false, granted: false, source: "existing governance boundary" },
    verification: { evidence_status: "ACTIVE" },
    continuity: { grounded: false, source: "learning_evidence", next_step: "EVALUATE_LEARNING_APPLICABILITY_BEFORE_APPLY" },
    ...overrides,
  };
}

const noContext = {
  decision: "NO_VERIFIED_LEARNING_CONTEXT",
  target_id: NAYA_ID,
  learning_context_available: false,
  influenced: false,
  reason: "test",
  context: { evidence_id: null, level: null, claim: null, source_event_id: null, observed_value: null, verification_method: null, provenance: null },
  authority: { changed: false, granted: false, source: "existing governance boundary" },
  verification: { evidence_status: null },
  continuity: { grounded: false, source: "no_learning_evidence", next_step: "RETRIEVE_VERIFIED_LEARNING_BEFORE_CONTINUATION" },
};

const irrelevantContext = decisionContext({
  context: {
    evidence_id: "evidence-wo4-2",
    level: "E4_TRANSFER",
    claim: "Always compress logs before rotation.",
    source_event_id: "event-wo4-2",
    observed_value: "LOGS_COMPRESSED",
    verification_method: "OBSERVATION",
    provenance: "OBSERVATION",
  },
});

function plan(dc) {
  return buildActPlan(request, lawReceipt, liveGrant, door, knowReceipt(), null, [], new Date("2026-10-09T12:00:01Z"), dc);
}

test("control plan (no lesson) builds READY with baseline behavior and a null decision context", () => {
  const p = plan(null);
  assert.equal(p.status, "READY");
  assert.equal(p.post_retrieval_plan.behavior, ACT_BASELINE_BEHAVIOR);
  assert.equal(p.decision_context, null);
  assert.equal(p.learning_context_applied, false);
  assert.equal(p.learning_prescription, null);
});

test("treatment plan with a relevant ACTIVE lesson steers behavior exactly as the lesson prescribes", () => {
  const control = plan(null);
  const treatment = plan(decisionContext());
  assert.equal(treatment.status, "READY");
  assert.equal(treatment.post_retrieval_plan.behavior, ACT_PROVENANCE_BEHAVIOR);
  assert.notEqual(treatment.post_retrieval_plan.behavior, control.post_retrieval_plan.behavior);
  assert.equal(treatment.learning_context_applied, true);
  assert.equal(treatment.learning_prescription, "PRESERVE_PROVENANCE_BEFORE_APPLY");
  assert.equal(treatment.decision_context.context.evidence_id, "evidence-wo4-1");
  // The lesson never touches authority scope.
  assert.deepEqual(
    { action: treatment.post_retrieval_plan.action, target: treatment.post_retrieval_plan.target },
    { action: control.post_retrieval_plan.action, target: control.post_retrieval_plan.target },
  );
});

test("lesson present but irrelevant: treatment is identical to control (no steering, no false application)", () => {
  const control = plan(null);
  const treatment = plan(irrelevantContext);
  assert.equal(treatment.status, "READY");
  assert.equal(treatment.decision_context.learning_context_available, true);
  assert.equal(treatment.learning_context_applied, false);
  assert.equal(treatment.learning_prescription, null);
  assert.ok(
    canonicalEqual(control.post_retrieval_plan, treatment.post_retrieval_plan),
    "an irrelevant lesson must not move the plan",
  );
});

test("influenced=true ONLY on an observed behavioral delta (relevant lesson)", () => {
  const control = plan(null);
  const treatment = plan(decisionContext());
  const influence = measureLearningInfluence(decisionContext(), control, treatment);
  assert.equal(influence.influenced, true);
  assert.equal(influence.basis, "OBSERVED_BEHAVIORAL_DELTA");
  assert.equal(influence.control_behavior, ACT_BASELINE_BEHAVIOR);
  assert.equal(influence.treatment_behavior, ACT_PROVENANCE_BEHAVIOR);
});

test("influenced=false when the lesson is present but prescribes nothing (the #1733 boundary)", () => {
  const control = plan(null);
  const treatment = plan(irrelevantContext);
  const influence = measureLearningInfluence(irrelevantContext, control, treatment);
  assert.equal(influence.influenced, false, "availability alone is not causal influence");
  assert.equal(influence.basis, "LESSON_PRESENT_NO_PLAN_DELTA");
});

test("influenced=false on the control arm (no ACTIVE lessons)", () => {
  const control = plan(null);
  const influence = measureLearningInfluence(noContext, control, control);
  assert.equal(influence.influenced, false);
  assert.equal(influence.basis, "NO_VERIFIED_LEARNING_CONTEXT");
});

test("influenced=false when an arm is not READY, even with a relevant lesson available", () => {
  const blocked = buildActPlan(request, null, liveGrant, door, knowReceipt(), null, [], new Date(), decisionContext());
  assert.equal(blocked.status, "BLOCKED");
  const treatment = plan(decisionContext());
  const influence = measureLearningInfluence(decisionContext(), blocked, treatment);
  assert.equal(influence.influenced, false);
  assert.equal(influence.basis, "PLANS_NOT_COMPARABLE");
});

test("a relevant lesson cannot rescue a blocked plan or mint authority", () => {
  const blocked = buildActPlan(request, null, liveGrant, door, knowReceipt(), null, [], new Date(), decisionContext());
  assert.equal(blocked.status, "BLOCKED");
  assert.equal(blocked.learning_context_applied, false);
  assert.equal(blocked.decision_context.learning_context_available, true);
});

test("pinned decision context survives a JSON round-trip and replays to an identical plan", () => {
  const treatment = plan(decisionContext());
  const roundTripped = JSON.parse(JSON.stringify(treatment.decision_context));
  const replayed = buildActPlan(request, lawReceipt, liveGrant, door, knowReceipt(), null, [], new Date("2026-10-09T12:00:02Z"), roundTripped);
  assert.ok(canonicalEqual(treatment, replayed), "execute-mode replay must reproduce the stored plan exactly");
});

test("applyDecisionContextToPlan applies nothing without an available context", () => {
  const pre = { action: "a", target: "t", door_id: "d", operation: "o", behavior: ACT_BASELINE_BEHAVIOR };
  for (const dc of [null, noContext]) {
    const r = applyDecisionContextToPlan(pre, { required_capability: "provenance_preservation" }, dc);
    assert.equal(r.applied, false);
    assert.equal(r.plan.behavior, ACT_BASELINE_BEHAVIOR);
  }
});

function stubAdmin({ evidence = null, error = null } = {}) {
  const filters = {};
  const builder = {
    select() { return builder; },
    eq(k, v) { filters[k] = v; return builder; },
    order() { return builder; },
    limit() { return builder; },
    async maybeSingle() { return { data: evidence, error }; },
  };
  return { admin: { from: () => builder }, filters };
}

const evidenceRow = {
  id: "evidence-wo4-9",
  target_id: NAYA_ID,
  level: "E4_TRANSFER",
  status: "ACTIVE",
  claim: "Preserve provenance before applying retained intelligence.",
  observed_value: "PROVENANCE_PRESERVED",
  source_event_id: "event-wo4-9",
  verification_method: "CONTROLLED_INTERVENTION",
  provenance: "VERIFICATION",
  created_at: "2026-10-09T00:00:00Z",
};

test("readDecisionContext returns the repaired shape: available, never influenced, no authority", async () => {
  const { admin, filters } = stubAdmin({ evidence: evidenceRow });
  const dc = await readDecisionContext(admin, OWNER_ID, NAYA_ID);
  assert.equal(dc.decision, "LEARNING_CONTEXT_AVAILABLE");
  assert.equal(dc.learning_context_available, true);
  assert.equal(dc.influenced, false);
  assert.equal(dc.target_id, NAYA_ID);
  assert.equal(dc.context.evidence_id, "evidence-wo4-9");
  assert.equal(dc.context.claim, "Preserve provenance before applying retained intelligence.");
  assert.equal(dc.authority.changed, false);
  assert.equal(dc.authority.granted, false);
  assert.equal(dc.continuity.grounded, false);
  // Owner-scoped ACTIVE boundary, newest first — the endpoint's exact query.
  assert.deepEqual(filters, { member_id: OWNER_ID, target_id: NAYA_ID, status: "ACTIVE" });
});

test("readDecisionContext reports no verified context when no ACTIVE row exists", async () => {
  const { admin } = stubAdmin({ evidence: null });
  const dc = await readDecisionContext(admin, OWNER_ID, NAYA_ID);
  assert.equal(dc.decision, "NO_VERIFIED_LEARNING_CONTEXT");
  assert.equal(dc.learning_context_available, false);
  assert.equal(dc.influenced, false);
  assert.equal(dc.context.evidence_id, null);
});

test("readDecisionContext fails closed on a database error (never a silent no-context)", async () => {
  const { admin } = stubAdmin({ error: { message: "connection reset" } });
  await assert.rejects(() => readDecisionContext(admin, OWNER_ID, NAYA_ID));
});

test("readDecisionContext requires a target", async () => {
  const { admin } = stubAdmin({ evidence: evidenceRow });
  await assert.rejects(() => readDecisionContext(admin, OWNER_ID, "   "), /TARGET/);
});
