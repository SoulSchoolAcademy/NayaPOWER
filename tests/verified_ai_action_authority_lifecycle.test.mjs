import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import { test } from 'node:test';
import vm from 'node:vm';

const source = readFileSync(new URL('../supabase/functions/nayanet-verified-ai-action/index.ts', import.meta.url), 'utf8');
const code = stripTypeScriptTypes(source.replace(/^import .*;\r?\n/gm, ''));

const OWNER_ID = 'adfdf0b8-5558-41d1-9fed-ec51abf4fe2f';
const NAYA_ID = 'NAYA-NODE-0001';
const MISSION_ID = 'NAYA-NODE-0001-CONTINUITY';
const ACTION = 'naya_node_apply';

const claims = {
  repository: 'SoulSchoolAcademy/NayaPOWER',
  ref: 'refs/heads/main',
  workflow_ref: 'SoulSchoolAcademy/NayaPOWER/.github/workflows/live-verified-ai-action-proof.yml@refs/heads/main',
  jti: 'authority-negative-matrix-jti',
  sub: 'repo:SoulSchoolAcademy/NayaPOWER:ref:refs/heads/main',
};

function canonicalGrant(overrides = {}) {
  return {
    grant_id: 'grant-1',
    issuer_id: OWNER_ID,
    subject_id: OWNER_ID,
    mission_id: MISSION_ID,
    scope: { target: NAYA_ID },
    actions: [ACTION],
    constraints: {},
    status: 'ACTIVE',
    issued_at: '2026-09-29T00:00:00Z',
    expires_at: null,
    revoked_at: null,
    ...overrides,
  };
}

function runtime({ grant = canonicalGrant(), grantExists = true } = {}) {
  let handler;
  let insertedReceipt = null;
  let receiptCount = 0;

  function query(table) {
    const filters = {};
    return {
      select() { return this; },
      eq(key, value) { filters[key] = value; return this; },
      order() { return this; },
      limit() { return this; },
      async maybeSingle() {
        if (table === 'nayanet_authority_grants') {
          if (!grantExists || filters.grant_id !== grant.grant_id) return { data: null, error: null };
          return { data: grant, error: null };
        }
        if (table === 'nayanet_execution_receipts') {
          return { data: { revision: 0 }, error: null };
        }
        throw new Error(`unexpected maybeSingle table: ${table}`);
      },
      insert(row) {
        if (table !== 'nayanet_execution_receipts') throw new Error(`unexpected insert table: ${table}`);
        insertedReceipt = row;
        return {
          select() {
            return {
              async single() {
                receiptCount += 1;
                return { data: { ...row, id: `refusal-${receiptCount}` }, error: null };
              },
            };
          },
        };
      },
    };
  }

  const admin = { from: query };

  vm.runInNewContext(code, {
    URL, Request, Response, console, Date, TextEncoder, Uint8Array, crypto,
    Deno: {
      env: { get: key => ({ SUPABASE_URL: 'https://offline.invalid', SUPABASE_SERVICE_ROLE_KEY: 'fake-key' })[key] },
      serve: callback => { handler = callback; },
    },
    createRemoteJWKSet: () => ({}),
    jwtVerify: async () => ({ payload: claims }),
    createClient: () => admin,
  });

  return {
    get insertedReceipt() { return insertedReceipt; },
    invoke: (authorityGrantId = 'grant-1') => handler(new Request('https://offline.invalid', {
      method: 'POST',
      headers: { authorization: 'Bearer test', 'content-type': 'application/json' },
      body: JSON.stringify({ mode: 'execute', authority_grant_id: authorityGrantId, idempotency_key: 'authority-negative-matrix' }),
    })),
  };
}

async function expectDenied(options, expectedReason, presented = 'grant-1') {
  const rt = runtime(options);
  const response = await rt.invoke(presented);
  assert.equal(response.status, 403);
  const body = await response.json();
  assert.equal(body.ok, false);
  assert.equal(body.status, 'BLOCKED');
  assert.equal(body.authority_reason, expectedReason);
  assert.equal(body.execution_outcome_id, null);
  assert.ok(body.refusal_receipt_id);
  assert.equal(rt.insertedReceipt.status, 'BLOCKED');
  assert.equal(rt.insertedReceipt.evidence.authority_decision, 'DENY');
  assert.equal(rt.insertedReceipt.evidence.action_executed, false);
  assert.equal(rt.insertedReceipt.evidence.outcome_created, false);
}

test('authority lifecycle fails closed when grant is missing', async () => {
  await expectDenied({ grantExists: false }, 'AUTHORITY_ABSENT', 'missing-grant');
});

test('authority lifecycle fails closed when grant is inactive', async () => {
  await expectDenied({ grant: canonicalGrant({ status: 'ISSUED' }) }, 'AUTHORITY_NOT_ACTIVE');
});

test('authority lifecycle fails closed for cross-owner grant', async () => {
  await expectDenied({ grant: canonicalGrant({ subject_id: '00000000-0000-0000-0000-000000000002' }) }, 'AUTHORITY_CROSS_OWNER');
});

test('authority lifecycle fails closed for wrong mission', async () => {
  await expectDenied({ grant: canonicalGrant({ mission_id: 'WRONG-MISSION' }) }, 'AUTHORITY_MISSION_MISMATCH');
});

test('authority lifecycle fails closed for wrong target scope', async () => {
  await expectDenied({ grant: canonicalGrant({ scope: { target: 'WRONG-TARGET' } }) }, 'AUTHORITY_SCOPE_MISMATCH');
});

test('authority lifecycle fails closed for action not granted', async () => {
  await expectDenied({ grant: canonicalGrant({ actions: ['read_only'] }) }, 'AUTHORITY_ACTION_NOT_GRANTED');
});

test('authority lifecycle fails closed for revoked-at grant even if status is ACTIVE', async () => {
  await expectDenied({ grant: canonicalGrant({ revoked_at: '2026-09-29T00:01:00Z' }) }, 'AUTHORITY_REVOKED');
});

test('authority lifecycle fails closed for expired grant', async () => {
  await expectDenied({ grant: canonicalGrant({ expires_at: '2020-01-01T00:00:00Z' }) }, 'AUTHORITY_EXPIRED');
});

test('negative matrix preserves distinct authority reasons in durable refusal evidence', async () => {
  const cases = [
    [canonicalGrant({ status: 'ISSUED' }), 'AUTHORITY_NOT_ACTIVE'],
    [canonicalGrant({ scope: { target: 'WRONG' } }), 'AUTHORITY_SCOPE_MISMATCH'],
    [canonicalGrant({ actions: [] }), 'AUTHORITY_ACTION_NOT_GRANTED'],
    [canonicalGrant({ revoked_at: '2026-09-29T00:01:00Z' }), 'AUTHORITY_REVOKED'],
    [canonicalGrant({ expires_at: '2020-01-01T00:00:00Z' }), 'AUTHORITY_EXPIRED'],
  ];
  for (const [grant, reason] of cases) {
    const rt = runtime({ grant });
    const response = await rt.invoke();
    assert.equal(response.status, 403);
    assert.equal(rt.insertedReceipt.evidence.authority_reason, reason);
  }
});


test('authority lifecycle rejects a stale cached grant after live revocation', async () => {
  const live = { grant: canonicalGrant() };
  const cachedGrant = { ...live.grant };
  let handler;
  let insertedReceipt = null;
  function query(table) {
    const filters = {};
    return {
      select() { return this; },
      eq(key, value) { filters[key] = value; return this; },
      order() { return this; },
      limit() { return this; },
      async maybeSingle() {
        if (table === 'nayanet_authority_grants') {
          if (filters.grant_id !== live.grant.grant_id) return { data: null, error: null };
          return { data: live.grant, error: null };
        }
        if (table === 'nayanet_execution_receipts') return { data: { revision: 0 }, error: null };
        throw new Error('unexpected maybeSingle table: ' + table);
      },
      insert(row) {
        insertedReceipt = row;
        return { select() { return { async single() { return { data: { ...row, id: 'cached-revocation-refusal' }, error: null }; } }; } };
      },
    };
  }
  vm.runInNewContext(code, {
    URL, Request, Response, console, Date, TextEncoder, Uint8Array, crypto,
    Deno: {
      env: { get: key => ({ SUPABASE_URL: 'https://offline.invalid', SUPABASE_SERVICE_ROLE_KEY: 'fake-key' })[key] },
      serve: callback => { handler = callback; },
    },
    createRemoteJWKSet: () => ({}),
    jwtVerify: async () => ({ payload: claims }),
    createClient: () => ({ from: query }),
  });

  // A caller has cached an ACTIVE grant. Live authority is then revoked.
  live.grant = canonicalGrant({ revoked_at: '2026-09-29T00:02:00Z' });

  const response = await handler(new Request('https://offline.invalid', {
    method: 'POST',
    headers: { authorization: 'Bearer test', 'content-type': 'application/json' },
    body: JSON.stringify({ mode: 'execute', authority_grant_id: cachedGrant.grant_id, idempotency_key: 'cached-revocation' }),
  }));
  assert.equal(response.status, 403);
  const body = await response.json();
  assert.equal(body.status, 'BLOCKED');
  assert.equal(body.authority_reason, 'AUTHORITY_REVOKED');
  assert.equal(body.execution_outcome_id, null);
  assert.ok(body.refusal_receipt_id);
  assert.equal(insertedReceipt.status, 'BLOCKED');
  assert.equal(insertedReceipt.evidence.authority_decision, 'DENY');
  assert.equal(insertedReceipt.evidence.action_executed, false);
  assert.equal(insertedReceipt.evidence.outcome_created, false);
});