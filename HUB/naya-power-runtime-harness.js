/* Harness for naya-power-runtime.js (tick t0480).
 * Proves, without touching any room HTML:
 *  1. an accessor returns parsed+validated data against a REAL fixture feed
 *     (today.json, copied byte-for-byte from the t0479 emission);
 *  2. a broken live feed (invalid JSON) falls back to L1 localStorage, no throw;
 *  3. an absent live feed with empty L1 falls back to the L2 empty-but-valid
 *     envelope, no throw;
 *  4. every accessor name the hub's live METHOD_MAP expects exists and is a
 *     function (METHOD_MAP-preferred names + brief short names + search/retrieve);
 *  5. the adapter's invoke() semantics (from index-8.html js/runtime-live.js)
 *     resolve against this bridge without throwing for today/lists/reports/spaces.
 * Exit 0 = all green; any failure prints and exits 1.
 */
'use strict';
const fs = require('fs');
const path = require('path');

let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (detail ? ' — ' + detail : '')); }
}

// ---- environment stubs ----
const store = {};
globalThis.localStorage = {
  getItem: k => (k in store ? store[k] : null),
  setItem: (k, v) => { store[k] = String(v); },
  removeItem: k => { delete store[k]; },
};

const FIXTURE_TODAY = fs.readFileSync(
  path.join(__dirname, 'naya-power-runtime-fixtures', 'today.json'), 'utf8');

const SEED_REPORTS = JSON.stringify({
  contract: 'room-feed/v1', room: 'reports',
  emitted_at: '2026-10-01T09:00:00-07:00',
  source_ref: 'engine-job:seed', items: [],
});

globalThis.fetch = async function (url, opts) {
  if (String(url).endsWith('/today.json')) return { ok: true, json: async () => JSON.parse(FIXTURE_TODAY) };
  if (String(url).endsWith('/lists.json')) return { ok: true, json: async () => { throw new Error('Unexpected token'); } };
  return { ok: false, status: 404, json: async () => ({}) };
};

globalThis.__NPR_FEED_BASE__ = 'https://example.test/feeds/';
const R = require('./naya-power-runtime.js');

(async () => {
  console.log('T1 accessor returns parsed+validated data (today vs real fixture)');
  const t = await R.today();
  check('ok true', t.ok === true);
  check('state ready', t.state === 'ready', t.state);
  check('contract handshake', t.data.contract === 'room-feed/v1' && t.data.room === 'today');
  check('20 items', t.data.items.length === 20, String(t.data.items.length));
  check('every item base fields', t.data.items.every(i =>
    typeof i.id === 'string' && i.id && typeof i.title === 'string' &&
    Array.isArray(i.topics) && i.topics.length >= 1 && typeof i.kind === 'string'));
  check('priority/blocker/next_action present', t.data.items.every(i =>
    typeof i.priority === 'number' && typeof i.blocker === 'boolean' && typeof i.next_action === 'string'));
  check('staleness visible', t.data._feed_meta && typeof t.data._feed_meta.age_seconds === 'number' && t.data._feed_meta.source === 'live',
    JSON.stringify(t.data._feed_meta));
  check('L1 write-through', store['nayanet.today.feed.v1'] != null);
  check('alias parity', (await R.intelligenceToday()).data.room === 'today' &&
    (await R.dailyIntelligence()).data.items.length === 20);

  console.log('T2 broken live feed -> L1 fallback, no throw');
  store['nayanet.lists.feed.v1'] = JSON.stringify({
    contract: 'room-feed/v1', room: 'lists',
    emitted_at: '2026-10-14T08:00:00-07:00',
    source_ref: 'engine-job:seed', items: [],
  });
  const l = await R.lists();
  check('ok true', l.ok === true);
  check('state cached', l.state === 'cached', l.state);
  check('data from L1', l.data._feed_meta.source === 'cache' && l.data.room === 'lists');
  check('L1 staleness visible', typeof l.data._feed_meta.age_seconds === 'number');

  console.log('T3 absent feed + empty L1 -> L2 empty envelope, no throw');
  const r = await R.reports();
  check('ok true', r.ok === true);
  check('state empty', r.state === 'empty', r.state);
  check('empty-but-valid envelope', r.data.contract === 'room-feed/v1' && r.data.room === 'reports' &&
    Array.isArray(r.data.items) && r.data.items.length === 0 && r.data._feed_meta.source === 'empty');

  console.log('T4 every METHOD_MAP name exists as a function');
  const names = [
    'smartFeed', 'intelligenceToday', 'dailyIntelligence', 'today',
    'smartReports', 'intelligenceReports', 'reports',
    'intelligentLibrary', 'knowledgeLibrary', 'library',
    'smartLedger', 'executionLedger', 'ledger',
    'smartConnections', 'relationshipIntelligence', 'connections',
    'smartLists', 'intelligenceLists', 'lists',
    'smartMail', 'messages', 'mail',
    'smartSpaces', 'contextSpaces', 'spaces',
    'settingsSnapshot', 'runtimeSnapshot', 'settings',
    'connect', 'manifest',
    'searchIntelligence', 'askNaya', 'search', 'retrieveIntelligence',
    'retrieveIntelligentBlock', 'getIntelligentBlock', 'retrieve',
    'runtimeStatus',
  ];
  const missing = names.filter(n => typeof R[n] !== 'function');
  check('all ' + names.length + ' accessors present', missing.length === 0, 'missing: ' + missing.join(','));
  check('identity object', R.identity && typeof R.identity === 'object');

  console.log('T5 adapter invoke() semantics (mirrors runtime-live.js) resolve without throw');
  const METHOD_MAP = {
    feed: ['smartFeed'],
    today: ['intelligenceToday', 'dailyIntelligence', 'today'],
    reports: ['smartReports', 'reports', 'intelligenceReports'],
    library: ['intelligentLibrary', 'library', 'knowledgeLibrary'],
    ledger: ['smartLedger', 'ledger', 'executionLedger'],
    connections: ['smartConnections', 'connections', 'relationshipIntelligence'],
    lists: ['smartLists', 'lists', 'intelligenceLists'],
    mail: ['smartMail', 'mail', 'messages'],
    spaces: ['smartSpaces', 'spaces', 'contextSpaces'],
    settings: ['settingsSnapshot', 'runtimeSnapshot'],
  };
  async function invoke(candidates, payload) {
    const name = candidates.find(n => typeof R[n] === 'function');
    if (!name) return { ok: false, state: 'not_verified' };
    try {
      const out = await R[name](payload);
      if (out == null) return { ok: true, state: 'empty', data: [] };
      if (out.ok === false) return { ...out, state: out.state || 'error' };
      return { ok: true, state: out.state || 'ready', data: out.data || out };
    } catch (err) { return { ok: false, state: 'error', message: err.message }; }
  }
  for (const room of ['today', 'lists', 'reports', 'spaces']) {
    const out = await invoke(METHOD_MAP[room] || [], {});
    check('invoke(' + room + ') no throw, method resolved',
      out.ok === true && ['ready', 'cached', 'empty'].includes(out.state),
      JSON.stringify(out).slice(0, 120));
  }
  const sf = await invoke(METHOD_MAP.feed, {});
  check('smartFeed honestly not_verified (feed wire untouched)', sf.ok === false && sf.state === 'not_verified');

  console.log('\n' + pass + ' passed, ' + fail + ' failed');
  process.exit(fail ? 1 : 0);
})().catch(e => { console.log('HARNESS THREW: ' + e.stack); process.exit(1); });
