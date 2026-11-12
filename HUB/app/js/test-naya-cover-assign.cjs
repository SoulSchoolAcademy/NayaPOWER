/* test-naya-cover-assign.cjs — tests for the manifest-driven assignment engine.
 * Run: node HUB/app/js/test-naya-cover-assign.cjs
 * No dependencies. Exit 0 = all pass; any failure prints and exits 1.
 * The live-manifest tests read the CURRENT manifest at
 * HUB/covers/manifest.json (../../covers/manifest.json from here), so the
 * counts are structural (>=, contains) — the live manifest grows as
 * Resolve supplies covers. The pinned-snapshot record with exact counts
 * lives in the PI workspace (cover-library-wiring/naya-cover-assign.test.js).
 * Fixture tests use a hand-built manifest so the logic never depends on
 * the live shelf's contents.
 */
'use strict';

var assert = require('node:assert');
var fs = require('node:fs');
var path = require('node:path');
var Assign = require('./naya-cover-assign.js');

var LIVE = JSON.parse(fs.readFileSync(path.join(__dirname, '..', '..', 'covers', 'manifest.json'), 'utf8'));

var passed = 0;
var failed = 0;
function test(name, fn) {
  try {
    fn();
    passed++;
    console.log('PASS ' + name);
  } catch (e) {
    failed++;
    console.log('FAIL ' + name + ' :: ' + (e && e.message));
  }
}

function fixtureManifest() {
  return {
    assignment_on_page_creation: {
      personal_page: 'area/personal',
      business_page: 'area/business',
      space: 'area/spaces',
      events_page: 'area/events',
      booking_page: 'area/booking',
      any_other_page: 'rotation set',
    },
    assets: [
      { key: 'area/personal', file: 'areas/personal.jpg', kind: 'area', status: 'ready', name: 'Area — Personal', category: 'house-area', suits: 'personal pages', credit: 'Naya Resolve', tier: 'signature' },
      { key: 'area/business', file: 'areas/business.jpg', kind: 'area', status: 'ready', name: 'Area — Business', category: 'house-area', suits: 'business pages', credit: 'Naya Resolve', tier: 'signature' },
      { key: 'area/spaces', file: 'areas/spaces.jpg', kind: 'area', status: 'ready', name: 'Area — Spaces', category: 'house-area', suits: 'spaces', credit: 'Naya Resolve', tier: 'signature' },
      { key: 'area/events', file: 'areas/events.jpg', kind: 'area', status: 'ready', name: 'Area — Events', category: 'house-area', suits: 'event pages', credit: 'Naya Resolve', tier: 'signature' },
      { key: 'area/booking', file: 'areas/booking.jpg', kind: 'area', status: 'designed', name: 'Area — Booking', category: 'house-area', suits: 'booking pages (designed)', credit: 'Naya Resolve', tier: 'signature' },
      { key: 'open/companion-golden', file: 'open/companion-golden.jpg', kind: 'open', status: 'ready', name: 'Companion Golden', category: 'companions', suits: 'a golden retriever at dawn, for dog lovers', credit: 'Naya Resolve', tier: 'open', featured_class: 'citizen', featured_order: 1 },
      { key: 'open/quiet-office', file: 'open/quiet-office.jpg', kind: 'open', status: 'ready', name: 'Quiet Office', category: 'craft', suits: 'a clean minimal office for professionals', credit: 'Naya Resolve', tier: 'open' },
      { key: 'open/retired-one', file: 'open/retired.jpg', kind: 'open', status: 'retired', name: 'Retired One', category: 'abstract', suits: 'retired', credit: 'Naya Resolve', tier: 'open' },
      { key: 'open/no-tier', file: 'open/no-tier.jpg', kind: 'open', status: 'ready', name: 'No Tier', category: 'abstract', suits: 'incomplete card', credit: 'Naya Resolve' },
      { key: 'rotation/hero', file: '01-hero.jpg', kind: 'rotation', status: 'ready', name: 'Hero', category: 'house-signature', suits: 'flagship', credit: 'Naya Resolve', tier: 'signature' },
      { key: 'rotation/second', file: '02-second.jpg', kind: 'rotation', status: 'ready', name: 'Second', category: 'house-signature', suits: 'flagship', credit: 'Naya Resolve', tier: 'signature' },
      { key: 'open/exclusive-one', file: 'open/exclusive.jpg', kind: 'open', status: 'ready', name: 'Exclusive One', category: 'cosmos', suits: 'her face', credit: 'Naya Resolve', tier: 'jewel', featured_class: 'exclusive' },
    ],
    typical_terms: { areas: {
      'companions-pets': { terms: ['dog', 'cat', 'puppy', 'pets'], covers: ['companion-golden'] },
      'business-professional': { terms: ['office', 'business', 'clean'], covers: ['quiet-office'] },
    } },
  };
}

/* ── 1. Assignment table: the born cover by page type ── */
test('defaults come from the assignment table (all 4 area types)', function () {
  var m = fixtureManifest();
  var cases = [['personal_page', 'area/personal'], ['business_page', 'area/business'],
    ['space', 'area/spaces'], ['events_page', 'area/events']];
  cases.forEach(function (c) {
    var d = Assign.assignCoverForPage({ pageType: c[0], page: {}, manifest: m });
    assert.strictEqual(d.cover_key, c[1]);
    assert.strictEqual(d.via, 'area_default');
    assert.strictEqual(d.set_by, 'system');
    assert.strictEqual(d.source, 'library');
    assert.strictEqual(d.cover_url, Assign.DEFAULT_ASSET_BASE + 'areas/' + c[1].split('/')[1] + '.jpg');
  });
});

test('designed default is NOT served: booking falls through to rotation', function () {
  var m = fixtureManifest();
  var d = Assign.assignCoverForPage({ pageType: 'booking_page', page: {}, manifest: m, seed: 0 });
  assert.notStrictEqual(d.cover_key, 'area/booking');
  assert.strictEqual(d.via, 'rotation');
  assert.strictEqual(d.cover_key, 'rotation/hero');
});

test('unknown page type cycles the rotation deterministically by seed', function () {
  var m = fixtureManifest();
  assert.strictEqual(Assign.assignCoverForPage({ pageType: 'any_other_page', page: {}, manifest: m, seed: 0 }).cover_key, 'rotation/hero');
  assert.strictEqual(Assign.assignCoverForPage({ pageType: 'any_other_page', page: {}, manifest: m, seed: 1 }).cover_key, 'rotation/second');
  assert.strictEqual(Assign.assignCoverForPage({ pageType: 'any_other_page', page: {}, manifest: m, seed: 2 }).cover_key, 'rotation/hero');
  assert.strictEqual(Assign.assignCoverForPage({ pageType: 'mystery_page', page: {}, manifest: m, seed: 1 }).cover_key, 'rotation/second');
});

/* ── 2. Recommendation: the matched pick ── */
test('recommend: dog page surfaces Companion Golden with a why', function () {
  var m = fixtureManifest();
  var page = { page_type: 'personal_page', purpose: 'a page for my dog', topics: ['dog', 'pets'] };
  var rec = Assign.recommend(page, m, false);
  assert.strictEqual(rec.top_pick, 'open/companion-golden');
  assert.ok(rec.why && rec.why.indexOf('Companion Golden') === 5);
  assert.ok(rec.signals.length >= 2);
  var d = Assign.assignCoverForPage({ pageType: 'membership_page', page: page, manifest: m });
  assert.strictEqual(d.cover_key, 'open/companion-golden');
  assert.strictEqual(d.via, 'recommendation');
});

test('recommend: office page surfaces Quiet Office', function () {
  var m = fixtureManifest();
  var page = { page_type: 'business_page', purpose: 'my consulting office', topics: ['office', 'business'] };
  var rec = Assign.recommend(page, m, false);
  assert.strictEqual(rec.top_pick, 'open/quiet-office');
});

test('recommend: thin page data surfaces nothing (falls back, never blank)', function () {
  var m = fixtureManifest();
  var rec = Assign.recommend({}, m, false);
  assert.strictEqual(rec.top_pick, null);
  var d = Assign.assignCoverForPage({ pageType: 'membership_page', page: {}, manifest: m, seed: 0 });
  assert.strictEqual(d.via, 'rotation');
});

test('recommend: citizens never get exclusive or house covers', function () {
  var m = fixtureManifest();
  var shelf = Assign.citizenShelf(m, false);
  var keys = shelf.map(function (a) { return a.key; });
  assert.ok(keys.indexOf('open/exclusive-one') < 0);
  assert.ok(keys.indexOf('rotation/hero') < 0);
  assert.ok(keys.indexOf('open/retired-one') < 0);
  assert.ok(keys.indexOf('open/no-tier') < 0);
  assert.ok(keys.indexOf('open/companion-golden') >= 0);
  var nayaShelf = Assign.citizenShelf(m, true);
  assert.ok(nayaShelf.map(function (a) { return a.key; }).indexOf('rotation/hero') >= 0);
});

/* ── 3. Never blank ── */
test('empty manifest still assigns the built-in default, never null', function () {
  var d = Assign.assignCoverForPage({ pageType: 'personal_page', page: {}, manifest: {} });
  assert.strictEqual(d.cover_key, Assign.DEFAULT_COVER);
  assert.strictEqual(d.cover_url, Assign.DEFAULT_COVER);
  assert.strictEqual(d.via, 'builtin_default');
  var d2 = Assign.assignCoverForPage({ pageType: 'personal_page', page: {}, manifest: null });
  assert.strictEqual(d2.cover_key, Assign.DEFAULT_COVER);
});

/* ── 4. URL resolution ── */
test('coverUrl resolves key to the raw asset base; unknown key is null', function () {
  var m = fixtureManifest();
  assert.strictEqual(Assign.coverUrl(m, 'area/personal'), Assign.DEFAULT_ASSET_BASE + 'areas/personal.jpg');
  assert.strictEqual(Assign.coverUrl(m, 'area/personal', 'https://nayanet.app/covers'), 'https://nayanet.app/covers/areas/personal.jpg');
  assert.strictEqual(Assign.coverUrl(m, 'area/nope'), null);
});

/* ── 5. Birth-shorthand parity (naya-page-birth.js delegation) ── */
var BIRTH_MANIFEST = {
  areas: {
    'area/personal': '/covers/area-personal.jpg',
    'area/business': '/covers/area-business.jpg',
    'area/spaces': '/covers/area-spaces.jpg',
    'area/events': '/covers/area-events.jpg',
  },
  rotating: ['/covers/rot-1.jpg', '/covers/rot-2.jpg', '/covers/rot-3.jpg'],
};

test('legacy: area key hit for personal/business/space/events', function () {
  assert.strictEqual(Assign.assignCoverLegacy('personal', BIRTH_MANIFEST, 0).cover, '/covers/area-personal.jpg');
  assert.strictEqual(Assign.assignCoverLegacy('business', BIRTH_MANIFEST, 0).cover, '/covers/area-business.jpg');
  assert.strictEqual(Assign.assignCoverLegacy('space', BIRTH_MANIFEST, 0).cover, '/covers/area-spaces.jpg');
  assert.strictEqual(Assign.assignCoverLegacy('events', BIRTH_MANIFEST, 0).cover, '/covers/area-events.jpg');
  assert.strictEqual(Assign.assignCoverLegacy('personal', BIRTH_MANIFEST, 0).source, 'area');
  assert.strictEqual(Assign.assignCoverLegacy('personal', BIRTH_MANIFEST, 0).key, 'area/personal');
});

test('legacy: missing area key falls to rotating, deterministically', function () {
  var noArea = { areas: {}, rotating: BIRTH_MANIFEST.rotating };
  assert.strictEqual(Assign.assignCoverLegacy('personal', noArea, 0).cover, '/covers/rot-1.jpg');
  assert.strictEqual(Assign.assignCoverLegacy('personal', noArea, 0).source, 'rotating');
  assert.strictEqual(Assign.assignCoverLegacy('personal', noArea, 1).cover, '/covers/rot-2.jpg');
  assert.strictEqual(Assign.assignCoverLegacy('personal', noArea, 5).cover, '/covers/rot-3.jpg');
  assert.strictEqual(Assign.assignCoverLegacy('personal', noArea, 0).key, 'rotating[0]');
});

test('legacy: empty manifest still assigns the built-in default, never null', function () {
  var r = Assign.assignCoverLegacy('personal', null, 0);
  assert.strictEqual(r.cover, Assign.DEFAULT_COVER);
  assert.strictEqual(r.source, 'default');
  assert.strictEqual(r.key, null);
  var r2 = Assign.assignCoverLegacy('space', { areas: {}, rotating: [] }, 0);
  assert.strictEqual(r2.cover, Assign.DEFAULT_COVER);
});

/* ── 6. Page types ── */
test('pageTypes covers the assignment table plus membership + catch-all', function () {
  var pts = Assign.pageTypes(fixtureManifest());
  ['personal_page', 'business_page', 'space', 'events_page', 'booking_page', 'membership_page', 'any_other_page'].forEach(function (pt) {
    assert.ok(pts.indexOf(pt) >= 0, 'missing ' + pt);
  });
});

/* ── 7. Live manifest snapshot (pinned 2026-11-12) ── */
test('live: 89 assets; 4 area defaults ready and assigned', function () {
  var cases = [['personal_page', 'area/personal'], ['business_page', 'area/business'],
    ['space', 'area/spaces'], ['events_page', 'area/events']];
  cases.forEach(function (c) {
    var d = Assign.assignCoverForPage({ pageType: c[0], page: {}, manifest: LIVE });
    assert.strictEqual(d.cover_key, c[1], c[0]);
    assert.strictEqual(d.via, 'area_default');
  });
  assert.strictEqual(Assign.coverUrl(LIVE, 'area/personal'),
    'https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/HUB/covers/areas/personal.jpg');
});

test('live: the 3 designed defaults fall through (Resolve owed supply)', function () {
  [['booking_page', 'area/booking'], ['templates_gallery', 'area/templates'], ['dashboard_intel', 'area/intel-today']].forEach(function (c) {
    var d = Assign.assignCoverForPage({ pageType: c[0], page: {}, manifest: LIVE, seed: 0 });
    assert.notStrictEqual(d.cover_key, c[1], c[0] + ' must not serve a designed cover');
    assert.ok(d.via === 'rotation' || d.via === 'recommendation', c[0] + ' via=' + d.via);
  });
  var v = Assign.validateManifest(LIVE);
  var notReady = v.defaults_not_ready.map(function (r) { return r[1]; });
  ['area/booking', 'area/intel-today', 'area/templates'].forEach(function (k) {
    assert.ok(notReady.indexOf(k) >= 0, k + ' must be flagged not-ready until supplied');
  });
});

test('live: validate counts match the measured manifest', function () {
  var v = Assign.validateManifest(LIVE);
  assert.ok(v.assets >= 89, 'assets=' + v.assets);
  assert.ok(v.ready >= 85, 'ready=' + v.ready);
  assert.ok(v.rotation_size >= 11, 'rotation=' + v.rotation_size);
  assert.ok(v.citizen_servable >= 66, 'servable=' + v.citizen_servable);
  assert.ok(v.featured_citizen >= 13, 'featured=' + v.featured_citizen);
  assert.ok(v.retired.indexOf('open/prosperity-city') >= 0);
  var dangling = v.dangling_term_refs.map(function (r) { return r.join(':'); });
  assert.ok(dangling.indexOf('business-professional:facets family') >= 0, 'facets family ref flagged');
});

test('live: dog page recommends a companions cover; office page a business cover', function () {
  var dog = Assign.recommend({ purpose: 'a page for my dog', topics: ['dog', 'pets'] }, LIVE, false);
  assert.ok(dog.top_pick, 'dog page must surface a pick');
  assert.ok(dog.top_pick.indexOf('companion') >= 0 || dog.top_pick.indexOf('best-friends') >= 0 || dog.top_pick.indexOf('cat-sovereign') >= 0, 'dog pick=' + dog.top_pick);
  var office = Assign.recommend({ purpose: 'my consulting office', topics: ['office', 'business'] }, LIVE, false);
  assert.ok(office.top_pick, 'office page must surface a pick');
});

/* ── 8. Match scoring parity (smart_match_v1_1) ── */
test('matchScore: identical topics+goals vectors score 65 with both signals', function () {
  var a = { topics: ['dog', 'pets'], goals: ['companions-pets'], offers: [], needs: [], wants: [] };
  var r = Assign.matchScore(a, a);
  assert.strictEqual(r.score, 65);
  assert.deepStrictEqual(r.signals.sort(), ['goals', 'topics']);
  assert.strictEqual(r.surface, true);
});

test('matchScore: empty vectors score 0 and do not surface', function () {
  var r = Assign.matchScore({ topics: [], goals: [], offers: [], needs: [], wants: [] },
    { topics: ['dog'], goals: [], offers: [], needs: [], wants: [] });
  assert.strictEqual(r.score, 0);
  assert.strictEqual(r.surface, false);
});

console.log('\n' + passed + ' passed, ' + failed + ' failed');
process.exit(failed ? 1 : 0);
