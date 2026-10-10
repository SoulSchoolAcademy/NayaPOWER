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
const RELATED = 'NAYA-0001-PROVENANCE-HELDOUT-002';
const UNRELATED = 'NAYA-0001-UNRELATED-ARITHMETIC-001';

function runtime() {
  let handler;
  const learning = {
    id: LEARNING_ID,
    target_id: NAYA_ID,
    level: 'E5_CAN_TEACH',
    status: 'ACTIVE',
    claim: LESSON,
    source_event_id: 'event-active-1',
    observed_value: { intelligent_block_id: ACTIVE_BLOCK_ID, behavioral_change: true },
    verification_method: 'independent causal verification',
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
      jti: 'successor-generalization-jti',
    } }),
    createClient: () => ({ from() { throw new Error('admin writes are not expected in successor proof'); } }),
    fetch: async url => {
      const u = String(url);
      if (u.includes('/rest/v1/nayanet_intelligent_blocks?')) {
        const active = u.includes(encodeURIComponent(ACTIVE_BLOCK_ID)) || u.includes(ACTIVE_BLOCK_ID);
        return new Response(JSON.stringify([{
          intelligent_block_id: active ? ACTIVE_BLOCK_ID : BLOCK_ID,
          owner_id: OWNER_ID,
          understanding_state: active ? 'LEARNED' : 'VERIFIED',
          content: { lesson: active ? LESSON : 'Canonical seed lesson.' },
          evidence_refs: ['event-active-1'],
          provenance: { source: 'event-active-1' },
        }]), { status: 200 });
      }
      if (u.includes('/rest/v1/nayanet_authority_grants?')) {
        return new Response(JSON.stringify([{
          grant_id: 'grant-node0001',
          scope: { target: NAYA_ID },
          actions: ['naya_node_apply'],
          status: 'ACTIVE',
        }]), { status: 200 });
      }
      if (u.includes('/rest/v1/learning_evidence?')) {
        return new Response(JSON.stringify([learning]), { status: 200 });
      }
      if (u.includes('/rest/v1/nayanet_brain_relationships?')) {
        return new Response(JSON.stringify([{
          relationship_id: 'rel-1',
          source_id: 'event-active-1',
          target_id: ACTIVE_BLOCK_ID,
          relationship_type: 'VERIFIED_BY',
          epistemic_state: 'VERIFIED',
          provenance: { source: 'verification' },
        }]), { status: 200 });
      }
      throw new Error(`unexpected fetch: ${u}`);
    },
  });

  return {
    invoke: (mode, taskId) => {
      const task = taskId ? `&task_id=${encodeURIComponent(taskId)}` : '';
      return handler(new Request(`https://offline.invalid?mode=${mode}&learning_id=${LEARNING_ID}${task}`, {
        method: 'GET',
        headers: { authorization: 'Bearer test' },
      }));
    },
  };
}

test('cold successor applies ACTIVE learning to a second related held-out task without inheriting authority', async () => {
  const response = await runtime().invoke('cold-successor', RELATED);
  assert.equal(response.status, 200);
  const body = await response.json();
  assert.equal(body.ok, true);
  assert.equal(body.cold_start.input_supplied_by_caller, 'learning_id_and_task_id_only');
  assert.equal(body.cold_start.intelligence_content_accepted_as_input, false);
  assert.equal(body.use.task_id, RELATED);
  assert.equal(body.use.task_class, 'RELATED_HELDOUT');
  assert.equal(body.use.applicable_to_task, true);
  assert.equal(body.use.behavior_derived_from_retrieved_lesson, 'PRESERVE_PROVENANCE_BEFORE_APPLY');
  assert.equal(body.use.materially_attributable, true);
  assert.equal(body.authority_boundary.authority_inherited, false);
  assert.equal(body.authority_boundary.successor_grant_count, 0);
  assert.equal(body.authority_boundary.executed, false);
  assert.equal(body.authority_boundary.blocked_by, 'IDENTITY_SCOPE');
});

test('cold successor refuses negative transfer on an unrelated task', async () => {
  const response = await runtime().invoke('cold-successor', UNRELATED);
  assert.equal(response.status, 200);
  const body = await response.json();
  assert.equal(body.use.task_id, UNRELATED);
  assert.equal(body.use.task_class, 'UNRELATED_NEGATIVE_TRANSFER');
  assert.equal(body.use.applicable_to_task, false);
  assert.equal(body.use.behavior_derived_from_retrieved_lesson, 'NO_APPLICABLE_RETAINED_INTELLIGENCE');
  assert.equal(body.use.correct_refusal, true);
  assert.equal(body.use.materially_attributable, false);
  assert.equal(body.authority_boundary.authority_inherited, false);
  assert.equal(body.authority_boundary.executed, false);
});

test('independent successor verifier recomputes second-task applicability and non-inheritance', async () => {
  const response = await runtime().invoke('cold-successor-verify', RELATED);
  assert.equal(response.status, 200);
  const body = await response.json();
  assert.equal(body.ok, true);
  assert.equal(body.independent_verification, true);
  assert.equal(body.executor_claim_trusted, false);
  assert.equal(body.recomputed.task_id, RELATED);
  assert.equal(body.recomputed.applicable_to_task, true);
  assert.equal(body.recomputed.behavior_recomputed, 'PRESERVE_PROVENANCE_BEFORE_APPLY');
  assert.equal(body.recomputed.successor_grant_count, 0);
  assert.equal(body.recomputed.authority_recomputed, false);
  assert.equal(body.recomputed.recomputed_blocked_by, 'IDENTITY_SCOPE');
});

test('independent successor verifier recomputes unrelated-task refusal', async () => {
  const response = await runtime().invoke('cold-successor-verify', UNRELATED);
  assert.equal(response.status, 200);
  const body = await response.json();
  assert.equal(body.ok, true);
  assert.equal(body.recomputed.task_id, UNRELATED);
  assert.equal(body.recomputed.applicable_to_task, false);
  assert.equal(body.recomputed.correct_refusal, true);
  assert.equal(body.recomputed.behavior_recomputed, 'NO_APPLICABLE_RETAINED_INTELLIGENCE');
  assert.equal(body.recomputed.successor_grant_count, 0);
});

test('cold successor rejects an unregistered task context', async () => {
  const response = await runtime().invoke('cold-successor', 'UNREGISTERED-TASK');
  assert.equal(response.status, 400);
  const body = await response.json();
  assert.equal(body.error, 'HELDOUT_TASK_REQUIRED');
});
