# Naya Power Handoff — Evidence Promotion Boundary

## Current canonical base
- Repository: `SoulSchoolAcademy/NayaPOWER`
- Main merge commit: `b7f535274b59dbc6ef5eb101b1eec5974b27ba4b`
- PR #37 verified head: `d5109097d3fec5ddebf75c3a6dd5ee43eab12448`

## Verified evidence
- Claim Evidence workflow: `32683644082` — success
- Oscar result: `ACCEPT`
- Oscar `promotion_allowed`: `true`
- Oscar expected commit: `d5109097d3fec5ddebf75c3a6dd5ee43eab12448`
- Artifact: `9504912190`
- Memory + Restore workflow: `32683643830` — success
- Governance workflow: `32683643758` — success

## Promotion boundary now enforced
`UNVERIFIED → BUILDER_VERIFIED → OSCAR_ACCEPTED → CANONICAL_VERIFIED → PRODUCTION_SAFE`

Eligibility requires:
`CLAIM + QUALIFYING EVIDENCE + BUILDER VERIFICATION + INDEPENDENT OSCAR ACCEPTANCE + CURRENT COMMIT`

Eligibility does **not** automatically become canonical. Canonical and production promotion require explicit promotion decisions. Production-safe additionally requires qualifying production evidence.

## Adversarial coverage
- builder verified / Oscar rejected
- stale evidence
- wrong commit
- superseded evidence
- missing provenance
- conflicting evidence
- production claim without production evidence
- historical verification mistaken for current verification
- verified state followed by repository change
- retrieved content influencing promotion
- eligible ≠ automatically canonical

## Current boundary
The exact PR head is verified. The resulting main commit still requires a fresh post-merge CI observation before current-main verification is claimed.

## Next execution directive
Inspect fresh post-merge CI bound to `b7f535274b59dbc6ef5eb101b1eec5974b27ba4b`. If green, record exact run/artifact provenance, set current-main verification to `VERIFIED_CI`, validate Smart Notes, Restore current/historical, Claim/Evidence, Oscar, promotion, governance, and then select the next highest-leverage capability from repository reality.
