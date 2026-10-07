import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import { test } from 'node:test';
import vm from 'node:vm';

// EXECUTED coverage for the 2026-10-07 production repair of the
// TRANSACTION_NOT_FOUND seam in nayanet-github-dispatch.
//
// Production evidence: the function booted but every projection returned 404
// TRANSACTION_NOT_FOUND even though the transaction row existed. Root cause:
// the transaction lookup used the user-scoped client, which cannot see
// v7_smart_note_transactions under the live RLS contract. The repair reads the
// row with the service-role client and keeps the explicit in-code ownership
// check, so the boundary is enforced without depending on RLS visibility.

const source = readFileSync(new URL('../supabase/functions/nayanet-github-dispatch/index.ts', import.meta.url), 'utf8');
const code = stripTypeScriptTypes(source.replace(/^import .*;\r?\n/gm, ''));

const USER_ID = '11111111-2222-4333-8444-555555555555';
const OTHER_USER_ID = '99999999-8888-4777-8666-000000000000';
const TX_ID = 'aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee';
const GRANT_ID = '99999999-8888-4777-8666-555555555555';
const IB_ID = 'IB-000042';
const IDEM = 'smart-note-projection:' + TX_ID;

const txRow = (ownerId) => ({
  id: TX_ID,
  user_id: ownerId,
  created_at: '2026-09-30T10:00:00.000Z',
  intelligent_block: {
    identity: { intelligent_block_id: IB_ID, event_id: 'ev-1' },
    meaning: { subject: 'Test subject', in_a_nutshell: 'The nutshell.' },
    perspectives: { human: 'h', naya: 'n', child: 'c', grandma: 'g', machine: 'm', meaning: 'wm', connections: 'hc', application: 'ha', value: 'v' },
    provenance: { source: 'test', source_ref: 'smart_note:ev-1', captured_by: ownerId },
    truth: { state: 'SUPPORTED' },
    authority: { state: 'AUTHORIZED', authority_ref: 'authenticated_owner_capture', constraints: ['owner_only'] },
    evidence: { evidence_state: 'OBSERVED', verification: 'ok' },
    learning: { lesson: 'lesson text' },
    metadata: { projection_category: 'system', projection_topic: 'test-topic' },
  },
});

const GRANT_ROW = {
  grant_id: GRANT_ID,
  status: 'ACTIVE',
  expires_at: new Date(Date.now() + 600000).toISOString(),
  actions: ['smart_note_github_projection'],
  scope: { target: TX_ID },
  issuer_id: USER_ID,
  subject_id: USER_ID,
};

// Simulates the LIVE RLS contract: the user-scoped client sees NOTHING on
// v7_smart_note_transactions (the production seam); the service-role client
// sees the row. `txOwner` controls who owns the row the service client returns.
function runtime({ txOwner = USER_ID } = {}) {
  let handler;
  const receipts = new Map();
  const blobs = new Map();
  const githubCalls = [];

  const receiptsTable = {
    insert(row) {
      return {
        select() {
          return {
            maybeSingle: async () => {
              if (receipts.has(row.idempotency_key)) {
                const e = new Error('duplicate');
                e.code = '23505';
                return { data: null, error: e };
              }
              const saved = { id: 'receipt-' + receipts.size, ...row };
              receipts.set(row.idempotency_key, saved);
              return { data: saved, error: null };
            },
          };
        },
      };
    },
    select() {
      return { eq: (col, val) => ({ maybeSingle: async () => ({ data: receipts.get(val) || null, error: null }) }) };
    },
    update(patch) {
      return {
        eq: (col, val) => {
          const result = () => {
            const cur = receipts.get(val);
            if (!cur) return { data: null, error: new Error('missing') };
            receipts.set(val, { ...cur, ...patch });
            return { data: receipts.get(val), error: null };
          };
          return { then: (resolve) => resolve(result()), select: () => ({ single: async () => result() }) };
        },
      };
    },
  };

  const from = (isAdmin) => (name) => {
    if (name === 'nayanet_github_dispatch_receipts') return receiptsTable;
    if (name === 'nayanet_authority_grants') {
      return { select() { return { eq: () => ({ maybeSingle: async () => ({ data: GRANT_ROW, error: null }) }) }; } };
    }
    if (name === 'v7_smart_note_transactions') {
      return {
        select() {
          return {
            eq: () => ({
              // RLS reality: user-scoped client sees nothing; service role sees the row.
              maybeSingle: async () => (isAdmin ? { data: txRow(txOwner), error: null } : { data: null, error: null }),
            }),
          };
        },
      };
    }
    throw new Error('unexpected table ' + name);
  };

  const context = {
    URL, Request, Response, console, btoa, TextEncoder, crypto,
    Deno: {
      env: {
        get: (key) => ({
          SUPABASE_URL: 'https://offline.invalid',
          SUPABASE_ANON_KEY: 'anon-key',
          SUPABASE_SERVICE_ROLE_KEY: 'service-key',
          GITHUB_TOKEN: 'legacy-token',
        }[key] || ''),
      },
      serve: (cb) => { handler = cb; },
    },
    createClient: (url, key) => {
      const isAdmin = key === 'service-key';
      return {
        auth: { getUser: async () => ({ data: { user: { id: USER_ID } }, error: null }) },
        from: from(isAdmin),
      };
    },
    fetch: async (url, init = {}) => {
      githubCalls.push({ url: String(url), method: init.method || 'GET' });
      const u = String(url);
      if (u.includes('/contents/')) {
        const path = u.split('/contents/')[1].split('?')[0];
        if ((init.method || 'GET') === 'PUT') {
          blobs.set(path, 'blobsha123');
          return new Response(JSON.stringify({ content: { sha: 'blobsha123' } }), { status: 201 });
        }
        if (blobs.has(path)) {
          return new Response(JSON.stringify({ sha: blobs.get(path), path }), { status: 200 });
        }
        return new Response(JSON.stringify({ message: 'Not Found' }), { status: 404 });
      }
      throw new Error('unexpected fetch ' + u);
    },
  };
  vm.runInNewContext(code, context);
  assert.ok(handler, 'Deno.serve handler registered');

  const post = (bodyObj, headers = {}) => {
    const req = new Request('https://offline.invalid/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: 'Bearer user-jwt', ...headers },
      body: JSON.stringify(bodyObj),
    });
    return handler(req).then(async (res) => ({ status: res.status, body: await res.json() }));
  };
  return { post, receipts };
}

const validBody = () => ({
  operation: 'project_smart_note',
  transaction_id: TX_ID,
  authority_grant_id: GRANT_ID,
  approval: 'EXPLICIT_APPROVAL_GRANTED',
  idempotency_key: IDEM,
});

test('RLS-hidden transaction row resolves via the service-role read (production 404 repair)', async () => {
  // The user-scoped client sees null (live RLS); the old code 404'd here.
  const { post } = runtime({ txOwner: USER_ID });
  const { status, body } = await post(validBody());
  assert.equal(status, 200);
  assert.equal(body.ok, true);
  assert.equal(body.pipeline, 'PROJECTION_VERIFIED');
  assert.ok(body.smart_link.includes('/' + IB_ID + '/smart-note.md'));
});

test('negative control: another user\u2019s transaction row is still refused fail-closed', async () => {
  // The service-role read sees the row, but the in-code ownership check must
  // fire — the repair must not widen authority to other owners' transactions.
  const { post, receipts } = runtime({ txOwner: OTHER_USER_ID });
  const { status, body } = await post(validBody());
  assert.equal(status, 404);
  assert.equal(body.error, 'TRANSACTION_NOT_FOUND');
  assert.equal(body.pipeline, 'PROJECTION_REFUSED');
  assert.equal(receipts.get(IDEM).status, 'failed');
});
