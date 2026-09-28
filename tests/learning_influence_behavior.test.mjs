import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import { test } from 'node:test';
import vm from 'node:vm';

const source = readFileSync(new URL('../supabase/functions/nayanet-cold-runtime-proof/index.ts', import.meta.url), 'utf8');
const code = stripTypeScriptTypes(source.replace(/^import .*;\n/gm, ''));

const OWNER_ID = 'adfdf0b8-5558-41d1-9fed-ec51abf4fe2f';
const NAYA_ID = 'NAYA-NODE-0001';
const BLOCK_ID = 'IB-NAYA-NODE-0001-0001';
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
    observed_value: { intelligent_block_id: BLOCK_ID, provenance_preserved: true },
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
        return new Response(JSON.stringify([{ intelligent_block_id: BLOCK_ID, owner_id: OWNER_ID, understanding_state: 'CANDIDATE', content: { lesson }, evidence_refs: [] }]), { status: 200 });
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
  assert.equal(body.outcome_delta.provenance_preserved, 1);
  assert.equal(body.counterfactual.computed_not_declared, true);
});

test('learning influence refuses causal success when retrieved intelligence causes no measured change', async () => {
  const response = await runtime({ lesson: 'A lesson with no relevant instruction.' }).invoke();
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.error, 'NO_MEASURED_LEARNING_EFFECT');
  assert.equal(body.behavioral_delta.changed, false);
  assert.equal(body.outcome_delta.provenance_preserved, 0);
});
