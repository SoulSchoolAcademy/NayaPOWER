import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import { test } from 'node:test';
import vm from 'node:vm';

const source = readFileSync(new URL('../supabase/functions/nayanet-causal-learning-experiment/index.ts', import.meta.url), 'utf8');
const code = stripTypeScriptTypes(source.replace(/^import[\s\S]*?;\r?\n/gm, ''));

const OWNER_ID = 'adfdf0b8-5558-41d1-9fed-ec51abf4fe2f';
const NAYA_ID = 'NAYA-NODE-0001';
const LEARNING_ID = 'active-learning-id';
const BLOCK_ID = 'IB-NAYA-FLOW-LESSON-ACTIVE-001';
const LESSON = 'Preserve provenance before applying retained intelligence.';
const RELATED = 'NAYA-0001-PROVENANCE-HELDOUT-002';
const UNRELATED = 'NAYA-0001-UNRELATED-ARITHMETIC-001';

function taskInput(taskId, taskClass, instruction) {
  return { task_id: taskId, task_class: taskClass, instruction, target_id: NAYA_ID };
}

const relatedInput = taskInput(
  RELATED,
  'RELATED_HELDOUT',
  'Transform a retained intelligence record for a successor handoff while preserving the exact authoritative source lineage.',
);
const unrelatedInput = taskInput(
  UNRELATED,
  'UNRELATED_NEGATIVE_TRANSFER',
  'Compute 7 + 5 and report the result.',
);

function makeReceipts({ tamperRelatedOutcome = false, forceUnrelatedTransfer = false } = {}) {
  const common = { user_id: OWNER_ID, project_id: 'NayaNET', status: 'SUCCESS' };
  const relatedControl = {
    ...common, id: 'r-control', observed_result: 'REQUIRE_DIRECT_CANONICAL_INTELLIGENCE',
    evidence: {
      experiment: 'ACTIVE_LEARNING_GENERALIZATION_V1', condition: 'CONTROL', learning_id: LEARNING_ID,
      retained_intelligence_available: false, retained_intelligence_applied: false,
      source_event_id: 'event-active-1', task_input: relatedInput,
      applicability: { required_capability: 'provenance_preservation', learning_capabilities: ['provenance_preservation'], applicable: false },
      behavior: 'REQUIRE_DIRECT_CANONICAL_INTELLIGENCE',
      outcome: { task_completed: true, provenance_preserved: false, source_event_bound: null, intelligent_block_bound: null },
    },
  };
  const relatedTreatment = {
    ...common, id: 'r-treatment', observed_result: 'PRESERVE_PROVENANCE_BEFORE_APPLY',
    evidence: {
      experiment: 'ACTIVE_LEARNING_GENERALIZATION_V1', condition: 'TREATMENT', learning_id: LEARNING_ID,
      retained_intelligence_available: true, retained_intelligence_applied: true, intelligence_id: BLOCK_ID,
      source_event_id: 'event-active-1', task_input: relatedInput,
      applicability: { required_capability: 'provenance_preservation', learning_capabilities: ['provenance_preservation'], applicable: true },
      behavior: 'PRESERVE_PROVENANCE_BEFORE_APPLY',
      outcome: {
        task_completed: true,
        provenance_preserved: tamperRelatedOutcome ? false : true,
        source_event_bound: 'event-active-1',
        intelligent_block_bound: BLOCK_ID,
      },
    },
  };
  const unrelatedControl = {
    ...common, id: 'u-control', observed_result: 'NO_APPLICABLE_RETAINED_INTELLIGENCE',
    evidence: {
      experiment: 'ACTIVE_LEARNING_GENERALIZATION_V1', condition: 'CONTROL', learning_id: LEARNING_ID,
      retained_intelligence_available: false, retained_intelligence_applied: false,
      source_event_id: 'event-active-1', task_input: unrelatedInput,
      applicability: { required_capability: 'arithmetic_only', learning_capabilities: ['provenance_preservation'], applicable: false },
      behavior: 'NO_APPLICABLE_RETAINED_INTELLIGENCE',
      outcome: { task_completed: true, answer: 12, provenance_preserved: null },
    },
  };
  const unrelatedTreatmentBehavior = forceUnrelatedTransfer
    ? 'PRESERVE_PROVENANCE_BEFORE_APPLY'
    : 'NO_APPLICABLE_RETAINED_INTELLIGENCE';
  const unrelatedTreatment = {
    ...common, id: 'u-treatment', observed_result: unrelatedTreatmentBehavior,
    evidence: {
      experiment: 'ACTIVE_LEARNING_GENERALIZATION_V1', condition: 'TREATMENT', learning_id: LEARNING_ID,
      retained_intelligence_available: true,
      retained_intelligence_applied: forceUnrelatedTransfer,
      intelligence_id: BLOCK_ID,
      source_event_id: 'event-active-1', task_input: unrelatedInput,
      applicability: {
        required_capability: 'arithmetic_only',
        learning_capabilities: ['provenance_preservation'],
        applicable: forceUnrelatedTransfer,
      },
      behavior: unrelatedTreatmentBehavior,
      outcome: forceUnrelatedTransfer
        ? { task_completed: true, answer: 12, provenance_preserved: true }
        : { task_completed: true, answer: 12, provenance_preserved: null },
    },
  };
  return [relatedControl, relatedTreatment, unrelatedControl, unrelatedTreatment];
}

function runtime(options = {}) {
  let handler;
  const requestedReceipts = makeReceipts(options);
  const requestedReceiptIds = requestedReceipts.map(r => r.id);
  if (options.noRelatedEffect) {
    const treatment = requestedReceipts[1];
    treatment.observed_result = 'REQUIRE_DIRECT_CANONICAL_INTELLIGENCE';
    treatment.evidence.behavior = 'REQUIRE_DIRECT_CANONICAL_INTELLIGENCE';
    treatment.evidence.retained_intelligence_applied = false;
    treatment.evidence.applicability.applicable = false;
    treatment.evidence.outcome.provenance_preserved = false;
  }
  if (options.mismatchedRelatedTask) {
    requestedReceipts[1].evidence.task_input = { ...relatedInput, instruction: 'Different task input.' };
  }
  if (options.mismatchedLearningId) requestedReceipts[1].evidence.learning_id = 'other-learning-id';
  if (options.mismatchedBlockId) requestedReceipts[1].evidence.intelligence_id = 'IB-OTHER';
  if (options.forgedExecutorPass) {
    requestedReceipts[1].evidence.executor_claim = {
      ok: true, related_causal_supported: true, negative_transfer_refused: true,
    };
  }
  const receipts = options.missingReceipt ? requestedReceipts.slice(0, 3) : requestedReceipts;
  const grants = options.missingAuthority ? [] : [{
    grant_id: 'grant-1', issuer_id: OWNER_ID, subject_id: OWNER_ID,
    mission_id: 'NAYA-NODE-0001-CONTINUITY', scope: { target: NAYA_ID },
    actions: ['naya_node_apply'], status: 'ACTIVE',
  }];
  const learning = {
    id: LEARNING_ID, target_id: NAYA_ID, level: 'E5_CAN_TEACH', status: options.learningStatus ?? 'ACTIVE',
    claim: LESSON, source_event_id: 'event-active-1',
    observed_value: { intelligent_block_id: BLOCK_ID, behavioral_change: true },
    verification_method: 'independent causal verification', provenance: 'OBSERVATION',
  };
  const block = {
    intelligent_block_id: BLOCK_ID, owner_id: OWNER_ID, understanding_state: 'LEARNED',
    content: { lesson: LESSON }, provenance: { source: 'event-active-1' },
  };

  function query(data) {
    const q = {
      select: () => q,
      eq: () => q,
      in: () => q,
      maybeSingle: async () => ({ data: Array.isArray(data) ? data[0] ?? null : data, error: null }),
      then: resolve => resolve({ data, error: null }),
    };
    return q;
  }

  const admin = {
    from(table) {
      if (table === 'nayanet_authority_grants') return query(grants);
      if (table === 'learning_evidence') return query(learning);
      if (table === 'nayanet_intelligent_blocks') return query(block);
      if (table === 'nayanet_execution_receipts') return query(receipts);
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
      jti: 'generalization-verifier-jti',
    } }),
    createClient: () => admin,
  });

  return {
    invoke: (body = {}) => handler(new Request('https://offline.invalid', {
      method: 'POST',
      headers: { authorization: 'Bearer test', 'content-type': 'application/json' },
      body: JSON.stringify({
        mode: 'verify-generalization',
        learning_id: LEARNING_ID,
        receipt_ids: requestedReceiptIds,
        ...body,
      }),
    })),
  };
}

test('independent generalization verifier recomputes related improvement and unrelated refusal', async () => {
  const response = await runtime().invoke();
  assert.equal(response.status, 200);
  const body = await response.json();
  assert.equal(body.ok, true);
  assert.equal(body.independent_verification, true);
  assert.equal(body.executor_claim_trusted, false);
  assert.equal(body.recomputed.related_causal_supported, true);
  assert.equal(body.recomputed.related_behavior_delta, true);
  assert.equal(body.recomputed.related_outcome_delta.metric, 'provenance_preserved');
  assert.equal(body.recomputed.related_outcome_delta.value, 1);
  assert.equal(body.recomputed.negative_transfer_refused, true);
  assert.equal(body.recomputed.unrelated_behavior_delta, false);
  assert.equal(body.recomputed.unrelated_outcome_stable, true);
});

test('independent generalization verifier rejects a related causal claim with no measured outcome improvement', async () => {
  const response = await runtime({ tamperRelatedOutcome: true }).invoke();
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.ok, false);
  assert.equal(body.recomputed.related_causal_supported, false);
  assert.equal(body.recomputed.related_outcome_delta.value, 0);
});

test('independent generalization verifier rejects negative transfer into an unrelated task', async () => {
  const response = await runtime({ forceUnrelatedTransfer: true }).invoke();
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.ok, false);
  assert.equal(body.recomputed.negative_transfer_refused, false);
  assert.equal(body.recomputed.unrelated_behavior_delta, true);
});

test('independent generalization verifier rejects answer-content injection', async () => {
  const response = await runtime().invoke({ lesson: LESSON });
  assert.equal(response.status, 400);
  const body = await response.json();
  assert.equal(body.error, 'INTELLIGENCE_CONTENT_INPUT_FORBIDDEN');
});

test('independent generalization verifier ignores a forged executor causal PASS when persisted outcome evidence fails', async () => {
  const response = await runtime({ tamperRelatedOutcome: true, forgedExecutorPass: true }).invoke({
    executor_claim: { ok: true, related_causal_supported: true, negative_transfer_refused: true },
  });
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.ok, false);
  assert.equal(body.independent_verification, false);
  assert.equal(body.executor_claim_trusted, false);
  assert.equal(body.recomputed.related_causal_supported, false);
});

test('independent generalization verifier rejects a missing persisted receipt', async () => {
  const response = await runtime({ missingReceipt: true }).invoke();
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.error, 'GENERALIZATION_RECEIPTS_NOT_UNIQUE');
  assert.equal(body.count, 3);
});

test('independent generalization verifier rejects mismatched related task inputs', async () => {
  const response = await runtime({ mismatchedRelatedTask: true }).invoke();
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.ok, false);
  assert.equal(body.recomputed.related_same_task_input, false);
  assert.equal(body.recomputed.related_causal_supported, false);
});

test('independent generalization verifier rejects mismatched learning identity in persisted receipts', async () => {
  const response = await runtime({ mismatchedLearningId: true }).invoke();
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.ok, false);
  assert.equal(body.recomputed.all_same_learning, false);
  assert.equal(body.recomputed.related_causal_supported, false);
});

test('independent generalization verifier rejects mismatched Intelligent Block identity', async () => {
  const response = await runtime({ mismatchedBlockId: true }).invoke();
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.ok, false);
  assert.equal(body.recomputed.related_causal_supported, false);
});

test('independent generalization verifier rejects a no-effect related treatment', async () => {
  const response = await runtime({ noRelatedEffect: true }).invoke();
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.ok, false);
  assert.equal(body.recomputed.related_behavior_delta, false);
  assert.equal(body.recomputed.related_outcome_delta.value, 0);
  assert.equal(body.recomputed.related_causal_supported, false);
});

test('independent generalization verifier fails closed for non-ACTIVE learning', async () => {
  const response = await runtime({ learningStatus: 'CANDIDATE' }).invoke();
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.error, 'ACTIVE_LEARNING_REQUIRED');
  assert.equal(body.status, 'CANDIDATE');
});

test('independent generalization verifier independently requires current authority binding', async () => {
  const response = await runtime({ missingAuthority: true }).invoke();
  assert.equal(response.status, 403);
  const body = await response.json();
  assert.equal(body.error, 'AUTHORIZATION_BINDING_INVALID');
  assert.equal(body.count, 0);
});
