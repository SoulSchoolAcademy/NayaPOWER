// Conversational Intake v1 (element #13, step 12) — module tests, node --test.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { createHash } from 'node:crypto';

const require = createRequire(import.meta.url);
const NI = require('../HUB/app/js/naya-intake.js');

const sha = (s) => createHash('sha256').update(s, 'utf8').digest('hex');

function completeWelcome(via = 'tap') {
  const s = NI.createSession('welcome', { ownerAlias: 'naya' });
  s.start();
  if (via === 'voice') {
    assert.equal(s.answer('  Maria  ', 'voice').ok, true); // name by voice
    assert.equal(s.answer('MARIA@Example.com', 'voice').ok, true); // email by voice
    assert.equal(s.answer('build my own app', 'voice').ok, true); // choice by voice
    assert.equal(s.answer('I run a bakery', 'voice').ok, true); // note by voice
  } else {
    assert.equal(s.answer('Maria').ok, true);
    assert.equal(s.answer('maria@example.com').ok, true);
    assert.equal(s.answer('build').ok, true);
    assert.equal(s.answer('I run a bakery').ok, true);
  }
  return s;
}

test('flows: one question at a time, in order, progress felt', () => {
  const s = NI.createSession('welcome', { ownerAlias: 'naya' });
  assert.equal(s.state().totalSteps, 4);
  assert.equal(s.state().step.key, 'name');
  assert.deepEqual(s.progress(), { current: 1, total: 4, answered: 0, pct: 0 });
  s.answer('Maria');
  assert.equal(s.state().step.key, 'email');
  assert.equal(s.progress().pct, 25);
  s.answer('maria@example.com');
  assert.equal(s.state().step.key, 'intent');
  s.answer('build');
  assert.equal(s.state().step.key, 'note');
  s.answer('hi');
  assert.equal(s.state().status, 'ready');
  assert.equal(s.progress().pct, 100);
});

test('validation: bad email and bad choice never advance', () => {
  const s = NI.createSession('welcome', { ownerAlias: 'naya' });
  s.answer('Maria');
  assert.equal(s.answer('not-an-email').reason, 'bad_email');
  assert.equal(s.state().step.key, 'email'); // still on the same question
  assert.equal(s.answer('maria@example.com').ok, true);
  assert.equal(s.answer('banana').reason, 'bad_choice');
  assert.equal(s.answer('learn').ok, true);
});

test('back: always allowed, answers kept', () => {
  const s = NI.createSession('welcome', { ownerAlias: 'naya' });
  s.answer('Maria');
  s.answer('maria@example.com');
  assert.equal(s.back().ok, true);
  assert.equal(s.state().step.key, 'email');
  assert.equal(s.state().answers.name, 'Maria');
  assert.equal(s.back().ok, true);
  assert.equal(s.back().reason, 'at_start');
});

test('optional step: skippable; required steps are not', () => {
  const s = NI.createSession('invite_accept', { ownerAlias: 'naya' });
  assert.equal(s.skip().reason, 'not_optional'); // email is required
  const w = completeWelcome();
  assert.equal(w.state().status, 'ready');
  const w2 = NI.createSession('welcome', { ownerAlias: 'naya' });
  w2.answer('A');
  w2.answer('a@b.co');
  w2.answer('learn');
  assert.equal(w2.skip().ok, true); // the note step
  assert.equal(w2.state().status, 'ready');
  assert.equal(w2.isComplete(), true); // optional absence never blocks
});

test('NEGATIVE CONTROL — half-finished intake creates NO join record', async () => {
  const s = NI.createSession('welcome', { ownerAlias: 'naya' });
  s.answer('Maria'); // name only — three answers missing
  assert.equal(s.isComplete(), false);
  assert.equal(NI.joinRecord(s, sha('maria@example.com')), null);
  s.answer('maria@example.com');
  s.answer('build');
  // note is optional, but the session has not reached review via its final
  // step until it is answered or skipped:
  assert.equal(s.state().status, 'in_progress');
  assert.equal(NI.joinRecord(s, sha('maria@example.com')), null);
  s.skip();
  assert.equal(s.isComplete(), true);
  const rec = NI.joinRecord(s, sha('maria@example.com'));
  assert.equal(rec.invitee_email_hash, sha('maria@example.com'));
  // and a record with a non-hash "hash" is refused too:
  assert.equal(NI.joinRecord(s, 'maria@example.com'), null);
});

test('NEGATIVE CONTROL — abandonment loses nothing already answered', () => {
  const s = NI.createSession('welcome', { ownerAlias: 'naya', sessionId: 'sess-1' });
  s.start();
  s.answer('Maria');
  s.answer('maria@example.com');
  assert.equal(s.abandon().ok, true);
  const snap = s.snapshot();
  const s2 = NI.createSession('welcome', { ownerAlias: 'naya' });
  assert.equal(s2.restore(snap).ok, true);
  assert.deepEqual(s2.state().answers, { name: 'Maria', email: 'maria@example.com' });
  assert.equal(s2.state().step.key, 'intent'); // resumes where they left off
});

test('voice and tap produce IDENTICAL records', async () => {
  const tap = completeWelcome('tap');
  const voice = completeWelcome('voice');
  const hash = await NI.hashEmail('maria@example.com');
  assert.deepEqual(NI.joinRecord(voice, hash), NI.joinRecord(tap, hash));
});

test('hashEmail: sha256 of the normalized address (the invites canon)', async () => {
  assert.equal(await NI.hashEmail('  MARIA@Example.com '), sha('maria@example.com'));
  assert.equal(NI.normalizeEmail(' A@B.Co '), 'a@b.co');
});

test('voice choice matching: spoken label resolves to the choice value', () => {
  const flow = NI.FLOWS.welcome;
  const intent = flow.steps[2];
  assert.equal(NI.matchChoice(intent, 'build my own app'), 'build');
  assert.equal(NI.matchChoice(intent, 'Join the community'), 'community');
  assert.equal(NI.matchChoice(intent, 'banana'), null);
});

test('completion stats: started / finished / abandoned / by-step', () => {
  const ev = (sid, event, step_key) => ({ session_id: sid, event, step_key });
  const stats = NI.completionStats([
    ev('a', 'started'), ev('a', 'finished'),
    ev('b', 'started'), ev('b', 'abandoned', 'email'),
    ev('c', 'started'), ev('c', 'abandoned', 'email'),
    ev('d', 'started'),
    ev('a', 'finished'), // duplicate finished must not double-count
  ]);
  assert.deepEqual(stats, {
    started: 4, finished: 1, abandoned: 2,
    completion_rate: 25, abandon_by_step: { email: 2 },
  });
  assert.equal(NI.completionStats([]).completion_rate, null);
});

// ── Store: transport injected; spies assert payloads ─────────────────

function spyFetch(handler) {
  const calls = [];
  const fn = (url, opts) => {
    calls.push({ url, opts, body: opts && opts.body ? JSON.parse(opts.body) : null });
    return handler(url, opts, calls);
  };
  fn.calls = calls;
  return fn;
}
const okJson = (rows) => Promise.resolve({
  ok: true, status: 201,
  json: () => Promise.resolve(rows),
});

test('store.submit (welcome): inserts the join into invites, hash only', async () => {
  const fetchImpl = spyFetch(() => okJson([{ id: 'inv-1', status: 'joined' }]));
  const store = NI.createStore({
    supabaseUrl: 'https://example.supabase.co', anonKey: 'anon', fetchImpl,
  });
  const r = await store.submit(completeWelcome());
  assert.equal(r.saved, true);
  const insert = fetchImpl.calls.find((c) => c.url.endsWith('/rest/v1/invites'));
  assert.ok(insert, 'invites insert happened');
  assert.equal(insert.body.status, 'joined');
  assert.equal(insert.body.owner_alias, 'naya');
  assert.equal(insert.body.invitee_email_hash, sha('maria@example.com'));
  // the raw email appears NOWHERE on the wire:
  assert.equal(JSON.stringify(fetchImpl.calls).includes('maria@example.com'), false);
});

test('store.submit (invite_accept): finds the recorded invite and flips it', async () => {
  const fetchImpl = spyFetch((url, opts) => {
    if (opts.method === 'PATCH') return okJson([{ id: 'inv-9', status: 'joined' }]);
    return Promise.resolve({
      ok: true, status: 200,
      json: () => Promise.resolve([{ id: 'inv-9', status: 'recorded' }]),
    });
  });
  const store = NI.createStore({
    supabaseUrl: 'https://example.supabase.co', anonKey: 'anon', fetchImpl,
  });
  const s = NI.createSession('invite_accept', { ownerAlias: 'naya' });
  s.answer('maria@example.com');
  s.answer('Maria');
  s.answer('learn');
  const r = await store.submit(s);
  assert.equal(r.saved, true);
  assert.equal(r.detail.updated, true);
  const patch = fetchImpl.calls.find((c) => c.opts.method === 'PATCH');
  assert.deepEqual(patch.body, { status: 'joined' });
});

test('NEGATIVE CONTROL — store refuses an incomplete session, sends nothing', async () => {
  const fetchImpl = spyFetch(() => okJson([]));
  const store = NI.createStore({
    supabaseUrl: 'https://example.supabase.co', anonKey: 'anon', fetchImpl,
  });
  const s = NI.createSession('welcome', { ownerAlias: 'naya' });
  s.answer('Maria');
  const r = await store.submit(s);
  assert.equal(r.saved, false);
  assert.equal(r.reason, 'incomplete');
  assert.equal(fetchImpl.calls.length, 0); // zero network traffic
});

test('NEGATIVE CONTROL — a failed write is never reported as saved', async () => {
  const fetchImpl = spyFetch(() => Promise.resolve({ ok: false, status: 403, json: () => Promise.resolve({}) }));
  const store = NI.createStore({
    supabaseUrl: 'https://example.supabase.co', anonKey: 'anon', fetchImpl,
  });
  const r = await store.submit(completeWelcome());
  assert.equal(r.saved, false);
  assert.equal(r.detail.reason, 'http_403');
});

test('store.recordEvent: posts the measurement row, honestly', async () => {
  const fetchImpl = spyFetch(() => Promise.resolve({ ok: true, status: 201, json: () => Promise.resolve([]) }));
  const store = NI.createStore({
    supabaseUrl: 'https://example.supabase.co', anonKey: 'anon', fetchImpl, ownerAlias: 'naya',
  });
  const r = await store.recordEvent(
    { session_id: 's1', flow: 'welcome', event: 'started', step_key: 'name', step_index: 0, via: null },
    null);
  assert.equal(r.recorded, true);
  assert.equal(fetchImpl.calls[0].url.endsWith('/rest/v1/intake_events'), true);
  assert.equal(fetchImpl.calls[0].body.event, 'started');
  const off = NI.createStore({ supabaseUrl: '', anonKey: '', fetchImpl });
  assert.equal((await off.recordEvent({ session_id: 's1', flow: 'welcome', event: 'started' })).recorded, false);
});

test('events: a full session emits started → steps → finished, in order', () => {
  const seen = [];
  const s = NI.createSession('welcome', {
    ownerAlias: 'naya',
    onEvent: (ev) => seen.push(ev.event + ':' + (ev.step_key || '')),
  });
  s.start();
  s.answer('Maria');
  s.answer('maria@example.com');
  s.answer('build', 'voice');
  s.skip();
  s.finish(NI.joinRecord(s, sha('maria@example.com')));
  assert.deepEqual(seen, [
    'started:name', 'step_completed:name', 'step_completed:email',
    'step_completed:intent', 'step_completed:note', 'finished:',
  ]);
});
