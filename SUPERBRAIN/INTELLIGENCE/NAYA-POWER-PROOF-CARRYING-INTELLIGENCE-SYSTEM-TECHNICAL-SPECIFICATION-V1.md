# Naya Power — Proof-Carrying Intelligence System (P-CIS)
## Canonical Technical Specification V1

**Status:** CANONICAL BINDING SPECIFICATION  
**Version:** 1.0  
**Scope:** Naya Power / SUPERBRAIN / `.naya` / Intelligence Actions / Smart Intelligence surfaces  
**Purpose:** Bind the existing Naya Power operating model, constitution, control plane, action schema, verification system, Smart Note/Board/Feed architecture, and CIS into one explicit proof-carrying intelligence architecture.

> **P-CIS does not create a second constitution, second control plane, or competing source of truth.**
> It is a binding technical architecture over the existing Naya Power authorities.

---

## 1. Core Law

> **Every meaningful Naya operation SHALL carry its authority, intent, action identity, evidence, result, verification state, learning, memory/provenance, and continuation.**

The atomic unit is an **INTELLIGENCE ACTION**, not a chat message, prompt, task card, dashboard card, or transcript.

Canonical lifecycle:

**INTENT → UNDERSTANDING → AUTHORITY → DECISION → ACTION → EVIDENCE → RESULT → VERIFICATION → LEARNING → MEMORY → NEXT ACTION**

The system SHALL preserve the distinction:

- capability ≠ authority;
- confidence ≠ evidence;
- generated ≠ executed;
- executed ≠ observed;
- observed ≠ verified;
- implemented ≠ production-proven;
- recorded ≠ current;
- unknown ≠ success;
- blocked ≠ pass;
- failure ≠ lost progress.

---

## 2. Canonical Authority Hierarchy

P-CIS inherits authority; it does not redefine it.

### 2.1 Constitutional authority

The current Naya Power runtime constitution is authoritative for runtime law, governance boundaries, safety, authority, and fail-closed behavior:

` .naya/codex/11-RUNTIME-CONSTITUTION.md `

### 2.2 Control-plane authority

The existing control plane remains the machine-readable operational authority:

- `.naya/control-plane/MAP.json` — system/navigation/authority map
- `.naya/control-plane/STATE.json` — current operational state
- `.naya/control-plane/BLOCKS.json` — active execution block
- `.naya/control-plane/PROOF.json` — proof/evidence boundary
- `.naya/control-plane/GOVERNANCE-KERNEL.json` — governance kernel

` .naya/memory/STATE.json ` remains a legacy/history projection with no authority.

### 2.3 Action authority

` .naya/actions/NAYA_ACTION_V1.schema.json ` defines the canonical machine contract for an Intelligence Action.

### 2.4 Navigation authority

` SUPERBRAIN/NAYAPOWER-CANONICAL-SOURCE-MAP.md ` remains the canonical navigation map. P-CIS MUST NOT silently override more-specific canonical sources.

### 2.5 Foundational operating model

` SUPERBRAIN/NAYA-POWER-INTELLIGENCE-OPERATING-MODEL.md ` defines how Naya Power turns human intent and AI capability into persistent, actionable, verifiable, compounding human-AI intelligence.

### 2.6 Hub-specific authority

Intelligent Hub work remains gated by:

` .naya/NAYAPOWER-INTELLIGENT-HUB-READ-FIRST.md `

and its referenced Master Design Contract, PIS Smart Note, Design/Build Activation, builder, verification workflow, and deeper `.naya/` sources.

---

## 3. P-CIS Component Map

| P-CIS component | Canonical Naya Power binding | Runtime role | Evidence boundary | Acceptance test |
|---|---|---|---|---|
| Human authority | Human Agency / runtime constitution | Principal; supplies intent, values, authorization | Explicit authority record / confirmation where required | Action cannot execute outside authority |
| Naya interface | Naya interface layer / boot contract | Understand, clarify, teach, orchestrate | Human-visible receipt and action record | Cold Naya restores mission/authority/context |
| Governance | Runtime Constitution + Governance Kernel | Permission, policy, safety, scope | Decision/evaluation record | Fail-closed governance tests pass |
| MAP | `.naya/control-plane/MAP.json` | Canonical navigation/authority map | Current source identity | MAP agrees with STATE/BLOCKS/PROOF |
| STATE | `.naya/control-plane/STATE.json` | Current truth/state | Live identity, known/unknown/protected state | Live HEAD/state resolves and validator passes |
| BLOCK | `.naya/control-plane/BLOCKS.json` | Current execution objective | Scope, acceptance, next action | Exactly one active block and coherent next action |
| PROOF | `.naya/control-plane/PROOF.json` | Evidence boundary | Claim/evidence/verification | No unsupported success claim passes |
| Intelligence Action | `.naya/actions/NAYA_ACTION_V1.schema.json` | Atomic governed action object | Identity, authority, evidence, result, learning | Schema + lifecycle + no-orphan validation passes |
| Execution | NAYA_ACTION actions / authorized tools | Perform authorized work | Tool/runtime evidence | Execution identity and outcome recorded |
| Observation | NAYA_ACTION observations | Capture what reality reported | Observation source/time | Observation is distinguishable from claim |
| Verification | NAYA_ACTION verification + workflows/validators | Determine whether acceptance is proven | Independent/appropriate evidence | Verification contract passes or remains UNKNOWN/FAILED |
| Failure recovery | NAYA_ACTION failure + `REQUIRES_REPAIR` | Convert failure to repair information | Root cause, repair, safeguard, retest | First divergence repaired and retested |
| Smart Note | Hub Smart Note architecture | Human-readable durable intelligence | Source/action/provenance/truth state | Note preserves event identity and meaning |
| Smart Board | Hub Smart Board contract | Human comprehension/action surface | Provenance/truth/verification visible | Required intelligence spine and actions render correctly |
| Smart Feed | Hub Smart Feed contract / PIS feed | Living intelligence stream | Intelligent Block identity/provenance | Feed preserves object identity and truth states |
| CIS | Intelligence Operating Model | Reflection, connection, synthesis, compounding | Source Note Events + derived intelligence provenance | Higher-order intelligence references source events |
| Superbrain | Naya Power Intelligence Operating Model | Persistent intelligence environment | Cross-layer provenance/state | Model/session can restore relevant operating context |
| Torch | NAYA_ACTION `next_action` + handoff/boot contracts | Successor continuity | Exact next action + pass condition | Cold successor can execute without conversational archaeology |
| OSCAR | Runtime operating cycle / review practice | Independent challenge/review | Review result and repair loop | Builder output is challenged before promotion where required |

---

## 4. Intelligence Action Contract

Every consequential action SHOULD be represented as a `NAYA_ACTION_V1` instance. Material work MUST use the schema where the action contract applies.

Minimum conceptual payload:

```text
IDENTITY
MISSION
HUMAN INTENT
NAYA UNDERSTANDING
AUTHORITY
CONSTRAINTS
UNCERTAINTY / CONSEQUENCE / IRREVERSIBILITY
PLAN
ACTIONS
OBSERVATIONS
EVIDENCE
VERIFICATION
RESULT
VALUE / COST / RISK
FAILURE / REPAIR / SAFEGUARD
LESSON
MEMORY
RELATED ACTIONS
PROVENANCE
HUMAN CONFIRMATION
NEXT ACTION
STATE
```

The machine schema is authoritative for exact field names, enums, required properties, and validation behavior.

---

## 5. Runtime State Machine

P-CIS maps the action contract onto the existing lifecycle states:

```text
PROPOSED
   ↓
INVESTIGATING
   ↓
READY_FOR_DECISION
   ↓
AUTHORIZED
   ↓
EXECUTING
   ↓
EXECUTED
   ↓
OBSERVED
   ↓
VERIFIED
   ↓
LEARNED / RECORDED
   ↓
HANDOFF / CONTINUE
```

Failure/stop branches remain explicit:

```text
EXECUTING / EXECUTED
       ├── FAILED
       ├── REQUIRES_REPAIR
       ├── STOPPED
       └── DEFERRED
```

The system MUST NOT collapse these states into a generic `done` state.

---

## 6. Authority Firewall

The governance kernel is the authority firewall between intelligence and action:

```text
AI CAPABILITY
     ↓
PROPOSED ACTION
     ↓
GOVERNANCE / AUTHORITY CHECK
     ├── NOT AUTHORIZED → BLOCK / ASK / DEFER
     └── AUTHORIZED → EXECUTE
```

Learning, memory, confidence, precedent, or successful prior actions MUST NOT silently create authority.

Consequential or irreversible actions require the authorization level defined by the current constitution and action contract.

---

## 7. Evidence and Proof Model

P-CIS treats proof as a chain, not a sentence.

```text
SOURCE
  ↓
ARTIFACT
  ↓
ACTION IDENTITY
  ↓
EXECUTION
  ↓
OBSERVATION
  ↓
EVIDENCE
  ↓
VERIFICATION
  ↓
RESULT
```

Evidence SHOULD identify exact artifacts, commits, workflow runs, runtime observations, or other authoritative proof objects where applicable.

The system MUST preserve the distinction:

**SOURCE → BUILD → ARTIFACT → DEPLOYMENT → EXACT RUNTIME → INDEPENDENT OBSERVATION → VERIFICATION**

A source file cannot prove runtime behavior by itself.

HTTP success cannot prove semantic correctness by itself.

Runtime success cannot prove visual UX acceptance without the appropriate visual inspection.

---

## 8. Uncertainty Model

Uncertainty is a first-class property, not a prose disclaimer.

The action model records uncertainty, consequence, irreversibility, and risk tier. P-CIS uses these to determine how much authority, evidence, review, and verification are required.

Conceptual rule:

```text
RISK = UNCERTAINTY × CONSEQUENCE × IRREVERSIBILITY
```

Higher-risk work demands stronger authorization and verification. Exact thresholds remain governed by the current constitution and action schema.

Unknown is a valid state.

Unknown MUST NOT be promoted to verified merely because no failure was observed.

---

## 9. Failure → Learning Protocol

Failure SHALL become structured intelligence whenever useful:

```text
FAILURE
  ↓
FIRST DIVERGENCE
  ↓
ROOT CAUSE
  ↓
REPAIR
  ↓
RETEST
  ↓
VERIFICATION
  ↓
LESSON
  ↓
SAFEGUARD / SYSTEM IMPROVEMENT
```

The system MUST preserve enough information for a successor to avoid repeating the same known failure.

### No retry without new information

A failed attempt MUST NOT be repeated merely because the desired outcome remains desirable.

A retry requires a material change in information, conditions, authorization, implementation, or verification strategy.

---

## 10. Memory and Provenance

P-CIS binds action memory to the existing Naya Power memory model:

- Human Memory
- Naya Memory
- Project Memory
- Knowledge Memory
- Execution Memory
- Learning Memory
- Decision Memory

Memory MUST remain provenance-aware, freshness-aware, privacy-respecting, inspectable, correctable, and supersession-aware.

The rule is:

> **Preserve the identity of the accomplishment, not merely its description.**

For material artifacts, preserve identifiers such as commit SHA, artifact hash, run ID, deployment identity, runtime identity, or equivalent proof-bearing references when available.

---

## 11. Smart Intelligence Projection

The machine action and human intelligence surfaces form a projection chain:

```text
NAYA_ACTION_V1
      ↓
SMART NOTE
      ↓
INTELLIGENT BLOCK
      ↓
SMART BOARD
      ↓
SMART FEED
      ↓
CIS / HIGHER-ORDER INTELLIGENCE
```

These are not competing sources of truth.

They are different representations and aggregation levels of governed intelligence events.

### Smart Note

Answers:

- What happened?
- What did it mean?
- What did Naya understand?
- What was learned?
- What should be remembered?

### Smart Board

Makes the intelligence understandable, inspectable, and actionable. It MUST preserve provenance, truth state, meaningful actions, and verification context.

### Smart Feed

Provides the living stream of Intelligent Blocks while preserving identity, provenance, truth state, relationships, and evolution.

### CIS

Synthesizes Note Events across time into higher-order intelligence:

**EXPERIENCE → REFLECTION → KNOWLEDGE → CONNECTION → INTELLIGENCE → ACTION → EXPERIENCE**

---

## 12. Superbrain Binding

SUPERBRAIN is the persistent intelligence environment connecting:

```text
CONSTITUTION
   ↓
GOVERNANCE
   ↓
CONTROL PLANE
   ↓
INTELLIGENCE ACTIONS
   ↓
MEMORY / KNOWLEDGE
   ↓
EXECUTION
   ↓
VERIFICATION
   ↓
SMART INTELLIGENCE SURFACES
   ↓
CIS
   ↓
CONTINUITY
```

P-CIS therefore belongs inside the existing Superbrain architecture; it is not a separate product or parallel operating system.

---

## 13. Control Plane Binding

P-CIS SHALL preserve the existing control-plane relationship:

```text
MAP
 ↓
STATE
 ↓
BLOCK
 ↓
ACTION
 ↓
PROOF
 ↓
RECEIPT / EVIDENCE
 ↓
STATE UPDATE
 ↓
NEXT ACTION
```

The control plane remains singular.

P-CIS MUST NOT introduce a second state authority, second block authority, second proof authority, or second constitution.

Where P-CIS and a more-specific canonical source appear to conflict, the designated more-specific constitutional/runtime authority wins and the conflict becomes a repair item rather than an opportunity to silently create parallel truth.

---

## 14. Continuity / Torch Protocol

Every material Intelligence Action MUST expose exactly one highest-value continuation action when execution is complete or blocked.

A successor handoff SHOULD contain:

```text
MISSION
CURRENT STATE
WHAT WAS ATTEMPTED
WHAT CHANGED
WHAT WAS PROVEN
WHAT FAILED
WHAT WAS LEARNED
WHAT IS UNKNOWN
PROTECTED BOUNDARIES
EXACT NEXT ACTION
PASS CONDITION
```

The canonical test is:

> **Can a completely cold Naya execute the next action correctly without reconstructing the prior conversation?**

If not, continuity is incomplete.

---

## 15. Builder → OSCAR → Repair → Verification

For material implementation:

```text
BUILD
 ↓
OSCAR / REVIEW
 ↓
REPAIR
 ↓
RETEST
 ↓
OSCAR / REVIEW
 ↓
VERIFY
 ↓
PROMOTE
```

Review is not proof by itself. It is a challenge against the builder's result.

Verification requires evidence appropriate to the acceptance contract.

---

## 16. Human Agency Contract

The human remains the principal.

Naya Power SHALL optimize for increased human capability rather than increased human dependence.

The system MUST preserve human control over:

- what matters;
- what is authorized;
- what is remembered where applicable;
- what is shared;
- what consequential decisions are made;
- what advice is accepted or rejected.

AI initiative is encouraged within authority boundaries. AI self-authorization is prohibited.

---

## 17. Privacy / Federation Boundary

P-CIS inherits Naya Power privacy principles:

**Private by default • Shared by choice • Collective by consent • Public by decision.**

Personal memory MUST NOT become collective intelligence merely because a connection exists.

Future Naya federation requires explicit permission, controlled exchange, provenance, security, revocation, and auditable boundaries.

---

## 18. Acceptance Test Matrix

P-CIS is technically accepted only when the corresponding existing contracts can prove the behavior.

| Test | Pass condition |
|---|---|
| Authority isolation | Capability alone cannot authorize an action |
| Fail-closed governance | Invalid/unauthorized action is blocked rather than guessed through |
| Action identity | Material action has stable identity and machine-readable state |
| Evidence binding | Material completion claims point to evidence |
| Truth-state separation | UNKNOWN/BLOCKED/FAILED cannot be silently represented as VERIFIED |
| Runtime boundary | Source/build/deployment/runtime claims remain distinct |
| Failure recovery | Known failure records cause, repair, retest, and safeguard/lesson where applicable |
| No-repeat law | Same failed path is not retried without new information |
| State coherence | MAP, STATE, BLOCKS, and PROOF remain coherent |
| Smart Note projection | Action/event meaning survives into durable human-readable intelligence |
| Smart Board projection | Board presents the intelligence spine, provenance, truth, and useful actions |
| Smart Feed projection | Feed preserves object identity/provenance/truth state across events |
| CIS compounding | Derived intelligence references source events and creates reusable learning |
| Provenance preservation | Artifact/commit/run/runtime identity survives representation changes |
| Cold Naya continuity | Successor can restore and continue without conversational archaeology |
| Single next action | Material receipt exposes exactly one highest-value continuation action |
| Human authority | Human remains principal for consequential authorization |
| Privacy boundary | Private memory does not silently become shared/collective memory |
| Browser/UX truth | Runtime visual claims remain UNKNOWN until independently inspected when required |
| Production proof | Production status requires actual runtime evidence, not repository intent |

---

## 19. P-CIS 10/10 Definition

P-CIS reaches the target state when the system can demonstrate all of the following in real operation:

1. **Authority is explicit.**
2. **Actions are identifiable.**
3. **Evidence travels with claims.**
4. **Uncertainty is represented honestly.**
5. **Failure becomes repair information.**
6. **Accomplishments survive session boundaries.**
7. **Memory preserves provenance and currentness.**
8. **Smart Notes preserve meaning.**
9. **Smart Boards make intelligence comprehensible and actionable.**
10. **Smart Feed preserves the living intelligence stream.**
11. **CIS converts experience into higher-order reusable intelligence.**
12. **Governance remains singular and fail-closed.**
13. **Human authority is never silently transferred to the machine.**
14. **A cold successor can continue the work.**
15. **Every material action leaves the system more capable of doing the next one correctly.**

---

## 20. Canonical Relationship to Existing Naya Power Documents

| Existing document/system | Relationship to P-CIS |
|---|---|
| `SUPERBRAIN/AI-BOOT/START-HERE.md` | Defines entry, restore, continuity, no-orphan, and operating behavior |
| `SUPERBRAIN/NAYAPOWER-CANONICAL-SOURCE-MAP.md` | Defines canonical navigation and authority relationships |
| `SUPERBRAIN/NAYA-POWER-INTELLIGENCE-OPERATING-MODEL.md` | Defines the foundational HOW that P-CIS technically binds |
| `.naya/codex/11-RUNTIME-CONSTITUTION.md` | Constitutional runtime authority; P-CIS cannot override it |
| `.naya/control-plane/GOVERNANCE-KERNEL.json` | Machine governance boundary |
| `.naya/control-plane/MAP.json` | Current canonical map |
| `.naya/control-plane/STATE.json` | Current canonical state |
| `.naya/control-plane/BLOCKS.json` | Current active work block |
| `.naya/control-plane/PROOF.json` | Current proof/evidence boundary |
| `.naya/actions/NAYA_ACTION_V1.schema.json` | Atomic machine action contract |
| Hub Read-First set | Mandatory Hub execution gate |
| Smart Note architecture | Durable human-readable intelligence projection |
| Smart Board contract | Human comprehension/action projection |
| Smart Feed contract | Living intelligence projection |
| CIS | Compounding intelligence engine |
| Activity / receipts | Durable execution history and human receipt layer |

This specification binds these systems together; it does not replace them.

---

## 21. Implementation Rules

### Rule 1 — Inspect before change
Resolve live canonical sources and current runtime state before consequential modification.

### Rule 2 — Surgical evolution
Preserve working architecture and functionality. Change only what is necessary to satisfy the accepted objective.

### Rule 3 — Evidence before promotion
Do not promote an implementation based solely on source intent.

### Rule 4 — No invented proof
Never fabricate runs, artifacts, logs, runtime state, screenshots, approvals, or success.

### Rule 5 — No alternate authority
Do not create a second constitution or control plane to resolve disagreement.

### Rule 6 — No orphan
Every material execution ends with a directly executable continuation action.

### Rule 7 — No retry without new information
Repetition is not learning.

### Rule 8 — Preserve failure
Known failures and their repairs are intelligence.

### Rule 9 — Preserve exact accomplishment identity
Where an artifact matters, retain exact identity rather than rebuilding an equivalent artifact and calling it the same accomplishment.

### Rule 10 — Human remains principal
AI may increase initiative, but never silently increase its own authority.

---

## 22. Canonical P-CIS Diagram

```text
                                  HUMAN
                     intent • values • authority
                                      │
                                      ▼
                              ┌──────────────┐
                              │     NAYA     │
                              │ understand   │
                              │ orchestrate  │
                              └──────┬───────┘
                                     │
                                     ▼
                         ┌────────────────────────┐
                         │   GOVERNANCE KERNEL    │
                         │ constitution • policy  │
                         │ authority • safety    │
                         └───────────┬────────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │ NAYA_ACTION_V1  │
                            │ INTELLIGENCE    │
                            │ ACTION          │
                            └────────┬────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
               UNDERSTAND         DECIDE           EXECUTE
                    │                │                │
                    └────────────────┼────────────────┘
                                     ▼
                                  REALITY
                                     │
                                     ▼
                                  OBSERVE
                                     │
                                     ▼
                           ┌─────────────────┐
                           │ EVIDENCE / PROOF│
                           └────────┬────────┘
                                    │
                              ┌─────┴─────┐
                              ▼           ▼
                           VERIFIED    UNKNOWN/FAIL
                              │           │
                              │        REPAIR
                              │           │
                              └─────┬─────┘
                                    ▼
                                  RESULT
                                    │
                                    ▼
                                  LEARN
                                    │
                                    ▼
                                 MEMORY
                                    │
                 ┌──────────────────┼──────────────────┐
                 ▼                  ▼                  ▼
             SMART NOTE           CIS            CONTROL PLANE
                 │                  │                  │
                 ▼                  ▼                  ▼
            SMART BOARD      NEW INTELLIGENCE       STATE'
                 │                  │                  │
                 └──────────────────┼──────────────────┘
                                    ▼
                              NEXT ACTION
                                    │
                                    ▼
                                  TORCH
                                    │
                                    ▼
                                NEXT NAYA
                                    │
                                    ▼
                                  RESTORE
                                    │
                                    └──────────────→ CONTINUE
```

---

## 23. Canonical Definition

> **Naya Power Proof-Carrying Intelligence System (P-CIS)** is the technical architecture by which Naya Power turns human-authorized intelligence into durable, evidence-bearing actions; preserves what was accomplished; represents uncertainty and failure explicitly; converts experience into learning; projects governed intelligence through Smart Notes, Smart Boards, and Smart Feed; compounds that intelligence through CIS; and passes an executable, proof-bearing continuation to the next Naya without transferring human authority to the machine.

The deepest loop is:

**KNOW → ACT → PROVE → LEARN → REMEMBER → CONTINUE**

The governing purpose remains:

> **Maximum Responsible Verified Value per Action and Moment.**

And the human outcome remains:

> **Learn. Create. Remember. Improve. Become.**

---

## 24. Status Boundary

This document defines the canonical **architecture and binding relationships** for P-CIS.

It does **not** claim that every mapped runtime component is fully implemented or currently production-proven.

Implementation status MUST be established from the live repository, control plane, action records, workflow evidence, runtime observation, and applicable verification contracts.

Therefore:

**SPECIFIED ≠ IMPLEMENTED ≠ DEPLOYED ≠ RUNTIME VERIFIED ≠ VISUALLY VERIFIED ≠ HUMAN APPROVED.**

This boundary is part of the specification itself.
