# TEAM NAYA — 12 Project Intelligence Edge Functions

**Date:** 2026-09-21  
**Mission:** Make Project Intelligence executable through explicit, bounded runtime capabilities instead of leaving the 12 capabilities hidden inside one multiplexer.

## What was wrong

The previous implementation deployed the 12 capabilities inside a single `nayanet-compound-intelligence` Edge Function. That made the architecture exist in code, but it did **not** make 12 distinct Edge Functions appear in the Supabase dashboard. That was a real delivery failure.

## Repair

Deployed these 12 distinct Supabase Edge Functions to project `dahisasgpfvziswqvmvm`:

1. `nayanet-pi-restore`
2. `nayanet-pi-retrieve`
3. `nayanet-pi-reconcile`
4. `nayanet-pi-understand`
5. `nayanet-pi-learning-candidate`
6. `nayanet-pi-learning-verify`
7. `nayanet-pi-successor-handoff`
8. `nayanet-pi-share`
9. `nayanet-pi-supersede`
10. `nayanet-pi-health`
11. `nayanet-pi-dream`
12. `nayanet-pi-compound`

## Live registry verification

The Supabase registry was queried after deployment and returned **12/12 ACTIVE, version 1, verify_jwt=true**.

These are real deployed functions, not documentation-only entries.

## Bounded-authority rule

The PI can act without asking a human **only** inside the fixed operation boundary of the endpoint, using the authenticated user's runtime authority and existing policy checks. It cannot turn capability into authority, silently promote learning, publish without explicit consent, or bypass director-authority checks.

## What remains to prove

The next proof is behavioral, not architectural: invoke all 12 with an authenticated user session, capture the exact response, and verify the expected durable effect (or read-only result) for each. Deployment is complete; authenticated execution proof is the next verification boundary.

## Successor instruction

A cold Naya should first read `.naya/project-intelligence/PI-12-EDGE-FUNCTIONS.md`, then verify the live Supabase registry, then execute the authenticated 12-function behavioral proof before declaring the 12/12 runtime complete.