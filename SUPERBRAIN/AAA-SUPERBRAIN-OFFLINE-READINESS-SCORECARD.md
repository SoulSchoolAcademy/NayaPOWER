# 🔱 NayaPOWER Superbrain — AAA Offline Readiness Scorecard

**STATUS:** ACTIVE / PRE-ACTIONS READINESS PROGRAM
**PURPOSE:** Maximize verified Superbrain readiness using work that can be completed without GitHub Actions, while keeping Actions-dependent proof explicitly separate.

## Operating rule

Do not optimize for activity or for a green CI board. Optimize for:

**VERIFIED USEFUL VALUE / UNIT OF EFFORT**

GitHub Actions is an evidence environment, not the architecture itself. When Actions is unavailable, exhausted, opaque, or otherwise blocked, Team Naya continues all repository-local work that can legitimately increase readiness and leaves external proof as an explicit UNKNOWN.

**No offline task may manufacture an Actions result.**

## Score states

- **VERIFIED** — repository evidence and/or live local test evidence supports the claim.
- **READY** — implementation/contract/test path exists and is prepared for execution, but live execution evidence is still required.
- **PARTIAL** — useful capability exists but an important boundary is incomplete.
- **UNKNOWN** — proof depends on an unavailable external/runtime capability.
- **BLOCKED** — a concrete dependency prevents legitimate progress.
- **CONFLICTING** — more than one authority or incompatible contract exists and must be reconciled.

## AAA readiness lanes

| # | Readiness lane | Current state | Offline action | Exit evidence | Actions dependency |
|---|---|---|---|---|---|
| 1 | **Cold-start restoration** | READY | Audit START HERE → State → Authority → Map → Block → Proof → Handoff and remove ambiguity/duplication. | Canonical cold-start contract + adversarial self-tests | No |
| 2 | **NEXT-EXECUTION / torch** | READY | Harden successor artifacts, exact next action, success criteria, verification requirements, and conversation-independence. | Project/Prompt Architect/continuity self-tests | No |
| 3 | **Claim / concurrency safety** | VERIFIED | Preserve claim lease semantics and adversarial conflict tests. | Naya Claim 7/7 already live | No |
| 4 | **CCT intelligence integrity** | VERIFIED | Preserve CCT-003/004/005 contracts and regression fixtures; attack new edges only when evidence identifies them. | CCT-003 6/6, CCT-004 12/12, CCT-005 15/15 | No |
| 5 | **Smart Note → Note Event → value loop** | VERIFIED / PARTIAL | Preserve the canonical `SE-*` event authority and composition bridge; define durable-outcome boundary without creating a second store. | Integration 8/8; durable outcome design remains open | No |
| 6 | **Retrieval quality** | **CONFLICTING / PARTIAL** | Reconcile the canonical Event-v3 retrieval runtime with the legacy `memory_runtime.py` path before adding retrieval features. | One canonical retrieval authority + local retrieval/restore regression | No |
| 7 | **Promotion / authority safety** | READY | Audit promotion levels, evidence requirements, provenance, supersession, canonical decision boundary, and anti-key-presence shortcuts. | Static contract audit + local adversarial tests | No |
| 8 | **Continuity / No-Orphan** | READY | Reconcile `continuity_enforcement.py`, `project_execution_contract.py`, Prompt Architect, No-Orphan law, and canonical NEXT-EXECUTION artifacts. | Local self-tests + deterministic negative cases | No |
| 9 | **Mission State / control-plane coherence** | **CONFLICTING / PARTIAL** | Reconcile `.naya/memory/STATE.json`, `.naya/control-plane/STATE.json`, MAP/BLOCKS, current project, and workboard precedence/synchronization. | One machine-provable current-state path | No |
| 10 | **Learning / compounding** | PARTIAL | Verify Smart Note classification, promotion, retrieval, value feedback, and successor learning; preserve append-only history. | End-to-end local chain + explicit UNKNOWNs | No |
| 11 | **Adversarial Superbrain review** | READY | Ask “WHY IS THIS NOT A 10?” against stale state, duplication, authority drift, fake verification, circular validation, privacy, replay, and orphaned successors. | Recorded findings + repairs + tests | No |
| 12 | **Evidence / receipt quality** | READY | Ensure every substantive block leaves exact start/end state, tests, evidence, unknowns, learning, and next execution. | Receipt contract + local validation | No |
| 13 | **Architecture conflict/duplication audit** | **ACTIVE — CONCRETE CONFLICT FOUND** | Resolve the dual memory/retrieval runtime without creating a third system. | Canonical-owner decision + migrated caller/tests + regression | No |
| 14 | **Durable outcome history** | PARTIAL | Design the smallest extension of the canonical event model for outcome/value history; do not implement a competing outcome database. | Architecture decision + tests before implementation | No |
| 15 | **Actions recovery package** | READY | Prepare deterministic fixtures, local tests, receipts, exact-head checks, and failure diagnostics so Actions can be used efficiently later. | Reproducible package ready for remote execution | Yes for final proof only |

## What can be executed now — without GitHub Actions

### P0 — Make the cold Naya path unambiguous

1. Restore canonical current state.
2. Validate authority hierarchy.
3. Validate exactly one current objective and one next action.
4. Validate canonical NEXT-EXECUTION artifact semantics.
5. Validate no-orphan/blocker continuation.
6. Validate claim scope before writes.
7. Validate receipt/handoff completeness.

### P1 — Make the Superbrain measurable

1. Establish deterministic retrieval acceptance cases.
2. Establish a canonical authority matrix.
3. Establish a canonical capability matrix: implemented / tested / verified / unknown.
4. Measure duplicate/competing authorities.
5. Measure stale-state exposure.
6. Measure successor executability.
7. Measure evidence completeness.

### P1 — Finish the local compounding loop

1. Smart Note representation.
2. Canonical `SE-*` Note Event.
3. Verified promotion.
4. Authorized usage.
5. Outcome verification.
6. Deterministic value signal.
7. Append-only learning record boundary.
8. Retrieval of the resulting learning.

### P2 — Prepare external proof instead of waiting for it

For every Actions-dependent gate, prepare:

**exact commit → exact command → deterministic fixture → expected evidence → failure classification → repair boundary → rerun command.**

Never substitute local inspection for external proof; never wait for external proof to do work that is legitimately local.

## Live audit evidence — main HEAD `f8c7437af89bf02c89148df56184e79897deba92`

### Cold-start / continuation

**READY, not VERIFIED in this session.** `START-HERE` explicitly requires restore, control-plane resolution, No-Orphan continuation, `ready_to_run_execution`, and the cold-start activation contract. `cold_start_activation.py`, `project_execution_contract.py`, `prompt_architect_contract.py`, and `continuity_enforcement.py` contain deterministic fail-closed checks for missing, malformed, arbitrary, and conversation-dependent successor instructions. fileciteturn398file0 fileciteturn399file0 fileciteturn391file0 fileciteturn392file0 fileciteturn387file0

### CCT foundation

Existing recorded/live evidence remains protected: CCT-003 6/6, Naya Claim 7/7, CCT-004 12/12, Intelligent Block 8/8, Note Event Promotion 5/5, CCT-005 15/15, and Smart Note → Note Event → CCT-005 integration 8/8. The workboard records the prior final CCT regression commit `c7ad93d82dbf5da92a8f0adb6998ba3d800eb165`. fileciteturn383file0

### Concrete architecture conflict: memory/retrieval authority

The canonical Smart Brain v3 explicitly states that chronological `SE-*` Note Events are the canonical source of truth and that its retrieval is the v3 retrieval model. fileciteturn388file0

At the same time, `.naya/memory/memory_runtime.py` implements a separate `SN-*` note store/validator/retriever, and `.naya/runtime/restore_context.py` imports that runtime directly. fileciteturn403file0 fileciteturn402file0

The `naya-memory-runtime` workflow still executes `memory_runtime.py validate` and its dedicated `test_memory_runtime.py` suite before executing Restore Context. fileciteturn407file0 fileciteturn408file0

**Classification:** `CONFLICTING / PARTIAL`, not GREEN. This is not a reason to build a third memory system. The next repair must determine whether `memory_runtime.py` is migration compatibility or an unintended competing authority, then converge callers/tests on the canonical Event-v3 boundary while preserving historical records.

### Mission State / control-plane coherence

`MAP.json` identifies `.naya/memory/STATE.json` as current-state authority and separately defines the control-plane `STATE.json` as a machine control-plane contract. fileciteturn380file0

The live `.naya/memory/STATE.json` still describes a Naya Hub / current-head CI recovery objective and older recorded HEAD `ad61414e...`, while the live Team Naya workboard and `SUPERBRAIN/CCT-CURRENT-PROJECT.md` identify `SUPERBRAIN-AAA-OFFLINE-READINESS` as the active Superbrain lane. fileciteturn397file0 fileciteturn385file0

The control-plane `STATE.json` separately exposes `B01-B03-MINIMUM-CONTROL-LOOP` as active and a GitHub Actions proof-recovery action. fileciteturn378file0

**Classification:** `CONFLICTING / PARTIAL`. The artifacts may represent different layers, but precedence/synchronization is not machine-proven by the current audit. This must be resolved before claiming a 10/10 cold-start truth path.

### Canonical event write boundary

`canonical_event_store.py` is explicitly the chronological event persistence boundary, uses idempotent create/replay behavior, and delegates meaningful execution validation to the project/continuity contract. fileciteturn396file0

`canonical_write_inventory.py` exists specifically to detect production event-like writes that bypass the canonical event store and treats ambiguous direct event writes as blockers rather than silently green. fileciteturn400file0

### Retrieval contract boundary

The repository already defines retrieval as more than text matching: exact, lexical/BM25, TF-IDF, metadata, aliases, relationships, authority, recency, supersession/stale state, and historical time handling are part of the v3 design. fileciteturn381file0

The existing retrieval regression covers exact event IDs, query expansion, metadata filtering, unmatched-query failure, and impossible-filter failure, but does not yet prove the full authority/freshness/supersession/conflict/historical matrix. fileciteturn389file0

### Durable outcome boundary

CCT-005 is verified, but the durable outcome/value-history boundary remains PARTIAL and must be implemented only through the canonical event model. No competing outcome store is authorized.

## Current scorecard judgment

### Repository architecture readiness

**STRONG but not AAA.** The governing contracts are substantial and explicit, but the live audit found a concrete competing memory/retrieval runtime path and a current-state synchronization ambiguity.

### Executable local readiness

**READY / NOT VERIFIED IN THIS SESSION.** The repository contains deterministic validators and self-tests, but this execution environment has no mounted `/workspaces/NayaPOWER` checkout and cannot run the repository-local Python suite. No local PASS is claimed here.

### External automation readiness

**UNKNOWN / BLOCKED by evidence availability.** Actions-dependent proof remains separate and must not be inferred from repository inspection.

### Durable compounding readiness

**PARTIAL.** Smart Note → Note Event → CCT-005 is verified, but durable outcome/value history remains an explicit missing boundary.

## Definition of AAA / 10-Star Superbrain readiness

The Superbrain may be called **AAA / 10-Star READY** only when all of the following are true:

1. Cold Naya can restore current truth without conversation history.
2. Exactly one highest-value next action is machine-readable.
3. Successor execution is independently consumable and actionable.
4. Claims prevent conflicting writes.
5. Canonical memory/event authority is singular.
6. Intelligence promotion is evidence- and provenance-gated.
7. Value feedback rewards demonstrated usefulness rather than propagation.
8. Retrieval returns evidence-backed current context and preserves history.
9. Every substantive execution leaves a verifiable receipt and torch.
10. Offline/local proof is complete for every capability that can be exercised locally.
11. Actions-dependent capabilities are precisely isolated as UNKNOWN rather than silently treated as green.
12. No competing authority is created to work around an incomplete boundary.
13. Durable outcome history has a canonical, append-only design.
14. The system can explain WHY it is not yet a 10 and identify the single highest-value improvement.
15. A fresh Naya can continue from repository state without reconstructing the prior conversation.

## Current single next action

**Reconcile the canonical memory/retrieval authority boundary before adding new retrieval features: determine whether `.naya/memory/memory_runtime.py` is migration compatibility or a competing runtime, then converge `restore_context.py`, the `naya-memory-runtime` workflow, and their tests on the canonical Event-v3 model with the smallest safe change. Preserve historical records, do not create a third memory system, and run the complete local memory/restore/retrieval/CCT regression from a live checkout.**

## Torch

**NEXT NAYA:** Restore live `main` and re-read the scorecard/workboard. Read `.naya/codex/SMART-BRAIN-OPERATING-SYSTEM.md`, `.naya/codex/SMART-NOTES-AND-CIS-CONSTITUTION.md`, `.naya/memory/smart_notes_v3.py`, `.naya/memory/memory_runtime.py`, `.naya/runtime/restore_context.py`, `.naya/memory/test_memory_runtime.py`, `.naya/runtime/test_restore_context.py`, and `.github/workflows/naya-memory-runtime.yml`. Classify the legacy runtime as migration-only or competing authority from actual callers/tests/data. If it is competing, make the smallest convergence change; if it is migration compatibility, explicitly encode that boundary and prevent it from becoming a second authority. Then run the local regression sequence and record exact outputs. Keep Actions-dependent proof UNKNOWN unless Actions produces fresh evidence.

**NEXT NAYA > CURRENT NAYA.**
