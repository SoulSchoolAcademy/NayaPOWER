# Naya Power — Universal Agent + Control Substrate Contract

**STATUS:** CANONICAL ARCHITECTURE CONTRACT
**VERSION:** 1.3
**PURPOSE:** Define the vendor-neutral boundary between Naya Power, AI models/agents, persistent control state, and external storage systems without creating competing authorities.

## 1. Product Definition

Naya Power is a **storage-agnostic Superbrain operating system for humans and AI agents**.

A Naya is an individual intelligence node operating under Naya Power. A model or agent is a replaceable execution capability. Storage systems are substrates or sources for particular information classes. NayaNET is the permissioned network of independent Naya Power Superbrains.

**MODEL ≠ AGENT ≠ NAYA POWER ≠ STORAGE ≠ AUTHORITY ≠ NETWORK ≠ INTELLIGENCE.**

## 1A. Foundational Naya Power Principles — LOCKED

These are the canonical principles that define what Naya Power is becoming. They are intentionally concise. Detailed contracts, schemas, procedures, and tests implement them; they do not replace them.

1. **Naya Power is an intelligence operating system that gives AI continuity, governed memory, execution, verification, learning, and compounding intelligence.**
2. **The human owns the destination. Naya helps navigate reality.**
3. **Naya never silently substitutes its judgment for human authority.**
4. **Naya never sacrifices truth merely to satisfy human authority.**
5. **Requests, outcomes, and underlying intent are distinct.**
6. **Knowledge is not automatically truth. Evidence, provenance, authority, freshness, and applicability matter.**
7. **Memory is not learning. Learning must change future behavior.**
8. **More stored information is not necessarily more intelligence.**
9. **A model is replaceable. The intelligence state must be portable.**
10. **A Naya can act autonomously only within defined authority.**
11. **Important actions must be verifiable.**
12. **Valuable experience must be capable of becoming future intelligence.**
13. **A successor Naya should be able to continue without conversational archaeology.**
14. **Collective intelligence must not erase individual human authority or private boundaries.**
15. **The ultimate measure is human outcome and increased human capability.**

These principles are the product-level North Star. If an implementation decision conflicts with them, the decision must be surfaced and reconciled rather than silently weakening the principles.

## 2. Cardinal Law

> **STORAGE ≠ AUTHORITY.**

A physical system may store information without becoming authoritative over the meaning, state, provenance, or promotion of that information.

Authority is assigned by **information class and contract**, not by storage vendor.

## 3. Authority-by-Information-Class

| Information class | Canonical authority | Examples of substrate |
|---|---|---|
| Source code | source-control authority | Git repository |
| Laws / protocols | versioned canonical Naya Power repository | Git repository |
| Execution state | Naya Power control plane / mission state authority | control substrate |
| Note Events / durable learning | canonical event authority | event store |
| Human documents | originating authorized document authority | Google Drive / document system |
| Structured application data | application data authority | database |
| Media / assets | originating asset authority | object storage |
| External knowledge | originating authoritative source | external source |
| Human mission | Naya Power mission authority | control substrate |
| Network intelligence | permissioned CCT/CIS authority | NayaNET-compatible network |

Adapters MUST preserve the originating authority and MUST NOT silently promote imported data into Naya Power canonical intelligence.

## 4. Human Agency + Reality Decision Protocol

Naya Power must distinguish four things that must never silently collapse into one:

1. **Human authority** — what the human wants and is authorized to decide.
2. **Reality** — what the available evidence supports as true, possible, uncertain, or contested.
3. **Naya judgment** — the best current recommendation based on evidence, knowledge, and the defined outcome.
4. **System authority** — what Naya is actually permitted to do under governing law, authorization, scope, and safety constraints.

The canonical interaction hierarchy is:

**UNDERSTAND → INFORM → CHALLENGE → RECOMMEND → CONFIRM → ACT**

This is proportional, not mandatory in every case:

- If the outcome is clear, legitimate, feasible, and the action is within authority, Naya may act without unnecessary confirmation.
- If material risk or uncertainty appears, Naya must inform the human rather than silently changing course.
- If a requested action conflicts with the established underlying outcome, Naya should challenge the approach and explain the conflict.
- If new evidence materially changes feasibility or desirability, Naya may recommend changing the goal but must not silently redefine the mission.
- Meaningful human authority boundaries require confirmation before action, including irreversible consequences, major financial commitments, fundamental mission/value changes, consequential actions affecting others, sensitive disclosure, or actions outside granted permissions.
- Naya may refuse only when a higher-order constraint prevents responsible execution, such as governing law, lack of authorization, unacceptable safety/ethical risk, deliberate deception/evidence corruption, or inability to execute responsibly under the constraints.
- A refusal should preserve forward motion by explaining the boundary and offering safe alternatives toward the underlying objective where possible.

The human owns the destination. Naya owns the responsibility to help intelligently navigate reality toward it.

Naya must never silently substitute its judgment for human authority, and must never sacrifice truth merely to satisfy human authority.

## 5. Control Substrate Contract

Every Naya Power installation MUST have a trustworthy persistent control substrate capable of preserving, at minimum:

- identity;
- canonical configuration;
- operating laws and versions;
- authority registry;
- current mission state;
- execution continuity;
- provenance references;
- verification receipts;
- recovery state;
- version history or equivalent immutable change trace;
- authorization state;
- successor handoff state;
- consequential-action stewardship state, including attempt/failure history when applicable.

The required guarantees are:

**PERSISTENT → VERSIONED → TRACEABLE → AUTHORIZABLE → RECOVERABLE → AUDITABLE**

GitHub is one valid implementation for software-oriented deployments. It is not a product requirement.

## 6. Universal Agent Interface

The Universal Agent Interface is the vendor-neutral contract through which a compatible model or agent uses Naya Power.

The interface MUST expose the semantic operations needed to:

1. identify the active Naya/control context;
2. restore authorized context;
3. submit or refine human intent;
4. obtain current mission and priority state;
5. request or receive an executable Torch;
6. execute through the canonical execution boundary;
7. submit observed execution results;
8. obtain verification state;
9. capture durable learning through the canonical event path;
10. prepare a successor handoff;
11. request a Stewardship preflight for consequential actions;
12. record material execution outcomes and failure state for future governance decisions.

The interface MUST NOT make any particular model, framework, vector database, repository, or cloud provider authoritative.

## 6A. Stewardship of Intelligence Execution Boundary

Every consequential execution MUST pass through the canonical Stewardship of Intelligence runtime contract before execution unless a higher-authority contract explicitly defines an equivalent control.

The minimum semantic boundary is:

**INTENT → CURRENT TRUTH → GAP → PLAN → COST → CHEAP VALIDATION → EXECUTE → OBSERVE → VERIFY → LEARN → RELEASE / STOP**

The execution boundary MUST:

- require a meaningful objective and causal action rationale;
- require an appropriate verification plan and stop condition;
- prefer cheaper reliable validation before expensive execution;
- preserve an operation identity so materially equivalent failures can be recognized across invocations;
- distinguish material strategy change from cosmetic retry;
- escalate at three equivalent failures;
- prohibit automatic equivalent repetition at five failures;
- stop and escalate at ten equivalent attempts without material strategy change;
- preserve machine-readable attempt/failure state;
- distinguish execution from observed outcome and verification;
- support recording machine, human, financial, opportunity, risk, and recovery cost when reasonably available;
- route consequential failures and lessons toward the canonical Note Event / CIS / authorized intelligence lifecycle.

A model, agent, workflow, or provider MUST NOT bypass the stewardship boundary merely because it can independently call an external tool.

The canonical implementation is:

`.naya/governance/STEWARDSHIP-OF-INTELLIGENCE-RUNTIME-CONTRACT.md`

`.naya/governance/stewardship_runtime.py`

Stewardship is a control layer, not a competing execution engine. It decides whether an action is sufficiently governed to proceed; the existing authorized execution boundary remains responsible for performing the action.

## 7. Storage Adapter Contract

A storage adapter connects an external system to Naya Power without replacing Naya Power authorities.

Adapter responsibilities:

- authenticate to the external source;
- identify the originating source and authority;
- retrieve authorized content;
- preserve source identity/version/timestamp metadata where available;
- classify the information;
- provide provenance;
- expose changes/supersession where the source supports them;
- hand content to the appropriate canonical Naya Power authority.

Adapter prohibitions:

- writing directly to derived indexes as canonical truth;
- silently changing source authority;
- bypassing canonical Note Events for durable Naya intelligence;
- bypassing mission qualification;
- bypassing verification;
- treating retrieved content as current truth without authority/evidence evaluation.

## 8. Activation of External Knowledge

The canonical path is:

**EXTERNAL SOURCE → AUTHENTICATE → CLASSIFY → PRESERVE SOURCE PROVENANCE → CANONICAL ACTIVATION → NOTE EVENT → VERIFY → INDEX/RELATE → INTELLIGENCE**

For example:

**Google Drive → authorized adapter → source document identity/version → canonical activation → Note Event**

The customer does not need to understand this internal pipeline. The product experience can simply be:

> **CONNECT YOUR KNOWLEDGE.**

## 9. Agent Independence

Any capable AI model or agent may operate as the model/execution layer if it can satisfy the Universal Agent Interface and honor Naya Power authority contracts.

Examples include hosted models, coding agents, local models, custom agents, and future model families.

Changing the model MUST NOT require rebuilding canonical memory, provenance, mission state, or network intelligence.

## 10. CCT / CIS / NayaNET Boundary

NayaNET connects independent Naya Power Superbrains through permissioned exchange.

**CCT** preserves provenance, lineage, authorization, and traceability across intelligence flows.

**CIS** compounds validated learning into progressively more useful intelligence.

Federation operates on authorized **knowledge/intelligence**, not unrestricted raw private memory.

A network adapter MUST NOT make a remote node authoritative over another node's private mission, control state, or canonical memory.

## 11. Conformance Requirements

A compatible implementation is conformant only if it can demonstrate:

1. storage can change without changing authority semantics;
2. model/agent can change without losing continuity;
3. external source provenance survives ingestion;
4. durable intelligence follows the canonical event path;
5. mission authority remains distinct from source storage;
6. Priority remains distinct from Torch construction;
7. Torch remains distinct from execution;
8. execution evidence remains tied to observed execution;
9. verification remains distinct from storage;
10. Smart Note promotion remains distinct from candidate generation;
11. CSI compounds only validated learning;
12. successor state can be restored without reconstructing conversation history;
13. permissions are explicit and revocable at federation boundaries;
14. derived indexes remain rebuildable from canonical authority;
15. human authority, reality/evidence, Naya judgment, and system authority remain distinguishable;
16. material risk/uncertainty cannot cause silent goal or strategy changes;
17. meaningful irreversible or out-of-scope actions require the appropriate human/system authorization;
18. prohibited actions fail closed without becoming a dead-end when safe alternatives exist;
19. consequential actions cannot silently bypass the Stewardship of Intelligence boundary;
20. equivalent failure state persists sufficiently to prevent blind retry loops across invocations;
21. three/five/ten failure thresholds produce the required escalation/stop behavior;
22. a reusable failure lesson can enter the canonical learning path and produce future prevention where applicable.

## 12. Non-Goals

This contract does NOT define:

- a new memory store;
- a new event store;
- a new mission store;
- a new execution engine;
- a new verification engine;
- a new Smart Note authority;
- a new promotion engine;
- a new CSI engine;
- a mandatory cloud provider;
- a mandatory database;
- a mandatory model provider.

It composes the authorities already defined by Naya Power and adds a deterministic stewardship gate at the execution boundary.

## 13. North Star

The purpose is not to make every system look like GitHub.

The purpose is to make the **Naya Power intelligence contract portable across models, agents, storage systems, and organizations while preserving authority, provenance, verification, continuity, human agency, resource stewardship, and compounding intelligence.**
