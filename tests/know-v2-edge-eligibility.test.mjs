import assert from "node:assert/strict";
import test from "node:test";
import { selectKnowContext, isSelectableEdge, enrichConnectionsWithCanonical } from "../supabase/functions/nayanet-know-runtime/know.ts";

// Graph Relationship Contract V2 edge-selection invariant in the LIVE
// retrieval path. These tests prove the selector enforces temporal validity,
// status, epistemic terminal states, consent for shared visibility, and
// applicability on the edges it follows or admits — the same invariant the
// proof harness (graphRelationshipEligible) enforces, now live in KNOW.
//
// Policy under test (reviewable; D1 may tighten): an edge is judged on what
// it declares. applicability.state === "UNKNOWN" (the writer's default for
// unclassified edges) does NOT exclude.

const OWNER = "owner-1";
const NOW = new Date("2026-09-30T12:00:00Z");
const req = (overrides = {}) => ({
  owner_id: OWNER,
  naya_id: "NAYA-NODE-0001",
  task_id: "KNOW-V2-001",
  task_class: "provenance_sensitive",
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
const edge = (overrides = {}) => ({
  target_block_id: "IB-NEW",
  relationship_type: "SUPERSEDES",
  status: "ACTIVE",
  epistemic_state: "VERIFIED",
  visibility: "PRIVATE",
  consent_ref: null,
  valid_from: "2026-09-29T00:00:00Z",
  valid_until: null,
  applicability: { state: "APPLICABLE", task_classes: ["provenance_sensitive"], limitations: [] },
  ...overrides,
});

test("V2: fully valid edge is selectable", () => {
  const r = isSelectableEdge(edge(), req(), NOW);
  assert.equal(r.ok, true);
});

test("V2: expired edge (valid_until in past) is not selectable", () => {
  const r = isSelectableEdge(edge({ valid_until: "2026-09-29T23:59:59Z" }), req(), NOW);
  assert.equal(r.ok, false);
  assert.equal(r.reason, "EDGE_EXPIRED");
});

test("V2: not-yet-valid edge (valid_from in future) is not selectable", () => {
  const r = isSelectableEdge(edge({ valid_from: "2026-10-01T00:00:00Z" }), req(), NOW);
  assert.equal(r.ok, false);
  assert.equal(r.reason, "EDGE_NOT_YET_VALID");
});

test("V2: non-ACTIVE status edge is not selectable", () => {
  const r = isSelectableEdge(edge({ status: "SUPERSEDED" }), req(), NOW);
  assert.equal(r.ok, false);
  assert.equal(r.reason, "EDGE_STATUS_NOT_ACTIVE");
});

test("V2: terminal epistemic state edge is not selectable", () => {
  const r = isSelectableEdge(edge({ epistemic_state: "SUPERSEDED" }), req(), NOW);
  assert.equal(r.ok, false);
  assert.equal(r.reason, "EDGE_EPISTEMIC_TERMINAL");
});

test("V2: writer-default CANDIDATE epistemic edge IS selectable (graduates via verification)", () => {
  const r = isSelectableEdge(edge({ epistemic_state: "CANDIDATE" }), req(), NOW);
  assert.equal(r.ok, true);
});

test("V2: DERIVED_SHARED without consent_ref is not selectable (shared by choice)", () => {
  const r = isSelectableEdge(edge({ visibility: "DERIVED_SHARED", consent_ref: null }), req(), NOW);
  assert.equal(r.ok, false);
  assert.equal(r.reason, "EDGE_SHARED_WITHOUT_CONSENT");
});

test("V2: DERIVED_SHARED with consent_ref is selectable", () => {
  const r = isSelectableEdge(edge({ visibility: "DERIVED_SHARED", consent_ref: "consent-123" }), req(), NOW);
  assert.equal(r.ok, true);
});

test("V2: NOT_APPLICABLE edge is not selectable", () => {
  const r = isSelectableEdge(edge({ applicability: { state: "NOT_APPLICABLE", task_classes: [], limitations: [] } }), req(), NOW);
  assert.equal(r.ok, false);
  assert.equal(r.reason, "EDGE_NOT_APPLICABLE");
});

test("V2: APPLICABLE edge with wrong task class is not selectable", () => {
  const r = isSelectableEdge(
    edge({ applicability: { state: "APPLICABLE", task_classes: ["other_class"], limitations: [] } }),
    req({ task_class: "provenance_sensitive" }), NOW);
  assert.equal(r.ok, false);
  assert.equal(r.reason, "EDGE_TASK_CLASS_MISMATCH");
});

test("V2: UNKNOWN applicability (unclassified) edge IS selectable — classification is LEARN's job", () => {
  const r = isSelectableEdge(edge({ applicability: { state: "UNKNOWN", task_classes: [], limitations: [] } }), req(), NOW);
  assert.equal(r.ok, true);
});

test("V2: legacy edge with no V2 metadata is selectable (block-level gates remain the backstop)", () => {
  const r = isSelectableEdge({ target_block_id: "IB-X", relationship_type: "SUPPORTS" }, req(), NOW);
  assert.equal(r.ok, true);
});

test("V2: malformed valid_from is fail-closed", () => {
  const r = isSelectableEdge(edge({ valid_from: "not-a-date" }), req(), NOW);
  assert.equal(r.ok, false);
  assert.equal(r.reason, "EDGE_VALID_FROM_MALFORMED");
});

test("V2: expired SUPERSEDES edge is not followed; selection stays on primary with blocked reason", () => {
  const oldB = block({ intelligent_block_id: "IB-OLD", connections: [edge({ target_block_id: "IB-NEW", valid_until: "2026-09-01T00:00:00Z" })] });
  const newB = block({ intelligent_block_id: "IB-NEW", updated_at: "2026-09-28T00:00:00Z" });
  const res = selectKnowContext(req(), [oldB, newB], NOW);
  assert.equal(res.status, "HIT");
  assert.equal(res.selected_block_id, "IB-OLD");
  assert.match(res.reason, /^SUPERSEDES_EDGE_BLOCKED:IB-NEW:EDGE_EXPIRED$/);
});

test("V2: valid SUPERSEDES edge is still followed", () => {
  const oldB = block({ intelligent_block_id: "IB-OLD", connections: [edge({ target_block_id: "IB-NEW" })] });
  const newB = block({ intelligent_block_id: "IB-NEW", updated_at: "2026-09-28T00:00:00Z" });
  const res = selectKnowContext(req(), [oldB, newB], NOW);
  assert.equal(res.selected_block_id, "IB-NEW");
  assert.match(res.reason, /^SUPERSEDES_EDGE_FOLLOWED:IB-NEW$/);
});

test("V2: shared-without-consent edge cannot annotate related context", () => {
  const main = block({
    intelligent_block_id: "IB-MAIN",
    connections: [edge({ target_block_id: "IB-REL", relationship_type: "SUPPORTS", visibility: "DERIVED_SHARED", consent_ref: null })],
  });
  const rel = block({ intelligent_block_id: "IB-REL", updated_at: "2026-09-28T00:00:00Z" });
  const res = selectKnowContext(req(), [main, rel], NOW);
  assert.equal(res.status, "HIT");
  assert.deepEqual(res.related_context, []);
});

test("V2: consented shared edge annotates related context", () => {
  const main = block({
    intelligent_block_id: "IB-MAIN",
    connections: [edge({ target_block_id: "IB-REL", relationship_type: "SUPPORTS", visibility: "DERIVED_SHARED", consent_ref: "consent-9" })],
  });
  const rel = block({ intelligent_block_id: "IB-REL", updated_at: "2026-09-28T00:00:00Z" });
  const res = selectKnowContext(req(), [main, rel], NOW);
  assert.equal(res.related_context.length, 1);
  assert.equal(res.related_context[0].block_id, "IB-REL");
});

test("V2: enrichment joins canonical rows onto the projection before selection", () => {
  const blocks = [block({ intelligent_block_id: "IB-A", connections: [{ target_block_id: "IB-B", relationship_type: "SUPPORTS" }] })];
  const rels = [{
    source_id: "IB-A", target_id: "IB-B", relationship_type: "SUPPORTS",
    status: "ACTIVE", epistemic_state: "VERIFIED", visibility: "PRIVATE",
    consent_ref: null, valid_from: "2026-09-29T00:00:00Z", valid_until: "2026-09-01T00:00:00Z",
    applicability: { state: "APPLICABLE", task_classes: ["provenance_sensitive"], limitations: [] },
  }];
  const enriched = enrichConnectionsWithCanonical(blocks, rels);
  const conn = enriched[0].connections[0];
  assert.equal(conn.valid_until, "2026-09-01T00:00:00Z");
  assert.equal(conn.status, "ACTIVE");
  // And the expired canonical row now blocks the edge at selection time.
  const b = block({ intelligent_block_id: "IB-B", updated_at: "2026-09-28T00:00:00Z" });
  const res = selectKnowContext(req(), [enriched[0], b], NOW);
  assert.deepEqual(res.related_context, []);
});

test("V2: enrichment leaves connections without canonical rows untouched (legacy path)", () => {
  const blocks = [block({ intelligent_block_id: "IB-A", connections: [{ target_block_id: "IB-B", relationship_type: "SUPPORTS" }] })];
  const enriched = enrichConnectionsWithCanonical(blocks, []);
  assert.deepEqual(enriched[0].connections, [{ target_block_id: "IB-B", relationship_type: "SUPPORTS" }]);
});
