# Master Checklist — Activation to Production

**Owner:** Naya 4 (builder seat), Team Naya
**Created:** 2026-10-09 (Shawn's direct order)
**Canonical location:** `BRAIN/00-ACTIVATION/ACTIVATION-CHECKLIST.md`
**Source of truth:** `BRAIN/00-ACTIVATION/ACTIVATION-MASTER-CHECKLIST.json` (this file is GENERATED — do not hand-edit)
**Status as of:** 2026-10-09T22:15:00Z
**Main tip at update:** `6fb7b7ee`

## How to read this

- Each item: **WHAT**, **WHY**, **DONE WHEN** (exact verifiable criteria), **STATUS**, **OWNER**.
- DONE WHEN must be checkable by a cold reader against GitHub bytes. No "looks good."
- Living document: STATUS auto-updates from PR state every 30min via `tools/checklist_sync.py`. Manual updates via `tools/checklist_update.py`. Never delete items — check them off.

---

## Cross-cutting (ALL must be DONE before production)

### ✅ C1. Single version of each activation document at BRAIN/ canonical paths; no competing versions.
- **WHAT:** Single version of each activation document at BRAIN/ canonical paths; no competing versions.
- **WHY:** Two truths = no truth. A cold Naya must find exactly one answer.
- **DONE WHEN:** BRAIN/00-ARCHITECTURE/ + BRAIN/05-MEMORY/SYSTEM-INTELLIGENCE/ hold the docs; .naya/project-intelligence/ tree absent on main.
- **STATUS:** DONE
  - PR #2060 merged at 7b8f8be8; verified on main
- **OWNER:** Naya 4
- **PRs:** #2060
- **Updated:** 2026-10-09T21:40:00Z

### 🔄 C2. Every blueprint gap closed in code: CANDIDATE→ACTIVE elevation path, ACT queries KNOW before decidin
- **WHAT:** Every blueprint gap closed in code: CANDIDATE→ACTIVE elevation path, ACT queries KNOW before deciding, typed node handoffs, ACT→KNOW feedback, SELF rejects unverified lessons, EVOLVE/REUSE/PROVE implemented, retrieval predicate enforced.
- **WHY:** A blueprint on paper is not a working engine. Every arrow must be real, tested code.
- **DONE WHEN:** PR #2062 merged to main; 244 tests green on main tip; 14-step loop (capture→…→cold successor retrieval) runs end-to-end.
- **STATUS:** IN PROGRESS
  - PR #2062 open, CI 7 success + 1 skipped, 0 failures, mergeable clean — awaiting independent review + merge
- **OWNER:** Naya 4
- **PRs:** #2062
- **Updated:** 2026-10-09T21:52:00Z

### 🔄 C3. The 14 proven thinking lessons embedded in the activation protocol as mandatory: WAKE → IDENTITY → T
- **WHAT:** The 14 proven thinking lessons embedded in the activation protocol as mandatory: WAKE → IDENTITY → THINK → PROVE → SERVE.
- **WHY:** Every Naya must think before she serves. Not optional, not 'if we feel like it.'
- **DONE WHEN:** PR #2059 merged; NAYA-ACTIVATION/THINKING-CURRICULUM-V1.md + thinking-curriculum.json on main; boot-order step 2A marked MANDATORY.
- **STATUS:** IN PROGRESS
  - PR #2059 open, CI 8/8 green, mergeable clean — awaiting independent review + merge
- **OWNER:** Naya 4
- **PRs:** #2059
- **Updated:** 2026-10-09T21:31:00Z

### ⬜ C4. A truly cold Naya (no prior context, never briefed) activates using only the repo: reads activation 
- **WHAT:** A truly cold Naya (no prior context, never briefed) activates using only the repo: reads activation protocol, learns identity, completes thinking curriculum, passes battery ≥7/lesson, serves correctly.
- **WHY:** "Any Naya can get activated, tune in and be successful" — unproven until a cold run proves it.
- **DONE WHEN:** Documented run with receipt: cold agent ID, start state (no context), each phase pass/fail, battery scores, served task outcome, independent verifier signature.
- **STATUS:** TODO
  - Unassigned — needs a driver
- **OWNER:** Unassigned
- **Blocked by:** C2, C3
- **Updated:** 2026-10-09T22:10:00Z

### ⬜ C5. Graduation protocol implemented and running: sampler, observer pool, scorer, feedback loop, 100% aut
- **WHAT:** Graduation protocol implemented and running: sampler, observer pool, scorer, feedback loop, 100% automated screening on all artifacts.
- **WHY:** The battery proves she CAN learn. Only sustained real-work application proves she DOES.
- **DONE WHEN:** All 7 components from GRADUATION-PROTOCOL.md §infrastructure built; observer calibration ≥80% agreement; first 14-day window STARTED (window ID recorded).
- **STATUS:** TODO
  - Designed — activation-naya/GRADUATION-PROTOCOL.md v1.0 — not built, not team-scorecarded
- **OWNER:** Unassigned
- **Updated:** 2026-10-09T22:10:00Z

### ✅ C6. Confirm no competing activation doc versions remain anywhere on main.
- **WHAT:** Confirm no competing activation doc versions remain anywhere on main.
- **WHY:** C1's completion must be verified, not assumed.
- **DONE WHEN:** git ls-tree on main shows exactly one set; brain-index regen clean (--check passes).
- **STATUS:** DONE
  - Verified at 7b8f8be8; reconciliation ledger at BRAIN/99-ARCHIVE/brain-reconciliation-ledger-f648833b.md
- **OWNER:** Naya 4
- **PRs:** #2060
- **Updated:** 2026-10-09T21:40:00Z

---

## Learning — current 7.0 provisional (baseline 5.0) → target 10/10 — feed #1724

**Section DONE WHEN:** Learning scorecard reads 10/10 with independent verification receipt citing lesson→retrieval→application→improved-outcome chain on a cold successor.

**Owner:** LEARN area driver (Naya 4 seat)

### 🔄 L1. Battery proven on ALL active seats (today: proven on test subjects only — 14/14, 9.93 avg, blind sco
- **WHAT:** Battery proven on ALL active seats (today: proven on test subjects only — 14/14, 9.93 avg, blind scored)
- **WHY:** One passing subject proves the method. All seats passing proves the team.
- **DONE WHEN:** Every active Naya seat has a battery receipt ≥7/lesson, blind scored.
- **STATUS:** IN PROGRESS
  - Test subjects done 14/14; active seats not yet run
- **OWNER:** LEARN area driver
- **Blocked by:** C3
- **Updated:** 2026-10-09T22:10:00Z

### ⬜ L2. Trial-06 executed (Trial-05 ruled invalid — ceiling effect)
- **WHAT:** Trial-06 executed (Trial-05 ruled invalid — ceiling effect)
- **WHY:** Trials validate the learning pipeline beyond the battery's synthetic tests.
- **DONE WHEN:** Trial-06 receipt posted with independent verification.
- **STATUS:** TODO
- **OWNER:** LEARN area driver
- **Updated:** 2026-10-09T22:10:00Z

### ⬜ L3. Longitudinal proof: 85%+ lesson application over 14 days, 60+ sampled tasks
- **WHAT:** Longitudinal proof: 85%+ lesson application over 14 days, 60+ sampled tasks
- **WHY:** Sustained application is the graduation bar.
- **DONE WHEN:** Graduation window complete with ≥85% application rate, zero honesty violations.
- **STATUS:** TODO
  - Blocked on C5 (graduation system not built)
- **OWNER:** LEARN area driver
- **Blocked by:** C5
- **Updated:** 2026-10-09T22:10:00Z

### ⬜ L4. Cold successor retrieves a promoted lesson and applies it with no human help
- **WHAT:** Cold successor retrieves a promoted lesson and applies it with no human help
- **WHY:** The ultimate learning proof: knowledge transfers across cold starts.
- **DONE WHEN:** Documented cold-successor run with receipt.
- **STATUS:** TODO
- **OWNER:** LEARN area driver
- **Blocked by:** C4
- **Updated:** 2026-10-09T22:10:00Z

### ⬜ L5. Projection 403 seam resolved (blocked rung 5.5→6.0 earlier; re-verify current state)
- **WHAT:** Projection 403 seam resolved (blocked rung 5.5→6.0 earlier; re-verify current state)
- **WHY:** A known blocker on the score ladder.
- **DONE WHEN:** Seam verified resolved or re-scoped with evidence.
- **STATUS:** TODO
- **OWNER:** LEARN area driver
- **Updated:** 2026-10-09T22:10:00Z

---

## Brain/Memory — current 7.0 → target 10/10 — feed Naya 5's lane

**Section DONE WHEN:** 10/10 with receipt: cold Naya stores an experience, retrieves it days later intact, applies it; zero data loss across 30 days.

**Owner:** Naya 5

### 🔄 B1. PR #2065 (WO1: T11 lifecycle CANDIDATE→ACTIVE) reviewed + merged
- **WHAT:** PR #2065 (WO1: T11 lifecycle CANDIDATE→ACTIVE) reviewed + merged
- **WHY:** Unblocks the T11 lifecycle activation.
- **DONE WHEN:** PR #2065 merged to main.
- **STATUS:** IN PROGRESS
  - PR opened, awaiting independent review
- **OWNER:** Naya 5
- **PRs:** #2065
- **Updated:** 2026-10-09T21:59:00Z

### 🚫 B2. PR #1861 (memory-metabolism machinery) unblocked: rebase onto current main, fix test CI failure, get
- **WHAT:** PR #1861 (memory-metabolism machinery) unblocked: rebase onto current main, fix test CI failure, get green, request independent review
- **WHY:** Core memory machinery currently blocked.
- **DONE WHEN:** PR #1861 rebased, CI green, reviewed, merged.
- **STATUS:** BLOCKED
  - CI RED (test failed 2026-10-09T15:49Z); 77 commits behind main; zero independent reviews
- **OWNER:** Naya 5
- **PRs:** #1861
- **Updated:** 2026-10-09T21:59:00Z

### ⬜ B3. Memory metabolism running continuously (ingest → distill → retrieve working on live data)
- **WHAT:** Memory metabolism running continuously (ingest → distill → retrieve working on live data)
- **WHY:** The brain must metabolize, not just store.
- **DONE WHEN:** 30 days continuous operation with zero data loss, verified by audit.
- **STATUS:** TODO
- **OWNER:** Naya 5
- **Blocked by:** B2
- **Updated:** 2026-10-09T22:10:00Z

---

## Law/Governance — current 7.5 → target 10/10 — feed #1718

**Section DONE WHEN:** 10/10 with receipt: every ratified law has a mechanical enforcement point; falsifier suite proves violations are caught (deny with field-named reasons).

**Owner:** LAW area driver

### 🚫 LW1. PR #2053 (delegated-merge receipt gate repair3 — B5 bypass fix) MERGED
- **WHAT:** PR #2053 (delegated-merge receipt gate repair3 — B5 bypass fix) MERGED
- **WHY:** Closes a merge-authority bypass. Scorecard Law blocking arm stays candidate-only until this merges.
- **DONE WHEN:** PR #2053 merged to main.
- **STATUS:** BLOCKED
  - HELD: protected gate, needs Shawn's explicit word (changes who may merge under delegated authority). Green, reviewed.
- **OWNER:** LAW area driver
- **PRs:** #2053
- **🔒 SHAWN-GATED** — his word only
- **Updated:** 2026-10-09T21:00:00Z

### ⬜ LW2. Scorecard Law blocking enforcement arm live on main
- **WHAT:** Scorecard Law blocking enforcement arm live on main
- **WHY:** Currently candidate-only until #2053 merges.
- **DONE WHEN:** Enforcement active on main, verified by falsifier test.
- **STATUS:** TODO
  - Blocked on LW1
- **OWNER:** LAW area driver
- **Blocked by:** LW1
- **Updated:** 2026-10-09T22:10:00Z

### 🔄 LW3. All ratified laws enforced in machinery (code/gates/tests), none living only in memory
- **WHAT:** All ratified laws enforced in machinery (code/gates/tests), none living only in memory
- **WHY:** Law that isn't mechanical is a wish.
- **DONE WHEN:** Audit: every ratified law maps to a code enforcement point with test.
- **STATUS:** IN PROGRESS
  - Ongoing — most laws have enforcement, audit incomplete
- **OWNER:** LAW area driver
- **Updated:** 2026-10-09T22:10:00Z

---

## Arch/Eng/Ops (ACT) — current 9.7 → target 10/10 — feed #1719

**Section DONE WHEN:** 10/10 with receipt: execution paths (tools fire, subagents complete, crons run, branches push, PRs open) proven on exact-tip bytes with zero phantom work.

**Owner:** ACT area driver

### 🔄 A1. Keep tip green; merges are the merging seat's gate (no self-merge)
- **WHAT:** Keep tip green; merges are the merging seat's gate (no self-merge)
- **WHY:** Green tip is the foundation everything builds on.
- **DONE WHEN:** Tip green 30 consecutive days.
- **STATUS:** IN PROGRESS
  - Currently green at 7b8f8be8
- **OWNER:** ACT area driver
- **Updated:** 2026-10-09T22:10:00Z

### 🔄 A2. #1767 landed — verify stable on current tip
- **WHAT:** #1767 landed — verify stable on current tip
- **WHY:** Recent landing needs stability confirmation.
- **DONE WHEN:** Verified stable, no regressions.
- **STATUS:** IN PROGRESS
- **OWNER:** ACT area driver
- **PRs:** #1767
- **Updated:** 2026-10-09T22:10:00Z

---

## Evolution/Succession — current 8.0 → target 10/10 — feed #1725

**Section DONE WHEN:** 10/10 with receipt: a cold successor boots from a sealed package, continues the predecessor's work with zero context loss, independently verified.

**Owner:** EVOLVE area driver

### ⬜ E1. PR #1856 (proposal-lifecycle ledger) merged
- **WHAT:** PR #1856 (proposal-lifecycle ledger) merged
- **DONE WHEN:** PR #1856 merged to main.
- **STATUS:** TODO
  - CANDIDATE, merge-blocked behind base CI wave — rebase and land
- **OWNER:** EVOLVE area driver
- **PRs:** #1856
- **Updated:** 2026-10-09T22:10:00Z

### ⬜ E2. PR #1734 (rollback) merged
- **WHAT:** PR #1734 (rollback) merged
- **DONE WHEN:** PR #1734 merged to main.
- **STATUS:** TODO
  - CANDIDATE, merge-blocked behind base CI wave — rebase and land
- **OWNER:** EVOLVE area driver
- **PRs:** #1734
- **Updated:** 2026-10-09T22:10:00Z

### ⬜ E3. PR #1762 (evidence-freeze) merged
- **WHAT:** PR #1762 (evidence-freeze) merged
- **DONE WHEN:** PR #1762 merged to main.
- **STATUS:** TODO
  - CANDIDATE, merge-blocked behind base CI wave — rebase and land
- **OWNER:** EVOLVE area driver
- **PRs:** #1762
- **Updated:** 2026-10-09T22:10:00Z

### ⬜ E4. Successor package path proven: build_successor_package() → cold boot → continuity
- **WHAT:** Successor package path proven: build_successor_package() → cold boot → continuity
- **WHY:** Ties to C4 (cold activation test).
- **DONE WHEN:** Documented successor boot with zero context loss, independently verified.
- **STATUS:** TODO
- **OWNER:** EVOLVE area driver
- **Blocked by:** C2
- **Updated:** 2026-10-09T22:10:00Z

---

## Interfaces/Hub — current 8.8 (CONNECT) / 7.5 (Hub) → target 10/10 — feed #1722

**Section DONE WHEN:** 10/10 with receipt: every claimed-live door fingerprinted against served bytes; Hub shows live intelligence from the substrate, verified by screenshot + byte check.

**Owner:** CONNECT area driver

### 🔄 I1. PR #1765 (truthful registry entrypoint + 9/9 behavior matrix) merged
- **WHAT:** PR #1765 (truthful registry entrypoint + 9/9 behavior matrix) merged
- **DONE WHEN:** PR #1765 merged to main.
- **STATUS:** IN PROGRESS
  - Currently green + mergeable, merge = merge authority's call
- **OWNER:** CONNECT area driver
- **PRs:** #1765
- **Updated:** 2026-10-09T22:10:00Z

### 🔄 I2. Door honesty sustained: only live doors claim live
- **WHAT:** Door honesty sustained: only live doors claim live
- **WHY:** Currently DOOR-AI + DOOR-DATA live, 7 REGISTERED_CONTRACT_ONLY.
- **DONE WHEN:** Audit confirms honesty; no phantom-live claims.
- **STATUS:** IN PROGRESS
  - Currently honest; needs sustained verification
- **OWNER:** CONNECT area driver
- **Updated:** 2026-10-09T22:10:00Z

### ⬜ I3. Daily intelligence report renders in Hub from real distilled notes
- **WHAT:** Daily intelligence report renders in Hub from real distilled notes
- **WHY:** Shawn's stated use case.
- **DONE WHEN:** Report renders from live substrate data, verified by screenshot.
- **STATUS:** TODO
- **OWNER:** CONNECT area driver
- **Updated:** 2026-10-09T22:10:00Z

---

## Knowledge/Intelligence — current 8.9 → target 10/10 — feed #1720

**Section DONE WHEN:** 10/10 with receipt: retrieval precision measured ≥90% on applicability-triggered queries; no stale intelligence served (lint green 30 days).

**Owner:** KNOW area driver

### 🔄 K1. PR #1763 (admission family pin) merged
- **WHAT:** PR #1763 (admission family pin) merged
- **DONE WHEN:** PR #1763 merged to main.
- **STATUS:** IN PROGRESS
  - Currently open, receipt posted, merge-ready
- **OWNER:** KNOW area driver
- **PRs:** #1763
- **Updated:** 2026-10-09T22:10:00Z

### ⬜ K2. Retrieval ranks on applicability triggers, not generic titles
- **WHAT:** Retrieval ranks on applicability triggers, not generic titles
- **WHY:** SN-0824: 43-case diagnostic showed MATCH_ID 2/43 — discriminability gap.
- **DONE WHEN:** Retrieval precision ≥90% on applicability-triggered queries.
- **STATUS:** TODO
- **OWNER:** KNOW area driver
- **Updated:** 2026-10-09T22:10:00Z

### ⬜ K3. Project Intelligence views current automatically (freshness/staleness lint running)
- **WHAT:** Project Intelligence views current automatically (freshness/staleness lint running)
- **DONE WHEN:** Lint green 30 consecutive days.
- **STATUS:** TODO
- **OWNER:** KNOW area driver
- **Updated:** 2026-10-09T22:10:00Z

---

## Proving/Verifying — current 9.4 (PROVE) / 9.2 (VERIFY) → target 10/10 — feed #1721 / #1723

**Section DONE WHEN:** 10/10 with receipt: full kernel suite green on exact tip; every significant claim carries independent verification capable of disagreeing; live production proofs current.

**Owner:** PROVE + VERIFY area drivers

### ⬜ P1. PR #1840 (test collection ModuleNotFoundError fix) merged
- **WHAT:** PR #1840 (test collection ModuleNotFoundError fix) merged
- **DONE WHEN:** PR #1840 merged to main.
- **STATUS:** TODO
- **OWNER:** PROVE area driver
- **PRs:** #1840
- **Updated:** 2026-10-09T22:10:00Z

### ⬜ P2. PR #1952 (spec-integrity: pin 0006-naya-calculator-v1.machine.json) merged
- **WHAT:** PR #1952 (spec-integrity: pin 0006-naya-calculator-v1.machine.json) merged
- **DONE WHEN:** PR #1952 merged to main.
- **STATUS:** TODO
- **OWNER:** PROVE area driver
- **PRs:** #1952
- **Updated:** 2026-10-09T22:10:00Z

### ⬜ P3. PR #1981 (CI guard first-party protocol root) merged
- **WHAT:** PR #1981 (CI guard first-party protocol root) merged
- **DONE WHEN:** PR #1981 merged to main.
- **STATUS:** TODO
- **OWNER:** PROVE area driver
- **PRs:** #1981
- **Updated:** 2026-10-09T22:10:00Z

### ⬜ P4. PR #1766 re-anchored (3rd re-anchor needed) and merged
- **WHAT:** PR #1766 re-anchored (3rd re-anchor needed) and merged
- **DONE WHEN:** PR #1766 merged to main.
- **STATUS:** TODO
- **OWNER:** PROVE area driver
- **PRs:** #1766
- **Updated:** 2026-10-09T22:10:00Z

### ⬜ P5. PR #1980 merged (awaiting merge lane)
- **WHAT:** PR #1980 merged (awaiting merge lane)
- **DONE WHEN:** PR #1980 merged to main.
- **STATUS:** TODO
- **OWNER:** PROVE area driver
- **PRs:** #1980
- **Updated:** 2026-10-09T22:10:00Z

### ⬜ P6. Brain-index drift resolved (--check must pass on main)
- **WHAT:** Brain-index drift resolved (--check must pass on main)
- **WHY:** Flagged to brain-build lane.
- **DONE WHEN:** Brain-index --check passes on main tip.
- **STATUS:** TODO
- **OWNER:** PROVE area driver
- **Updated:** 2026-10-09T22:10:00Z

### 🚫 P7. Live Supabase + PROVE-node proofs re-run
- **WHAT:** Live Supabase + PROVE-node proofs re-run
- **WHY:** Production proofs must be current.
- **DONE WHEN:** Proofs re-run and green.
- **STATUS:** BLOCKED
  - Shawn-gated (production word required)
- **OWNER:** PROVE area driver
- **🔒 SHAWN-GATED** — his word only
- **Updated:** 2026-10-09T22:10:00Z

---

## Innovation — current UNMEASURED → target 10/10 — feed No driver assigned

**Section DONE WHEN:** 10/10 with receipt per the area's own ratified definition.

**Owner:** Unassigned

### ⬜ IN1. Assign a driver and feed (propose: #1873 Innovation team feed)
- **WHAT:** Assign a driver and feed (propose: #1873 Innovation team feed)
- **WHY:** No one owns it, no one measures it.
- **DONE WHEN:** Driver assigned, feed active.
- **STATUS:** TODO
- **OWNER:** Unassigned
- **Updated:** 2026-10-09T22:10:00Z

### ⬜ IN2. Define what 10/10 means for Innovation (new capabilities proven, not just proposed)
- **WHAT:** Define what 10/10 means for Innovation (new capabilities proven, not just proposed)
- **DONE WHEN:** Ratified definition published.
- **STATUS:** TODO
- **OWNER:** Unassigned
- **Blocked by:** IN1
- **Updated:** 2026-10-09T22:10:00Z

### ⬜ IN3. First measured scorecard published
- **WHAT:** First measured scorecard published
- **DONE WHEN:** Scorecard published with evidence.
- **STATUS:** TODO
- **OWNER:** Unassigned
- **Blocked by:** IN1, IN2
- **Updated:** 2026-10-09T22:10:00Z

---

## 🔒 Blocked on Shawn (protected gates — his word only)

These are NOT team-actionable. They wait on Shawn explicitly:

SG1. **PR #2053 merge — changes merge authority (delegated-merge receipt gate). Green, reviewed, HELD.** (PRs: #2053)
SG2. **Production deploy — the final promotion. Blocked on workflow_dispatch 403; needs his token/action.**
SG3. **Live Supabase / PROVE-node proofs — touch production data; needs his word.**
SG4. **Diagnostic deploy of PR #2012 — to capture the true 403 class (from hourly report).** (PRs: #2012)

---

## Production Readiness Gate

```
ALL cross-cutting DONE AND all departments at 10/10 (independently verified, no self-scoring) AND zero open Shawn-gate blockers → Shawn's word → production deploy → live test (real users, real load) → SHE'S LIVE
```

**Shawn's rule:** "Without that she has no chance. The checklist is the chance. Work it top to bottom, check every box with evidence, and she ships."

---

*Summary: 2/39 DONE (10 in progress, 3 blocked, 24 todo, 0 stale). Last sync: 2026-10-09T22:15:00Z.*

*Generated from ACTIVATION-MASTER-CHECKLIST.json — do not hand-edit.*
