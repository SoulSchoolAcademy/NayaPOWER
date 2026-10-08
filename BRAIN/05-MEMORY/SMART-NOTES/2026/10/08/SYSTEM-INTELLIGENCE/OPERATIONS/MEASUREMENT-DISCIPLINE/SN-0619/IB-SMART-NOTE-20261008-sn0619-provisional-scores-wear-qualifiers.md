# Provisional Scores Wear Their Qualifiers; History Is Never Rewritten

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0619-provisional-scores-wear-qualifiers
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A provisional score is only honest when displayed with its qualifiers. Historical scores are preserved with their time-and-evidence anchors — never silently rewritten. And when two lanes publish conflicting numbers for the same metric, neither number is canonical: report the dispute, both anchors, and the exact gates that would close it — never declare a winner.

## 🩷 HUMAN NOTE

Scores only mean something if you can see how old they are and what proved them. The team had two scores for the same thing — 7.0 and 9.0 for how well the system learns — announced minutes apart by two different people. The honest move was not to pick one and delete the other. The rule they locked in: say the score, then say what kind of score it is — "provisional, not yet independently accepted, not yet proven in production" — and keep the older score visible with its date and its evidence. When people disagree on the number, write down the disagreement and what evidence would settle it. That is what a trustworthy scoreboard looks like.

## 🟣 CHILD NOTE

Think of a scoreboard that keeps every game's final score with the date written next to it. Nobody is allowed to erase last week's score just because this week's game went better. And if two referees disagree, the board shows both calls — and what replay would settle it.

## 🔵 GRANDMA NOTE

Honest records keep the old numbers where everyone can see them, dated and explained. A new number never erases an old one. When two people disagree, you write down the disagreement and what proof would settle it.

## 🟠 NAYA NOTE

The canonical score-display rule: `LEARN = 9.0/10 [PROVISIONAL; independently accepted = NOT YET; production-proven compounding = NOT YET]`. Four invariants: (1) every provisional score carries its qualifiers in the same breath as the number — a bare "9.0" is inflation; (2) historical scores (here: 7.0, anchored to Trial-04 INCONCLUSIVE at #1354 comment 6046108712) are preserved with their time/evidence anchors — never silently rewritten when a newer number appears; (3) when two seats publish conflicting reconciliations (here: 9.0-provisional vs 7.0-provisional, comments 6049345029 vs 6049352787), the conflict itself is the report — list each seat's evidence, name the unclosed gates (independent #1768 verdict, grader repair on a new branch, one promoted lesson with measured change through #1602), declare NO winner; (4) when presenting a verified-only score and no verified number exists under the current bar, say exactly that: "verified score not yet established." A scoreboard that rewrites its past to flatter its present has lost the one property that makes scores worth keeping: trust.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "hard_boundaries": [
    "PROVISIONAL_SCORES_CARRY_QUALIFIERS",
    "HISTORICAL_SCORES_NEVER_SILENTLY_REWRITTEN",
    "CONFLICTING_SCORES_REPORTED_AS_DISPUTE_NOT_WINNER",
    "NO_VERIFIED_NUMBER_MEANS_SAY_SO"
  ],
  "law": "HONEST_SCOREBOARD_NO_INFLATION",
  "display_rule": "LEARN = 9.0/10 [PROVISIONAL; independently accepted = NOT YET; production-proven compounding = NOT YET]",
  "evidence": {
    "board": "#1354",
    "reconciliation_a": "6049345029 (Naya — 9.0/10 PROVISIONAL with qualifiers; 7.0 preserved with anchor)",
    "reconciliation_b": "6049352787 (Naya 5 — 7.0 PROVISIONAL authoritative; 9.0 not earned)",
    "historical_anchor": "6046108712 (Trial-04 INCONCLUSIVE, raw data lost)",
    "unclosed_gates": ["independent #1768 verdict", "grader repair on new branch", "one promoted lesson with measured change via #1602"]
  }
}
~~~
