// Command + universal search (element #12, step 13) — module tests,
// node --test. The service-side isolation contract is pinned separately
// in tests/test_universal_search_contract.py; here we pin the client
// half: one query path for voice and typing, the ranked merge, the
// action contract, and the refusal behaviors.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const NS = require('../HUB/app/js/naya-search.js');

function row(type, id, title, score, at, kind, target) {
  return {
    object_type: type, object_id: id, title, snippet: type + ' snippet',
    action_kind: kind, action_target: target, score,
    occurred_at: at || '2026-10-22T00:00:00Z',
  };
}

test('parseQuery: trims, collapses, bounds', () => {
  assert.deepEqual(NS.parseQuery('  maria   jones '), { ok: true, query: 'maria jones' });
  assert.deepEqual(NS.parseQuery('   '), { ok: false, reason: 'empty' });
  assert.deepEqual(NS.parseQuery(null), { ok: false, reason: 'empty' });
  assert.deepEqual(NS.parseQuery('x'.repeat(NS.MAX_QUERY + 1)), { ok: false, reason: 'too_long' });
});

test('voice intent: wake word + intent verbs are packaging, not query', () => {
  assert.deepEqual(NS.parseVoiceIntent('Naya, find Maria'), { intent: 'search', query: 'Maria' });
  assert.deepEqual(NS.parseVoiceIntent('Naya find the pricing thread'), { intent: 'search', query: 'the pricing thread' });
  assert.deepEqual(NS.parseVoiceIntent('find Maria'), { intent: 'search', query: 'Maria' });
  assert.deepEqual(NS.parseVoiceIntent('search for quarterly plan'), { intent: 'search', query: 'quarterly plan' });
  assert.deepEqual(NS.parseVoiceIntent('show me Bob'), { intent: 'search', query: 'Bob' });
  assert.deepEqual(NS.parseVoiceIntent('look up pricing'), { intent: 'search', query: 'pricing' });
  // No packaging: the whole transcript is the query — still a search.
  assert.deepEqual(NS.parseVoiceIntent('Maria'), { intent: 'search', query: 'Maria' });
  // A bare wake word is not a search.
  assert.deepEqual(NS.parseVoiceIntent('Naya'), { intent: 'none', query: '' });
  assert.deepEqual(NS.parseVoiceIntent('   '), { intent: 'none', query: '' });
});

test('rankResults: one merged set across types, score then recency', () => {
  const rows = [
    row('naya_note', 'n1', 'Maria note', 40, '2026-10-22T10:00:00Z', 'open_room', 'lists'),
    row('person', 'p1', 'Maria Jones', 100, '2026-10-20T10:00:00Z', 'open_person', 'p1'),
    row('mail_thread', 't1', 'Maria — pricing', 60, '2026-10-21T10:00:00Z', 'open_room', 'mail'),
    row('smart_link', 'l1', 'maria', 80, '2026-10-19T10:00:00Z', 'open_url', 'https://nayanet.live/maria'),
    row('smart_note', '', 'Maria posted…', 40, '2026-10-22T11:00:00Z', 'open_room', 'feed'),
  ];
  const out = NS.rankResults(rows, 20);
  assert.deepEqual(out.map((r) => r.type),
    ['person', 'smart_link', 'mail_thread', 'smart_note', 'naya_note']);
  // The 40-tie breaks by recency: the 11:00 wall note beats the 10:00 capture.
  assert.equal(out[3].occurred_at, '2026-10-22T11:00:00Z');
  // Every result carries its action — no dead results.
  for (const r of out) {
    assert.ok(r.action && r.action.kind, r.type);
    assert.ok(r.action.target !== undefined, r.type);
  }
});

test('rankResults: dedupe keeps the first (strongest), cap applies', () => {
  const rows = [
    row('naya_note', 'n1', 'dup', 90, null, 'open_room', 'lists'),
    row('naya_note', 'n1', 'dup again', 10, null, 'open_room', 'lists'),
    row('naya_note', 'n2', 'other', 50, null, 'open_room', 'lists'),
    row('naya_note', 'n3', 'third', 40, null, 'open_room', 'lists'),
  ];
  const out = NS.rankResults(rows, 2);
  assert.equal(out.length, 2);
  assert.deepEqual(out.map((r) => r.id), ['n1', 'n2']);
  assert.equal(out[0].title, 'dup');
});

test('normalizeResult: unknown types dropped; missing actions derived', () => {
  assert.equal(NS.normalizeResult({ object_type: 'secret_thing', title: 'x' }), null);
  assert.equal(NS.normalizeResult(null), null);
  const p = NS.normalizeResult({ object_type: 'person', object_id: 'k1', title: 'Maria' });
  assert.deepEqual(p.action, { kind: 'open_person', target: 'k1' });
  const l = NS.normalizeResult({ object_type: 'smart_link', object_id: 'l9', title: 'go' });
  assert.equal(l.action.kind, 'open_url');
  const n = NS.normalizeResult({ object_type: 'naya_note', object_id: 'n9', title: 'hi' });
  assert.deepEqual(n.action, { kind: 'open_room', target: 'lists' });
});

test('groupByType: canonical order, only present types', () => {
  const out = NS.rankResults([
    row('smart_link', 'l1', 'a', 10, null, 'open_url', 'https://nayanet.live/a'),
    row('person', 'p1', 'b', 20, null, 'open_person', 'p1'),
  ]);
  const groups = NS.groupByType(out);
  assert.deepEqual(groups.map((g) => g.type), ['person', 'smart_link']);
  assert.equal(groups[0].label, 'People');
});

test('defaultAction: rooms route in the Hub, links open, nothing fakes', () => {
  const env = { location: { hash: '' }, open: (url, tgt, feat) => { env.opened = [url, tgt, feat]; } };
  const person = NS.normalizeResult(row('person', 'k1', 'Maria', 100, null, 'open_person', 'k1'));
  assert.equal(NS.defaultAction(person, env).via, 'open_person');
  assert.equal(env.location.hash, '#/hub/connections');
  const note = NS.normalizeResult(row('naya_note', 'n1', 'x', 10, null, 'open_room', 'lists'));
  assert.equal(NS.defaultAction(note, env).via, 'open_room');
  assert.equal(env.location.hash, '#/hub/lists');
  const link = NS.normalizeResult(row('smart_link', 'l1', 'go', 10, null, 'open_url', 'https://nayanet.live/go'));
  assert.equal(NS.defaultAction(link, env).via, 'open_url');
  assert.deepEqual(env.opened, ['https://nayanet.live/go', '_blank', 'noopener']);
  assert.equal(NS.defaultAction(null, env).acted, false);
});

test('moveActive: wrap-around both ways, empty stays inactive', () => {
  assert.equal(NS.moveActive(-1, 1, 3), 0);
  assert.equal(NS.moveActive(-1, -1, 3), 2);
  assert.equal(NS.moveActive(2, 1, 3), 0);
  assert.equal(NS.moveActive(0, -1, 3), 2);
  assert.equal(NS.moveActive(0, 1, 0), -1);
});

test('NEGATIVE CONTROL — empty query: refused locally, zero network', async () => {
  let calls = 0;
  const store = NS.createStore({
    supabaseUrl: 'https://example.supabase.co', anonKey: 'anon',
    getAccessToken: () => 'jwt-1',
    fetchImpl: async () => { calls++; return { ok: true, json: async () => [] }; },
  });
  assert.deepEqual(await store.search('   '), { invalid: true, reason: 'empty', results: [] });
  assert.equal(calls, 0);
});

test('NEGATIVE CONTROL — no session: not_verified, zero network', async () => {
  let calls = 0;
  const store = NS.createStore({
    supabaseUrl: 'https://example.supabase.co', anonKey: 'anon',
    getAccessToken: () => null,
    fetchImpl: async () => { calls++; return { ok: true, json: async () => [] }; },
  });
  const out = await store.search('maria');
  assert.equal(out.not_verified, true);
  assert.equal(out.reason, 'no_session');
  assert.deepEqual(out.results, []);
  assert.equal(calls, 0); // search never fakes a result
});

test('store contract: body carries ONLY the query and limit — no owner field exists to spoof', async () => {
  const sent = [];
  const store = NS.createStore({
    supabaseUrl: 'https://example.supabase.co/', anonKey: 'anon-key',
    getAccessToken: () => 'jwt-1',
    fetchImpl: async (url, init) => {
      sent.push({ url, init });
      return { ok: true, json: async () => [row('person', 'p1', 'Maria', 100, null, 'open_person', 'p1')] };
    },
  });
  const out = await store.search('  maria ', { limit: 5 });
  assert.equal(sent.length, 1);
  assert.equal(sent[0].url, 'https://example.supabase.co/rest/v1/rpc/search_universal');
  assert.equal(sent[0].init.method, 'POST');
  assert.equal(sent[0].init.headers.Authorization, 'Bearer jwt-1');
  const body = JSON.parse(sent[0].init.body);
  assert.deepEqual(Object.keys(body).sort(), ['p_limit', 'p_query']);
  assert.deepEqual(body, { p_query: 'maria', p_limit: 5 });
  assert.equal(out.results.length, 1);
  assert.equal(out.results[0].type, 'person');
});

test('no-match: an empty service page is an honest empty result set', async () => {
  const store = NS.createStore({
    supabaseUrl: 'https://example.supabase.co', anonKey: 'anon',
    getAccessToken: () => 'jwt-1',
    fetchImpl: async () => ({ ok: true, json: async () => [] }),
  });
  assert.deepEqual(await store.search('zzz-no-such-thing'), { results: [] });
});

test('dictation: routes transcripts through the one voice-intent path', () => {
  class FakeRec {
    start() { this.onresult({ resultIndex: 0, results: [{ isFinal: true, 0: { transcript: 'Naya, find Maria' } }] }); }
  }
  const d = NS.createDictation({ recognitionCtor: FakeRec });
  assert.equal(d.supported, true);
  let heard = null;
  d.start((t) => { heard = t; }, () => {});
  assert.equal(heard, 'Naya, find Maria');
  assert.deepEqual(NS.parseVoiceIntent(heard), { intent: 'search', query: 'Maria' });
  const none = NS.createDictation({ recognitionCtor: null });
  assert.equal(none.supported, false); // honestly absent, never assumed
});

test('hotkey: Cmd-K and Ctrl-K both open; plain k does not', () => {
  const listeners = {};
  const fakeDoc = {
    addEventListener: (name, fn) => { listeners[name] = fn; },
    removeEventListener: (name) => { delete listeners[name]; },
  };
  let opens = 0;
  const uninstall = NS.installHotkey(fakeDoc, () => { opens++; });
  const ev = (key, mods) => ({ key, ...mods, preventDefault() { this.prevented = true; } });
  listeners.keydown(ev('k', { metaKey: true }));
  listeners.keydown(ev('k', { ctrlKey: true }));
  listeners.keydown(ev('k', {}));
  listeners.keydown(ev('j', { metaKey: true }));
  assert.equal(opens, 2);
  uninstall();
  assert.equal(listeners.keydown, undefined);
});

test('LATENCY — the merge ranks a fat page fast (service returns ≤50; this stresses 5,000)', () => {
  const types = NS.TYPES;
  const corpus = [];
  for (let i = 0; i < 5000; i++) {
    corpus.push(row(
      types[i % types.length], 'id-' + i, 'title ' + i,
      (i * 37) % 101,
      new Date(1700000000000 + i * 1000).toISOString(),
      'open_room', 'lists',
    ));
  }
  const t0 = performance.now();
  const out = NS.rankResults(corpus, 50);
  const ms = performance.now() - t0;
  console.log(`rankResults: 5000 rows -> ${out.length} ranked in ${ms.toFixed(2)}ms`);
  assert.equal(out.length, 50);
  assert.ok(ms < 100, `ranking 5000 rows took ${ms}ms — the everyday path must stay light`);
});
