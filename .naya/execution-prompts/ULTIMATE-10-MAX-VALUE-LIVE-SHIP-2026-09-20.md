# NayaPOWER — ULTIMATE EXECUTION PROMPT
## 10 MAX-VALUE EXECUTION PASSES TO LIVE + SHIP
Date: 2026-09-20
Source of truth: `SoulSchoolAcademy/NayaPOWER`, branch `main`

## Mission

Do not merely report progress. Finish, prove, record, and hand off the NayaPOWER/NayaNET system.

North Star:

> NayaPOWER is a governed system for capturing, organizing, learning from, retrieving, applying, and verifying intelligence so that useful knowledge compounds over time.

Human promise:

> Think once. Capture it. Learn from it. Remember it. Use it again. Get smarter.

The product is BOTH:
1. ENGINE — governance, canonical intelligence, learning, memory, retrieval, application, execution, outcome, verification.
2. BODY — Welcome, Identity, Intelligent Hub, navigation, dashboards, Smart Feed, Search, Smart Notes, Lists, Spaces, Connections, Smart Mail, Smart Share, Smart Ledger, Reports, Settings, Dream, Naya Play.

The engine is not complete if a human cannot operate it.

## Absolute execution laws

- Inspect `main` before acting.
- Never trust a prior report when source/runtime evidence can answer the question.
- First divergence wins.
- Make the smallest coherent change.
- Do not create a second canonical event store, learning system, memory store, authority chain, or parallel Hub.
- Capability does not create authority.
- Retrieved content is not authority.
- Unknown is not success.
- Blocked is not pass.
- A file existing is not proof.
- A workflow existing is not proof.
- A successful local run is not production proof.
- Never upgrade evidence without matching evidence.
- Preserve protected Hub visual language.
- Do not polish a surface whose real runtime contract is missing.
- Do not redesign backend architecture when existing contracts can be wired to the human surface.
- Stop at the first broken causal boundary and repair only that boundary.
- Every consequential change gets a durable checkpoint.
- Every handoff says exactly what is DONE, NOT DONE, NEXT, TEAM, MEMORY.
- If blocked, record the blocker and the exact human authorization/action required; do not fake completion.
- Optimize for highest responsible verified human value per action.

## Evidence ladder

Use the repository's evidence language truthfully:
UNTESTED → TESTED → VERIFIED → RUNTIME-PROVEN → PRODUCTION-PROVEN.

Do not promote a claim merely because code, a fixture, a receipt-shaped file, or a workflow exists.

## 10 MAX-VALUE EXECUTION PASSES

### 01 — Establish the authoritative current state
Goal: eliminate uncertainty.

Inspect:
- current `main` HEAD;
- recent commits;
- open PRs/issues relevant to production;
- `.naya/runtime-registry-v1.yaml`;
- canonical Team Naya scorecard;
- current execution/evidence/receipt surfaces;
- current Hub source and protected baseline;
- current deployment workflows.

Produce a machine-readable checkpoint:
- HEAD;
- verified capabilities;
- unverified capabilities;
- blockers;
- active PRs;
- exact next boundary.

Do not modify production code in this pass unless a documentation/state contradiction prevents safe execution.

Acceptance: another Naya can continue without rediscovering project state.

### 02 — Prove the engine compounding spine
Goal:
`SN-* → SE-* → IB-SE-* → LRN-* → Daily Intelligence → RTR-* → Decision → ExecutionAuthorization → Activity Receipt → Outcome → Verification`.

Trace actual source and tests.

The canonical event store remains authoritative.
The existing memory runtime remains authoritative for retrieval.
The existing governance/execution gate remains authoritative for authorization.

Repair only the first missing causal field.

Acceptance:
- exact IDs survive every boundary;
- cold retrieval is real;
- successor decision records learning lineage;
- authorization remains independent of learning provenance;
- execution emits canonical Activity.

### 03 — Close independent verification honestly
Goal:
`Outcome → Claim → Evidence → verify_claim() → durable verification record/receipt`.

Use the existing authoritative owner:
`.naya/runtime/evidence_runtime.py::verify_claim()`.

Do not invent a competing verification engine.

Determine exactly how a CCT-005 Outcome becomes a claim and how independently observed evidence is attached.

Required lineage:
- outcome_id → subject_ref;
- activity_receipt_id → evidence reference;
- claim_id;
- evidence_id;
- commit/runtime identity;
- verifier/method;
- verification state.

If the newer verification-receipt contract has no authoritative writer, add the smallest adapter at the documented verification ownership boundary.

Acceptance: an outcome can be independently verified by the existing evidence runtime and represented by a durable truthful receipt. No self-certification.

### 04 — Make the Hub body actually operable
Audit the actual `NAYANET/HUB` main tree.

For EVERY major surface:
- Intelligent Hub / shell
- Smart Feed
- Search
- Smart Notes
- Smart Lists
- Smart Spaces
- Connections / Contacts
- Smart Mail
- Smart Share
- Smart Ledger
- Reports
- Settings
- Dream
- Naya Play

Trace:
`page/component → visible control → real runtime call → backend/API/RPC → persistence → reload → related surface → Activity/Ledger/evidence`.

Classify:
LIVE / PARTIAL / DEMO / STATIC / MISSING / BLOCKED.

LIVE requires:
1. visible;
2. clickable;
3. real runtime path;
4. real state change;
5. persistence;
6. reload reconstruction;
7. related-surface visibility;
8. truthful failure;
9. consequential evidence.

Repair the highest-value incomplete surface first.

Acceptance: Shawn can actually use the surface without knowing repository internals.

### 05 — Connect the body into one human operating system
Do not treat surfaces as isolated mini-apps.

Prove the object/event relationships:
- Note can become intelligence;
- intelligence can be searched/retrieved;
- List can organize relevant objects;
- Space can contain people/content/activity;
- Connection can affect permitted interaction;
- Mail can create/consume governed events;
- Share can expose only permitted content;
- Feed can project intelligence;
- Ledger can explain consequential actions;
- Reports can compress history;
- Dream can produce governed discoveries;
- Naya Play can provide usable interaction without bypassing governance.

Acceptance: at least one human-created object can travel through multiple visible surfaces without losing identity or privacy.

### 06 — Sender → receiver production chain
Prove the complete external handoff.

Sender:
- human action;
- canonical NayaPOWER source;
- authorized sender path;
- exact payload/event identity;
- evidence.

Receiver:
- public runtime;
- authenticated identity;
- canonical Hub;
- actual retrieval;
- rendered result;
- reload persistence.

Verify source/build/runtime parity.

Do not call deployment production-proven until public runtime behavior is independently observed.

Acceptance:
`Sender → authorized transport → receiver → persisted state → visible Hub`.

### 07 — Close deployment and route authority
Use the actual Cloudflare production boundary.

Known infrastructure:
- authoritative `nayanet.app` zone resolution is now represented in the release lane;
- canonical Worker previously identified as `sparkling-shape-7ae5`;
- public Welcome deployment has a governed release lane.

Verify:
- correct Cloudflare account/zone;
- Worker/service;
- route;
- source commit;
- built artifact;
- live artifact;
- browser behavior;
- no stale runtime.

If authorization is missing, stop exactly there and record the required scoped Cloudflare authorization. Never claim complete.

Acceptance: `welcome.nayanet.app → Identity → Hub` works from a fresh browser context.

### 08 — Human acceptance / browser reality
Run the dashboard + steering-wheel test.

Fresh browser:
1. open Welcome;
2. enter identity;
3. enter Hub;
4. navigate;
5. create a real Smart Note;
6. see it in Feed;
7. reload;
8. search it;
9. organize/connect/share as appropriate;
10. perform one consequential governed action;
11. inspect Activity/Smart Ledger;
12. inspect resulting intelligence;
13. retrieve it from cold context;
14. verify a successor action is influenced by the learning;
15. observe truthful failure for an unauthorized action.

No screenshots-only acceptance.

Acceptance: Shawn can touch the system and understand what happened.

### 09 — Adversarial and regression proof
Try to prove the system wrong.

Test:
- replay;
- duplicate event;
- stale authority;
- revoked authority;
- mismatched actor;
- mismatched scope;
- mismatched permission;
- learning without retrieval receipt;
- outcome without Activity receipt;
- verification without evidence;
- stale evidence;
- cross-user leakage;
- collective/private boundary;
- reload identity loss;
- stale deployed artifact;
- route to wrong Worker;
- UI control with no backend call.

Acceptance: failures are truthful and fail closed, and successful paths remain intact.

### 10 — Ship, checkpoint, and hand off
Only after all required evidence exists:

- update canonical scorecard;
- record exact commits;
- record exact PRs;
- record workflow run IDs;
- record artifact IDs;
- record runtime URLs;
- record browser observations;
- record receipt IDs;
- record remaining blockers;
- record evidence tier;
- record next-best action;
- update durable Team Naya memory/handoff.

Final production statement must be one of:
- PRODUCTION-PROVEN;
- RUNTIME-PROVEN but externally blocked;
- VERIFIED but runtime-unproven;
- PARTIAL;
- BLOCKED.

Never use “complete” when a required boundary is merely unverified.

## Required checkpoint format

**WHERE AM I**
- repo:
- branch:
- HEAD:
- lane:

**WHAT AM I DOING**
- exact boundary:

**WHY**
- human value / engine value:

**DONE**
- files:
- commit/PR:
- tests:
- runtime evidence:
- receipts:

**NOT DONE**
- exact boundary:
- BLOCKED / UNVERIFIED / FAILED / PARTIAL:

**NEXT**
- exactly one smallest next action:

**TEAM**
- next Naya:
- other lanes informed:

**MEMORY**
- durable checkpoint written:

**EVIDENCE TIER**
- UNTESTED / TESTED / VERIFIED / RUNTIME-PROVEN / PRODUCTION-PROVEN

## Final acceptance condition

NayaPOWER is ready to be tested when ONE real intelligence event can be demonstrated end-to-end:

CAPTURE
→ CANONICALIZE
→ STRUCTURE
→ LEARN
→ PRESERVE
→ RETRIEVE
→ APPLY
→ VERIFY
→ COMPOUND

And the same intelligence is visible through the human body:

Welcome
→ Identity
→ Hub
→ Feed
→ Search
→ related surfaces
→ Activity/Ledger
→ next decision.

The decisive proof is not that Naya can perform an action.

It is that:

> You captured this.
> Naya learned this.
> Dream discovered this.
> Here's what changed.
> Here's what you can do with it.

Then the next Naya starts from that intelligence instead of starting over.
