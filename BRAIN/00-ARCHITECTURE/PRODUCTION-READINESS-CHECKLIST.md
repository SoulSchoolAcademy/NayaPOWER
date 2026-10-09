# PRODUCTION READINESS CHECKLIST — NayaPOWER

**The single source of truth for "are we ready."**

Shawn's law: *"Without this checklist, she has no chance. With it, she has a chance."*

This document lists everything that must be complete before Naya goes live for production testing. Every item has a plain-language description, observable done criteria, a real current status, an owner, and an evidence link. Nothing here is aspirational — it is the actual bar.

**Scope note:** this is *intelligence readiness* — is she ready to think, learn, and build? The *deployment* readiness slice (is the tip deployable?) is measured by the mechanical instrument `tools/production_readiness_checklist.py`, referenced under Infrastructure. Two different questions, two different instruments, no duplication.

**Related but different:** `BRAIN/00-ACTIVATION/activation-checklist.json` is the cold-start protocol (what a waking Naya does). This document is the bar she must clear before she goes live. `BRAIN/00-ARCHITECTURE/ACTIVATION-NAYA-PLAN.md` is the execution plan. `BRAIN/00-ARCHITECTURE/MACHINE-INTELLIGENCE.json` is the machine truth. This checklist consolidates their acceptance criteria into one visible list.

**Statuses:** DONE (verified) · IN REVIEW (built, awaiting independent verification) · IN PROGRESS · NOT STARTED · BLOCKED (with the blocker named).

**Rule:** IN REVIEW becomes DONE only on an independent verification receipt — never on the builder's word. "Tests pass" is not done. Done means observed behavior change, verified by someone who didn't build it.

---

## DEPARTMENT 1 — LEARNING / LEARN CHAIN
*Owner: Naya 4 (engine lead). The lesson lifecycle: capture → verify → promote → behavior change.*

| ID | What (plain language) | Done looks like (observable) | Status | Evidence |
|---|---|---|---|---|
| L1 | The commit-proof pipeline is green (WO1) | A `live-intelligence-commit-proof` run completes all green on the held-out branch; the `AssertionError: CANDIDATE` is gone | NOT STARTED | — |
| L2 | Nothing becomes ACTIVE by accident (WO8) | A capture that omits `lifecycle_state` is rejected by the gate with the right error — it fails, not passes | NOT STARTED | — |
| L3 | The front door has a bouncer (WO3) | Submit a bad candidate → rejected with a named reason visible in the log. Submit a good one → accepted | IN PROGRESS | #2049 (10-min fix needed), #2048 (needs Naya 4 rework) |
| L4 | One intake path, not three (WO9) | Every capture flows through a single canonical intake; the old parallel paths are removed or formally retired | NOT STARTED | — |
| L5 | One real lesson through the real chain (SEED) | A single ACTIVE seed lesson travels capture → persist → index → verify → promote, each step observed | NOT STARTED | — |
| L6 | The database and the repo agree (WO2) | After a promotion, the repo registry's `truth_state` matches the database within one workflow run — proven on a test capture | NOT STARTED | — |
| L7 | No duplicate lesson numbers (WO7) | Registry query returns zero duplicate Smart Note numbers; CI fails a test branch that submits a duplicate | NOT STARTED | — |
| L8 | She learns day after day, not just in tests (longitudinal) | A measurement harness records her learning behavior under real load over time; trend is visible, not a single data point | NOT STARTED | Design only (Naya 1) |
| L9 | ~~14/14 learning proof with database receipts~~ | Blind-scored, receipts in the database | DONE | #1354 receipts |
| L10 | ~~Thinking pattern transfers~~ | Taught Naya scores 10/10 vs control 9/10; the mirror check is the habit that stuck | DONE | Experiment report 2026-10-09 |

## DEPARTMENT 2 — IDENTITY / ACTIVATION
*Owner: Naya 2. A cold Naya wakes up and knows who she is.*

| ID | What (plain language) | Done looks like (observable) | Status | Evidence |
|---|---|---|---|---|
| I1 | The startup checklist points somewhere real | The `MEMORY.md` path the activation checklist requires resolves to a real file on main (today it 404s) | NOT STARTED | — |
| I2 | The two-engine architecture lives in the repo | UNDERSTAND→CREATE→APPLY→IMPROVE and REMEMBER→VERIFY→LEARN→COMPOUND are in a repo document on the cold-start path — she can reach what she must learn | NOT STARTED | — |
| I3 | Every Naya gets the thinking pattern at birth | The thinking pattern is part of activation itself, for all seats — not a separate test for test subjects | NOT STARTED | — |
| I4 | Cold identity test scores ≥ 40/50 | Re-run the five-question cold test after I1–I3; she names the living-intelligence identity, the mission, the laws, and the protocol | NOT STARTED | Baseline 28/50 (2026-10-09) |
| I5 | ~~Cold retrieval works~~ | A cold Naya finds project intelligence through the librarian wiring | DONE | #2056 merged |
| I6 | ~~Learning-system blueprint exists~~ | 497 lines, evidence-tagged, on main | DONE | `BRAIN/07-LEARNING/learning-system-blueprint-v1.md` |

## DEPARTMENT 3 — DECISIONS / ACT
*Owner: Naya 4. Verified lessons change what she actually does.*

| ID | What (plain language) | Done looks like (observable) | Status | Evidence |
|---|---|---|---|---|
| A1 | Lessons reach the decision engine (WO4) | CONTROL vs TREATMENT plans differ exactly as the lesson prescribes; `influenced=true` appears only on an observed behavioral delta — confirmed by diffing both plans | IN REVIEW | #2063 (82/82 tests; awaiting independent verification) |
| A2 | Lessons change behavior patterns (WO5b) | A decision in a previously-seen situation reflects the integrated lesson; rollback restores prior behavior — proven with before/after transcripts | IN REVIEW | #2061 (84/84 tests; awaiting independent verification) |
| A3 | The TypeScript/Python split is bridged (WO10) | A verified lesson produced on one side of the runtime boundary is usable on the other — proven with a cross-boundary test | NOT STARTED | — |
| A4 | ACT actually asks KNOW (GAP-2) | `evaluate_candidates()` and `retrieval_eligible()` have real operational callers — confirmed by grep on live main, not by reading the spec | IN REVIEW | Via #2063 |
| A5 | What she does becomes what she knows (GAP-4) | Execution results are recorded as knowledge — the `ExecutionHandoff` type exists and is used in code | NOT STARTED | — |

## DEPARTMENT 4 — MEMORY / KNOW
*Owner: Naya 4 (retrieval), Naya 2 (docs). One truth, reachable.*

| ID | What (plain language) | Done looks like (observable) | Status | Evidence |
|---|---|---|---|---|
| K1 | One canonical document set | The two machine files and two blueprint sets are reconciled into one — no competing sources of truth | IN PROGRESS | Naya 4 reconciling (#2054 open) |
| K2 | The projection bridge works or is retired (WO6) | Either one projection succeeds end-to-end (Smart Link resolves) or the bridge is formally retired with a retirement record | NOT STARTED | — |
| K3 | The kernel-to-database read path is scoped (WO5a) | The exact seam is named, its contract written, and both sides agree on it | NOT STARTED | — |
| K4 | Truth state gates retrieval (GAP-8) | `retrieval_eligible()` is called on the live path — unverified lessons don't reach decisions just because they're relevant | NOT STARTED | — |
| K5 | ~~Project intelligence pilot accepted~~ | Naya 2 ACCEPTED with qualifications; RLS posture documented | DONE | #2050, #1354/6088727181 |

## DEPARTMENT 5 — VERIFICATION / PROVE
*Owner: Naya 1 (judge). Nothing counts without independent proof.*

| ID | What (plain language) | Done looks like (observable) | Status | Evidence |
|---|---|---|---|---|
| V1 | #2061 independently verified | A seat that didn't build it confirms the behavior change on live bytes and posts the receipt | NOT STARTED | Blocked: needs a verifier |
| V2 | #2063 independently verified | A seat that didn't build it confirms the decision-seam delta on live bytes and posts the receipt | NOT STARTED | Blocked: needs a verifier |
| V3 | The first closed loop | One novel lesson, all nine steps, eyes on each one: captured → promoted (DB + repo in sync) → retrieved by a cold Naya → applied to a held-out task → behavior change confirmed by an independent verifier → full hash-carrying receipt chain | NOT STARTED | Blocked: needs L1–L7, A1–A2 |
| V4 | The behavioral quartet runs | The four held-out behavioral tests execute (they have never run — 0/4) | NOT STARTED | — |
| V5 | REUSE and PROVE exist in code (GAP-6/7) | Of the seven lifecycle steps, REUSE and PROVE have implementing functions — confirmed by grep, not by the plan | NOT STARTED | — |
| V6 | ~~Archive replay proven~~ | SR-P2, SR-P5, SR-P6 all reproduce — 3/3 independent | DONE | #1354/6089165047 |
| V7 | ~~Score-the-method law~~ | Every proof scorecard names method flaws, not just the verdict | DONE | AGENTS.md |

## DEPARTMENT 6 — INFRASTRUCTURE
*Owner: Naya 5 (CI/pipeline), Naya 2 (build loop). The ground she stands on.*

| ID | What (plain language) | Done looks like (observable) | Status | Evidence |
|---|---|---|---|---|
| F1 | Main tip is green | Full pytest (no exclusions) + brain index `--check` + adversarial harness all pass on the exact tip bytes | DONE | Tip `6fb7b7ee`: 1937 passed / 11 skipped / 0 failed, 6/6 adversarial |
| F2 | What's deployed matches main | The production deployment is built from the current tip — not 43 hours stale | NOT STARTED | BLOCKED: production deploy is human-gated |
| F3 | The parity gate is exercised | The deployed↔main parity check runs and passes — not just exists | NOT STARTED | — |
| F4 | The workflow red is repaired | `licp.yml` no longer fails on the exact-`provenance` index; repair merged | NOT STARTED | BLOCKED: workflow files are human-gated (#2051 open) |
| F5 | Brain index regen merged | The stale-basis regen lands and the index is clean on the tip | IN PROGRESS | #2057 open |
| F6 | Admission-gate PRs land | #2049 (after its 10-min fix) merges; #2048 after Naya 4's rework | IN PROGRESS | #2049, #2048 open |
| F7 | Production database migrations applied | Pending migrations land in the production DB | NOT STARTED | BLOCKED: production DB is human-gated (#1136) |
| F8 | ~~Deployment readiness instrument~~ | Mechanical deployability checks (tip currency, promotion workflow health, migration hygiene) run in CI | DONE | `tools/production_readiness_checklist.py` |

## DEPARTMENT 7 — INTERFACE
*Owner: Naya 2 (Head of Design). Entry criteria for "she builds herself."*

| ID | What (plain language) | Done looks like (observable) | Status | Evidence |
|---|---|---|---|---|
| N1 | All departments above are DONE | Every item in Departments 1–6 shows DONE with an evidence link — the gate below fires | NOT STARTED | This document |
| N2 | The interface build spec exists | "She builds herself" is defined: what she takes as input (intent), what she reads (project intelligence), what she produces (a working smart app), and how we score the result | NOT STARTED | — |
| N3 | Production readiness review held | Each department owner presents evidence; Naya 1 scores; Shawn gives the word | NOT STARTED | Blocked: needs N1 |
| N4 | The live test | One novel lesson through all nine steps on production, cold successor, independent verifier — the graduation exam | NOT STARTED | Blocked: needs N3 |

---

## THE GATE

When every item above reads DONE — each with an evidence link, each verified by someone who didn't build it — the following fires in order:

1. **Department sign-off.** Each department owner posts a sign-off receipt on #1354 with links to every item's evidence.
2. **The readiness review.** Naya 1 (judge) scores the whole system against this checklist. Nothing below 9.0 passes.
3. **Shawn's word.** He gives the go. This is his call and only his.
4. **The live test.** One novel lesson, all nine steps, on production, cold successor, independent verifier. The graduation exam.
5. **She goes live.** Only then does she start building.

No step is skipped. No step is merged with the next. A green test suite is not the gate — the gate is the checklist, fully DONE.

---

## UPDATE PROTOCOL

A checklist nobody maintains is decoration. This is how it stays true:

1. **Owners update their department.** When an item's status changes (PR opened, merged, verified, blocked), the department owner edits this file in the same PR or a follow-up within 24 hours. Every status change carries an evidence link.
2. **IN REVIEW → DONE needs a receipt.** Only an independent verifier's posted receipt moves an item to DONE. The builder's word never does.
3. **Stale flag.** If an item shows no status change and no linked activity for 7 days, the team relay flags it STALE on #1354. STALE is not a status — it's a demand for an update.
4. **Versioned.** Changes to this file go through PR like everything else. The history is the audit trail.
5. **Weekly review.** Every Friday, the department owners confirm their sections are current — or fix them on the spot.

---

## SCOREBOARD

*Updated 2026-10-09 ~22:00 UTC at main tip `6fb7b7ee`.*

| Department | Done | In Review | In Progress | Not Started | Blocked |
|---|---|---|---|---|---|
| 1 — Learning | 2 | 0 | 1 | 7 | 0 |
| 2 — Identity | 2 | 0 | 0 | 4 | 0 |
| 3 — Decisions | 0 | 3 | 0 | 2 | 0 |
| 4 — Memory | 1 | 0 | 1 | 3 | 0 |
| 5 — Verification | 2 | 0 | 0 | 3 | 2 |
| 6 — Infrastructure | 2 | 0 | 2 | 2 | 2 |
| 7 — Interface | 0 | 0 | 0 | 4 | 0 |
| **Total** | **11** | **3** | **4** | **25** | **4** |

**Bottom line:** 11 of 47 done. The foundation is real — the learning proof, the green tip, the two surged builds awaiting verification. The distance to the gate is 25 unstarted items and 4 human-gated blockers. Every one of them is named above, with an owner and a done criterion. That is the whole point of this document: no hidden work, no vague "almost," just the list.
