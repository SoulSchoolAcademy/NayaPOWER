// Smart Lists (element #16, step 15) — module tests, node --test.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const SL = require('../HUB/app/js/smart-lists.js');

test('list validation: trims, defaults category to General, bounds lengths', () => {
  assert.deepEqual(SL.validateList({ title: '  Launch guests  ' }), {
    ok: true, list: { title: 'Launch guests', category: 'General' },
  });
  assert.deepEqual(SL.validateList({ title: 'VIPs', category: ' Events ' }).list,
    { title: 'VIPs', category: 'Events' }); // owner-named category (element #19)
  assert.equal(SL.validateList({ title: '   ' }).reason, 'empty_title');
  assert.equal(SL.validateList({}).reason, 'empty_title');
  assert.equal(SL.validateList({ title: 'x'.repeat(SL.MAX_TITLE + 1) }).reason, 'title_too_long');
  assert.equal(SL.validateList({ title: 'ok', category: 'c'.repeat(SL.MAX_CATEGORY + 1) }).reason,
    'category_too_long');
});

test('item validation: the six typed kinds, text vs reference shapes', () => {
  for (const kind of ['smart_note', 'naya_note', 'person', 'mail_thread', 'smart_link']) {
    const v = SL.validateItem({ kind, ref: 'ref-1' });
    assert.equal(v.ok, true, kind);
    assert.equal(v.item.item_kind, kind);
    assert.equal(v.item.item_ref, 'ref-1');
    assert.equal(v.item.text, null);
  }
  // Naya Notes are first-class from day one (element #15 store items).
  const nn = SL.validateItem({ kind: 'naya_note', ref: 'note-uuid-1', label: 'Call Mary' });
  assert.deepEqual(nn.item, { item_kind: 'naya_note', item_ref: 'note-uuid-1', label: 'Call Mary', text: null });
  // Plain text items carry text, never a ref.
  const t = SL.validateItem({ kind: 'text', text: '  buy stamps  ' });
  assert.deepEqual(t.item, { item_kind: 'text', item_ref: null, label: null, text: 'buy stamps' });
  // Refusals: unknown kind, ref-kind without ref, text without text, bounds.
  assert.equal(SL.validateItem({ kind: 'board', ref: 'x' }).reason, 'bad_kind');
  assert.equal(SL.validateItem({ kind: 'person', ref: '  ' }).reason, 'empty_ref');
  assert.equal(SL.validateItem({ kind: 'text', text: ' ' }).reason, 'empty_text');
  assert.equal(SL.validateItem({ kind: 'text', text: 'a'.repeat(SL.MAX_TEXT + 1) }).reason, 'text_too_long');
  assert.equal(SL.validateItem({ kind: 'person', ref: 'r'.repeat(SL.MAX_REF + 1) }).reason, 'ref_too_long');
});

test('grouping + categories: every list lands in exactly one category', () => {
  const lists = [
    { title: 'a', category: 'Events' }, { title: 'b' },
    { title: 'c', category: 'Events' }, { title: 'd', category: 'People' },
  ];
  const groups = SL.groupListsByCategory(lists);
  assert.deepEqual(Object.keys(groups).sort(), ['Events', 'General', 'People']);
  assert.equal(groups.Events.length, 2);
  assert.equal(groups.General.length, 1); // missing category defaults, never lost
  assert.deepEqual(SL.categoriesOfLists(lists), ['Events', 'General', 'People']);
});

test('REGRESSION (cure round 4) — hostile category names cannot break grouping', () => {
  // validateList accepts these names, so the grouping the Lists room
  // renders with must survive them. On a plain {} accumulator,
  // 'constructor' read back as the inherited function and threw;
  // '__proto__' retargeted the prototype instead of grouping.
  for (const hostile of ['__proto__', 'constructor', 'hasOwnProperty', 'toString']) {
    assert.equal(SL.validateList({ title: 't', category: hostile }).ok, true,
      `validateList still accepts ${hostile} — grouping must cope`);
    const lists = [{ title: 'x', category: hostile }, { title: 'y', category: 'Events' }];
    const groups = SL.groupListsByCategory(lists);
    assert.ok(Array.isArray(groups[hostile]), `group for ${hostile} is a real array`);
    assert.equal(groups[hostile].length, 1);
    assert.equal(groups[hostile][0].title, 'x');
    assert.deepEqual(SL.categoriesOfLists(lists), ['Events', hostile].sort());
  }
  // Repeated hostile keys accumulate into the same own group, and the
  // grouping leaves Object.prototype untouched.
  const two = SL.groupListsByCategory([
    { title: 'a', category: 'constructor' }, { title: 'b', category: 'constructor' },
  ]);
  assert.equal(two.constructor.length, 2);
  assert.equal({}.polluted, undefined);
  assert.equal(Object.prototype.polluted, undefined);
});

test('ordering + reorder plan: position order is stable, swaps are exact', () => {
  const items = [
    { id: 'c', position: 2, created_at: '2026-10-22T00:00:03Z' },
    { id: 'a', position: 0, created_at: '2026-10-22T00:00:01Z' },
    { id: 'b', position: 1, created_at: '2026-10-22T00:00:02Z' },
  ];
  assert.deepEqual(SL.orderItems(items).map((i) => i.id), ['a', 'b', 'c']);
  assert.equal(SL.nextPosition(items), 3);
  assert.equal(SL.nextPosition([]), 0);
  assert.deepEqual(SL.movePlan(items, 'b', -1), [
    { id: 'b', position: 0 }, { id: 'a', position: 1 },
  ]);
  assert.deepEqual(SL.movePlan(items, 'b', 1), [
    { id: 'b', position: 2 }, { id: 'c', position: 1 },
  ]);
  assert.deepEqual(SL.movePlan(items, 'a', -1), []); // already first
  assert.deepEqual(SL.movePlan(items, 'c', 1), []); // already last
  assert.deepEqual(SL.movePlan(items, 'nope', 1), []); // unknown id
});

test('device import planning: Hub saved shape and flagship list shape', () => {
  const hub = SL.planDeviceImport({
    saved: [
      { id: 'board-1', kind: 'favorite', title: 'Maria — Connections', savedAt: 1760000000000 },
      { id: 'board-2', kind: 'save', title: 'Reports', savedAt: 1760000001000 },
    ],
  });
  assert.equal(hub.lists.length, 1);
  assert.equal(hub.lists[0].items.length, 2);
  assert.equal(hub.lists[0].items[0].kind, 'text');
  assert.match(hub.lists[0].items[0].provenance, /board-1/);

  const flagship = SL.planDeviceImport({
    lists: [{ name: 'Errands', items: ['stamps', { text: 'call bank' }] }],
  });
  assert.equal(flagship.lists.length, 1);
  assert.equal(flagship.lists[0].title, 'Errands');
  assert.deepEqual(flagship.lists[0].items.map((i) => i.text), ['stamps', 'call bank']);

  const garbage = SL.planDeviceImport(42);
  assert.deepEqual(garbage.lists, []);
  assert.ok(garbage.notes.length > 0);
});

test('NEGATIVE CONTROL — no session: the store refuses, nothing is sent', async () => {
  let calls = 0;
  const store = SL.createStore({
    supabaseUrl: 'https://example.supabase.co', anonKey: 'anon',
    ownerAlias: 'shawn', getAccessToken: () => null,
    fetchImpl: async () => { calls++; return { ok: true, json: async () => [] }; },
  });
  assert.deepEqual(await store.lists(), { not_verified: true, reason: 'no_session' });
  assert.deepEqual(await store.addList({ title: 'X' }), { not_verified: true, reason: 'no_session' });
  assert.deepEqual(await store.updateList('l1', { title: 'Y' }), { not_verified: true, reason: 'no_session' });
  assert.deepEqual(await store.removeList('l1'), { not_verified: true, reason: 'no_session' });
  assert.deepEqual(await store.items('l1'), { not_verified: true, reason: 'no_session' });
  assert.deepEqual(await store.addItem('l1', { kind: 'text', text: 'hi' }),
    { not_verified: true, reason: 'no_session' });
  assert.deepEqual(await store.moveItem('i1', 3), { not_verified: true, reason: 'no_session' });
  assert.deepEqual(await store.removeItem('i1'), { not_verified: true, reason: 'no_session' });
  assert.equal(calls, 0); // zero network traffic without the owner's session
  // Invalid input is refused before the network too.
  assert.deepEqual(await store.addItem('l1', { kind: 'board', ref: 'x' }),
    { invalid: true, reason: 'bad_kind' });
  assert.equal(calls, 0);
});

test('store with session: shaped rows to the two tables, and only those', async () => {
  const sent = [];
  const store = SL.createStore({
    supabaseUrl: 'https://example.supabase.co/', anonKey: 'anon',
    ownerAlias: 'shawn', ownerId: 'uid-1', getAccessToken: () => 'jwt-1',
    fetchImpl: async (url, init) => {
      sent.push({ url, init });
      if (init && init.method === 'POST' && url.includes('smart_list_items')) {
        return { ok: true, json: async () => [{ id: 'i1', item_kind: 'naya_note' }] };
      }
      if (init && init.method === 'POST') {
        return { ok: true, json: async () => [{ id: 'l1', title: 'Guests' }] };
      }
      if (init && init.method === 'PATCH') {
        return { ok: true, json: async () => [{ id: 'i1', position: 5 }] };
      }
      if (init && init.method === 'DELETE') {
        return { ok: true, json: async () => [] };
      }
      return { ok: true, json: async () => [{ id: 'l1', title: 'Guests', category: 'Events' }] };
    },
  });

  const listed = await store.lists();
  assert.equal(listed[0].id, 'l1');
  assert.ok(sent[0].url.includes('/rest/v1/smart_lists'));
  assert.equal(sent[0].init.headers.Authorization, 'Bearer jwt-1');

  const added = await store.addList({ title: ' Guests ', category: 'Events' });
  assert.equal(added.saved, true);
  const listRow = JSON.parse(sent[1].init.body);
  assert.deepEqual(listRow, {
    owner_alias: 'shawn', owner_id: 'uid-1',
    title: 'Guests', category: 'Events', position: 0,
  });

  const item = await store.addItem('l1', { kind: 'naya_note', ref: 'note-9', position: 0 });
  assert.equal(item.saved, true);
  const itemRow = JSON.parse(sent[2].init.body);
  assert.deepEqual(itemRow, {
    list_id: 'l1', owner_alias: 'shawn', owner_id: 'uid-1',
    item_kind: 'naya_note', item_ref: 'note-9', label: 'note-9', text: null, position: 0,
  });

  const moved = await store.moveItem('i1', 5);
  assert.equal(moved.updated, true);
  assert.deepEqual(JSON.parse(sent[3].init.body), { position: 5 });
  assert.ok(sent[3].url.includes('/rest/v1/smart_list_items?id=eq.i1'));

  // NEGATIVE CONTROL — removing an item calls DELETE on the membership
  // table ONLY: the referenced object (here a Naya Note) is never called.
  const removed = await store.removeItem('i1');
  assert.deepEqual(removed, { removed: true });
  const del = sent[4];
  assert.equal(del.init.method, 'DELETE');
  assert.ok(del.url.includes('/rest/v1/smart_list_items?id=eq.i1'));
  for (const s of sent) {
    assert.ok(!s.url.includes('/rest/v1/naya_notes'), 'must never touch the notes table: ' + s.url);
    assert.ok(!s.url.includes('/rest/v1/smart_notes'), 'must never touch the smart notes table: ' + s.url);
    assert.ok(!s.url.includes('/rest/v1/smart_links'), 'must never touch the links table: ' + s.url);
  }
});

test('the panel module surface the Hub mounts is present', () => {
  for (const key of ['validateList', 'validateItem', 'groupListsByCategory',
    'categoriesOfLists', 'orderItems', 'movePlan', 'planDeviceImport',
    'createStore', 'mountPanel']) {
    assert.equal(typeof SL[key], 'function', key);
  }
  assert.deepEqual(SL.ITEM_KINDS,
    ['smart_note', 'naya_note', 'person', 'mail_thread', 'smart_link', 'text']);
});
