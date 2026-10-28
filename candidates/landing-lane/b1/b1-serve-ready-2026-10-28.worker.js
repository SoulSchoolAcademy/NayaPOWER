'use strict';
/*
 * b1-serve-ready-2026-10-28.worker.js — B1 SHAPE CONTRACT, JS mirror
 * (TEAM BUILD, 2026-10-28). Workspace only, NOT deployed, NOT live.
 *
 * Purpose: the same {counts, items} shape contract as the Python
 * serve-ready module (workspace/system/b1-serve-ready-2026-10-28.py),
 * expressed in the language the merged Cloudflare worker runs, so the
 * landing lane (Nitro) wires proven logic instead of re-deriving it.
 *
 * This file contains PURE SHAPING ONLY — no fetch, no runtime I/O.
 * The worker's live fetch (query at serve time, project filter, paged
 * read) is the landing lane's wiring and is NOT proven here. What IS
 * proven here (node fixture tests): dedup, owner mapping, area-null,
 * face fields, counts math, and the 503 unavailable shape.
 *
 * Rules (identical to the Python module):
 *  - One row per item_key, most recently updated wins (input rows are
 *    ordered updated_at DESC NULLS LAST; ties -> first seen).
 *  - owner_seat -> owner (null stays null; face shows "Ownerless").
 *  - area: null on EVERY row (area schema not applied; nothing derived).
 *  - Failure body carries NO items and NO counts, ever.
 */
const PROJECT = 'a554e536-66a6-4808-8c36-988f13d9f394';
const FACE_FIELDS = ['item_key', 'title', 'state', 'owner', 'priority',
  'evidence_url', 'next_action', 'blocker', 'updated_at', 'area'];

function shapeItems(rows) {
  const seen = new Map();
  for (const row of (rows || [])) {
    const k = row.item_key;
    if (!seen.has(k)) seen.set(k, row);
  }
  const items = [];
  for (const j of seen.values()) {
    items.push({
      item_key: j.item_key, title: j.title, state: j.state,
      owner: j.owner_seat, priority: j.priority,
      evidence_url: j.evidence_url, next_action: j.next_action,
      blocker: j.blocker, updated_at: j.updated_at, area: null,
      maker_seat: j.maker_seat, prover_seat: j.prover_seat,
    });
  }
  return items;
}

function buildCounts(items, rowsRead) {
  return {
    rows_read: rowsRead,
    unique: items.length,
    done_proven: items.filter((it) => it.state === 'done_proven').length,
  };
}

function buildResponse(rows, generatedAt, mapping) {
  const items = shapeItems(rows);
  return {
    counts: buildCounts(items, rows.length),
    items: items,
    per_app: computePerApp(items, mapping),
    project: 'NayaPOWER',
    project_id: PROJECT,
    generated_at: generatedAt || new Date().toISOString().replace(/\.\d+Z$/, 'Z'),
    area_note: "area is null on every row (area schema not applied; face shows 'unplaced' honestly; no areas derived or invented)",
    dedup_rule: 'one row per item_key, most recently updated wins',
    source: 'live work_items (read-only), NOT a snapshot, NOT live-served yet',
  };
}

// Per-app done/total (App Brief standard). Mapping {item_key -> app} is
// supplied by the caller (FILL-pipeline data); NOTHING is inferred from
// key prefixes or titles here. Absent mapping -> everything unmapped,
// reconciling honestly. Mapping keys absent from items create no apps.
function computePerApp(items, mapping) {
  const m = mapping || {};
  const perApp = {};
  let unmappedDone = 0, unmappedTotal = 0, mappedKeys = 0;
  for (const it of (items || [])) {
    const app = m[it.item_key];
    if (app) {
      mappedKeys++;
      const slot = perApp[app] || (perApp[app] = { done: 0, total: 0 });
      slot.total++;
      if (it.state === 'done_proven') slot.done++;
    } else {
      unmappedTotal++;
      if (it.state === 'done_proven') unmappedDone++;
    }
  }
  return {
    per_app: perApp,
    unmapped: { done: unmappedDone, total: unmappedTotal },
    mapping: {
      mapped_keys: mappedKeys, unmapped_keys: unmappedTotal,
      note: 'apps come from the supplied mapping only; no app is inferred from key prefixes or titles; unmapped rows are counted honestly, never hidden',
    },
  };
}

function unavailableResponse(reason) {
  return {
    error: 'live_rows_unavailable',
    status: 503,
    message: 'Live rows unavailable — the face must show unavailable, never a stale snapshot.',
    reason: String(reason == null ? '' : reason).slice(0, 300),
    project_id: PROJECT,
    generated_at: new Date().toISOString().replace(/\.\d+Z$/, 'Z'),
  };
}

module.exports = { PROJECT, FACE_FIELDS, shapeItems, buildCounts, buildResponse, unavailableResponse, computePerApp };
