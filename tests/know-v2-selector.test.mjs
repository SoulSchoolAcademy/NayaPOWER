import assert from "node:assert/strict";
import test from "node:test";
import { selectKnowContext } from "../supabase/functions/nayanet-know-runtime/know.ts";

// Graph V2 selector gates in the KNOW retrieval path (contract 0003 —
// CANDIDATE_CONTRACT, pending D1 ratification). The selector must exclude
// superseded, expired, not-yet-valid, revoked, consentless cross-owner, and
// not-applicable edges — while admitting applicable edges and preserving
// legacy two-field projections byte-for-byte.
//
// Every negative case is non-vacuous: it runs the attack universe against a
// baseline with the offending V2 field stripped. The attack must exclude the
// edge AND the baseline must admit it — so each test fails if its gate is
// removed.

const NOW = new Date("2026-09-30T12:00:00Z");
const OWNER = "owner-1";

const req = (overrides = {}) => ({
  owner_id: OWNER,
  naya_id: "NAYA-NODE-0001",
  task_id: "KNOW-V2-001",
  task_class: "V2_SELECTOR",
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
  content: {
    capabilities: ["provenance_preservation"],
    lesson: "Preserve provenance before applying retained intelligence.",
  },
  provenance: { source: "TEST-SEED" },
  evidence_refs: [{ receipt: "test-receipt-1" }],
  superseded_by_block_id: null,
  updated_at: "2026-09-29T00:00:00Z",
  ...overrides,
});

// Source block (selected: newest eligible) -> target block via one edge.
const universe = (edge) => {
  const src = block({ intelligent_block_id: "IB-SRC", connections: [edge] });
  const tgt = block({
    intelligent_block_id: "IB-TGT",
    updated_at: "2026-09-28T00:00:00Z",
    understanding_state: "LEARNED",
  });
  return [src, tgt];
};

const sel = (blocks) => selectKnowContext(req(), blocks, NOW);

// Baseline: same universe with every V2 field stripped from the edge.
// A legacy two-field projection must behave exactly as before V2.
const stripV2 = (blocks) =>
  blocks.map((b) => ({
    ...b,
    connections: Array.isArray(b.connections)
      ? b.connections.map((c) => ({
          target_block_id: c.target_block_id,
          relationship_type: c.relationship_type,
        }))
      : b.connections,
  }));

const relatedIds = (out) => out.related_context.map((e) => e.block_id);

const V2_EDGE = {
  target_block_id: "IB-TGT",
  relationship_type: "SUPPORTS",
  status: "ACTIVE",
  valid_from: "2026-09-29T00:00:00Z",
  valid_until: "2026-10-01T00:00:00Z",
  visibility: "PRIVATE",
  applicability: { state: "APPLICABLE", task_classes: ["V2_SELECTOR"], limitations: [] },
};

// --- Positive controls -----------------------------------------------------

test("V2-P0: applicable edge with full V2 fields IS selected", () => {
  const out = sel(universe({ ...V2_EDGE }));
  assert.equal(out.status, "HIT");
  assert.equal(out.selected_block_id, "IB-SRC");
  assert.deepEqual(relatedIds(out), ["IB-TGT"]);
});

test("V2-P1: legacy two-field edge is admitted unchanged (no V2 fields)", () => {
  const out = sel(universe({ target_block_id: "IB-TGT", relationship_type: "SUPPORTS" }));
  assert.equal(out.status, "HIT");
  assert.deepEqual(relatedIds(out), ["IB-TGT"]);
});

test("V2-P2: UNKNOWN applicability stays admitted (retrieval != applicability)", () => {
  const edge = { ...V2_EDGE, applicability: { state: "UNKNOWN", task_classes: [], limitations: [] } };
  const out = sel(universe(edge));
  assert.deepEqual(relatedIds(out), ["IB-TGT"]);
});

// --- Negative battery ------------------------------------------------------

test("V2-N1: SUPERSEDED edge is NOT selected", () => {
  const edge = { ...V2_EDGE, status: "SUPERSEDED" };
  const attack = sel(universe(edge));
  assert.deepEqual(relatedIds(attack), []);
  const baseline = sel(stripV2(universe(edge)));
  assert.deepEqual(relatedIds(baseline), ["IB-TGT"]);
});

test("V2-N2: REVOKED edge is NOT selected", () => {
  const edge = { ...V2_EDGE, status: "REVOKED" };
  const attack = sel(universe(edge));
  assert.deepEqual(relatedIds(attack), []);
  const baseline = sel(stripV2(universe(edge)));
  assert.deepEqual(relatedIds(baseline), ["IB-TGT"]);
});

test("V2-N3: expired edge (valid_until in the past) is NOT selected", () => {
  const edge = { ...V2_EDGE, valid_until: "2026-09-29T00:00:00Z" };
  const attack = sel(universe(edge));
  assert.deepEqual(relatedIds(attack), []);
  const baseline = sel(stripV2(universe(edge)));
  assert.deepEqual(relatedIds(baseline), ["IB-TGT"]);
});

test("V2-N4: not-yet-valid edge (valid_from in the future) is NOT selected", () => {
  const edge = { ...V2_EDGE, valid_from: "2026-10-01T00:00:00Z" };
  const attack = sel(universe(edge));
  assert.deepEqual(relatedIds(attack), []);
  const baseline = sel(stripV2(universe(edge)));
  assert.deepEqual(relatedIds(baseline), ["IB-TGT"]);
});

test("V2-N5: DERIVED_SHARED edge without consent_ref is NOT selected", () => {
  const edge = { ...V2_EDGE, visibility: "DERIVED_SHARED", consent_ref: null };
  const attack = sel(universe(edge));
  assert.deepEqual(relatedIds(attack), []);
  // With explicit consent the same edge is admitted.
  const consented = sel(universe({ ...edge, consent_ref: "consent-123" }));
  assert.deepEqual(relatedIds(consented), ["IB-TGT"]);
});

test("V2-N6: NOT_APPLICABLE edge is NOT selected", () => {
  const edge = {
    ...V2_EDGE,
    applicability: { state: "NOT_APPLICABLE", task_classes: [], limitations: ["out of scope"] },
  };
  const attack = sel(universe(edge));
  assert.deepEqual(relatedIds(attack), []);
  const baseline = sel(stripV2(universe(edge)));
  assert.deepEqual(relatedIds(baseline), ["IB-TGT"]);
});

test("V2-N7: supersession by relationship_id excludes the superseded edge", () => {
  const tgtB = block({
    intelligent_block_id: "IB-TGT-B",
    updated_at: "2026-09-28T00:00:00Z",
    understanding_state: "LEARNED",
  });
  const src = block({
    intelligent_block_id: "IB-SRC",
    connections: [
      { ...V2_EDGE, relationship_id: "rel-old" },
      {
        target_block_id: "IB-TGT-B",
        relationship_type: "SUPPORTS",
        status: "ACTIVE",
        relationship_id: "rel-new",
        supersedes_relationship_id: "rel-old",
      },
    ],
  });
  const out = sel([src, universe({ ...V2_EDGE })[1], tgtB]);
  // rel-old is superseded by rel-new: only IB-TGT-B's edge survives.
  assert.deepEqual(relatedIds(out), ["IB-TGT-B"]);
});

test("V2-N8: expired SUPERSEDES edge is NOT followed by the chase", () => {
  const newer = block({ intelligent_block_id: "IB-NEWER", updated_at: "2026-09-28T00:00:00Z" });
  const older = block({
    intelligent_block_id: "IB-OLDER",
    updated_at: "2026-09-29T00:00:00Z",
    connections: [
      {
        target_block_id: "IB-NEWER",
        relationship_type: "SUPERSEDES",
        status: "ACTIVE",
        valid_until: "2026-09-29T00:00:00Z", // expired before NOW
      },
    ],
  });
  const attack = sel([older, newer]);
  assert.equal(attack.status, "HIT");
  assert.equal(attack.selected_block_id, "IB-OLDER");
  assert.doesNotMatch(attack.reason, /SUPERSEDES_EDGE_FOLLOWED/);
  // Baseline: the same edge without the expiry IS followed.
  const baseline = sel(stripV2([older, newer]));
  assert.equal(baseline.selected_block_id, "IB-NEWER");
  assert.match(baseline.reason, /SUPERSEDES_EDGE_FOLLOWED/);
});

test("V2-N9: malformed temporal value fails closed", () => {
  const edge = { ...V2_EDGE, valid_from: "not-a-time" };
  const attack = sel(universe(edge));
  assert.deepEqual(relatedIds(attack), []);
  const baseline = sel(stripV2(universe(edge)));
  assert.deepEqual(relatedIds(baseline), ["IB-TGT"]);
});

test("V2-N10: unrecognized status fails closed", () => {
  const edge = { ...V2_EDGE, status: "DURABLE" }; // block status, not an edge status
  const attack = sel(universe(edge));
  assert.deepEqual(relatedIds(attack), []);
});
