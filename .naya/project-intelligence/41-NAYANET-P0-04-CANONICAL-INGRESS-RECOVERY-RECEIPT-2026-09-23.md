# NayaNET P0-04 Canonical Ingress Recovery Receipt — 2026-09-23

## Result

**P0-04 VERIFIED** at source head `fe8af3d71082b00443e8e1e213ecb46e7427825e`.

Workflow run: `35915882471`
Job: `107372505645`
Artifact: `p0-04-meaningful-output-proof`
Artifact ID: `10776170794`

## Bounded proof

The fresh run established:

`START → IDENTITY → AUTHORITY → intelligence_commit → PROVENANCE/VALIDATION/INTEGRATION/CHECKPOINT → INTELLIGENT_BLOCK → FRESH_RETRIEVAL`

Owner: `e20bb8e8-2a3b-4795-b227-987aa7c07abe`

Event: `intelligence:p0-04-p00435915882471-ab5af0f150`

Checkpoint: `checkpoint:p0-04-p00435915882471-ab5af0f150`

Learning evidence: `ee6bada4-841b-4c57-af15-cd56681f9cfb`

Intelligence index: `671b6159-2b13-4494-8f42-289d39d44cd8`

Intelligent Block: `da3e2ae1-6369-595d-96ba-2f923488105b`

Privacy: `PRIVATE_OWNER_SCOPE`

## Causal finding

The prior reported canonical-ingress `TypeError: Failed to fetch` did **not** reproduce on the fresh rerun.

Supabase evidence shows deployment/runtime churn at the same boundary: function versions 29 and 30 returned 503s during the affected window, while the stabilized version 31 subsequently returned successful authenticated POSTs. The successful P0-04 rerun executed against the same repository source head and reached canonical ingress and all downstream proof stages.

Therefore **no additional source-code repair was justified by the evidence in this execution**. Making an arbitrary code change merely to satisfy a “one repair” requirement would violate the causal-repair rule.

The effective recovery was restoration of a healthy deployed runtime; current production deployment is `nayanet-compound-intelligence v31`.

## Learning boundary

Verified-learning remains proven by workflow run `35915387903`, including later decision influence and cold reuse. This P0-04 run separately proves the canonical promotion path through Intelligent Block and fresh retrieval.

This does **not** prove universal automatic promotion from every meaningful Naya output.

## Scope decision

P0-04 is now green at the bounded acceptance target.

Do not mutate or “dispose” any legacy cognition-event cohort yet. The previously cited 88-event scope has not been re-derived from canonical lineage evidence.

## Next frontier

Advance to Priority #2 only after recording this receipt and refreshing the control-plane baton:

**Derive the exact legacy cognition-event disposition cohort from canonical lineage/schema evidence, without deleting or fabricating backfill.**

