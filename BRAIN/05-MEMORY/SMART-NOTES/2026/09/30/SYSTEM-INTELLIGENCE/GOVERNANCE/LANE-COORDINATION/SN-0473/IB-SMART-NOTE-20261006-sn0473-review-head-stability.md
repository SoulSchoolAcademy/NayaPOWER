# Intelligent Block: SN-0473
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Concurrent force-refreshes cancel review. In the Round-2 evidence-integrity cycle, moving the review head repeatedly killed an in-flight review — so a rebuilt scoring override (extras could set the accuracy weight to 0 and still PASS) was repaired as an **isolated #1631** instead of another write to the shared #1629, explicitly to avoid concurrent writes. Standing coordination lesson: keep the review head stable until a concrete finding — or a necessary base change — warrants movement.

## HUMAN NOTE
If someone is reviewing your work, don't move the floor under them. Every time you force-push or rebase mid-review, the review has to start over — and it probably won't.

## CHILD NOTE
Don't move the table while someone is reading the map on it.

## GRANDMA NOTE
Let people finish what they're reading before you shuffle the papers.

## NAYA NOTE
Lane-coordination rule: when a review is in flight, the review head is frozen. Two motions only: (1) a concrete finding the review itself produced, or (2) a necessary base change (upstream tip moved, base no longer valid). Anything else — force-refresh, rebase, "just one more commit" — cancels the review and wastes the lane's time. If a second repair is needed on the same surface, isolate it (separate PR/branch) rather than churning the under-review head.

## MACHINE NOTE
{"sn":"SN-0473","doctrine":"review-head-stability","anti_pattern":"concurrent-force-refresh","warranted_moves":["concrete-finding-from-review","necessary-base-change"],"remedy":"isolate-second-repair-as-separate-PR","example":"PR #1631 isolated from #1629 to avoid concurrent writes; scoring override: extras could set accuracy weight to 0 and still PASS","status":"CANDIDATE"}

## EVIDENCE
- #1354 comment 6022567221 ([NAYA][CYCLE RESULT], 2026-10-06 18:14 UTC) — "Coordination lesson: concurrent force-refreshes canceled review — keep the review head stable until a concrete finding or necessary base change warrants movement."
- Same comment — new reproduced scoring override repaired as isolated #1631 (head `dbdcb783`) "to avoid concurrent writes to #1629"; "864 Python PASS/11 SKIP; 269 Node PASS; fetched/tested trees equal; all 4 GitHub workflows SUCCESS."
- Same comment — constraint named: "original experiment fixtures remain unavailable; no synthetic substitute."
