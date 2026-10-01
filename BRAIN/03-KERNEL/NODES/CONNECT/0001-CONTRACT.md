# CONNECT Node Contract V1

**ID:** NAYA-KERNEL-CONNECT

## Purpose

CONNECT turns isolated intelligence into relevant, situated intelligence. It resolves relationships, detects conflicts, and explains why retrieved intelligence applies to the current context.

## Inputs

- Intelligence objects and their relationships
- Retrieval queries (semantic, structural, relational, contextual)
- Current context and objective
- Contradiction and supersession rules

## Outputs

- Relevant intelligence set
- Relationship context (how objects connect)
- Applicability assessment (why this matters now)
- Freshness indicators
- Reconciliation context (conflicts, supersessions)

## MUST Rules

- Resolve typed relationships accurately.
- Retrieve by semantic, structural, relational and contextual relevance.
- Detect contradiction, supersession and dependency.
- Explain why retrieved intelligence applies.
- Maintain relationship provenance.
- Surface conflicts rather than resolving silently.

## MUST NOT Rules

- Treat relevance as authority.
- Create arbitrary relationships without provenance.
- Hide contradictions or supersessions.
- Serve stale intelligence without freshness marker.
- Infer relationships from co-occurrence alone.
- Allow relationship cycles without detection.

## Acceptance Criteria

- Retrieved intelligence is relevant to the current context.
- Relationships are typed and provenance-bound.
- Conflicts and supersessions are explicitly surfaced.
- Applicability is explained, not assumed.
- Freshness is indicated for all retrieved objects.
- Reconciliation context is complete.

## Failure States

| Failure | Behavior |
|---|---|
| Relationship type unknown | Mark as RELATED_TO; flag for classification |
| Contradiction detected | Surface both claims; do not choose |
| Supersession detected | Serve superseding object; mark superseded |
| Relevance cannot be established | Exclude from results; log reason |
| Provenance missing | Mark as UNVERIFIED; do not serve as canonical |

## Bounded runtime seam (proven, exact-revision)

The aspiration above is bounded by the one canonical executable seam on main.
CONNECT has exactly one canonical runtime seam; there is no second graph path.

**The seam (present on main):**

- `supabase/functions/nayanet-cold-runtime-proof/index.ts` — `mode === "graph-behavior"`
  (relationship-context treatment: graph ON → `APPLY_CONTEXTUALIZED_VERIFIED_INTELLIGENCE`)
  and `mode === "graph-verify"` (control/treatment receipt-pair verification)
- `.github/workflows/live-supabase-runtime-proof.yml` — invokes the seam
- `tests/verify_cold_graph_behavior.py` — behavioral verification of the seam

**Exact historical proof (exact-revision only):** acceptance run `36516790588`
(recorded in issue #1021) at commit `c9b31890c93f4f5f7d60bb8cd346093c11ab427f`
independently supported:

- graph OFF → `REQUIRE_DIRECT_CANONICAL_INTELLIGENCE`
- graph ON → `APPLY_CONTEXTUALIZED_VERIFIED_INTELLIGENCE`

with persisted OFF/ON receipts, VERIFIED provenance-bearing relationships, and
independent pair reread/recomputation. The proof is exact-revision only: it does
not transfer to other commits without a new acceptance run.

**NOT PROVEN (explicit limits — claiming any of these is an overclaim):**

- current-main production parity of this proof
- general multi-hop traversal
- cycle handling
- freshness semantics
- contradiction / supersession reconciliation
- generalized semantic / structural / relational retrieval
- universal CONNECT behavior

**Canonical-seam rule:** No new graph. No new persistence. No new authority.
No runtime behavior change. Any future CONNECT runtime work extends this seam
or records a new exact-revision proof; it does not create a parallel graph path.
