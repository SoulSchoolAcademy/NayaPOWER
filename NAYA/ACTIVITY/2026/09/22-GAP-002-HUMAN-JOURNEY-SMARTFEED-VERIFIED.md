# 2026-09-22 — GAP-002 + HUMAN JOURNEY + SMART FEED API VERIFIED

STATUS: VERIFIED

## Current source
- main: ea5cd50b0e0bedf93d25fe30eeb4efba24f1d900
- Live browser acceptance: run 35781191036
- Artifact: 10717912938
- Artifact SHA-256: d1df4b7fc11fb4af621eb5e5eef7ce79fe5505a8644f32bd6f23c145b18a34fc

## GAP-002
SMART NOTE -> INTELLIGENT BLOCK -> INDEX -> SMART FEED -> RELOAD -> EVIDENCE -> CONTINUE is VERIFIED.

## Human journey
OPEN -> UNDERSTAND -> NAVIGATE -> SEARCH -> CREATE -> SAVE -> SEE RESULT -> RELOAD -> FIND -> UNDERSTAND EVIDENCE -> CONTINUE

## Fresh proof
- Event: 3ffe7940-1571-4918-b4e1-10f0681e42d1
- Receipt: 1b46f984-cf9f-4226-b840-5e98745c6947
- Fresh audit user: 9427c556-39c5-40c7-94de-192820697bc2
- Hub title: NayaNET — Intelligent Hub V7 · 509 AAA
- Navigation surfaces: 26
- Search: PASS
- Smart Feed API response: HTTP 200
- Smart Feed API Intelligent Block projection: PASS
- Smart Feed DOM projection: PASS
- Reload identity: PASS
- Same event identity: PASS
- Console errors: 0

## Causal repairs made
1. Smart Feed browser CORS/auth boundary hardened.
2. Supabase function moved to explicit in-function Bearer authentication with verify_jwt=false so browser preflight reaches the canonical OPTIONS handler.
3. Assistant runtime Smart Feed reads now use the established Supabase client.
4. Hub runtime cache key advanced to 20260922-smartfeed-client-fix1.
5. Smart Feed block lookup reconciled to canonical block identity and inline canonical Intelligent Block fallback.
6. Browser harness now waits for/accepts the canonical capture redirect before runtime API assertions.

## Important learning
The original Failed-to-fetch was a browser harness race: the capture flow intentionally redirects to /feed after persistence, so asserting Smart Feed during the redirect aborted the request. Once the navigation settled, the runtime API returned HTTP 200. The remaining projection defect was that the event carried its canonical Intelligent Block in metadata while the table projection query did not surface it; version 16 now preserves the canonical object as the projection fallback.

## Next action
Run the consolidated adversarial acceptance matrix on current main:
owner/non-owner isolation, revocation, replay/idempotency, stale intelligence, superseded lineage, receipt integrity, unauthorized persistence, and privacy boundary.

TAG -> YOU'RE IT.
