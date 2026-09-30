import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import { test } from 'node:test';
import vm from 'node:vm';

const source = readFileSync(new URL('../supabase/functions/nayanet-github-dispatch/index.ts', import.meta.url), 'utf8');
const code = stripTypeScriptTypes(source.replace(/^import .*;\r?\n/gm, ''));

const USER_ID = '11111111-2222-4333-8444-555555555555';
const TX_ID = 'aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee';
const GRANT_ID = '99999999-8888-4777-8666-555555555555';
const IB_ID = 'IB-000042';
const IDEM = 'smart-note-projection:' + TX_ID;
const CALLER_LINK_RE = /^https:\/\/github\.com\/SoulSchoolAcademy\/NayaPOWER\/blob\/main\/.+\/IB-\d{6}\/smart-note\.md$/;

const TX_ROW = {
  id: TX_ID,
  user_id: USER_ID,
  created_at: '2026-09-30T10:00:00.000Z',
  intelligent_block: {
    identity: { intelligent_block_id: IB_ID, event_id: 'ev-1' },
    meaning: { subject: 'Test subject', in_a_nutshell: 'The nutshell.' },
    perspectives: { human: 'h', naya: 'n', child: 'c', grandma: 'g', machine: 'm', meaning: 'wm', connections: 'hc', application: 'ha', value: 'v' },
    provenance: { source: 'test', source_ref: 'smart_note:ev-1', captured_by: USER_ID },
    truth: { state: 'SUPPORTED' },
    authority: { state: 'AUTHORIZED', authority_ref: 'authenticated_owner_capture', constraints: ['owner_only'] },
    evidence: { evidence_state: 'OBSERVED', verification: 'ok' },
    learning: { lesson: 'lesson text' },
    metadata: { projection_category: 'system', projection_topic: 'test-topic' },
  },
};

const GRANT_ROW = {
  grant_id: GRANT_ID,
  status: 'ACTIVE',
  expires_at: new Date(Date.now() + 600000).toISOString(),
  actions: ['smart_note_github_projection'],
  scope: { target: TX_ID },
  issuer_id: USER_ID,
  subject_id: USER_ID,
};

function runtime(opts = {}) {
  const { token = 'gh-test-token', grant = GRANT_ROW, tx = TX_ROW, receipt = null } = opts;
  let handler;
  const receipts = new Map();
  const blobs = new Map();
  if (receipt) receipts.set(receipt.idempotency_key, { ...receipt });
  const githubCalls = [];

  const table = (name) => {
    if (name === 'nayanet_github_dispatch_receipts') {
      return {
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
          return {
            eq: (col, val) => ({
              maybeSingle: async () => ({ data: receipts.get(val) || null, error: null }),
            }),
          };
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
              return {
                then: (resolve) => resolve(result()),
                select: () => ({ single: async () => result() }),
                single: async () => result(),
              };
            },
          };
        },
      };
    }
    if (name === 'nayanet_authority_grants') {
      return {
        select() {
          return {
            eq: () => ({
              maybeSingle: async () => ({ data: grant, error: null }),
            }),
          };
        },
      };
    }
    if (name === 'v7_smart_note_transactions') {
      return {
        select() {
          return {
            eq: () => ({
              maybeSingle: async () => ({ data: tx, error: null }),
            }),
          };
        },
      };
    }
    throw new Error('unexpected table ' + name);
  };

  // make update().eq() awaitable-with-single: emulate supabase builder
  const wrapUpdate = (t) => t;
  void wrapUpdate;

  const context = {
    URL, Request, Response, console, btoa, TextEncoder, crypto,
    Deno: {
      env: {
        get: (key) => ({
          SUPABASE_URL: 'https://offline.invalid',
          SUPABASE_ANON_KEY: 'anon-key',
          SUPABASE_SERVICE_ROLE_KEY: 'service-key',
          GITHUB_TOKEN: token,
        }[key] || ''),
      },
      serve: (cb) => { handler = cb; },
    },
    createClient: (url, key) => key === 'service-key'
      ? { from: table }
      : {
          auth: { getUser: async () => ({ data: { user: { id: USER_ID } }, error: null }) },
          from: table,
        },
    fetch: async (url, init = {}) => {
      githubCalls.push({ url: String(url), method: init.method || 'GET' });
      const u = String(url);
      if (u.startsWith('https://api.github.com/repos/SoulSchoolAcademy/NayaPOWER/contents/')) {
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
  return { post, handler, receipts, githubCalls };
}

const validBody = () => ({
  operation: 'project_smart_note',
  transaction_id: TX_ID,
  authority_grant_id: GRANT_ID,
  approval: 'EXPLICIT_APPROVAL_GRANTED',
  idempotency_key: IDEM,
});

test('rejects non-POST with 405', async () => {
  const { handler } = runtime();
  const res = await handler(new Request('https://offline.invalid/', { method: 'GET' }));
  assert.equal(res.status, 405);
  assert.equal((await res.json()).error, 'METHOD_NOT_ALLOWED');
});

test('requires Authorization', async () => {
  const { handler } = runtime();
  const res = await handler(new Request('https://offline.invalid/', { method: 'POST' }));
  assert.equal(res.status, 401);
});

test('rejects unknown operation', async () => {
  const { post } = runtime();
  const { status, body } = await post({ operation: 'delete_everything' });
  assert.equal(status, 400);
  assert.equal(body.error, 'UNKNOWN_OPERATION');
});

test('refuses when authority grant is absent', async () => {
  const { post, receipts } = runtime({ grant: null });
  const { status, body } = await post(validBody());
  assert.equal(status, 403);
  assert.equal(body.error, 'PROJECTION_AUTHORITY_REFUSED');
  assert.equal(body.pipeline, 'PROJECTION_REFUSED');
  assert.equal(receipts.get(IDEM).status, 'failed');
});

test('refuses when grant is scoped to another transaction', async () => {
  const { post } = runtime({ grant: { ...GRANT_ROW, scope: { target: 'other-tx' } } });
  const { status, body } = await post(validBody());
  assert.equal(status, 403);
  assert.equal(body.error, 'PROJECTION_AUTHORITY_REFUSED');
});

test('fail-closed 503 when GITHUB_TOKEN is not configured', async () => {
  const { post, receipts, githubCalls } = runtime({ token: '' });
  const { status, body } = await post(validBody());
  assert.equal(status, 503);
  assert.equal(body.error, 'GITHUB_CREDENTIAL_NOT_CONFIGURED');
  assert.equal(body.pipeline, 'PROJECTION_BLOCKED');
  assert.equal(githubCalls.length, 0, 'no GitHub call without credential');
  assert.equal(receipts.get(IDEM).status, 'blocked');
});

test('happy path returns PROJECTION_VERIFIED with caller-compatible smart_link', async () => {
  const { post, receipts, githubCalls } = runtime();
  const { status, body } = await post(validBody());
  assert.equal(status, 200);
  assert.equal(body.ok, true);
  assert.equal(body.pipeline, 'PROJECTION_VERIFIED');
  assert.ok(CALLER_LINK_RE.test(body.smart_link), 'smart_link matches caller regex: ' + body.smart_link);
  assert.ok(body.smart_link.includes('/' + IB_ID + '/smart-note.md'));
  assert.ok(body.receipt.id);
  assert.ok(body.projection_verification.completed_at);
  assert.equal(body.projection_verification.commit_sha, 'blobsha123');
  const puts = githubCalls.filter((c) => c.method === 'PUT');
  assert.equal(puts.length, 1);
  assert.ok(puts[0].url.endsWith('/' + IB_ID + '/smart-note.md'), 'PUT targets the IB path');
  assert.equal(receipts.get(IDEM).status, 'completed');
});

test('idempotent replay returns stored receipt without touching GitHub', async () => {
  const stored = {
    id: 'receipt-0',
    idempotency_key: IDEM,
    status: 'completed',
    smart_link: 'https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/x/IB-000042/smart-note.md',
    commit_sha: 'blobsha123',
    completed_at: '2026-09-30T10:05:00.000Z',
  };
  const { post, githubCalls } = runtime({ receipt: stored });
  const { status, body } = await post(validBody());
  assert.equal(status, 200);
  assert.equal(body.ok, true);
  assert.equal(body.pipeline, 'PROJECTION_VERIFIED');
  assert.equal(body.smart_link, stored.smart_link);
  assert.equal(body.replayed, true);
  assert.equal(githubCalls.length, 0, 'no GitHub call on replay');
});
