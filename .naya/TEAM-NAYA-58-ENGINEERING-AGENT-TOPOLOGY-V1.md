# TEAM NAYA — 01–58 ENGINEERING AGENT TOPOLOGY V1

**Status:** ACTIVE EXECUTION PLAN
**Repository:** `SoulSchoolAcademy/NayaPOWER`
**Purpose:** Turn the 58-area architectural understanding into coordinated engineering work without creating 58 independent implementations.

## 1. CORE DECISION

Do **not** assign one agent to each numbered area.

The 58 areas collapse into shared engineering domains. Each agent owns a coherent domain, its contracts, implementation surfaces, tests, evidence, and handoff. Shared primitives are built once and consumed by downstream domains.

## 2. OPENCode OPERATING REALITY

OpenCode supports primary agents and specialized subagents. The current OpenCode model provides a full-access `build` agent, a read-only/planning `plan` agent, a broad `general` subagent, and a read-only `explore` subagent; custom agents can be given domain-specific prompts and permissions. Tool permissions can allow, ask, or deny read/edit/shell/task and other capabilities. Therefore this program must use explicit write ownership, read-only review roles, and a final independent verifier rather than assuming every agent can safely edit everything.

**Important:** Agent capability never creates Naya Power authority. Repository governance and the explicit current human authority remain controlling.

## 3. RECOMMENDED TEAM — 10 ROLES

### NAYA-PRIME — Orchestrator / Lead Architect
**Owns:** system integration, sequencing, cross-domain decisions, current mission state, conflict resolution, final handoff.
**Reads:** all 01–58.
**Writes:** orchestration/state/assignment records only unless explicitly delegated.
**Must not:** silently redefine authority or declare another agent's work verified.

### NAYA-INTEL — Intelligence Fabric Engineer
**Areas:** 01–18, 37, 50, 57.
**Owns:** Smart Note semantics, PIS, CIS, ALS, Smart Flow, Library/retrieval contracts, conversation intelligence.
**Primary output:** one coherent intelligence substrate and retrieval path.

### NAYA-GOV — Governance / Value / Authority Engineer
**Areas:** 20, 21, 25, 26, 27, 29–38.
**Owns:** constitution/governance integration, authority, MVPA, value math, preflight, Lead Mode, diagnostics, semantic rules.
**Primary output:** machine-enforceable governance boundaries.

### NAYA-RUNTIME — Execution / Continuity Engineer
**Areas:** 19, 28, 32–36, 54.
**Owns:** execution lifecycle, mission state, durable execution identity, successor handoff, universal execution loop.
**Primary output:** one executable governed lifecycle.

### NAYA-EVENT — Event / Activity / Evidence Engineer
**Areas:** 14, 39, 43, 44, 45, 58.
**Owns:** canonical event substrate, Activity projection, evidence/ledger linkage, event integrity, trust-loop evidence.
**Primary output:** `EXECUTE → CANONICAL EVENT → EVIDENCE → ACTIVITY → STATE → HANDOFF` with no orphan completion.

### NAYA-HUB — Intelligent Hub Engineer
**Areas:** 04, 08–13, 40–42, 47–50, 56–57.
**Owns:** Hub projection, Smart Boards/Blocks, feed UX, spaces, links, search UX, welcome/PWA experience.
**Primary output:** Hub consuming canonical intelligence/events rather than inventing alternate truth.

### NAYA-NET — Identity / Privacy / Collective Engineer
**Areas:** 10–13, 22–25, 46–49, 53, 56–57.
**Owns:** identity, privacy, publication, collective intelligence, Smart Share/Space/Link, NayaNET/Git bridge boundaries.
**Primary output:** safe network/collective layer with explicit publication state.

### NAYA-RELEASE — Source / Build / Runtime Observer
**Areas:** 41, 51, 52, 55 plus all deployment surfaces.
**Owns:** canonical source identification, build chain, deployment authority, live runtime verification, release evidence.
**Primary output:** one proven source→build→deploy→runtime chain.

### NAYA-HISTORIAN — Canonical Intelligence / Cleanup / Provenance
**Areas:** all 01–58 cross-cutting.
**Owns:** document provenance, duplicate/supersession detection, canonical references, historical preservation, evidence matrix integrity.
**Primary output:** clean navigation without destructive loss of unique intelligence.

### OSCAR — Independent Adversarial Verifier
**Areas:** all 01–58, but never as builder of the same claim being verified.
**Owns:** contradiction discovery, evidence challenge, negative testing, boundary testing, final readiness challenge.
**Writes:** verification/audit artifacts only.
**Must not:** certify its own implementation.

## 4. DOMAIN GROUPING

| Domain | Areas | Primary owner | Verification |
|---|---|---|---|
| Intelligence Fabric | 01–18, 37, 50, 57 | NAYA-INTEL | OSCAR |
| Governance / Value | 20–21, 25–27, 29–38 | NAYA-GOV | OSCAR |
| Superbrain Runtime | 19, 28, 32–36, 54 | NAYA-RUNTIME | OSCAR + NAYA-GOV |
| Event / Evidence / Trust | 14, 39, 43–45, 58 | NAYA-EVENT | OSCAR |
| Identity / Collective | 10–13, 22–25, 46–49, 53, 56–57 | NAYA-NET | OSCAR |
| Hub Experience | 04, 08–13, 40–52, 56–57 | NAYA-HUB | OSCAR + NAYA-RELEASE |
| Source / Release | 41, 51, 52, 55 | NAYA-RELEASE | OSCAR |
| Provenance / Cleanup | all | NAYA-HISTORIAN | NAYA-PRIME + OSCAR |

## 5. DEPENDENCY ORDER

### Wave 0 — Truth
All agents inspect the 58-area evidence matrix, canonical source map, control plane, current state, protected surfaces, and unresolved #55 source/deployment conflict.

### Wave 1 — Spine
NAYA-GOV + NAYA-RUNTIME + NAYA-EVENT establish the executable spine:
`IDENTITY → MISSION → PREFLIGHT → AUTHORITY → VALUE → EXECUTION → EVENT → EVIDENCE → VERIFY → STATE → HANDOFF`.

### Wave 2 — Intelligence
NAYA-INTEL connects Smart Notes/PIS/retrieval/learning to verified events and future action selection.

### Wave 3 — Network
NAYA-NET connects identity/privacy/sharing/collective contracts without creating a second truth system.

### Wave 4 — Hub
NAYA-HUB projects canonical intelligence, events, state and identity into the human experience.

### Wave 5 — Release
NAYA-RELEASE resolves #55 and proves the exact source/build/deploy/runtime chain.

### Wave 6 — Adversarial Proof
OSCAR attacks the integrated loop, not isolated documentation.

### Wave 7 — Cold-Naya Continuation
NAYA-PRIME executes the cold-start test from repository state alone and proves the next Naya can continue.

## 6. PARALLELIZATION RULE

Parallel work is allowed only when file ownership and dependency boundaries are explicit.

Do not allow two agents to modify the same canonical contract simultaneously.

A downstream agent must not build against an unresolved contradiction that an upstream agent is actively changing.

## 7. EVERY AGENT MUST RETURN

1. What I understood.
2. What I changed.
3. What I did not change.
4. What I proved.
5. Evidence paths/commands.
6. Failures and unknowns.
7. Contradictions discovered.
8. Current state.
9. Single next action.
10. Successor instructions.

## 8. NO FALSE GREEN

`DOCUMENTED != IMPLEMENTED != TESTED != INDEPENDENTLY VERIFIED != LIVE VERIFIED != ACCEPTED`.

An agent may report only the strongest state supported by evidence.

## 9. DEFINITION OF SUCCESS

Success is not 58 completed documents.

Success is one functioning loop:

`HUMAN INTENT → UNDERSTAND → PREFLIGHT → GOVERN → SELECT → EXECUTE → OBSERVE → VERIFY → CANONICAL EVENT → ACTIVITY → INTELLIGENCE → STATE → HANDOFF → NEXT NAYA`.

The 58 areas are successful when they cooperate as that loop without duplicate truth, authority ambiguity, invisible execution, or broken continuity.
