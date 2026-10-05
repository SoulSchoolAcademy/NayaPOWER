# NayaPOWER Brain — Master Map V1

**Status:** PROPOSED CANONICAL — HUMAN DIRECTOR RATIFICATION REQUIRED  
**Purpose:** The single human/AI-readable map of the NayaPOWER brain.

> **Reconciliation note (2026-09-30):** Brain-level status is PROPOSED pending Human-Director ratification. Individual files carry their own status declarations (see file headers); where a file claims CANONICAL and this map says PROPOSED, both statements are preserved as written — the Human Director owns the ratification decision, not this map.

**Key references:**
- [REAL-TREE.md](./REAL-TREE.md) — machine-verified file inventory
- [12-ENGINEERING/0002-BRAIN-AAA-SCORECARD-V1.md](./12-ENGINEERING/0002-BRAIN-AAA-SCORECARD-V1.md) — AAA quality scorecard

## 1. What this map means

This map answers four questions immediately:

- **WHERE** is a responsibility?
- **WHAT** is its canonical semantic home?
- **HOW** does it connect to the rest of the system?
- **WHAT PROVES** that it works?

The repository tree is navigation. It is not the brain by itself.

The living brain is the combination of:

**CANONICAL OBJECTS + RELATIONSHIPS + CONTRACTS + PROVENANCE + MEMORY + KERNEL BEHAVIOR + PROOF + LEARNING + SUCCESSION**

## 2. Canonical brain layers

The repository-level master design, CONSTITUTION, GOVERNANCE, and ARCHITECTURE surfaces sit above and outside the BRAIN directory. There is no literal `ROOT/` directory; repository-root paths below are exact.

```
REPOSITORY ROOT/
├── 0000-NAYAPOWER-MASTER-DESIGN-CONTRACT-V1.md
├── CONSTITUTION/          ← human-level principles (outside BRAIN)
├── GOVERNANCE/            ← authority, consent, change control (outside BRAIN)
├── ARCHITECTURE/          ← system design (outside BRAIN)
└── BRAIN/
    ├── 00-SPEC/           ← definitions, schemas, naming laws
    ├── 01-GOVERNANCE/     ← brain-level governance contracts
    ├── 02-ARCHITECTURE/   ← brain-level boundaries
    ├── 03-KERNEL/         ← nine-node semantic runtime
    ├── 04-INTELLIGENCE/   ← durable objects, events, relationships
    ├── 05-MEMORY/         ← retention, indexing, retrieval
    ├── 06-PROOF/          ← evidence, verification, causal acceptance
    ├── 07-LEARNING/        ← candidate and verified learning
    ├── 08-SUCCESSION/     ← cold boot, handoff, continuity
    ├── 09-EVOLUTION/      ← governed self-improvement
    ├── 10-INTERFACES/     ← Hub, API, NayaNET projections
    ├── 11-KNOWLEDGE/      ← distilled domain knowledge
    ├── 12-ENGINEERING/    ← implementation, runtime, deployment
    ├── 90-OPERATIONS/     ← current operational truth
    └── 99-ARCHIVE/        ← historical material
```

| Address | Layer | Canonical responsibility |
|---|---|---|
| REPO ROOT | CONSTITUTION | Human-level governing principles |
| REPO ROOT | GOVERNANCE | Authority, consent, change, promotion and revocation |
| REPO ROOT | ARCHITECTURE | System boundaries, dependencies and composition |
| 00 | SPEC | Definitions, schemas, naming and representation laws |
| 01 | GOVERNANCE | Brain-level governance contracts |
| 02 | ARCHITECTURE | Brain-level boundaries and dependencies |
| 03 | KERNEL | Nine-node semantic runtime |
| 04 | INTELLIGENCE | Durable objects, events and relationships |
| 05 | MEMORY | Retention, indexing, retrieval and reconciliation |
| 06 | PROOF | Evidence, verification, causal acceptance |
| 07 | LEARNING | Candidate learning, verified learning and compounding |
| 08 | SUCCESSION | Cold boot, handoff and continuity |
| 09 | EVOLUTION | Governed self-improvement and system evolution |
| 10 | INTERFACES | Hub, API, NayaNET and other projections |
| 11 | KNOWLEDGE | Distilled domain knowledge and source lineage |
| 12 | ENGINEERING | Implementations, runtime, deployment and recovery |
| 90 | OPERATIONS | Current operational truth, health and procedures |
| 99 | ARCHIVE | Historical and superseded material |

## 3. The semantic kernel

Exactly nine V1 responsibilities exist:

**SELF → LAW → ACT → KNOW → PROVE → CONNECT → VERIFY → LEARN → EVOLVE → SELF**

They are semantic organs of one kernel.

They are not nine databases, nine products, nine memories, or nine authorities.

## 4. The intelligence object model

The canonical persisted machine object behind the current **Smart Node** operating command is an **Intelligent Block**.

“Make this a Smart Node” means route valuable material through the existing governed intelligence river. It does **not** create a tenth Master Node, another canonical object family, another graph, or another persistence path.

An Intelligent Block should remain identity-, owner/scope-, provenance-, epistemic-state-, applicability-, evidence-, relationship-, freshness-, verification-, supersession- and successor-aware.

Older source/concept material may use **Naya Node / Intelligent Node** as semantic terminology. Preserve that lineage without turning it into a competing persistence object.

A capture artifact is not automatically verified intelligence.

## 5. The intelligence chain

**EXPERIENCE → CAPTURE → DISTILL → STRUCTURE → CONNECT → PROVE → PRESERVE → RETRIEVE → APPLY → ACT → OUTCOME → VERIFY → LEARN → COMPOUND → SUCCESSOR → EVOLVE**

Every meaningful transition must have an owner, input, output, authority requirement, proof requirement, and failure behavior.

## 6. Truth model

Never collapse these:

- source vs interpretation
- event vs understanding
- understanding vs lesson
- lesson vs verified learning
- capability vs authority
- implementation vs verification
- verification vs production proof
- retrieval vs authorization
- successor context vs authority
- confidence vs truth
- storage vs intelligence
- UI projection vs canonical state

## 7. Brain entry sequence for a cold Naya

A cold Naya reads and verifies:

1. **CONSTITUTION/0000-NAYAPOWER-CONSTITUTION-ACT-V1.md** — governing principles
2. **GOVERNANCE/0000-NAYAPOWER-GOVERNANCE-CONTRACT-V1.md** — authority and consent
3. **BRAIN/01-GOVERNANCE/0004-NONSTOP-LOOP-V1.ai.md** — standing execution loop for every Naya seat
4. **0000-NAYAPOWER-MASTER-DESIGN-CONTRACT-V1.md** — master design
5. **ARCHITECTURE/0000-NAYAPOWER-SUPERBRAIN-MASTER-SPEC-V1.md** — superbrain spec
6. **BRAIN/MASTER-MAP.md** — this map
7. **BRAIN/03-KERNEL/MANIFEST.json** + node contracts — declared kernel/runtime-binding state
8. **BRAIN/90-OPERATIONS/0001-MAX-10-EXECUTION-QUEUE-V1.md** + **0003-ULTIMATE-MASTER-EXECUTION-PLAN-V1.md** — current execution projection
9. **Live GitHub main / open priority work / current runtime and proof evidence** — fresher evidence outranks dated projections
10. **BRAIN/04-INTELLIGENCE/** — relevant canonical intelligence
11. **BRAIN/06-PROOF/** — evidence and verification
12. **BRAIN/08-SUCCESSION/** — successor context

The system must be discoverable without Shawn reconstructing it.

## 8. Canonical source rule

Every semantic responsibility has one canonical owner.

Other representations are explicitly classified as:

**PROJECTION / CACHE / DERIVED / HISTORICAL / EXPERIMENTAL / ARCHIVE**

No projection may silently become authority.

## 9. Current proof and execution status

NayaPOWER has one important bounded production-proven intelligence specimen, but the entire architecture is not universally production-proven.

**Issue #913 bounded proof:** exact source/deployed revision `0dcff9b815039d20a7c4c06e05da3a8d9fab5ba4` demonstrated:

**experience → durable intelligence → paired WITHOUT/WITH behavior delta → measurable outcome → independent recomputation → ACTIVE learning → identifier-only cold retrieval → successor reuse without inherited authority**

That receipt is deliberately narrow. Later `main` does not inherit its production status, and it does not prove universal runtime binding, generalized applicability, multi-generation compounding, or NayaNET scale.

**Issue #944 Phase 1:** Concept #17 reconciliation returned `NO_NEW_CANDIDATE — SOURCE RECONCILED`. Do not create a duplicate Concept #17 Smart Node. Its surviving value is behavioral test pressure on existing architecture.

### Current dependency-correct queue

> **Reconciliation note (2026-09-30):** the embedded queue table that lived here dated from the September 2026 hardening era and was superseded by the refreshed queue. It has been removed to prevent cold-start confusion; its history is preserved in Git. The current queue is `BRAIN/90-OPERATIONS/0001-MAX-10-EXECUTION-QUEUE-V1.md` — always resolve that live file, never an embedded copy.

Canonical execution surfaces:

- `BRAIN/90-OPERATIONS/0001-MAX-10-EXECUTION-QUEUE-V1.md`
- `BRAIN/90-OPERATIONS/0003-ULTIMATE-MASTER-EXECUTION-PLAN-V1.md`
- `BRAIN/90-OPERATIONS/0003-ULTIMATE-MASTER-EXECUTION-PLAN-V1.json`
- `BRAIN/90-OPERATIONS/0004-ISSUE-944-CONCEPT-17-RECONCILIATION.md`

**Do not reopen semantic architecture merely because a review proposed a sophisticated replacement. Repair the first broken proof rung.**

## 10. Acceptance

The brain is operationally real only when a cold authorized Naya can:

**DISCOVER → RESTORE → RETRIEVE → UNDERSTAND → AUTHORIZE → APPLY → ACT → OBSERVE → VERIFY → LEARN → HANDOFF → CONTINUE**

and the next Naya demonstrably performs better because the retained intelligence survived.

**PATH IS NAVIGATION. ID IS IDENTITY. PROOF IS REQUIRED.**
