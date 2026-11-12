import test from "node:test";
import assert from "node:assert/strict";

// Behavior matrix for the CONNECT-owned edge admissibility gate.
// IMPORTS THE SHIPPED MODULE — this test executes the real selector code path
// (supabase/functions/_shared/connect_selector.ts), not a mirror. Any behavior
// change to the gate must update this matrix.
//
// Contract: Graph V2 selector gates (contract 0003-GRAPH-RELATIONSHIP-CONTRACT-V2).
// An edge carrying no V2 fields is a legacy two-field projection and passes
// every gate. V2-carrying edges are held to V2 semantics; malformed values
// fail closed.
import {
  v2EdgeExclusionReason,
  selectableConnections,
} from "../supabase/functions/_shared/connect_selector.ts";

const NOW = Date.parse("2026-10-07T15:00:00Z");
const FUTURE = new Date(NOW + 3600_000).toISOString();
const PAST = new Date(NOW - 3600_000).toISOString();

const parsed = (overrides = {}) => ({
  target_block_id: "block-b",
  relationship_type: "SUPPORTS",
  relationship_id: null,
  supersedes_relationship_id: null,
  status: null,
  epistemic_state: null,
  valid_from: null,
  valid_until: null,
  visibility: null,
  consent_ref: null,
  applicability_state: null,
  ...overrides,
});

const carrier = (conns) => ({ connections: conns });

test("selector matrix — legacy edge passes every gate", () => {
  assert.equal(v2EdgeExclusionReason(parsed(), new Set(), NOW), null);
});

test("selector matrix — terminal statuses excluded", () => {
  assert.equal(v2EdgeExclusionReason(parsed({ status: "SUPERSEDED" }), new Set(), NOW), "EDGE_STATUS_SUPERSEDED");
  assert.equal(v2EdgeExclusionReason(parsed({ status: "REVOKED" }), new Set(), NOW), "EDGE_STATUS_REVOKED");
  assert.equal(v2EdgeExclusionReason(parsed({ status: "INVALIDATED" }), new Set(), NOW), "EDGE_STATUS_INVALIDATED");
  assert.equal(v2EdgeExclusionReason(parsed({ status: "ACTIVE" }), new Set(), NOW), null);
  assert.equal(v2EdgeExclusionReason(parsed({ status: "BOGUS" }), new Set(), NOW), "EDGE_STATUS_UNKNOWN");
});

test("selector matrix — terminal epistemic states excluded", () => {
  assert.equal(v2EdgeExclusionReason(parsed({ epistemic_state: "SUPERSEDED" }), new Set(), NOW), "EDGE_EPISTEMIC_SUPERSEDED");
  assert.equal(v2EdgeExclusionReason(parsed({ epistemic_state: "INVALIDATED" }), new Set(), NOW), "EDGE_EPISTEMIC_INVALIDATED");
  assert.equal(v2EdgeExclusionReason(parsed({ epistemic_state: "SUPPORTED" }), new Set(), NOW), null);
});

test("selector matrix — supersession by newer edge", () => {
  const c = parsed({ relationship_id: "rel-1" });
  assert.equal(v2EdgeExclusionReason(c, new Set(["rel-1"]), NOW), "EDGE_SUPERSEDED_BY_NEWER_EDGE");
  assert.equal(v2EdgeExclusionReason(c, new Set(["rel-9"]), NOW), null);
});

test("selector matrix — temporal window", () => {
  assert.equal(v2EdgeExclusionReason(parsed({ valid_from: FUTURE }), new Set(), NOW), "EDGE_NOT_YET_VALID");
  assert.equal(v2EdgeExclusionReason(parsed({ valid_until: PAST }), new Set(), NOW), "EDGE_EXPIRED");
  assert.equal(v2EdgeExclusionReason(parsed({ valid_from: PAST, valid_until: FUTURE }), new Set(), NOW), null);
  assert.equal(v2EdgeExclusionReason(parsed({ valid_from: "not-a-date" }), new Set(), NOW), "EDGE_TEMPORAL_INVALID");
  assert.equal(v2EdgeExclusionReason(parsed({ valid_until: "not-a-date" }), new Set(), NOW), "EDGE_TEMPORAL_INVALID");
});

test("selector matrix — consent gate", () => {
  assert.equal(v2EdgeExclusionReason(parsed({ visibility: "PUBLIC_DERIVED" }), new Set(), NOW), "EDGE_CROSS_OWNER_CONSENT_REQUIRED");
  assert.equal(v2EdgeExclusionReason(parsed({ visibility: "PUBLIC_DERIVED", consent_ref: "consent-1" }), new Set(), NOW), null);
  assert.equal(v2EdgeExclusionReason(parsed({ visibility: "PRIVATE" }), new Set(), NOW), null);
  assert.equal(v2EdgeExclusionReason(parsed({ visibility: "BOGUS" }), new Set(), NOW), "EDGE_VISIBILITY_UNKNOWN");
});

test("selector matrix — applicability tristate", () => {
  assert.equal(v2EdgeExclusionReason(parsed({ applicability_state: "NOT_APPLICABLE" }), new Set(), NOW), "EDGE_NOT_APPLICABLE");
  assert.equal(v2EdgeExclusionReason(parsed({ applicability_state: "UNKNOWN" }), new Set(), NOW), null);
  assert.equal(v2EdgeExclusionReason(parsed({ applicability_state: "APPLICABLE" }), new Set(), NOW), null);
});

test("selector matrix — selectableConnections filters a mixed projection", () => {
  const block = carrier([
    { target_block_id: "good", relationship_type: "SUPPORTS" },
    { target_block_id: "stale", relationship_type: "SUPPORTS", status: "SUPERSEDED" },
    { target_block_id: "forged", relationship_type: "NOT_A_REAL_TYPE" },
    { target_block_id: "", relationship_type: "SUPPORTS" },
    { target_block_id: "old", relationship_id: "rel-old", relationship_type: "REFINES" },
    { target_block_id: "new", relationship_id: "rel-new", relationship_type: "REFINES", supersedes_relationship_id: "rel-old" },
    { target_block_id: "consentless", relationship_type: "SUPPORTS", visibility: "PUBLIC_DERIVED" },
  ]);
  const selected = selectableConnections(block, NOW).map((c) => c.target_block_id).sort();
  assert.deepEqual(selected, ["good", "new"]);
});

test("selector matrix — empty and malformed carriers", () => {
  assert.deepEqual(selectableConnections({}, NOW), []);
  assert.deepEqual(selectableConnections({ connections: null }, NOW), []);
  assert.deepEqual(selectableConnections({ connections: "x" }, NOW), []);
});
