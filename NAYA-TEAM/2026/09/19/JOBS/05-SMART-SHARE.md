# JOB 05 — SMART SHARE
## Mission
Make sharing a controlled authorization boundary, not a cosmetic button.

## Current known state
`nayanet_intelligence_publications` currently has 0 rows. Smart Feed v1 exposes publish/revoke with owner checks.

## Job
Reconcile the existing publication/share primitive with the product Share surface.

## Build
- Determine and document the canonical Share path before adding anything.
- Preserve existing Hub visual design.
- Define exact share scope: owner, recipient/member, object/intelligence, permissions, lifetime/revocation where supported.
- Implement one real authorized share end-to-end.
- Enforce non-recipient denial and owner-only mutation.
- Verify protected content is not leaked through alternate retrieval paths.
- Implement revoke and prove it takes effect at use/read time.
- Preserve provenance and publication/receipt evidence.
- Do not create a second publication store.
- Prove Cloudflare parity.

## Acceptance
One authorized recipient can see exactly what was shared; an unauthorized user cannot. Revocation removes access without deleting the underlying source intelligence.

## Handoff
Update Share report/checklist/activity and coordinate with Feed, Mail, Spaces, and Smart Tabs.
