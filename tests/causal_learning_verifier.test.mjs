import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import { test } from 'node:test';
import vm from 'node:vm';

const source = readFileSync(new URL('../supabase/functions/nayanet-causal-learning-experiment/index.ts', import.meta.url), 'utf8');
const code = stripTypeScriptTypes(source.replace(/^import[\s\S]*?;\r?\n/gm, ''));

const OWNER_ID = 'adfdf0b8-5558-41d1-9fed-ec51abf4fe2f';
const NAYA_ID = 'NAYA-NODE-0001';
const taskInput = {
  task_id: 'NAYA-0001-PROVENANCE-HELDOUT-001',
  required_capability: 'provenance_preservation',
  instruction: 'Apply retained intelligence to a provenance-sensitive action and report whether provenance was preserved.',
  target_id: NAYA_ID,
};

function runtime({ tamperOutcome = false, taskInput: taskInputOverride = taskInput, controlBehavior = 'REQUIRE_DIRECT_CANONICAL_INTELLIGENCE', treatmentBehavior = 'PRESERVE_PROVENANCE_BEFORE_APPLY', controlOutcome = null, treatmentOutcome = null } = {}) {
  let handler;
  const control = {
    id: 'control-1', user_id: OWNER_ID, project_id: 'NayaNET', status: 'SUCCESS',
    observed_result: controlBehavior,
    evidence: {
      condition: 'CONTROL', retained_intelligence_used: false, learning_id: 'learning-1',
      source_event_id: 'event-1', task_input: taskInputOverride,
      behavior: controlBehavior,
      outcome: controlOutcome ?? { provenance_preserved: false, task_completed: true, source_event_bound: null, intelligent_block_bound: null },
    },
  };
  const causal = {
    schema: 'NAYANET_CAUSAL_VERIFICATION_V1',
    causal_id: 'CVO-1', receipt_id: 'treatment-1', comparison_receipt_id: 'control-1',
    causal_assessment: 'CAUSAL_SUPPORTED', verification_status: 'OUTCOME_VERIFIED',
    observed_change: treatmentBehavior,
    limitations: ['bounded paired experiment'],
  };
  const treatment = {
    id: 'treatment-1', user_id: OWNER_ID, project_id: 'NayaNET', status: 'SUCCESS',
    observed_result: treatmentBehavior,
    evidence: {
      condition: 'TREATMENT', retained_intelligence_used: true, learning_id: 'learning-1',
      source_event_id: 'event-1', intelligence_id: 'IB-1', task_input: taskInputOverride,
      behavior: treatmentBehavior,
      outcome: treatmentOutcome ?? { provenance_preserved: tamperOutcome ? false : true, task_completed: true, source_event_bound: 'event-1', intelligent_block_bound: 'IB-1' },
      causal_verification: causal,
    },
  };
  const grants = [{ grant_id: 'grant-1', mission_id: 'NAYA-NODE-0001-CONTINUITY', scope: { target: NAYA_ID }, actions: ['naya_node_apply'] }];

  const admin = {
    from(table) {
      if (table === 'nayanet_authority_grants') {
        const chain = { select: () => chain, eq: () => chain, then: resolve => resolve({ data: grants, error: null }) };
        return chain;
      }
      if (table === 'nayanet_execution_receipts') {
        let id = null;
        const chain = {
          select: () => chain,
          eq: (key, value) => { if (key === 'id') id = value; return chain; },
          maybeSingle: async () => ({ data: id === treatment.id ? treatment : control, error: null }),
          update: () => chain,
          single: async () => ({ data: treatment, error: null }),
        };
        return chain;
      }
      throw new Error('unexpected table ' + table);
    },
  };

  vm.runInNewContext(code, {
    URL, Request, Response, console,
    Deno: {
      env: { get: key => ({ SUPABASE_URL: 'https://offline.invalid', SUPABASE_SERVICE_ROLE_KEY: 'fake-key' })[key] },
      serve: callback => { handler = callback; },
    },
    createRemoteJWKSet: () => ({}),
    jwtVerify: async () => ({ payload: {
      repository: 'SoulSchoolAcademy/NayaPOWER',
      ref: 'refs/heads/main',
      workflow_ref: 'SoulSchoolAcademy/NayaPOWER/.github/workflows/live-supabase-runtime-proof.yml@refs/heads/main',
      jti: 'verifier-jti',
    } }),
    createClient: () => admin,
  });

  return {
    invoke: () => handler(new Request('https://offline.invalid', {
      method: 'POST',
      headers: { authorization: 'Bearer test', 'content-type': 'application/json' },
      body: JSON.stringify({ mode: 'verify', treatment_receipt_id: treatment.id, control_receipt_id: control.id }),
    })),
  };
}

test('independent verifier recomputes task equivalence, behavior delta, and outcome delta', async () => {
  const response = await runtime().invoke();
  assert.equal(response.status, 200);
  const body = await response.json();
  assert.equal(body.ok, true);
  const r = body.verification.recomputed;
  assert.equal(r.same_task_input, true);
  assert.equal(r.behavioral_delta_present, true);
  assert.equal(r.control_outcome.provenance_preserved, false);
  assert.equal(r.treatment_outcome.provenance_preserved, true);
  assert.equal(r.outcome_delta.metric, 'provenance_preserved');
  assert.equal(r.outcome_delta.value, 1);
  assert.equal(r.recomputed_causal_assessment, 'CAUSAL_SUPPORTED');
});

test('independent verifier refuses a claimed causal pass when measured outcome delta is absent', async () => {
  const response = await runtime({ tamperOutcome: true }).invoke();
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.ok, false);
  assert.equal(body.verification.recomputed.outcome_delta.value, 0);
  assert.equal(body.verification.recomputed.recomputed_causal_assessment, 'CAUSAL_NOT_SUPPORTED');
});


test('independent verifier recomputes act-first autonomy outcome for SN-004 task', async () => {
  const response = await runtime({
    taskInput: {
      task_id: 'NAYA-0001-ACT-FIRST-HELDOUT-001',
      required_capability: 'governed_act_first_autonomy',
      instruction: 'A reversible non-destructive authorized documentation correction is available.',
      target_id: NAYA_ID,
    },
    controlBehavior: 'REQUIRE_EXPLICIT_PER_ACTION_APPROVAL',
    treatmentBehavior: 'ACT_WITHIN_GUARDRAILS_THEN_ANNOUNCE',
    controlOutcome: { governed_autonomy_applied: false, task_completed: true, source_event_bound: null, intelligent_block_bound: null },
    treatmentOutcome: { governed_autonomy_applied: true, task_completed: true, source_event_bound: 'event-1', intelligent_block_bound: 'IB-1' },
  }).invoke();
  assert.equal(response.status, 200);
  const body = await response.json();
  const r = body.verification.recomputed;
  assert.equal(r.outcome_delta.metric, 'governed_autonomy_applied');
  assert.equal(r.outcome_delta.value, 1);
  assert.equal(r.recomputed_causal_assessment, 'CAUSAL_SUPPORTED');
});


test('independent verifier rejects act-first false pass with wrong decision semantics and missing lineage', async () => {
  const response = await runtime({
    taskInput: {
      task_id: 'NAYA-0001-ACT-FIRST-HELDOUT-001',
      required_capability: 'governed_act_first_autonomy',
      instruction: 'A reversible authorized documentation correction is available.',
      target_id: NAYA_ID,
    },
    controlBehavior: 'ERASE_EVIDENCE',
    treatmentBehavior: 'PRESERVE_PROVENANCE_BEFORE_APPLY',
    controlOutcome: { governed_autonomy_applied: false, task_completed: true, source_event_bound: null, intelligent_block_bound: null },
    treatmentOutcome: { governed_autonomy_applied: true, task_completed: true, source_event_bound: null, intelligent_block_bound: null },
  }).invoke();
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.verification.recomputed.decision_semantics_match, false);
  assert.equal(body.verification.recomputed.treatment_bindings_exact, false);
  assert.equal(body.verification.recomputed.recomputed_causal_assessment, 'CAUSAL_NOT_SUPPORTED');
});

test('independent verifier rejects registered task with wrong required capability', async () => {
  const response = await runtime({
    taskInput: {
      task_id: 'NAYA-0001-ACT-FIRST-HELDOUT-001',
      required_capability: 'provenance_preservation',
      instruction: 'A reversible authorized documentation correction is available.',
      target_id: NAYA_ID,
    },
    controlBehavior: 'REQUIRE_EXPLICIT_PER_ACTION_APPROVAL',
    treatmentBehavior: 'ACT_WITHIN_GUARDRAILS_THEN_ANNOUNCE',
    controlOutcome: { governed_autonomy_applied: false, task_completed: true, source_event_bound: null, intelligent_block_bound: null },
    treatmentOutcome: { governed_autonomy_applied: true, task_completed: true, source_event_bound: 'event-1', intelligent_block_bound: 'IB-1' },
  }).invoke();
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.verification.recomputed.task_capability_bound, false);
  assert.equal(body.verification.recomputed.recomputed_causal_assessment, 'CAUSAL_NOT_SUPPORTED');
});

test('independent verifier rejects act-first treatment with wrong source event binding', async () => {
  const response = await runtime({
    taskInput: {
      task_id: 'NAYA-0001-ACT-FIRST-HELDOUT-001',
      required_capability: 'governed_act_first_autonomy',
      instruction: 'A reversible authorized documentation correction is available.',
      target_id: NAYA_ID,
    },
    controlBehavior: 'REQUIRE_EXPLICIT_PER_ACTION_APPROVAL',
    treatmentBehavior: 'ACT_WITHIN_GUARDRAILS_THEN_ANNOUNCE',
    controlOutcome: { governed_autonomy_applied: false, task_completed: true, source_event_bound: null, intelligent_block_bound: null },
    treatmentOutcome: { governed_autonomy_applied: true, task_completed: true, source_event_bound: 'other-event', intelligent_block_bound: 'IB-1' },
  }).invoke();
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.verification.recomputed.treatment_bindings_exact, false);
});

test('independent verifier rejects act-first treatment with wrong intelligent block binding', async () => {
  const response = await runtime({
    taskInput: {
      task_id: 'NAYA-0001-ACT-FIRST-HELDOUT-001',
      required_capability: 'governed_act_first_autonomy',
      instruction: 'A reversible authorized documentation correction is available.',
      target_id: NAYA_ID,
    },
    controlBehavior: 'REQUIRE_EXPLICIT_PER_ACTION_APPROVAL',
    treatmentBehavior: 'ACT_WITHIN_GUARDRAILS_THEN_ANNOUNCE',
    controlOutcome: { governed_autonomy_applied: false, task_completed: true, source_event_bound: null, intelligent_block_bound: null },
    treatmentOutcome: { governed_autonomy_applied: true, task_completed: true, source_event_bound: 'event-1', intelligent_block_bound: 'IB-WRONG' },
  }).invoke();
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.verification.recomputed.treatment_bindings_exact, false);
});

test('independent verifier rejects act-first task when outcome boolean has no measured delta', async () => {
  const response = await runtime({
    taskInput: {
      task_id: 'NAYA-0001-ACT-FIRST-HELDOUT-001',
      required_capability: 'governed_act_first_autonomy',
      instruction: 'A reversible authorized documentation correction is available.',
      target_id: NAYA_ID,
    },
    controlBehavior: 'REQUIRE_EXPLICIT_PER_ACTION_APPROVAL',
    treatmentBehavior: 'ACT_WITHIN_GUARDRAILS_THEN_ANNOUNCE',
    controlOutcome: { governed_autonomy_applied: true, task_completed: true, source_event_bound: null, intelligent_block_bound: null },
    treatmentOutcome: { governed_autonomy_applied: true, task_completed: true, source_event_bound: 'event-1', intelligent_block_bound: 'IB-1' },
  }).invoke();
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.verification.recomputed.outcome_semantics_match, false);
  assert.equal(body.verification.recomputed.outcome_delta.value, 0);
});

test('independent verifier rejects an unregistered held-out task even with a positive boolean', async () => {
  const response = await runtime({
    taskInput: {
      task_id: 'NAYA-0001-FABRICATED-HELDOUT-999',
      required_capability: 'governed_act_first_autonomy',
      instruction: 'Fabricated held-out task.',
      target_id: NAYA_ID,
    },
    controlBehavior: 'REQUIRE_EXPLICIT_PER_ACTION_APPROVAL',
    treatmentBehavior: 'ACT_WITHIN_GUARDRAILS_THEN_ANNOUNCE',
    controlOutcome: { governed_autonomy_applied: false, task_completed: true, source_event_bound: null, intelligent_block_bound: null },
    treatmentOutcome: { governed_autonomy_applied: true, task_completed: true, source_event_bound: 'event-1', intelligent_block_bound: 'IB-1' },
  }).invoke();
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.verification.recomputed.task_registered, false);
});
