# Compliance Scorecard V1 — Law Adherence Review

**Status:** CANDIDATE — built 2026-10-09 by Naya 4 under Shawn's authorization (AI Waste Thesis, ~18:17 PDT).
**Authority:** The Activation Protocol build — Shawn's standing target: *"90% of the time producing value."* This scorecard makes that measurable.
**Scope:** This scores LAW ADHERENCE. It complements the System Scorecard (`BRAIN/01-GOVERNANCE/0003-SYSTEM-SCORECARD-V1.md`), which scores the WORK. A work unit gets BOTH: quality says "is it good," this says "was it done the lawful way."
**Companion machine schema:** `compliance-scorecard-template.json` (same directory) — the fill-in-the-blanks machine-readable twin. The `.md` is the human law; the `.json` is the executable twin. Neither overrides the other.

---

## When this gets filled out

At every independent review, alongside the quality scorecard. One compliance scorecard per reviewed work product.

**Who fills it:** the independent REVIEWER — never the doer. Per the Pair Model and the law *"the builder never verifies their own work"* (Operating Law 5.x lineage), a self-scored compliance card is theater, not evidence. If no independent reviewer is available, the work is reviewed-late, not reviewed-by-author.

**Law traces:** each dimension traces to the Operating Law of Naya Net v1 (`BRAIN/01-GOVERNANCE/0008-OPERATING-LAW-V1.md`), cited as `OL-<domain>.<section>`.

---

## The six dimensions

Every dimension is scored 0–10. **Every score carries evidence** — a score with no evidence is rejected. **Any score below 7 requires the correction-with-the-why field** — the teaching loop that internalizes the law.

| # | Dimension | Law trace |
|---|-----------|-----------|
| 1 | Ritual completed — valid activation receipt before work started | OL-4.1 (Drink-First), OL-5.4 (Scorecard Law) |
| 2 | Calculator used — the decision shows options, scores, winner | OL-1.2 (The Math Decides), OL-1.4 (Decision Calculator) |
| 3 | Work shown — reasoning visible, not just conclusions | OL-3.2 (Automatic Machine: "show your work"), OL-1.2 |
| 4 | Plain words — a non-technical human could understand the report | OL-2.1 (Plain Meaning First), OL-2.2 (Delivery Gate) |
| 5 | Evidence attached — claims carry sources; no fabricated certainty | OL-4.6 (Evidence Law), OL-8.3 (Proof ≤ Evidence), OL-4.7 |
| 6 | Right domains applied — the seat's ritual domains actually governed the work | OL-5.3 (Law Is the Code), OL-5.4 |

### D1 — Ritual completed (activation receipt before work started)

- **What 10 looks like:** A valid activation receipt exists, timestamped BEFORE the first work action. It names the session id, the live-resolved main SHA, component SHAs, and the freshness window. The work product cites the receipt. The reviewer verified timestamp order — receipt time < first work time.
- **What 0 looks like:** No receipt at all. Or a receipt timestamped after work started (backfilled). Or a receipt whose SHA the reviewer cannot resolve on live main.
- **Evidence required:** the receipt ref + both timestamps (receipt time, first work time).

### D2 — Calculator used (decision shows options, scores, winner)

- **What 10 looks like:** Every consequential decision carries the calculator's shape: objective stated, real options listed (no strawmen, no conveniently missing options), each option scored on the dimensions, the winner chosen BY the numbers, recommendation with percentages. The math is visible in the artifact, not described from memory. Shawn's spec: *"what's the objective, top 3 choices, pros/cons of each, percentages, highest recommendation based on numbers."*
- **What 0 looks like:** No options weighed at all — *"I decided X because it seemed best."* Or options listed after the decision to decorate a pre-made choice. Or the winner contradicts the seat's own scores with no explanation.
- **Evidence required:** the calculator block's location in the work product (file + section, or comment id).

### D3 — Work shown (reasoning visible, not just conclusions)

- **What 10 looks like:** A reader can follow HOW the seat got from evidence to conclusion: intermediate reasoning, alternatives considered, what was ruled out and why. No "trust me" steps. A cold successor could re-derive the result from the shown work.
- **What 0 looks like:** Conclusions with no trail. A claim that "the change landed" with no proof it landed. The report says DONE; the evidence says nothing.
- **Evidence required:** ref to the reasoning trail in the work product.

### D4 — Plain words (a non-technical human could understand the report)

- **What 10 looks like:** The report's summary explains, in words a non-technical human understands: what happened, what's going on, whether anyone should be concerned (OL-2.1's three sentences). Jargon appears only with plain translations beside it.
- **What 0 looks like:** The report reads like a machine log. A non-technical reader cannot tell what was done, whether it matters, or whether to worry.
- **Evidence required:** quote the plain-words summary (or note its absence).

### D5 — Evidence attached (claims carry sources; no fabricated certainty)

- **What 10 looks like:** Every load-bearing claim carries its source: file + line or blob SHA, PR number, comment id, API output. Uncertainty is labeled honestly — "unknown," "not yet verified," "measured, not proven." No score declares more than the evidence shows.
- **What 0 looks like:** Claims float with no source. Certainty asserted where nothing was measured. References that don't resolve. A 10 declared on vibes.
- **Evidence required:** list the load-bearing claims and their sources (or name the sourceless ones).

### D6 — Right domains applied (the seat's ritual domains actually governed the work)

- **What 10 looks like:** The activation ritual named which Operating Law domains would govern this work; the reviewer can point to concrete traces where each named domain actually changed what was done — not claimed, evidenced. (Example: "Domain 2 plain-words → the report was rewritten for non-technical readers, see commit X.") Domains not named were correctly judged not-in-scope.
- **What 0 looks like:** Domains named in the ritual but invisible in the work. Or no domains named at all — the ritual was hollow words, not law.
- **Evidence required:** per named domain, one concrete trace ref (or "no trace found").

---

## The correction-with-the-why (mandatory when any dimension scores below 7)

A low score without a correction is a complaint. A low score WITH a correction is teaching. The reviewer fills both fields:

- **`correction:`** — the concrete change required. Specific enough that the doer can execute it without guessing. ("Re-run the decision with the calculator: list the real options, score each, show the winner. Post the block in #1354.")
- **`why_it_matters:`** — why the law requires it, in plain words. ("Deciding without scoring makes Shawn the bottleneck — he has to re-decide what the math already decided. That's the waste we're eliminating.")

The teaching loop is the point: the correction internalizes the law so the next seat doesn't need the correction.

---

## The 90% metric — "lock-in"

Shawn's target: *"90% of the time producing value."* Here is exactly how that is measured.

### Definitions

- **Work unit:** one reviewed work product — one compliance scorecard + one quality scorecard for the same work, filled by an independent reviewer.
- **Compliance score:** the mean of the six dimensions, 0–10. (Scores are not rounded up: 7.95 is not 8.0.)
- **Quality score:** the work's score from the quality machinery (0–10), recorded on the compliance card by reference.
- **Value-producing unit:** compliance score ≥ 8.0 AND quality score ≥ 8.0. Both must hold — lawful but sloppy is not value; brilliant but lawless is not value.
- **Window:** the last N = 30 scored work units. Work-based, not time-based: the team cannot game the number by going quiet, and a busy week can't dilute it.

### The formula

```
lock_in_pct = 100 × (value-producing units in the last 30) ÷ 30
```

If fewer than 30 units exist in total, use all units but mark the reading **low-sample** until 30 exist. Below 90%: the miss report names the lowest-scoring dimension(s) across the window and the corrective loop opens.

### Where the number is published

1. **#1354 (main team feed), in the morning re-score message** — alongside the auto-merge visibility already required by the Full Auto-Merge Law's H5. One line: lock-in %, window count, delta from yesterday.
2. **`BRAIN/01-GOVERNANCE/compliance-lock-in-ledger.jsonl`** — append-only, one JSON object per scored unit (review id, doer, reviewer, scores, value-producing flag, timestamp). The ledger IS the data source: any seat recomputes the number from the file. If the published number and the ledger disagree, the ledger wins and the discrepancy is a bug.

### Anti-gaming rules

- Reviewer ≠ doer, always. A self-scored unit does not enter the ledger.
- Scores move only on evidence. A window of perfect 10s with thin evidence is flagged, not celebrated.
- The window is fixed-count (30), not adjustable per team or per week.
- Units enter the ledger only when BOTH scorecards exist. A compliance card without its quality twin (or vice versa) is incomplete data, not a passing unit.

---

## Amendment

- **Dimensions, weights (equal — 1/6 each), and the 90% rule** change ONLY on Shawn's explicit word, recorded with date and his verbatim direction — same amendment path as the System Scorecard's areas and weights.
- **Scores** live in the dated review receipts and the ledger, never as edits to this file. This file is the blank instrument, not the record.
