/* Tests for naya-factory-cover-picker.js — mirrors the Python suite
 * (factory-cover-picker-2026-11-12.py, TestFactoryCoverPicker) on a
 * hand-built fixture manifest, so the two runtimes can never disagree.
 * Run: node test-naya-factory-cover-picker.cjs
 * Exit 0 = all pass. No network, no live manifest, no engine required:
 * the assign engine is NOT beside this file in the workspace, so these
 * tests exercise the built-in fallback chain — the same chain the live
 * repo run uses when the engine is absent.
 */
'use strict';
const assert = require('node:assert');
const picker = require('./naya-factory-cover-picker.js');

const FIXTURE = {
  assignment_on_page_creation: {
    personal_page: 'area/personal',
    business_page: 'area/business',
    space: 'area/spaces',
    events_page: 'area/events',
    booking_page: 'area/booking',
    dashboard_intel: 'area/intel-today',
    any_other_page: 'rotation set',
  },
  assets: [
    { key: 'area/personal', file: 'areas/personal.jpg', kind: 'area', status: 'ready', name: 'Area — Personal', category: 'house-area', suits: 'personal pages', credit: 'Naya Resolve', tier: 'signature' },
    { key: 'area/business', file: 'areas/business.jpg', kind: 'area', status: 'ready', name: 'Area — Business', category: 'house-area', suits: 'business pages', credit: 'Naya Resolve', tier: 'signature' },
    { key: 'area/spaces', file: 'areas/spaces.jpg', kind: 'area', status: 'ready', name: 'Area — Spaces', category: 'house-area', suits: 'spaces', credit: 'Naya Resolve', tier: 'signature' },
    { key: 'area/events', file: 'areas/events.jpg', kind: 'area', status: 'ready', name: 'Area — Events', category: 'house-area', suits: 'event pages', credit: 'Naya Resolve', tier: 'signature' },
    { key: 'area/booking', file: 'areas/booking.jpg', kind: 'area', status: 'designed', name: 'Area — Booking', category: 'house-area', suits: 'booking pages', credit: 'Naya Resolve', tier: 'signature' },
    { key: 'area/intel-today', file: 'areas/intel-today.jpg', kind: 'area', status: 'designed', name: 'Area — Intel Today', category: 'house-area', suits: 'intel pages', credit: 'Naya Resolve', tier: 'signature' },
    { key: 'open/companion-golden', file: 'open/companion-golden.jpg', kind: 'open', status: 'ready', name: 'Companion Golden', category: 'companions', suits: 'a golden retriever at dawn, for dog lovers', credit: 'Naya Resolve', tier: 'open', featured_class: 'citizen', featured_order: 1 },
    { key: 'open/quiet-office', file: 'open/quiet-office.jpg', kind: 'open', status: 'ready', name: 'Quiet Office', category: 'craft', suits: 'a clean minimal office for professionals', credit: 'Naya Resolve', tier: 'open' },
    { key: 'open/retired-one', file: 'open/retired.jpg', kind: 'open', status: 'retired', name: 'Retired One', category: 'abstract', suits: 'retired', credit: 'Naya Resolve', tier: 'open' },
    { key: 'rotation/her-kingdom-tree', file: 'rotation/her-kingdom-tree.jpg', kind: 'rotation', status: 'ready', name: 'Her Kingdom Tree', category: 'house-signature', suits: 'kingdom tree', credit: 'Naya Resolve', tier: 'signature' },
    { key: 'rotation/quiet-harbor', file: 'rotation/quiet-harbor.jpg', kind: 'rotation', status: 'ready', name: 'Quiet Harbor', category: 'house-signature', suits: 'quiet harbor', credit: 'Naya Resolve', tier: 'signature' },
  ],
};

const TESTS = [];
function test(name, fn) { TESTS.push([name, fn]); }

test('every registry template maps', () => {
  for (const t of picker.REGISTRY_TEMPLATES) {
    const { pageType } = picker.templatePageType(t);
    assert.ok(pageType, t);
  }
  assert.strictEqual(picker.REGISTRY_TEMPLATES.length, 12);
});

test('unknown template is named error', () => {
  for (const bad of [null, '', '  ', 'smart-list', 'today', 'no-such-template']) {
    assert.throws(() => picker.templatePageType(bad), /unknown factory template/);
  }
  assert.throws(() => picker.openFactoryCoverStep({ template: 'today', manifest: FIXTURE }),
    /unknown factory template/);
});

test('open step preselects born cover', () => {
  const step = picker.openFactoryCoverStep({ template: 'personal', manifest: FIXTURE });
  assert.strictEqual(step.template, 'personal');
  assert.strictEqual(step.page_type, 'personal_page');
  assert.strictEqual(step.mode, 'create');
  assert.strictEqual(step.preselected.cover_key, 'area/personal');
  assert.strictEqual(step.born_cover.via, 'area_default');
  assert.deepStrictEqual(step.doors, ['recommended', 'library', 'upload']);
  assert.strictEqual(step.skip.taps, 1);
  assert.strictEqual(step.skip.keeps, 'area/personal');
});

test('designed area defaults fall to rotation, never blank', () => {
  // Mirrors the live manifest: area/booking + area/intel-today are
  // `designed`, not ready — booking + dashboard are born via rotation.
  for (const t of ['booking', 'dashboard']) {
    const step = picker.openFactoryCoverStep({ template: t, manifest: FIXTURE });
    assert.ok(step.born_cover.cover_key);
    assert.strictEqual(step.born_cover.via, 'rotation');
  }
});

test('pick stores chosen cover', () => {
  const step = picker.openFactoryCoverStep({ template: 'personal', manifest: FIXTURE });
  const r = picker.resolveFactoryCoverAction(step,
    { action: 'pick', source: 'library', cover_key: 'open/companion-golden' }, FIXTURE);
  assert.strictEqual(r.error, null);
  assert.strictEqual(r.state.cover_key, 'open/companion-golden');
  assert.strictEqual(r.state.set_by, 'owner');
  assert.strictEqual(r.meta.changed, true);
  assert.strictEqual(r.meta.template, 'personal');
  const a = picker.applyCoverToContract({ template: 'personal', handle: 'alex' }, r.state, FIXTURE);
  assert.strictEqual(a.error, null);
  assert.strictEqual(a.contract.cover.cover_key, 'open/companion-golden');
  assert.ok(a.contract.cover.cover_url.endsWith('open/companion-golden.jpg'));
  assert.strictEqual(a.contract.cover.cover_source, 'library');
  assert.strictEqual(a.contract.handle, 'alex');
});

test('invalid pick keeps born cover', () => {
  const step = picker.openFactoryCoverStep({ template: 'personal', manifest: FIXTURE });
  for (const action of [
    { action: 'pick', source: 'library', cover_key: 'open/retired-one' },
    { action: 'pick', source: 'library', cover_key: 'no-such-cover' },
    { action: 'pick', source: 'upload', upload_ref: '../escape.jpg' },
  ]) {
    const r = picker.resolveFactoryCoverAction(step, action, FIXTURE);
    assert.ok(r.error, JSON.stringify(action));
    assert.strictEqual(r.state, null);
    assert.strictEqual(r.meta.changed, false);
    assert.strictEqual(r.meta.kept, 'area/personal');
  }
});

test('skip keeps born and stores it', () => {
  const step = picker.openFactoryCoverStep({ template: 'booking', manifest: FIXTURE });
  const born = step.born_cover.cover_key;
  const r = picker.resolveFactoryCoverAction(step, { action: 'skip' }, FIXTURE);
  assert.strictEqual(r.error, null);
  assert.strictEqual(r.state.cover_key, born);
  assert.strictEqual(r.meta.changed, false);
  const a = picker.applyCoverToContract({ template: 'booking' }, r.state, FIXTURE);
  assert.strictEqual(a.error, null);
  assert.strictEqual(a.contract.cover.cover_key, born);
});

test('no-state apply resolves born default', () => {
  const a = picker.applyCoverToContract({ template: 'event' }, null, FIXTURE);
  assert.strictEqual(a.error, null);
  assert.strictEqual(a.contract.cover.cover_key, 'area/events');
  assert.strictEqual(a.contract.cover.cover_via, 'area_default');
  assert.strictEqual(a.contract.cover.set_by, 'system');
});

test('apply refuses unknown template', () => {
  const a = picker.applyCoverToContract({ template: 'today' }, null, FIXTURE);
  assert.ok(a.error);
  assert.match(a.error, /unknown factory template/);
  assert.strictEqual(a.contract, null);
});

test('upload pick accepted and stored', () => {
  const step = picker.openFactoryCoverStep({ template: 'product', manifest: FIXTURE });
  const r = picker.resolveFactoryCoverAction(step,
    { action: 'pick', source: 'upload', upload_ref: 'uploads/alex/hero.jpg' }, FIXTURE);
  assert.strictEqual(r.error, null);
  assert.strictEqual(r.state.upload_ref, 'uploads/alex/hero.jpg');
  const a = picker.applyCoverToContract({ template: 'product' }, r.state, FIXTURE);
  assert.strictEqual(a.error, null);
  assert.strictEqual(a.contract.cover.cover_url, 'uploads/alex/hero.jpg');
  assert.strictEqual(a.contract.cover.cover_source, 'upload');
});

test('catch-all templates smoke open', () => {
  for (const t of ['menu', 'portfolio', 'product', 'signup']) {
    const step = picker.openFactoryCoverStep({ template: t, manifest: FIXTURE });
    assert.strictEqual(step.page_type, 'any_other_page');
    assert.ok(step.page_type_note);
    assert.ok(step.born_cover.cover_key);
    const r = picker.resolveFactoryCoverAction(step, { action: 'skip' }, FIXTURE);
    assert.strictEqual(r.error, null);
    assert.strictEqual(r.state.cover_key, step.born_cover.cover_key);
  }
});

test('receipt carries cover', () => {
  const fields = { cover_key: 'open/companion-golden',
    cover_url: 'https://example.invalid/open/companion-golden.jpg',
    cover_source: 'library', cover_via: 'owner_pick', set_by: 'owner', offset_y: 0 };
  const r = picker.factoryCoverReceipt('b-1', 'personal', fields, 'naya-app-alex', 'https://x');
  assert.strictEqual(r.cover.cover_key, 'open/companion-golden');
  assert.strictEqual(r.template, 'personal');
});

test('shelves are featured-first and capped', () => {
  const step = picker.openFactoryCoverStep({ template: 'personal', manifest: FIXTURE });
  for (const [cat, sh] of Object.entries(step.shelves)) {
    assert.ok(sh.covers.length <= 8, cat);
    assert.strictEqual(sh.total, sh.covers.length + sh.more);
  }
  assert.ok(step.shelves.companions);
  assert.deepStrictEqual(step.shelves.companions.featured, ['open/companion-golden']);
});

test('selftest passes', () => {
  const s = picker.selftest();
  assert.strictEqual(s.ok, true, JSON.stringify(s.failed));
});

let failed = 0;
for (const [name, fn] of TESTS) {
  try { fn(); console.log('ok - ' + name); }
  catch (e) { failed++; console.log('FAIL - ' + name + ': ' + e.message); }
}
console.log(TESTS.length - failed + '/' + TESTS.length + ' PASS');
process.exit(failed ? 1 : 0);
