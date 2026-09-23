# NayaPOWER — Smart Doors Architecture

## Architectural law

**One brain. One governance. Many doors.**

NayaPOWER is one governed intelligence system. A Smart Door is an access/integration channel through which an authorized human, application, agent, service, or system can exchange context, intelligence, requests, actions, or events with that same underlying NayaPOWER system.

**Doors are channels, not architectures.**

A new door must not create a second brain, competing memory, independent governance model, duplicate source of truth, or parallel intelligence architecture.

## Core separation

NayaPOWER has four distinct concerns:

1. **Intelligence** — memory, Smart Notes, learning, retrieval, reasoning, state and intelligence projections.
2. **Governance** — constitution, authority, permissions, privacy, policy and controlled action.
3. **Verification / accountability** — events, evidence, verification, receipts, Ledger and trust.
4. **Smart Doors** — controlled interfaces into the system.

The Hub is the human-facing presentation/action surface. Smart Doors are the integration boundary.

**The Hub is a door. It is not the brain.**

## Non-negotiable authority rule

**Capability does not create authority.**

A door may expose a capability without granting permission to use it.

Every consequential request entering through a door must remain subject to the same identity, authority, privacy, governance, verification and accountability boundaries used elsewhere in NayaPOWER.

Therefore:

- authentication is not authorization;
- connection is not permission;
- tool visibility is not action authority;
- event ingestion is not event approval;
- an agent's capability is not human authority;
- a webhook's arrival is not permission to act;
- an API credential is not permission to perform every available operation;
- a successful transport response is not proof that the requested work succeeded.

## The 11 Smart Doors

| Priority | Smart Door | Direction | Primary role | Lifecycle emphasis |
|---:|---|---|---|---|
| **1** | **MCP** | Agent → NayaPOWER | Governed tools and context for agents | First-class |
| **2** | **REST / OpenAPI** | App/agent → NayaPOWER | Standard programmatic API | First-class |
| **3** | **GitHub App** | Coding agent ↔ NayaPOWER | Repository, code and development integration | First-class |
| **4** | **Webhooks** | System → NayaPOWER | Verified external event ingestion | First-class |
| **5** | **SDK** | Developer ↔ NayaPOWER | Embedded developer integration | First-class |
| **6** | **A2A** | Agent ↔ agent | Governed agent collaboration | First-class |
| Later | **MCP Apps / Embedded UI** | Agent → rich interface | Agent-triggered interactive experiences | Later |
| Existing | **Browser / Web Hub** | Human ↔ NayaPOWER | Human-facing Hub | Existing |
| Existing / expanding | **Email / Messaging Adapters** | Human/network ↔ NayaPOWER | Communication intelligence | Expanding |
| Later | **Enterprise Identity** | Organization ↔ NayaPOWER | Organization-level identity and authorization | Later |
| Specialized | **Private MCP Tunnel** | Private agent ↔ NayaPOWER | Private/on-premise agent access | Specialized |

Priority describes the current architectural sequencing of the integration program. It does **not** rank intelligence, authority, trustworthiness, or importance of users or agents.

## Door contract

Every Smart Door must have an explicit contract containing:

### 1. Identity
Who or what is connecting?

### 2. Authentication
How is the connecting party authenticated?

### 3. Capability
What NayaPOWER capabilities can this door expose?

### 4. Scope
What resources, projects, Spaces, intelligence, or operations are in scope?

### 5. Authority
What is the connecting party actually authorized to do?

### 6. Input contract
What requests, context, commands, or events can enter?

### 7. Output contract
What intelligence, result, receipt, event, or error can leave?

### 8. Verification
How is authenticity, execution, result, or event state verified?

### 9. Privacy
What information can cross the boundary, under whose choice and consent?

### 10. Accountability
What consequential exchange is recorded in the canonical event/Ledger system?

### 11. Failure truth
How are rejected, blocked, unavailable, unverified, expired, replayed, or failed requests represented?

### 12. Revocation
How can access, credentials, sessions, grants, or connections be revoked?

A door is not production-complete until these boundaries are defined for the capabilities it exposes.

## Door lifecycle / status model

Door **status** is separate from architectural **priority**.

Recommended canonical lifecycle:

1. **PLANNED** — door is defined but not available.
2. **IMPLEMENTED** — transport/interface exists but is not necessarily activated.
3. **CONNECTED** — a connection exists.
4. **AUTHENTICATED** — identity has been successfully authenticated.
5. **AUTHORIZED** — required authority/grants are present for the requested scope.
6. **HEALTHY** — connection and required capabilities are operating and verification is passing.
7. **DEGRADED** — connection exists but one or more required capabilities/verification paths are impaired.
8. **BLOCKED** — a request or capability is intentionally denied by authority/governance.
9. **REVOKED** — previously granted access is no longer valid.
10. **EXPIRED** — session, credential, grant, or connection has reached its validity boundary.
11. **FAILED** — the door or requested operation failed without a successful verified result.
12. **DISCONNECTED** — connection no longer exists.

These states must never be collapsed into a single generic “connected” boolean.

For example:

**CONNECTED ≠ AUTHORIZED ≠ HEALTHY ≠ SUCCESSFUL**

## Request path

All doors converge on the same governed system boundary:

**DOOR → IDENTITY → AUTHORITY → GOVERNANCE → CAPABILITY → EXECUTION → VERIFICATION → EVENT / RECEIPT → PROJECTION**

The exact implementation may differ by door, but the governing semantics do not.

### Agent/tool example

**MCP request → authenticated agent identity → scoped authority check → governed tool execution → verification → receipt/event → intelligence projection**

### External event example

**Webhook → authenticated sender/signature → event validation → canonical event boundary → authorized processing → verification → receipt/event → projection**

### Human example

**Browser Hub → human identity → authorized action → NayaPOWER execution → verification → event/Ledger → Hub projection**

The transport is different. The brain and governance are not.

## Source-of-truth rule

Smart Doors must not become competing stores of truth.

Canonical ownership remains:

- **Smart Notes / intelligence** → canonical intelligence substrate
- **Events** → canonical event contract/boundary
- **Evidence / verification** → evidence and verification system
- **Authority** → authority registry/governance
- **State** → mission/state system
- **Ledger** → accountability system
- **Hub** → human presentation/action projection
- **Smart Doors** → controlled integration boundary

A door may cache, transform, serialize, queue, or transport information as required by its protocol, but it must not silently redefine canonical truth.

## Door-specific role boundaries

### MCP — Priority 1
The primary agent-facing tool/context door. MCP should expose governed NayaPOWER capabilities and context without becoming a separate agent brain.

### REST / OpenAPI — Priority 2
The standard machine-to-machine HTTP contract for applications and agents that require explicit API operations. OpenAPI describes capabilities; NayaPOWER governance determines authority.

### GitHub App — Priority 3
The coding/repository door. Repository events, code operations, issues, pull requests and development workflows enter through this boundary while remaining subject to NayaPOWER authority and verification.

### Webhooks — Priority 4
The event-ingestion door. External systems notify NayaPOWER of events; receipt of a webhook must not be treated as proof that downstream processing succeeded.

### SDK — Priority 5
The developer embedding door. SDKs make NayaPOWER easier to integrate without creating a second semantic or governance model.

### A2A — Priority 6
The agent-collaboration door. Agents may communicate and coordinate through NayaPOWER while retaining distinct identities, capabilities and authority.

### MCP Apps / Embedded UI — Later
Rich interfaces invoked from agent workflows. The UI is another presentation surface, not another intelligence system.

### Browser / Web Hub — Existing
The principal human-facing door into the NayaNET/NayaPOWER experience. Its UI projects canonical intelligence and exposes only authorized actions.

### Email / Messaging Adapters — Existing / Expanding
Communication doors that turn messages into governed intelligence and connected communication objects where authorized.

### Enterprise Identity — Later
Organization-level identity, SSO and authorization integration. Enterprise identity establishes organizational identity; it does not by itself grant NayaPOWER action authority.

### Private MCP Tunnel — Specialized
Private-network/on-premise access for agents that require a controlled private transport path. Private transport does not bypass NayaPOWER governance.

## Smart Doors in the Hub

Smart Doors may eventually have a human-facing **Smart Doors** control surface, but this does not change the existing ten Hub surface contracts.

The Smart Doors surface is an infrastructure/integration control plane projection. It may show:

- available doors;
- connected doors;
- lifecycle status;
- authenticated identity;
- authorized scopes;
- exposed capabilities;
- connection health;
- verification state;
- recent door events;
- revocation/expiration state;
- documentation and activation requirements.

It must never display or expose secret credentials merely to make a door appear configured.

The existing Hub destinations remain:

1. Your Intelligence Today
2. Your Reports
3. Intelligent Library
4. Smart Share
5. Smart Ledger
6. Your Connections
7. Smart Lists
8. Smart Mail
9. Smart Spaces
10. Settings

**Adding Smart Doors to NayaPOWER does not rename, reorder, replace, or redefine those ten product contracts.**

## Smart Doors and the Hub

The relationship is:

**Smart Doors = ways into NayaPOWER**

**Hub = what the human sees and controls**

**NayaPOWER = the governed intelligence system underneath both**

The browser Hub is itself an existing Smart Door, but it remains the canonical human experience rather than becoming a second integration architecture.

## Security and trust invariants

1. One identity model where practical; adapters must map identities explicitly when protocols differ.
2. One authority model.
3. One governance model.
4. One canonical event model.
5. One verification/trust model.
6. One accountability model.
7. No transport-specific bypass.
8. No “internal” door automatically receives elevated authority.
9. No successful HTTP/MCP/A2A/Webhook response is itself proof of business success.
10. Revocation must propagate to the affected door and its sessions/grants.
11. Replay resistance is required where the protocol/event semantics require it.
12. Unknown must remain unknown; blocked must remain blocked.
13. No retry may be treated as success without new evidence.
14. Door telemetry must not replace canonical events.
15. A door may expose capability only within its declared contract and granted scope.

## Activation model

A Smart Door becomes operational through the same controlled activation philosophy as NayaPOWER itself:

**DEFINE → AUTHENTICATE → AUTHORIZE → CONNECT → VERIFY → ACTIVATE → OBSERVE → REVOKE/ROTATE**

Activation must produce evidence of the actual boundary established.

The architecture should distinguish:

- **door implemented**
- **door configured**
- **door connected**
- **door authenticated**
- **door authorized**
- **door verified**
- **door operational**

No one of these states should be inferred from another.

## Relationship to the 01–58 architecture

Smart Doors are an architectural layer spanning the existing NayaPOWER model, not a replacement for it.

The strongest direct relationships are to domains concerning:

- Primary Intelligence System
- Human Authority + AI Intelligence
- NayaNET
- Collective Intelligence
- Privacy by Choice
- Constitution Act
- Governance Act
- Authority Registry
- Master System Architecture
- Master Activation Protocol
- Cross-System Event Contract
- Hub Construction / Experience
- Hub Implementation / Repository Reality
- Identity / Privacy / Publication
- Smart Link Contract
- Hub Runtime Deployment / Verification
- GitHub App Bridge + Communication
- Hub Source / Deployment Reconciliation
- Ultimate Trust Loop

The 01–58 domains remain the canonical intelligence/architecture model. Smart Doors provides an explicit integration-boundary layer across those domains.

## Acceptance criteria

Smart Doors architecture is considered established when:

1. the 11 doors are explicitly named;
2. MCP is priority 1, REST/OpenAPI 2, GitHub App 3, Webhooks 4, SDK 5, A2A 6;
3. later/existing/specialized lifecycle categories are explicit;
4. priority and runtime status are separate concepts;
5. every door has an identity/authority boundary;
6. all doors converge on the same NayaPOWER intelligence/governance substrate;
7. no door creates a competing brain or source of truth;
8. authentication is not confused with authorization;
9. transport success is not confused with business success;
10. verification and accountability remain canonical;
11. revocation/expiration/failure are first-class states;
12. the existing ten Hub surface contracts remain unchanged;
13. future Smart Doors UI is treated as an infrastructure projection, not a replacement Hub architecture.

## Governing statement

> **One brain. One governance. One truth model. Many doors.**
>
> **Every door may provide a different way in. None provides a different NayaPOWER.**
