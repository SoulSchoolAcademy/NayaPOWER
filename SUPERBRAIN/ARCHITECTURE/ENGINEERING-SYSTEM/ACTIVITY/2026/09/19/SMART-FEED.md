# SMART FEED — MASTER NAYA READINESS REVIEW — 2026-09-19

**Role:** Smart Feed owner  
**Mission:** Replace demo/local feed behavior with the real canonical projection while preserving the existing Intelligent Board design.

## Executive state

**Current product readiness: 6.0 / 10 — backend v2, dedicated production surface, and Cloudflare source/runtime parity are now proven; authenticated transaction and privacy closure remain.**

### Fresh live runtime evidence

Supabase currently shows an ACTIVE `naya-smart-feed` Edge Function **v1**, JWT-protected. It supports:
- authenticated Personal/Activity retrieval from `nayanet_cognition_events`;
- cursor-style `before` pagination;
- Collective retrieval from explicit `nayanet_intelligence_publications`;
- publish/revoke;
- save/favorite/like/love interaction recording through `nayanet_record_cognition_event`.

Live tables include `nayanet_cognition_events` (124 rows), `nayanet_intelligence_publications` (0 rows), `nayanet_intelligence_index` (348 rows), and `nayanet_execution_outcomes` (0 rows). All inspected public tables have RLS enabled.

**Important:** existence of the function is not end-to-end product verification. Its deployed behavior still needs authenticated execution and two-user denial proof.

## Readiness matrix

| Dimension | Rating | State |
|---|---:|---|
| Specification | 9.5/10 | Strong three-stream/projection contract |
| Requirements completeness | 9/10 | Clear acceptance criteria |
| Today's execution plan | 9/10 | Backend v1 gives a concrete starting point |
| Engine/backend | 6/10 | Real v1 exists; deeper consequence/provenance proof remains |
| Interface/design | 8.5/10 | Existing Hub/Intelligent Board is substantial |
| Product integration | 3.5/10 | UI-to-v1 mapping not proven |
| Security/privacy | 4/10 | JWT + RLS exist; behavioral two-user proof missing |
| Runtime/deployment | 5/10 | Live function exists; source/build/UI parity not proven |
| Ship readiness | 4.7/10 | Not shippable |

## Architecture

Hub shell → Smart Feed surface → authenticated canonical retrieval → authorization → Intelligent Block → authorized action → canonical consequence → fresh retrieval.

The Feed is a projection, never a new event store.

## What is already real

- Strong Smart Feed and Activity Projection specifications.
- Existing Intelligent Board visual language.
- Live JWT-protected `naya-smart-feed` v1.
- Personal/Activity query path.
- Explicit Collective publication path.
- Pagination mechanism.
- Interaction mechanism.
- Existing cognition/event spine and RLS.

## Critical gaps

1. Activity and Personal currently share the same cognition-event retrieval branch; their intended semantic distinction must be proven/refined.
2. Collective currently has zero published rows, so real collective presentation is unproven.
3. UI is not yet proven wired to the function.
4. Interaction events need end-to-end receipt/ledger consequence verification.
5. Source/evidence drill-down is not closed.
6. Two-real-user denial is not proven.
7. Loading/empty/stale/error/unauthorized states need production QA.
8. Source→build→Cloudflare parity is not proven.
9. Demo/local state must be removed or isolated from production behavior.

## Complete today

1. Map the deployed Hub to `naya-smart-feed`.
2. Execute authenticated Activity and Personal retrieval.
3. Establish one legitimate Collective publication and retrieve it.
4. Prove pagination/no duplicates.
5. Prove source drill-down.
6. Prove save/favorite/interaction persistence and resulting canonical event.
7. Run two-user A/B isolation.
8. Replace remaining demo/local feed behavior with the real path.
9. QA every visual state without redesigning the board.
10. Capture source/build/runtime evidence.

## Definition of COMPLETE

A real authenticated human can switch ACTIVITY/PERSONAL/COLLECTIVE, retrieve only authorized canonical intelligence, paginate without duplicates, inspect provenance, perform authorized actions, refresh and observe consequences; another user is denied protected material; Cloudflare runtime matches the verified source.

**NEXT:** Wire and execute the live `naya-smart-feed` v1 against the existing Hub surface, then close authorization, consequence, parity, and visual-state proof.


## Session 003 — Production surface closure

Priority 1 is now **VERIFIED**. The dedicated Smart Feed application surface is deployed through the canonical Cloudflare release. GitHub Actions run `35453966388` passed exact artifact deployment, exact source/runtime parity, desktop runtime baseline, mobile runtime baseline, and final Assistant-lane runtime proof. The Smart Feed Edge Function is now v2 with JWT verification enabled, and the production publication boundary has explicit-consent owner authorization.

This does **not** close the feature at 10/10. The remaining work is authenticated Activity/Personal/Collective execution, real publication/retrieval, pagination/no-duplicate proof, canonical action consequences, two-user denial, and final visual state QA.

**Next:** execute authenticated Activity retrieval and consequence proof against the deployed `/feed` surface.


## Session 004 — Wave A coordination

**Timestamp:** 2026-09-19T16:27:35Z

Wave A was reconciled with Smart Tabs and Smart Ledger. The existing Smart Feed production surface remains intact. Smart Tabs now has a production persistence/API/runtime/UI path. Smart Feed authenticated execution remains open. No authenticated browser transaction or two-user proof was fabricated.

**Successor:** Execute coordinated authenticated Wave A proof across Feed retrieval, Tabs CRUD/reload/isolation, and Ledger fresh lineage.


## Session 005 — Maximum-value Wave A handoff

**Timestamp:** 2026-09-19T16:45:00Z

The execution discipline was tightened: Wave A now has a ten-action back-to-back closure sequence spanning deployed parity, authenticated Feed retrieval, pagination, explicit Collective publication, consequential interaction, Ledger lineage, two-user denial, and final evidence reconciliation. The dedicated Smart Feed source remains production-backed; authenticated browser execution remains the hard boundary and is not being fabricated.

Smart Tabs was also advanced from create/navigation-only UI to full CRUD/reorder/favorite/delete controls using the existing owner-scoped API. Commit: `c5d21b6db36661546561aeb0ec479735ba555199`.

**Successor:** Execute the ten actions in Session 005 sequentially; start with deployed Smart Tabs source/runtime parity, then use the first legitimate authenticated session available to close behavior and privacy proofs.

## Session 005 checkpoint — 2026-09-19T16:55:00Z

Wave A execution began. A real source defect was discovered in Smart Tabs before deployment parity could be claimed: commit `c5d21b6db36661546561aeb0ec479735ba555199` appended a duplicate render function after the IIFE. It was repaired in `3627a484533411921765dd53e793cf970564f818`.

**Current truth:** Smart Tabs source repair is committed; Cloudflare parity is not proven because GitHub exposes zero workflow runs for the repair commit and the available local network cannot perform an independent live hash check. Authenticated Feed/Personal/Collective and two-user proofs remain blocked by the absence of a legitimate authenticated session.

**Do not promote this checkpoint to PASS.**
## Session 006 — Authenticated production closure — 2026-09-19T16:59Z

**Wave A closure boundary materially advanced.**

- Legitimate authenticated execution path found through the production NayaNET name-first Supabase Auth adapter on the authorized Windows execution plane.
- Cloudflare release **35455850419** proved repaired Smart Tabs commit **3627a484533411921765dd53e793cf970564f818** deployed with exact live Smart Tabs SHA-256 **bb772e3888c7ebd65193c17c1fc6995460f28ee5f211c9c5a88d5b64c4cdb26b**.
- Authenticated Activity and Personal retrieval passed.
- Personal cursor pagination passed with 3 unique canonical IDs across two pages.
- Explicit Collective publish → retrieval → revoke passed.
- One consequential Feed interaction passed and generated a SUCCESS receipt plus canonical cognition event.
- Fresh Smart Ledger retrieval proved the interaction cognition row and verified execution receipt lineage.
- A/B private ownership denial passed for Feed and cognition; Smart Tabs cross-user list/update/delete passed after a real delete semantic defect was repaired.
- Repaired naya-smart-tabs is now **v2**; unauthorized delete returns **404 TAB_NOT_FOUND_OR_NOT_AUTHORIZED**.
- Publication owner-read RLS was repaired so an owner can inspect a revoked publication while Collective readers cannot.

**Current product state:** backend/security/lineage closure is substantially proven. Remaining closure is authenticated browser-level visual interaction QA, direct human target-navigation proof, final accessibility/mobile acceptance, and the independent execution-outcome observation boundary.

**Successor:** finish those remaining product-facing closure boundaries, then perform final Wave A acceptance.
## Session 007 — Live runtime cache-bust repair — 2026-09-19T17:10Z

Live browser observation exposed a stale Assistant Runtime cache key in the Hub HTML: assistant-runtime.js?v=20260918-r7. The stale cached runtime threw a browser SyntaxError and left NayaAssistantRuntime undefined. The Hub source was repaired to assistant-runtime.js?v=20260919-wavea6 in commit **6018ed5002ee09505767852e4f39d1d81c9c96ab**.

Cloudflare run **35457054828** deployed the repair and passed exact live parity plus desktop/mobile/final runtime checks. Early live browser observation after deployment confirmed NayaAssistantRuntime and listSmartTabs are present. Authenticated browser CRUD remains the narrow remaining Feed/Tabs UI boundary.