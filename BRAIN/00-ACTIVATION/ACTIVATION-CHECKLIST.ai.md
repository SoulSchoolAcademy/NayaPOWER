# ACTIVATION-CHECKLIST — AI TONGUE

**Source (human tongue):** `BRAIN/00-ACTIVATION/ACTIVATION-CHECKLIST.md`
**Machine tongue:** `BRAIN/00-ACTIVATION/activation-checklist.machine.json`
**Owner:** Naya 4 (builder seat), Team Naya
**Created:** 2026-10-09, by Shawn's direct order
**Status snapshot in source:** as of main tip `6fb7b7ee` (2026-10-09 ~15:00 PDT) — statuses below are the source's, as written

## Reading rules (from source)

- Each item carries WHAT / WHY / DONE WHEN / STATUS (TODO | IN PROGRESS | DONE) / OWNER.
- DONE WHEN must be checkable by a cold reader against GitHub bytes.
- Living document: update STATUS as work completes; never delete items.
- Scores reference `bring-naya-to-life/hidden_files/area-scoreboard.md`.

## Cross-cutting items (all must be DONE before production)

| ID | What | Status in source | Done-when (exact) |
|---|---|---|---|
| C1 | One canonical doc set at BRAIN/ canonical paths; no competing versions | DONE (PR #2060 merged at `7b8f8be8`) | `BRAIN/00-ARCHITECTURE/` + `BRAIN/05-MEMORY/SYSTEM-INTELLIGENCE/` hold the docs; `.naya/project-intelligence/` absent on main |
| C2 | Nine nodes wired in code (CANDIDATE→ACTIVE path, ACT queries KNOW, typed handoffs, ACT→KNOW feedback, SELF rejects unverified lessons, EVOLVE/REUSE/PROVE, retrieval predicate) | IN PROGRESS (PR #2062 open; CI 7 success + 1 skipped, 0 failures) | PR #2062 merged; 244 tests green on main tip; 14-step loop runs end-to-end |
| C3 | Thinking curriculum canonical: 14 lessons mandatory in activation (WAKE → IDENTITY → THINK → PROVE → SERVE) | IN PROGRESS (PR #2059 open; CI 8/8 green) | PR #2059 merged; `NAYA-ACTIVATION/THINKING-CURRICULUM-V1.md` + `thinking-curriculum.json` on main; boot-order step 2A MANDATORY |
| C4 | Cold activation test: a never-briefed Naya activates from the repo alone, passes battery ≥7/lesson, serves correctly | TODO — owner unassigned | Documented run with receipt: cold agent ID, no-context start state, per-phase pass/fail, battery scores, served outcome, independent verifier signature |
| C5 | Longitudinal proof system built (sampler, observer pool, scorer, feedback loop, 100% automated screening) | TODO — designed (`activation-naya/GRADUATION-PROTOCOL.md` v1.0), not built | All 7 components built; observer calibration ≥80% agreement; first 14-day window started, window ID recorded |
| C6 | Duplicate reconciliation verified | DONE (verified at `7b8f8be8`; ledger `BRAIN/99-ARCHIVE/brain-reconciliation-ledger-f648833b.md`) | `git ls-tree` on main shows exactly one set; brain-index regen `--check` passes |

## Department checklists (current → target, all target 10/10)

- **Learning** — 7.0 provisional (baseline 5.0). Open: battery on ALL active seats; Trial-06 (Trial-05 invalid, ceiling effect); longitudinal ≥85% application / 14 days / 60+ tasks (blocked on C5); cold successor applies a promoted lesson unaided; Projection 403 seam re-verify. Owner: LEARN area driver (Naya 4 seat). Feed #1724.
- **Brain/Memory** — 7.0. Open: PR #2065 merged; PR #1861 unblocked (rebase, fix `test` CI failure of 2026-10-09T15:49Z, green, independent review); memory metabolism continuous. Owner: Naya 5. 
- **Law/Governance** — 7.5. Open: PR #2053 merged (HELD — protected gate, Shawn's word); Scorecard Law enforcement arm live; every ratified law mechanically enforced. Owner: LAW area driver. Feed #1718.
- **Arch/Eng/Ops** — 9.7. Open: no self-merge; tip stays green; #1767 verified stable. Owner: ACT area driver. Feed #1719.
- **Evolution/Succession** — 8.0. Open: PRs #1856, #1734, #1762 merged (all CANDIDATE, merge-blocked behind base CI wave); successor package path proven (`build_successor_package()` → cold boot → continuity; ties to C4). Owner: EVOLVE area driver. Feed #1725.
- **Interfaces/Hub** — 8.8 (CONNECT) / 7.5 (Hub). Open: PR #1765 merged; door honesty sustained (DOOR-AI + DOOR-DATA live; 7 REGISTERED_CONTRACT_ONLY); daily intelligence report renders in Hub from real distilled notes. Owner: CONNECT area driver. Feed #1722.
- **Knowledge/Intelligence** — 8.9. Open: PR #1763 merged; retrieval ranks on applicability triggers (SN-0824 diagnostic: MATCH_ID 2/43); Project Intelligence freshness lint running. Owner: KNOW area driver. Feed #1720.
- **Proving/Verifying** — 9.4 / 9.2. Open: PRs #1840, #1952, #1981, #1980 merged; #1766 re-anchored (3rd) and merged; brain-index drift resolved (`--check` passes); live Supabase + PROVE-node proofs re-run (Shawn-gated). Owners: PROVE + VERIFY drivers. Feeds #1721 / #1723.
- **Innovation** — UNMEASURED. Open: assign driver + feed (proposed #1873); define 10/10; first measured scorecard. Owner: unassigned.

Each department's DONE WHEN (source pattern): scorecard reads 10/10 with an independent verification receipt proving the area's named end-to-end chain.

## Blocked on Shawn (protected gates — not team-actionable)

1. PR #2053 merge (changes delegated merge authority).
2. Production deploy (blocked on `workflow_dispatch` 403; needs his token/action).
3. Live Supabase / PROVE-node proofs (touch production data).
4. Diagnostic deploy of PR #2012 (capture the true 403 class).

## Production readiness gate (exact chain)

ALL cross-cutting DONE AND all departments 10/10 (independently verified, no self-scoring) AND zero open Shawn-gate blockers → Shawn's word → production deploy → live test (real users, real load) → SHE'S LIVE.

Governing rule quoted in source (Shawn): "Without that she has no chance." Work top to bottom; check every box with evidence.
