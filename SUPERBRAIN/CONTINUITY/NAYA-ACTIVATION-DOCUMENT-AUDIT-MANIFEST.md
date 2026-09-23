# NAYA POWER — ACTIVATION DOCUMENT AUDIT & BUILD MANIFEST

**STATUS:** ACTIVE EXECUTION ARTIFACT
**DATE:** 2026-08-26
**OBJECTIVE:** Bring the portable Naya activation package from architectural design to verified cold-start readiness.
**GOVERNING SPEC:** `SUPERBRAIN/NAYA-ACTIVATION-SYSTEM-SPECIFICATION.md`
**GOVERNING ARCHITECTURE:** `SUPERBRAIN/MASTER-SYSTEMS-ARCHITECTURE.md`
**TRACKER:** GitHub Issue #56

> This manifest is an execution map. A document being listed here does not mean it is already verified as a complete portable activation document.

## 1. CANONICAL 12-LAYER ORDER

1. Master Governing Protocol — Human Maximus Digital Codex
2. Naya Modes & Orchestration
3. Naya Lead
4. Naya Master
5. Naya Coder
6. Naya Designer
7. Naya Notes / Memory
8. Naya Nitro / Execution
9. Naya Oscar / Independent QA
10. Superbrain / CIS
11. Scorecard / Verification
12. SOM(E) System Optimization

The canonical order was reconciled on 2026-08-26 after an internal inconsistency was found in the architecture table. The master architecture is now aligned with Issue #56 and the repository README.

## 2. EXISTING CANDIDATE OWNERS

| Layer | Candidate owner(s) | Preliminary state | Main action |
|---|---|---|---|
| 01 Master Law | `NAYA LAW ACTIVATION`; `docs/NAYA-LAW-MASTER-ACTIVATION-SPECIFICATION.md`; `docs/NAYA-DIGITAL-CODEX-MASTER-GUIDE.md` | Strong | Consolidate authority; preserve domain law |
| 02 Modes | `NAYA MODES ACTIVATION`; `docs/NAYA-POWER-AI-SUPERCHARGER-MODES-ACTIVATION.md` | Strong | Normalize modes vs human activity states |
| 03 Lead | `docs/NAYA-LEAD-MODE.md`; `docs/NAYA-LEAD-EXECUTION-COMMUNICATION-PROTOCOL.md` | Strong | Merge/generalize portable owner |
| 04 Master | `NAYA MASTER PLAN`; `docs/NAYA-MASTER-EXECUTION-GATE.md`; Master section of Modes | Incomplete owner | Create one portable orchestration owner |
| 05 Coder | `NAYA MASTER CODER ACTIVATION`; `docs/NAYA-MASTER-DESIGN-CODER-LAWS.md` | Strong | Add common activation contract + portable tests |
| 06 Designer | `NAYA MASTER DESIGNER ACTIVATION`; `docs/NAYA-MASTER-DESIGN-CODER-LAWS.md` | Strong | Add common activation contract + portable tests |
| 07 Notes | `🧠 NAYA NOTES ACTIVATION`; `docs/NAYA-NOTES-MASTER-ACTIVATION-SPECIFICATION.md` | Strong | Canonicalize to Note Event / Smart Note model |
| 08 Nitro | `⚡ NAYA NITRO ACTIVATION`; `NAYA-NITRO-BUILD-PROTOCOL.md`; `docs/NAYA-NITRO-MASTER-ACTIVATION-SPECIFICATION.md` | Strong | Consolidate portable owner |
| 09 Oscar | `.naya/runtime/OSCAR.md`; `.naya/runtime/oscar.py`; Lead Oscar section | Capability exists | Create one portable activation owner + challenge suite |
| 10 Superbrain/CIS | `NAYA BRAIN ACTIVATION`; `.naya/codex/SMART-BRAIN-OPERATING-SYSTEM.md`; `SUPERBRAIN/AI-BOOT/START-HERE.md` | Strong | Separate Brain behavior from durable CIS infrastructure |
| 11 Scorecard | `SUPERBRAIN/10-10-SCORECARD.md`; `docs/NAYA-SCORECARDING-SYSTEM.md` | Strong | Add portable verification/acceptance contract |
| 12 SOM(E) | `.naya/codex/NAYA-OPTIMIZATION-AND-EXCELLENCE-LAW.md`; Master Architecture | Strong law | Create explicit portable activation wrapper |

## 3. COMMON ACTIVATION CONTRACT

Every official portable activation document must contain:

1. Identity
2. Layer
3. Version
4. Authority
5. Purpose
6. What activates
7. What it does not activate
8. Inherited laws
9. Dependencies
10. Inputs
11. Activation behavior
12. Behavioral contract
13. Human benefit
14. Output contract
15. Conflict behavior
16. Failure behavior
17. Verification tests
18. Receipt requirements
19. Smart Note requirements where applicable
20. Next Execution behavior
21. Integration behavior
22. Known limitations
23. Definition of done

## 4. CROSS-CUTTING LOCKS

### Human activity states

Naya infers three primary states:

- WORK / PROJECT
- LEARNING
- REFLECTION / CONVERSATION

These are not technical modes the human must select.

### Output Intelligence

`INTENT → ACTIVITY STATE → COMPLEXITY → OUTPUT CONTRACT`

Default target:

**MINIMUM SUFFICIENT + MAXIMUM USEFUL**

### Smart Note semantics

A Smart Note is the complete intelligence representation of a meaningful event. Naya and Human/Shawn notes are perspectives of the same underlying event. A Machine Note is optional when machine-native communication materially helps.

### Activation truth

`RECEIVED → READ → PARSED → UNDERSTOOD → MAPPED → ACTIVATED → VERIFIED → REPORTED → PRESERVED`

Never collapse these states.

## 5. GUIDED VS RAPID ACTIVATION

### Recommended: Guided

`UPLOAD → UNDERSTAND → ACTIVATE → VERIFY → EXPLAIN BENEFIT → RECEIPT → NEXT`

One capability at a time reduces cognitive load, makes failures easier to isolate, teaches the human what each capability does, and creates visible evidence of progress.

### Supported: Rapid

`UPLOAD ALL → INVENTORY → MAP → RESOLVE → ACTIVATE → VERIFY EACH → RECEIPTS → FINAL REPORT`

Batch upload must not become undifferentiated interpretation. Naya must establish authority and dependencies before activation.

## 6. COLD-START TEST MATRIX

Minimum scenarios:

- zero prior context;
- one-by-one full package;
- all-at-once package;
- canonical order;
- reverse order;
- random order;
- 1/12, 3/12, 6/12, 11/12 partial states;
- missing prerequisite;
- duplicate document;
- outdated document;
- unreadable document;
- unknown document;
- contradictory documents;
- interrupted session;
- new session;
- no persistence available;
- conversation output;
- learning output;
- project output;
- reflection output;
- real integrated project execution.

## 7. RELEASE BLOCKERS

1. One canonical portable owner per layer.
2. Common activation contract applied to every owner.
3. Machine-readable activation manifest.
4. Dependency/authority behavior proven in cold start.
5. Behavioral acceptance test for every material capability.
6. Honest partial/failure/conflict states.
7. Human-readable receipts.
8. Integrated one-Naya test.
9. Cold-start proof.
10. Continuity/restore proof where persistence is supported.
11. Independent Oscar challenge.
12. Final scorecard.

## 8. CURRENT VERIFIED FACTS

- The repository identifies `SoulSchoolAcademy/NayaPOWER` main as the canonical governance branch.
- The repository currently reports Superbrain maturity at **8.4/10**, explicitly not 10/10.
- `SUPERBRAIN/AI-BOOT/START-HERE.md` is the mandatory AI entry point and explicitly requires restoration, verification, receipts, and Next Execution.
- The 10-Star constitutional amendment is active and requires Naya to understand, lead, execute, verify, learn, preserve, and continue.
- The Prompt Architect is active and already defines intent-to-execution conversion.
- Runtime activation infrastructure and tests already exist in `.naya/runtime` and `.naya/tests`.
- The portable activation specification now defines the human activation experience, output intelligence, activation states, receipts, verification, cold start, failure handling, and release gates.

## 9. NEXT EXECUTION

Read the remaining candidate owners completely, beginning with Naya Master, Naya Designer, Naya Notes, Naya Nitro, Oscar, Superbrain/CIS, Scorecard, and SOM(E). Score each against the 23-point common activation contract. Preserve strong domain knowledge. Consolidate duplicate authorities. Create or upgrade only the smallest coherent portable owner required for cold-start activation. Then build the manifest and behavioral test suite and execute the cold-start matrix.

**Do not call any layer VERIFIED until its behavioral acceptance evidence exists.**
