import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import { test } from 'node:test';
import vm from 'node:vm';
import {
  CapabilityValidationError,
  validateCapabilities,
} from '../supabase/functions/nayanet-intelligence-commit-runtime/capability-vocabulary.ts';
import {
  TaskClassValidationError,
  validateTaskClasses,
} from '../supabase/functions/nayanet-intelligence-commit-runtime/task-class-vocabulary.ts';

// Execute the real handler offline. Only external services and the Deno host
// are substituted; authentication decisions and RPC serialization remain real.
const source = readFileSync(new URL('../supabase/functions/nayanet-intelligence-commit-runtime/index.ts', import.meta.url), 'utf8');
const code = stripTypeScriptTypes(source.replace(/^import .*;\r?\n/gm, ''));
const claims = {
  repository: 'SoulSchoolAcademy/NayaPOWER', ref: 'refs/heads/main',
  workflow_ref: 'SoulSchoolAcademy/NayaPOWER/.github/workflows/live-intelligence-commit-proof.yml@refs/heads/main',
  jti: 'test-verified-token-id',
};

function runtime({ payload = claims, rpcStatus = 200 } = {}) {
  let handler;
  const calls = [];
  vm.runInNewContext(code, {
    URL, Request, Response,
    // The handler's import lines are stripped for offline execution; the real
    // vocabulary modules are injected so validation stays real.
    validateCapabilities, CapabilityValidationError,
    validateTaskClasses, TaskClassValidationError,
    Deno: {
      env: { get: key => ({ SUPABASE_URL: 'https://offline.invalid', SUPABASE_SERVICE_ROLE_KEY: 'fake-server-key' })[key] },
      serve: callback => { handler = callback; },
    },
    createRemoteJWKSet: () => ({}),
    jwtVerify: async () => ({ payload }),
    createClient: () => ({}),
    fetch: async (url, options) => {
      calls.push({ url, options, body: JSON.parse(options.body) });
      return new Response(JSON.stringify(rpcStatus === 200 ? { ok: true, receipt_id: 'test-receipt' } : { message: 'grant denied' }), { status: rpcStatus });
    },
  });
  return { calls, invoke: (body, authorization = 'Bearer fake-oidc') => handler(new Request('https://offline.invalid', {
    method: 'POST', headers: authorization ? { authorization } : {}, body: JSON.stringify(body),
  })) };
}

test('execute carries lesson fields and authenticated token ID across the RPC boundary', async () => {
  const r = runtime();
  const lesson = { mode: 'execute', p_event_id: 'fresh-event', p_title: 'Lesson', p_content: 'Useful intelligence', p_category: 'KNOWLEDGE', p_topic: 'CONTINUITY', p_target_id: 'NAYA-NODE-0001', p_authority_grant_id: 'test-grant', p_project_id: 'NayaNET', p_runtime_jti: 'untrusted', p_owner_id: 'untrusted', p_naya_id: 'untrusted' };
  const response = await r.invoke(lesson);
  assert.equal(response.status, 200);
  assert.equal((await response.json()).result.receipt_id, 'test-receipt');
  assert.equal(r.calls.length, 1);
  const { mode, p_runtime_jti, p_owner_id, p_naya_id, ...fields } = lesson;
  assert.deepEqual(r.calls[0].body, { ...fields, p_connections: null, p_capabilities: null, p_declared_task_classes: null, p_runtime_jti: claims.jti, p_owner_id: 'adfdf0b8-5558-41d1-9fed-ec51abf4fe2f', p_naya_id: 'NAYA-NODE-0001' });
  assert.equal(r.calls[0].url, 'https://offline.invalid/rest/v1/rpc/nayanet_intelligence_commit_runtime');
});

test('execute threads caller-supplied p_connections across the RPC boundary', async () => {
  const r = runtime();
  const lesson = { mode: 'execute', p_event_id: 'fresh-event', p_title: 'Lesson', p_content: 'Useful intelligence', p_category: 'KNOWLEDGE', p_topic: 'CONTINUITY', p_target_id: 'NAYA-NODE-0001', p_authority_grant_id: 'test-grant', p_project_id: 'NayaNET', p_connections: [{ type: 'SUPPORTS', target: 'IB-000001' }] };
  const response = await r.invoke(lesson);
  assert.equal(response.status, 200);
  assert.equal(r.calls.length, 1);
  assert.deepEqual(r.calls[0].body.p_connections, [{ type: 'SUPPORTS', target: 'IB-000001' }]);
});

test('execute threads validated p_capabilities across the RPC boundary (normalized, deduped)', async () => {
  const r = runtime();
  const lesson = { mode: 'execute', p_event_id: 'fresh-event', p_title: 'Lesson', p_content: 'Useful intelligence', p_category: 'KNOWLEDGE', p_topic: 'CONTINUITY', p_target_id: 'NAYA-NODE-0001', p_authority_grant_id: 'test-grant', p_project_id: 'NayaNET', p_capabilities: [' Governance_Triage ', 'compounding_capture', 'governance_triage'] };
  const response = await r.invoke(lesson);
  assert.equal(response.status, 200);
  assert.equal(r.calls.length, 1);
  assert.deepEqual(r.calls[0].body.p_capabilities, ['compounding_capture', 'governance_triage']);
});

test('execute fails closed on unknown capability before reaching the RPC', async () => {
  const r = runtime();
  const lesson = { mode: 'execute', p_event_id: 'fresh-event', p_title: 'Lesson', p_content: 'Useful intelligence', p_category: 'KNOWLEDGE', p_topic: 'CONTINUITY', p_target_id: 'NAYA-NODE-0001', p_authority_grant_id: 'test-grant', p_project_id: 'NayaNET', p_capabilities: ['mind_control'] };
  const response = await r.invoke(lesson);
  assert.equal(response.status, 400);
  assert.match((await response.json()).error, /^CAPABILITY_UNKNOWN:mind_control/);
  assert.equal(r.calls.length, 0, 'rejected captures must never reach the RPC');
});

test('execute fails closed on malformed capabilities before reaching the RPC', async () => {
  const r = runtime();
  const lesson = { mode: 'execute', p_event_id: 'fresh-event', p_title: 'Lesson', p_content: 'Useful intelligence', p_category: 'KNOWLEDGE', p_topic: 'CONTINUITY', p_target_id: 'NAYA-NODE-0001', p_authority_grant_id: 'test-grant', p_project_id: 'NayaNET', p_capabilities: 'governance_triage' };
  const response = await r.invoke(lesson);
  assert.equal(response.status, 400);
  assert.match((await response.json()).error, /^CAPABILITY_MALFORMED/);
  assert.equal(r.calls.length, 0);
});

test('supersede mode calls the supersede bridge with identity and p_connections', async () => {
  const r = runtime();
  const body = { mode: 'supersede', p_superseded_block_id: '11111111-1111-1111-1111-111111111111', p_title: 'B', p_content: 'Preserve provenance before applying retained intelligence.', p_authority_grant_id: 'test-grant', p_idempotency_key: 'idem-1', p_connections: [{ type: 'RELATED_TO', target: 'IB-000002' }] };
  const response = await r.invoke(body);
  assert.equal(response.status, 200);
  const result = await response.json();
  assert.equal(result.status, 'SUPERSEDED');
  assert.equal(r.calls.length, 1);
  assert.equal(r.calls[0].url, 'https://offline.invalid/rest/v1/rpc/nayanet_supersede_intelligent_block_runtime');
  assert.deepEqual(r.calls[0].body.p_connections, [{ type: 'RELATED_TO', target: 'IB-000002' }]);
  assert.equal(r.calls[0].body.p_naya_id, 'NAYA-NODE-0001');
  assert.equal(r.calls[0].body.p_runtime_jti, claims.jti);
  assert.equal(r.calls[0].body.p_superseded_block_id, '11111111-1111-1111-1111-111111111111');
  assert.equal(r.calls[0].body.p_idempotency_key, 'idem-1');
});

test('supersede mode fails closed on missing fields', async () => {
  const r = runtime();
  const response = await r.invoke({ mode: 'supersede', p_title: 'B' });
  assert.equal(response.status, 400);
  assert.match((await response.json()).error, /^SUPERSEDE_FIELDS_REQUIRED:/);
  assert.equal(r.calls.length, 0);
});

test('connect-proof workflow is bound alongside the commit-proof workflow', async () => {
  const connectClaims = { ...claims, workflow_ref: 'SoulSchoolAcademy/NayaPOWER/.github/workflows/live-connect-proof.yml@refs/heads/main' };
  const r = runtime({ payload: connectClaims });
  const response = await r.invoke({ mode: 'execute', p_event_id: 'e', p_title: 't', p_content: 'c', p_category: 'c', p_topic: 't', p_authority_grant_id: 'g' });
  assert.equal(response.status, 200);
  assert.equal(r.calls.length, 1);
});

test('missing identity and wrong workflow cannot reach the RPC', async () => {
  for (const [payload, authorization, error] of [[claims, '', 'RUNTIME_IDENTITY_REQUIRED'], [{ ...claims, ref: 'refs/heads/untrusted' }, 'Bearer fake-oidc', 'WORKFLOW_BINDING_MISMATCH']]) {
    const r = runtime({ payload });
    const response = await r.invoke({ mode: 'execute' }, authorization);
    assert.equal(response.status, 400);
    assert.equal((await response.json()).error, error);
    assert.equal(r.calls.length, 0);
  }
});

test('RPC refusal cannot become a successful execution receipt', async () => {
  const r = runtime({ rpcStatus: 403 });
  const response = await r.invoke({ mode: 'execute' });
  const result = await response.json();
  assert.equal(response.status, 400);
  assert.equal(result.ok, false);
  assert.match(result.error, /^COMMIT_RPC_403:/);
  assert.equal(result.status, undefined);
});
