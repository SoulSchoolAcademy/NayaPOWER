# Ledger Rebuild Folds Scores Through a Canonical Dedup Rule First — Latest Wins on (tick, lane, agent)

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01850-ledger-rebuild-needs-canonical-dedup
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-22
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 17:08 PDT smart-note-distillation tick (2026-10-22) from the lane-scorer 17:00 PDT tick report in `~/memory/2026-10-22.md` — the ledger rebuild exposed 786 duplicate score keys (370 with differing scores) and named the missing dedup rule for the director/ledger owner the same turn.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Today's lane-scorer tick rebuilt the ledger and found 5513 rows in twelve-lane-scores.jsonl collapsing to ~3646 distinct (tick,lane,agent) keys — 786 keys carry 2+ scores, 370 of them with differing scores, one batch-labeled tick ('lane-scorer-20261019-1700') with 34 scores on a single key. Prior runs appended without dedup; several old receipts show both 9.0 and 9.5 from different runs. The ledger writer carries those dupes into the ledger, so "the" score for a key is whichever row landed first/last — nondeterministic score truth downstream. The write side is now dedup-guarded (this tick's guard appended 0 rows), but the rebuild path has no rule at all. The rule: fold scores through a canonical dedup — latest score wins per (tick,lane,agent) key — before the ledger rebuild consumes them.

## 🩷 HUMAN NOTE

The score ledger had the same test graded twice with two different grades — sometimes three, sometimes thirty-four — and nobody could say which grade was real. Today's scorer fixed the intake so doubles can't get in anymore, but the ledger rebuild still has no rule for picking the real score out of the doubles already inside. The fix: when rebuilding, keep only the latest grade for each (tick, lane, agent) triple, and say so out loud.

## 🟣 CHILD NOTE

Imagine a report card where your math test shows a B, an A, and another A — from three different days. Which one counts? Without a rule, nobody knows. The rule we picked: the newest one counts. Always.

## 🔵 GRANDMA NOTE

Sweetheart, the team keeps scorecards for how the work is going. We found some scorecards were recorded more than once with different scores, and the bookkeeping had no way to pick the right one. The lesson is simple: when you copy the scores into the master book, check for doubles first, and keep the newest one. That way the book always tells the truth.

## 🟠 NAYA NOTE

Sister, this is the append-side/rebuild-side split biting us. We dedup-guarded the append (0 rows added this tick) but the rebuild still folds raw rows — 370 conflicting keys, one with 34 scores. Any director decision that reads the ledger is reading whichever dupe landed last. Latest-wins canonical dedup before folding is the whole fix; it belongs in the rebuild path itself, not in the scorer's discretion. When you own the ledger, own the dedup.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "duplicate_score_keys_without_canonical_dedup",
  "evidence": {
    "rebuild_finding": "lane-scorer tick 2026-10-22 17:00 PDT, ~/memory/2026-10-22.md: 5513 rows in twelve-lane-scores.jsonl vs ~3646 distinct (tick,lane,agent) keys — 786 keys carry 2+ scores (370 with differing scores; max 34 on a batch-labeled tick 'lane-scorer-20261019-1700')",
    "write_side": "prior runs appended without dedup; several old receipts show both 9.0 and 9.5 scores from different runs; this tick's dedup-guarded append added 0 rows",
    "read_side": "ledger writer carries dupes into the ledger; no dedup rule exists in the rebuild path"
  },
  "rule": "ledger_rebuild_applies_canonical_dedup_before_folding",
  "applies_when": [["scorecard", "ledger-rebuild"], ["scorecard", "score-dedup"], ["scorecard", "ledger-write"]],
  "enforcement": "the ledger-rebuild path (ledger_writer.py / rebuild script) gains a dedup assertion step that canonicalizes duplicate (tick,lane,agent) keys (latest score wins) before folding; a rebuild that folds raw rows with >1 score per key fails the step; the lane-scorer's dedup-guarded append is the worked reference for the write side",
  "procedure": [
    "before folding twelve-lane-scores.jsonl into the ledger, group rows by (tick,lane,agent)",
    "for any key with 2+ rows, keep the latest row; log the collapsed count per rebuild as the dedup receipt",
    "if conflicting scores survive to the ledger, the rebuild step fails loudly — never silently",
    "mirror the guard on the append side (dedup-guarded append, already in place) so both halves of the pipeline agree on canonical keys"
  ],
  "decision_change": "how the director/ledger owner rebuilds the ledger: raw rows are folded through latest-wins canonical dedup on (tick,lane,agent) instead of folded as-is",
  "falsifier": "would be proven wrong if the ledger writer already canonicalizes duplicates downstream, or if duplicate keys are shown to never influence any downstream read or decision",
  "mechanism": "conflicting scores for one (tick,lane,agent) key leave 'the' score undefined; whichever duplicate row the fold lands on wins nondeterministically, so downstream consumers (director ticks, gap recycling) read corrupted score truth; latest-wins dedup restores determinism at the fold"
}
~~~
