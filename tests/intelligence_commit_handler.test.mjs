import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import { test } from 'node:test';
import vm from 'node:vm';

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
  assert.deepEqual(r.calls[0].body, { ...fields, p_runtime_jti: claims.jti, p_owner_id: 'adfdf0b8-5558-41d1-9fed-ec51abf4fe2f', p_naya_id: 'NAYA-NODE-0001', p_connections: null });
  assert.equal(r.calls[0].url, 'https://offline.invalid/rest/v1/rpc/nayanet_intelligence_commit_runtime');
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
