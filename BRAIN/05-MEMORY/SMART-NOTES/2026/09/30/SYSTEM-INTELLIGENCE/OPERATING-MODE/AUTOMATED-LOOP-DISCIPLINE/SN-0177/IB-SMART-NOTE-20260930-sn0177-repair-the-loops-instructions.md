# Repair the Loop's Instructions, Not the Instance

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0177-repair-the-loops-instructions
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5947578719 (Naya 2 relay, 2026-10-02T07:41:52Z) — receipt on the #1315 repair thread: PR #1315 closed unmerged at 07:31:59Z (comment 5947417268) as a byte-identical duplicate repair of the same RED class already covered by canonical open repair #1312; root cause named: the 07:26Z scheduled loop run opened the repair without checking for in-flight work. Acknowledged by Naya 4, 5947765882 (2026-10-02T07:56:28Z).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #1315 was opened by a scheduled 07:26Z loop run as a repair of the 05-MEMORY domain-count RED (ledger 21→26 + index regen on main tip 25268675) — while canonical repair #1312 was already open for that exact RED class on the same base. It was closed unmerged an hour later, byte-identical to the work #1312 already covered, and the close was correct under standing law (one open repair per RED class, SN-117 family). But closing the duplicate is only half the fix: the recurrence was produced by an *automated loop*, and its root cause was named in the close comment — the loop opened without checking for in-flight repair work. The durable repair targets the mechanism, not the instance: the loop's standing instructions gain the in-flight-scan discipline, so the mechanism cannot re-create the duplicate. The rule: every automated loop is an executing seat. It must carry the same scan-before-execute discipline as a human-driven lane (SN-108's "scan the board for in-flight execution before executing," SN-115's three-layer registry: board + open repair PRs + branch tree). When a recurrence arrives from a scheduled loop, ask "what did the loop's instructions fail to check?" and repair that — repairing only the instance leaves the loop free to produce the duplicate again on the next tick.

## 🩷 HUMAN NOTE

Shawn — a scheduled loop opened PR #1315 as a duplicate of the repair work #1312 was already doing, because the loop's instructions didn't include the "check for in-flight work first" step that the lanes all follow. The duplicate was closed correctly, but the lasting fix went into the loop's own instructions so it can't happen again. New rule: automated loops are executing seats — they get the same scan-before-you-act discipline, and when a loop produces a bad output, we fix the loop, not just the output.

## 🟣 CHILD NOTE

Imagine a robot helper that runs every morning to clean the kitchen — but nobody told it to check whether someone already started cleaning. It cleans the kitchen twice and makes a mess of the schedule. The fix isn't just undoing today's double-cleaning — it's adding one line to the robot's instructions: "look to see if cleaning already started before you start." That's what we did here.

## 🔵 GRANDMA NOTE

It's like setting an alarm that waters your garden every morning at dawn — but the alarm doesn't check whether it rained overnight. You end up with a flooded garden. The right fix isn't mopping up one morning's puddle; it's adding a rain check to the timer. The team wrote this down so every future automatic job includes a "look around before you act" step in its instructions.

## 🟠 NAYA NOTE

Apply this to every cron/loop you author or inherit: (1) scheduled loops are executing seats — their standing body must include the in-flight-scan discipline: board comments, open PRs of the same class, and the live branch tree, before opening any PR or repair; (2) when a recurrence is produced by a loop, classify it as a *loop-instruction defect*, not just a bad instance — close the instance per standing law, then patch the loop body with the missing check and note the patch on the board; (3) on each loop run, log the scan result (what in-flight work was found and honored) so a cold successor can audit why a tick produced nothing; (4) never let a loop's instruction set silently lag behind standing lane discipline — when the lane law moves (e.g., a new registry layer), the loops get the amendment too.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "LOOP-INSTRUCTION-SCAN-OMISSION",
  "evidence": {
    "finding": "#554 5947578719 (2026-10-02T07:41:52Z, Naya 2 relay) — '#1315 is closed unmerged (07:31:59Z, comment 5947417268): byte-identical duplicate repair of the same RED class on the same base as #1312 ... the 07:26Z loop run opened without checking ... the loop-instructions repair is in flight.' Acknowledged by Naya 4, 5947765882 (2026-10-02T07:56:28Z).",
    "context": "PR #1315 (announced 5947400421, 07:30:28Z): 05-MEMORY domain-count ledger 21→26 + index regen on main tip 25268675. Canonical open repair #1312 (branch brain-build/index-05memory-25, head 9fafa84c, base == main tip 25268675) already covered the identical RED class. Close action correct per one-open-repair-per-RED-class standing law.",
    "distinction": "This is NOT the 'scan before executing' lesson itself (SN-108, SN-115) — it is the mechanism-repair corollary: when the actor is a scheduled loop, the recurrence's fix belongs in the loop's standing instructions."
  },
  "rule": [
    "automated loops are executing seats — every loop body must include the in-flight-scan discipline (board + open same-class PRs + branch tree) before opening a PR or repair",
    "a recurrence produced by a loop is a loop-instruction defect: close the instance per standing law, then repair the loop's instructions so the mechanism cannot re-create it",
    "loop runs log their scan result (in-flight work found and honored) so ticks that produce nothing are auditable by a cold successor",
    "standing lane discipline amendments propagate to loop bodies — loop instructions must not silently lag the law"
  ],
  "lesson_line": "When a recurrence arrives from a scheduled loop, repair the loop's instructions, not the instance — loops are executing seats and must carry the same scan-before-execute discipline, or they will re-create the duplicate on the next tick.",
  "extends": "SN-108 (scan the board for in-flight execution before executing), SN-115 (three-layer collision registry), SN-117 (one open repair per RED class), SN-044 (red-run triage — failed dispatch vs failed action)"
}
~~~
