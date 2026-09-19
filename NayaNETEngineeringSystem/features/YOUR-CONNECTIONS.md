# Your Connections — Engineering Specification

## What / why

Your Connections is NayaNET's human-facing relationship layer. It answers **WHO am I connected with?** It is not a contact dump and it is not a message transport.

The canonical relationship model is created through shared context, especially Smart Space participation:

**DISCOVERY / RELEVANCE → SPACE → JOIN / MEMBERSHIP → RELATIONSHIP → CONNECTION → AUTHORIZED COMMUNICATION / ORGANIZATION**

A connection is a durable relationship projection derived from an authorized relationship context. It resolves to canonical identity and must not create a duplicate person/contact record.

## Core rule

**Interest may create discovery. Membership may create relationship. Relationship may enable communication. Authority determines what communication is permitted.**

Therefore: interest ≠ membership; discovery ≠ membership; membership ≠ connection; connection ≠ unrestricted communication; communication ≠ intelligence access; connection ≠ sharing authority; membership ≠ private-data access.

A person must not be contacted merely because Naya inferred relevance.

## Human experience

A human can discover a relevant Smart Space, inspect its topic and participation boundary, join it, become connected through the permitted relationship context, organize eligible connections, communicate with eligible connections, discover shared Spaces, and leave/revoke a relationship where permitted.

**JOIN** is the primary discovery-to-participation action. **INVITE** is optional, not the default relationship mechanism.

## Relationship lifecycle

`DISCOVER → VIEW → JOIN → MEMBERSHIP ACTIVE → CONNECTION ELIGIBLE → CONNECTION ESTABLISHED → COMMUNICATE / ORGANIZE → OBSERVE → REVOKE / LEAVE`

The system preserves the causal source of the relationship, especially shared Smart Space membership.

## Front end requirements

- Your Connections index and person/connection detail.
- Connection origin/context, especially shared Spaces.
- Search/filter.
- Add/remove from Smart Lists.
- Mail/message actions only when eligibility is true.
- View shared Spaces where visibility permits.
- Truthful relationship state: discovered / member / connected / communication eligible / revoked.
- Empty/loading/error/unauthorized states.
- No private attributes exposed merely because a person is discoverable.

## Back end requirements

- Resolve humans through canonical authenticated identity/profile primitives.
- Resolve relationship through canonical Space membership and future authorized relationship primitives.
- Enforce actor, scope, visibility and revocation at use time.
- Emit relationship events through the existing canonical event substrate.
- Project connection views without duplicating identity records.
- Make relationship mutations idempotent.
- Preserve provenance: who, whom, source relationship, source Space/context, time, authority and resulting state.
- Do not create a parallel contact database.

## Conceptual data contract

Until runtime mapping is complete, the conceptual relationship is:

`connection(actor_id, subject_id, relationship_state, source_type, source_id, visibility, created_at, updated_at, revoked_at, provenance_ref)`

This is a relationship projection, not a replacement for identity/profile, Space membership, authority grants, messages, intelligence objects or Smart List membership. Exact production names must follow existing implementation.

## Canonical cross-feature flow

`Smart Space created → activity event → relevant discovery projection → human views Space → JOIN → membership persists → relationship/connection eligibility → connection projection → Smart List organization → Smart Mail/message eligibility → communication event → Ledger/evidence where consequential`

Reversal:

`LEAVE / REVOKE → relationship eligibility recalculated → communication eligibility recalculated → protected access denied → projections update`

## Smart Space interaction

A Space may support Join the conversation, Invite people, live/instant interaction, posts, comments/replies, authorized intelligence sharing, Smart Mail actions, and participant-to-connection actions.

Joining establishes participation in the Space's defined relationship boundary. It does not silently grant unrelated private data or intelligence access.

## Smart List relationship

Smart Lists can organize canonical intelligence and people/connections. List membership references canonical identity/connection state; it does not copy profile data. Removing a person from a List does not remove the connection. Removing a connection does not delete the person or Space history.

## Smart Mail / messaging relationship

`CONNECTION ≠ MESSAGE DELIVERY`

At use time, communication must verify authentication, recipient identity, relationship/Space eligibility, communication policy, current revocation, intelligence-attachment authorization, and replay/idempotency rules.

## Activity + intelligence

Relevant relationship events may appear in Activity: Space created, Space discovered, person joined, connection established, meaningful interaction, and connection removed/revoked. Activity remains a projection of canonical events, not a relationship database. Consequential events enter Smart Ledger only according to its existing contract.

## Privacy and authority

**Private by default • Shared by choice • Collective by consent • Public by decision.**

Naya may surface relevant Spaces or candidates from authorized signals, but must not reveal private signals to the candidate, contact a person without communication authority, infer consent from topic similarity, turn interest into membership, or turn membership into unrestricted data access.

## Verification

Minimum proof: authenticated A creates Space → activity appears → authorized B discovers → B joins → membership persists → connection eligibility is created exactly once → permitted relationship information is visible → eligible communication becomes available → Smart List organizes the connection without duplication → consequences are recorded → B leaves/revocation occurs → communication/access is denied where required → unauthorized users cannot obtain the same relationship/protected content → Cloudflare source/build/runtime parity is proven.

## Current state

**DEFINED — ARCHITECTURE ESTABLISHED, RUNTIME UNPROVEN.**

The model is grounded in existing Smart Space, identity/privacy, Smart Mail and Smart List contracts. No new relationship/contact store should be created until runtime inspection is complete.

## Gap / next action

Inspect live identity/profile, Space membership, Mail eligibility, List membership and canonical event primitives. Select the smallest existing substrate for **JOIN → MEMBERSHIP → CONNECTION → COMMUNICATION → LIST → ACTIVITY → LEDGER**.

## Source authority

Existing Smart Space, identity/privacy/publication, Smart Mail and Smart List contracts. No new `.naya` authority is invented by this specification.

## COMPLETION CHECKLIST — 2026-09-19

- [x] Relationship semantics defined
- [x] Existing cross-feature contracts mapped conceptually
- [ ] Live identity/profile primitive mapped
- [ ] Live Space membership primitive mapped
- [ ] Canonical relationship persistence identified
- [ ] Communication eligibility mapped
- [ ] List/person membership mapped
- [ ] Authenticated two-user lifecycle proven
- [ ] Revocation proven
- [ ] Source → build → runtime parity proven
- [x] Dated activity record exists
- [x] One next action recorded

**Current state:** DEFINED — ARCHITECTURE ESTABLISHED, RUNTIME UNPROVEN.
