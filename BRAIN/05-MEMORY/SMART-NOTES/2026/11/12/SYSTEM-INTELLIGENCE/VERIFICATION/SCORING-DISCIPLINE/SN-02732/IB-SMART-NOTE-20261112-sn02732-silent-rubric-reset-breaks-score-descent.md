**Intelligent Block:** IB-SMART-NOTE-20261112-sn02732-silent-rubric-reset-breaks-score-descent
**Smart Note:** SN-2732
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-12 15:38 PST. Evidence read first-hand from local bytes (git protocol + on-disk ledger, zero REST quota): shared-state stand_down=false, issue_1354_comments=2500 <= board watermark 6101230756, so no GitHub fetch per budget law; local lesson review only. Score rows read from hidden_files/twelve-lane-scores.jsonl (receipt-field rows, agent Team Naya Scorer). Pre-number check (this tick, full-domain): main tip e3c06103 — BRAIN tree 2026/11/12 holds SN-2672..SN-2738 (SN-2732 absent, SN-2739 absent), .naya/capture holds no SN-27xx claims, ledger max ~SN-2717, branch naya4/smart-notes-2026-09-30 max SN-02696 plus SN-02697/02698/02700/02701 (branch numbers collide with main's different-content notes of the same numbers — known collision, not mine), counter file last line 2731 (lags main's 2738). SN-2732 and SN-2739 verified free in every readable domain.

## ✦ IN A NUTSHELL

Twelve identical gate-stall receipts descended in exact 0.5 steps — 8.5, 8.0, 7.5, all the way to 3.0 — and then the thirteenth and fourteenth both scored 8.5. The descent was never written down anywhere; it lived only as repeated scorer behavior. A fresh scorer tick re-derived from the receipt's own self-score and documentation quality, and the baseline silently reset to 8.5. An unwritten scoring convention is not a rule — it is a habit, and habits reset without announcement.

## 🩷 HUMAN NOTE

Shawn — the stall receipts were scored 8.5, 8.0, 7.5, down to 3.0, one half-point per receipt, twelve in a row. Then the next two both came back 8.5. Nothing improved — the scorer just stopped descending, because the descent was never written into its instructions; it was only something it had been doing. Two lessons: when a score jumps, ask whether the ruler changed before you celebrate or panic; and if a scoring rule matters, write it into the scorer's brief, or expect it to vanish on the next fresh run.

## 🟣 CHILD NOTE

Imagine a teacher who takes away half a mark every time you hand in the same homework again — 8.5, then 8, then 7.5. Twelve times in a row. Then one day she gives you 8.5 again. You didn't do better homework. She just forgot the rule, because nobody ever wrote it down — it was only in her head. Rules that live only in someone's head disappear. Write the rule down, or it will reset when nobody is looking.

## 🔵 GRANDMA NOTE

Dear, the scores went down half a point at a time, twelve times, neat as stairs — and then jumped right back up to 8.5. Nothing got better, love. The person doing the scoring had just been following a habit, and habits fade when they aren't written down. If a rule matters, put it on paper. And when a number jumps, don't believe the jump until you've checked whether the ruler itself changed.

## 🟠 NAYA NOTE

The verified facts: (1) Twelve consecutive gate-stall receipts on 2026-11-12, 00:54 through 12:43 PST, were scored by the lane scorer (receipt-field rows, agent Team Naya Scorer, in hidden_files/twelve-lane-scores.jsonl) in exact 0.5 steps: 0054 → 8.5, 0158 → 8.0, 0305 → 7.5, 0409 → 7.0, 0514 → 6.5, 0618 → 6.0, 0726 → 5.5, 0830 → 5.0, 0933 → 4.5, 1038 → 4.0, 1138 → 3.5, 1243 → 3.0. (2) The next two, gate-stall-20261112-1400.md and gate-stall-20261112-1503.md, both scored 8.5. (3) The 1400 scorer note states the rationale explicitly: "Score 8.5, matching the receipt's own honest self-score" — scored on documentation quality, with no mention of the descent convention. (4) No scorer row, brief, or note announces a policy change; the reset is silent. (5) Mechanism: the descent was never encoded in any rubric, brief, or check script — it existed only as repeated scorer behavior. A scorer tick re-derives its score from the receipt in front of it (self-score + documentation quality), so the baseline resets to the receipt's own 8.5. Conventions not encoded in a check decay to the default. (6) What is NOT new here: SN-2671 (a rubric change moves the median — that one is about a KNOWN scorer policy change moving the median); SN-2672 (a score without its pin is not a measurement). What IS new: this is about an UNWRITTEN convention silently resetting with no announcement — the jump looks like improvement and is not.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2732",
  "slug": "silent-rubric-reset-breaks-score-descent",
  "title": "An unwritten scoring convention resets silently: the 0.5-per-receipt stall descent broke at 8.5",
  "observation": false,
  "applies_when": [["score", "trend"], ["scorer", "rubric"], ["scorecard", "series-break"]],
  "enforcement": "Any reader of a score series (scorecard build, nightly report, lane scorer) checks for a step-break before reporting a trend: a jump of >=0.5 against the running step is flagged RUBRIC-RESET-SUSPECT and the pre/post segments are never trended as one series. And any scorer convention (e.g. a per-receipt descent) must be written into the scorer's brief or a check script — an unwritten convention is assumed to reset at the next fresh tick.",
  "evidence": "twelve-lane-scores.jsonl receipt-field rows (agent Team Naya Scorer): gate-stall-20261112-0054 8.5, 0158 8.0, 0305 7.5, 0409 7.0, 0514 6.5, 0618 6.0, 0726 5.5, 0830 5.0, 0933 4.5, 1038 4.0, 1138 3.5, 1243 3.0 (exact 0.5 descent, 00:54-12:43 PST); gate-stall-20261112-1400 8.5 and gate-stall-20261112-1503 8.5. The 1400 row's note: 'Score 8.5, matching the receipt's own honest self-score' — scored on documentation quality, no mention of the descent; no scorer row announces a policy change. Existing doctrine checked and NOT duplicated: SN-2671 (known rubric change moves the median), SN-2672 (score without pin is not a measurement).",
  "decision_change": "When a score series jumps, the first reading is a possible rubric reset, not real improvement or regression; and a scoring convention that matters gets written into the scorer's brief or a check, because an unwritten one will reset silently.",
  "falsifier": "If a scorer row or brief shows the 8.5 was a documented policy change, or if later stall receipts resume descending from 8.5 (8.0, 7.5...), the 'silent reset' reading is wrong — it was a rebase, not a reset.",
  "cousins": ["SN-2671 (A rubric change moves the median — known policy change; this note is the unwritten-convention silent reset)", "SN-2672 (A score without its pin is not a measurement — same score-integrity family)", "SN-1650 (pin the PR's state before pinning its head — same check-live-state family)"],
  "captured": "2026-11-12",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```