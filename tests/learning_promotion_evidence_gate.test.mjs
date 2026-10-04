import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import { test } from 'node:test';
import vm from 'node:vm';

const source = readFileSync(
  new URL('../supabase/functions/nayanet-learning-verify/index.ts', import.meta.url),
  'utf8',
);
const code = stripTypeScriptTypes(source.replace(/^import .*;\r?\n/gm, ''));

const OWNER_ID = 'adfdf0b8-5558-41d1-9fed-ec51abf4fe2f';
const NAYA_ID = 'NAYA-NODE-0001';
const LEARNING_ID = 'learning-1';
const BLOCK_ID = 'IB-POISON-GATE-001';
const EVENT_ID = 'event-1';

const taskInput = {
  task_id: 'NAYA-0001-PROVENANCE-HELDOUT-001',
  required_capability: 'provenance_preservation',
  instruction: 'Apply retained intelligence to a provenance-sensitive action.',
  target_id: NAYA_ID,
};

function makePair() {
  const control = {
    id: 'control-1',
    user_id: OWNER_ID,
    project_id: 'NayaNET',
    status: 'SUCCESS',
    observed_result: 'REQUIRE_DIRECT_CANONICAL_INTELLIGENCE',
    evidence: {
      condition: 'CONTROL',
      retained_intelligence_used: false,
      learning_id: LEARNING_ID,
      source_event_id: EVENT_ID,
      task_input: taskInput,
      behavior: 'REQUIRE_DIRECT_CANONICAL_INTELLIGENCE',
      outcome: {
        provenance_preserved: false,
        task_completed: true,
        source_event_bound: null,
        intelligent_block_bound: null,
      },
    },
  };
  const treatment = {
    id: 'treatment-1',
    user_id: OWNER_ID,
    project_id: 'NayaNET',
    status: 'SUCCESS',
    observed_result: 'PRESERVE_PROVENANCE_BEFORE_APPLY',
    evidence: {
      condition: 'TREATMENT',
      retained_intelligence_used: true,
      learning_id: LEARNING_ID,
      source_event_id: EVENT_ID,
      intelligence_id: BLOCK_ID,
      task_input: taskInput,
      behavior: 'PRESERVE_PROVENANCE_BEFORE_APPLY',
      outcome: {
        provenance_preserved: true,
        task_completed: true,
        source_event_bound: EVENT_ID,
        intelligent_block_bound: BLOCK_ID,
      },
      causal_verification: {
        schema: 'NAYANET_CAUSAL_VERIFICATION_V1',
        causal_id: 'CVO-VALID-1',
        receipt_id: 'treatment-1',
        comparison_receipt_id: 'control-1',
        causal_assessment: 'CAUSAL_SUPPORTED',
        verification_status: 'OUTCOME_VERIFIED',
        observed_change: 'PRESERVE_PROVENANCE_BEFORE_APPLY',
        limitations: ['bounded paired experiment'],
      },
    },
  };
  return [control, treatment];
}

function runtime({ persistedReceipts = [] } = {}) {
  let handler;
  const promotionWrites = [];
  const learning = {
    id: LEARNING_ID,
    member_id: OWNER_ID,
    target_id: NAYA_ID,
    status: 'CANDIDATE',
    claim: 'Preserve provenance before applying retained intelligence.',
    source_event_id: EVENT_ID,
    observed_value: {
      intelligent_block_id: BLOCK_ID,
      lineage_id: 'lineage-1',
      relationship_id: 'relationship-1',
      checkpoint_id: 'checkpoint-1',
      index_id: 'index-1',
    },
    verification_method: 'pending',
    provenance: 'OBSERVATION',
  };

  function chainFor(table) {
    const chain = {
      select() { return chain; },
      eq() { return chain; },
      in() { return chain; },
      maybeSingle: async () => {
        if (table === 'learning_evidence') return { data: learning, error: null };
        if (table === 'nayanet_intelligent_blocks') return { data: null, error: null };
        return { data: null, error: null };
      },
      update(payload) {
        if (table === 'learning_evidence') promotionWrites.push(payload);
        chain._update = payload;
        return chain;
      },
      async single() {
        if (table === 'learning_evidence') {
          return {
            data: { ...learning, ...chain._update },
            error: null,
          };
        }
        return { data: null, error: null };
      },
      then(resolve) {
        if (table === 'nayanet_execution_receipts') {
          return Promise.resolve({ data: persistedReceipts, error: null }).then(resolve);
        }
        return Promise.resolve({ data: [], error: null }).then(resolve);
      },
    };
    return chain;
  }

  const admin = { from: table => chainFor(table) };

  vm.runInNewContext(code, {
    URL,
    Request,
    Response,
    console,
    Deno: {
      env: {
        get: key => ({
          SUPABASE_URL: 'https://offline.invalid',
          SUPABASE_SERVICE_ROLE_KEY: 'fake-key',
        })[key],
      },
      serve: callback => { handler = callback; },
    },
    createRemoteJWKSet: () => ({}),
    jwtVerify: async () => ({
      payload: {
        repository: 'SoulSchoolAcademy/NayaPOWER',
        ref: 'refs/heads/main',
        workflow_ref:
          'SoulSchoolAcademy/NayaPOWER/.github/workflows/live-supabase-runtime-proof.yml@refs/heads/main',
        jti: 'promotion-gate-test-jti',
      },
    }),
    createClient: () => admin,
  });

  return {
    promotionWrites,
    invoke: evidence_refs =>
      handler(new Request('https://offline.invalid', {
        method: 'POST',
        headers: {
          authorization: 'Bearer test',
          'content-type': 'application/json',
        },
        body: JSON.stringify({
          learning_id: LEARNING_ID,
          evidence_refs,
          verification_method: 'claimed independent verification',
        }),
      })),
  };
}

test('poisoned/arbitrary evidence refs cannot trigger an ACTIVE promotion write', async () => {
  const r = runtime({ persistedReceipts: [] });
  const response = await r.invoke([
    'fake-control',
    'fake-treatment',
    LEARNING_ID,
    'CVO-FAKE',
    NAYA_ID,
  ]);
  assert.equal(
    r.promotionWrites.length,
    0,
    'learning verifier attempted ACTIVE promotion before proving the supplied evidence refs',
  );
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.match(
    body.error,
    /EVIDENCE|CAUSAL|RECEIPT/,
    'failure must name the evidence boundary',
  );
});

test('a persisted causally valid control/treatment pair may cross the promotion evidence gate', async () => {
  const r = runtime({ persistedReceipts: makePair() });
  const response = await r.invoke([
    'treatment-1',
    'control-1',
    LEARNING_ID,
    'CVO-VALID-1',
    NAYA_ID,
  ]);
  assert.equal(
    r.promotionWrites.length,
    1,
    'valid persisted causal evidence should reach the existing promotion write',
  );
  // The lightweight fixture intentionally stops after the gate at the later
  // Intelligent Block lock-in read. We only prove the promotion evidence gate here.
  assert.notEqual(response.status, 409);
});
