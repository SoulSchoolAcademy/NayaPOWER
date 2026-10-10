// held_out_evidence.test.ts — writer-side contract tests (Phase 3C).
//
// Run: node --experimental-strip-types --test \
//        supabase/functions/nayanet-learning-verify/held_out_evidence.test.ts
//
// These tests prove, without touching production:
//  1. the emitted marker block is well-formed per naya.held-out-evidence.v1,
//  2. the merge preserves existing observed_value keys (no clobbering),
//  3. overlap between evaluation refs and the support chain is detected and
//     flips held_out_from_support to false (fail-closed downstream),
//  4. the evaluator is the normalized verifier seat, never the runtime identity.

import { describe, it } from "node:test";
import assert from "node:assert/strict";
import {
  HELD_OUT_EVIDENCE_SCHEMA,
  HELD_OUT_EVIDENCE_KEY,
  HELD_OUT_RECORDED_BY,
  normalizeSeatIdentity,
  buildSupportArmIds,
  buildHeldOutEvidence,
  mergeHeldOutEvidence,
} from "./held_out_evidence.ts";

const OBSERVED = {
  intelligent_block_id: "IB-aaa111",
  source_event_id: "EVT-1",
  lineage_id: "LIN-222",
  relationship_id: "REL-333",
  index_id: "IDX-444",
  checkpoint_id: "CHK-555",
  provenance_preserved: true,
  custom_note: "must survive the merge",
};

const BASE_INPUT = {
  learningId: "d4fc8e73-a6de-587e-b47e-0de69c2a925f",
  observed: OBSERVED,
  evidenceRefs: ["CVO-NAYA-NODE-0001-FRESH-LEARNING-2026-10-10"],
  verifierSeat: "Naya-5",
  queueEntryId: "VQ-d4fc8e73",
  nowIso: "2026-10-10T19:40:00.000Z",
};

describe("schema identity", () => {
  it("uses the exact v1 schema string the reader expects", () => {
    assert.equal(HELD_OUT_EVIDENCE_SCHEMA, "naya.held-out-evidence.v1");
    assert.equal(HELD_OUT_EVIDENCE_KEY, "held_out_evidence");
  });
});

describe("normalizeSeatIdentity (mirrors tools/learning_admission_gate.normalize_identity)", () => {
  it("treats Naya-5, naya-5 and NAYA-5 as one seat", () => {
    assert.equal(normalizeSeatIdentity("Naya-5"), normalizeSeatIdentity("naya-5 "));
    assert.equal(normalizeSeatIdentity("NAYA-5"), normalizeSeatIdentity("naya-5"));
  });
  it("empty/blank input normalizes to empty (reader fails closed on it)", () => {
    assert.equal(normalizeSeatIdentity("   "), "");
    assert.equal(normalizeSeatIdentity(null), "");
  });
});

describe("buildSupportArmIds (deterministic arm mapping)", () => {
  it("derives the five prefixed provenance-chain IDs", () => {
    assert.deepEqual(buildSupportArmIds(OBSERVED), [
      "intelligent_block:IB-aaa111",
      "lineage:LIN-222",
      "relationship:REL-333",
      "index:IDX-444",
      "checkpoint:CHK-555",
    ]);
  });
  it("drops missing links rather than emitting empty arms", () => {
    assert.deepEqual(buildSupportArmIds({ intelligent_block_id: "IB-x" }), ["intelligent_block:IB-x"]);
  });
});

describe("buildHeldOutEvidence (v1 well-formedness)", () => {
  it("emits every required top-level field with correct types", () => {
    const m = buildHeldOutEvidence(BASE_INPUT) as Record<string, any>;
    assert.equal(m.schema, "naya.held-out-evidence.v1");
    assert.equal(m.recorded_at, "2026-10-10T19:40:00.000Z");
    assert.equal(typeof m.recorded_by, "string");
    assert.ok(Array.isArray(m.evidence_families) && m.evidence_families.length === 2);
    const hoe = m.held_out_evaluation;
    for (const k of ["evaluation_id", "evaluator", "evaluator_role", "verdict", "measured_at",
                     "support_arm_ids", "evaluation_arm_ids", "overlap_with_support", "held_out_from_support"]) {
      assert.ok(k in hoe, `missing held_out_evaluation.${k}`);
    }
    assert.ok(["UNAFFECTED", "REQUALIFIED", "DOWNGRADED", "INSUFFICIENT_DATA", "SUSPENDED", "REVOKED"].includes(m.revocation_verdict));
    assert.ok(["independently_cleared", "unassessed", "possibly_compromised", "confirmed_compromised"].includes(m.uncertainty_assessment));
    assert.equal(m.incident_id, null);
  });

  it("records the evaluator as the normalized verifier seat, not the runtime identity", () => {
    const m = buildHeldOutEvidence({ ...BASE_INPUT, verifierSeat: "  NAYA-5 " }) as Record<string, any>;
    assert.equal(m.held_out_evaluation.evaluator, "naya-5");
    assert.equal(m.held_out_evaluation.evaluator_role, "verifier");
    assert.equal(m.recorded_by, HELD_OUT_RECORDED_BY);
    assert.notEqual(m.held_out_evaluation.evaluator, "github-actions-oidc");
    assert.notEqual(m.recorded_by, m.held_out_evaluation.evaluator);
  });

  it("records the queue audit link when supplied, null when absent (never invented)", () => {
    const withLink = buildHeldOutEvidence(BASE_INPUT) as Record<string, any>;
    assert.equal(withLink.queue_entry_id, "VQ-d4fc8e73");
    const withoutLink = buildHeldOutEvidence({ ...BASE_INPUT, queueEntryId: null }) as Record<string, any>;
    assert.equal(withoutLink.queue_entry_id, null);
  });

  it("marks CVO evaluation refs as held out from the support chain", () => {
    const m = buildHeldOutEvidence(BASE_INPUT) as Record<string, any>;
    const hoe = m.held_out_evaluation;
    assert.equal(hoe.overlap_with_support, false);
    assert.equal(hoe.held_out_from_support, true);
    assert.deepEqual(hoe.evaluation_arm_ids, ["CVO-NAYA-NODE-0001-FRESH-LEARNING-2026-10-10"]);
    const vf = (m.evidence_families as any[]).find((f) => f.family_id === "verification-evidence");
    assert.equal(vf.independent_of_lesson, true);
  });

  it("detects a ref that names a support-chain ID (case-insensitive) and fails the held-out claim", () => {
    const m = buildHeldOutEvidence({
      ...BASE_INPUT,
      evidenceRefs: ["INTELLIGENT_BLOCK:ib-aaa111"], // same ID, different case/prefix style
    }) as Record<string, any>;
    const hoe = m.held_out_evaluation;
    assert.equal(hoe.overlap_with_support, true);
    assert.equal(hoe.held_out_from_support, false);
    const vf = (m.evidence_families as any[]).find((f) => f.family_id === "verification-evidence");
    assert.equal(vf.independent_of_lesson, false);
  });

  it("the lesson-support-chain family is never marked independent of the lesson", () => {
    const m = buildHeldOutEvidence(BASE_INPUT) as Record<string, any>;
    const sf = (m.evidence_families as any[]).find((f) => f.family_id === "lesson-support-chain");
    assert.equal(sf.independent_of_lesson, false);
  });

  it("evaluation_id is deterministic per learning", () => {
    const a = buildHeldOutEvidence(BASE_INPUT) as Record<string, any>;
    const b = buildHeldOutEvidence(BASE_INPUT) as Record<string, any>;
    assert.equal(a.held_out_evaluation.evaluation_id, b.held_out_evaluation.evaluation_id);
    assert.ok(String(a.held_out_evaluation.evaluation_id).startsWith("HO-"));
  });
});

describe("mergeHeldOutEvidence (no clobbering)", () => {
  it("preserves every existing observed_value key and adds held_out_evidence", () => {
    const marker = buildHeldOutEvidence(BASE_INPUT);
    const merged = mergeHeldOutEvidence(OBSERVED, marker);
    for (const k of Object.keys(OBSERVED)) {
      assert.deepEqual(merged[k], (OBSERVED as Record<string, any>)[k], `clobbered key: ${k}`);
    }
    assert.deepEqual(merged[HELD_OUT_EVIDENCE_KEY], marker);
  });

  it("starts from {} when observed_value is null or not an object (the COALESCE equivalent)", () => {
    const marker = buildHeldOutEvidence(BASE_INPUT);
    assert.deepEqual(mergeHeldOutEvidence(null, marker), { [HELD_OUT_EVIDENCE_KEY]: marker });
    assert.deepEqual(mergeHeldOutEvidence("junk", marker), { [HELD_OUT_EVIDENCE_KEY]: marker });
    assert.deepEqual(mergeHeldOutEvidence([1, 2], marker), { [HELD_OUT_EVIDENCE_KEY]: marker });
  });

  it("re-promotion replaces the block instead of nesting it", () => {
    const first = mergeHeldOutEvidence(OBSERVED, buildHeldOutEvidence(BASE_INPUT));
    const second = buildHeldOutEvidence({ ...BASE_INPUT, nowIso: "2026-10-10T20:00:00.000Z" });
    const repromoted = mergeHeldOutEvidence(first, second);
    assert.equal((repromoted[HELD_OUT_EVIDENCE_KEY] as Record<string, any>).recorded_at, "2026-10-10T20:00:00.000Z");
    assert.ok(!(HELD_OUT_EVIDENCE_KEY in ((repromoted[HELD_OUT_EVIDENCE_KEY] as Record<string, any>))));
    assert.equal(repromoted["custom_note"], "must survive the merge");
  });

  it("does not mutate the input observed object", () => {
    const before = JSON.stringify(OBSERVED);
    mergeHeldOutEvidence(OBSERVED, buildHeldOutEvidence(BASE_INPUT));
    assert.equal(JSON.stringify(OBSERVED), before);
  });
});
