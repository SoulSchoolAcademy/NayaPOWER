// CONNECT SELECTOR — edge admissibility gate for retrieval.
// ============================================================================
// OWNER: NAYA-KERNEL-CONNECT (BRAIN/03-KERNEL/0004-NINE-NODE-ORGANISM-CONTRACT-V1.json
//   nodes.CONNECT owns: relationships, retrieval, reconciliation, context,
//   applicability).
// CONTRACT: NAYANODE/AI-CONNECT-CONTRACT-V2.md — required functions
//   validate_edge, resolve_relationship, assess_applicability.
// CONSUMER: supabase/functions/nayanet-know-runtime/know.ts imports the gate;
//   KNOW owns block eligibility and request authority, CONNECT owns edge
//   admissibility. Retrieval never creates authority (see contract).
// CHANGE RULE: logic here is CONNECT's responsibility. Moved verbatim from
//   nayanet-know-runtime/know.ts (2026-10-07) — pure relocation, zero behavior
//   change. Any behavior change must update the Deno behavior matrix that
//   covers v2EdgeExclusionReason + selectableConnections.
// ============================================================================

// Minimal structural view of a block the selector reads. The selector touches
// only the edge projection; IntelligentBlock (know.ts) satisfies this
// structurally, so no import cycle is needed.
export type EdgeProjection = {
  target_block_id?: string | null;
  relationship_type?: string | null;
  relationship_id?: string | null;
  supersedes_relationship_id?: string | null;
  status?: string | null;
  epistemic_state?: string | null;
  valid_from?: string | null;
  valid_until?: string | null;
  visibility?: string | null;
  consent_ref?: string | null;
  applicability?: { state?: string | null; task_classes?: unknown; limitations?: unknown } | null;
};

export type EdgeCarrier = {
  connections?: EdgeProjection[] | null;
};


// Canonical relationship vocabulary, mirrored from
// BRAIN/00-SPEC/BRAIN-MACHINE-CONTRACT-V1.schema.json $defs.relationshipType.
// An edge whose type is not in this vocabulary is forged for retrieval
// purposes and can never steer selection or context.
export const EDGE_VOCABULARY=new Set([
  "DERIVED_FROM","SUPPORTS","CONTRADICTS","DEPENDS_ON","IMPLEMENTS","GOVERNS",
  "AUTHORIZED_BY","USED_BY","CAUSED","RESULTED_IN","VERIFIED_BY","LEARNED_FROM",
  "SUPERSEDES","SUCCEEDS","RELATED_TO","CONTEXTUALIZES","INVALIDATES","REFINES",
  "CORRECTS","ENABLES","PRODUCES","APPLIES_TO"
]);

// A connection parsed and normalized for selector evaluation. V2 fields are
// normalized defensively: the DB check constraints hold the canonical rows,
// but the projection is writer-supplied JSON — malformed values fail closed
// in the gate below rather than throwing here.
export type ParsedBlockConnection = {
  target_block_id: string;
  relationship_type: string;
  relationship_id: string | null;
  supersedes_relationship_id: string | null;
  status: string | null;
  epistemic_state: string | null;
  valid_from: string | null;
  valid_until: string | null;
  visibility: string | null;
  consent_ref: string | null;
  applicability_state: string | null; // APPLICABLE | NOT_APPLICABLE | UNKNOWN | null
};

function normUpper(value: unknown): string | null {
  const s = String(value ?? "").trim();
  return s ? s.toUpperCase() : null;
}

function normText(value: unknown): string | null {
  const s = String(value ?? "").trim();
  return s ? s : null;
}

export function parsedTime(value:unknown):number|null{
  if(value===null||value===undefined||value==="") return null;
  const t=Date.parse(String(value));
  return Number.isFinite(t)?t:NaN;
}

function blockConnections(block: EdgeCarrier): ParsedBlockConnection[] {
  const raw = block.connections;
  if (!Array.isArray(raw)) return [];
  const out: ParsedBlockConnection[] = [];
  for (const c of raw) {
    const target = String((c as any)?.target_block_id ?? "").trim();
    const rel = String((c as any)?.relationship_type ?? "").trim().toUpperCase();
    if (!target) continue;
    if (!EDGE_VOCABULARY.has(rel)) continue;
    const applicability = (c as any)?.applicability;
    out.push({
      target_block_id: target,
      relationship_type: rel,
      relationship_id: normText((c as any)?.relationship_id),
      supersedes_relationship_id: normText((c as any)?.supersedes_relationship_id),
      status: normUpper((c as any)?.status),
      epistemic_state: normUpper((c as any)?.epistemic_state),
      valid_from: normText((c as any)?.valid_from),
      valid_until: normText((c as any)?.valid_until),
      visibility: normUpper((c as any)?.visibility),
      consent_ref: normText((c as any)?.consent_ref),
      applicability_state: normUpper(
        applicability !== null && typeof applicability === "object"
          ? (applicability as any)?.state
          : null
      ),
    });
  }
  return out;
}

// ---------------------------------------------------------------------------
// Graph V2 selector gates (contract 0003 — RATIFIED_CONTRACT.
// ratification). An edge carrying no V2 fields is a legacy two-field
// projection and passes every gate: flat pre-V2 behavior is preserved
// byte-for-byte. An edge carrying V2 fields is held to V2 semantics:
//   - superseded / revoked / invalidated edges never influence retrieval
//     (V2 historical_truth_rule: expired or superseded relationships must
//     not be returned as current);
//   - not-yet-valid and expired edges never influence behavior
//     (V2 temporal_contract: null valid_until means open-ended);
//   - non-PRIVATE visibility requires an explicit consent_ref. Current
//     participation state is not a retroactive read gate for already accepted
//     identity-safe derived intelligence. Collective participation/revocation semantics
//     are governed separately; this selector must not infer constitutional ratification.
//   - NOT_APPLICABLE edges never influence retrieval; UNKNOWN stays UNKNOWN
//     (V2 applicability_contract: retrieval does not imply applicability).
// Malformed V2 values fail closed. No gate creates authority: admission is
// not authorization, and AUTHORIZED_BY edges are never treated as current
// authorization (see authority_boundary in the contract).
// ---------------------------------------------------------------------------

export const V2_ALLOWED_STATUS = new Set(["ACTIVE", "REVOKED", "SUPERSEDED", "INVALIDATED"]);
export const V2_TERMINAL_STATUS = new Set(["SUPERSEDED", "REVOKED", "INVALIDATED"]);
export const V2_TERMINAL_EPISTEMIC = new Set(["SUPERSEDED", "INVALIDATED"]);
export const V2_ALLOWED_VISIBILITY = new Set(["PRIVATE", "DERIVED_SHARED", "PUBLIC_DERIVED"]);

// Returns null when the edge is admissible for retrieval; otherwise the
// machine reason code for its exclusion. Pure: no I/O, no clock — nowMs is
// injected so delayed-inspect and stale-edge behavior stay recomputable.
export function v2EdgeExclusionReason(
  conn: ParsedBlockConnection,
  supersededIds: Set<string>,
  nowMs: number
): string | null {
  // Supersession.
  if (conn.status !== null && !V2_ALLOWED_STATUS.has(conn.status)) return "EDGE_STATUS_UNKNOWN";
  if (conn.status !== null && V2_TERMINAL_STATUS.has(conn.status)) return `EDGE_STATUS_${conn.status}`;
  if (conn.epistemic_state !== null && V2_TERMINAL_EPISTEMIC.has(conn.epistemic_state))
    return `EDGE_EPISTEMIC_${conn.epistemic_state}`;
  if (conn.relationship_id !== null && supersededIds.has(conn.relationship_id))
    return "EDGE_SUPERSEDED_BY_NEWER_EDGE";
  // Temporal window. Validity is boundary-inclusive: an edge is live on
  // [valid_from, valid_until]; unparseable-but-present is corrupt → closed.
  if (conn.valid_from !== null) {
    const from = parsedTime(conn.valid_from);
    if (from === null || Number.isNaN(from)) return "EDGE_TEMPORAL_INVALID";
    if (from > nowMs) return "EDGE_NOT_YET_VALID";
  }
  if (conn.valid_until !== null) {
    const until = parsedTime(conn.valid_until);
    if (until === null || Number.isNaN(until)) return "EDGE_TEMPORAL_INVALID";
    if (until < nowMs) return "EDGE_EXPIRED";
  }
  // Consent. Absent visibility defaults to PRIVATE (V2 migration default);
  // the block-level owner check in isEligibleBlock already confines PRIVATE
  // edges to the requesting owner.
  if (conn.visibility !== null && !V2_ALLOWED_VISIBILITY.has(conn.visibility)) return "EDGE_VISIBILITY_UNKNOWN";
  if (conn.visibility !== null && conn.visibility !== "PRIVATE" && conn.consent_ref === null)
    return "EDGE_CROSS_OWNER_CONSENT_REQUIRED";
  // Applicability tristate. Only NOT_APPLICABLE excludes; UNKNOWN is
  // admitted without being promoted — retrieval does not imply applicability.
  if (conn.applicability_state === "NOT_APPLICABLE") return "EDGE_NOT_APPLICABLE";
  return null;
}

// The V2-gated edge set for one block's projection: parsed, then filtered
// through the V2 selector gates with within-projection supersession
// resolution (an edge naming supersedes_relationship_id marks the named edge
// superseded — provenance is never deleted, only excluded from retrieval).
// Every consumer of edges — supersession chase and related context — reads
// through this gate.
export function selectableConnections(block: EdgeCarrier, nowMs: number): ParsedBlockConnection[] {
  const parsed = blockConnections(block);
  const supersededIds = new Set<string>();
  for (const c of parsed) if (c.supersedes_relationship_id) supersededIds.add(c.supersedes_relationship_id);
  return parsed.filter((c) => v2EdgeExclusionReason(c, supersededIds, nowMs) === null);
}
