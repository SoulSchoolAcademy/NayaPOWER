# JOB 01 — SMART FEED
## Mission
Make Smart Feed the truthful authenticated retrieval/presentation spine of NayaNET.

## Current known state
Live `naya-smart-feed` v1 is JWT-protected and supports Personal/Activity retrieval, cursor-style `before` pagination, Collective retrieval from `nayanet_intelligence_publications`, publish/revoke, and save/favorite/like/love through canonical cognition-event recording. Current evidence shows 348 intelligence-index rows, 124 cognition events, and 0 publications.

## Job
Map the existing Hub Feed UI to the live Smart Feed runtime without redesigning the visual product.

## Build
- Identify canonical Feed component/regions in `2026 09 17 NAYANET HUB.html`.
- Separate presentation from data/retrieval logic.
- Connect Personal, Activity, and Collective modes to the real API.
- Preserve cursor pagination and truthful loading/empty/error states.
- Connect interaction consequences to the canonical cognition/event path.
- Ensure source attribution/drill-down exists where the underlying record supports it.
- Ensure visibility/authority filtering happens before presentation.
- Do not create a second feed database or duplicate intelligence index.
- Prove authenticated owner isolation and non-owner denial where applicable.
- Remove or clearly eliminate demo/local-state behavior from the production path.
- Prove source → build → Cloudflare runtime parity.

## Acceptance
A real authenticated user can open Feed, retrieve real intelligence, paginate, inspect source context, perform supported interactions, reload, and see truthful persisted state. Unauthorized/second-user access is denied. Empty Collective state is truthful until publications exist.

## Evidence required
Capture endpoint/version, source files, database objects, authenticated request/response behavior, persistence, denial test, and deployed Cloudflare result.

## Handoff
Update Smart Feed report/checklist/activity and leave one exact successor action for Smart Tabs and Smart Ledger integration.
