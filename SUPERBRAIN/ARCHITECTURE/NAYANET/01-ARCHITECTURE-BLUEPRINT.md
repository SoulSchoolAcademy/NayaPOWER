# 🔱 NAYANET — ARCHITECTURE BLUEPRINT

**Status:** CANONICAL PLANNING SPECIFICATION

## 1. Architectural objective

Create a provider-neutral intelligence network whose user experience can remain simple while its intelligence, memory, connection, and collective layers scale independently.

## 2. Core boundaries

```text
Experience Layer
  Player / Hub / future apps
        ↓
Naya Interaction Layer
        ↓
Intelligence Orchestration
        ↓
CIS / Note Event Layer
        ↓
Personal Superbrain Boundary
        ↓
Contribution / Collective Boundary
        ↓
Network / Connection Services
        ↓
Infrastructure
```

No layer may silently assume ownership of another layer's private state.

## 3. Static-first application boundary

The first Player release must work as a static application dropped into Cloudflare Pages/static hosting without Wrangler.

Static capabilities include:

- HTML/CSS/JS;
- local application state;
- deterministic content/config;
- browser audio/video;
- browser speech APIs where supported;
- client-side navigation;
- client-side visualizations;
- local persistence where appropriate;
- deep links handled by the host configuration where supported.

Capabilities requiring a server/runtime are represented by explicit integration seams rather than simulated as live infrastructure.

## 4. Future runtime boundary

When required, Cloudflare Worker/edge services may provide:

- authenticated APIs;
- secure secrets;
- LLM gateway;
- GitHub App integration;
- Supabase integration;
- server-side event writes;
- scheduled report generation;
- notifications;
- network matching;
- contribution processing.

The static Player must not require these services merely to render the core experience.

## 5. Identity model

Initial UX:

`Name → NayaNET identity → Smart Name → Smart Link`

Production security can later bind this identity to a durable authentication credential.

Do not treat a display name as proof of identity in security-sensitive operations.

## 6. Authentication model

Preferred future architecture:

```text
NayaNET UI
   ↓
Supabase Auth / equivalent identity service
   ↓
short-lived authenticated session
   ↓
Cloudflare edge/application APIs
```

The first static experience can operate without authentication for public content and use a progressive account-creation flow for personalized features.

## 7. Data ownership

### Public

Marketing/product content, public educational content, public NayaNET profile information chosen by the user.

### Personal

Profile, preferences, private notes, personal reports, private Superbrain references.

### Sensitive integration

GitHub installation information, provider tokens/installation IDs, private repository references, contribution permissions.

### Collective

Generalized, privacy-reviewed intelligence events intentionally published to the Collective.

The collective object must not require exposing the contributor's identity.

## 8. Event architecture

The fundamental intelligence unit remains an event rather than a silo.

Conceptual lifecycle:

`capture → normalize → validate → classify → store → retrieve → synthesize → learn → optionally contribute`

Events need stable IDs, timestamps, source/provenance, actor context where permitted, privacy classification, confidence/evidence metadata, and lifecycle status.

## 9. Integration contracts

The application must communicate through explicit contracts for:

- Naya interaction;
- Note Event creation;
- Smart Notes;
- Human Notes;
- daily reports;
- Superbrain access;
- GitHub connection;
- Wisdom Contribution;
- Collective Intelligence Events;
- network discovery;
- notifications.

Implementations may change. Contracts must remain stable unless formally versioned.

## 10. Failure isolation

A missing integration must not destroy the core Player.

Examples:

- GitHub disconnected → Player remains usable.
- LLM unavailable → deterministic fallback / honest unavailable state.
- Collective unavailable → private intelligence remains usable.
- media unavailable → text/transcript fallback.
- authentication unavailable → public experience remains accessible.

## 11. Modularity

Each Player block is independently deployable and replaceable.

A block must have:

- explicit inputs;
- explicit outputs;
- no hidden dependency on another block's DOM;
- namespaced CSS;
- namespaced JS;
- no global collisions;
- documented message/event interfaces;
- responsive behavior;
- accessibility behavior;
- test harness.

## 12. Groove boundary

Cloudflare hosts the block.

Groove embeds the stable URL.

The block owns its internal UI state.

Cross-frame communication is not required for the first release unless a concrete use case demands it. Future communication may use `postMessage` with a strict origin allowlist and versioned message schema.

## 13. Navigation

Default rule: navigation stays inside the application/block unless a destination is explicitly external or belongs to the parent Groove experience.

Do not couple navigation to parent-page DOM.

## 14. Long-term service map

```text
Cloudflare
 ├── static Player blocks
 ├── edge/API gateway
 ├── auth/session boundary
 ├── integration adapters
 └── scheduled intelligence jobs

Supabase
 ├── authentication
 ├── relational application state
 ├── secure persistence
 └── realtime/network features where appropriate

GitHub
 ├── canonical NayaPOWER source
 ├── optional personal Superbrain repositories
 └── GitHub App integration

CIS / Superbrain
 ├── personal events
 ├── retrieval
 ├── synthesis
 └── continuity

Collective
 ├── contribution
 ├── validation
 ├── collective events
 └── distribution
```

## 15. Architectural law

> **Connect the Superbrain. Do not absorb the Superbrain.**

> **Synchronize intelligence events, not private repositories.**

> **Keep the experience simple by making the architecture disciplined.**
