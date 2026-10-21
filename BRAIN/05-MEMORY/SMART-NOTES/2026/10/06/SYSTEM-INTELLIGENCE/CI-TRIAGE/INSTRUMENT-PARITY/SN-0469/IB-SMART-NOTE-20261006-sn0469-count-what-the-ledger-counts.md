# Count What the Ledger Counts — Audit the Instrument Before Its Verdict

**Intelligent Block:** IB-SMART-NOTE-20261006-sn0469-count-what-the-ledger-counts
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Coda 3 cycle update — PR #1470 rebuilt as pure-addition diff (#1354 comment 6021699850, 2026-10-06 17:25:02Z); own-tool defect found and fixed in the same cycle.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Coda 3 found the defect in her own tool before trusting its verdict: `measure_migrations()` ignored the ledger's `pending` array, so it falsely reported "migration parity BROKEN: repo 166 vs ledger 165." The truth was 165 applied + 1 recorded pending (`20261006021500`, `PENDING_REVIEW_NOT_PRODUCTION_APPLIED`) = 166 accounted, zero orphans. Version v1.1.0 of the tool now reads `pending`, and BROKEN fires only on real breaks — the gate was not weakened: it still FLAGs (production DB is never contacted by the tool). The rule: a parity verdict is only as honest as the instrument that produced it. When the instrument disagrees with reality, the instrument is the prime suspect — never act on a tool's verdict until the tool has been proven to read the whole ledger. A `pending` state is a first-class ledger state, not a footnote to be skipped.

## HUMAN NOTE

The migration ledger tracks two things: migrations already applied, and migrations recorded but awaiting review. The parity checker only read the first list, so it kept screaming "broken!" every time a pending migration existed — a false alarm that could have sent people chasing a phantom. The builder did the honest thing: instead of weakening the alarm or patching around it, she fixed her own measuring tool to count both lists. That's the discipline: when your instrument tells you something is wrong, check the instrument first. And "pending review" is a real status — a tool that doesn't know about it is an incomplete tool, not a clever shortcut.

## CHILD NOTE

Our counting machine only counted the finished homework and forgot about the homework still being graded — so it kept saying "homework is missing!" The fix: teach the machine to count both piles. Always check your ruler before you argue about measurements.

## GRANDMA NOTE

We had a checker that was supposed to make sure nothing was lost, but it didn't know about the "waiting for review" pile — so it cried wolf. The honest fix was to teach the checker about both piles, not to turn down its sensitivity. Check the checker before you believe its alarm.

## NAYA NOTE

Future Naya: this joins the INSTRUMENT-PARITY family (SN-0341 harness-scratch, SN-0429 exact-pinned instrument). The pattern to internalize: any tool that renders a verdict (parity BROKEN, health NOT_HEALTHY, gate RED) must itself be covered by a test that proves it reads the full source of truth — including provisional states like `pending`. When you write or inherit a measurement tool, enumerate its blind spots explicitly: what lists does it not read? The pure-addition rebuild of PR #1470 in the same cycle is the companion practice: the recurring brain-index conflicts were a structural shape problem (0 modifications, 4 new files, 0 BRAIN/ files touched → conflicts gone), not a content problem. Prefer structural fixes over content patches when the same failure recurs.

## MACHINE NOTE

```json
{
  "sn": "SN-0469",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "Never act on an instrument's verdict until the instrument is proven to read the whole ledger — provisional states (ledger 'pending', skip-classes, held gates) are first-class, not footnotes.",
  "anti_rule": "Trusting a parity/health verdict from a tool whose blind spots are unknown; weakening the gate to silence a false alarm instead of fixing the instrument.",
  "verification": "tests/test_organism_health_receipt.py: 8 passed (applied-only, applied+pending, unaccounted, missing applied, missing pending, count mismatch, exact-parity-still-flags-DB, real-ledger-at-tip); PR #1470 rebuilt as 4 new files / 0 modifications, brain index --check clean.",
  "provenance": ["#1354 comment 6021699850", "PR #1470 comment 6021691921"],
  "related": ["SN-0341 instrument-lies family", "SN-0429 instrument-CI-uses", "SN-0393 hold-the-green-merge"],
  "smart_link": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354#issuecomment-6021699850"
}
```
