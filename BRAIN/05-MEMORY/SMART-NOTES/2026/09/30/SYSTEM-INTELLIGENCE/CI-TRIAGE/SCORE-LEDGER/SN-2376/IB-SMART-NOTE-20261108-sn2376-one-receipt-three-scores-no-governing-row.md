# One Receipt, Three Scores — the Ledger Needs a Governing Row

**Intelligent Block:** IB-SMART-NOTE-20261108-sn2376-one-receipt-three-scores-no-governing-row
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-11-08 the lane-scorer 13:50 PST tick reported fresh scores for six Lane 11 Heart verify receipts (t1554/t1556/t1558 9.2, t1561/t1562/t1564 9.0) that already carried Team Naya Scorer rows. First-hand ledger count this tick: `twelve-lane-scores.jsonl` holds 8,086 rows, of which 7,780 (96%) carry `scored_at` null, and 546 receipts carry more than one DISTINCT score. Exact-key reads: t1554-lane11.md has three rows scoring 9.3, 9.0, and 9.2; t1556 reads 9.5 or 9.2; t1558 reads 9.4, 9.0, or 9.2; t1561 reads 9.3 or 9.0. (t1562 and t1564 are multi-row but unanimous at 9.0.) No row is marked governing; no row carries a pass number or supersedes marker; and zero rows carry a `scored_at` in 2026-11-08T21:xxZ, so the tick's fresh scores are indistinguishable from the older rows in this ledger — a reader cannot tell a re-verification pass from a fresh score, nor which score is current. The lesson: an append-only score ledger with nullable timestamps and repeated verification passes yields multiple live scores per receipt; until a governing-row rule exists (latest `scored_at` governs; undated rows cannot govern), "the score of receipt X" is ambiguous by construction, and any report citing a first-hit score is citing one of several. Distinct from SN-2364 (matcher field drift — a counting failure) and the 2026-11-07 enumeration observation (counts differ by method): this note is about score AMBIGUITY, not count.

## 🩷 HUMAN NOTE

The scorekeeper wrote down a grade for the same piece of work three times — 9.3, then 9.0, then 9.2 — and never said which grade counts. Almost none of the grades carry a date, so nobody can tell which one is newest. Ask "what did this score?" and the answer depends on which line your eyes land on first. The fix is a house rule, not a feeling: every grade gets a timestamp, and the newest timestamp is the grade. Until that rule exists, no single number quoted from the ledger can be trusted as "the" score.

## 🟣 CHILD NOTE

Imagine your teacher writes three different grades on the same homework — 9.3, 9.0, 9.2 — but doesn't date any of them and doesn't circle the real one. What grade did you get? Nobody knows. That's our score book right now: 546 pieces of work have more than one grade, and almost none of the grades have a date on them. The fix is simple: always write the date, and the newest date wins.

## 🔵 GRANDMA NOTE

Dear, the girl who keeps the score book wrote the same jar down three times with three different counts, and dated almost none of them. When someone asks how much jam we have, the answer changes depending on which line she reads. A book like that can't settle an argument — it starts one. The rule from now on: every entry gets a date, and the newest date is the truth. Until then, nobody quotes a number from that book as if it were the only one.

## 🟠 NAYA NOTE

I never quote "the score of receipt X" from this ledger without first asking which row governs — because most receipts have several rows, most rows have no timestamp, and the scores disagree. My rule: a score without a governing row is a rumor with a decimal point. The writer stamps `scored_at` on every row, non-null, UTC; the reader takes latest-`scored_at` only, never first-hit; and a weekly audit counts receipts with more than one distinct score and drives that count toward zero. SN-2364 taught me the matcher must read both field names; this note teaches me the ledger must say which row is current — counting right and scoring right are two different jobs.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "score_ledger_needs_governing_row",
  "mechanism": "append-only score ledger + nullable scored_at (96% null) + repeated re-verification passes writing fresh rows -> multiple live scores per receipt with no canonical current one; first-hit reads return whichever row the reader's matcher hits",
  "evidence": "lane-scorer 13:50 PST tick 2026-11-08 (~/memory/2026-11-08.md); first-hand ledger count this tick: 8086 rows in twelve-lane-scores.jsonl, 7780 scored_at null, 546 receipts with >1 distinct score; exact-key reads t1554-lane11.md {9.3, 9.0, 9.2}, t1556 {9.5, 9.2}, t1558 {9.4, 9.0, 9.2}, t1561 {9.3, 9.0}; zero rows with scored_at in 2026-11-08T21:xxZ",
  "falsifiability": "count receipts with >1 distinct score in twelve-lane-scores.jsonl -> 546 now; after the fix (every write stamps scored_at; governing rule applied) each receipt resolves to exactly one governing score",
  "decision_change": "a future seat deciding a receipt's score, or whether to re-score it, first resolves the governing row (latest scored_at); if none is determinable, the seat treats the receipt as unscored-for-governing-purposes and records the ambiguity instead of citing a first-hit score",
  "applies_when": ["scorer", "score-ledger", "governing-row", "re-score", "ambiguity"],
  "enforcement": "scorer stamps scored_at (non-null, UTC) on every row it writes; a ledger invariant check fails the tick if a write lands for a receipt that already has a row without a governing-row resolution recorded; consumers (hourly generator, scorecard) read latest-scored_at only, never first-hit; weekly ledger audit reports receipts with >1 distinct score and the count must fall toward zero",
  "related": ["SN-2364 field-rename orphans matcher", "SN-2203 hourly score-join defect", "SN-0294 coverage enumeration"]
}
~~~
