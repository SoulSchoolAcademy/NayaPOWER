# JOB 04 — COMMUNICATION + ORGANIZATION SUBSYSTEM

## Mission

Own the connected relationship/communication subsystem across four human-facing surfaces:

- **Your Connections = WHO**
- **Smart Spaces = WHERE**
- **Smart List = HOW I ORGANIZE**
- **Smart Mail = HOW I COMMUNICATE**

Smart Share remains the cross-cutting controlled sharing boundary.

Do not build four disconnected systems.

## Canonical lifecycle

`DISCOVERY → SPACE → JOIN → MEMBERSHIP → CONNECTION → COMMUNICATION / LIST → ACTIVITY → LEDGER`

Reversal:

`LEAVE / REVOKE → RELATIONSHIP RECALCULATION → COMMUNICATION / ACCESS DENIAL`

## First law

**Do not create a contact/relationship table until the existing identity, profile, Space membership, Mail, List and event primitives have been inspected.**

The first job is reconciliation, not invention.

## Required inspection

Inspect:

1. canonical authenticated identity/profile;
2. existing Space object and membership primitives;
3. existing connection/relationship primitives, if any;
4. current Smart Mail recipient eligibility and messaging primitives;
5. current Smart List person/membership primitives, if any;
6. existing Activity/event writes;
7. authority/privacy/revocation functions;
8. current Hub source regions for Spaces, Mail, Lists and people;
9. Supabase live objects/functions;
10. Cloudflare source/build/runtime path.

## Relationship semantics

Lock these distinctions into implementation:

- interest ≠ membership;
- discovery ≠ membership;
- membership ≠ connection;
- connection ≠ unrestricted communication;
- communication ≠ intelligence access;
- membership ≠ private-data access;
- connection ≠ sharing authority.

A person may be surfaced as relevant from authorized signals, but relevance never silently creates membership or sends a message.

## Smart Space boundary

A Smart Space is the primary shared-context boundary where relationships can form.

Primary action:

**JOIN THE CONVERSATION**

Secondary action:

**INVITE PEOPLE**

Joining establishes participation in the Space's defined relationship boundary. It does not grant unrelated private data or intelligence access.

A Space creation should produce the expected Activity projection. Relevant people may be surfaced through authorized discovery signals, but Naya must not expose their private signals or contact them without authority.

## Connection boundary

When the governing Space contract permits, active shared membership can make a relationship eligible for Your Connections.

The connection projection must retain provenance:

who → whom → relationship source → Space/context → time → state → authority.

It must resolve to canonical identity and never copy a second person/contact record.

## Communication boundary

At message/send time, verify:

authenticated actor → recipient identity → relationship/Space eligibility → communication policy → current revocation → intelligence attachment authorization → idempotency/replay.

Connection does not automatically equal unrestricted messaging.

## Organization boundary

Smart List may contain both canonical intelligence and people/connections.

List membership references canonical identity/relationship state. It does not copy profiles or relationship records.

Removing a person from a List does not remove the connection.

## Activity / Ledger boundary

Relationship and communication events use the existing canonical event substrate.

Activity is a projection.

Smart Ledger receives consequential evidence according to its existing contract.

Do not create a second relationship event store merely to power UI.

## Verification sequence

1. Authenticated A creates a real Space.
2. Verify Space creation Activity.
3. Authorized B discovers the Space through the permitted path.
4. B joins.
5. Verify membership persistence after reload.
6. Verify connection eligibility/creation exactly once.
7. Verify permitted relationship information for A/B.
8. Verify eligible Mail/message action.
9. Verify List organization without identity duplication.
10. Verify Activity and consequential Ledger evidence.
11. B leaves/revocation occurs.
12. Verify communication/access denial where required.
13. Verify unauthorized/non-member isolation.
14. Verify source → build → Cloudflare deployed runtime parity.

## Failure law

If any link is missing:

**OBSERVED → DIAGNOSED → SMALLEST CHANGE → RERUN → VERIFIED / BLOCKED**

Do not substitute demo state, browser-local state, fabricated users, or documentation claims for production proof.

## Deliverables

- canonical relationship mapping;
- smallest implementation path;
- Your Connections surface;
- Space membership/Join connection;
- Mail/message eligibility connection;
- List/person connection;
- Activity projection connection;
- Ledger/evidence connection where applicable;
- authenticated two-user proof;
- revocation proof;
- Cloudflare parity proof;
- updated feature records and immutable Team Naya session.

## Current state

Architecture is defined. Runtime relationship lifecycle is not yet proven.

## One next action

**Inspect the live identity/profile, Space membership, Mail eligibility, List membership and canonical event primitives and document the smallest existing substrate that can carry JOIN → MEMBERSHIP → CONNECTION → COMMUNICATION → LIST → ACTIVITY → LEDGER without a duplicate contact store.**


## ACTION 02 RECONCILIATION — 2026-09-19

**Canonical identity proven:** `auth.users.id = members.id` (291 auth users, 291 members, zero unmatched).

**Canonical profile selected:** `nayanet_profiles.member_id → members.id` (83 populated rows). `v7_profiles` currently has 0 rows and is not the populated relationship profile substrate.

**Canonical Space proven:** `nayanet_spaces`, owned by `owner_member_id → members.id`, visibility `private|shared`, owner-only RLS.

**Membership result:** **MEMBERSHIP CANONICALITY BLOCKED — NO EXISTING SUBSTRATE FOUND.** No dedicated Space membership/participant table or Space JOIN/LEAVE/INVITE function exists in the live public production inventory. `v7_mail_members` is thread membership and must not be reused as Space membership.

**Hub result:** the canonical Hub HTML is a visual baseline; it contains Connections/Smart Mail UI but no direct Supabase/auth/Space/Mail runtime wiring. UI labels are not runtime proof.

**Implementation rule:** do not introduce membership until Action 03 reconciles `v7_connection_requests` and defines the canonical relationship state/provenance. No production schema was changed in Action 02.

## ACTION 03–05 EXECUTION STATE — 2026-09-19

### Relationship reconciliation
`v7_connection_requests` is confirmed request-only state. It does not become the durable Connection object.

### Membership
`nayanet_space_members` is now canonical for Space participation. JOIN/LEAVE are authenticated server RPCs with event lineage.

### Connections
`nayanet_connections` is now canonical for explicit saved relationships. It requires active shared Space participation and preserves source Space provenance.

### Security boundary
Membership and Connection are relationship state. They do not grant Smart Mail authority. Smart Mail must continue to validate authority at use time.

### Remaining work
Wire the current Hub to these primitives, implement Smart List, bind Mail relationship eligibility, prove two real users, and prove Cloudflare parity.


## FINAL CURRENT STATE — 2026-09-19

**IMPLEMENTED / SOURCE-PROVEN / CLOUDFLARE-PARITY-PROVEN / FINAL HUMAN BROWSER PROOF PENDING**

Canonical production primitives now exist for Identity → Space → Membership → Connection → Smart List → Smart Mail relationship gating → Activity/Ledger lineage.

The final blocker is strictly the real two-user authenticated browser acceptance proof. Do not mark Job 04 COMPLETE until that proof passes.


## ACTION 10 LIVE CLOSURE UPDATE — 2026-09-19

### DONE
- Authenticated A session reached the deployed Cloudflare Hub.
- Real shared Space created: `04ee4dc8-bc73-47df-a1de-162570f6a56e`.
- Space creation Ledger evidence: `294b64e3-f77c-465a-855a-79ae613b5b7e`.
- Production `nayanet_space_members` RLS recursion found during live context retrieval and fixed by migration `20260919172900_fix_space_members_rls_recursion`; source commit `a59cf18cf8c735307b6388c6f2dc9fa695b4dec8`.

### PROOF
- Post-fix Space context retrieval succeeds on the live Cloudflare Hub.
- Owner membership exists and is active.

### NOT PROVEN
- Distinct B authentication, JOIN, mutual Connection, Smart List, authority, real receiver Mail verification, replay, revocation denial, unrelated C denial.

### STATUS
**IMPLEMENTED / SOURCE-PROVEN / CLOUDFLARE-PARITY-PROVEN / A LIVE-PROVEN / FINAL HUMAN A+B PROOF PENDING**
