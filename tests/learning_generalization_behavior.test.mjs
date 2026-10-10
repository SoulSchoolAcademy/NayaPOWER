import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import { test } from 'node:test';
import vm from 'node:vm';

const source = readFileSync(new URL('../supabase/functions/nayanet-cold-runtime-proof/index.ts', import.meta.url), 'utf8');
const code = stripTypeScriptTypes(source.replace(/^import[\s\S]*?;\r?\n/gm, ''));

const OWNER_ID = 'adfdf0b8-5558-41d1-9fed-ec51abf4fe2f';
const NAYA_ID = 'NAYA-NODE-0001';
const BLOCK_ID = 'IB-NAYA-NODE-0001-0001';
const ACTIVE_BLOCK_ID = 'IB-NAYA-FLOW-LESSON-ACTIVE-001';
const LEARNING_ID = 'active-learning-id';
const LESSON = 'Preserve provenance before applying retained intelligence.';
const claims = {
  repository: 'SoulSchoolAcademy/NayaPOWER',
  ref: 'refs/heads/main',
  workflow_ref: 'SoulSchoolAcademy/NayaPOWER/.github/workflows/live-supabase-runtime-proof.yml@refs/heads/main',
  jti: 'generalization-runtime-jti',
};

function runtime({ learningStatus = 'ACTIVE', lesson = LESSON } = {}) {
  let handler;
  let receiptId = 0;
  let revision = 50;
  const inserted = [];
  const learning = {
    id: LEARNING_ID,
    target_id: NAYA_ID,
    level: 'E5_CAN_TEACH',
    status: learningStatus,
    claim: lesson,
    source_event_id: 'event-active-1',
    observed_value: { intelligent_block_id: ACTIVE_BLOCK_ID, behavioral_change: true },
    verification_method: 'independent causal verification',
    provenance: 'OBSERVATION',
  };

  const admin = {
    from(table) {
      assert.equal(table, 'nayanet_execution_receipts');
      return {
        insert(row) {
          inserted.push(row);
          return {
            select() {
              return {
                async single() {
                  receiptId += 1;
                  return { data: { ...row, id: `generalization-receipt-${receiptId}` }, error: null };
                },
              };
            },
          };
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
    fetch: async (url) => {
      const u = String(url);
      if (u.includes('/rest/v1/nayanet_intelligent_blocks?')) {
        const active = u.includes(encodeURIComponent(ACTIVE_BLOCK_ID)) || u.includes(ACTIVE_BLOCK_ID);
        return new Response(JSON.stringify([{
          intelligent_block_id: active ? ACTIVE_BLOCK_ID : BLOCK_ID,
          owner_id: OWNER_ID,
          understanding_state: active ? 'LEARNED' : 'VERIFIED',
          content: { lesson: active ? lesson : 'Canonical seed lesson.' },
          evidence_refs: [],
          provenance: { source: 'test' },
        }]), { status: 200 });
      }
      if (u.includes('/rest/v1/nayanet_authority_grants?')) {
        return new Response(JSON.stringify([{
          grant_id: 'grant-1',
          scope: { target: NAYA_ID },
          actions: ['naya_node_apply'],
          status: 'ACTIVE',
        }]), { status: 200 });
      }
      if (u.includes('/rest/v1/learning_evidence?')) {
        return new Response(JSON.stringify([learning]), { status: 200 });
      }
      if (u.includes('/rest/v1/nayanet_execution_receipts?')) {
        revision += 1;
        return new Response(JSON.stringify([{ revision }]), { status: 200 });
      }
      throw new Error(`unexpected fetch: ${u}`);
    },
  });

  return {
    inserted,
    invoke: (body = { learning_id: LEARNING_ID }) => handler(new Request('https://offline.invalid?mode=learning-generalization', {
      method: 'POST',
      headers: { authorization: 'Bearer test', 'content-type': 'application/json' },
      body: JSON.stringify(body),
    })),
  };
}

test('ACTIVE learning improves a second related held-out task and refuses unrelated transfer', async () => {
  const rt = runtime();
  const response = await rt.invoke();
  assert.equal(response.status, 200);
  const body = await response.json();

  assert.equal(body.schema, 'NAYANET_ACTIVE_LEARNING_GENERALIZATION_V1');
  assert.equal(body.learning_status, 'ACTIVE');
  assert.deepEqual(body.input_boundary.caller_supplied, ['learning_id']);
  assert.equal(body.input_boundary.intelligence_content_accepted_as_input, false);
  assert.equal(body.result.related_heldout_improved, true);
  assert.equal(body.result.unrelated_negative_transfer_refused, true);
  assert.equal(body.result.independent_verification_required, true);
  assert.equal(body.result.executor_claim_trusted_as_verification, false);

  const related = body.tasks['NAYA-0001-PROVENANCE-HELDOUT-002'];
  assert.equal(related.task_class, 'RELATED_HELDOUT');
  assert.equal(related.applicability, true);
  assert.equal(related.behavioral_delta, true);
  assert.equal(related.control_outcome.provenance_preserved, false);
  assert.equal(related.treatment_outcome.provenance_preserved, true);
  assert.notEqual(related.control_behavior, related.treatment_behavior);

  const unrelated = body.tasks['NAYA-0001-UNRELATED-ARITHMETIC-001'];
  assert.equal(unrelated.task_class, 'UNRELATED_NEGATIVE_TRANSFER');
  assert.equal(unrelated.applicability, false);
  assert.equal(unrelated.behavioral_delta, false);
  assert.equal(unrelated.control_behavior, 'NO_APPLICABLE_RETAINED_INTELLIGENCE');
  assert.equal(unrelated.treatment_behavior, 'NO_APPLICABLE_RETAINED_INTELLIGENCE');
  assert.equal(unrelated.control_outcome.answer, 12);
  assert.equal(unrelated.treatment_outcome.answer, 12);

  assert.equal(rt.inserted.length, 4);
  assert.equal(body.receipt_ids.length, 4);
});

test('generalization refuses caller-supplied intelligence content', async () => {
  const response = await runtime().invoke({ learning_id: LEARNING_ID, lesson: LESSON });
  assert.equal(response.status, 400);
  const body = await response.json();
  assert.equal(body.error, 'INTELLIGENCE_CONTENT_INPUT_FORBIDDEN');
});

test('generalization fails closed unless persisted learning is ACTIVE', async () => {
  const response = await runtime({ learningStatus: 'CANDIDATE' }).invoke();
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.error, 'ACTIVE_LEARNING_REQUIRED');
  assert.equal(body.status, 'CANDIDATE');
});

test('generalization cannot claim improvement when the retained lesson has no applicable capability', async () => {
  const response = await runtime({ lesson: 'A lesson unrelated to any predeclared capability.' }).invoke();
  assert.equal(response.status, 409);
  const body = await response.json();
  assert.equal(body.error, 'NO_PREDECLARED_APPLICABLE_GENERALIZATION_TASK');
});
