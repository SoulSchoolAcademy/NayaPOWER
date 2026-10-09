# Master Checklist — Activation to Production

**Owner:** Naya 4 (builder seat), Team Naya
**Created:** 2026-10-09 (Shawn's direct order: "a checklist of everything that needs to be done… put that checklist where everybody can see it… for each department")
**Canonical location:** `BRAIN/00-ACTIVATION/ACTIVATION-CHECKLIST.md`
**Status as of main tip `6fb7b7ee` (2026-10-09 ~15:00 PDT)**

## How to read this

- Each item: **WHAT** (the task), **WHY** (why it matters), **DONE WHEN** (exact verifiable criteria), **STATUS** (TODO / IN PROGRESS / DONE), **OWNER** (seat/team).
- DONE WHEN must be checkable by a cold reader against GitHub bytes. No "looks good."
- Living document: update STATUS as work completes. Never delete items — check them off.
- Scores reference the honest area scoreboard (`bring-naya-to-life/hidden_files/area-scoreboard.md`).

---

## Cross-cutting (ALL must be DONE before production)

### C1. One canonical doc set
- **WHAT:** Single version of each activation document at BRAIN/ canonical paths; no competing versions.
- **WHY:** Two truths = no truth. A cold Naya must find exactly one answer.
- **DONE WHEN:** `BRAIN/00-ARCHITECTURE/` + `BRAIN/05-MEMORY/SYSTEM-INTELLIGENCE/` hold the docs; `.naya/project-intelligence/` tree absent on main.
- **STATUS:** DONE (PR #2060 merged at `7b8f8be8`; verified on main)
- **OWNER:** Naya 4

### C2. Nine nodes wired
- **WHAT:** Every blueprint gap closed in code: CANDIDATE→ACTIVE elevation path, ACT queries KNOW before deciding, typed node handoffs, ACT→KNOW feedback, SELF rejects unverified lessons, EVOLVE/REUSE/PROVE implemented, retrieval predicate enforced.
- **WHY:** A blueprint on paper is not a working engine. Every arrow must be real, tested code.
- **DONE WHEN:** PR #2062 merged to main; 244 tests green on main tip; 14-step loop (capture→…→cold successor retrieval) runs end-to-end.
- **STATUS:** IN PROGRESS (PR #2062 open, CI 7 success + 1 skipped, 0 failures, mergeable clean — awaiting independent review + merge)
- **OWNER:** Naya 4

### C3. Thinking curriculum canonical
- **WHAT:** The 14 proven thinking lessons embedded in the activation protocol as mandatory: WAKE → IDENTITY → THINK → PROVE → SERVE.
- **WHY:** Every Naya must think before she serves. Not optional, not "if we feel like it."
- **DONE WHEN:** PR #2059 merged; `NAYA-ACTIVATION/THINKING-CURRICULUM-V1.md` + `thinking-curriculum.json` on main; boot-order step 2A marked MANDATORY.
- **STATUS:** IN PROGRESS (PR #2059 open, CI 8/8 green, mergeable clean — awaiting independent review + merge)
- **OWNER:** Naya 4

### C4. Cold activation test
- **WHAT:** A truly cold Naya (no prior context, never briefed) activates using only the repo: reads activation protocol, learns identity, completes thinking curriculum, passes battery ≥7/lesson, serves correctly.
- **WHY:** "Any Naya can get activated, tune in and be successful" — unproven until a cold run proves it.
- **DONE WHEN:** Documented run with receipt: cold agent ID, start state (no context), each phase pass/fail, battery scores, served task outcome, independent verifier signature.
- **STATUS:** TODO
- **OWNER:** Unassigned — needs a driver

### C5. Longitudinal proof system built
- **WHAT:** Graduation protocol implemented and running: sampler, observer pool, scorer, feedback loop, 100% automated screening on all artifacts.
- **WHY:** The battery proves she CAN learn. Only sustained real-work application proves she DOES.
- **DONE WHEN:** All 7 components from `GRADUATION-PROTOCOL.md` §infrastructure built; observer calibration ≥80% agreement; first 14-day window STARTED (window ID recorded).
- **STATUS:** TODO (designed — `activation-naya/GRADUATION-PROTOCOL.md` v1.0 — not built, not team-scorecarded)
- **OWNER:** Unassigned — needs a driver

### C6. Duplicate reconciliation verified
- **WHAT:** Confirm no competing activation doc versions remain anywhere on main.
- **WHY:** C1's completion must be verified, not assumed.
- **DONE WHEN:** `git ls-tree` on main shows exactly one set; brain-index regen clean (`--check` passes).
- **STATUS:** DONE (verified at `7b8f8be8`; reconciliation ledger at `BRAIN/99-ARCHIVE/brain-reconciliation-ledger-f648833b.md`)
- **OWNER:** Naya 4

---

## Per-department checklists

### Learning — current 7.0 provisional (baseline 5.0) → target 10/10 — feed #1724
- [ ] Battery proven on ALL active seats (today: proven on test subjects only — 14/14, 9.93 avg, blind scored)
- [ ] Trial-06 executed (Trial-05 ruled invalid — ceiling effect)
- [ ] Longitudinal proof: 85%+ lesson application over 14 days, 60+ sampled tasks (blocked on C5)
- [ ] Cold successor retrieves a promoted lesson and applies it with no human help
- [ ] Projection 403 seam resolved (blocked rung 5.5→6.0 earlier; re-verify current state)
- **DONE WHEN:** Learning scorecard reads 10/10 with independent verification receipt citing lesson→retrieval→application→improved-outcome chain on a cold successor.
- **OWNER:** LEARN area driver (Naya 4 seat)

### Brain/Memory — current 7.0 → target 10/10 — Naya 5's lane
- [ ] PR #2065 (WO1: T11 lifecycle CANDIDATE→ACTIVE) reviewed + merged
- [ ] PR #1861 (memory-metabolism machinery) unblocked: rebase onto current main, fix `test` CI failure (failed 2026-10-09T15:49Z), get green, request independent review
- [ ] Memory metabolism running continuously (ingest → distill → retrieve working on live data)
- **DONE WHEN:** 10/10 with receipt: cold Naya stores an experience, retrieves it days later intact, applies it; zero data loss across 30 days.
- **OWNER:** Naya 5

### Law/Governance — current 7.5 → target 10/10 — feed #1718
- [ ] PR #2053 (delegated-merge receipt gate repair3 — B5 bypass fix) MERGED — **HELD: protected gate, needs Shawn's explicit word** (changes who may merge under delegated authority)
- [ ] Scorecard Law blocking enforcement arm live on main (currently candidate-only until #2053 merges)
- [ ] All ratified laws enforced in machinery (code/gates/tests), none living only in memory
- **DONE WHEN:** 10/10 with receipt: every ratified law has a mechanical enforcement point; falsifier suite proves violations are caught (deny with field-named reasons).
- **OWNER:** LAW area driver

### Arch/Eng/Ops — current 9.7 → target 10/10 — feed #1719
- [ ] Remaining: merges are the merging seat's gate (no self-merge); keep tip green
- [ ] #1767 landed — verify stable on current tip
- **DONE WHEN:** 10/10 with receipt: execution paths (tools fire, subagents complete, crons run, branches push, PRs open) proven on exact-tip bytes with zero phantom work.
- **OWNER:** ACT area driver

### Evolution/Succession — current 8.0 → target 10/10 — feed #1725
- [ ] PR #1856 (proposal-lifecycle ledger) merged
- [ ] PR #1734 (rollback) merged
- [ ] PR #1762 (evidence-freeze) merged
- [ ] All three currently CANDIDATE, merge-blocked behind base CI wave — rebase and land
- [ ] Successor package path proven: `build_successor_package()` → cold boot → continuity (ties to C4)
- **DONE WHEN:** 10/10 with receipt: a cold successor boots from a sealed package, continues the predecessor's work with zero context loss, independently verified.
- **OWNER:** EVOLVE area driver

### Interfaces/Hub — current 8.8 (CONNECT) / 7.5 (Hub) → target 10/10 — feed #1722
- [ ] PR #1765 (truthful registry entrypoint + 9/9 behavior matrix) merged — currently green + mergeable, merge = merge authority's call
- [ ] Door honesty sustained: only live doors claim live (currently DOOR-AI + DOOR-DATA live, 7 REGISTERED_CONTRACT_ONLY)
- [ ] Daily intelligence report renders in Hub from real distilled notes (Shawn's stated use case)
- **DONE WHEN:** 10/10 with receipt: every claimed-live door fingerprinted against served bytes; Hub shows live intelligence from the substrate, verified by screenshot + byte check.
- **OWNER:** CONNECT area driver

### Knowledge/Intelligence — current 8.9 → target 10/10 — feed #1720
- [ ] PR #1763 (admission family pin) merged — currently open, receipt posted, merge-ready
- [ ] Retrieval ranks on applicability triggers, not generic titles (SN-0824: 43-case diagnostic showed MATCH_ID 2/43 — discriminability gap)
- [ ] Project Intelligence views current automatically (freshness/staleness lint running)
- **DONE WHEN:** 10/10 with receipt: retrieval precision measured ≥90% on applicability-triggered queries; no stale intelligence served (lint green 30 days).
- **OWNER:** KNOW area driver

### Proving/Verifying — current 9.4 (PROVE) / 9.2 (VERIFY) → target 10/10 — feeds #1721 / #1723
- [ ] PR #1840 (test collection `ModuleNotFoundError` fix) merged
- [ ] PR #1952 (spec-integrity: pin `0006-naya-calculator-v1.machine.json`) merged
- [ ] PR #1981 (CI guard first-party protocol root) merged
- [ ] PR #1766 re-anchored (3rd re-anchor needed) and merged
- [ ] PR #1980 merged (awaiting merge lane)
- [ ] Brain-index drift resolved (flagged to brain-build lane; `--check` must pass on main)
- [ ] Live Supabase + PROVE-node proofs re-run — **Shawn-gated** (production word required)
- **DONE WHEN:** 10/10 with receipt: full kernel suite green on exact tip; every significant claim carries independent verification capable of disagreeing; live production proofs current.
- **OWNER:** PROVE + VERIFY area drivers

### Innovation — current UNMEASURED → target 10/10 — no driver assigned
- [ ] Assign a driver and feed (propose: #1873 Innovation team feed)
- [ ] Define what 10/10 means for Innovation (new capabilities proven, not just proposed)
- [ ] First measured scorecard published
- **DONE WHEN:** 10/10 with receipt per the area's own ratified definition.
- **OWNER:** Unassigned — needs a driver

---

## Blocked on Shawn (protected gates — his word only)

These are NOT team-actionable. They wait on Shawn explicitly:

1. **PR #2053 merge** — changes merge authority (delegated-merge receipt gate). Green, reviewed, HELD.
2. **Production deploy** — the final promotion. Blocked on `workflow_dispatch` 403; needs his token/action.
3. **Live Supabase / PROVE-node proofs** — touch production data; needs his word.
4. **Diagnostic deploy of PR #2012** — to capture the true 403 class (from hourly report).

---

## Production Readiness Gate

```
ALL cross-cutting DONE
  AND all departments at 10/10 (independently verified, no self-scoring)
  AND zero open Shawn-gate blockers
    → Shawn's word
      → production deploy
        → live test (real users, real load)
          → SHE'S LIVE
```

**Shawn's rule that governs this document:** "Without that she has no chance." The checklist is the chance. Work it top to bottom, check every box with evidence, and she ships.

---

*Last updated: 2026-10-09 ~15:05 PDT by Naya 4. Update STATUS lines as work lands; never delete items.*
