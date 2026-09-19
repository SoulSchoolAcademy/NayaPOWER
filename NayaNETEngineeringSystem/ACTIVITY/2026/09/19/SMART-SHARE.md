# SMART SHARE — MASTER NAYA READINESS REVIEW — 2026-09-19

**Role:** Smart Share owner  
**Mission:** Make explicit consented sharing a real, reversible, provenance-preserving product capability.

## Executive state

**Current product readiness: 2.7 / 10 — specification is strong; runtime/product path is not proven.**

Fresh runtime evidence includes `nayanet_intelligence_publications` with **0 rows**. The new `naya-smart-feed` function contains publish/revoke logic with explicit consent and owner checks, which is a useful primitive, but this is not yet proof of a complete Smart Share product.

## Readiness matrix

| Dimension | Rating |
|---|---:|
| Specification | 9.5/10 |
| Requirements completeness | 9/10 |
| Today's execution plan | 9/10 |
| Engine/backend | 3/10 |
| Interface/design | 7/10 |
| Product integration | 2/10 |
| Security/privacy | 4/10 |
| Runtime/deployment | 3/10 |
| Ship readiness | 2.7/10 |

## Core role

Share must answer:

**WHAT? WITH WHOM? AT WHAT SCOPE? WHAT WILL THEY SEE?**

It is not the same thing as Mail, Space membership, or collective publication.

## What is real

- Strong privacy/publication contract.
- `nayanet_intelligence_publications` exists with RLS.
- Smart Feed v1 contains explicit publish/revoke paths with owner checks.
- Consent state is explicitly represented.

## Critical gaps

1. No real publication rows yet.
2. No proven Smart Share UI.
3. No proven recipient/scope preview.
4. No non-recipient denial proof.
5. No protected-content leakage proof.
6. Revocation behavior not proven end-to-end.
7. No complete receipt/provenance proof.
8. Cloudflare source/build/runtime parity not proven.

## Complete today

1. Map all existing share/publication primitives.
2. Decide whether Smart Feed publish is the canonical publication path or merely an adapter.
3. Build the smallest Share UI using existing Hub design.
4. Share one private item to one authorized recipient/scope.
5. Verify exact scope.
6. Attempt non-recipient access and prove denial.
7. Test protected list/space leakage.
8. Revoke if supported and prove post-revoke behavior.
9. Capture provenance/receipt.
10. Verify deployed parity.

## Definition of COMPLETE

A human explicitly chooses an object and audience → previews exact scope → confirms → canonical publication/share record is created → recipient sees exactly what is authorized → non-recipient is denied → protected context does not leak → revoke behaves correctly → receipt/provenance is retrievable.

**NEXT:** Reconcile Smart Feed publication with the Smart Share contract, then execute one authorized share and one denial before adding any new storage.
