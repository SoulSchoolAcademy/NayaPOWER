# 🔱 NayaNET Intelligent Hub — Room System

**Status:** PROPOSED FUNCTIONAL / DESIGN CONTRACTS · TEAM CONSENSUS REVIEW OPEN  
**Review PR:** #1290  
**Coordination board:** #554  
**Implementation owner:** #1270

## One shell. Eleven masterpieces. One Naya. One governed substrate.

The sidebar is navigation. **The center workspace is the room.**

Clicking a room does not replace the Hub with another disconnected page. The same shell, sidebar, Naya presence and global context remain while the center becomes a different intelligent software experience.

## Read first

1. [Human Director Google Drive source notes](./SOURCES/2026-10-01-HUMAN-DIRECTOR-GOOGLE-DRIVE-ROOM-NOTES.md)
2. [Consensus & Review Protocol](./CONSENSUS-PROTOCOL.md)
3. [Consensus Status](./CONSENSUS-STATUS.md)
4. [Room Package Standard](./_STANDARD/ROOM-PACKAGE-STANDARD.md)
5. [Room Review Checklist](./_STANDARD/ROOM-REVIEW-CHECKLIST.md)
6. [Shared Room Functional Contract](./ROOM-FUNCTIONAL-CONTRACT-V1.md)
7. [Aggregate Machine Contract](./ROOMS-MACHINE-V1.json)
8. [Room Specification Scorecard](./ROOM-SPEC-SCORECARD.md)

## Canonical room packages

| # | Room | Mental model | Package |
|---:|---|---|---|
| 01 | Smart Feed | **The Game** | [01-smart-feed/](./01-smart-feed/) |
| 02 | Your Intelligence Today | **The Highlight Reel** | [02-your-intelligence-today/](./02-your-intelligence-today/) |
| 03 | Your Reports | **The Film Room / Time Machine** | [03-your-reports/](./03-your-reports/) |
| 04 | Intelligent Library | **The Vault / Your Mind** | [04-intelligent-library/](./04-intelligent-library/) |
| 05 | Smart Connect | **The Portal Bay** | [05-smart-connect/](./05-smart-connect/) |
| 06 | Smart Ledger | **The Black Box / Proof Room** | [06-smart-ledger/](./06-smart-ledger/) |
| 07 | Your Connections | **The Constellation** | [07-your-connections/](./07-your-connections/) |
| 08 | Smart Lists | **The Mission Table** | [08-smart-lists/](./08-smart-lists/) |
| 09 | Smart Mail | **The Signal Room** | [09-smart-mail/](./09-smart-mail/) |
| 10 | Smart Spaces | **The Worlds / Context Environments** | [10-smart-spaces/](./10-smart-spaces/) |
| 11 | Settings | **The Control Deck** | [11-settings/](./11-settings/) |

Every package contains:

`README.md · FUNCTIONAL-SPEC.md · DESIGN-CONTRACT.md · SPEC.HUMAN.md · SPEC.AI.md · SPEC.MACHINE.json`

## Five-layer room law

Every room must express the Human Director's five layers:

1. **ORIENTATION** — Where am I?
2. **CURRENT STATE** — What is happening here right now?
3. **INTELLIGENCE** — What does Naya understand?
4. **ACTION** — What can I actually do?
5. **PROOF** — Why should I trust it?

Visual grammar can express this as:

**HERO → INTELLIGENCE WALL → ACTION DECK → EVIDENCE LAYER → NAYA LAYER**

but each room composes those pieces differently.

## Shared product hierarchy

**Smart Feed = the game.**  
**Your Intelligence Today = the daily highlight reel.**  
**Reports = meaning across time.**  
**Library = retained knowledge and retrieval.**  
**Ledger = proof beneath consequential activity.**  
**Connections / Mail / Spaces / Lists = relationships, communication, context and organization.**  
**Smart Connect = the governed connection layer into the wider world.**  
**Settings = human control over the relationship with NayaNET.**

## Universal capabilities, not extra primary rooms

- Search Intelligence
- Ask Naya
- Smart Note / Capture
- Save / Favorite
- Add to List
- Inspect Source / Evidence
- current Space context
- truth state

### IA reconciliation

Open PR #1278 currently exposes **Smart Notes** and **System** as additional primary rail rooms.

Current proposal:
- **Smart Notes** → universal capture capability + optional focused capture surface.
- **System** → `Settings → System Health` advanced surface.

The functionality is preserved; the primary navigation stays simple unless consensus explicitly changes it.

## Consensus law

These files are **reviewable project intelligence**, not immutable scripture.

If a reviewer sees a better approach:
1. comment on PR #1290;
2. post material not-right findings to #554 with evidence;
3. propose an improved contract;
4. score the impact;
5. reconcile rather than silently fork;
6. lock only after consensus/ratification.

## Build sequence

Do not half-build eleven rooms.

**YOUR INTELLIGENCE TODAY → exact states → exact data → interaction → implement → browser test → runtime test → persistence test → proof → then next room.**

The Today room is the reference masterpiece because it forces identity, retrieval, synthesis, evidence, Naya interpretation and cross-room action to work together.
