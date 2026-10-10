// held_out_evidence.ts — held-out evidence marker emission (writer side).
//
// Phase 3C (2026-10-10, Shawn's word "Word!"): at learning promotion, the
// verify edge function merges a `held_out_evidence` block into
// learning_evidence.observed_value, per the v1 contract specified in
// kernel/db_evidence_eligibility.py (Phase 3B, reader/gate side).
//
// This module is PURE: no Deno, no Supabase, no network. It is imported by
// index.ts and unit-tested with node --experimental-strip-types.
//
// ---------------------------------------------------------------------------
// OPEN QUESTION 1 — arm-id mapping (resolved by team, deterministic):
// The verify function works from Intelligent Blocks, not admission arms, so
// "arms" here are evidence references, mapped as follows:
//   support_arm_ids    = the lesson's own supporting evidence: the provenance
//                        chain IDs recorded at capture, prefixed by type
//                        (intelligent_block:<id>, lineage:<id>,
//                         relationship:<id>, index:<id>, checkpoint:<id>).
//   evaluation_arm_ids = the evidence the verification actually examined:
//                        body.evidence_refs (already validated upstream:
//                        non-empty, at least one CVO- ref, no junk).
//   overlap_with_support = case-insensitive intersection of the two sets.
//   held_out_from_support = !overlap && evaluation_arm_ids.length > 0.
// A ref that names a support-chain ID is caught by the overlap check and the
// reader then refuses the row (INELIGIBLE_UNCERTAIN) — fail closed.
//
// OPEN QUESTION 2 — evaluator identity (resolved by team):
// The marker's `evaluator` MUST be the queue's claim() verifier seat, never
// the github-actions-oidc runtime identity. Mechanism implemented here:
// the caller passes body.verifier_seat (required; 400 VERIFIER_SEAT_REQUIRED
// if empty); it is normalized (trim + casefold, mirroring
// tools/learning_admission_gate.normalize_identity) and recorded as
// `evaluator` with evaluator_role "verifier". `recorded_by` separately names
// the emitting service ("nayanet-learning-verify") so the receipt
// distinguishes WHO evaluated from WHAT SERVICE wrote the markers.
//   Trust boundary (honest limitation): the edge function runs in Supabase
//   and cannot read the repo-local queue.json, so the asserted seat is
//   trusted via the OIDC workflow binding (only the main-branch workflow
//   can invoke) plus the LAW authority gate that already guards promotion.
// PARKED HARDENING (needs Shawn's word — schema change, not implemented):
//   mirror queue claims into a Supabase table `nayanet_verification_claims`
//   (learning_id, queue_entry_id, verifier_seat, claimed_at) written by the
//   queue-claim step through an authorized path; the edge function then
//   joins learning_id -> claim and rejects a mismatched verifier_seat with
//   409 VERIFIER_SEAT_MISMATCH instead of trusting the assertion.
// ---------------------------------------------------------------------------

export const HELD_OUT_EVIDENCE_SCHEMA = "naya.held-out-evidence.v1";
export const HELD_OUT_EVIDENCE_KEY = "held_out_evidence";
export const HELD_OUT_RECORDED_BY = "nayanet-learning-verify";

// Mirrors tools/learning_admission_gate.normalize_identity:
// "Naya-5", "naya-5 " and "NAYA-5" are one seat.
export function normalizeSeatIdentity(value: unknown): string {
  return String(value ?? "").trim().toLowerCase();
}

export interface HeldOutEvidenceInput {
  learningId: string;
  observed: Record<string, unknown>;
  evidenceRefs: unknown[];
  verifierSeat: string;
  queueEntryId: string | null;
  nowIso: string;
}

// The lesson's own supporting evidence, deterministically derived from the
// provenance chain recorded at capture. All five links are required upstream
// (LEARNING_PROVENANCE_LINKS_REQUIRED, 409) so they are present here.
export function buildSupportArmIds(observed: Record<string, unknown>): string[] {
  const pairs: Array<[string, unknown]> = [
    ["intelligent_block", observed["intelligent_block_id"]],
    ["lineage", observed["lineage_id"]],
    ["relationship", observed["relationship_id"]],
    ["index", observed["index_id"]],
    ["checkpoint", observed["checkpoint_id"]],
  ];
  const ids: string[] = [];
  for (const [kind, raw] of pairs) {
    const id = String(raw ?? "").trim();
    if (id) ids.push(`${kind}:${id}`);
  }
  return ids;
}

export function buildHeldOutEvidence(input: HeldOutEvidenceInput): Record<string, unknown> {
  const { learningId, observed, evidenceRefs, verifierSeat, queueEntryId, nowIso } = input;
  const supportArmIds = buildSupportArmIds(observed);
  const evaluationArmIds = (Array.isArray(evidenceRefs) ? evidenceRefs : []).map((r) => String(r ?? "").trim()).filter((s) => s.length > 0);
  const supportSet = new Set(supportArmIds.map((s) => s.toLowerCase()));
  const overlapWithSupport = evaluationArmIds.some((a) => supportSet.has(a.toLowerCase()));
  const heldOutFromSupport = !overlapWithSupport && evaluationArmIds.length > 0;
  const evaluator = normalizeSeatIdentity(verifierSeat);

  return {
    schema: HELD_OUT_EVIDENCE_SCHEMA,
    recorded_at: nowIso,
    recorded_by: HELD_OUT_RECORDED_BY,
    // The queue-claim audit link, when the caller supplies it. Null is
    // honest: absence of the link is recorded, never invented.
    queue_entry_id: queueEntryId && queueEntryId.trim() ? queueEntryId.trim() : null,
    evidence_families: [
      {
        family_id: "lesson-support-chain",
        independent_of_lesson: false,
        basis: "provenance chain recorded at capture: intelligent block, lineage, relationship, index, checkpoint",
      },
      {
        family_id: "verification-evidence",
        independent_of_lesson: !overlapWithSupport,
        basis: "evidence_refs examined by this verification run",
      },
    ],
    held_out_evaluation: {
      evaluation_id: `HO-${String(learningId).slice(0, 8)}`,
      evaluator,
      evaluator_role: "verifier",
      verdict: "VERIFIED",
      measured_at: nowIso,
      support_arm_ids: supportArmIds,
      evaluation_arm_ids: evaluationArmIds,
      overlap_with_support: overlapWithSupport,
      held_out_from_support: heldOutFromSupport,
    },
    // No incident is on record at promotion: the verification just passed.
    // Reader semantics: unassessed + null incident = eligible (not
    // "unassessed under an incident"). Emitting these explicitly keeps the
    // block well-formed so the reader never fails closed on a missing key.
    revocation_verdict: "UNAFFECTED",
    uncertainty_assessment: "unassessed",
    incident_id: null,
  };
}

// Top-level merge into observed_value: the exact equivalent of
//   COALESCE(observed_value,'{}') || jsonb_build_object('held_out_evidence', <markers>)
// Existing keys are preserved; only the held_out_evidence key is (re)written.
// Re-promotion therefore replaces a stale block instead of nesting one.
export function mergeHeldOutEvidence(
  observed: unknown,
  marker: Record<string, unknown>,
): Record<string, unknown> {
  const base = observed && typeof observed === "object" && !Array.isArray(observed)
    ? (observed as Record<string, unknown>)
    : {};
  return { ...base, [HELD_OUT_EVIDENCE_KEY]: marker };
}
