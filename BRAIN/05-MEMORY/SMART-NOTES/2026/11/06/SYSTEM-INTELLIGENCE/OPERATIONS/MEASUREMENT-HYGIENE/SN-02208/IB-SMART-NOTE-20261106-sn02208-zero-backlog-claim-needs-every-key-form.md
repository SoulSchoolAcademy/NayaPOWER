# INTELLIGENT BLOCK — SN-2208

**Intelligent Block:** IB-SMART-NOTE-20261106-sn02208-zero-backlog-claim-needs-every-key-form
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Lane-scorer tick 2026-11-06 01:30 PST, recorded in ~/memory/2026-11-06.md ("Lane-scorer tick — 2026-11-06 01:30 PST"): prior scorer ticks claimed "unscored backlog = 0 of 2113 receipts" (e.g. the 00:35 tick note); reconciliation under every plausible (tick, lane) key form finds that claim WRONG — true unscored backlog was 61 before the tick, 55 after scoring the 6 oldest. Duplication check this tick: branch naya4/smart-notes-2026-09-30 tip 4c81eed5 (SN-02207) carries no unscored-backlog note (grep: 0 hits for "unscored backlog" / "backlog count" / "backlog = 0"); nearest cousin SN-01851 covers a different mechanism (a JSON-lane regex misreading markdown receipts, overcounting) — this note is the false-zero direction, a key-form miss, not a format miss.

## ✦ IN A NUTSHELL

A scorer that reports "unscored backlog = 0" can be wrong by 61 receipts and never know it. The lane-scorer tick at 01:30 PST found the standing claim — "unscored backlog = 0 of 2113 receipts" — false: reconciling the count under every plausible (tick, lane) key form showed a true unscored backlog of 61, falling to 55 after the tick scored the 6 oldest stall receipts. The lesson: **a zero backlog claim is only as good as the key forms its query reconciles.** One key form returns the count of one partial view, not of the ledger — and zero from a partial view is the most dangerous miscount there is, because it reads as "done" and stops the sweep while the unscored work sits uncounted. The daily scorecard tracks the reconciled number (55), never the single-query number (0).

## 🩷 HUMAN NOTE

Shawn — the scorekeeper was telling us "nothing left to grade" when 61 receipts were still ungraded. The counter was only looking in one drawer of the filing cabinet, so it reported zero — and zero looks like "done," which is exactly why it's dangerous: it stops anyone from looking further. The fix is simple and now standing: before anyone reports "backlog is zero," they must count every drawer — every way a receipt can be filed — and the daily scorecard carries the reconciled number (55 tonight), not the single-drawer number. Filed as Smart Note candidate SN-02208.

## 🟣 CHILD NOTE

Imagine you count the dirty dishes by opening only the top drawer of the dishwasher — it's empty, so you say "no dishes to wash!" But there are 61 dirty plates sitting in the bottom drawer you never opened. Saying "zero" when you only checked one drawer isn't counting — it's guessing with confidence. The rule is: open every drawer before you say zero, and write down the number you get from all the drawers together.

## 🔵 GRANDMA NOTE

Dear, it is like counting the library books by checking only the shelf by the door — empty, so you announce the library has no books left to shelve. Meanwhile sixty-one books are waiting on the back shelves, uncounted, because nobody looked there. A zero that comes from looking in one place is not a zero — it is a blind spot wearing a number. The rule is: walk every aisle before you say the shelves are empty, and put the walked number on the board, not the one-aisle number.

## 🟠 NAYA NOTE

For every seat that scores receipts or reports a backlog: (1) never report "unscored backlog = 0" from a single key-form query — reconcile the count under every plausible (tick, lane) key form first, and report the reconciled number; (2) the daily scorecard tracks the reconciled number (55 on 2026-11-06), and a "0 backlog" claim is only reportable after that reconciliation; (3) the backlog sweep works oldest-first from the reconciled set — this tick scored the 6 oldest unscored stall receipts (gate-stall-20261029-1430, seat-stall-20261030-0938/-1251/-1356/-2129/-2235, all 9.0), leaving 55 with the oldest remaining seat-stall-20261030-2338 and the Oct 31 seat-stall run; (4) the 61 were almost all Oct 29–Nov 5 gate-/seat-stall receipts plus distill-monthly-20261101 and weekly-distill-20261101-librarian-heir — stall receipts are the class most likely to be missed, because they accumulate while the queue is frozen; (5) the follow-up finding stands with this lesson: no lane-sweep log survives before 2026-11-05, so per-attempt exit codes for those older receipts rest on the receipts' own listings — a receipt is the only record when the log is gone, so the receipt must carry the full listing.

## 🟢 MACHINE NOTE

```json
{
  "slug": "zero-backlog-claim-needs-every-key-form",
  "sn": "SN-2208",
  "title": "A Zero Backlog Claim Is Only as Good as Its Key Forms",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-06",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": [["scorecard", "backlog"], ["scorer", "ledger"], ["measurement", "count"]],
  "enforcement": "The daily scorecard's unscored-backlog number is produced only by reconciling the count under every plausible (tick, lane) key form; a '0 backlog' claim is reportable only after that reconciliation, and the scorecard tracks the reconciled number, never the single-query number. The scorer's backlog sweep works oldest-first from the reconciled set. Regression check: run the single-form query and the every-form reconciliation side by side on a ledger holding receipts under mixed key forms and assert they disagree (single-form reports 0, reconciliation reports the true count); on a ledger with uniform key forms assert they agree, including on 0.",
  "falsifier": "If a single-form query and the every-form reconciliation agree on the count — including agreeing on 0 — across ledgers with mixed key forms, the premise fails and this note collapses. If the 55 remaining receipts turn out to be scored already under a form the reconciliation double-counted, the 61 figure is falsified and the count must be re-derived.",
  "decision_changed": "How the scorer reports backlog: the daily scorecard tracks the reconciled unscored count (55 on 2026-11-06) instead of the single-query claim (0), and a 'backlog is zero' claim is only made after every-key-form reconciliation — so a false zero can no longer stop the backlog sweep.",
  "mechanism": "The ledger keys receipts under (tick, lane) forms, and different receipts are keyed under different forms. A count query that uses one key form silently excludes every receipt keyed under another form — the query returns the count of one partial view, not of the ledger. Zero from a partial view is the most dangerous miscount because it reads as 'done' and stops the sweep, while the unscored work sits uncounted. Reconciling under every plausible key form turns the count from a query result into a ledger fact.",
  "cousins": ["SN-01851 (parse the declared lane, not the JSON shape — the sibling measurement-hygiene failure in the other direction: a format miss that overcounted pending receipts; this note is the key-form miss that undercounted to a false zero)", "SN-01649 (stall-sweep escalation — the stall receipts this backlog is mostly made of)"],
  "provenance": "Lane-scorer tick 2026-11-06 01:30 PST, recorded in ~/memory/2026-11-06.md: 'BACKLOG CORRECTION: prior scorer ticks claimed \"unscored backlog = 0 of 2113 receipts\" (e.g. the 00:35 tick note). Reconciliation under every plausible (tick, lane) key form finds that claim WRONG: true unscored backlog was 61 before this tick, 55 after (oldest remaining: seat-stall-20261030-2338 and the Oct 31 seat-stall run). The 61 are almost all Oct 29–Nov 5 gate-/seat-stall receipts plus distill-monthly-20261101 and weekly-distill-20261101-librarian-heir. Daily scorecard should track 55, not 0. Ledger rebuilt: 7,489 entries.' This tick scored the 6 oldest unscored stall receipts, all 9.0 (gate-stall-20261029-1430, seat-stall-20261030-0938, -1251, -1356, -2129, -2235). Follow-up the same tick: full-tree search confirms no lane-sweep-*.log exists before 2026-11-05 (30 logs total, oldest lane-sweep-20261105-1658.log), so per-attempt exit codes for older stall receipts rest on the receipts' own listings. Duplication check this tick: branch naya4/smart-notes-2026-09-30 tip 4c81eed5 (SN-02207) — grep 0 hits for 'unscored backlog' / 'backlog count' / 'backlog = 0' across BRAIN/05-MEMORY/SMART-NOTES/; counter ends at 2207; open PRs #3256, #3255, #3254, #3178, #3089 claim no SN file; #1354 capped at 2,500 comments, commenting disabled 2026-10-10, board fetch skipped per the cheap check (shared-state issue_1354_comments=2500, watermark 6101230756)."
}
```
