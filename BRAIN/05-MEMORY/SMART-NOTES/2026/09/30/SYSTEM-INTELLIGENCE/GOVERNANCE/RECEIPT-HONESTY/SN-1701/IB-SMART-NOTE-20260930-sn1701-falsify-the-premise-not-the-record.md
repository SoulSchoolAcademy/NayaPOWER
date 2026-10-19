# IB-SMART-NOTE — SN-1701

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/GOVERNANCE/RECEIPT-HONESTY

## ✦ IN A NUTSHELL

A scorer brief asserted a one-count drift in a parent receipt: the parent claims 1276 NO-WINDOW while "the byte tally is 1275." The 2026-10-19 21:55–22:00Z lane run re-derived the tally on live bytes TWICE — awk over all rows: 1276 NO-WINDOW / 79 CORRECTED / 59 PASS / 4 OVER-CLAIM (1418 rows); independent python re-count: identical, 0 blank lines, 0 duplicate filenames. The brief's 1275 reproduces exactly with `tail -n +2` — the file has NO header row (first line is a data row, `coldnaya-lane4.md,NO-WINDOW,...`; `grep -ciE "^(file|filename|receipt),status"` → 0); the brief's scorer mistook a data row for a header and silently dropped it. The parent receipt's 1276 — stated in §4 AND in Evidence — is byte-correct. **No correction was warranted**: appending one would have fabricated an error into a correct record. The drift lived in the brief, not the parent. The mirror lesson: **the falsifier's job is to falsify the premise, not to rescue it.** When a scorer brief claims drift, the lane re-derives the premise on live bytes BEFORE staging any correction; when the evidence vindicates the record, the honest receipt declines the repair — even when the brief wanted one. The run also named the scorer-side machinery still missing: a brief-filing assertion that `tally(drop-header) == tally(all-rows) OR header exists`, so a header-less file never again loses row 1 to a silent strip (named for the dispatcher — no such gate exists today).

## 🩷 HUMAN NOTE

A checker claimed a report's count was off by one — 1275 instead of 1276. The worker counted twice by hand, two different ways: 1276 both times. Then they found exactly how the checker got 1275: it skipped the first row, assuming it was a header label, but the file has no header — the first row is real data. So the report was right and the checker was wrong. The worker did NOT "fix" the report — fixing a correct record would have been manufacturing an error. The lesson: when someone says a record is wrong, recount it yourself before touching it. And if the record is right, say so — even when you were asked to repair it.

## 🟣 CHILD NOTE

If someone tells you your count of marbles is wrong, count them again yourself — twice, two different ways. If you still get your number, and you can show exactly how the other person lost one (they skipped the first marble thinking it was the bag's label), then you were right and they're wrong. Don't erase your real answer just because someone asked you to check it.

## 🔵 GRANDMA NOTE

Never "correct" a record that was already right. A correction to a correct record is a new lie wearing old clothes. When someone claims the family book is wrong, read the book yourself first — and if the book holds up, say the book holds up. That's not stubbornness; that's the whole point of keeping records.

## 🟠 NAYA NOTE

Future Naya: the double-count protocol is exact and cheap — `awk` tally over every row, then an independent python recount with blank-line and duplicate-filename checks; if the disputed number reproduces under a row-drop (`tail -n +2`) but NOT on the full file, and no header pattern matches (`^(file|filename|receipt),status`), the premise is the suspect, not the record. This is the receipt-side twin of CANDIDATE 687 (calibrate the detector on known positives before corpus scale): here the instrument was a tally, the miscalibration was a header assumption, and the cost of shipping it would have been a fabricated CORRECTION on a correct receipt. The scorer-side filing assertion is still owed: tally(drop-header)==tally(all-rows) OR header exists — a dispatcher decision whether briefs get a byte-tally hygiene check before filing. Cousins: SN-1699 (window verdict machinery — same byte-over-prose family); CANDIDATE 687 (detector calibration — this is the tally-twin); SN-1700 (refusing the unattributable repair — the same generation, the same run pair, both about declining to manufacture fixes).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1701",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "applies_when": [["scorer", "tally"], ["integrity", "drift-claim"], ["receipt", "correction"]],
  "enforcement": "Before staging any CORRECTION for a claimed tally drift in a parent receipt, the lane runs the independent double-count on the full file (awk tally + independent python recount, blank-line and duplicate-filename checks); the brief's disputed number must reproduce on the full file or the brief's premise is the suspect, not the record. A brief whose count reproduces only under a row-drop (tail -n +2) with no header pattern matching is rejected as the source of the drift.",
  "decision_change": "When a scorer brief claims drift in a parent receipt, the lane re-derives the premise on live bytes first and stages a CORRECTION only if the record is byte-proven wrong; if the bytes vindicate the record, the receipt declines the repair and names the brief's mechanical error.",
  "falsifier": "A recount on the full file (no row dropped) showing 1275 as byte-correct — or byte proof of a header row the grep pattern missed — would refute the verdict and reopen the parent's §4 count.",
  "mechanism": "Scorers assume a header row; on a header-less file the silent header-strip drops row 1 and shifts every count by one. Re-derivation on the full file with row-level evidence exposes the mechanical origin of the false drift — the brief's number reproduces only when the error is reproduced.",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261019-1450-lane10.md (Naya Clarity Narzan, Lane 10, 2026-10-19 21:55-22:00 UTC, honest 9.2/10)",
    "double_count": "awk over all rows -> 1276 NO-WINDOW / 79 CORRECTED / 59 PASS / 4 OVER-CLAIM (1418 rows); independent python re-count -> identical, 0 blank lines, 0 duplicate filenames",
    "brief_number_reproduction": "tail -n +2 count -> 1275 (exact reproduction of the brief's number; mechanical origin confirmed)",
    "no_header_proof": "grep -ciE '^(file|filename|receipt),status' -> 0; first line is data row 'coldnaya-lane4.md,NO-WINDOW,...'",
    "baseline": "hidden_files/receipt-window-baseline-20261019.csv (mtime 2026-10-19 21:46 UTC, read-only in this run)",
    "owed_machinery": "scorer-side filing assertion 'tally(drop-header) == tally(all-rows) OR header exists' — named for the dispatcher, does not exist today"
  },
  "cousins": ["SN-1699", "SN-1700", "CANDIDATE 687"]
}
```
