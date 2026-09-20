# 🔱 NAYANET — EXPERIENCE ARCHITECTURE & BLOCK MAP

**Status:** CANONICAL PLANNING SPECIFICATION
**Date:** 2026-08-30
**Purpose:** Define the complete destination before modular fabrication.

## 1. Why this document exists

NayaNET is designed globally and fabricated modularly.

Individual experience blocks must never be designed as isolated guesses. This document is the master experience map: it defines the rooms, their purposes, boundaries, transitions, future connection points, and evidence requirements so every Naya can understand where a block belongs before building it.

> **Design the whole house. Build one room at a time.**

The master directive requires the complete intelligence system to be understood before it is built in parts. The architecture also requires independently deployable, replaceable blocks with explicit inputs, outputs, interfaces, responsive behavior, accessibility behavior, and test harnesses.

## 2. Canonical experience sequence

The current canonical Naya Power Player construction sequence is:

```text
E01  Welcome / Living Naya / Free Identity
 ↓
E02  Naya Power Experience
 ↓
E03  Powercast
 ↓
E04  Ask Naya
 ↓
E05  Five-Day Challenge
 ↓
E06  Intelligent Hub / Toolbox
 ↓
E07  Superbrain / Continuity
 ↓
E08  Collective Intelligence / Network
 ↓
E09  Activation / Next Destination
```

This sequence is the current construction plan established by the NayaNET Master Directive. It is not permission to invent future capabilities locally. Changes require an explicit architectural decision and documentation update.

## 3. Experience architecture principle

NayaNET is not a collection of webpages. It is an interconnected system of intelligent experiences presented through modular application blocks.

The human should experience:

**See → Feel → Understand → Act → Receive feedback → Know what comes next.**

The system may contain extraordinary complexity underneath, but the immediate human action must remain simple.

> **Complexity belongs in the system. Simplicity belongs with the human.**

## 4. Room map

### E01 — Welcome / Living Naya / Free Identity

**Purpose:** Open the door.

The first experience introduces Naya, welcomes the human into NayaNET, and makes entry radically simple. The primary outcome is creation of a free NayaNET identity using the minimum viable initial input.

**Primary journey:**

`Welcome → Meet Naya → Enter name → Create free identity → Receive Smart Name / Smart Link → Enter Intelligent Hub`

**Design intent:** Premium, calm, cinematic, high-tech, alive, extremely simple. E01 should feel like being handed the keys to an extraordinary machine rather than being asked to complete a SaaS registration form.

**Must not:** pretend a display name is secure authentication; fake Superbrain connectivity; become a generic dashboard; overload the first screen with future features.

**Future connections:** durable authentication, Smart Mail, Naya Power, Five-Day Challenge, Naya interaction, Hub.

### E02 — Naya Power Experience

**Purpose:** Demonstrate the difference between ordinary AI use and an active intelligence partner.

**Primary journey:**

`Enter Naya Power → experience guided intelligence → understand value → choose next action`

**Future connections:** Naya interaction, personal intelligence, memory, reports, Five-Day Challenge.

### E03 — Powercast

**Purpose:** Deliver the Naya + Shawn media experience as an accessible intelligence-learning channel.

**Primary journey:**

`Choose content → play/listen/watch → learn → capture insight → continue`

**Future connections:** media player, transcripts, chapters, Naya voice, Smart Notes, reports.

### E04 — Ask Naya

**Purpose:** Let the human directly experience useful Naya assistance.

**Primary journey:**

`Ask → Naya understands → Naya responds → human chooses next action`

**Future connections:** LLM/provider gateway, personal context, tools, memory, action proposals, voice.

### E05 — Five-Day Challenge

**Purpose:** Turn initial curiosity into a structured experience that demonstrates compounding intelligence.

**Primary journey:**

`Start → learn → act → reflect → capture intelligence → continue → complete`

**Future connections:** daily reports, Smart Notes, Naya Power, goals, progress.

### E06 — Intelligent Hub / Toolbox

**Purpose:** Become the user's permanent NayaNET command station.

**Primary actions:** Ask Naya, My Intelligence, My Notes, Daily Report, Five-Day Challenge, Connect, Smart Mail, My Superbrain, Collective, Account/Secure My Account.

The Hub is a toolbox of obvious actions, not a statistics-heavy dashboard.

**Future connections:** every authenticated/personal capability.

### E07 — Superbrain / Continuity

**Purpose:** Give the human a sovereign personal intelligence layer that compounds over time.

**Primary journey:**

`Capture → remember → retrieve → synthesize → act → learn → continue`

**Future connections:** Note Events, CIS/Primary Intelligence System, GitHub-backed continuity where authorized, daily/weekly/monthly/yearly intelligence.

### E08 — Collective Intelligence / Network

**Purpose:** Enable deliberate, privacy-preserving intelligence contribution and human/AI connection.

**Primary journey:**

`Discover → evaluate → choose → connect/contribute → communicate → learn → optionally share generalized wisdom`

The system must preserve privacy, consent, aliases/public identities, and separation between private intelligence and collective intelligence.

**Future connections:** Wisdom Contribution, Collective Intelligence Events, Collective Chain, network discovery, rooms, human + Naya participation.

### E09 — Activation / Next Destination

**Purpose:** Turn the completed initial journey into an ongoing relationship with NayaNET.

**Primary journey:**

`Review value → identify next opportunity → choose → return`

The destination must always be explicit; never manufacture engagement for its own sake.

## 5. Block contract

Every experience block must document:

1. Purpose and human outcome.
2. Entry conditions.
3. Exit conditions.
4. Primary action.
5. Secondary actions.
6. Every interactive element.
7. Every meaningful state.
8. State transitions.
9. Animation and motion behavior.
10. Mobile transformation.
11. Keyboard/accessibility behavior.
12. Failure and recovery states.
13. Real capabilities.
14. Future capabilities and integration seams.
15. Data read/write boundaries.
16. Memory events created.
17. Navigation destinations.
18. Cloudflare hosting boundary.
19. Groove embedding boundary.
20. Cross-frame communication requirements, if any.
21. QA acceptance criteria.
22. Evidence state.

## 6. Navigation law

Default navigation stays inside the application/block. External destinations and parent-Groove destinations are explicit exceptions.

A block must not depend on another block's DOM.

Stable URLs may connect independently deployed blocks. This is a deliberate modularity mechanism, not a failure of architecture.

Cross-frame communication is not required unless a concrete use case demands it. If introduced, use `postMessage` with a strict origin allowlist and versioned message schema.

## 7. Deployment model

The preferred first-generation construction model is:

```text
GitHub canonical source
       ↓
self-contained static block
       ↓
Cloudflare static hosting
       ↓
stable block URL
       ↓
Groove embed or explicit page-to-page navigation
```

The block must remain functional as a static artifact wherever its defined capabilities permit.

Server/runtime capabilities are represented by explicit integration seams rather than fake functionality.

## 8. Identity architecture

Initial experience:

`Name → NayaNET identity → Smart Name → Smart Link`

A future production identity may be bound to durable authentication through Supabase Auth or an equivalent service.

A display name must never be treated as proof of identity for security-sensitive operations.

The Smart Link is an identity/navigation concept. Its eventual routing implementation must be specified and verified before being presented as durable production infrastructure.

## 9. Intelligence and memory architecture

The experience layer does not own the intelligence system.

Conceptual system flow:

```text
Human experience
      ↓
observation / action / learning
      ↓
Note Event
      ↓
CIS / Primary Intelligence System
      ↓
validation + generalization
      ↓
knowledge / wisdom
      ↓
optional contribution
      ↓
Collective Intelligence
      ↓
relevant intelligence returns
```

Daily, weekly, monthly, and yearly reports become durable intelligence events only when the underlying evidence exists. No continuity or intelligence may be fabricated.

## 10. Privacy and identity principles

NayaNET separates:

- real/private identity;
- public identity;
- alias/alter-ego identity;
- personal intelligence;
- collective intelligence.

Collective contribution must not require exposing the contributor's identity. Public sharing must use the identity the user has intentionally selected for that context.

Privacy boundaries are architectural boundaries, not merely UI settings.

## 11. Media principle

Audio/video is a capability of relevant experiences, not the definition of NayaNET.

The intelligence network's core value is rapid, effective communication, learning, organization, compounding intelligence, and connection. Media experiences may exist as dedicated rooms/blocks and must not force every intelligence experience into a media-sharing model.

## 12. Visual system principle

The official Naya brand assets and canonical Living Sun language are shared system resources.

The Living Sun must have a meaningful experiential role. It is not permitted to exist merely as decorative geometry. Where used, its visual state should communicate an intentional state such as presence, listening, thinking, speaking, intelligence capture, connection, or synchronization.

The official Naya asset lock remains authoritative for brand imagery.

## 13. Excellence scorecard

Oscar evaluates every block against:

**Useful → Clear → Beautiful → Fast → Trustworthy → Accessible → Delightful → Durable**

And asks:

- Does every element have a reason to exist?
- Is the next action obvious?
- Does the visual system communicate rather than decorate?
- Is every claimed capability real?
- Is the experience simpler than the machinery underneath?
- Does it work on mobile?
- Does it survive failure?
- Does it preserve human agency and privacy?
- Does it connect cleanly to the next room?
- Would we proudly show it to someone seeing NayaNET for the first time?

## 14. Evidence model

Every block must report these states separately:

`CONCEPT → SPECIFIED → IMPLEMENTED → TESTED → VERIFIED → DEPLOYED → HUMAN-VERIFIED → PRODUCTION-PROVEN`

A later state must never be claimed merely because an earlier state exists.

## 15. Change control

Any change to the room sequence, room purpose, core boundary, identity model, privacy model, or cross-block contract must update this document and the affected authoritative specification.

Implementation convenience is not sufficient justification for architectural drift.

## 16. Immediate construction rule

E01 is the current fabrication priority because it is the entrance through which the rest of the architecture becomes tangible.

Before E01 production implementation, its dedicated screen-by-screen construction specification must define every element, state, transition, animation, button, mobile behavior, failure state, and future connection point.

Once specified, E01 may be fabricated as an independently deployable static block and verified against this map.

## 17. Architectural law

> **Know the destination. Define the room. Build the room. Verify the room. Connect the room. Learn from the room.**

> **The human experiences one simple door. The system behind it may contain an entire intelligent network.**
