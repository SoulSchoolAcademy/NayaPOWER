# The Merge→Promote→Prove Cycle — Post-Merge Parity RED Is Expected, Not a Regression

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0396-merge-promote-prove-cycle
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6004557162 (2026-10-05, [NAYA 2] Merge receipts — #1506, #1509, #1514 all landed); corroborated by #1354 comment 6004631311 (production stamps source `4a2f7282`, two commits behind main `cc2465f6`).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

After #1506, #1509, and #1514 landed on main (`cc2465f6`) while production still stamped the earlier source, the next proof run was guaranteed to show parity RED — and Naya 2 stated the classification plainly: "That's the normal merge → promote → prove cycle, not a regression." Merges move main; promotion stamps the production branch to the promoted SHA; proof verifies parity between them. Parity RED that appears *between* merge and promotion is the cycle's heartbeat, not a code failure — the next action is a promotion, never a code repair.

Why this is brain-grade: a cold successor reading a RED parity check without this lesson will do the expensive wrong thing — debug code, open a repair PR, or duplicate a mechanism that already exists. The classification rule is mechanical: if `main_tip > production.stamped_source` and no promotion run has fired since the newest merge, parity RED classifies as **CYCLE-EXPECTED**. Close the loop by promoting, then re-run proof. Cousin of SN-0235 (deployment parity is a failure class — prove the deployed artifact matches before changing code); this one covers the *timing* half of that family: parity measured mid-cycle is not a parity violation at all. Related family: SN-0392 (first RED is the only RED — read the chain top-down; a mid-cycle parity RED is upstream of any code conclusion).

## 🩷 HUMAN NOTE

Shawn — banking one classification rule from today's merge wave: right after merges land and *before* the next promotion fires, a parity RED is the normal heartbeat of the merge→promote→prove cycle, not a regression. Nobody should debug code over it; the only next action is promotion. It saves us from ever opening a repair PR for a RED that a promotion was always going to clear.

## 🟣 CHILD NOTE

Imagine three buckets: the workshop (main), the delivery truck (promotion), and the check station (proof). When new work piles up in the workshop but the truck hasn't moved it to the check station yet, the check station will say "this doesn't match." That's not broken work — it's just the truck not having run yet. Rule: after new merges land, expect the mismatch; the fix is sending the truck (promotion), not rebuilding the work.

## 👵 GRANDMA NOTE

When several fixes went in during the day, the "is everything in sync" check went red — but that was simply because the new work hadn't been moved to the live copy yet, not because anything was broken. The lesson: after changes go in, a red sync check just means "please run the promotion step now" — it never means "something is broken, start fixing code."

## 🤖 NAYA NOTE

I see this pattern constantly: RED on a dashboard and every instinct screams "repair the code." But parity has a clock. If main moved and no promotion fired, the RED is *temporal*, not structural — the system is mid-breath between merge and promote. I will check `production.stamped_source` against `main_tip` before I ever classify a parity RED as a code problem. The calm move is promotion; the panic move is a repair PR nobody needed.

## ⚙ MACHINE NOTE

```json
{
  "sn_id": "SN-0396",
  "truth_state": "CANDIDATE",
  "captured": "2026-10-05",
  "classification_rule": "IF main_tip > production.stamped_source AND no promotion run since newest merge THEN parity RED = CYCLE-EXPECTED (not code regression).",
  "correct_action": "promotion (governed dispatch), then re-run proof. Never open a repair PR or duplicate a mechanism for CYCLE-EXPECTED RED.",
  "cousins": ["SN-0235", "SN-0392"],
  "evidence": {
    "board": "#1354 comment 6004557162 (2026-10-05): 'main has moved three PRs past it, so the next proof run will show parity RED until the next promotion. That's the normal merge -> promote -> prove cycle, not a regression.'",
    "corroborating": "#1354 comment 6004631311: production stamps 4a2f7282, two commits behind main cc2465f6 — cycle in action"
  }
}
```
