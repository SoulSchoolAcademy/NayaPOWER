// WO4 — verified-lesson → decision seam: decision-context query for the ACT runtime.
//
// The standalone `naya-decision-context` edge function is user-scoped (it reads
// the caller from the Authorization header) and currently has zero callers.
// The ACT runtime cannot call it over HTTP — it authenticates as the owner via
// a workflow OIDC identity, not as a user — so this module ports the endpoint's
// exact query and its repaired semantics (PR #1733: context AVAILABILITY is
// reported; causal INFLUENCE is never claimed here) into an owner-scoped helper
// the plan handler can invoke directly.
//
// Semantics (must stay in lockstep with naya-decision-context/index.ts):
//   - learning_context_available: an ACTIVE learning_evidence row exists for the target.
//   - influenced: ALWAYS false at this layer. Availability is not proof of
//     influence. Causal influence is measured by the caller's controlled
//     intervention (control plan vs treatment plan) — see measureLearningInfluence
//     in act.ts — never by the mere presence of a lesson.
//   - authority: reading learning context never changes or grants authority.
// A database failure throws: planning must fail closed rather than silently
// plan as if no verified learning existed.

export type DecisionContext = {
  decision: "LEARNING_CONTEXT_AVAILABLE" | "NO_VERIFIED_LEARNING_CONTEXT";
  target_id: string;
  learning_context_available: boolean;
  influenced: false;
  reason: string;
  context: {
    evidence_id: string | null;
    level: string | null;
    claim: string | null;
    source_event_id: string | null;
    observed_value: unknown;
    verification_method: string | null;
    provenance: unknown;
  };
  authority: { changed: false; granted: false; source: string };
  verification: { evidence_status: string | null };
  continuity: { grounded: false; source: string; next_step: string };
};

type EvidenceRow = {
  id?: string | null;
  target_id?: string | null;
  level?: string | null;
  status?: string | null;
  claim?: string | null;
  observed_value?: unknown;
  source_event_id?: string | null;
  verification_method?: string | null;
  provenance?: unknown;
};

export async function readDecisionContext(
  admin: { from: (table: string) => any },
  memberId: string,
  targetId: string,
): Promise<DecisionContext> {
  const target = String(targetId ?? "").trim();
  if (!target) throw new Error("DECISION_CONTEXT_TARGET_REQUIRED");
  const { data: evidence, error } = await admin
    .from("learning_evidence")
    .select("id,target_id,level,status,claim,observed_value,source_event_id,verification_method,provenance,created_at")
    .eq("member_id", memberId)
    .eq("target_id", target)
    .eq("status", "ACTIVE")
    .order("created_at", { ascending: false })
    .limit(1)
    .maybeSingle();
  if (error) throw error;
  // maybeSingle() returns one row or null; normalize defensively so an
  // out-of-contract array can never read as "context available".
  const row = (Array.isArray(evidence) ? evidence[0] ?? null : evidence ?? null) as EvidenceRow | null;
  const available = !!row;
  return {
    decision: available ? "LEARNING_CONTEXT_AVAILABLE" : "NO_VERIFIED_LEARNING_CONTEXT",
    target_id: target,
    learning_context_available: available,
    influenced: false,
    reason: available
      ? "Verified learning context is available in the canonical learner evidence boundary; causal influence is not established by availability alone."
      : "No active learning evidence was found for this target.",
    context: {
      evidence_id: row?.id ?? null,
      level: row?.level ?? null,
      claim: row?.claim ?? null,
      source_event_id: row?.source_event_id ?? null,
      observed_value: row?.observed_value ?? null,
      verification_method: row?.verification_method ?? null,
      provenance: row?.provenance ?? null,
    },
    authority: { changed: false, granted: false, source: "existing governance boundary" },
    verification: { evidence_status: row?.status ?? null },
    continuity: {
      grounded: false,
      source: available ? "learning_evidence" : "no_learning_evidence",
      next_step: available
        ? "EVALUATE_LEARNING_APPLICABILITY_BEFORE_APPLY"
        : "RETRIEVE_VERIFIED_LEARNING_BEFORE_CONTINUATION",
    },
  };
}
