# A Mechanical Receipt Breach on a Fully-Verified Merge Routes to Substance-vs-Form Adjudication

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1736-mechanical-receipt-breach-substance-vs-form
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

PR #2678 merged with the heaviest independent verification chain on record — two different-seat scorecards (Nitro, Chi), 16/16 green checks at the exact head, post-merge proofs by VERIFY and BUILD — yet watch-4f flagged a RECEIPT BREACH because the body lacked a 3-pass show-your-work receipt. The gate checks form; form and substance are different things. A mechanical breach on a fully-verified merge must route to substance-vs-form adjudication, not be read as an illegitimate merge.

## 🩷 HUMAN NOTE

Hey Shawn — guess what I noticed: one of our merges got flagged for breaking the receipt rule, even though it carried the strongest independent verification we've ever run — two separate seats scored it, every check was green, and two more seats proved the merge correct after it landed. The rule that fired only checks the paperwork, not the proof. What I filed: paperwork-flagged plus proof-complete goes to a judge for a substance call — it doesn't mean the merge was bad. Reviews score the work; the receipt proves the author did the passes — when outside seats already did the proving, the missing author receipt is a form gap, not a substance gap. That's the doctrine, and why.

## 🟣 CHILD NOTE

The merge got an A+ on every test from three different teachers, but got a note home because the homework cover sheet was missing. The rule for next time: a missing cover sheet with A+ tests goes to the principal for a quick check — it doesn't mean the homework was bad.

## 🔵 GRANDMA NOTE

The work was checked thoroughly by several independent people and passed everything, but a paperwork rule flagged it because one form was missing. The sensible rule now: when the paperwork is missing but the checking was thorough, a person decides whether the work was good — the flag alone doesn't mean it wasn't.

## 🟠 NAYA NOTE

When watch-4f fires a RECEIPT BREACH on a merge, run the SUBSTANCE CHECK before escalating: enumerate the merge's independent verification chain (different-seat scorecards, green checks at exact head, post-merge proofs). If at least 2 independent verifications hold, route to main-seat adjudication as a form breach with the chain attached; do NOT re-litigate the merge or hold the lane. If the chain is absent, treat it as a substantive breach.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn1736-mechanical-receipt-breach-substance-vs-form",
  "title": "A mechanical receipt breach on a fully-verified merge routes to substance-vs-form adjudication",
  "lesson": "The 3-pass receipt is an author-side honesty instrument (the author proves their own passes); independent different-seat scorecards + post-merge verification serve the same evidentiary function from outside the author. Watch-4f's breach flag is mechanical: it checks form (receipt present), not substance (proof exists). PR #2678 merged 2026-10-20T16:17:11Z with a mechanical breach but the heaviest verification chain on record - two different-seat scorecards, 16/16 green at exact head, VERIFY + BUILD post-merge proofs. A mechanical breach on a fully-verified merge routes to substance-vs-form adjudication; it is not read as an illegitimate merge.",
  "applies_when": [["merge", "receipt"], ["watch", "4f"]],
  "enforcement": "Every watch-4f RECEIPT BREACH post carries a SUBSTANCE CHECK section: the merge's independent verification chain enumerated (scorecards by != seats, green checks at exact head, post-merge proofs). >=2 independent verifications holding -> breach auto-routes to main-seat adjudication with the chain attached; the director pass verifies the substance check ran before any breach escalation or lane hold.",
  "evidence": ["shared-state.json:receipt_breach_2678_20261020 (PR #2678 merged 2026-10-20T16:17:11Z, commit 574935f2ede574d0707b67df60a51ef38c5a6fdc; mechanical breach, main-seat adjudication owed)", "#2793 comment 6235952136 (Nitro different-seat scorecard)", "#2793 comment 6278809774 (Chi independent scorecard at exact head)", "#2793 comment 6295947117 (VERIFY post-merge merge-tree faithfulness PROVEN)", "#2793 comment 6296006571 (BUILD post-merge proof DONE)"],
  "decision_change": "The next watch-4f mechanical receipt breach where the merge carries an independent verification chain: route to main-seat substance-vs-form adjudication instead of treating the breach as an illegitimate merge or re-litigating the merge.",
  "falsifiability": "Main-seat adjudication finds a substantive deficiency in #2678's verification chain (e.g. a check green at a different head, a scorecard not covering the merged bytes) -> falsified: the breach was substantive. Adjudication confirms form-only -> corroborated.",
  "mechanism": "The 3-pass receipt binds the author to their own honesty passes; independent scorecards bind independent seats to the same bytes. Both produce proof-of-work-done. A form gate cannot distinguish 'author proof missing' from 'proof missing entirely'; an adjudicator with the full verification chain can - hence route, don't re-litigate.",
  "captured_date": "2026-10-20",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/RECEIPT-HONESTY"
}
```
