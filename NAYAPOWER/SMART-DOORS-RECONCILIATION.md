# NayaPOWER — Smart Doors Reconciliation Matrix

## Purpose

This document is the canonical **architecture/control reconciliation** for Smart Doors.

It reconciles the 11 Smart Doors defined by `NAYAPOWER/SMART-DOORS-ARCHITECTURE.md` against the actual repository evidence currently visible on `main`.

**Control rule:** this document changes no UI, creates no new door, and adds no runtime. It records what exists, what is partially established, what is externally unproven, and what remains future work.

## Evidence model

Status is deliberately separated into four questions:

- **Defined** — the architecture/contract exists.
- **Implemented** — repository code exists.
- **Deployed** — a deployment path has executed.
- **Proven** — the required external/runtime boundary has been verified end-to-end.

These states must not be inferred from one another.

## Current reconciliation

| # | Smart Door | Priority | Repository evidence | Current state | Boundary/proof gap | Next proof condition |
|---:|---|---:|---|---|---|---|
| 1 | MCP | 1 | `NAYANET/UNIVERSAL-AGENT-INTERFACE/worker.js`; release boundary; MCP initialize/tools/list/call contract | 🟢 **PROVEN AT CURRENT OWNER-BOUND PRODUCTION SCOPE** | Gate 1 proof run `35821213839` completed successfully after the live route became reachable; all MCP checks passed, including unauthorized fail-closed, authenticated initialize/tools/list, cold restore, persistence/receipt, retrieval and restore | Maintain freshness by rerunning the same proof after material runtime/route changes |
| 2 | REST / OpenAPI | 2 | `NAYANET/UNIVERSAL-AGENT-INTERFACE/openapi.yaml`; same Worker boundary | 🟢 **PROVEN AT CURRENT OWNER-BOUND PRODUCTION SCOPE** | Gate 1 proof run `35821213839` completed successfully; public health, unauthorized REST fail-closed, authenticated REST cold-restore/understand/retrieve and canonical-path convergence all passed | Maintain freshness by rerunning the same proof after material runtime/route changes |
| 3 | GitHub App | 3 | `NAYANET/EXECUTION-BRIDGE`; GitHub App Bridge specification; `nayanet-github-dispatch`; webhook adapter | 🟠 **PARTIALLY IMPLEMENTED** | Production App installation, production webhook wiring, identity/session boundary and full source→event→normalize→authorize→persist→project→verify chain are not proven | Prove an actual installed App delivery and authorized dispatch against the canonical event/receipt/projection chain |
| 4 | Webhooks | 4 | `NAYANET/EXECUTION-BRIDGE/nayanet-github-webhook/index.ts` | 🟠 **IMPLEMENTED RECEIVER / PRODUCTION CHAIN UNPROVEN** | Receiver verifies `x-hub-signature-256` and `x-github-delivery`, but external GitHub App configuration and end-to-end production delivery are not proven | Deliver a real signed GitHub App webhook and prove exact-once canonical event persistence plus downstream verification/projection |
| 5 | SDK | 5 | No canonical SDK implementation identified in the repository reconciliation | ⚪ **FUTURE** | No implementation/contract package established | Define SDK contract only when a concrete integration requirement exists; then implement against existing API/governance semantics |
| 6 | A2A | 6 | No canonical A2A implementation or contract identified | ⚪ **FUTURE** | No transport/protocol boundary established | Define governed agent-to-agent contract only when required; preserve distinct identities, scopes and authority |
| 7 | MCP Apps / Embedded UI | Later | No canonical implementation identified | ⚪ **FUTURE** | No embedded rich-interface door established | Do not build until an agent-triggered rich UI use case is authorized and specified |
| 8 | Browser / Web Hub | Existing | `NAYANET/HUB` canonical Hub; Cloudflare Worker/runtime; Hub auth and browser verification work | 🟢 **EXISTING / SUBSTANTIALLY PROVEN** | Current Hub release still has a separate browser page-error issue in the latest release evidence; this is not evidence that the Smart Door architecture is missing | Restore clean browser runtime proof, then maintain route/source/runtime parity |
| 9 | Email / Messaging Adapters | Existing / expanding | Smart Mail Hub surface/runtime and communication lifecycle evidence | 🟠 **EXISTING / EXPANDING** | The Smart Mail product surface exists, but broad external email/messaging adapter coverage is not proven as a unified production door family | Specify each external adapter boundary and prove identity, privacy, authorization, ingestion, persistence and projection per adapter |
| 10 | Enterprise Identity | Later | NayaPOWER identity/authority architecture exists | ⚪ **FUTURE ADAPTER** | No enterprise SSO/organizational identity integration established | Define organization identity mapping and authorization semantics before implementation |
| 11 | Private MCP Tunnel | Specialized | No canonical private tunnel implementation identified | ⚪ **SPECIALIZED FUTURE** | No private/on-prem transport boundary established | Define network, identity, revocation and audit requirements before implementation |

## Door state versus implementation state

The architecture's lifecycle states remain:

`PLANNED → IMPLEMENTED → CONNECTED → AUTHENTICATED → AUTHORIZED → HEALTHY`

with `DEGRADED`, `BLOCKED`, `REVOKED`, `EXPIRED`, `FAILED`, and `DISCONNECTED` as explicit states.

A repository implementation does **not** imply `CONNECTED`, `AUTHORIZED`, or `HEALTHY`.

### Current control interpretation

- **MCP:** implemented, deployment executed, public route not proven.
- **REST/OpenAPI:** implemented, deployment executed, public route not proven.
- **GitHub App:** adapter/dispatch architecture and code exist; external installation and complete production chain not proven.
- **Webhooks:** signed receiver exists; external production delivery chain not proven.
- **Browser/Web Hub:** existing door with substantial prior browser/deployment proof; current release has an unrelated-to-door page-error gate that must still be repaired before claiming a clean release.
- **Email/Messaging:** product surface exists; adapter family remains broader than currently proven evidence.
- **SDK/A2A/MCP Apps/Enterprise Identity/Private MCP Tunnel:** future/specialized; do not implement merely because the architecture names them.

## Cross-door control invariants

Every door remains subject to:

1. **One brain.**
2. **One governance model.**
3. **One canonical truth model.**
4. **One identity/authority model where protocol translation permits.**
5. **One canonical event model.**
6. **One verification/accountability model.**
7. Authentication is not authorization.
8. Connection is not permission.
9. Capability is not authority.
10. Transport success is not business success.
11. Event receipt is not downstream success.
12. Unknown remains unknown.
13. Blocked remains blocked.
14. Retry does not become success without new evidence.
15. Revocation and expiration are first-class.
16. Doors may transport/cache/transform/queue, but must not redefine canonical truth.

## Canonical convergence

The governing semantic path is:

**DOOR → IDENTITY → AUTHORITY → GOVERNANCE → CAPABILITY → EXECUTION → VERIFICATION → EVENT / RECEIPT → PROJECTION**

The transport-specific mechanics may differ. The authority, governance, truth and verification semantics do not.

## Proof program — one gap at a time

### Gate 1 — MCP / REST public route

**CLOSED / PROVEN at the current owner-bound production scope.** The authorized Cloudflare route is now reachable, and proof run `35821213839` on main commit `ed58f7176b0d33b6b09558abe91cf26ba2f7448e` completed successfully.

The run established public health, unauthorized REST/MCP fail-closed behavior, authenticated MCP initialize/tools/list/call, 14-question cold restore, persistence/receipt/retrieval, authenticated REST cold-restore/understand/retrieve, and MCP/REST convergence on the same canonical Worker path.

The first run after route access exposed proof-harness envelope assumptions and an intermittent `JWT issued at future` Supabase clock-skew rejection. The smallest proof-harness corrections were made; the final proof was then rerun unchanged and passed. No second runtime or Cloudflare redesign was introduced.

The existing verification sequence remains the canonical Gate 1 proof:

1. health
2. unauthorized REST fail-closed
3. unauthorized MCP initialize fail-closed
4. authenticated REST restore/retrieve/understand
5. authenticated MCP initialize
6. MCP tools/list
7. authenticated MCP tools/call
8. canonical persistence/retrieval
9. evidence/receipt
10. fresh retrieval
11. verified outcome
12. cold successor continuation

**Control:** MCP and REST are now considered proven only at the recorded owner-bound production scope of run `35821213839`; this does not generalize beyond that evidence scope.

### Gate 2 — GitHub App

Only after the MCP/REST public boundary is verified should the GitHub App chain be closed.

Required proof:

**GitHub App identity → signed event/authorized request → canonical normalization → authority check → persistence → execution where authorized → receipt/evidence → projection → verification**

The external App installation/configuration boundary must be evidenced; code presence is insufficient.

### Gate 3 — Webhooks

The existing receiver already establishes a meaningful implementation boundary: signature verification, delivery identification, normalization and canonical cognition-event persistence are explicit.

Remaining proof is external:

**real GitHub App delivery → receiver → exact-once canonical event → downstream processing → verified projection**

Do not treat receipt of a signed webhook as proof that downstream business processing succeeded.

## What must not be built now

Until the proof gates above are closed, do **not** build:

- a second MCP runtime;
- a second REST runtime;
- a new Smart Doors UI;
- an SDK;
- an A2A runtime;
- MCP Apps;
- enterprise SSO adapters;
- a private MCP tunnel;
- a parallel GitHub event store;
- a door-specific governance model;
- a door-specific source of truth.

The existing architecture is sufficient to continue the proof program.

## Relationship to 01–58

Smart Doors is a cross-cutting integration boundary over the existing 01–58 model. It does not replace any 01–58 domain and does not create a competing intelligence architecture.

The strongest existing 01–58 relationships are the domains covering:

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
- Intelligent Hub Construction + Experience
- Hub Implementation + Repository Reality Map
- Smart Note / Intelligent Block Data Contract
- Smart Feed / Activity Projection Contract
- Identity / Privacy / Publication
- Smart Space Contract
- Smart Link Contract
- Hub Runtime Deployment / Verification
- GitHub App Bridge + Communication
- Hub Source / Deployment Reconciliation
- Ultimate Trust Loop

## Control decision

**Architecture:** established.

**Existing doors:** Browser/Web Hub; Email/Messaging surface; MCP/REST/Webhook implementation boundaries.

**Partially established doors:** GitHub App; broad Email/Messaging adapter family.

**Closed proof boundary:** MCP/REST public runtime exposure, proven by run `35821213839` at owner-bound production scope.

**Future doors:** SDK, A2A, MCP Apps/Embedded UI, Enterprise Identity, Private MCP Tunnel.

**Next work:** Gate 1 is closed. Move to Gate 2: prove the existing GitHub App production identity/event/authority/execution chain; then close Webhook production-chain proof.

> **One brain. One governance. One truth model. Many doors.**
>
> **No new door is a reason to create a new brain.**
