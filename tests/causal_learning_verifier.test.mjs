import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import { test } from 'node:test';
import vm from 'node:vm';

const source = readFileSync(new URL('../supabase/functions/nayanet-causal-learning-experiment/index.ts', import.meta.url), 'utf8');
const code = stripTypeScriptTypes(source.replace(/^import .*;\r?\n/gm, ''));

const OWNER_ID = 'adfdf0b8-5558-41d1-9fed-ec51abf4fe2f';
const NAYA_ID = 'NAYA-NODE-0001';
const taskInput = {
  task_id: 'NAYA-0001-PROVENANCE-HELDOUT-001',
  instruction: 'Apply retained intelligence to a provenance-sensitive action and report whether provenance was preserved.',
  target_id: NAYA_ID,
};

function runtime({ tamperOutcome = false } = {}) {
  let handler;
  const control = {
    id: 'control-1', user_id: OWNER_ID, project_id: 'NayaNET', status: 'SUCCESS',
    observed_result: 'REQUIRE_DIRECT_CANONICAL_INTELLIGENCE',
    evidence: {
      condition: 'CONTROL', retained_intelligence_used: false, learning_id: 'learning-1',
      source_event_id: 'event-1', task_input: taskInput,
      behavior: 'REQUIRE_DIRECT_CANONICAL_INTELLIGENCE',
      outcome: { provenance_preserved: false, task_completed: true },
    },
  };
  const causal = {
    schema: 'NAYANET_CAUSAL_VERIFICATION_V1',
    causal_id: 'CVO-1', receipt_id: 'treatment-1', comparison_receipt_id: 'control-1',
    causal_assessment: 'CAUSAL_SUPPORTED', verification_status: 'OUTCOME_VERIFIED',
    observed_change: 'PRESERVE_PROVENANCE_BEFORE_APPLY',
    limitations: ['bounded paired experiment'],
  };
  const treatment = {
    id: 'treatment-1', user_id: OWNER_ID, project_id: 'NayaNET', status: 'SUCCESS',
    observed_result: 'PRESERVE_PROVENANCE_BEFORE_APPLY',
    evidence: {
      condition: 'TREATMENT', retained_intelligence_used: true, learning_id: 'learning-1',
      source_event_id: 'event-1', intelligence_id: 'IB-1', task_input: taskInput,
      behavior: 'PRESERVE_PROVENANCE_BEFORE_APPLY',
      outcome: { provenance_preserved: tamperOutcome ? false : true, task_completed: true },
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
  assert.equal(r.outcome_delta.provenance_preserved, 1);
  assert.equal(r.recomputed_causal_assessment, 'CAUSAL_SUPPORTED');
});

test('independent verifier refuses a claimed causal pass when measured outcome delta is absent', async () => {
  const response = await runtime({ tamperOutcome: true }).invoke();
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.ok, false);
  assert.equal(body.verification.recomputed.outcome_delta.provenance_preserved, 0);
  assert.equal(body.verification.recomputed.recomputed_causal_assessment, 'CAUSAL_NOT_SUPPORTED');
});
