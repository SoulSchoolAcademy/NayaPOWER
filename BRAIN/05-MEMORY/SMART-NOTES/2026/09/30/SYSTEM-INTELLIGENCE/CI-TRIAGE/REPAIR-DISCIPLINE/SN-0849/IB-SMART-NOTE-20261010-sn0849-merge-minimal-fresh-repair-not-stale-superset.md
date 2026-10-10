# Merge the Minimal Fresh Repair — Don't Wait for the Canonical Superset's Rebase

**Intelligent Block:** IB-SMART-NOTE-20261010-sn0849-merge-minimal-fresh-repair-not-stale-superset
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6092353249 ([NAYA 2][SCORECARD] PR #2084 — spec-integrity exclusion, 2026-10-10T01:48:13Z, decision: merge #2084 now, scored 9.0 vs 4.0) corroborated by comment 6092456735 (brain-build battery 2026-10-10T01:26Z: #2083 base stale, main moved twice, index portion already green on main, #2083 closed unmerged as superseded) — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

`spec-integrity` was red on main (unpinned Law-of-One machine spec). Two repairs existed: **#2083** (superset: index regen + exclusion — declared canonical by the brain-build loop, but built against stale tip `a6daf915` with main having moved twice since) and **#2084** (exclusion only — 5 lines, spec-integrity GREEN on its head, fresh). Naya 2's scorecard: merge #2084 now (9.0: unblocks CI, 5 lines, green, reversible) vs wait for #2083's rebase (4.0: burns time, no additional value, the index regen portion already green on main, verified by the battery). Decision: merge the minimal fresh fix now; if #2083's index portion is still needed after rebase, that's a separate decision. The battery then proved the call right — live-tip evidence showed both reds already healed by lane merges (#2084 at 01:48Z, #2080 at ~01:55Z) before any stale repair could ship, and #2083 was closed unmerged as superseded: merging it would have regressed the index basis and duplicated merged content.

Why this is brain-grade: "canonical" is a status, and status decays when the tip moves. The instinct is to honor the bigger, officially-blessed repair — but a superset whose base is stale is not more valuable than a subset that is fresh, green-on-head, and minimal; it is a time bomb wearing a medal. The selection rule is mechanical: compare the repairs against the CURRENT tip, not their declared status. If the superset's unique value is already green on main, its only remaining contribution is regression risk. Merging the minimal fresh repair first also unblocks CI immediately, which is the actual objective — the canonical superset can return as a separate decision if it still has anything to add.

Rule for a cold successor: **when two repairs race one red, score them on freshness × minimality × green-on-head, never on who was declared canonical first.** A declaration is evidence about the past; the tip is evidence about now.

## HUMAN NOTE

Two fixes for the same problem: a big official one that's gone stale, and a tiny fresh one that's already proven green. The right move is the tiny fresh one — now — not waiting for the big one to catch up. "Official" and "bigger" don't beat "current and working." Unblock the pipeline first; the rest is a separate decision.

## CHILD NOTE

Imagine two kids want to fix a broken toy. One has a huge toolbox but it's from yesterday and some tools are already used up. The other has just the one screwdriver you need, right now. You pick the screwdriver — the toy gets fixed today, not tomorrow. The big toolbox can come back if it's still needed.

## GRANDMA NOTE

When there are two ways to fix something — a big complicated one and a small simple one that already works — take the small simple one first. It fixes the problem today. The big one can wait its turn; if it's still useful later, that becomes a new decision.

## NAYA NOTE

Shawn, when the lanes had two competing spec-integrity repairs, Naya 2 didn't wait for the officially-canonical superset — its base was stale and its unique value was already green on main — she merged the 5-line fresh fix at 9.0/10 and unblocked CI immediately. The battery later confirmed: both reds were healed by lane merges before any stale repair shipped. The team rule this firms up: canonical status decays with the tip; score repairs on freshness, minimality, and green-on-head.

## MACHINE NOTE

```json
{
  "intelligent_block": "IB-SMART-NOTE-20261010-sn0849-merge-minimal-fresh-repair-not-stale-superset",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "provenance": {
    "board_comments": [6092353249, 6092456735],
    "board": "#1354",
    "decider": "Naya 2",
    "merged_pr": 2084,
    "superseded_pr": 2083,
    "created_at": "2026-10-10T01:48:13Z"
  },
  "lesson": {
    "pattern": "canonical_status_decays_with_tip",
    "selection_rule": "score_repairs_on_freshness_x_minimality_x_green_on_head",
    "scores": {"merge_minimal_fresh_2084": 9.0, "wait_for_superset_rebase_2083": 4.0},
    "rule": "a_declaration_is_evidence_about_the_past_the_tip_is_evidence_about_now"
  },
  "related": ["SN-0493", "SN-0780", "SN-0419"]
}
```
