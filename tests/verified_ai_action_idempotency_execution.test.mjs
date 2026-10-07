import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import { test } from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';

const FUNCTION = new URL('../supabase/functions/nayanet-verified-ai-action/index.ts', import.meta.url);
const MIGRATION = new URL('../supabase/migrations/20261006120000_idempotency_key_unique_v1.sql', import.meta.url);
const SOURCE = readFileSync(FUNCTION, 'utf8');
const MIGRATION_SOURCE = readFileSync(MIGRATION, 'utf8');

const OWNER_ID = 'adfdf0b8-5558-41d1-9fed-ec51abf4fe2f';
const NAYA_ID = 'NAYA-NODE-0001';
const MISSION_ID = 'NAYA-NODE-0001-CONTINUITY';
const ACTION = 'naya_node_apply';
const BLOCK_ID = 'IB-NAYA-NODE-0001-0001';
const GRANT_ID = '99999999-8888-4777-8666-555555555555';
const ALT_GRANT_ID = '88888888-7777-4666-8555-444444444444';
const LESSON = 'Preserve provenance before applying retained intelligence.';
const TOKEN_JWT = 'runtime-jwt';

const GRANTS = [
  {
    grant_id: GRANT_ID,
    issuer_id: OWNER_ID,
    subject_id: OWNER_ID,
    mission_id: MISSION_ID,
    scope: { target: NAYA_ID },
    actions: [ACTION],
    constraints: {},
    status: 'ACTIVE',
    issued_at: '2026-10-06T00:00:00.000Z',
    expires_at: '2099-01-01T00:00:00.000Z',
    revoked_at: null,
  },
  {
    grant_id: ALT_GRANT_ID,
    issuer_id: OWNER_ID,
    subject_id: OWNER_ID,
    mission_id: MISSION_ID,
    scope: { target: NAYA_ID },
    actions: [ACTION],
    constraints: {},
    status: 'ACTIVE',
    issued_at: '2026-10-06T00:00:00.000Z',
    expires_at: '2099-01-01T00:00:00.000Z',
    revoked_at: null,
  },
];

const BLOCK = {
  intelligent_block_id: BLOCK_ID,
  owner_id: OWNER_ID,
  understanding_state: 'ACTIVE',
  content: { lesson: LESSON },
  evidence_refs: [{ type: 'source', id: 'source-1' }],
};

const claims = {
  repository: 'SoulSchoolAcademy/NayaPOWER',
  ref: 'refs/heads/main',
  workflow_ref: 'SoulSchoolAcademy/NayaPOWER/.github/workflows/live-verified-ai-action-proof.yml@refs/heads/main',
  jti: 'gate1-executor-jti',
  sub: 'repo:SoulSchoolAcademy/NayaPOWER:ref:refs/heads/main',
};

function makeRuntime({ enforceUnique = true, sourceTransform = (source) => source } = {}) {
  let handler;
  let receiptSequence = 0;
  let outcomeSequence = 0;
  const rows = {
    nayanet_authority_grants: GRANTS.map((row) => ({ ...row })),
    nayanet_intelligent_blocks: [{ ...BLOCK }],
    nayanet_execution_receipts: [],
    nayanet_execution_outcomes: [],
  };

  const executeQuery = (query) => {
    const table = rows[query.table];
    if (!table) throw new Error('UNKNOWN_TABLE_' + query.table);

    if (query.op === 'insert') {
      const row = {
        ...query.insertRow,
        id: query.table === 'nayanet_execution_receipts'
          ? 'receipt-' + receiptSequence++
          : 'outcome-' + outcomeSequence++,
      };

      if (
        query.table === 'nayanet_execution_receipts' &&
        enforceUnique &&
        row.idempotency_key != null &&
        table.some((existing) => existing.idempotency_key === row.idempotency_key)
      ) {
        return { data: null, error: { code: '23505', message: 'duplicate idempotency key' } };
      }

      table.push(row);
      return { data: { ...row }, error: null };
    }

    if (query.op === 'update') {
      const matches = table.filter((row) => query.filters.every(([column, value]) => row[column] === value));
      for (const row of matches) Object.assign(row, query.updatePatch);
      const data = matches.length ? { ...matches[0] } : null;
      return data
        ? { data, error: null }
        : { data: null, error: { code: '404', message: 'row not found' } };
    }

    let matches = table.filter((row) => query.filters.every(([column, value]) => row[column] === value));
    if (query.orderBy) {
      const { column, ascending } = query.orderBy;
      matches.sort((a, b) => {
        const left = Number(a[column] ?? 0);
        const right = Number(b[column] ?? 0);
        return ascending ? left - right : right - left;
      });
    }
    if (query.limitCount != null) matches = matches.slice(0, query.limitCount);
    if (query.singleRequired) {
      if (matches.length !== 1) {
        return { data: null, error: { code: 'PGRST116', message: 'expected one row' } };
      }
      return { data: { ...matches[0] }, error: null };
    }
    return { data: matches[0] ? { ...matches[0] } : null, error: null };
  };

  class Query {
    constructor(table) {
      this.table = table;
      this.op = 'select';
      this.filters = [];
      this.orderBy = null;
      this.limitCount = null;
      this.insertRow = null;
      this.updatePatch = null;
      this.singleRequired = false;
    }
    select() { return this; }
    eq(column, value) { this.filters.push([column, value]); return this; }
    order(column, options = {}) {
      this.orderBy = { column, ascending: options.ascending !== false };
      return this;
    }
    limit(count) { this.limitCount = count; return this; }
    maybeSingle() { return Promise.resolve(executeQuery(this)); }
    single() { this.singleRequired = true; return Promise.resolve(executeQuery(this)); }
    insert(row) { this.op = 'insert'; this.insertRow = row; return this; }
    update(patch) { this.op = 'update'; this.updatePatch = patch; return this; }
  }

  const client = { from: (table) => new Query(table) };

  const context = {
    URL, Request, Response, TextEncoder, Uint8Array, console, crypto,
    createRemoteJWKSet: () => ({ kind: 'mock-jwks' }),
    jwtVerify: async (token, jwks, options) => {
      assert.equal(token, TOKEN_JWT);
      assert.equal(jwks.kind, 'mock-jwks');
      assert.equal(options.issuer, 'https://token.actions.githubusercontent.com');
      assert.equal(options.audience, 'nayanet-runtime');
      return { payload: claims };
    },
    createClient: (url, key) => {
      assert.equal(url, 'https://supabase.example');
      assert.equal(key, 'service-role-key');
      return client;
    },
    Deno: {
      env: {
        get: (key) => ({
          SUPABASE_URL: 'https://supabase.example',
          SUPABASE_SERVICE_ROLE_KEY: 'service-role-key',
        }[key] ?? ''),
      },
      serve: (callback) => { handler = callback; },
    },
  };

  const code = stripTypeScriptTypes(sourceTransform(SOURCE.replace(/^import .*;\r?\n/gm, '')));
  vm.runInNewContext(code, context, { filename: 'nayanet-verified-ai-action/index.ts' });
  assert.ok(handler, 'Deno.serve registered the production handler');

  const post = async (body) => {
    const req = new Request('https://supabase.example/functions/v1/nayanet-verified-ai-action', {
      method: 'POST',
      headers: {
        authorization: 'Bearer ' + TOKEN_JWT,
        'content-type': 'application/json',
      },
      body: JSON.stringify(body),
    });
    const res = await handler(req);
    return { status: res.status, body: await res.json() };
  };

  return { post, rows };
}

const executeBody = (overrides = {}) => ({
  mode: 'execute',
  authority_grant_id: GRANT_ID,
  idempotency_key: 'gate-1-replay-key',
  ...overrides,
});

async function assertReplaySafety(options = {}) {
  const { post, rows } = makeRuntime(options);
  const first = await post(executeBody());
  assert.equal(first.status, 200);
  assert.equal(first.body.status, 'EXECUTED');
  assert.equal(first.body.idempotent_replay, undefined);

  const second = await post(executeBody());
  assert.equal(second.status, 200);
  assert.equal(second.body.status, 'EXECUTED');
  assert.equal(second.body.idempotent_replay, true);
  assert.equal(rows.nayanet_execution_receipts.length, 1);
  assert.equal(rows.nayanet_execution_outcomes.length, 1);
  assert.equal(rows.nayanet_execution_receipts[0].idempotency_key, 'gate-1-replay-key');
  assert.equal(second.body.receipt.id, first.body.receipt.id);
}

test('G1 execution crosses the canonical production handler and requires an idempotency key', async () => {
  const { post, rows } = makeRuntime();
  const result = await post(executeBody({ idempotency_key: '' }));
  assert.equal(result.status, 400);
  assert.equal(result.body.error, 'IDEMPOTENCY_KEY_REQUIRED');
  assert.equal(rows.nayanet_execution_receipts.length, 0);
  assert.equal(rows.nayanet_execution_outcomes.length, 0);
});

test('G1 same key + same request yields one durable receipt and replay', async () => {
  await assertReplaySafety();
});

test('G1 same key + different request fingerprint is refused', async () => {
  const { post, rows } = makeRuntime();
  const first = await post(executeBody());
  assert.equal(first.status, 200);

  const conflict = await post(executeBody({ authority_grant_id: ALT_GRANT_ID }));
  assert.equal(conflict.status, 409);
  assert.equal(conflict.body.error, 'IDEMPOTENCY_KEY_REUSE_CONFLICT');
  assert.equal(rows.nayanet_execution_receipts.length, 1);
  assert.equal(rows.nayanet_execution_outcomes.length, 1);
});

test('G1 deliberate key-population falsifier turns the replay gate RED', async () => {
  const broken = (source) => source.replace(
    'idempotency_key: idempotencyKey',
    'idempotency_key: undefined',
  );
  await assert.rejects(
    () => assertReplaySafety({ sourceTransform: broken }),
    /Expected values to be strictly equal|replay|gate-1-replay-key/i,
  );
});

test('G1 deliberate required-key-guard falsifier turns the missing-key gate RED', async () => {
  const broken = (source) => source.replace(
    'if (!idempotencyKey) {',
    'if (false && !idempotencyKey) {',
  );
  await assert.rejects(
    async () => {
      const { post } = makeRuntime({ sourceTransform: broken });
      const result = await post(executeBody({ idempotency_key: '' }));
      assert.equal(result.status, 400);
      assert.equal(result.body.error, 'IDEMPOTENCY_KEY_REQUIRED');
    },
    /Expected values to be strictly equal|IDEMPOTENCY_KEY_REQUIRED/i,
  );
});

test('G1 deliberate database-uniqueness falsifier turns the replay gate RED', async () => {
  await assert.rejects(
    () => assertReplaySafety({ enforceUnique: false }),
    /Expected values to be strictly equal|replay|gate-1-replay-key/i,
  );
});

test('G1 canonical migration declares the database uniqueness boundary', () => {
  assert.match(
    MIGRATION_SOURCE,
    /CREATE UNIQUE INDEX IF NOT EXISTS nayanet_execution_receipts_idempotency_key_uidx/i,
  );
  assert.match(
    MIGRATION_SOURCE,
    /ON public\.nayanet_execution_receipts \(idempotency_key\)/i,
  );
  assert.match(
    MIGRATION_SOURCE,
    /WHERE idempotency_key IS NOT NULL/i,
  );
});

test('G1 executor does not self-certify independent verification', async () => {
  const { post } = makeRuntime();
  const result = await post(executeBody());
  assert.equal(result.body.outcome.verified, false);
  assert.equal(result.body.outcome.verification_method, 'PENDING_INDEPENDENT_RUNTIME_VERIFICATION');
  assert.notEqual(result.body.independent_verification, true);
});
