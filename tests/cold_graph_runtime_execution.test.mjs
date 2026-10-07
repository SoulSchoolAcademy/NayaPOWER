import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import { test } from 'node:test';
import vm from 'node:vm';

const source = readFileSync(
  new URL('../supabase/functions/nayanet-cold-runtime-proof/index.ts', import.meta.url),
  'utf8',
);
const code = stripTypeScriptTypes(source.replace(/^import .*;\r?\n/gm, ''));

const OWNER_ID = 'adfdf0b8-5558-41d1-9fed-ec51abf4fe2f';
const NAYA_ID = 'NAYA-NODE-0001';
const BLOCK_ID = 'IB-NAYA-NODE-0001-0001';

function runtime({ verifiedRelationship = true } = {}) {
  let handler;
  const writes = [];

  vm.runInNewContext(code, {
    URL,
    Request,
    Response,
    console: { error() {} },
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
        workflow_ref: 'SoulSchoolAcademy/NayaPOWER/.github/workflows/live-supabase-runtime-proof.yml@refs/heads/main',
        jti: 'binding-contract-jti',
      },
    }),
    createClient: () => ({
      from: table => ({
        insert: row => ({
          select: () => ({
            single: async () => {
              const persisted = { ...row, id: 'runtime-connect-receipt' };
              writes.push({ table, row: persisted });
              return { data: persisted, error: null };
            },
          }),
        }),
      }),
    }),
    fetch: async url => {
      const u = String(url);
      if (u.includes('/rest/v1/nayanet_intelligent_blocks?')) {
        return new Response(JSON.stringify([{
          intelligent_block_id: BLOCK_ID,
          owner_id: OWNER_ID,
          understanding_state: 'LEARNED',
          evidence_refs: ['CVO-1'],
          provenance: { source: 'CVO-1' },
          content: { lesson: 'Preserve provenance before applying retained intelligence.' },
        }]), { status: 200 });
      }
      if (u.includes('/rest/v1/nayanet_authority_grants?')) {
        return new Response(JSON.stringify([{
          grant_id: 'grant-node0001',
          mission_id: 'NAYA-NODE-0001-CONTINUITY',
          scope: { target: NAYA_ID },
          actions: ['naya_node_apply'],
          status: 'ACTIVE',
        }]), { status: 200 });
      }
      if (u.includes('/rest/v1/nayanet_brain_relationships?')) {
        const relationship = {
          relationship_id: 'REL-1',
          source_id: 'CVO-1',
          target_id: BLOCK_ID,
          relationship_type: 'VERIFIED_BY',
          epistemic_state: verifiedRelationship ? 'VERIFIED' : 'UNVERIFIED',
          status: 'ACTIVE',
          visibility: 'PRIVATE',
          provenance: { source: 'CVO-1' },
          evidence_refs: ['CVO-1'],
          valid_from: '2026-01-01T00:00:00Z',
          applicability: {
            state: 'APPLICABLE',
            task_classes: ['provenance_sensitive'],
          },
        };
        return new Response(JSON.stringify([relationship]), { status: 200 });
      }
      throw new Error('unexpected fetch: ' + u);
    },
  });

  return {
    invoke: () => handler(new Request(
      'https://offline.invalid?mode=connect',
      { method: 'GET', headers: { authorization: 'Bearer test' } },
    )),
    writes,
  };
}

test('CONNECT actual runtime preserves verified relationship support', async () => {
  const rt = runtime({ verifiedRelationship: true });
  const response = await rt.invoke();
  assert.equal(response.status, 200);
  const body = await response.json();
  assert.equal(body.ok, true);
  assert.equal(body.receipt.connect.connected, true);
  assert.equal(body.receipt.connect.verified_support_count, 1);
  assert.equal(body.receipt.behavior.allowed, false);
  assert.equal(body.receipt.authority_boundary.connect_grants_authority, false);
  assert.equal(rt.writes.length, 0);
});

test('CONNECT actual runtime refuses contextual verification when relationship evidence is not verified', async () => {
  const rt = runtime({ verifiedRelationship: false });
  const response = await rt.invoke();
  assert.equal(response.status, 200);
  const body = await response.json();
  assert.equal(body.ok, true);
  assert.equal(body.receipt.connect.connected, true);
  assert.equal(body.receipt.connect.verified_support_count, 0);
  assert.equal(body.receipt.behavior.executed, false);
  assert.equal(body.receipt.authority_boundary.consequential_actions_authorized, false);
});

test('CONNECT actual runtime is bound to canonical block and workflow identity', async () => {
  const rt = runtime({ verifiedRelationship: true });
  const response = await rt.invoke();
  const body = await response.json();
  assert.equal(body.receipt.block_id, BLOCK_ID);
  assert.equal(body.receipt.naya_id, NAYA_ID);
  assert.equal(body.receipt.block_owner_match, true);
  assert.equal(body.receipt.workflow_ref.includes('.github/workflows/live-supabase-runtime-proof.yml@refs/heads/main'), true);
});
