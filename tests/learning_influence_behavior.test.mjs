import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import { test } from 'node:test';
import vm from 'node:vm';

const source = readFileSync(new URL('../supabase/functions/nayanet-cold-runtime-proof/index.ts', import.meta.url), 'utf8');
const code = stripTypeScriptTypes(source.replace(/^import .*;\r?\n/gm, ''));

const OWNER_ID = 'adfdf0b8-5558-41d1-9fed-ec51abf4fe2f';
const NAYA_ID = 'NAYA-NODE-0001';
const BLOCK_ID = 'IB-NAYA-NODE-0001-0001';
const FRESH_BLOCK_ID = 'IB-NAYA-FLOW-LESSON-FRESH-001';
const LEARNING_ID = 'test-learning-id';
const claims = {
  repository: 'SoulSchoolAcademy/NayaPOWER',
  ref: 'refs/heads/main',
  workflow_ref: 'SoulSchoolAcademy/NayaPOWER/.github/workflows/live-supabase-runtime-proof.yml@refs/heads/main',
  jti: 'test-runtime-jti',
};

function runtime({ lesson = 'Preserve provenance before applying retained intelligence.' } = {}) {
  let handler;
  let receiptId = 0;
  let revision = 10;
  const learning = {
    id: LEARNING_ID, target_id: NAYA_ID, level: 'E1_UNDERSTANDS', status: 'CANDIDATE',
    claim: lesson, source_event_id: 'event-1',
    observed_value: { intelligent_block_id: FRESH_BLOCK_ID, provenance_preserved: true },
    verification_method: 'pending', provenance: 'OBSERVATION',
  };
  const admin = {
    from(table) {
      assert.equal(table, 'nayanet_execution_receipts');
      return {
        insert(row) {
          return { select() { return { async single() {
            receiptId += 1;
            return { data: { ...row, id: `receipt-${receiptId}` }, error: null };
          } }; } };
        },
      };
    },
  };

  vm.runInNewContext(code, {
    URL, Request, Response, console,
    Deno: {
      env: { get: key => ({ SUPABASE_URL: 'https://offline.invalid', SUPABASE_SERVICE_ROLE_KEY: 'fake-key' })[key] },
      serve: callback => { handler = callback; },
    },
    createRemoteJWKSet: () => ({}),
    jwtVerify: async () => ({ payload: claims }),
    createClient: () => admin,
    fetch: async (url, options = {}) => {
      const u = String(url);
      if (u.includes('/rest/v1/nayanet_intelligent_blocks?')) {
        const fresh = u.includes(encodeURIComponent(FRESH_BLOCK_ID)) || u.includes(FRESH_BLOCK_ID);
        return new Response(JSON.stringify([{
          intelligent_block_id: fresh ? FRESH_BLOCK_ID : BLOCK_ID,
          owner_id: OWNER_ID,
          understanding_state: 'CANDIDATE',
          content: { lesson },
          evidence_refs: [],
        }]), { status: 200 });
      }
      if (u.includes('/rest/v1/nayanet_authority_grants?')) {
        return new Response(JSON.stringify([{ grant_id: 'grant-1', scope: { target: NAYA_ID }, actions: ['naya_node_apply'], status: 'ACTIVE' }]), { status: 200 });
      }
      if (u.includes('/rest/v1/learning_evidence?') && (options.method ?? 'GET') === 'GET') {
        return new Response(JSON.stringify([learning]), { status: 200 });
      }
      if (u.includes('/rest/v1/nayanet_execution_receipts?')) {
        revision += 1;
        return new Response(JSON.stringify([{ revision }]), { status: 200 });
      }
      if (u.includes('/rest/v1/learning_evidence?') && options.method === 'PATCH') {
        return new Response(JSON.stringify([learning]), { status: 200 });
      }
      throw new Error(`unexpected fetch: ${u}`);
    },
  });

  return {
    invoke: () => handler(new Request('https://offline.invalid?mode=learning-influence', {
      method: 'POST',
      headers: { authorization: 'Bearer test', 'content-type': 'application/json' },
      body: JSON.stringify({ learning_id: LEARNING_ID }),
    })),
  };
}

test('learning influence computes behavior and measurable outcome from one bounded task', async () => {
  const response = await runtime().invoke();
  assert.equal(response.status, 200);
  const body = await response.json();
  assert.equal(body.counterfactual.task_id, 'NAYA-0001-PROVENANCE-HELDOUT-001');
  assert.deepEqual(body.control.evidence.task_input, body.treatment.evidence.task_input);
  assert.equal(body.control.evidence.outcome.provenance_preserved, false);
  assert.equal(body.treatment.evidence.outcome.provenance_preserved, true);
  assert.notDeepEqual(body.control.evidence.behavior, body.treatment.evidence.behavior);
  assert.equal(body.behavioral_delta.changed, true);
  assert.equal(body.outcome_delta.metric, 'provenance_preserved');
  assert.equal(body.outcome_delta.value, 1);
  assert.equal(body.treatment.evidence.outcome.source_event_bound, "event-1");
  assert.equal(body.treatment.evidence.outcome.intelligent_block_bound, FRESH_BLOCK_ID);
  assert.equal(body.counterfactual.computed_not_declared, true);
  assert.equal(body.treatment.evidence.intelligence_id, FRESH_BLOCK_ID);
  assert.equal(body.intelligence_applied.intelligent_block_id, FRESH_BLOCK_ID);
  assert.equal(body.intelligence_applied.claim_matches_block, true);
});

test('learning influence refuses causal success when retrieved intelligence causes no measured change', async () => {
  const response = await runtime({ lesson: 'A lesson with no relevant instruction.' }).invoke();
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.error, 'NO_MEASURED_LEARNING_EFFECT');
  assert.equal(body.behavioral_delta.changed, false);
  assert.equal(body.outcome_delta.value, 0);
});


const SN004_LESSON = JSON.stringify({
  machine_view: {
    operating_mode: 'act-first within guardrails; announce after; document everything',
    permitted_without_per_action_approval: [
      'repository reads, tests, verification',
      'documentation and evidence recording',
    ],
    hard_boundaries_require_explicit_authorization: [
      'production deployment/dispatch',
      'destructive or irreversible actions',
      'credentials / money movement',
      'constitutional ratification or amendment',
    ],
  },
  human_view: {
    simple_rule: 'See what needs doing, check it is safe and within guardrails, do it, then tell everyone.',
  },
});

test('SN-004 does not pass the provenance held-out by accidental retrieval alone', async () => {
  const response = await runtime({ lesson: JSON.stringify({ human_view: { simple_rule: 'act when useful' } }) }).invoke();
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.error, 'NO_MEASURED_LEARNING_EFFECT');
  assert.equal(body.counterfactual.task_id, 'NAYA-0001-NO-APPLICABLE-CAPABILITY');
  assert.equal(body.behavioral_delta.changed, false);
});

test('SN-004 semantics select the fixed act-first held-out task and measurable autonomy outcome', async () => {
  const response = await runtime({ lesson: SN004_LESSON }).invoke();
  assert.equal(response.status, 200);
  const body = await response.json();
  assert.equal(body.counterfactual.task_id, 'NAYA-0001-ACT-FIRST-HELDOUT-001');
  assert.equal(body.counterfactual.required_capability, 'governed_act_first_autonomy');
  assert.deepEqual(body.control.evidence.task_input, body.treatment.evidence.task_input);
  assert.equal(body.control.evidence.behavior, 'REQUIRE_EXPLICIT_PER_ACTION_APPROVAL');
  assert.equal(body.treatment.evidence.behavior, 'ACT_WITHIN_GUARDRAILS_THEN_ANNOUNCE');
  assert.equal(body.control.evidence.outcome.governed_autonomy_applied, false);
  assert.equal(body.treatment.evidence.outcome.governed_autonomy_applied, true);
  assert.equal(body.outcome_delta.metric, 'governed_autonomy_applied');
  assert.equal(body.outcome_delta.value, 1);
  assert.equal(body.treatment.evidence.outcome.source_event_bound, 'event-1');
  assert.equal(body.treatment.evidence.outcome.intelligent_block_bound, FRESH_BLOCK_ID);
});

test('SN-004 classification fails closed when hard-boundary semantics are missing', async () => {
  const weak = JSON.stringify({
    machine_view: {
      operating_mode: 'act-first within guardrails; announce after; document everything',
      permitted_without_per_action_approval: [
        'repository reads, tests, verification',
        'documentation and evidence recording',
      ],
      hard_boundaries_require_explicit_authorization: [],
    },
  });
  const response = await runtime({ lesson: weak }).invoke();
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.error, 'NO_MEASURED_LEARNING_EFFECT');
  assert.equal(body.counterfactual.task_id, 'NAYA-0001-NO-APPLICABLE-CAPABILITY');
});
