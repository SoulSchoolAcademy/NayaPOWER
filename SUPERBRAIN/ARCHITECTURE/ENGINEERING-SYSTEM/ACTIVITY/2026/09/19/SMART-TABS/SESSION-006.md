# Wave A Session 006 — Authenticated Production Closure

**Timestamp:** 2026-09-19T16:59Z
**Mission:** Execute the real authenticated Wave A proof across Smart Tabs, Smart Feed, and Smart Ledger using legitimate Supabase Auth sessions; repair any concrete defect encountered; record evidence.

## Authenticated execution surface

A legitimate execution path was found on the authorized Windows execution plane: the production NayaNET name-first identity adapter uses Supabase Auth signInAnonymously() and provisions members / nayanet_profiles. Two real Supabase Auth sessions were created for this proof. No fabricated JWT, service-role human impersonation, or copied browser credential was used.

## Actions executed

### Action 01 — execution surface
**PASS.** Authorized Desktop Commander device was online. Repository contains production closure tooling, the canonical Cloudflare release workflow, Supabase runtime, and the name-first Supabase Auth adapter. gh auth status confirmed the authorized GitHub account is logged in. The authenticated NayaNET path was then exercised through Supabase Auth.

### Action 02 — repaired Smart Tabs deployment
**PASS.** Cloudflare release run 35455850419 used head SHA 3627a484533411921765dd53e793cf970564f818 and completed successfully. Deploy job 105930850691 passed exact source parity, exact runtime parity, desktop baseline, mobile baseline, and final Assistant-lane proof. Smart Tabs live SHA-256: bb772e3888c7ebd65193c17c1fc6995460f28ee5f211c9c5a88d5b64c4cdb26b.

### Action 03 — Smart Tabs CRUD/reload
**PASS.** Authenticated User A created two tabs, edited label/target, toggled favorite, reordered both, reloaded from server, then deleted both. Final server list was empty for that test owner. Tab IDs: 718c7d36-58fd-42ba-9b17-7d9b4b87c665 and 4c4e503e-97fa-445c-b5b9-023e695f7f8a.

### Action 04 — Smart Tabs isolation
**PASS.** User B list returned zero A tabs. B update returned HTTP 400 because no authorized row was visible. During this action the delete path was discovered to return a false-success envelope when RLS deleted zero rows. This was a real semantic defect. It was repaired by deploying naya-smart-tabs v2 so unauthorized delete now returns 404 TAB_NOT_FOUND_OR_NOT_AUTHORIZED. The repaired delete behavior was then exercised: B delete returned HTTP 404 and A's tabs remained intact.

### Action 05 — Activity + Personal
**PASS.** User A Activity returned only A's authenticated cognition event; it did not contain B's private event. Personal returned A's event and excluded B. User B Personal returned B's event and excluded A.

### Action 06 — Personal pagination
**PASS.** Three fresh A cognition events were retrieved with limit=2, then the returned next_before cursor. Page 1 contained two unique canonical row IDs; page 2 contained the third. Combined count 3, unique count 3, descending creation order preserved.

### Action 07 — Collective publish/retrieve/revoke
**PASS.** A explicitly published cognition row e68f49a2-1bf0-4ea0-9272-9ad5969b027b; publication e8b86117-3e84-4556-843a-3c1e5dae8c68 appeared to B in Collective with consent_state=explicit. A revoked it successfully after the RLS read-policy repair. The revoked row remained visible to its owner with status revoked; B's Collective stream no longer contained it.

### Action 08 — consequential Feed action
**PASS.** B performed like on A's explicitly published source. The real Feed function returned a SUCCESS receipt with cognition event 44cf8718-c268-4bec-b596-194e5c62af99 and receipt 6c7784e3-e9b1-4bd0-b45f-0d73dae5e793.

### Action 09 — fresh Smart Ledger lineage
**PASS.** B's fresh Ledger retrieval contained the interaction cognition row cb82a32e-8077-4390-9498-1c5ff95801b2 with source 44cf8718-c268-4bec-b596-194e5c62af99, followed by verified execution receipt Ledger row faa28b8e-0339-4ba3-82bc-3ce6f7338d1a with source 6c7784e3-e9b1-4bd0-b45f-0d73dae5e793, receipt status SUCCESS, and chain sequence 123/124.

### Action 10 — A/B denial matrix
**PASS for tested private boundaries.** A could retrieve A; B could retrieve B; A could not retrieve B; B could not retrieve A. Smart Tabs cross-user list/update/delete were denied server-side, and Feed Personal/Activity were owner-scoped. Collective was intentionally available to both while published, then disappeared after revoke. The tested matrix therefore distinguishes private ownership from explicit collective visibility.

## Concrete repairs made

1. Deployed naya-smart-tabs v2. Unauthorized delete now returns an explicit not-authorized/not-found result instead of a false success.
2. Applied migration smart_feed_publication_owner_read_revoked_v2 so publication owners can retrieve their own revoked publication while collective readers only see explicitly published rows.

## Current truth

**PROVEN:** Cloudflare Smart Tabs source/runtime parity; authenticated Smart Tabs CRUD/reload/reorder/favorite/delete; Smart Tabs A/B isolation; Activity; Personal; Personal pagination; explicit Collective publish/revoke; one consequential Feed interaction; fresh Smart Ledger lineage; private A/B denial.

**NOT YET PROVEN:** browser-level human visual QA of the authenticated Smart Tabs/Feed controls; direct human target-navigation click proof; final AAA accessibility/mobile interaction audit on the authenticated surfaces; independent nayanet_execution_outcomes observation boundary; complete final Wave A UI acceptance.

## Protected constraints

No fake auth. No fabricated JWT. No service-role human impersonation. No client-only privacy. No duplicate event/ledger universe. No promotion of receipt existence into independent observed outcome.

## Successor

Complete the remaining product-facing authenticated browser/visual proof and the independent outcome-observation boundary, then reconcile Wave A to final acceptance and generate the next ten highest-value actions.
