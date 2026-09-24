# 🔱 NayaNET System Update — HUB Is the House

**Date:** 2026-09-24  
**Status:** ACTIVE SYSTEM DIRECTION / CANONICAL ALIGNMENT

## The simplest possible model

NayaNET is a house.

- **NayaPOWER / Superbrain** = the governed intelligence and operating system behind the house.
- **NayaNET Intelligent Hub** = the house itself — the human-facing application and action surface.
- **The Hub rooms** = the capabilities humans actually use: Intelligence Today, Feed, Reports, Library, Smart Lists, Smart Mail, Contacts, Smart Spaces, Dream, Smart Ledger, Naya Play, Settings, and the connection/participation surface.
- **Smart Connect** = the doors into the house. The seven technical doors are GitHub App, MCP, REST/OpenAPI, Webhooks, SDK, A2A, and MCP Apps.
- **Welcome / Identity** = the future front door and identity entry sequence. They are not the current production application boundary and must not be treated as a finished login-to-Hub flow.

## What we are ultimately building

The objective is a working, governed NayaNET where a human can enter the Intelligent Hub, understand their intelligence, learn automatically, connect through governed doors, contribute useful wisdom by participation consent, protect their private intelligence/activity/identity by default, and use Naya to turn intelligence into useful action.

The system must compound intelligence without sacrificing truth, privacy, consent, or authority.

The core operating law is:

> **LEARN BY DEFAULT. SHARE WISDOM BY CONSENT. PROTECT IDENTITY BY DEFAULT. PUBLISH BY DECISION.**

Smart Connect means participation in the NayaNET intelligence network. It does **not** grant execution authority, public identity disclosure, public publication, or access to another person's private intelligence.

**Capability does not create authority.**

## How the system works

1. A human uses the **Intelligent Hub**.
2. The Hub is the human-facing projection/action surface. It is not a second brain.
3. NayaPOWER remains the governance and authority layer.
4. Intelligence is captured as governed Smart Notes / intelligent events.
5. Learning happens automatically where the runtime permits it.
6. When a human opens a **Smart Connect** door, participation is recorded.
7. Participation defaults to wisdom sharing while personal intelligence, personal activity, and identity remain private.
8. Useful intelligence can be distilled into collective wisdom through a governed runtime boundary.
9. Collective wisdom exposes the useful learning, not the contributor's private identity or raw private source.
10. Execution still requires its own authority boundary. Smart Connect never silently becomes execution permission.
11. Public publication is a separate deliberate decision.
12. Smart Ledger / receipts provide accountability and evidence so the system can prove what actually happened.
13. The system learns from verified evidence and carries that intelligence forward.

## What is DONE

### Governance and architecture
- NayaPOWER remains the governance / authority / execution control plane.
- NayaNET Intelligent Hub is the human-facing projection/action surface.
- The canonical participation/privacy protocol is documented.
- Smart Share has been retired as the participation concept; **Smart Connect** is canonical.
- The seven Smart Connect doors are defined.
- Participation is separated from execution authority.
- Privacy defaults are defined: personal intelligence private, personal activity private, identity private.
- Public publication is separated from participation.

### Smart Connect runtime seam
- Production participation storage exists.
- Authenticated Smart Connect / disconnect RPC boundaries exist.
- Collective wisdom storage and safe feed boundary exist.
- Collective wisdom contribution is restricted to the governed service-role execution boundary.
- Collective wisdom contribution requires active Smart Connect participation.
- Derived-only provenance prevents raw private source material and identity from being exposed through the collective contribution boundary.
- Edge Function nayanet-compound-intelligence version 38 contains the Smart Connect runtime seam.
- The denied path was proven in production: contribution without participation is rejected.
- The allowed causal seam was proven transactionally and rolled back; no synthetic participation remains in production.
- RPC privilege boundaries were verified.
- Authority requirements for intelligence_commit remain intact.
- Regression assertions were added.
- PR #607 was merged.

### Current Hub
- NAYANET/HUB/index.html is the canonical Hub implementation lane on main.
- The Hub already contains the major human-facing projection structure and multiple room/workspace surfaces.
- The Hub explicitly avoids fabricating unknown intelligence; several room states are correctly marked NOT VERIFIED where authoritative retrieval is not yet exposed.
- The Hub contains Personal / Collective / Activity feed concepts.
- Smart Note capture is wired into the governed runtime path.
- Smart Ledger and other room surfaces exist as application surfaces, but existence of a UI surface is not being treated as proof that its complete backend/runtime contract is finished.

## What is NOT DONE

The house is **not finished**. The following are still required before the front door is connected as the real production entry sequence:

### 1. Finish the Intelligent Hub
Every intended room must be a real working product surface, not merely a rendered interface.

For each room, prove:
- real data source
- authenticated retrieval
- correct privacy boundary
- real actions
- governed execution where applicable
- persistence
- receipts / evidence
- empty/error/unknown states
- source/runtime/UI parity

### 2. Complete the Hub's core operating loop
The Hub must reliably support:

**See → Understand → Learn → Prioritize → Remember → Question → Interpret → Act**

with authoritative evidence behind the states it presents.

### 3. Complete the authenticated Hub identity/runtime boundary
The Hub needs one canonical authenticated application path that establishes the real member context and connects that identity to the governed runtime without bypassing authority or privacy boundaries.

### 4. Put Smart Connect inside the finished Hub
Smart Connect belongs in the Intelligent Hub as the connection/participation surface.

The seven doors must become real governed entry points, with the same participation/privacy contract across all door types.

### 5. Prove one real participant journey
After the Hub and Smart Connect UI are ready, one real authorized participant must complete:

**Hub → Smart Connect → real participation → real intelligence event → intelligence_commit → collective wisdom → independent receipt verification**

This must use real authenticated identity and real production evidence. No synthetic consent counts.

### 6. Finish the accountability loop
The Smart Ledger must be able to independently reconstruct meaningful system actions from durable receipts rather than merely display UI.

### 7. Connect the future front door
Only after the Hub is actually finished:

**Welcome → Identity → Authenticated Intelligent Hub**

becomes the production entry sequence.

Until then:
- welcome.nayanet.app is a future front door.
- It must not be treated as the current completed NayaNET application.
- Opening the Welcome page is not proof of entering the real Hub.
- The Hub remains the house under construction.

### 8. Release S54 only after the real causal proof
S54 remains blocked until the real participant proof passes every required boundary.

## The finish line

The objective is not “a beautiful Hub.”

The objective is a **real governed intelligence network** in which:

**Human enters → identity is established → Hub operates → Naya learns → intelligence compounds → Smart Connect enables participation → useful wisdom becomes collective intelligence → privacy remains protected → authority remains scoped → actions are accountable → verified intelligence feeds the next moment.**

When that entire loop works in production, the Welcome page can become the real front door.

Until then, we finish the house.

**This document is the system-wide alignment message. Every Naya and coder working on NayaPOWER should use it as current direction. Do not build the front door ahead of the house. Do not mistake UI presence for runtime completion. Do not weaken governance to make a feature appear finished.**
