'use strict';
// test-b1-serve-ready-2026-10-28.worker.cjs — Fixture tests for the JS
// shape-contract mirror. Workspace only. Exits 0 only if every check
// passes. These are FIXTURE tests: the worker's live fetch is NOT proven
// here (that proof is the Python module's live test, run separately).
const W = require('./b1-serve-ready-2026-10-28.worker.js');
const FAILURES = [];
function check(name, cond, detail) {
  console.log((cond ? 'PASS' : 'FAIL') + ' ' + name + (detail ? ' ' + detail : ''));
  if (!cond) FAILURES.push(name);
}
const rows = [
  { item_key: 'k1', title: 'Old', state: 'queued', owner_seat: null, priority: 1, evidence_url: null, next_action: 'a', blocker: null, maker_seat: 'm', prover_seat: null, updated_at: '2026-10-20T00:00:00+00:00' },
  { item_key: 'k1', title: 'New', state: 'in_progress', owner_seat: 'naya-power', priority: 2, evidence_url: 'http://x', next_action: 'b', blocker: null, maker_seat: 'm', prover_seat: 'p', updated_at: '2026-10-27T00:00:00+00:00' },
  { item_key: 'k2', title: 'TieFirst', state: 'queued', owner_seat: 'naya-resolve', priority: 1, evidence_url: null, next_action: 'c', blocker: null, maker_seat: 'm', prover_seat: null, updated_at: '2026-10-25T00:00:00+00:00' },
  { item_key: 'k2', title: 'TieSecond', state: 'queued', owner_seat: 'nitro', priority: 1, evidence_url: null, next_action: 'd', blocker: null, maker_seat: 'm', prover_seat: null, updated_at: '2026-10-25T00:00:00+00:00' },
  { item_key: 'k3', title: 'Done', state: 'done_proven', owner_seat: null, priority: 1, evidence_url: 'http://y', next_action: null, blocker: null, maker_seat: 'm', prover_seat: 'p', updated_at: '2026-10-26T00:00:00+00:00' },
];
const rowsSorted = [...rows].sort((a, b) => (b.updated_at || '').localeCompare(a.updated_at || ''));
const items = W.shapeItems(rowsSorted);
const byKey = {};
for (const it of items) byKey[it.item_key] = it;
check('W1 dedup-most-recent-wins', byKey.k1.title === 'New' && items.length === 3, 'items=' + items.length);
check('W2 dedup-tie-first-seen', byKey.k2.title === 'TieFirst', 'k2=' + byKey.k2.title);
check('W3 owner-mapping', byKey.k1.owner === 'naya-power' && byKey.k3.owner === null, 'k1=' + byKey.k1.owner);
check('W4 area-null-all', items.every((it) => it.area === null), '');
check('W4b face-fields-all', items.every((it) => W.FACE_FIELDS.every((k) => k in it)), '');
const counts = W.buildCounts(items, 5);
check('W5 counts-math', counts.rows_read === 5 && counts.unique === 3 && counts.done_proven === 1, JSON.stringify(counts));
const resp = W.buildResponse(rowsSorted, '2026-10-28T00:00:00Z');
check('W6 response-shape', resp.counts.unique === 3 && resp.items.length === 3 && resp.project_id === W.PROJECT, '');
const un = W.unavailableResponse('simulated failure');
check('W7 unavailable-503', un.status === 503 && un.error === 'live_rows_unavailable', 'status=' + un.status);
check('W7b unavailable-no-items-no-counts', !('items' in un) && !('counts' in un), 'keys=' + Object.keys(un).sort().join(','));
const shaped = [
  { item_key: 'a1', title: 'A1', state: 'done_proven', owner: null, area: null },
  { item_key: 'a2', title: 'A2', state: 'queued', owner: null, area: null },
  { item_key: 'b1', title: 'B1', state: 'in_progress', owner: null, area: null },
  { item_key: 'u1', title: 'U1', state: 'done_proven', owner: null, area: null },
];
const pa = W.computePerApp(shaped, { a1: 'App A', a2: 'App A', b1: 'App B', 'ghost-key': 'Ghost App' });
check('W8 per-app-grouping', JSON.stringify(pa.per_app) === JSON.stringify({ 'App A': { done: 1, total: 2 }, 'App B': { done: 0, total: 1 } }), JSON.stringify(pa.per_app));
check('W9 unmapped-bucket', pa.unmapped.done === 1 && pa.unmapped.total === 1, JSON.stringify(pa.unmapped));
check('W10 phantom-ignored', !('Ghost App' in pa.per_app), 'ghost absent');
const tot = Object.values(pa.per_app).reduce((a, v) => a + v.total, 0) + pa.unmapped.total;
const dn = Object.values(pa.per_app).reduce((a, v) => a + v.done, 0) + pa.unmapped.done;
check('W11 reconciliation-invariant', tot === 4 && dn === 2, 'tot=' + tot + ' done=' + dn);
console.log('FAILURES:', FAILURES.length ? FAILURES : 'none');
console.log('ALL_PASS:', FAILURES.length === 0);
process.exit(FAILURES.length ? 1 : 0);
