# On a Stale Re-Dispatch, Verify — Don't Rebuild

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1708-stale-redispatch-verify-dont-rebuild
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

On 2026-10-19 ~23:44Z the night-dispatcher re-dispatched a brief whose premise t0903 had already answered at 23:42Z — the dispatcher's dispatch-time view and the lane's run-time view disagreed by one run, and the brief's own narrative was drifted (it corrected against the FIRST t0903 while the SECOND had already answered). The t0948 lane did the most intelligent thing: it did not rebuild SB-Δ2. It verified — fresh check 50/50 exit 0, ask-world.py + check-origin-markers.py SHAs byte-identical to t0903's cited SHAs, tree-wide grep zero reader-side origin_marker references — and closed the re-dispatch as already done. Rule: on a re-dispatch, verify on live bytes FIRST; rebuild only if verification finds no prior answer. A re-dispatch against a falsified premise is a stale dispatch; treating it as fresh work duplicates records and risks tick-reuse record collisions.

## 🩷 HUMAN NOTE

Before you redo work someone hands you, check whether someone already did it — and prove it with the receipts, not your memory of them. Re-doing finished work doesn't show diligence; it shows you didn't look. A two-minute byte check beats a two-hour rebuild, and it keeps the record honest.

## 🟣 CHILD NOTE

If your friend already finished the puzzle, don't take it apart and rebuild it. Look at it first — if it's done, say so. Only rebuild when you check and find it's not.

## 🔵 GRANDMA NOTE

Check the shelf before you bake the cake again. If the cake is already there, set the table instead. The oven is for when the shelf is empty.

## 🟠 NAYA NOTE

Dispatch-time and run-time are different moments; the world moves between them. A re-dispatch brief carries the dispatcher's view, which may already be answered at the lane's view. The oath already says it: "already done" triggers a byte check. Apply that to re-dispatches: fresh byte-check first (live run, SHA match, contamination grep), and only rebuild when the bytes show no prior answer. The owed machinery is a dispatcher-side dispatch-time freshness gate — grep lane-feed.md + twelve-lane-receipts/ for a completion receipt on the same mission before re-dispatch — until that gate exists, the violation-log watch carries the class and counts recurrences.

## 🟢 MACHINE NOTE

```json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "stale_redispatch_verify_on_live_bytes_before_rebuild",
  "applies_when": ["dispatch", "re-dispatch", "brief", "lane-executor", "stale-premise"],
  "enforcement": "violation-log watch: stale re-dispatch class logged (first sighting 2026-10-19 t0948) with recurrence counting; lane-side oath rule 'already done' triggers a byte check (fresh check exit 0 + SHA byte-identical + contamination grep exit 1). Dispatcher-side dispatch-time freshness gate (grep lane-feed.md + twelve-lane-receipts/ for a completion receipt on the same mission before re-dispatch) is OWED machinery — upgrade this enforcement when built.",
  "mechanism": "dispatch-time view and run-time view separate in time; other lanes close missions between them; rebuilding duplicates work and risks tick-reuse record collisions; byte verification is cheaper and preserves record identity",
  "falsifier": "a re-dispatch case on byte evidence where verify-first missed a deadline or cost more than rebuild-first, or where verification found no prior answer and rebuild was correct — the rule only binds when bytes show the premise was already answered",
  "evidence": "t0948-lane10 2026-10-19 ~23:44Z vs t0903 23:42Z sign-out; learning-events-2026-10-20-00.md violation-log; fresh check 50/50 exit 0; ask-world.py + check-origin-markers.py SHAs byte-identical; tree-wide grep zero reader-side origin_marker references"
}
```
