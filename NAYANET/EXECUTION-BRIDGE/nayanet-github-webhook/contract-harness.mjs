import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { createHmac } from 'node:crypto';
import { pathToFileURL } from 'node:url';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const SOURCE_PATH = new URL('./index.ts', import.meta.url);
const SECRET = 'test-only-webhook-secret-no-production-value';
const OWNER = '36f8f43c-2a5e-4b0f-9c6d-000000000001';
const INSTALLATION = 12345678;
const REPO = 'SoulSchoolAcademy/NayaPOWER';

let src = readFileSync(SOURCE_PATH, 'utf8');
src = src.replace(/^import\s+"jsr:[^\n]*\n/m, '');
src = src.replace(/^import\s*\{[^}]*\}\s*from\s*"[^\n]*"\s*;\s*\n/m, '');

const envMap = { GITHUB_WEBHOOK_SECRET: SECRET, SUPABASE_URL: 'https://dahisasgpfvziswqvmvm.supabase.co', SUPABASE_SERVICE_ROLE_KEY: 'test' };
let handler = null;
let rpcLog = [];
let resolverResults = [];
let recordResults = [];

globalThis.Deno = {
  env: { get: (k) => (k in envMap ? envMap[k] : null) },
  serve: (fn) => { handler = fn; },
};
globalThis.createClient = (url, key, opts) => ({
  rpc: async (name, args) => {
    rpcLog.push({ name, args });
    if (name === 'nayanet_resolve_github_webhook_owner') return resolverResults.shift() || { data: null, error: { message: 'NO_ACTIVE_UNAMBIGUOUS_BINDING' } };
    if (name === 'nayanet_record_cognition_event') return recordResults.shift() || { data: { replayed: false }, error: null };
    return { data: null, error: { message: 'UNEXPECTED_RPC:' + name } };
  },
});

const buildPath = join(tmpdir(), 'coda3-webhook-harness');
mkdirSync(buildPath, { recursive: true });
const buildFile = join(buildPath, 'edge-function.ts');
writeFileSync(buildFile, src);
await import(pathToFileURL(buildFile));
if (!handler) throw new Error('Deno.serve handler not captured');

function sign(secret, body) { return 'sha256=' + createHmac('sha256', secret).update(body).digest('hex'); }

function pushPayload(overrides = {}) {
  return {
    action: null,
    ref: 'refs/heads/main',
    after: '9f8f0a5e2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e',
    repository: { full_name: REPO },
    installation: { id: INSTALLATION },
    head_commit: { message: 'chore: adapter observability proof\n\nThis is the body line of the commit message.', timestamp: '2026-09-24T18:00:00Z' },
    pusher: { name: 'shawn' },
    sender: { login: 'SoulSchoolAcademy' },
    ...overrides,
  };
}

async function call({ method = 'POST', delivery = null, signature = null, body = null, rawBody = undefined }) {
  const headers = {};
  if (delivery) headers['x-github-delivery'] = delivery;
  if (signature) headers['x-hub-signature-256'] = signature;
  const text = rawBody ?? (body === null ? null : JSON.stringify(body));
  const hasBody = text !== null && method !== 'GET' && method !== 'HEAD';
  const req = new Request('https://edge.test/nayanet-github-webhook', { method, headers: { ...headers, ...(hasBody ? { 'content-type': 'application/json' } : {}) }, ...(hasBody ? { body: text } : {}) });
  const res = await handler(req);
  const raw = await res.text().catch(() => null);
  let json = null;
  try { json = JSON.parse(raw); } catch {}
  return { status: res.status, json, text: raw };
}

const passed = [];
const failed = [];
function check(name, cond, extra = {}) {
  if (cond) passed.push(name);
  else failed.push({ name, extra });
  console.log((cond ? 'PASS' : 'FAIL') + '  ' + name + (cond ? '' : '  ' + JSON.stringify(extra)));
}

function resetEnv() {
  delete envMap.GITHUB_WEBHOOK_SECRET;
  delete envMap.SUPABASE_URL;
  delete envMap.SUPABASE_SERVICE_ROLE_KEY;
}
function setEnv(partial) { resetEnv(); Object.assign(envMap, partial); }

// --- OPTIONS preflight ---
{
  setEnv({ GITHUB_WEBHOOK_SECRET: SECRET, SUPABASE_URL: 'https://dahisasgpfvziswqvmvm.supabase.co', SUPABASE_SERVICE_ROLE_KEY: 'test' });
  const r = await call({ method: 'OPTIONS' });
  check('OPTIONS preflight returns 200 ok', r.status === 200 && r.text === 'ok', r);
}
// --- method not allowed ---
{
  setEnv({ GITHUB_WEBHOOK_SECRET: SECRET });
  const r = await call({ method: 'GET', delivery: 'delivery-1', body: {} });
  check('non-POST returns 405 METHOD_NOT_ALLOWED', r.status === 405 && r.json?.error === 'METHOD_NOT_ALLOWED', r);
}
// --- missing secret (external boundary) ---
{
  resetEnv(); setEnv({});
  const delivery = 'delivery-secret-missing';
  const body = pushPayload();
  const r = await call({ delivery, signature: sign('anything', JSON.stringify(body)), body });
  check('missing secret -> 503 GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED', r.status === 503 && r.json?.error === 'GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED' && r.json?.status === 'BLOCKED_EXTERNAL_CREDENTIAL', r);
}
// --- missing delivery id ---
{
  setEnv({ GITHUB_WEBHOOK_SECRET: SECRET, SUPABASE_URL: 'x', SUPABASE_SERVICE_ROLE_KEY: 'x' });
  const body = pushPayload();
  const r = await call({ delivery: null, signature: sign(SECRET, JSON.stringify(body)), body });
  check('missing delivery -> 400 GITHUB_DELIVERY_ID_REQUIRED', r.status === 400 && r.json?.error === 'GITHUB_DELIVERY_ID_REQUIRED', r);
}
// --- invalid signature ---
{
  setEnv({ GITHUB_WEBHOOK_SECRET: SECRET, SUPABASE_URL: 'x', SUPABASE_SERVICE_ROLE_KEY: 'x' });
  const body = pushPayload();
  const r = await call({ delivery: 'delivery-bad-sig', signature: 'sha256=' + '0'.repeat(64), body });
  check('invalid signature -> 401 INVALID_GITHUB_SIGNATURE', r.status === 401 && r.json?.error === 'INVALID_GITHUB_SIGNATURE', r);
  const r2 = await call({ delivery: 'delivery-bad-format', signature: 'hmac-whatever', body });
  check('malformed signature format -> 401 INVALID_GITHUB_SIGNATURE', r2.status === 401 && r2.json?.error === 'INVALID_GITHUB_SIGNATURE', r2);
}
// --- invalid JSON ---
{
  setEnv({ GITHUB_WEBHOOK_SECRET: SECRET, SUPABASE_URL: 'x', SUPABASE_SERVICE_ROLE_KEY: 'x' });
  const raw = 'this is not json';
  const r = await call({ delivery: 'delivery-invalid-json', signature: sign(SECRET, raw), rawBody: raw });
  check('invalid JSON -> 400 INVALID_JSON', r.status === 400 && r.json?.error === 'INVALID_JSON', r);
}
// --- missing installation id ---
{
  setEnv({ GITHUB_WEBHOOK_SECRET: SECRET, SUPABASE_URL: 'x', SUPABASE_SERVICE_ROLE_KEY: 'x' });
  const body = pushPayload({ installation: undefined });
  const r = await call({ delivery: 'delivery-no-install', signature: sign(SECRET, JSON.stringify(body)), body });
  check('missing installation -> 403 GITHUB_OWNER_BINDING_REQUIRED', r.status === 403 && r.json?.error === 'GITHUB_OWNER_BINDING_REQUIRED' && r.json?.status === 'BLOCKED_OWNER_BINDING', r);
}
// --- missing repository ---
{
  setEnv({ GITHUB_WEBHOOK_SECRET: SECRET, SUPABASE_URL: 'x', SUPABASE_SERVICE_ROLE_KEY: 'x' });
  const body = pushPayload({ repository: { full_name: '' } });
  const r = await call({ delivery: 'delivery-no-repo', signature: sign(SECRET, JSON.stringify(body)), body });
  check('missing repository -> 403 GITHUB_OWNER_BINDING_REQUIRED', r.status === 403 && r.json?.error === 'GITHUB_OWNER_BINDING_REQUIRED' && r.json?.status === 'BLOCKED_OWNER_BINDING', r);
}
// --- missing supabase credentials ---
{
  resetEnv(); setEnv({ GITHUB_WEBHOOK_SECRET: SECRET });
  const body = pushPayload();
  const r = await call({ delivery: 'delivery-no-supabase', signature: sign(SECRET, JSON.stringify(body)), body });
  check('missing supabase credentials -> 503 SUPABASE_SERVICE_ROLE_NOT_CONFIGURED', r.status === 503 && r.json?.error === 'SUPABASE_SERVICE_ROLE_NOT_CONFIGURED' && r.json?.status === 'BLOCKED_EXTERNAL_CREDENTIAL', r);
}
// --- unresolved owner ---
{
  setEnv({ GITHUB_WEBHOOK_SECRET: SECRET, SUPABASE_URL: 'https://dahisasgpfvziswqvmvm.supabase.co', SUPABASE_SERVICE_ROLE_KEY: 'test' });
  resolverResults = [{ data: null, error: { message: 'GITHUB_BINDING_NOT_FOUND' } }];
  const body = pushPayload();
  const r = await call({ delivery: 'delivery-unresolved', signature: sign(SECRET, JSON.stringify(body)), body });
  check('unresolved owner -> 403 GITHUB_OWNER_BINDING_NOT_RESOLVED', r.status === 403 && r.json?.error === 'GITHUB_OWNER_BINDING_NOT_RESOLVED' && r.json?.status === 'BLOCKED_OWNER_BINDING' && r.json?.detail === 'GITHUB_BINDING_NOT_FOUND', r);
}
// --- successful normalization + persistence (PERSISTED) ---
{
  setEnv({ GITHUB_WEBHOOK_SECRET: SECRET, SUPABASE_URL: 'https://dahisasgpfvziswqvmvm.supabase.co', SUPABASE_SERVICE_ROLE_KEY: 'test' });
  resolverResults = [{ data: OWNER, error: null }];
  recordResults = [{ data: { replayed: false }, error: null }];
  rpcLog = [];
  const delivery = 'delivery-ok-1';
  const body = pushPayload();
  const r = await call({ delivery, signature: sign(SECRET, JSON.stringify(body)), body });
  check('bound owner persisted -> 200 PERSISTED', r.status === 200 && r.json?.ok === true && r.json?.status === 'PERSISTED' && r.json?.event_id === 'github:' + delivery && r.json?.owner_id === OWNER && r.json?.repository === REPO, r);

  const resolveCall = rpcLog.find((x) => x.name === 'nayanet_resolve_github_webhook_owner');
  check('resolver called with installation+repository', resolveCall && resolveCall.args.p_installation_id === INSTALLATION && resolveCall.args.p_repository === REPO, resolveCall?.args);
  const recordCall = rpcLog.find((x) => x.name === 'nayanet_record_cognition_event');
  const auth = recordCall?.args?.p_execution_authorization;
  check('canonical receiver called with github webhook authorization', auth && auth.source === 'github_app_webhook' && auth.actor_id === OWNER && auth.installation_id === String(INSTALLATION) && auth.repository === REPO && auth.verification === 'SIGNED_GITHUB_WEBHOOK', auth);
  check('receiver action is github_webhook_received', recordCall?.args?.p_action === 'github_webhook_received', recordCall?.args);

  const ev = recordCall?.args?.p_event;
  check('normalized event is renderable in Feed/Activity', ev
    && String(ev.title).includes('github.webhook') && String(ev.title).includes(REPO)
    && ev.content.includes('chore: adapter observability proof')
    && ev.content.includes('This is the body line of the commit message.')
    && ev.content.includes('commit 9f8f0a5e')
    && ev.type === 'github.webhook'
    && ev.classification === 'observation'
    && ev.created_at === '2026-09-24T18:00:00Z'
    && ev.schema_version === '2.0.0'
    && ev.idempotency_key === 'github:' + delivery
    && ev.event_id === 'github:' + delivery
    && ev.metadata?.event_type === 'github.webhook'
    && ev.metadata?.source === 'github_webhook', ev);
  check('normalized event preserves smart-connect privacy (no repository identity in display content)', ev && !ev.content.includes('shawn') && !String(ev.title).includes('shawn'), ev);
}
// --- duplicate delivery -> REPLAYED (idempotency) ---
{
  setEnv({ GITHUB_WEBHOOK_SECRET: SECRET, SUPABASE_URL: 'https://dahisasgpfvziswqvmvm.supabase.co', SUPABASE_SERVICE_ROLE_KEY: 'test' });
  resolverResults = [{ data: OWNER, error: null }];
  recordResults = [{ data: { replayed: false }, error: null }];
  const delivery = 'delivery-dup-1';
  const body = pushPayload();
  const first = await call({ delivery, signature: sign(SECRET, JSON.stringify(body)), body });
  recordResults = [{ data: { replayed: true }, error: null }];
  resolverResults = [{ data: OWNER, error: null }];
  const second = await call({ delivery, signature: sign(SECRET, JSON.stringify(body)), body });
  check('first delivery -> PERSISTED', first.status === 200 && first.json?.status === 'PERSISTED', first);
  check('duplicate delivery -> REPLAYED (no duplicate intelligence)', second.status === 200 && second.json?.status === 'REPLAYED' && second.json?.event_id === 'github:' + delivery, second);
}
// --- persistence failure -> 502 ---
{
  setEnv({ GITHUB_WEBHOOK_SECRET: SECRET, SUPABASE_URL: 'https://dahisasgpfvziswqvmvm.supabase.co', SUPABASE_SERVICE_ROLE_KEY: 'test' });
  resolverResults = [{ data: OWNER, error: null }];
  recordResults = [{ data: null, error: { message: 'receiver rejected event' } }];
  const body = pushPayload();
  const r = await call({ delivery: 'delivery-fail-persist', signature: sign(SECRET, JSON.stringify(body)), body });
  check('persistence failure -> 502 CANONICAL_EVENT_PERSISTENCE_FAILED', r.status === 502 && r.json?.error === 'CANONICAL_EVENT_PERSISTENCE_FAILED' && r.json?.status === 'PERSISTENCE_FAILED', r);
}

console.log('\nRESULT ' + passed.length + ' passed, ' + failed.length + ' failed');
if (failed.length) { console.log(JSON.stringify(failed, null, 2)); process.exitCode = 1; }