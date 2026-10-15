# SYSTEM-BLUEPRINT-20261009 — AI decision framing

## Reach for this when

You need to decide what to build next in NayaPOWER, what the acceptance bar is, or whether a component is real or spec-only. This is the build manual — the vision (§1), the nine nodes (§2), the learning lifecycle (§3), what's connected (§4), what's not (§5), the connection plan (§6), what "done right" looks like (§7), and the visual maps (§8).

## The decision facts (carried exactly, not paraphrased)

**The test:** Shawn teaches something once; days later, in a completely new conversation, a completely fresh Naya faces a similar situation — and gets it right, because she pulled the lesson from memory. Everything in the blueprint serves that test.

**The node cycle:** EVOLVE → SELF → LAW → ACT → KNOW → PROVE → CONNECT → VERIFY → LEARN → EVOLVE → … (with feedback arcs). Node handshake statuses: SELF→LAW is the only transition with code; the other eight batons exist as unratified CANDIDATE prose — `grep ExecutionHandoff` across Python/TypeScript returned zero hits.

**The lifecycle wall:** CAPTURE ✅ → GOVERN ✅ → VERIFY ⚠️ → RECORD ✅ → **[WALL: nothing promotes to ACTIVE]** → RETRIEVE ✅ (orphaned — works but feeds nothing) → REUSE 🔴 (no code) → PROVE 🔴 (no code).

## The gap table (decision order — builders start here)

| # | Gap | Severity | Blocks |
|---|-----|----------|--------|
| 1 | CANDIDATE→ACTIVE ladder is a dead end — `apply_elevation()` has zero operational callers | CRITICAL | All learning permanence |
| 2 | ACT never queries KNOW — decision math is dead code | CRITICAL | All intelligent decisions |
| 3 | Nine node specs CANDIDATE, zero wiring | CRITICAL | The entire pipeline |
| 4 | ACT→KNOW feedback arc missing | HIGH | Learning from outcomes |
| 5 | SELF accepts unverified lessons | HIGH | Memory integrity |
| 6 | EVOLVE has no working code | HIGH | Successor continuity |
| 7 | REUSE + PROVE have no code | HIGH | Compounding |
| 8 | Retrieval predicate bypassed | MEDIUM | Governance |
| 9 | Phantom executable named in ops plan | MEDIUM | Trust in docs |

## The build order (dependency-respecting — parallelize only where independent)

1. **Phase 1 — Unblock the Flow (Gaps 1, 8):** wire the elevation ladder (`elevate`/`ratify`/`activate` CLI on `tools/smart_note_v2.py`); enforce the retrieval predicate (`retrieval_eligible` from `kernel/value_calculus.py` in `retrieve()`).
2. **Phase 2 — Connect Decision to Memory (Gap 2):** build the ACT→KNOW query path (truth floor VERIFIED, top 5 with provenance); wire `evaluate_candidates()` as the decision engine (LAW PROHIBITED still short-circuits — LAW runs before math, always).
3. **Phase 3 — Build the Missing Lifecycle Steps (Gaps 4, 7):** `ExecutionHandoff` dataclass + `ingest_execution()` in KNOW; REUSE (`retrieve_applicable_intelligence` at truth floor ACTIVE, max 3); PROVE (`prove_execution()`, verdict written back to KNOW with lineage; MISMATCH flags, never silent).
4. **Phase 4 — Harden Identity and Succession (Gaps 5, 6):** gate `SELF.record_experience()` to `smart_note_id` with truth_state ≥ VERIFIED (else REFUSED); build the EVOLVE successor package (all fields + sha256 hash + verification).
5. **Phase 5 — Fix the Docs (Gap 9):** correct the ops plan to name `kernel/value_calculus.py` (which exists), noting caller status. Independent — do anytime.

Phases 4 and 5 are independent of the Phase 1→2→3 chain and may run in parallel.

## What "done" does and does not mean

- ❌ Code written. Tests passing on mock data. "It should work." Shawn saying it's fine.
- ✅ The §7 acceptance criteria met **with evidence** — the registry JSON diff, the decision log with intelligence populated, the KNOW query returning the execution edge, the package hash validating. Then the 14-step ultimate test (§7): cold Naya retrieves the lesson and applies it correctly, behavior changed because of the lesson — not coincidence.

## Status caveat (carry it, don't smooth it)

CANDIDATE, v1.0, 2026-10-09. Section 4's numbers and CI states are a dated snapshot; all nine node specs were CANDIDATE at write time; gaps may have moved since. Treat §4–§5 as evidence to re-verify, §6–§7 as the standing build contract.

## Circle links

- 📋 Board: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537 (live coordination)
- 📜 Master Directive: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2601
- Owning doc: `BRAIN/00-ARCHITECTURE/SYSTEM-BLUEPRINT-20261009.md`
- Paired tongues: `SYSTEM-BLUEPRINT-20261009.human.md` · `system-blueprint-20261009.machine.json`
