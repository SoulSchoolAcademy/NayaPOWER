# Duplicate-Seam Detection — Diff the Diffs Before the Merge List Gets Two of the Same Repair

**Intelligent Block:** IB-SMART-NOTE-20260930-sn052-duplicate-seam-merge-routing
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 02:45 PDT distillation tick (2026-10-01) from the overnight run 02:18 PDT tick entry (drive-loop finding) and #554 factual comment 5928421888; byte-identity verified independently this tick by diffing both PR diffs live.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Parallel lanes building repairs against the same backlog will sometimes land the same repair twice. On 2026-10-01, PR #1238 (`naya4/selfbuild-ledger-metadata-drift` @ `1297013c6`, statement_count 19 → 3 on pending ledger entry `20261001030000`) and merge-listed green PR #1209 (`fix/ledger-statement-count-20261001030000` @ `1a256233a`) were diffed live this tick: **byte-identical modulo index lines** — the same single-field ledger change, the same migration path, the same entry. The drive-loop flagged it first, posted factual comment 5928421888, and the overnight run recorded the routing note: merge #1209 (merge-listed, green), close/redirect #1238 — the Director's merge call, not the lanes'. The lesson is the protocol: (1) when two PRs claim the same repair, diff the diffs — compare the actual changed bytes, not titles or descriptions; (2) if byte-identical, one merge + one close/redirect — never let both sit in the merge queue, never merge both; (3) the routing note goes on the board with the numbers and the merge call stays with Shawn; (4) this is a coordination artifact, not a blame artifact — both lanes were working correctly, and credit stays with both.

## 🩷 HUMAN NOTE

It's like two cooks both fixing the same recipe card in the kitchen — each one corrects the same typo and hands you the card. You don't need two corrected cards; you take one, thank both cooks, and file the other. The trick is checking the actual words on the card, not just the note that says "fixed the typo" — because two different typos look identical in a note.

## 🟣 CHILD NOTE

Imagine you and a friend both draw the same missing piece for a puzzle and hand it to the teacher. The teacher doesn't need two pieces — she checks that they're really the same shape, picks one to put in the puzzle, and says thank you to both of you. Checking the actual shape matters: two pieces that both "look right" might be for different holes.

## 🔵 GRANDMA NOTE

It's like two grandchildren both paying the same electric bill on the same afternoon — both were trying to help, and both receipts show the same amount. You don't pay it twice; you compare the receipts, keep one, and mark the other "already paid — thank you." The key step is reading the actual receipt, not just hearing "I paid the bill."

## 🟠 NAYA NOTE

Run this every time the board or the merge list shows two PRs touching the same file/entry: (1) fetch both diffs (`/pulls/<n>` with the diff accept header) and diff them — byte-identical (modulo index lines) means same seam, same repair; (2) if identical: route — merge the merge-listed/canonical one, close/redirect the other with a pointer comment on the board (this tick's precedent: merge #1209, close/redirect #1238, comment 5928421888); (3) merge authority stays with the Director — the note is a routing recommendation, never an authorization; (4) credit both authors in the note; (5) if the diffs differ in any byte beyond index lines, they are NOT the same seam — keep both and note why. Never merge both copies of a duplicate seam; the second merge is pure churn with zero delta.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "duplicate_repair_seam_parallel_lanes_merge_queue_collision",
  "evidence": {
    "prs": "#1238 (naya4/selfbuild-ledger-metadata-drift @ 1297013c6) vs #1209 (fix/ledger-statement-count-20261001030000 @ 1a256233a), both base main, both open",
    "byte_verification": "both PR diffs fetched live 2026-10-01 02:45 PDT tick; diff of diffs: IDENTICAL modulo 'index <sha>..<sha>' lines — one hunk, supabase/PRODUCTION-MIGRATION-LEDGER-V1.json, statement_count 19 -> 3 on entry 20261001030000_disconnect_stop_future_v1",
    "board_comment": "5928421888 — drive-loop factual duplicate-seam notice",
    "run_file": "overnight-run-2026-10-01.md, 02:18 PDT tick — routing note: merge #1209, close/redirect #1238 (Shawn's merge call)"
  },
  "rule": "diff_the_diffs_one_merge_one_close_redirect",
  "procedure": [
    "when two PRs touch the same file/entry, fetch both diffs and diff them",
    "byte-identical (modulo index lines): route — merge the merge-listed one, close/redirect the other with a board comment",
    "routing recommendation only — the merge call stays with the Director",
    "any byte difference beyond index lines means different seams — keep both, note why"
  ],
  "related": ["SN-039 (merge-carry-forward regression — audit against the reconciled base)", "SN-033 (collision registry — first-claim stands)"]
}
~~~
