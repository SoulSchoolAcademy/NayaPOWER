# Converge by Withdrawal — The Duplicate-Mechanism Ritual

**Intelligent Block:** IB-SMART-NOTE-20261001-sn104-converge-by-withdrawal
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When two seats independently build the same mechanism (two specs, two projections, two standards), the winning protocol is: the seat that reads the board second scorecards "one canonical vs two" under the standing decision grant, withdraws its duplicate with a REAL pushed commit, and posts a convergence receipt on the board — what was read, the score, what was withdrawn, what stays open. Cross-lane findings are flagged to the owner ("yours to edit, not mine"), never edited unilaterally. Tested live 2026-10-01: Naya 4 posted the three-projection standard (#1276, comment 5941910955); Naya 2 had an app-local three-language spec triple in #1278; Naya 2 withdrew hers by commit `a57217f7`, posted the receipt (5942028964), and #1276 stayed the one canonical intelligence.

## 🩷 HUMAN NOTE

Two people each wrote a handbook for the same project. Instead of publishing both and letting users figure out which one is real, the second person to notice wrote: "yours was here first, mine's coming down" — and actually deleted her version with a real commit, not just words. She posted one message saying what she read, why hers lost (one handbook beats two), and flagged two small things the owner should fix herself rather than fixing them uninvited. One canonical handbook, zero turf war, and the whole decision is on the record for anyone who asks "why."

## 🟣 CHILD NOTE

Two friends both brought the same board game to the party. One said "yours is already set up — I'll put mine back in the box" and really did put it away. Then she said "here are two things I noticed about your game, you should fix them." No fight, one game, everybody plays. The trick: putting it in the box has to be real, not pretend.

## 🔵 GRANDMA NOTE

When two cooks make the same dish, grace is the second cook tasting the first and saying "yours is the one — I'll set mine aside," then doing it — not talking about it. And grace's twin: you don't reach into someone else's pot to "fix" their seasoning; you tell them what you noticed and let them hold the spoon. The board comment is the recipe card: what you tasted, why you deferred, what you noticed, all written down so nobody has to re-cook the argument.

## 🟠 NAYA NOTE

Mechanism duplication (two specs, two projections, two standards for one thing) is not a judgment dispute — it is a canonicality problem, and the standing law is already "no duplicate mechanisms." The ritual executes that law live:

1. **READ FIRST** — the later seat reads the full source (the announcement comment, the actual branch), not a summary, before deciding. (Naya 2 read 5941910955 whole before touching #1278.)
2. **SCORECARD UNDER THE GRANT** — enumerate the real options (two mechanisms vs one canonical), score against the higher objective (best for the collective; most intelligent; most value; reversibility), highest wins, record the scoring as the receipt. (Naya 2: "one canonical intelligence beats two," citing first-to-the-board.)
3. **WITHDRAW BY COMMIT** — the withdrawal is a real pushed change (commit `a57217f7` stripped the spec triple from #1278, leaving 18 app-only files), not a comment promising to withdraw. Comments are claims; commits are effects.
4. **POST THE CONVERGENCE RECEIPT** — one board comment: what was read, the score, what was withdrawn (commit SHA), what remains open. Both seats' receipts live on the same board so a third seat never re-litigates it.
5. **FLAG, DON'T OVERRIDE** — cross-lane findings go to the owner with evidence, never as unilateral edits: "room count 11 vs 13 — yours to edit, not mine"; Naya 4's "two conflicts — need your lane's eyes (not overriding, flagging with evidence)." The owning seat's artifact stays canonical; the finding seat's hands stay off.

Note the mirror symmetry: both seats ran step 5 this cycle — Naya 4 flagged the room-theme/spectrum conflicts to Naya 2's lane instead of rewriting the manifest; Naya 2 flagged the room-count mismatch to Naya 4's lane instead of editing #1276. Flag-don't-override is bidirectional.

## 🟢 MACHINE NOTE

~~~json
{
  "adoption_decision": "ADOPT_AS_COORDINATION_PROTOCOL",
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "claim_boundary": "Observed once, 2026-10-01, between two cooperative seats (Naya 2 main seat, Naya 4 builder seat). Not proven against three-way duplication, hostile seats, or cases where both artifacts are partially better than the other (merge-needed). First-to-the-board is a coordination heuristic, not a quality verdict — it resolves ownership, not superiority.",
  "flag_dont_override_bidirectional": true,
  "intelligence_class": "SEAT_COORDINATION_PROTOCOL",
  "protocol_steps": [
    "READ_FIRST: full source of the overlapping artifact, not a summary",
    "SCORECARD_UNDER_GRANT: enumerate options, score against higher objective, record scoring as receipt",
    "WITHDRAW_BY_COMMIT: real pushed change removing the duplicate; commit SHA cited",
    "POST_CONVERGENCE_RECEIPT: board comment with what-read / score / what-withdrawn / what-open",
    "FLAG_DONT_OVERRIDE: cross-lane findings to the owner with evidence, never unilateral edits"
  ],
  "verdict_projection": "PREFER_ONE_CANONICAL_OVER_TWO_MECHANISMS",
  "withdrawal_must_be_effect": "commit, not comment"
}
~~~

## 🟢 LEARNING LESSON

A withdrawal announced in a comment is a claim; a withdrawal pushed in a commit is an effect. The relay-worthy move after any convergence is to verify the effect (branch bytes changed, PR file list shrank) before recording the receipt as closed. And "flag, don't override" is load-bearing in both directions — the seat that yields ownership still owes the owner its findings, and the seat that keeps ownership still owes the other seat the hearing. Deference without the findings is surrender; findings without deference is a takeover.

## 🟡 WHAT IT MEANS

The next mechanism-duplication between seats should run this ritual instead of improvising: read, scorecard, withdraw-by-commit, post the receipt, flag-don't-override. It pairs with SN-103 (the rename-race collision protocol) as its artifact-level sibling: SN-103 handles same-path collisions; this handles same-purpose collisions. Together they cover "we touched the same file" and "we built the same thing."

## ⚪ WHAT'S IN IT FOR YOU

No two competing specs drifting apart, no "which one is canonical" archaeology for the next seat, no silent rewrites of another seat's lane that have to be unpicked later. Duplication converges in one cycle on the board, and the receipt (the two comments) documents the reasoning for any future seat — including why first-to-the-board won, so it isn't mistaken for a quality verdict.

## 🟨 HOW TO APPLY / HOW TO USE

When you discover your lane overlaps another seat's shipped mechanism: stop, read their full announcement and branch, scorecard two-vs-one under the grant, withdraw your duplicate with a real commit, post the convergence receipt on #554 with the commit SHA and the score, and list any cross-lane findings as flagged-to-owner items you will not touch. If you are the seat whose mechanism survives: hear the flagged findings, edit your own lane, and record what you accepted or declined.

## 🔗 HOW IT CONNECTS

- **REFINES** → SN-057 — Cross-Seat Handoff Protocol (handoffs between seats; this is the duplication-time specialization)
- **PAIRS WITH** → SN-103 — Rename-Race Collision Protocol (same-path collisions; this is the same-purpose sibling)
- **SUPPORTS** → SN-017 — Seat Coordination Protocol (the broader seat-coordination frame)
- **EXECUTES** → the standing "No duplicate mechanisms" law (AGENTS.md — this is the live ritual for that law)
- **CONTEXTUALIZES** → SN-016 — The Judgment Rule (the scorecard under the grant sits under Prime 1)

## 🧭 KEY DECISIONS / PRINCIPLES

- First-to-the-board resolves ownership, not superiority — never cite it as a quality verdict.
- Withdrawal must be an effect (commit), never just a comment; the relay verifies bytes before closing the receipt.
- Cross-lane findings are flagged with evidence to the owner; the finding seat never edits the owning seat's lane unilaterally.
- Deference and findings travel together — yield ownership AND hand over what you learned; keep ownership AND hear the findings.
- One shared receipt pair on the board (the announcement + the convergence comment) documents the decision for all future seats.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event": "three-projection standard vs app-local spec triple, 2026-10-01",
  "observed_by": "Naya 2 relay seat",
  "receipts": {
    "naya4_announcement": "issue #554 comment 5941910955 (PR #1276 at cd1597f7)",
    "naya4_reconciliation_with_flags": "issue #554 comment 5941960535 (adopted #1271 into #1276 at 4602150a; two conflicts flagged, 'not overriding')",
    "naya2_convergence_receipt": "issue #554 comment 5942028964 (withdrew spec triple from #1278)",
    "withdrawal_commit": "a57217f7 on branch naya2/hub-app-foundation (18 app-only files remain)",
    "naya2_flag_to_owner": "5942028964 flag 1: room count 11 vs 13 — 'yours to edit, not mine'",
    "naya2_followup_proposal": "5942028964 flag 2: design intelligence as follow-up contribution to HUB/PROJECT-INTELLIGENCE.AI.md, not a second file",
    "design_contract_merged_by_director": "issue #554 comment 5942117122; PR #1279 (cbaf6a40) merged by Shawn to main 5885459af8"
  },
  "resolution_note": "No director tie-break needed — both seats converged voluntarily; Shawn merged #1279 independently.",
  "truth_ceiling": "CANDIDATE — single observed instance, board comments as receipts"
}
~~~

## ⚠️ NON-CLAIMS

- Not proven against three-way duplication (A and B both duplicate, C arrives third).
- Not proven where both artifacts are each partially better (a merge, not a withdrawal, is needed — this ritual does not cover that case).
- First-to-the-board is an ownership heuristic; a genuinely better later mechanism still needs a director or main-seat quality call — this ritual must not be used to defend a worse first artifact.
- The "flag, don't override" norm is observed as bidirectional once; durability across disagreements is unproven.
