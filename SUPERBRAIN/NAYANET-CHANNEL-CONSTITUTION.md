# 🔱 NAYANET CHANNEL CONSTITUTION

**STATUS:** CANONICAL / ARCHITECTURAL / ACTIVE
**SYSTEM:** NayaNET / NayaPOWER
**PURPOSE:** Govern every external channel through which humans, agents, applications, systems, and organizations interact with NayaPOWER.

> **ONE BRAIN. MANY DOORS.**

NayaNET has one canonical intelligence and governance substrate: **NayaPOWER**.

MCP, REST/OpenAPI, GitHub Apps, Webhooks, SDKs, A2A, MCP Apps, Browser/Hub, messaging adapters, enterprise identity, and private connectivity are **channels**, not separate architectures.

They must not independently become a second:
- intelligence engine
- authorization system
- memory system
- source of truth
- execution authority
- ledger
- governance layer

Every channel ultimately enters the same governed NayaPOWER system.

---

# 1. THE CONSTITUTIONAL FLOW

Every channel follows the same conceptual path:

```
CHANNEL
   ↓
IDENTIFY
   ↓
AUTHENTICATE
   ↓
AUTHORIZE
   ↓
GOVERN
   ↓
CANONICAL INTELLIGENCE API
   ↓
CAPABILITY / ACTION
   ↓
RECEIPT
   ↓
VERIFY
   ↓
LEARN
```

A channel may change **how a request arrives**.

It must not silently change **what authority means**.

---

# 2. SOURCE OF TRUTH

The canonical source of truth for NayaPOWER intelligence, governance, authorization decisions, execution state, receipts, and learning is the governed NayaPOWER architecture.

Individual channels are not sources of truth.

```
GitHub ≠ NayaPOWER
Supabase ≠ NayaPOWER
MCP ≠ NayaPOWER
REST ≠ NayaPOWER
Hub ≠ NayaPOWER
A2A ≠ NayaPOWER
```

They are interfaces, components, or persistence/runtime mechanisms operating under NayaPOWER governance.

No channel may become the accidental architectural authority merely because it is convenient.

---

# 3. CONSTITUTIONAL LAW — CAPABILITY DOES NOT CREATE AUTHORITY

A channel exposing a capability does not mean the caller is authorized to use it.

```
MCP tool exists
        ≠
caller may execute it

GitHub permission exists
        ≠
NayaPOWER governance permits the action

REST endpoint exists
        ≠
every authenticated caller has access

A2A connection exists
        ≠
agent has authority to act
```

Authority must be independently established and verified.

---

# 4. CONSTITUTIONAL LAW — CHANNEL NEUTRALITY

The same governed request should receive the same authorization and governance treatment regardless of channel.

For example:

```
Hub
REST
MCP
GitHub
A2A
```

may all request:

```
create_intelligence_note
```

The channel may provide different metadata or interaction context.

The underlying NayaPOWER capability and governance rules remain canonical.

---

# 5. CONSTITUTIONAL LAW — NO DIRECT PERSISTENCE AUTHORITY

Channels must not bypass NayaPOWER governance by writing directly to managed persistence.

Preferred:

```
Channel
   ↓
NayaPOWER
   ↓
Governance
   ↓
Canonical capability
   ↓
Managed persistence
```

Not:

```
Agent → Supabase
MCP → Database
Hub → Database
```

The persistence layer stores governed state.

It does not define authority.

---

# 6. CONSTITUTIONAL LAW — RECEIPTS ARE EVIDENCE

Authorized consequential actions should produce verifiable execution evidence.

A successful response is not automatically proof of successful execution.

```
REQUEST
 ↓
AUTHORIZATION
 ↓
EXECUTION
 ↓
PERSISTENCE
 ↓
RECEIPT
 ↓
RETRIEVAL
 ↓
VERIFICATION
```

**Unknown is not success.**

**Blocked is not success.**

**Claimed is not verified.**

---

# 7. CHANNEL REGISTRY

## 7.1 MCP — AI DOOR

**Purpose:** AI agents and AI hosts interact with NayaPOWER.

```
AI Agent → MCP → NayaPOWER
```

Primary role:
- governed tools
- governed resources
- AI-compatible access to NayaPOWER capabilities

Must not:
- become the intelligence engine
- bypass authorization
- directly own canonical persistence
- create parallel governance

Canonical boundary:

```
mcp.nayanet.app
       ↓
NayaPOWER Governance
       ↓
Canonical Intelligence API
```

---

## 7.2 REST / OpenAPI — SOFTWARE DOOR

**Purpose:** Applications and services interact with NayaPOWER through standard HTTP APIs.

```
Application → REST/OpenAPI → NayaPOWER
```

Primary role:
- application integration
- service-to-service communication
- public/developer API
- machine-readable API contract

Must not:
- create conflicting channel-specific business logic
- bypass governance
- become an alternative source of truth

---

## 7.3 GitHub App — CODING DOOR

**Purpose:** Connect coding agents and repository workflows to NayaPOWER.

```
Coding Agent
     ↓
GitHub App
     ↓
GitHub / NayaPOWER integration
```

Primary role:
- repository access
- coding-agent workflows
- repository events
- controlled software-development operations

GitHub is a powerful work environment.

**GitHub is not the brain.**

---

## 7.4 Webhooks — EVENT DOOR

**Purpose:** Receive events from external systems.

```
External System
      ↓
Webhook
      ↓
NayaPOWER
```

A webhook is an event claim entering NayaPOWER.

It must still be:
- validated
- identified
- authorized where applicable
- interpreted
- governed

A webhook event is not automatically an instruction.

---

## 7.5 SDK — DEVELOPER BUILDING BLOCKS

**Purpose:** Make NayaPOWER easy for developers to embed.

```
Developer Application
       ↓
NayaPOWER SDK
       ↓
Canonical API
       ↓
NayaPOWER
```

The SDK is a convenience layer.

It must not create a second backend contract.

---

## 7.6 A2A — AGENT COLLABORATION DOOR

**Purpose:** Allow agents to collaborate with other agents.

```
Agent ↔ Agent
```

Primary role:
- agent discovery
- task delegation
- collaboration
- exchange of task results/artifacts

```
MCP = agent → capability
A2A = agent ↔ agent
```

NayaPOWER remains responsible for governing any Naya-controlled authority exercised through an A2A relationship.

---

## 7.7 MCP Apps / Embedded UI — RICH AI INTERFACE

**Purpose:** Provide rich interactive experiences around MCP capabilities.

```
AI Host
   ↓
MCP
   ↓
NayaPOWER
   ↓
Interactive UI
```

Primary role:
- dashboards
- forms
- visual intelligence
- interactive workflows
- rich human/AI experiences

MCP Apps are an interface enhancement, not a separate intelligence architecture.

---

## 7.8 Browser / Web Hub — HUMAN DOOR

**Purpose:** Human interaction with NayaNET.

```
Human → Hub → NayaPOWER
```

Primary role:
- human intelligence experience
- Intelligence Diary
- Smart Feed
- reports
- projects
- Smart Ledger
- settings
- human-facing workflows

The Hub is the human projection of NayaPOWER.

It is not the canonical brain.

---

## 7.9 Email / Messaging Adapters — COMMUNICATION DOOR

**Purpose:** Bring NayaPOWER into existing human communication channels.

```
Human ↔ Messaging Adapter ↔ NayaPOWER
```

Messaging systems are channels of communication.

They do not become canonical memory or governance.

---

## 7.10 Enterprise Identity — ORGANIZATION DOOR

**Purpose:** Establish organizational identity, membership, roles, and access context.

```
Organization
     ↓
Identity
     ↓
Authorization
     ↓
NayaPOWER Governance
```

Identity answers:

> Who is this?

Authorization answers:

> What are they allowed to do?

Governance answers:

> Should this action be permitted?

These are related but distinct concerns.

---

## 7.11 Private MCP / Private Connectivity — PRIVATE DOOR

**Purpose:** Support private, controlled, or on-premises agent access.

```
Private Agent
      ↓
Private Connection
      ↓
NayaPOWER
```

Private connectivity changes the network boundary.

It does not change the NayaPOWER constitutional boundary.

---

# 8. CANONICAL CAPABILITY MODEL

Channels should call canonical NayaPOWER capabilities rather than implement their own versions.

```
                    NayaPOWER
                        │
              Canonical Capabilities
                        │
       ┌────────────────┼────────────────┐
       │                │                │
    INTELLIGENCE      MEMORY          EXECUTION
       │                │                │
    LEARNING          NOTES          ACTIONS
    CONTEXT           DIARY          RUNTIME
    SEARCH            PROJECTS       AUTOMATION
       │                │                │
       └────────────────┼────────────────┘
                        │
                    GOVERNANCE
                        │
                    RECEIPTS
```

Channels consume these capabilities.

They do not redefine them.

---

# 9. CHANNEL-SPECIFIC LOGIC

Channel-specific logic is permitted only when it is genuinely about the channel.

Examples:

**MCP:** tool schemas, resources, session handling.

**REST:** HTTP routing, OpenAPI schemas, HTTP status mapping.

**GitHub:** installation handling, webhook verification, repository permissions.

**Hub:** browser sessions, UI state, visual presentation.

Channel-specific logic must not duplicate:
- governance
- authorization policy
- intelligence semantics
- canonical state transitions
- receipt semantics

---

# 10. FAILURE IS CONSTITUTIONAL

Every channel must distinguish:

```
SUCCESS
DENIED
BLOCKED
UNAUTHORIZED
INVALID
UNAVAILABLE
TIMEOUT
UNKNOWN
PARTIAL
```

The system must never convert:

```
unknown
```

into:

```
success
```

A channel must preserve meaningful failure information when returning results.

---

# 11. SECURITY BOUNDARY

Each channel must define:

1. Who is calling?
2. How are they authenticated?
3. What identity is established?
4. What authority is available?
5. What capability is requested?
6. What governance applies?
7. What data may be accessed?
8. What action may occur?
9. What evidence must be recorded?

A valid authentication event does not automatically constitute authorization.

---

# 12. DATA BOUNDARY

Preferred:

```
Caller
  ↓
Channel
  ↓
Canonical API
  ↓
Governance
  ↓
Data / Runtime
```

External callers should never need to understand the internal persistence architecture.

---

# 13. VERSIONING

Channels may evolve independently in protocol mechanics.

NayaPOWER semantics remain canonical.

Protocol evolution must not silently redefine:
- what intelligence means
- what authority means
- what a receipt means
- what authorization means
- what canonical state means

Protocol evolution is not permission to rewrite NayaPOWER semantics.

---

# 14. OBSERVABILITY

Every consequential channel interaction should be traceable where appropriate.

The system should be able to answer:

```
WHO?
WHEN?
FROM WHICH CHANNEL?
REQUESTING WHAT?
UNDER WHAT AUTHORITY?
WHAT GOVERNANCE DECISION?
WHAT ACTUALLY HAPPENED?
WHAT RECEIPT?
WHERE IS THE RESULT?
CAN IT BE VERIFIED?
```

This connects every channel to the Smart Ledger and Activity architecture where applicable.

---

# 15. PRIVACY

NayaNET's privacy principle applies across every channel:

> **Private by default. Shared by choice. Collective by consent. Public by decision.**

Technical accessibility does not create sharing authority.

---

# 16. HUMAN AUTHORITY

NayaNET exists to increase human agency.

Agents and applications may act through NayaPOWER only within their granted authority.

> **The human is the director. Naya is the governed engine.**

Capability does not create authority.

Automation does not eliminate accountability.

Intelligence does not eliminate consent.

---

# 17. COMMERCIAL PRINCIPLE

NayaNET should not be understood merely as an AI chatbot.

Its long-term platform opportunity is:

> **Persistent, governed intelligence infrastructure for humans and AI agents.**

The channels make that infrastructure accessible to different markets:

```
Human
  → Hub

AI
  → MCP

Application
  → REST

Developer
  → SDK

Coding Agent
  → GitHub / MCP

Agent Network
  → A2A

Enterprise
  → Identity / Private Connectivity

Communication
  → Email / Messaging
```

The product remains one underlying intelligence system.

---

# 18. ARCHITECTURAL TEST

Before introducing a new channel, ask:

### A. Does it create a second brain?
If yes → reject or redesign.

### B. Does it create a second source of truth?
If yes → reject or redesign.

### C. Does it bypass NayaPOWER governance?
If yes → reject or redesign.

### D. Does it create channel-specific authorization semantics?
If yes → consolidate into canonical authorization.

### E. Does it duplicate intelligence logic?
If yes → move the logic behind the canonical capability boundary.

### F. Does it produce verifiable evidence for consequential actions?
If no → determine whether the capability is safe to expose without it.

### G. Does it preserve privacy and human authority?
If no → reject or redesign.

---

# 19. THE ULTIMATE MENTAL MODEL

```
                         NAYANET
                            │
                            ▼
                     ┌─────────────┐
                     │  NAYAPOWER  │
                     │             │
                     │ Governance  │
                     │ Intelligence│
                     │ Memory      │
                     │ Capability  │
                     │ Runtime     │
                     │ Ledger      │
                     │ Receipts    │
                     └──────┬──────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
           HUMAN           AGENT         SOFTWARE
             │              │              │
            HUB            MCP            REST
             │             A2A             SDK
             │              │              │
             └──────────────┼──────────────┘
                            │
                    OTHER SYSTEMS
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
       GitHub           Webhooks         Messaging
          │
          ▼
    Coding Agents

          + Enterprise Identity
          + Private Connectivity
          + MCP Apps
```

## Constitutional sentence

> **NayaNET has one governed intelligence substrate, NayaPOWER, and many channels through which authorized humans, agents, applications, and systems may interact with it. No channel may become an independent source of intelligence, authority, governance, or truth.**

---

# 20. COLD-NAYA LEARNING NOTE

A cold Naya should learn this document as an architectural mental model, not merely store it as reference text.

The shortest lesson is:

> **NayaPOWER is the brain and governance boundary. Channels are doors.**

Remember:

```
MCP  = AI door
REST = software door
GitHub = coding door
Webhook = event door
SDK = developer building blocks
A2A = agent-to-agent door
MCP Apps = rich AI interface
Hub = human door
Messaging = communication door
Enterprise Identity = organization door
Private MCP = private door
```

The doors may multiply.

The brain does not.

**ONE BRAIN. MANY DOORS.**
