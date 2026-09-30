import assert from "node:assert/strict";
import test from "node:test";
import { selectKnowContext } from "../supabase/functions/nayanet-know-runtime/know.ts";

// Negative battery for the edge-aware KNOW retrieval seam (OSRA Wave 2,
// Worker E cases N0–N6). Each case injects an adversarial edge and compares
// the attack run against a no-edge baseline: the attack must be evaluated
// and rejected, never silently absent. Every test is non-vacuous: it fails
// if the guard it targets is removed.

const OWNER_A = "owner-a";
const OWNER_B = "owner-b";

const reqA = (overrides = {}) => ({
  owner_id: OWNER_A,
  naya_id: "NAYA-NODE-0001",
  task_id: "KNOW-NEG-001",
  task_class: "deploy_checklist_review",
  required_capability: "provenance_preservation",
  ...overrides,
});

const mkBlock = (overrides = {}) => ({
  intelligent_block_id: "IB-FIXTURE",
  owner_id: OWNER_A,
  status: "DURABLE",
  understanding_state: "VERIFIED",
  owner_scope: "PRIVATE",
  applicable_scope: { target: "NAYA-NODE-0001" },
  content: {
    capabilities: ["provenance_preservation"],
    lesson: "Preserve provenance before applying retained intelligence.",
  },
  provenance: { source: "FIXTURE-SEED" },
  evidence_refs: [{ receipt: "fixture-receipt-1" }],
  superseded_by_block_id: null,
  updated_at: "2026-09-29T00:00:00Z",
  ...overrides,
});

// The no-edge baseline for a universe: identical request, edges stripped.
const baselineOf = (blocks) =>
  selectKnowContext(
    reqA(),
    blocks.map((b) => ({ ...b, connections: undefined }))
  );

// ---------------------------------------------------------------------------
// N0 — Positive control: SUPPORTS edge is evaluated and admitted.
// The edge changes the result (related_context gains the target) for the
// right reason. If the allowlist admission were removed, this fails.
// ---------------------------------------------------------------------------
test("NEG N0: SUPPORTS edge is evaluated and admitted as related context", () => {
  const main = mkBlock({
    intelligent_block_id: "IB-N0-MAIN",
    connections: [{ target_block_id: "IB-N0-SUP", relationship_type: "SUPPORTS" }],
  });
  const sup = mkBlock({ intelligent_block_id: "IB-N0-SUP", understanding_state: "LEARNED" });
  const out = selectKnowContext(reqA(), [main, sup]);
  const base = baselineOf([main, sup]);

  assert.equal(out.status, "HIT");
  assert.equal(out.selected_block_id, "IB-N0-MAIN");
  // The edge was evaluated and admitted — the ONLY delta vs baseline.
  assert.equal(out.related_context.length, 1);
  assert.equal(out.related_context[0].block_id, "IB-N0-SUP");
  assert.equal(out.related_context[0].relationship_type, "SUPPORTS");
  assert.match(out.related_context[0].why_admitted, /eligible owner-scoped/);
  assert.equal(out.conflict_detected, false);
  const { related_context: _r, conflict_detected: _c, ...outRest } = out;
  const { related_context: _br, conflict_detected: _bc, ...baseRest } = base;
  assert.deepEqual(outRest, baseRest);
});

// ---------------------------------------------------------------------------
// N1 — Forged edge: target with empty provenance is rejected.
// isEligibleBlock requires non-empty provenance; the edge dies with its
// target. If the provenance check were removed, the ghost would be admitted.
// ---------------------------------------------------------------------------
test("NEG N1: edge to a provenance-empty target contributes zero", () => {
  const main = mkBlock({
    intelligent_block_id: "IB-N1-MAIN",
    connections: [
      { target_block_id: "IB-N1-GHOST", relationship_type: "SUPPORTS" },
      { target_block_id: "IB-N1-GHOST", relationship_type: "SUPERSEDES" },
    ],
  });
  const ghost = mkBlock({
    intelligent_block_id: "IB-N1-GHOST",
    provenance: {}, // forged/empty: fails the trust gate
    updated_at: "2026-09-30T00:00:00Z", // newer — would win flat recency
  });
  const out = selectKnowContext(reqA(), [main, ghost]);
  const base = baselineOf([main, ghost]);

  assert.deepEqual(out, base); // identical to the no-edge baseline
  assert.equal(out.selected_block_id, "IB-N1-MAIN");
  assert.match(out.reason, /OWNER_SCOPED_CURRENT_BLOCK_MATCHES_REQUIRED_CAPABILITY/);
  assert.deepEqual(out.related_context, []);
});

// ---------------------------------------------------------------------------
// N2a — Stale edge, status arm: a SUPERSEDED-status target is rejected.
// If SUPERSEDED were added to the servable statuses, the stale endorsement
// would resurrect and the chase would follow — this fails.
// ---------------------------------------------------------------------------
test("NEG N2a: SUPERSEDED-status targets are rejected (status arm)", () => {
  const target_new = mkBlock({ intelligent_block_id: "IB-N2-NEW", updated_at: "2026-09-27T00:00:00Z" });
  const target_old = mkBlock({
    intelligent_block_id: "IB-N2-OLD",
    status: "SUPERSEDED",
    // No superseded_by_block_id pointer here: this arm isolates the status
    // check. (N2b covers the pointer arm.)
  });
  const main = mkBlock({
    intelligent_block_id: "IB-N2-MAIN",
    updated_at: "2026-09-28T00:00:00Z",
    connections: [
      { target_block_id: "IB-N2-OLD", relationship_type: "SUPPORTS" },
      { target_block_id: "IB-N2-OLD", relationship_type: "SUPERSEDES" },
    ],
  });
  const out = selectKnowContext(reqA(), [main, target_old, target_new]);
  const base = baselineOf([main, target_old, target_new]);

  assert.deepEqual(out, base);
  assert.equal(out.selected_block_id, "IB-N2-MAIN");
  assert.deepEqual(out.related_context, []);
  assert.match(out.reason, /OWNER_SCOPED_CURRENT_BLOCK_MATCHES_REQUIRED_CAPABILITY/);
});

// ---------------------------------------------------------------------------
// N2b — Stale edge, pointer arm: a block carrying superseded_by_block_id is
// rejected even when its status row is still servable (writer-race shape).
// If the pointer check were removed, the chase would follow into the stale
// target and the endorsement would attach — this fails.
// ---------------------------------------------------------------------------
test("NEG N2b: superseded_by_block_id pointer rejects even a servable-status target", () => {
  const target_new = mkBlock({ intelligent_block_id: "IB-N2B-NEW", updated_at: "2026-09-27T00:00:00Z" });
  const target_old = mkBlock({
    intelligent_block_id: "IB-N2B-OLD",
    status: "ACTIVE", // servable status, but the supersession pointer is set
    superseded_by_block_id: "IB-N2B-NEW",
  });
  const main = mkBlock({
    intelligent_block_id: "IB-N2B-MAIN",
    updated_at: "2026-09-28T00:00:00Z",
    connections: [
      { target_block_id: "IB-N2B-OLD", relationship_type: "SUPPORTS" },
      { target_block_id: "IB-N2B-OLD", relationship_type: "SUPERSEDES" },
    ],
  });
  const out = selectKnowContext(reqA(), [main, target_old, target_new]);
  const base = baselineOf([main, target_old, target_new]);

  assert.deepEqual(out, base);
  assert.equal(out.selected_block_id, "IB-N2B-MAIN");
  assert.deepEqual(out.related_context, []);
  assert.match(out.reason, /OWNER_SCOPED_CURRENT_BLOCK_MATCHES_REQUIRED_CAPABILITY/);
});

// ---------------------------------------------------------------------------
// N3 — Irrelevant edge: related context is gated on the required capability.
// A SUPPORTS edge to an eligible block that does not serve the requested
// capability must not annotate the result. Guard added with this battery.
// ---------------------------------------------------------------------------
test("NEG N3: SUPPORTS edge to a capability-mismatched target is rejected", () => {
  const main = mkBlock({
    intelligent_block_id: "IB-N3-MAIN",
    connections: [{ target_block_id: "IB-N3-BILLING", relationship_type: "SUPPORTS" }],
  });
  const billing = mkBlock({
    intelligent_block_id: "IB-N3-BILLING",
    content: { capabilities: ["billing_audit"], lesson: "Billing audit lesson." },
  });
  const out = selectKnowContext(reqA(), [main, billing]);
  const base = baselineOf([main, billing]);

  assert.deepEqual(out, base);
  assert.deepEqual(out.related_context, []);
  assert.equal(out.selected_block_id, "IB-N3-MAIN");
});

// ---------------------------------------------------------------------------
// N4 — Contradiction injection: CONTRADICTS is surfaced, never merged.
// The conflict names the injected target; selection and epistemic state are
// untouched (no winner is picked, nothing is upgraded). If conflict
// surfacing were removed, conflict_detected would be false and this fails.
// ---------------------------------------------------------------------------
test("NEG N4: CONTRADICTS is surfaced as conflict, selection untouched", () => {
  const a = mkBlock({
    intelligent_block_id: "IB-N4-A",
    updated_at: "2026-09-29T00:00:00Z",
    connections: [{ target_block_id: "IB-N4-B", relationship_type: "CONTRADICTS" }],
  });
  const b = mkBlock({
    intelligent_block_id: "IB-N4-B",
    updated_at: "2026-09-28T00:00:00Z",
  });
  const out = selectKnowContext(reqA(), [a, b]);
  const base = baselineOf([a, b]);

  assert.equal(out.status, "HIT");
  // No winner picked: selection identical to baseline.
  assert.equal(out.selected_block_id, base.selected_block_id);
  assert.equal(out.selected_epistemic_state, "VERIFIED"); // not upgraded
  // The conflict is surfaced and names the injected edge target.
  assert.equal(out.conflict_detected, true);
  assert.equal(out.related_context.length, 1);
  assert.equal(out.related_context[0].block_id, "IB-N4-B");
  assert.equal(out.related_context[0].relationship_type, "CONTRADICTS");
  assert.match(out.related_context[0].why_admitted, /surfaced as conflict, not merged/);
});

// ---------------------------------------------------------------------------
// N5 — Privacy: cross-owner edge target is excluded with no oracle.
// The attack run must be byte-identical to a universe where the foreign edge
// target does not exist; a control run as the owning owner proves the edge
// itself is well-formed (exclusion is scope, not a broken edge).
// ---------------------------------------------------------------------------
test("NEG N5: cross-owner edge target excluded, no oracle in the result", () => {
  const main = mkBlock({
    intelligent_block_id: "IB-N5-MAIN",
    connections: [{ target_block_id: "IB-N5-SECRET", relationship_type: "SUPPORTS" }],
  });
  const secret = mkBlock({ intelligent_block_id: "IB-N5-SECRET", owner_id: OWNER_B });
  const attack = selectKnowContext(reqA(), [main, secret]);
  const base = selectKnowContext(reqA(), [main]); // universe without the foreign block

  assert.deepEqual(attack, base); // no count/name/reason oracle
  assert.deepEqual(attack.related_context, []);

  // Control: as owner B the same edge shape is admitted — the edge is fine.
  const bMain = mkBlock({
    intelligent_block_id: "IB-N5-BMAIN",
    owner_id: OWNER_B,
    connections: [{ target_block_id: "IB-N5-SECRET", relationship_type: "SUPPORTS" }],
  });
  const control = selectKnowContext(reqA({ owner_id: OWNER_B }), [bMain, secret]);
  assert.equal(control.status, "HIT");
  assert.equal(control.related_context.length, 1);
  assert.equal(control.related_context[0].block_id, "IB-N5-SECRET");
});

// ---------------------------------------------------------------------------
// N6 — Authority laundering: retrieval never becomes authorization.
// Even with an AUTHORIZED_BY edge and provenance claiming a grant, the
// result carries retrieval_creates_authority=false and the reason text
// contains no authorization language.
// ---------------------------------------------------------------------------
test("NEG N6: authority claims in edges/provenance confer zero authority", () => {
  const auth = mkBlock({
    intelligent_block_id: "IB-N6-AUTH",
    provenance: { source: "FIXTURE-SEED", law_grant: "GRANTED", authorized: true },
  });
  const main = mkBlock({
    intelligent_block_id: "IB-N6-MAIN",
    updated_at: "2026-09-29T12:00:00Z", // unambiguously primary: recency tiebreak must not select the grant-claiming block
    connections: [{ target_block_id: "IB-N6-AUTH", relationship_type: "AUTHORIZED_BY" }],
  });
  const out = selectKnowContext(reqA(), [main, auth]);

  assert.equal(out.retrieval_creates_authority, false);
  assert.match(out.reason, /^(SUPERSEDES_EDGE_FOLLOWED|OWNER_SCOPED_CURRENT_BLOCK_MATCHES_REQUIRED_CAPABILITY)/);
  assert.doesNotMatch(out.reason, /authorized|permitted|granted/i);
  // AUTHORIZED_BY is not a context edge: it neither annotates nor steers.
  assert.deepEqual(out.related_context, []);
  assert.equal(out.conflict_detected, false);
});

// ---------------------------------------------------------------------------
// TOCTOU — edges resolve from the same snapshot as selection.
// The universe contains two rows for the chase target: a stale SUPERSEDED
// duplicate first, the live row second. First occurrence wins (no re-fetch,
// no last-wins). A re-fetching implementation would select IB-T-TOCTOU.
// ---------------------------------------------------------------------------
test("NEG TOCTOU: supersession chase uses the input snapshot, no re-fetch", () => {
  const staleDup = mkBlock({
    intelligent_block_id: "IB-T-TOCTOU",
    status: "SUPERSEDED",
    superseded_by_block_id: "IB-T-OTHER",
  });
  const liveDup = mkBlock({ intelligent_block_id: "IB-T-TOCTOU", updated_at: "2026-09-28T00:00:00Z" });
  const main = mkBlock({
    intelligent_block_id: "IB-T-MAIN",
    updated_at: "2026-09-29T12:00:00Z",
    connections: [{ target_block_id: "IB-T-TOCTOU", relationship_type: "SUPERSEDES" }],
  });
  const out = selectKnowContext(reqA(), [main, staleDup, liveDup]);

  assert.equal(out.selected_block_id, "IB-T-MAIN");
  assert.match(out.reason, /OWNER_SCOPED_CURRENT_BLOCK_MATCHES_REQUIRED_CAPABILITY/);
});

// ---------------------------------------------------------------------------
// Revoked target: a SUPPORTS edge to a REVOKED-status block is rejected.
// ---------------------------------------------------------------------------
test("NEG REVOKED: edge to a revoked-status target contributes zero", () => {
  const main = mkBlock({
    intelligent_block_id: "IB-R-MAIN",
    connections: [{ target_block_id: "IB-R-REV", relationship_type: "SUPPORTS" }],
  });
  const revoked = mkBlock({ intelligent_block_id: "IB-R-REV", status: "REVOKED" });
  const out = selectKnowContext(reqA(), [main, revoked]);
  const base = baselineOf([main, revoked]);

  assert.deepEqual(out, base);
  assert.deepEqual(out.related_context, []);
});

// ---------------------------------------------------------------------------
// Candidate target: an unpromoted (CANDIDATE) target can neither capture the
// chase nor appear as related context — even when it is newer by recency.
// ---------------------------------------------------------------------------
test("NEG CANDIDATE: unpromoted target cannot steer selection or context", () => {
  const main = mkBlock({
    intelligent_block_id: "IB-C-MAIN",
    updated_at: "2026-09-28T00:00:00Z",
    connections: [
      { target_block_id: "IB-C-CAND", relationship_type: "SUPERSEDES" },
      { target_block_id: "IB-C-CAND", relationship_type: "SUPPORTS" },
    ],
  });
  const cand = mkBlock({
    intelligent_block_id: "IB-C-CAND",
    understanding_state: "CANDIDATE",
    updated_at: "2026-09-30T00:00:00Z", // newer — a naive recency pick would prefer it
  });
  const out = selectKnowContext(reqA(), [main, cand]);
  const base = baselineOf([main, cand]);

  assert.deepEqual(out, base);
  assert.equal(out.selected_block_id, "IB-C-MAIN");
  assert.match(out.reason, /OWNER_SCOPED_CURRENT_BLOCK_MATCHES_REQUIRED_CAPABILITY/);
  assert.deepEqual(out.related_context, []);
});

// ---------------------------------------------------------------------------
// Unknown relationship type: forged types are inert — a valid SUPERSEDES
// edge in the same connection list still works, the forged one does not.
// ---------------------------------------------------------------------------
test("NEG UNKNOWN-TYPE: forged relationship types are inert", () => {
  const newer = mkBlock({ intelligent_block_id: "IB-U-NEWER", updated_at: "2026-09-28T00:00:00Z" });
  const main = mkBlock({
    intelligent_block_id: "IB-U-MAIN",
    updated_at: "2026-09-29T00:00:00Z",
    connections: [
      { target_block_id: "IB-U-NEWER", relationship_type: "SUPERSEDES" },
      { target_block_id: "IB-U-X", relationship_type: "MIND_CONTROLS" },
      { target_block_id: "IB-U-X", relationship_type: "SUPPORTZ" },
    ],
  });
  const x = mkBlock({ intelligent_block_id: "IB-U-X" });
  const out = selectKnowContext(reqA(), [main, newer, x]);

  // The valid edge still steers; the forged types contribute nothing.
  assert.equal(out.selected_block_id, "IB-U-NEWER");
  assert.match(out.reason, /SUPERSEDES_EDGE_FOLLOWED:IB-U-NEWER/);
  assert.ok(!out.related_context.some((e) => e.block_id === "IB-U-X"));
  assert.equal(out.conflict_detected, false);
});
