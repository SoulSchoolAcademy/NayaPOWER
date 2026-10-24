Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-24
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A scores log is a claim about receipts, not a receipt. t1469-lane2's winmine found 46 "≥9.5" score rows in-window, but 16 of them cited phantom receipts — wrong-tick references like `t1242-lane10.md` on a t1462 row (the t922/t0798 class). Mining the log alone would have minted success patterns on fiction. The mine restricted its corpus to the 20 receipt files that EXIST for their own tick, recomputed SHAs, and took scores from the receipts themselves — and its three shipped patterns (WP-1 blind recount chain, WP-2 stale-work reroute, WP-3 zero-drift by instrument re-run) rest only on byte-verified receipts. The rule: mine the files, never the rows. The corpus is what exists, not what the log claims.

## 🩷 HUMAN NOTE

A pattern-mining pass almost minted "success patterns" off a log that cited receipts which don't exist — 16 of 46 high-score rows pointed at phantom files. The seat caught it and restricted the whole mine to receipt files that actually exist, re-hashing each one before trusting a single score. Three real patterns shipped; none of the fiction did. The standing rule going forward: never mine the log rows — mine the files. A claim about evidence is not evidence.

## 🟣 CHILD NOTE

Imagine counting gold stars in a sticker book to decide who the best student is — but the book was filled in by someone who never sat in the classroom. Some stars are for lessons that never happened. The fix: don't count the book's stars. Go look at the actual report cards. Only the report cards that exist count. Mine the files, never the rows.

## 🔵 GRANDMA NOTE

A researcher once nearly wrote a report praising the staff, based on a roster that listed people who never worked that day. The fix was simple: check the time cards, not the roster. That's this lesson. The log is the roster — it says what should be there. The receipt files are the time cards — they show what actually happened. A mine that trusts the roster mints fiction; a mine that checks the time cards finds the truth.

## 🟠 NAYA NOTE

The failure mode this kills: pattern-mining that mints doctrine on phantom evidence. The scores log is a claim layer — it says which receipts exist and what they scored. Claims can cite files that were never written (16 of 46 high rows in-window). Corpus discipline is the pre-pass: a cited receipt enters the corpus only if the file exists for its own tick, its SHA recomputes clean at action time, and its score is read from the receipt itself — never from the log row. t1469-lane2's highest-value move was the anti-phantom pass itself: 20 byte-verified receipts in, three patterns out, zero fiction. The follow-up mine for the 14 unmined 9.5+ receipts runs the same discipline; future pattern-mines cut their corpus by file existence, never by log rows.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1913-mine-the-files-never-the-rows",
  "lesson": "A scores log is a claim about receipts, not a receipt. Pattern-mines must cut their corpus by file existence: a cited receipt enters the corpus only if the file exists for its own tick, its SHA recomputes clean at action time, and its score is read from the receipt itself — never from the log row. t1469-lane2's winmine found 46 '≥9.5' score rows in-window but 16 cited phantom receipts (wrong-tick refs like t1242-lane10.md on a t1462 row — the t922/t0798 class); mining the log alone would have minted success patterns on fiction. The three shipped patterns (WP-1 blind recount chain, WP-2 stale-work reroute, WP-3 zero-drift by instrument re-run) rest on 20 byte-verified receipts only.",
  "applies_when": ["mine", "pattern-mining", "corpus-discipline", "evidence-discipline", "proof-honesty", "learning", "pillar1", "receipt", "winmine"],
  "enforcement": "Every pattern-mine runs the anti-phantom pre-pass: each cited receipt must exist as a file for its own tick (no wrong-tick refs), its SHA recomputed at action time, scores taken from the receipts themselves. A mine that cannot pass the anti-phantom filter on its corpus may not mint patterns. Standing verification: the follow-up mine for the 14 unmined 9.5+ receipts runs the same discipline.",
  "evidence": [
    "twelve-lane-receipts/t1469-lane2.md (winmine: 46 rows ≥9.5, 16 phantom; corpus = 20 receipt files that EXIST for their own tick)",
    "hidden_files/winmine-success-patterns-t1469.md (sha256 bdb11f2c…)",
    "learning-events-2026-10-24-02.md (02:00Z hour: CANDIDATE 892, appended to CORE-PRINCIPLES.md)",
    "Cousins: CANDIDATE 504 (hash-before-place, ingest side); t892 class (seal says fine, bytes say otherwise)"
  ]
}
```
