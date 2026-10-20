# IB-SMART-NOTE-20260930-sn01733

**Intelligent Block:** SN-01733
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The first WINMINE extraction mined 6 success patterns from 8 receipts scoring 9.5+ — and the mining discipline mattered more than the mining: the window was named receipt-by-receipt up front, one stem-match imposter was excluded on sight (a different task wearing similar bytes), and one receipt-vs-ledger score discrepancy was flagged, not smoothed. A pattern that cites a non-task receipt isn't a success pattern — it's a collision artifact with a story.

## 🩷 HUMAN NOTE

Here's what actually happened on 2026-10-20. A lane ran the first WINMINE extraction ever — mining what "success" looks like from a cluster of 9.5+ lane receipts. Before extracting a single pattern, it named the window exactly: 8 receipts, t0970–t1024, with both scores for each (self-scorecard and scorer-ledger). Two things showed up in the window check. First, t1022 was an imposter: same receipt template, but it was an Oct-12 PR #2385 re-verify at the old tip — a different task entirely. It was excluded before mining started, with the reason on record. Second, t0983 self-scored 9.6 while the ledger's scorer-instrument scored 9.0 on it: two different instruments measuring two different things. That disagreement went on the record as a disagreement — not averaged, not smoothed. The 6 patterns that survived (seal-before-run, fresh-harness-never-inherited, the-9.0-is-a-queued-next-action, falsifiers-first, name-the-window, gate-the-delta) are each byte-quoted from at least 2 receipts, drafted in three languages (machine, AI, human), and all ship as CANDIDATE — permanence is earned through use, never granted at mining. The lesson: mining success from a dirty window manufactures confidence about nothing. Name the window, exclude the imposters, flag the disagreements.

## 🟣 CHILD NOTE

Imagine you want to find out what makes a great sandwich, so you collect your 8 best sandwiches. But one of them is actually a taco from a different restaurant's kitchen — it just came in a sandwich-shaped box. And two of your sandwich scores disagree: you gave one a 10 and your friend gave it a 6. If you don't check first, your "great sandwich recipe" will have taco seasoning in it, and you'll never know why your friends' sandwiches taste funny. Before you write the recipe: list exactly which sandwiches count, throw out the taco, and write down the score disagreement instead of splitting the difference.

## 🔵 GRANDMA NOTE

Dear, when you collect what worked, the first job is deciding what counts as "what worked" — exactly which attempts, no more and no less. A practice round isn't the real race, and one person's best day isn't another person's. Write the list down before you start looking, and don't let anything sneak in wearing the right costume. And when two scorecards disagree about the same work, don't split the difference and call it the score — mark the disagreement honestly. The honest question is worth more than a tidy average.

## 🟠 NAYA NOTE

Method, for any seat running a WINMINE extraction (12-lanes STAGE 0 item 13-0): (1) name the mining window FIRST — exact receipt paths with both scores (self-scorecard and scorer-ledger) — before extracting any pattern; (2) exclude on sight any receipt whose bytes belong to a different task (stem-match imposter) — cite the excluded path and the exclusion reason; (3) score discrepancies between self-scorecard and ledger are flagged, never smoothed — the two instruments measure different things, and the disagreement is data; (4) every pattern must be byte-quoted from at least 2 window receipts and drafted in three languages (machine / AI / human) per STAGE 0 item 0 [SMARTBLOCKS]; (5) every extracted block ships as CANDIDATE — permanence is earned through use (the 3-use permanence rule), never granted at mining. Cousins: SN-01731 (run the untested gate against itself first — sibling extraction product, falsifiers-first); SN-01732 (seal the falsifying verdict — the t1024 STOP that proved seals precede runs).

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-01733",
  "lesson": "When mining success patterns (WINMINE), name the receipt window first, exclude imposters on sight, and flag score discrepancies instead of smoothing them. A pattern that cites a non-task receipt is a collision artifact, not a success pattern.",
  "applies_when": ["winmine", "success-pattern", "receipt-mining", "extraction", "window-admission"],
  "enforcement": "WINMINE extraction receipts must name the mining window (exact receipt paths with self and ledger scores) before any pattern; any pattern citing a receipt outside the named window, or quoting a stem-match imposter receipt, fails the extraction-window check. The check runs in the daily learning review's window audit (receipts named in the learning-events log); an extraction whose window includes an imposter or that smooths a self-vs-ledger discrepancy is returned as a dirty-window extraction. Standing authority: 12-lanes STAGE 0 items 0 [SMARTBLOCKS] and 13-0 [WINMINE]; the 3-use permanence rule withholds permanence from patterns mined under a dirty window.",
  "decision_changed": "Future WINMINE extractions name the window before mining and reject outside-window receipts as evidence — the learning review treats 'the pattern came from somewhere similar' as ineligible. Lane scorers and pattern drafters never average self-scorecard and ledger scores; discrepancies go on the record as discrepancies.",
  "falsifier": "A future extraction that (a) admits a stem-match imposter into the window or smooths a self-vs-ledger discrepancy, and (b) still produces a pattern that earns 3-use permanence (registry count plus check-success-block-usage.py R1-R4 green) — the dirty-window rule is wrong, and this note reverts to OBSERVATION.",
  "mechanism": "Two mechanisms. (1) Window contamination compounds: a pattern mined from a different task's receipts recommends moves that succeeded at a different task; the imposter shares the template (stem match) but not the task, so every pattern it cites is a recommendation with the wrong context. (2) Score-smoothing hides instrument drift: the self-scorecard (builder) and the ledger score (scorer instrument) measure different things; averaging them buries the disagreement instead of investigating which instrument is wrong.",
  "evidence": "hidden_files/success-patterns-winmine-t1027.md (mined 2026-10-20 ~13:35 UTC, sha256 0a4248...): window named exactly — 8 receipts t0970-t1024 (self/ledger: 9.5/9.5, 9.5/9.5, 9.5/9.5, 9.6/9.0, 9.5/9.5, 9.5/-, 9.0/-, 9.0/9.0); t1022 excluded on sight (Oct-12 stem-match imposter: PR #2385 re-verify at old tip 665098e3f, a different task); t0983 discrepancy flagged not smoothed (self 9.6 vs one ledger entry 9.0 — distinct instruments); 6 patterns mined (seal-before-run, fresh-harness-never-inherited, the-9.0-is-a-queued-next-action, falsifiers-first, name-the-window, gate-the-delta), each byte-quoted from >=2 receipts, three-language block drafts, CANDIDATE status. twelve-lane-receipts/t1027-lane10.md (13:37Z, 9.5/10, first WINMINE extraction ever). Logged in hidden_files/learning-events-2026-10-20-14.md (14:20Z hour)."
}
```
