# LEAD NAYA — FULL MASTER EXECUTION DIRECTIVE
## COMMUNICATION + ORGANIZATION SUBSYSTEM
**Date:** 2026-09-19  
**Owner:** Lead Naya  
**Repository:** `SoulSchoolAcademy/NayaPOWER`  
**Live Supabase project:** `dahisasgpfvziswqvmvm`  
**Supabase Functions:** https://supabase.com/dashboard/project/dahisasgpfvziswqvmvm/functions  
**Canonical Hub source:** `2026 09 17 NAYANET HUB.html`  
**Deployment target:** Cloudflare  
**Status:** IN PROGRESS — ACTIONS 01–05 EXECUTED; ACTION 06 IS THE IMMEDIATE EXECUTION

---

# 1. MISSION

Turn Your Connections, Smart Spaces, Smart List, Smart Mail and Smart Share into one authenticated, permissioned, observable, evidence-producing NayaNET relationship system.

The final causal chain is:

**IDENTITY → SPACE → DISCOVERY → JOIN → MEMBERSHIP → CONNECTION → SMART LIST → SMART MAIL → SMART SHARE → ACTIVITY → LEDGER → INTELLIGENCE → REVOCATION**

The governing relationship law is:

> **Interest may create discovery. Membership may create relationship. Relationship may enable communication. Authority determines what communication is permitted.**

The human-facing interfaces are:

- **Your Connections = WHO**
- **Smart Spaces = WHERE**
- **Smart List = HOW I ORGANIZE**
- **Smart Mail = HOW I COMMUNICATE**
- **Smart Share = WHAT I AM AUTHORIZED TO SHARE**

Do not build five disconnected features. Build one underlying relationship system with five interfaces.

---

# 2. WHY THIS MATTERS

The missing capability is not another screen.

It is the ability for NayaNET to represent a real human relationship with a defensible causal history:

**Person → shared context → participation → relationship → permission → communication/organization → observation → evidence → revocation.**

If JOIN does not create real membership, then Connections is fake.

If Connections is fake, Mail authorization is fake.

If Mail is only client-visible state, communication is fake.

If Activity is manually generated, history is fake.

If Ledger is disconnected, evidence is incomplete.

If Cloudflare serves different code than the source, the product is not actually deployed.

Therefore every layer must agree.

---

# 3. SYSTEM CONTEXT

NayaNET is a private intelligent network.

NayaPOWER is the governance/control substrate around intelligence and action.

The Hub is the human-facing projection/cockpit.

The database/event substrate is the canonical state and history.

Authority determines whether an action is permitted.

RLS protects data boundaries.

The event spine records consequential state changes.

The Smart Ledger preserves evidence/integrity.

Cloudflare is the intended deployed human-facing runtime.

Core privacy principle:

**Private by default • Shared by choice • Collective by consent • Public by decision.**

Core governance principle:

**Capability does not create authority.**

Do not allow a technically reachable recipient, Space, record or attachment to become automatically authorized.

---

# 4. CURRENT PRODUCT STATE

The architecture is defined but the subsystem is not yet production-verified.

Current readiness by surface:

| Surface | Current state |
|---|---|
| Your Connections | Architecture DEFINED; runtime NOT PROVEN |
| Smart Spaces | Partial production primitive; JOIN/MEMBERSHIP NOT PROVEN |
| Smart List | Architecture DEFINED; runtime substrate NOT MAPPED |
| Smart Mail | Live production function; relationship gating NOT PROVEN |
| Smart Share | Defined boundary; current publication rows = 0 |
| Activity | Existing canonical event substrate FOUND |
| Smart Ledger | Existing populated canonical substrate FOUND |
| Intelligence | Existing populated canonical substrate FOUND |
| Revocation | Authority revocation primitives exist; relationship revocation NOT PROVEN |
| Cloudflare | Deployment parity UNKNOWN |

The most important unresolved boundary is:

**JOIN → MEMBERSHIP**

---

# 5. WHAT HAS ALREADY BEEN BUILT

Already defined and committed:

- Communication + Organization architecture.
- Your Connections specification.
- Smart Spaces specification.
- Smart List specification.
- Smart Mail specification.
- Smart Share specification.
- Team Naya Job 04 for Communication + Organization.
- Relationship lifecycle.
- Space discovery/JOIN concept.
- Activity/Ledger integration model.
- Privacy/authority distinctions.
- Lead Naya master handoff.
- Daily activity hierarchy.
- Feature completion/activity requirements.
- Canonical Hub visual baseline.

Relationship lifecycle:

**DISCOVER → VIEW → JOIN → MEMBERSHIP ACTIVE → CONNECTION ELIGIBLE → CONNECTION ESTABLISHED → COMMUNICATE / ORGANIZE → OBSERVE → REVOKE / LEAVE**

JOIN is primary. INVITE is secondary.

No new relationship/contact database is authorized before existing production primitives are reconciled.

---

# 6. WHAT HAS ACTUALLY BEEN PROVEN

Action 01 inspected actual live/source evidence.

### Live production facts observed

- `nayanet_spaces`: 1 row.
- `v7_connection_requests`: 0 rows.
- `v7_mail_threads`: 64 rows.
- `v7_mail_members`: 128 rows.
- `v7_mail_messages`: 64 rows.
- `nayanet_cognition_events`: 123 rows.
- `nayanet_smart_ledger`: 94 rows.
- `nayanet_intelligence_index`: 353 rows.
- `nayanet_execution_receipts`: 125 rows.
- `nayanet_execution_outcomes`: 0 rows.
- `nayanet_intelligence_publications`: 0 rows.

### Existing production primitives proven present

Identity/profile:

- `members`
- `nayanet_profiles`
- `v7_profiles`

Space:

- `nayanet_spaces`
- `nayanet_space_intelligence`

Relationship:

- `v7_connection_requests`

Communication:

- `nayanet-smart-mail` v12, ACTIVE, JWT-protected.
- `v7_mail_threads`
- `v7_mail_members`
- `v7_mail_messages`

Authority:

- `nayanet_authority_grants`
- `nayanet_validate_authority_grant`
- `nayanet_issue_authority_grant`

Evidence/intelligence:

- `nayanet_cognition_events`
- `nayanet_smart_ledger`
- `nayanet_intelligence_index`
- `nayanet_execution_receipts`

### Critical proven findings

1. A production connection-request primitive already exists.
2. A production Space primitive exists.
3. A dedicated Space-membership table was not found in the inspected public live inventory.
4. Multiple identity/profile layers exist.
5. Smart Mail is real and protected by JWT + authority.
6. Smart Mail relationship gating is not yet proven.
7. Canonical event/Ledger infrastructure exists.
8. Cloudflare deployment parity is not yet mapped.

---

# 7. WHAT IS NOT PROVEN

The following must remain explicitly NOT PROVEN until evidence exists:

- canonical identity owner;
- canonical public profile owner;
- canonical Space membership;
- authenticated Space JOIN;
- membership persistence;
- JOIN idempotency;
- relationship establishment;
- accepted connection-request semantics;
- connection provenance;
- Smart List person/connection membership;
- relationship-gated Smart Mail;
- revocation-at-use;
- two-user isolation;
- unauthorized-user denial;
- protected attachment denial;
- replay/idempotency across the complete relationship flow;
- Activity causal projection;
- Ledger consequence for relationship/communication events where required;
- Cloudflare source/build/runtime parity.

No engineer may turn any of these into VERIFIED by documentation, source code existence, screenshots of static UI, or local state.

---

# 8. CURRENT SOURCE OF TRUTH

Priority order:

1. **Live authorization/data behavior** for runtime truth.
2. **Canonical GitHub source and migrations** for implementation truth.
3. **Feature specifications and .naya authority documents** for intended contract.
4. **Activity/handoff records** for engineering history.
5. **Conversation memory** only as context, never as production proof.

Canonical repository:

`SoulSchoolAcademy/NayaPOWER`

Canonical engineering directory:

`NayaNETEngineeringSystem/`

Canonical Hub:

`2026 09 17 NAYANET HUB.html`

Current Team Naya master directive:

`NAYA-TEAM/2026/09/19/2026-09-19__LEAD-NAYA-MASTER-HANDOFF-COMMUNICATION-ORGANIZATION.md`

Supabase project:

`dahisasgpfvziswqvmvm`

---

# 9. CANONICAL ARCHITECTURE

The underlying system is:

**AUTH USER → CANONICAL MEMBER/PROFILE → SPACE → MEMBERSHIP → RELATIONSHIP → AUTHORITY → COMMUNICATION/ORGANIZATION/SHARING → EVENT → LEDGER/INTELLIGENCE**

Four primary interfaces:

### WHO
Your Connections.

### WHERE
Smart Spaces.

### HOW I ORGANIZE
Smart List.

### HOW I COMMUNICATE
Smart Mail.

### WHAT I MAY SHARE
Smart Share.

Required distinctions:

- discovery ≠ membership;
- membership ≠ connection;
- connection ≠ authority;
- authority ≠ sharing;
- sharing ≠ public;
- communication ≠ intelligence access.

---

# 10. EXISTING PRODUCTION PRIMITIVES

## Identity
- `members`
- `nayanet_profiles`
- `v7_profiles`

## Spaces
- `nayanet_spaces`
- `nayanet_space_intelligence`

## Relationship clue
- `v7_connection_requests`

Its observed fields include:

`id, requester_id, target_id, topic, status, created_at, responded_at`

Observed RLS:
- requester can insert own request;
- requester or target can read;
- target can update.

Current rows: 0.

## Mail
- `v7_mail_threads`
- `v7_mail_members`
- `v7_mail_messages`
- Edge Function `nayanet-smart-mail` v12.

## Authority
- `nayanet_authority_grants`
- `nayanet_validate_authority_grant`
- `nayanet_issue_authority_grant`

## Events / evidence
- `nayanet_cognition_events`
- `nayanet_smart_ledger`
- `nayanet_intelligence_index`
- `nayanet_execution_receipts`
- `nayanet_execution_outcomes`

## Sharing
- `nayanet_intelligence_publications`

Do not duplicate these stores.

---

# 11. FEATURE-BY-FEATURE STATUS

## Your Connections
Architecture defined.

Must become a projection of canonical identity + relationship state.

Needs:
- index/detail;
- origin;
- shared Spaces;
- current relationship state;
- communication eligibility;
- List action;
- privacy-safe profile projection.

## Smart Spaces
Production Space object exists.

Needs:
- authenticated creation;
- discovery;
- JOIN;
- membership persistence;
- participant state;
- activity;
- interaction;
- leave/revoke;
- unauthorized denial.

## Smart List
No confirmed canonical person/connection List substrate has yet been mapped.

Needs:
- source reconciliation;
- canonical list ownership;
- connection membership;
- add/remove;
- reload;
- owner isolation;
- no relationship deletion from list removal.

## Smart Mail
Live v12 function.

Needs:
- relationship eligibility at use time;
- authority at use time;
- recipient preview;
- real recipient authorization;
- send;
- receiver verification;
- replay/idempotency;
- revoked-state denial;
- attachment authorization.

## Smart Share
Publication table currently has 0 rows.

Needs:
- authorized share;
- exact scope;
- provenance;
- recipient denial;
- revoke;
- protected intelligence denial.

## Activity / Ledger
Existing infrastructure exists.

Needs:
- causal relationship/communication events;
- projection;
- evidence;
- no duplicate event store.

---

# 12. SECURITY / AUTHORITY MODEL

Every consequential action must evaluate at use time:

**authenticated actor + target + relationship + Space membership + visibility + authority + revocation + scope + RLS + idempotency**

Existing authority substrate must remain intact.

Smart Mail currently validates an authority grant for `smart_mail_send`.

Do not replace authority with a boolean such as `connected=true`.

Connection eligibility is a prerequisite/context boundary; authority remains the permission boundary.

A technically callable function is not proof of authorization.

A UI button is never an authorization boundary.

---

# 13. PRIVACY MODEL

**Private by default • Shared by choice • Collective by consent • Public by decision.**

Rules:

- Non-members must not see protected Space content.
- Membership must not reveal private profile attributes.
- Discovery must not reveal private inferred interests.
- Connection must not imply unrestricted intelligence access.
- Communication must not imply sharing authority.
- A revoked relationship must be re-evaluated at use time.
- Naya may surface authorized relevance without exposing private signals.
- No automatic messaging based solely on inferred similarity.

---

# 14. DATA / EVENT / LEDGER MODEL

Do not create a parallel relationship event store.

Use existing event infrastructure.

Expected causal pattern:

**ACTION → CANONICAL EVENT → ACTIVITY PROJECTION → LEDGER/EVIDENCE WHERE CONSEQUENTIAL → INTELLIGENCE PROJECTION WHERE CONTRACTED**

Relevant existing functions include:

- `nayanet_record_cognition_event`
- `nayanet_cognition_event_to_ledger`
- `nayanet_space_to_ledger`
- `nayanet_record_smart_mail`
- `nayanet_record_smart_mail_outcome`
- `nayanet_send_smart_mail`
- `nayanet_send_smart_mail_authorized`

Every new mutation must preserve actor, target/context, authorization, timestamp, idempotency where applicable, resulting state and provenance.

---

# 15. FRONT-END REQUIREMENTS

Preserve the existing canonical Hub design.

Do not redesign the visual system.

## Your Connections
- WHO;
- relationship state;
- why connected;
- shared Space/context;
- Mail action only when eligible;
- Add to List;
- search/filter;
- truthful loading/empty/error/revoked states.

## Smart Spaces
- Space list/detail;
- purpose/topic;
- visibility;
- JOIN THE CONVERSATION;
- INVITE;
- participant state;
- authorized activity;
- interaction;
- LEAVE;
- truthful state transitions.

## Smart List
- list index;
- create/edit/delete where contracted;
- person/connection membership;
- add/remove;
- no duplicate members;
- removal does not delete relationship.

## Smart Mail
- recipient selection;
- eligibility;
- send;
- verification;
- idempotency;
- unauthorized state;
- revoked state;
- attachment authorization;
- truthful loading/error/empty states.

No fake local success.

---

# 16. BACK-END REQUIREMENTS

Canonical ownership must be explicit for:

- identity;
- profile;
- Space;
- membership;
- relationship;
- List;
- Mail;
- sharing;
- authority;
- event;
- Ledger.

Every mutation must be server-authorized.

Every relationship-sensitive action must re-check state at use time.

Every mutation must be idempotent where the contract requires it.

Every protected read must respect RLS/visibility.

---

# 17. RUNTIME REQUIREMENTS

The runtime must prove:

- real authentication;
- real database reads/writes;
- no browser-local production state;
- no demo data;
- no fake success;
- no dead controls;
- truthful loading;
- truthful empty;
- truthful errors;
- truthful unauthorized state;
- reload persistence;
- stale-state rejection where necessary;
- server-side authorization;
- real activity/evidence consequence.

---

# 18. CLOUDFLARE DEPLOYMENT REQUIREMENTS

Cloudflare is the deployment target.

Current state: **UNKNOWN / NOT PROVEN.**

Must map:

**SOURCE FILE → BUILD INPUT → BUILD ARTIFACT → DEPLOYMENT → LIVE ROUTE → DEPLOYED COMMIT/MARKER → BROWSER**

Verify that the deployed runtime contains the same identity/auth/navigation/relationship implementation as the canonical source.

No Cloudflare parity claim without concrete evidence.

---

# 19. INTEGRATION REQUIREMENTS

Required connected flow:

**Human auth**
→ Hub
→ Space discovery
→ JOIN
→ membership
→ relationship
→ Connections
→ Smart List
→ Mail
→ Smart Share where separately authorized
→ Activity
→ Ledger
→ Intelligence
→ Leave/Revoke
→ denial/restriction
→ evidence.

Cross-feature rules:

- Space membership is a relationship origin, not unlimited authority.
- Connections projects relationship state.
- List organizes relationships; it does not own them.
- Mail communicates only when authorized.
- Share controls intelligence distribution separately.
- Activity observes canonical events.
- Ledger records consequential evidence.

---

# 20. NON-GOALS / THINGS NOT TO BUILD

Do not build:

1. duplicate contact database;
2. duplicate identity store;
3. duplicate Space store;
4. duplicate membership store before reconciliation;
5. duplicate message store;
6. duplicate event/activity database;
7. duplicate Ledger;
8. duplicate intelligence index;
9. browser-local production relationship state;
10. direct-message bypass around Space/relationship rules;
11. authority bypass;
12. redesigned Hub;
13. fake demo data;
14. synthetic-user proof;
15. speculative AI discovery that exposes private information.

---

# 21. KNOWN RISKS

### R1 — Missing membership substrate
Highest architectural risk.

### R2 — Multiple identity layers
Risk of joining one identity model while Mail/Hub uses another.

### R3 — Legacy connection-request primitive
Risk of creating a second relationship graph.

### R4 — Mail authorization gap
Risk that authority exists without relationship eligibility.

### R5 — List substrate unknown
Risk of duplicate organization storage.

### R6 — Event duplication
Risk of creating UI-only activity.

### R7 — Cloudflare drift
Risk of source and deployed runtime diverging.

### R8 — Two-user isolation
Not yet proven for this subsystem.

### R9 — Revocation
Authority revocation exists, but relationship revocation is not yet proven.

### R10 — False completion
Existing documentation is ahead of runtime proof in several features.

---

# 22. KNOWN GAPS

The current gap list is:

1. canonical identity decision;
2. canonical Space membership decision;
3. real JOIN;
4. relationship substrate decision;
5. Connections runtime;
6. Smart List runtime;
7. relationship-gated Mail;
8. Smart Share runtime proof;
9. relationship revocation;
10. two-user adversarial proof;
11. Cloudflare deployment map;
12. complete source/build/runtime parity;
13. current authenticated Hub proof;
14. full causal Activity/Ledger proof for the subsystem.

---

# 23. EXACT EXECUTION SEQUENCE

Execute in this order. Do not reorder to skip a dependency.

**01 Truth map**  
→ **02 Identity + membership reconciliation**  
→ **03 Relationship reconciliation**  
→ **04 Real JOIN**  
→ **05 Connections projection**  
→ **06 List + Mail binding**  
→ **07 Activity + Ledger binding**  
→ **08 Two-user adversarial proof**  
→ **09 Cloudflare parity**  
→ **10 Closure + handoff**

Each action must finish with:

**DONE / PROOF / NOT PROVEN / DECISION / BLOCKERS / NEXT**

The NEXT must itself be a full cold-start master directive.

---

# 24. 10 MAX-VALUE ACTIONS

## ACTION 01 — PRODUCTION TRUTH MAP
**STATUS: COMPLETE**

Inspect:
- live Supabase tables;
- columns;
- RLS;
- functions;
- Edge Functions;
- Smart Mail;
- canonical Hub;
- feature records;
- Cloudflare/source markers.

Evidence already established:
- Space exists;
- connection-request primitive exists;
- Mail exists;
- identity layers exist;
- no dedicated Space-membership table found in public inventory;
- event/Ledger substrate exists;
- Cloudflare parity remains unknown.

Do not implement.

## ACTION 02 — CANONICAL IDENTITY + SPACE MEMBERSHIP
**STATUS: READY — IMMEDIATE**

Inspect all source/migrations/functions/triggers/constraints/RLS for:
- `members`;
- `nayanet_profiles`;
- `v7_profiles`;
- `nayanet_spaces`;
- `space`;
- `member`;
- `participant`;
- `membership`;
- `join`;
- `leave`;
- `invite`.

Answer:
1. canonical identity key;
2. canonical profile;
3. legacy profile;
4. Space owner semantics;
5. visibility;
6. discovery;
7. JOIN;
8. INVITE;
9. membership storage;
10. duplicate prevention;
11. membership states;
12. LEAVE;
13. REVOKE;
14. membership visibility;
15. event provenance.

Inspect foreign keys, indexes, triggers and RPCs before designing anything.

If a canonical membership primitive exists under another name, reuse it.

If none exists, explicitly record:

**MEMBERSHIP CANONICALITY BLOCKED — NO EXISTING SUBSTRATE FOUND**

Then design the smallest possible canonical model; do not deploy until reviewed against the rest of the architecture.

Evidence required:
AUTH USER → MEMBER → PROFILE → SPACE → MEMBERSHIP.

Update:
- Your Connections;
- Smart Spaces;
- Job 04;
- Team Naya;
- this directive.

## ACTION 03 — CANONICAL RELATIONSHIP SUBSTRATE

Reconcile `v7_connection_requests`.

Inspect:
- migrations;
- source history;
- accepted/rejected states;
- functions;
- triggers;
- foreign keys;
- RLS;
- all references;
- Space membership relationship semantics.

Answer:
- request vs established connection;
- manual vs Space-derived origin;
- canonical CONNECTED;
- COMMUNICATION_ELIGIBLE;
- REVOKED;
- provenance;
- duplicate prevention;
- multi-origin merge;
- origin revocation behavior.

Do not create `connections` unless absence is proven.

## ACTION 04 — REAL JOIN

Bind the authenticated transaction:

AUTHENTICATE
→ CHECK SPACE VISIBILITY
→ AUTHORIZE JOIN
→ IDEMPOTENT MEMBERSHIP WRITE
→ EVENT
→ PROJECTION
→ RESPONSE.

Test:
- first join;
- duplicate join;
- unauthorized join;
- persistence after reload;
- event once;
- no private-data expansion.

## ACTION 05 — YOUR CONNECTIONS

Build only as a projection of canonical relationship state.

Prove:
- relationship appears;
- origin is correct;
- shared Space is correct;
- profile exposure is privacy-safe;
- current state is truthful;
- revoked relationship changes state.

No duplicate contact row.

## ACTION 06 — SMART LIST + SMART MAIL

Smart List:
- connection → List membership;
- persist;
- reload;
- remove;
- relationship survives.

Smart Mail:
- relationship eligibility;
- authority;
- send;
- receiver verification;
- replay/idempotency;
- attachment scope;
- revocation-at-use.

The server must reject an ineligible/revoked send.

## ACTION 07 — ACTIVITY + LEDGER

Use canonical event infrastructure.

Prove:
source action → event → Activity → Ledger/evidence where required.

Do not create UI-only events.

## ACTION 08 — TWO-USER ADVERSARIAL PROOF

Use real authenticated identities.

A:
- creates Space.

B:
- discovers;
- joins;
- verifies membership;
- verifies relationship;
- uses List;
- sends authorized Mail.

Then:
- revoke/leave;
- retry Mail;
- retry protected access;
- verify denial.

C:
- attempts unauthorized access.

Also test:
- reload;
- duplicate JOIN;
- duplicate relationship;
- message replay;
- stale client state;
- attachment authorization.

Record exact denial/error evidence.

## ACTION 09 — CLOUDFLARE SOURCE/BUILD/RUNTIME PARITY

Map:
source → build → artifact → deployment → route → deployed marker → browser.

Verify:
- authentication;
- Space;
- JOIN;
- Connections;
- List;
- Mail;
- Share;
- Activity;
- errors;
- unauthorized;
- revoked states.

No parity claim from GitHub alone.

## ACTION 10 — PRODUCTION CLOSURE

Update every affected feature:
- current state;
- checklist;
- evidence;
- blockers;
- next action;
- dated activity.

Update:
- Team Naya root;
- year/month/day indexes;
- subsystem job;
- master directive.

Closure requires complete evidence package and one cold-start successor directive.

---

# 25. DEFINITION OF DONE

The subsystem is LIVE VERIFIED only when:

### Identity
Canonical identity is proven and reused.

### Space
Real authenticated Space creation/discovery works.

### Membership
JOIN persists, is idempotent, authorized and revocable.

### Connection
Relationship derives from canonical state with provenance.

### List
Connections can be organized without owning relationship truth.

### Mail
Eligible people can communicate; ineligible/revoked users are denied.

### Share
Sharing is separately authorized.

### Activity
Canonical events produce truthful activity.

### Ledger
Consequential evidence is recorded.

### Privacy
Unauthorized users cannot see protected information.

### Two-user isolation
A and B are isolated correctly from unrelated C.

### Runtime
Cloudflare serves the proven source/build.

### Evidence
The full transaction can be reconstructed.

Anything less is IN PROGRESS / NOT VERIFIED.

---

# 26. PROOF REQUIREMENTS

For every claim, provide:

- exact actor;
- exact timestamp;
- exact environment;
- exact source commit;
- exact table/function/policy;
- exact request/action;
- expected result;
- observed result;
- evidence identifier;
- resulting state;
- failure/limitation.

Proof hierarchy:

**LIVE AUTHENTICATED RUNTIME > DATABASE/RLS OBSERVATION > SOURCE INSPECTION > DOCUMENTATION**

Documentation can define intent but cannot prove runtime.

---

# 27. FAILURE / DEBUGGING LAW

When something fails:

**OBSERVED FAILURE**
→ **EXACT BOUNDARY**
→ **SOURCE OF TRUTH**
→ **ROOT CAUSE**
→ **SMALLEST CORRECT CHANGE**
→ **RERUN SAME PROOF**
→ **RECORD RESULT**

Rules:

- no blind retries;
- no random edits;
- no weakening security;
- no bypassing RLS;
- no replacing production state with local state;
- no declaring success after a partial path;
- no hiding blockers;
- no creating a duplicate primitive to avoid understanding an existing one.

---

# 28. EVIDENCE REQUIREMENTS

Each substantive session must record:

1. actor;
2. session timestamp;
3. feature;
4. mission;
5. files inspected;
6. files changed;
7. commit SHA;
8. database objects inspected;
9. database objects changed;
10. functions/versions;
11. RLS policies;
12. exact authenticated test;
13. observed result;
14. expected result;
15. evidence/receipt/event IDs;
16. blockers;
17. unresolved questions;
18. current state;
19. next master directive.

---

# 29. TEAM NAYA UPDATE REQUIREMENTS

Every substantive engineering session must update the activity system before sign-out.

Required hierarchy:

**YEAR → MONTH → DAY → SUBSYSTEM/FEATURE → SESSION**

Required session report:

## DONE
What actually changed.

## PROOF
What actually passed and how.

## NOT PROVEN
Every remaining uncertainty.

## DECISION
Canonical ownership decisions.

## BLOCKERS
Exact blockers.

## NEXT
A complete master execution directive.

Never write “continued progress.”

Never close a session without updating the feature record when feature state changed.

---

# 30. HANDOFF REQUIREMENTS

A cold-start Naya must be able to execute without the previous conversation.

The handoff must contain:

- mission;
- why;
- system context;
- current state;
- completed work;
- proven evidence;
- unproven boundaries;
- source of truth;
- architecture;
- production objects;
- security;
- privacy;
- data/event/Ledger model;
- UI requirements;
- backend requirements;
- runtime requirements;
- deployment requirements;
- integration dependencies;
- non-goals;
- risks;
- gaps;
- exact execution sequence;
- ten actions;
- Definition of Done;
- proof requirements;
- failure law;
- evidence law;
- Team Naya law;
- final acceptance test;
- immediate next action.

No two-sentence continuation is acceptable.

---

# 31. FINAL ACCEPTANCE TEST

The final end-to-end proof is:

### A — HUMAN A
Authenticate.

### B — SPACE
Create a real Space.

### C — ACTIVITY
Observe the Space creation consequence.

### D — HUMAN B
Authenticate as a distinct real user.

### E — DISCOVERY
B discovers the Space through an authorized path.

### F — JOIN
B performs JOIN.

### G — MEMBERSHIP
Server proves B is a member.

### H — CONNECTION
The canonical relationship state is derived/proven.

### I — CONNECTIONS
B/A relationship appears in Your Connections according to policy.

### J — LIST
Connection is added to Smart List and survives reload.

### K — MAIL
Authorized communication succeeds through the real Smart Mail path.

### L — SHARE
If intelligence is shared, Smart Share authorization is independently proven.

### M — ACTIVITY
The canonical event is observable.

### N — LEDGER
Consequential evidence is recorded where contracted.

### O — REVOCATION
B leaves or relationship authority is revoked.

### P — RECHECK
Mail/access is attempted again.

### Q — DENIAL
The server denies the now-ineligible action.

### R — UNAUTHORIZED C
A distinct unauthorized user attempts protected operations and is denied.

### S — REPLAY
Repeated requests do not duplicate state.

### T — CLOUDFLARE
The same proven behavior is observed in the deployed Cloudflare runtime.

Only after A→T passes may the subsystem be called:

**LIVE VERIFIED**

---

# ACTION 02 CLOSURE — 2026-09-19

## DONE

Identity and Space-membership reconciliation is complete against live production schema/RLS/functions/migrations, Smart Mail v12 and the canonical Hub source.

## PROOF

- `auth.users.id = members.id`; 291/291 with zero unmatched.
- `nayanet_profiles.member_id = members.id`; 83 populated profiles.
- `v7_profiles` has 0 rows.
- `nayanet_spaces.owner_member_id = members.id`; one live Space.
- Space visibility is `private|shared`; owner-only RLS.
- No dedicated Space membership/participant table exists in the live public schema.
- No Space JOIN/LEAVE/INVITE function exists in the live Space function inventory.
- `v7_mail_members` is thread membership only.
- Hub source is visual baseline, not wired runtime proof.

## NOT PROVEN

JOIN, membership persistence, participant visibility, connection establishment, revocation, List membership, relationship-gated Mail, two-user lifecycle, Cloudflare parity.

## DECISION

Canonical identity is `auth.users.id = members.id`. Canonical member is `public.members`. Canonical current profile is `public.nayanet_profiles`. Canonical Space is `public.nayanet_spaces`. No membership substrate exists.

**MEMBERSHIP CANONICALITY BLOCKED — NO EXISTING SUBSTRATE FOUND**

No schema change was deployed in Action 02.

## NEXT

Action 03 must reconcile `v7_connection_requests` before membership implementation.

# 32. IMMEDIATE ACTION 06

## ACTION 06 — SMART LIST + SMART MAIL RELATIONSHIP BINDING

**Status: IMMEDIATE EXECUTION**

### Mission

Reconcile the existing Smart List substrate, then bind it to canonical Connections without duplicating relationship state. At the same time, bind Smart Mail's send-time eligibility to the canonical relationship boundary while preserving the existing authority-grant requirement.

### Exact sequence

1. Inventory all live tables/functions/indexes/RLS matching List, Favorite, Saved, Collection, Group and person organization.
2. Determine whether an existing List primitive can be reused.
3. If absent, create the smallest owner-scoped List + membership model.
4. Make List membership reference canonical Connection/Member identity, never copied profile rows.
5. Implement idempotent add/remove and reload persistence.
6. Ensure removing a List entry does not revoke the Connection.
7. Inspect current Smart Mail v12 and `nayanet_send_smart_mail_authorized`.
8. Add relationship eligibility at use time without replacing authority validation.
9. Require an active shared Space or canonical Connection state according to the reconciled communication contract.
10. Preserve authority-grant validation, revocation-at-use and idempotency.
11. Test unauthorized relationship denial in a transaction.
12. Update Smart List, Smart Mail, Job 04, Team Naya and this master directive.
13. Finish with DONE / PROOF / NOT PROVEN / DECISION / BLOCKERS / NEXT.

### Hard rules

- Do not redesign the Hub.
- Do not replace `nayanet_authority_grants`.
- Do not make Connection equal authority.
- Do not copy identity/profile data into Lists.
- Do not allow a UI-only recipient to bypass server relationship checks.
- Do not call Smart Mail verified until the new relationship gate is proven.

### Success condition

A canonical Connection can be organized in Smart List, survives reload, and does not change relationship truth when removed from a List; Smart Mail rejects a recipient who lacks the required relationship boundary even if the client presents a callable recipient.

### Canonical execution prompt

See:
`NAYA-TEAM/2026/09/19/COMMUNICATION-ORGANIZATION/2026-09-19__ACTION-06-EXECUTION-PROMPT.md`
