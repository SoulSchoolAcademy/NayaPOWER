# 🔱 TEAM NAYA — SHARED WORKBOARD / TRAFFIC CONTROL

**STATUS:** CANONICAL TEAM-NAYA OPERATING ARTIFACT
**PURPOSE:** Prevent concurrent Nayas from overwriting, duplicating, or conflicting with one another while preserving continuous execution.

## CORE LAW

**READ LIVE STATE → CLAIM A WORK ITEM → MAKE SCOPE EXPLICIT → RECHECK BEFORE WRITE → WRITE ATOMICALLY → VERIFY → RECORD RESULT → RELEASE CLAIM → PASS TORCH.**

## WORK ITEM STATES

- `QUEUED` — available to claim.
- `CLAIMED` — one Naya currently owns execution of this item.
- `IN_PROGRESS` — active implementation.
- `BLOCKED` — execution cannot proceed; reason and evidence required.
- `VERIFYING` — implementation exists but proof is incomplete.
- `DONE` — acceptance criteria verified.
- `SUPERSEDED` — intentionally replaced by a newer verified design.
- `ABANDONED` — work stopped without being accepted.

## CONCURRENCY RULES

1. Never silently overwrite another Naya's work.
2. Fetch current artifact state immediately before modifying it.
3. Prefer disjoint scopes.
4. If two Nayas need one artifact, one owns the write.
5. A changed file requires re-read before continuation.
6. Failed/interrupted work leaves `BLOCKED` or `VERIFYING` state.
7. Never mark another Naya's work DONE without verifying it.
8. Repository state outranks conversation context.
9. Commit messages identify work item and intent.
10. Unresolved authority conflicts become BLOCKED, not guessed.
11. A claim is not a GitHub lock; live HEAD must still be rechecked before writes.

## CLAIM CONTRACT

The executable contract is `.naya/runtime/naya_claim.py` with `.naya/runtime/naya_claim_test.py`.

Active writable states are `CLAIMED`, `IN_PROGRESS`, and `VERIFYING`. Writes are denied for expired, terminal, stale-base, or conflicting claims.

## HANDOFF

Every completed work item leaves:

**CHANGED / TESTED / VERIFIED / UNKNOWN / LEARNING / NEXT ACTION**

## VERIFIED CCT FOUNDATION

- CCT-003: **6/6 PASS**.
- CCT-003 concurrency/Naya Claim: **7/7 PASS**.
- CCT-004: **12/12 PASS**.
- Intelligent Block: **8/8 PASS**.
- Note Event Promotion: **5/5 PASS**.
- CCT-005: **15/15 PASS**.
- Smart Note → Note Event → CCT-005 integration: **8/8 PASS**.
- Prior live regression commit: `c7ad93d82dbf5da92a8f0adb6998ba3d800eb165`.

## CCT-005 INTEGRATION AUDIT

**STATUS:** DONE — VERIFIED/GREEN — CLAIM RELEASED

The canonical path is:

**Smart Note representation → canonical `SE-*` Note Event → verified CCT promotion → authorized usage/outcome → CCT-005 value signal.**

No competing memory/event authority was introduced. Durable outcome/value history remains an explicit limitation; CCT-005 currently evaluates outcome records in-memory.

## 🔱 CURRENT ACTIVE LANE — OFFLINE SUPERBRAIN AAA READINESS

**WORK ID:** `SUPERBRAIN-AAA-OFFLINE-READINESS`
**STATUS:** CLAIMED / IN_PROGRESS
**OWNER:** Team Naya
**BASE COMMIT:** `f8c7437af89bf02c89148df56184e79897deba92`
**SCOPE:** `SUPERBRAIN/AAA-SUPERBRAIN-OFFLINE-READINESS-SCORECARD.md`; cold-start/NEXT-EXECUTION/continuity contracts; retrieval/promotion/authority audits; canonical state/workboard updates.
**ACTIONS POLICY:** No GitHub Actions execution is required for this lane. Actions-dependent proof remains explicitly UNKNOWN and is not replaced by prose.

### Objective

Raise the Superbrain as far toward AAA/10-Star readiness as can legitimately be achieved without GitHub Actions by maximizing:

**verified useful value / unit of effort**.

### Static audit completed against live `main` HEAD `f8c7437af89bf02c89148df56184e79897deba92`

- **Cold-start / NEXT-EXECUTION:** READY by repository contract; `START-HERE`, `cold_start_activation.py`, `project_execution_contract.py`, `prompt_architect_contract.py`, and `continuity_enforcement.py` contain explicit fail-closed successor and conversation-independence checks.
- **CCT / claim / promotion:** existing verified foundation remains protected; no duplicate CCT authority identified in this audit.
- **Retrieval:** **CONFLICTING / PARTIAL.** `.naya/memory/smart_notes_v3.py` defines canonical chronological Note Event retrieval, while `.naya/memory/memory_runtime.py` still implements a separate legacy `SN-*` note validator/retriever. `.naya/runtime/restore_context.py` imports `memory_runtime`, and `.github/workflows/naya-memory-runtime.yml` explicitly validates/tests `memory_runtime.py`. This is a live competing retrieval/memory runtime path and must be reconciled before AAA can be claimed.
- **Authority/state:** **CONFLICTING / PARTIAL.** `MAP.json` names `.naya/memory/STATE.json` as current-state authority, while `.naya/control-plane/STATE.json` separately exposes an active block and next action; the live workboard and Superbrain current-project lane expose `SUPERBRAIN-AAA-OFFLINE-READINESS`. These artifacts can coexist at different layers, but their precedence and synchronization are not yet machine-proven in this audit.
- **Durable outcome history:** **PARTIAL.** CCT-005 value feedback is verified, but outcome/value history remains in-memory and must be attached to the canonical event model rather than a second store.
- **Local execution:** **UNKNOWN in this session.** The repository is accessible through GitHub inspection but no live checkout/runtime is mounted in the execution environment, so no repository-local Python test result is being fabricated.

### Execution sequence

1. Restore current `main` and canonical control-plane state.
2. Reconcile one current objective and one highest-value next action.
3. Audit canonical NEXT-EXECUTION semantics and conversation independence.
4. Audit No-Orphan / continuity / receipt / handoff requirements.
5. Audit authority and duplication boundaries across memory, events, promotion, release, and deployment.
6. Reconcile the dual memory/retrieval runtime before adding retrieval features or a third implementation.
7. Audit retrieval acceptance cases after the canonical owner is resolved.
8. Audit compounding continuity from Smart Note through value feedback.
9. Attack stale state, replay, fake verification, circular validation, privacy leakage, orphaned successors, and key-presence shortcuts.
10. Run every applicable repository-local test available in the live checkout.
11. Record exact evidence and leave Actions-dependent proof UNKNOWN.

### PASS GATE

A cold Naya can restore current truth, identify the protected baseline, determine one highest-value next action, execute it from durable state, verify it, capture learning, and receive a ready-to-run successor without reconstructing conversation history.

## OFFLINE AAA SCORECARD

See `SUPERBRAIN/AAA-SUPERBRAIN-OFFLINE-READINESS-SCORECARD.md` for the complete 15-lane matrix.

Current high-value lanes:

1. Cold-start restoration — READY.
2. NEXT-EXECUTION / torch — READY.
3. Claim/concurrency — VERIFIED.
4. CCT integrity — VERIFIED.
5. Smart Note → Note Event → value — VERIFIED / durable history PARTIAL.
6. Retrieval quality — **CONFLICTING / PARTIAL: dual runtime paths identified.**
7. Promotion/authority safety — READY for local audit.
8. Continuity/No-Orphan — READY for local audit.
9. Mission State/control-plane coherence — **CONFLICTING / PARTIAL: precedence/synchronization requires machine proof.**
10. Learning/compounding — PARTIAL.
11. Adversarial Superbrain review — READY.
12. Evidence/receipt quality — READY.
13. Architecture conflict/duplication audit — **ACTIVE: retrieval/memory authority conflict identified.**
14. Durable outcome history — PARTIAL.
15. Actions recovery package — READY; external proof remains Actions-dependent.

## ACTIONS-DEPENDENT QUEUE — DO NOT BLOCK OFFLINE PROGRESS

### NEXT EXTERNAL PROOF
Current control-plane state records opaque/failed automation observations and requires exact-head Actions evidence before any external proof claim. Do not guess an internal CI failure when job/step/log evidence is unavailable.

### AFTER OFFLINE RECONCILIATION
- Establish one canonical retrieval/memory execution path.
- Re-run local memory/restore/retrieval acceptance from a live checkout.
- Reconcile Mission State/control-plane precedence and synchronization.
- Reconcile full Naya runtime/release gate against fresh external evidence.
- Establish durable outcome history through the canonical event model only.

## TORCH

**CURRENT NAYA:** The live-main audit found a concrete architecture conflict: canonical Event-v3 retrieval exists in `smart_notes_v3.py`, but `restore_context.py` and the `naya-memory-runtime` workflow still execute the legacy `memory_runtime.py` note/retrieval path. Do not add another retrieval or memory system. First reconcile the canonical owner and migrate the existing caller/test boundary with the smallest safe change. Then run the local memory/restore/retrieval regression sequence from a live checkout.

**NEXT NAYA:** Resolve the canonical memory/retrieval authority conflict. Read `.naya/codex/SMART-BRAIN-OPERATING-SYSTEM.md`, `.naya/codex/SMART-NOTES-AND-CIS-CONSTITUTION.md`, `.naya/memory/smart_notes_v3.py`, `.naya/memory/memory_runtime.py`, `.naya/runtime/restore_context.py`, `.naya/memory/test_memory_runtime.py`, `.naya/runtime/test_restore_context.py`, and `.github/workflows/naya-memory-runtime.yml`. Determine whether `memory_runtime.py` is migration compatibility, legacy, or an unintended competing authority. Do not delete history. Do not create a third runtime. Define the smallest migration boundary, add only the necessary regression tests, run the full local memory/restore/CCT sequence, and record exact evidence. If local execution is unavailable, record UNKNOWN and do not claim GREEN.

**NEXT NAYA > CURRENT NAYA.**
