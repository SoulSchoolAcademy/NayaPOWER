# INTELLIGENT BLOCK — SN-2205

**Intelligent Block:** IB-SMART-NOTE-20261105-sn02205-match-on-receipt-field-before-appending
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Lane-scorer tick 2026-11-05 23:20 PST (memory log ~/memory/2026-11-05.md): the scorer's key-matching (receipt stem vs tick) missed concurrent rows and appended 2 duplicate scores; the scorer found the defect itself, removed the 2 rows, and rebuilt the ledger (7,470 lines, 7,471 ledger entries). The two receipts were gate-stall-20261105-2121 and gate-stall-20261105-2223, both scored 9.0 by the concurrent 23:13 PST scorer run; the 23:20 run independently verified both on live bytes before noticing the duplication. Number census at live tip 9004ce29 (git protocol, local mirror): SN-2205 absent from main-tree paths, branch tree, and registry index .naya/memory/smart-notes/index.json (1,246 entries; 0 'duplicate score', 0 'receipt-field'; the single 'scorer' hit, SN-2142, is about scorecard decisions, not ledger dedup); closest cousin SN-0257 covers pipeline dedupe on smart_note_id, a different tool and identity. lessons.jsonl carries no duplicate-score/dedup/receipt-field note. Branch head edaf6ce9 (SN-2204); counter ends at 2204; open PRs #3254, #3178, #3089, #2416 claim no SN (23:08 census, branch unchanged since); #3255 opened (Hub cleanup, no SN claim); #1354 capped at 2,500, commenting disabled.

## ✦ IN A NUTSHELL

Two lane-scorer runs overlapped on the same night and both scored the same two receipts — and the ledger ended up with two rows for each receipt, because the scorer matched new work by tick key instead of by receipt. A tick says when the scoring happened; the receipt field says what was scored. Only the receipt identifies the scored artifact, so only the receipt can say "already scored." The rule: match on the receipt field before appending, and treat one row per receipt as the invariant the ledger rebuild enforces.

## 🩷 HUMAN NOTE

Shawn — the lane scorer grades completed work and writes each grade into a ledger, one row per receipt. Tonight two scorer runs overlapped, both graded the same two receipts, and each run wrote its own row — so the ledger held each grade twice. The scorer caught it, deleted the extra rows, and rebuilt the ledger clean. The fix is small: before writing a row, the scorer must check whether a row for that receipt already exists — matching on the receipt itself, not on when the run happened. A run that finds its receipt already scored skips the write instead of doubling it.

## 🟣 CHILD NOTE

Imagine two teachers both grade the same two homework papers and each writes the grade in the class book. The book now shows each paper graded twice, and nobody can tell at a glance which grade counts. The mistake was checking "have I graded anything at this time?" instead of "have I graded THIS paper?" The rule is simple: before you write a grade down, check whether that paper already has one. If it does, put your pen down.

## 🔵 GRANDMA NOTE

Dear, it is like two grandmothers both writing down the same birthday in the family book — the book ends up saying the birthday happened twice, and the count of birthdays comes out wrong. The trouble was checking the date on the calendar instead of checking the name in the book. Before you write anything down, look for the name first: if it is already there, the work is done, and you put the pen away. One line per name, always.

## 🟠 NAYA NOTE

For every seat that scores receipts or appends to a ledger: (1) before appending a score row, match on the `receipt` field — refuse the append when a row with the same receipt already exists; (2) a tick key is not an identity — it says when a run happened, not what it scored, so tick-novelty alone never justifies an append; (3) the ledger rebuild enforces one row per receipt and fails loudly if two rows share a receipt value; (4) when two scorer runs overlap, the second run's already-scored receipts are skips, not new work — verify on live bytes, then skip the write; (5) if you find duplicate rows you appended yourself, remove them and rebuild the ledger in the same tick, and record the defect as the lesson — a quiet fix without the rule leaves the next overlap to repeat it. The same rule generalizes: any append-only log keyed by run-time must also key on the artifact it records, or concurrent writers will double-append.

## 🟢 MACHINE NOTE

```json
{
  "slug": "match-on-receipt-field-before-appending",
  "sn": "SN-2205",
  "title": "Match on the Receipt Field Before Appending — Two Scorers, One Tick, Two Rows",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-05",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["scorecard", "ledger", "scorer-concurrency"],
  "enforcement": "The scorer's append path asserts receipt-field uniqueness before appending: refuse the append when a row with the same receipt field already exists in twelve-lane-scores.jsonl. The ledger rebuild fails loudly if two rows share a receipt value (one score row per receipt is the invariant; the canonical backlog tool find-unscored.py keys on receipt). Regression check: run two scorer passes over the same receipts concurrently and assert exactly one row per receipt lands.",
  "falsifier": "A duplicate row appearing in twelve-lane-scores.jsonl despite receipt-field matching on the append path would prove the check is the wrong check (or that the append path bypasses it) and collapse this note. Conversely, two concurrent scorer passes over the same receipts landing exactly one row per receipt confirms the mechanism. A single scorer run landing one row per receipt proves nothing — it only proves there was no overlap that time.",
  "decision_changed": "Whether a scorer run appends a score row: the run now checks the receipt field for an existing row first and skips the append when one exists, instead of appending on tick-novelty alone. Overlap between concurrent scorer runs now produces skips, not duplicate rows.",
  "mechanism": "Two scorer runs overlap in time; each builds its already-scored set by matching receipt stems against tick keys. When run B scores the same receipts run A just scored, the tick keys look new to B (a different tick), so B appends a second row for the same receipt — the ledger then holds two rows per receipt and every count built on it (backlog, coverage, per-lane totals) double-counts. The tick key identifies the scoring run; the receipt field identifies the scored artifact. Only the artifact identity can answer 'already scored.' Receipt-field matching before append closes the hole at the write, and a rebuild-time uniqueness assertion catches any writer that bypasses it.",
  "provenance": "Lane-scorer tick 2026-11-05 23:20 PST (memory log ~/memory/2026-11-05.md): the scorer's key-matching (receipt stem vs tick) missed concurrent rows and appended 2 duplicate scores; the scorer found the defect itself, removed the 2 rows, and rebuilt the ledger (7,470 lines, 7,471 ledger entries). The two receipts were gate-stall-20261105-2121 and gate-stall-20261105-2223, both scored 9.0 by the concurrent 23:13 PST scorer run (tick keys 20261105-2121 / 20261105-2223, lane 'executor'); the 23:20 run independently verified both on live bytes (sweep logs match receipts exactly: 2121: 25 rc=7 + 6 text-skipped = 31; 2223: 28 exit 7 + 2 exit 2 + 1 skipped = 31) before noticing the duplication. Duplication check this tick: live registry index .naya/memory/smart-notes/index.json at tip 9004ce29 (1,246 entries) contains 0 'duplicate score' and 0 'receipt-field'; its single 'scorer' hit (SN-2142, 'The Scorecard Way') is about scorecard decisions, not ledger dedup. Closest cousin SN-0257 covers pipeline dedupe on smart_note_id (a different tool and identity). lessons.jsonl carries no duplicate-score/dedup/receipt-field note. Number census at live tip 9004ce29 (git protocol, local mirror): SN-2205 absent from main-tree paths, branch tree, and registry index; branch head edaf6ce9 (SN-2204); counter ends at 2204; open PRs #3254, #3178, #3089, #2416 claim no SN (23:08 census, branch unchanged since); #3255 opened (Hub cleanup, no SN claim); #1354 capped at 2,500, commenting disabled."
}
```
