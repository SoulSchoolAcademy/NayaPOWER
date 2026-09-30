import assert from "node:assert/strict";
import test from "node:test";
import { selectKnowContext } from "../supabase/functions/nayanet-know-runtime/know.ts";

// Edge-aware retrieval: the graph must be load-bearing. These tests prove that
// relationships change retrieval behavior for the right reason, and that
// stale, forged, irrelevant, private, or revoked edges cannot influence it.

const OWNER = "owner-1";
const req = (overrides = {}) => ({
  owner_id: OWNER,
  naya_id: "NAYA-NODE-0001",
  task_id: "KNOW-EDGE-001",
  task_class: "EDGE_CONTEXT",
  required_capability: "provenance_preservation",
  ...overrides,
});
const block = (overrides = {}) => ({
  intelligent_block_id: "IB-BASE",
  owner_id: OWNER,
  status: "DURABLE",
  understanding_state: "VERIFIED",
  owner_scope: "PRIVATE",
  applicable_scope: { target: "NAYA-NODE-0001" },
  content: { lesson: "Preserve provenance before applying retained intelligence; retrieval never grants authority." },
  provenance: { source: "TEST-SEED" },
  evidence_refs: [{ receipt: "test-receipt-1" }],
  superseded_by_block_id: null,
  updated_at: "2026-09-29T00:00:00Z",
  ...overrides,
});

test("EDGE: SUPERSEDES chase follows the edge to the current truth", () => {
  // IB-OLDER is newer by timestamp, so flat recency selection would pick it.
  // The SUPERSEDES edge must override recency: the graph changes the outcome.
  const newer = block({ intelligent_block_id: "IB-NEWER", updated_at: "2026-09-28T00:00:00Z" });
  const older = block({
    intelligent_block_id: "IB-OLDER",
    updated_at: "2026-09-29T00:00:00Z",
    connections: [{ target_block_id: "IB-NEWER", relationship_type: "SUPERSEDES" }],
  });
  const out = selectKnowContext(req(), [older, newer]);
  assert.equal(out.status, "HIT");
  assert.equal(out.selected_block_id, "IB-NEWER");
  assert.match(out.reason, /SUPERSEDES_EDGE_FOLLOWED/);
});

test("EDGE: SUPPORTS edge attaches eligible related context", () => {
  const main = block({
    intelligent_block_id: "IB-MAIN",
    connections: [{ target_block_id: "IB-SUPPORT", relationship_type: "SUPPORTS" }],
  });
  const support = block({ intelligent_block_id: "IB-SUPPORT", understanding_state: "LEARNED" });
  const out = selectKnowContext(req(), [main, support]);
  assert.equal(out.status, "HIT");
  assert.equal(out.selected_block_id, "IB-MAIN");
  assert.equal(out.related_context.length, 1);
  assert.equal(out.related_context[0].block_id, "IB-SUPPORT");
  assert.equal(out.related_context[0].relationship_type, "SUPPORTS");
  assert.match(out.related_context[0].why_admitted, /eligible owner-scoped/);
  assert.equal(out.conflict_detected, false);
});

test("EDGE: CONTRADICTS is surfaced as conflict, never merged", () => {
  const main = block({
    intelligent_block_id: "IB-MAIN",
    connections: [{ target_block_id: "IB-RIVAL", relationship_type: "CONTRADICTS" }],
  });
  const rival = block({ intelligent_block_id: "IB-RIVAL", understanding_state: "VERIFIED" });
  const out = selectKnowContext(req(), [main, rival]);
  assert.equal(out.status, "HIT");
  assert.equal(out.selected_block_id, "IB-MAIN");
  assert.equal(out.conflict_detected, true);
  assert.equal(out.related_context.length, 1);
  assert.match(out.related_context[0].why_admitted, /surfaced as conflict, not merged/);
});

test("EDGE: demotion guard — edges cannot launder ineligible blocks", () => {
  // A CANDIDATE target must neither capture the selection via SUPERSEDES
  // nor appear as related context via SUPPORTS.
  const main = block({
    intelligent_block_id: "IB-MAIN",
    connections: [
      { target_block_id: "IB-CAND", relationship_type: "SUPERSEDES" },
      { target_block_id: "IB-CAND", relationship_type: "SUPPORTS" },
    ],
  });
  const cand = block({ intelligent_block_id: "IB-CAND", understanding_state: "CANDIDATE" });
  const out = selectKnowContext(req(), [main, cand]);
  assert.equal(out.selected_block_id, "IB-MAIN");
  assert.equal(out.reason, "OWNER_SCOPED_CURRENT_BLOCK_MATCHES_REQUIRED_CAPABILITY");
  assert.deepEqual(out.related_context, []);
  assert.equal(out.conflict_detected, false);
});

test("EDGE: forged edges — unknown relationship types are ignored", () => {
  const main = block({
    intelligent_block_id: "IB-MAIN",
    connections: [{ target_block_id: "IB-X", relationship_type: "MIND_CONTROLS" }],
  });
  const x = block({ intelligent_block_id: "IB-X" });
  const out = selectKnowContext(req(), [main, x]);
  assert.equal(out.status, "HIT");
  assert.deepEqual(out.related_context, []);
  assert.equal(out.conflict_detected, false);
});

test("EDGE: private edges — cross-owner targets cannot influence retrieval", () => {
  const main = block({
    intelligent_block_id: "IB-MAIN",
    connections: [{ target_block_id: "IB-OTHER", relationship_type: "SUPPORTS" }],
  });
  const other = block({ intelligent_block_id: "IB-OTHER", owner_id: "other-owner" });
  const out = selectKnowContext(req(), [main, other]);
  assert.deepEqual(out.related_context, []);
  assert.equal(out.conflict_detected, false);
});

test("EDGE: no edges — behavior is byte-identical to flat retrieval", () => {
  const out = selectKnowContext(req(), [block({ intelligent_block_id: "IB-PLAIN" })]);
  assert.equal(out.status, "HIT");
  assert.equal(out.selected_block_id, "IB-PLAIN");
  assert.equal(out.reason, "OWNER_SCOPED_CURRENT_BLOCK_MATCHES_REQUIRED_CAPABILITY");
  assert.deepEqual(out.related_context, []);
  assert.equal(out.conflict_detected, false);
});

test("EDGE: MISS carries empty related context and no conflict", () => {
  const out = selectKnowContext(
    req({ required_capability: "nonexistent_capability" }),
    [block({ intelligent_block_id: "IB-PLAIN" })]
  );
  assert.equal(out.status, "MISS");
  assert.deepEqual(out.related_context, []);
  assert.equal(out.conflict_detected, false);
});
