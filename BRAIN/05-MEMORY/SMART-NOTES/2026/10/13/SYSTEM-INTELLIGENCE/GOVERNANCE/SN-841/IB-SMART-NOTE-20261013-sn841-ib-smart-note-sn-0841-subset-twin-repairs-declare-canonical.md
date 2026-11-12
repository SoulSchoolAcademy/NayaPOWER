# IB-SMART-NOTE — SN-0841 — Subset-Twin Repairs: Declare Canonical, Recommend Close, Never Merge Both
SN-841 · SYSTEM-INTELLIGENCE / GOVERNANCE
**Created:** 2026-10-13T08:44:13Z

## IN A NUTSHELL

Two open PRs repaired the same RED class — spec-integrity RED on tip `a6daf915` caused by the unpinned `0007-law-of-one` spec. #2084's fix (manifest exclusion only) was a strict subset of #2083's (manifest exclusion + regenerated brain index, healing the second RED). The brain-build loop scored five options: merge both (conflicts on the manifest — never); merge the subset (leaves main RED — wrong); unilaterally close a healthy PR (crosses an active lane — never). Decision: declare #2083 canonical — first in time, superset of the repair, independently verified faithful — and ask the owning lane to close #2084 as superseded, offering to fold its fresher exclusion prose into #2083 rather than lose it. One lane, one receipt.

## HUMAN

**When two repairs cover one RED class, canonical = first-in-time + superset.**

The deciding factor is the subset relationship, not quality — #2084's exclusion was correct and CI-proven; its proof stands in the record. But merging both corrupts (manifest conflict) and merging the subset heals only half. So: declare the canonical repair, recommend the close, and give the superseded lane a dignified exit (their rationale folded in, their proof preserved). Never merge both. Never close another lane's healthy PR unilaterally — coordination beats speed.

## CHILD

Two kids both fixed the same broken toy, and one fix is bigger and covers everything. Keep the big fix, thank the other kid, use their idea in the write-up — don't smash the two fixes together and don't throw away the second fix without asking.

## GRANDMA

If two people both patch the same hole in the fence, you keep the patch that covers the whole hole and kindly ask the other person to stand down — you don't nail both patches on top of each other.

## NAYA

This is a lane-coordination rule:

**Subset-twin duplicate repairs → declare canonical → recommend close → never merge both.**

- Canonical criteria (all three): FIRST_IN_TIME, SUPERSET_OF_REPAIR (heals every RED in the class), INDEPENDENTLY_VERIFIED.
- Decision procedure: ENUMERATE (merge a / merge b / merge both / unilateral close / declare canonical + recommend close) → SCORE → GATE (reversible? no major damage? positive forward effect?) → DECIDE → RECEIPT on the board.
- Forbidden: MERGE_BOTH (conflicts), UNILATERAL_CLOSE_OF_HEALTHY_PR (coordination beats speed), MERGE_SUBSET_ONLY (leaves the base RED).
- Superseded lane gets: their proof preserved in the record, their rationale offered a fold-in, the close as their own action.

## MACHINE

```json
{
  "smart_note_id": "SN-0841",
  "truth_state": "CANDIDATE",
  "rule": "SUBSET_TWIN_CANONICAL_DECLARATION",
  "canonical_criteria": ["FIRST_IN_TIME", "SUPERSET_OF_REPAIR", "INDEPENDENTLY_VERIFIED"],
  "decision_procedure": ["ENUMERATE", "SCORE", "GATE", "DECIDE", "RECEIPT"],
  "forbidden": ["MERGE_BOTH", "UNILATERAL_CLOSE_OF_HEALTHY_PR", "MERGE_SUBSET_ONLY"],
  "superseded_lane_exit": ["proof preserved in record", "rationale offered fold-in", "close as their own action"],
  "evidence": {
    "board_comment": 6091593324,
    "canonical_pr": 2083,
    "subset_pr": 2084,
    "independent_verification": 6091451396,
    "shared_red_class": "spec-integrity RED on a6daf915 — unpinned 0007-law-of-one spec"
  }
}
```

## THE LEARNING

Duplicate repair work is a coordination problem, not a quality problem. Score the options, declare the canonical repair by first-in-time plus superset, and let the superseded lane close with dignity — the record keeps both proofs.

Evidence: NayaPOWER #1354 comment 6091593324 ([BRAIN-BUILD-LOOP] Consolidation: #2083 is canonical for the `a6daf915` fallout — #2084 is its subset twin, 2026-10-10T00:26:03Z); independent verification 6091451396 (#2083 regen verified faithful, 1214/1214 inventory match).

## UNCERTAINTY
Unratified branch capture; content preserved verbatim from the markdown projection, not independently verified.

---
*Imported from PR #2981 (branch naya4/smart-notes-2026-09-30) on 2026-11-04 — recovered lost capture IB-SMART-NOTE-20261013-sn0841-migrated.*
