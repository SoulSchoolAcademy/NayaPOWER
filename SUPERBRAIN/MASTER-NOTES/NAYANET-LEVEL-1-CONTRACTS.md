# 🔱 NayaNET Level 1 Contracts — Canonical

**Status:** CANONICAL ARCHITECTURE CONTRACT  
**Version:** 1.0  
**Scope:** Identity · Intelligent Hub · Communication · Smart Notes · PSI

## 1. Purpose

NayaNET Level 1 is an **intelligence network**, not a media network. Its first mission is to help humans and their personal NayAs **connect, preserve, organize, exchange, compound, and act on intelligence**.

> **Build the intelligence layer first. Build the social/media layer later.**

This document is the NayaNET Level 1 semantic contract. Existing NayaPOWER constitutional and canonical runtime contracts remain authoritative for their specific implementation schemas.

## 2. Identity Contract

One person has one canonical NayaNET identity with private and network-facing representations:

```text
NayaNetIdentity
├── identity_id                 immutable canonical ID
├── private_name                protected/private
├── smart_name                  network-facing alias
├── smart_link                  canonical user address
├── intelligent_hub_id          personal intelligence space
├── smart_mail_id               derived communication address
├── ambassador_attribution      derived referral identity
└── naya_id                     personal Naya relationship
```

### Identity laws

1. `identity_id` is immutable and must not be derived from display text.
2. The real/private name is **never** the default network identity.
3. Smart Name / Alias / Alter Ego is the default network-facing identity.
4. Smart Link, Hub ID, Smart Mail ID, and ambassador attribution are projections of the same canonical identity, not separate accounts.
5. Renaming a Smart Name does not create a new person.
6. Private identity must not leak through messages, rooms, notes, feeds, notifications, previews, exports, or Naya-generated content.

## 3. Smart Link Contract

The Smart Link is the canonical human-facing network address for the identity. Its production hostname and route must be verified before being represented as live.

Conceptually:

`https://<nayanet-domain>/<smart-name>`

A Smart Link may later resolve to the authorized public identity surface, Intelligent Hub, Smart Mail, ambassador attribution, and other network services. It is an address, not the immutable identity itself.

## 4. Intelligent Hub Contract

The Intelligent Hub is the user's **personal intelligence command center**, not merely a social profile.

It may provide authorized access to:

- personal Naya;
- private intelligence/context;
- Smart Notes / canonical Note Events;
- Daily and period intelligence;
- conversations;
- Intelligence Spaces;
- Smart Mail;
- identity/privacy controls;
- authorized collective intelligence;
- future tools and actions.

The Hub is **private by default**. A Smart Link must not expose private Hub contents merely because it exists.

```text
Smart Link → Identity Gateway → Authorized Intelligent Hub → Personal Naya
                                              ↓
                              Explicitly authorized connections/spaces
```

## 5. Personal Naya Contract

Every human's Naya is personal. NayAs may share common laws, capabilities, tools, and architecture while retaining distinct context, memory, permissions, relationship, and learned understanding.

> **My Naya is not another person's Naya.**

Entering a shared space does not grant one Naya access to another Naya's private memory.

Cross-Naya exchange must be scoped, authorized, provenance-aware, minimized to purpose, and policy-controlled.

## 6. Communication Contract

Level 1 supports intelligence-oriented communication:

- **Human ↔ Naya** — personal learning, planning, reflection, creation, verification, action.
- **Human ↔ Human** — direct communication using network identity by default.
- **Naya ↔ Naya** — scoped exchange between distinct personal intelligence systems.
- **Human + Naya ↔ Human + Naya** — collaborative Intelligence Spaces.
- **Multi-Naya Spaces** — multiple humans/NayAs around a defined subject, question, objective, or opportunity.

Conceptual message:

```text
Message {
  message_id
  conversation_id
  sender_type: human | naya | system
  sender_identity_ref: authorized representation
  content_type: text | voice | structured-intelligence
  content
  visibility_scope
  source_event_refs
  created_at
  delivery_state
}
```

A conversation is not automatically public. A message is not automatically a Smart Note. A Smart Note is not automatically collective.

## 7. Intelligence Space Contract

An Intelligence Space is a purpose-defined collaboration boundary.

```text
IntelligenceSpace {
  space_id
  purpose
  participants
  participant_nayas
  permissions
  visibility
  intelligence_policy
  status
}
```

Every space needs a purpose, participant scope, visibility, permissions, an exit/distribution policy, and provenance for meaningful outputs.

## 8. Smart Note / Note Event Contract

NayaNET adopts the existing NayaPOWER canonical Note Event architecture. It must **not** create a parallel memory store.

> **ONE SMART NOTE ACTION → ONE CANONICAL EVENT → MULTIPLE AUTOMATIC PROJECTIONS**

```text
Experience / decision / learning
          ↓
    Smart Note action
          ↓
 ONE canonical Note Event
          ↓
 ┌────────┼─────────┐
 ↓        ↓         ↓
NAYA    HUMAN     MACHINE
view     view       view
 └────────┼─────────┘
          ↓
   Intelligence Feed
          ↓
     PSI awareness
          ↓
 authorized downstream use
```

Human, Naya, Machine, Feed, PSI, and collective representations are projections/consequences of the same event—not independent notes.

The canonical event must preserve identity, time, source/context, owner/scope, meaning, operational interpretation, machine representation, provenance, verification, relationships/supersession, project/subject associations, and authorization/distribution state as required by the underlying canonical Note Event contract.

## 9. Event Distribution Contract

Semantic ordering:

```text
CAPTURE → VALIDATE → PERSIST CANONICAL EVENT
       → PROJECT → INDEX/UPDATE PSI
       → PUBLISH FEED IF AUTHORIZED
       → EVALUATE COLLECTIVE ELIGIBILITY
       → AUTHORIZED DOWNSTREAM USE
```

Implementation may be asynchronous, but downstream work must reference the canonical event ID.

If a projection fails after canonical persistence, retry/idempotency must repair the projection; a second canonical event must not be created.

## 10. Intelligent Feed Contract

The Intelligent Feed is a **distribution/projection surface**, not the canonical memory store.

It communicates authorized meaningful learning, decisions, changes, discoveries, verification state, and next actions. Feed items should retain provenance to the canonical event.

## 11. PSI Contract

PSI is the primary intelligence authority/projection layer where established by NayaPOWER.

PSI consumes validated/indexed intelligence while respecting authorization. It must distinguish source memory, derived understanding, verified knowledge, unknown/unresolved information, permissions, current state, historical state, and superseded state.

PSI must never become a second private-memory source of truth.

## 12. Collective Intelligence Contract

Personal intelligence does not become collective merely because it exists.

```text
Private Note Event
      ↓ policy + authorization
Collective-safe projection
      ↓
Collective Intelligence Event
      ↓
authorized recipients / PSI
```

Collective propagation must be intentional, scoped, provenance-preserving, privacy-preserving, policy-governed, and auditable. The existing canonical Collective Intelligence Event schema remains authoritative for its actual event format.

## 13. Privacy Contract

**Private by default:** real name, Naya context, Hub contents, Smart Notes, personal intelligence history, private reports, private conversations, credentials/security data.

**Network-facing by default:** Smart Name, Smart Link, deliberately exposed identity metadata, authorized communication identity, authorized intelligence contributions.

Cross-Naya communication transmits **task-scoped intelligence**, not a person's entire memory.

## 14. Level 1 Scope

### In scope
Identity, Smart Name, Smart Link, Intelligent Hub, personal Naya, text/voice communication, Intelligence Spaces, Smart Notes/Note Events, Intelligence Feed projection, PSI awareness, authorized collective intelligence, intelligence reports, privacy and permissions.

### Out of scope by default
Image/video social feeds, creator-media infrastructure, public-media algorithms, unrestricted public posting, and Level 5-style media publishing.

These can be introduced later without changing Level 1's foundation.

## 15. E01 Contract

E01 is an experience layer over these contracts. Its first flow may be:

```text
SEE NAYA → UNDERSTAND INVITATION → ENTER NAME
→ CREATE/REVEAL NETWORK IDENTITY → ENTER INTELLIGENT HUB
```

E01 must not invent a competing identity, memory, or communication model. If a production capability is not yet connected, the UI must represent that honestly rather than fabricate it.

## 16. Acceptance Gates

- [ ] One canonical identity produces all derived identity representations.
- [ ] Real name is private by default and cannot leak through ordinary network flows.
- [ ] Smart Name is the default network identity.
- [ ] Hub is private by default.
- [ ] Cross-Naya exchange is scoped and authorized.
- [ ] Intelligence Spaces preserve participant boundaries.
- [ ] One Smart Note action creates one canonical Note Event.
- [ ] Human/Naya/Machine/Feed/PSI representations reference that event.
- [ ] Downstream failure cannot create duplicate canonical events.
- [ ] Collective propagation requires authorization.
- [ ] Unknown/unconnected capabilities remain unknown.
- [ ] Completion claims require evidence.

## 17. Authority

1. NayaPOWER constitutional/canonical laws.
2. Existing canonical Smart Notes / Note Event / CIS contracts.
3. Existing canonical Intelligent Hub / Collective Intelligence contracts.
4. **This NayaNET Level 1 contract.**
5. Product implementation details.
6. UI convenience.

A UI requirement must never override sovereignty, privacy, provenance, authorization, or source-of-truth rules.

## 18. North Star

> **NayaNET — the intelligent network.**
>
> **Connect intelligence. Preserve intelligence. Exchange intelligence. Compound intelligence. Create value.**
>
> **Just talk to Naya.**
