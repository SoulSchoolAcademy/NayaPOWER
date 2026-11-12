// Naya Notes (element #15, Hub half) — module tests, node --test.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const NN = require('../HUB/app/js/naya-notes.js');

test('validation: trims, defaults category to General, bounds length', () => {
  assert.deepEqual(NN.validateNote({ text: '  call Mary about pricing  ' }), {
    ok: true,
    note: { text: 'call Mary about pricing', category: 'General', list_name: null },
  });
  assert.deepEqual(NN.validateNote({ text: 'x', category: 'Ideas', list: 'Someday' }).note,
    { text: 'x', category: 'Ideas', list_name: 'Someday' });
  assert.equal(NN.validateNote({ text: '   ' }).reason, 'empty');
  assert.equal(NN.validateNote({}).reason, 'empty');
  assert.equal(NN.validateNote({ text: 'a'.repeat(NN.MAX_TEXT + 1) }).reason, 'too_long');
});

test('grouping + categories: every note lands in exactly one category', () => {
  const notes = [
    { text: 'a', category: 'Ideas' }, { text: 'b' },
    { text: 'c', category: 'Ideas' }, { text: 'd', category: 'Calls' },
  ];
  const groups = NN.groupByCategory(notes);
  assert.deepEqual(Object.keys(groups).sort(), ['Calls', 'General', 'Ideas']);
  assert.equal(groups.Ideas.length, 2);
  assert.equal(groups.General.length, 1); // missing category defaults, never lost
  assert.deepEqual(NN.categoriesOf(notes), ['Calls', 'General', 'Ideas']);
});

test('copy contract: text, with list context when present', () => {
  assert.equal(NN.copyTextFor({ text: 'buy stamps' }), 'buy stamps');
  assert.equal(NN.copyTextFor({ text: 'buy stamps', list_name: 'Errands' }),
    'buy stamps\n— List: Errands');
  assert.equal(NN.copyTextFor(null), '');
});

test('NEGATIVE CONTROL — no session: the store refuses, nothing is sent', async () => {
  let calls = 0;
  const store = NN.createStore({
    supabaseUrl: 'https://example.supabase.co', anonKey: 'anon',
    ownerAlias: 'shawn', getAccessToken: () => null,
    fetchImpl: async () => { calls++; return { ok: true, json: async () => [] }; },
  });
  assert.deepEqual(await store.list(), { not_verified: true, reason: 'no_session' });
  assert.deepEqual(await store.add({ text: 'hello' }), { not_verified: true, reason: 'no_session' });
  assert.equal(calls, 0); // zero network traffic without a session
});

test('store with session: list reads, add posts the shaped row', async () => {
  const sent = [];
  const store = NN.createStore({
    supabaseUrl: 'https://example.supabase.co/', anonKey: 'anon',
    ownerAlias: 'shawn', getAccessToken: () => 'jwt-1',
    fetchImpl: async (url, init) => {
      sent.push({ url, init });
      if (init && init.method === 'POST') {
        return { ok: true, json: async () => [{ id: 'n1', text: 'hello', category: 'General', list_name: null }] };
      }
      return { ok: true, json: async () => [{ id: 'n1', text: 'hello' }] };
    },
  });
  const listed = await store.list();
  assert.equal(listed[0].id, 'n1');
  assert.ok(sent[0].url.includes('/rest/v1/naya_notes'));
  assert.equal(sent[0].init.headers.Authorization, 'Bearer jwt-1');
  const added = await store.add({ text: ' hello ', category: '', list: '' });
  assert.equal(added.saved, true);
  const row = JSON.parse(sent[1].init.body);
  assert.deepEqual(row, {
    owner_alias: 'shawn', owner_id: null,
    text: 'hello', category: 'General', list_name: null,
  });
  // invalid input never reaches the network either
  const bad = await store.add({ text: ' ' });
  assert.deepEqual(bad, { invalid: true, reason: 'empty' });
  assert.equal(sent.length, 2);
});

test('dictation: unsupported environment is honest; supported wires results', () => {
  const none = NN.createDictation({ recognitionCtor: null });
  assert.equal(none.supported, false);
  assert.equal(none.start(() => {}, () => {}), null);

  class FakeRecognition {
    start() { this.onresult({ resultIndex: 0, results: [{ isFinal: true, 0: { transcript: '  hello world ' } }] }); }
  }
  const heard = [];
  const d = NN.createDictation({ recognitionCtor: FakeRecognition });
  assert.equal(d.supported, true);
  d.start((t) => heard.push(t), () => {});
  assert.deepEqual(heard, ['hello world']);
});

test('the panel module surface the Hub mounts is present', () => {
  for (const key of ['validateNote', 'groupByCategory', 'categoriesOf',
    'copyTextFor', 'createStore', 'createDictation', 'mountPanel']) {
    assert.equal(typeof NN[key], 'function', key);
  }
});
