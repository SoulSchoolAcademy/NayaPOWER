# When the Runtime Kills Delegation, Execute Directly

**Intelligent Block:** IB-SMART-NOTE-20261004-sn0326-delegation-timeout-direct-execution
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 5988488663 (2026-10-05T05:09:22Z / 2026-10-04 22:09 PDT — Naya 2's #1438 merge receipt: "Honest note: the rebase took my own hands after three specialist attempts died on runtime inference timeouts. The runtime is hostile to delegated work tonight — direct execution is the reliable path until it stabilizes."); context in comment 5988473463 (rebase executed by direct hand: fresh clone, byte-identical page carry-forward, index regen, single commit `2c010ee8fade`, full test suite green).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Delegation has a hostility detector, and Naya 2 calibrated it this run: three specialist attempts to perform the #1438 rebase died on runtime inference timeouts, so she stopped delegating and did the rebase with her own hands — fresh clone at live main tip, byte-identical carry-forward, index regenerated, single commit, 646 tests green, merged. The lesson is the pattern, not the incident: **when delegated work keeps dying on the same failure mode, the correct move is not a fourth attempt — it is to drop to direct execution.** Retrying a hostile substrate is the delegation equivalent of arguing with a frozen system; each retry burns wall-clock and produces nothing but a new timeout receipt.

The rule for a cold Naya: count the consecutive failures. One timeout is noise — retry once. Two is signal — change something (smaller scope, different lane, wait). Three identical failures is the threshold: stop delegating that task tonight, execute it yourself with your own tools, and log the runtime hostility on the board so other seats don't repeat the pattern. Naya 2 did exactly this — she named the hostility in her merge receipt, which is why every seat now knows tonight is a direct-execution night without each of them paying three timeouts to learn it. The log IS the value; without it, the lesson dies with the session.

This also refines the "direct is reliable" instinct: direct execution wasn't braver here, it was cheaper — the rebase she performed by hand took less total time than the three dead specialist attempts combined. In degraded runtime, the default assumption ("delegation is cheaper") inverts, and the seat that notices the inversion fastest wins the night.

## 🩷 HUMAN NOTE

Shawn — small but real lesson from tonight's board traffic: Naya 2 lost three specialist runs to runtime inference timeouts trying to rebase #1438, then did the whole thing herself by hand and merged it clean. The takeaway we're banking: three identical delegation failures is the signal to stop delegating and do it directly — and to say so on the board, so no other seat pays the same tuition. In a degraded night, direct execution isn't braver, it's just cheaper. Worth remembering next time the runtime gets flaky.

## 🟣 CHILD NOTE

Imagine asking a friend to do a puzzle for you, and every time they try, their hands are too cold and they drop the pieces — three times in a row! You wouldn't ask a fourth time. You'd pick up the pieces and do it yourself. That's the rule: if you hand someone a job and it fails the same way three times, stop handing it out — do it yourself, and tell everyone else what happened so they don't waste their turns too.

## 👵 GRANDMA NOTE

When things are going wrong, sometimes you just have to do it yourself. One of our builders tried three times to get help from her tools, and each time the tools froze up. So she rolled up her sleeves and did the work with her own hands — and it went beautifully. The lesson she's left for the rest of us: after three tries that fail the same way, don't try a fourth — do it yourself, and write down what happened so nobody else trips over the same step.

## 🤖 NAYA NOTE

For future seats, the escalation ladder when delegated work fails on runtime inference timeouts: 1 failure → retry once (noise). 2 failures → change the shape (smaller scope, different lane, wait and retry). 3 identical failures → STOP delegating this task this session; execute directly with your own tools; post the hostility observation on #1354 so the pattern is shared, not re-discovered. Note the inversion: in degraded runtime, direct execution is usually cheaper than delegation, not just more reliable — measure it that way when deciding. Do not keep a failure invisible; an un-logged workaround is a lesson that never compounds.

## ⚙️ MACHINE NOTE

```json
{
  "sn_number": "SN-0326",
  "slug": "delegation-timeout-direct-execution",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-04",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "evidence": [
    "#1354 comment 5988488663 (2026-10-05T05:09:22Z) — 'the rebase took my own hands after three specialist attempts died on runtime inference timeouts. The runtime is hostile to delegated work tonight — direct execution is the reliable path until it stabilizes'",
    "#1354 comment 5988473463 (2026-10-05T05:07:37Z) — direct-execution rebase receipt: fresh clone at 580bfdddae71, byte-identical carry-forward (blob 096d965a), index regen --check OK, commit 2c010ee8fade, 646 passed / 0 failed"
  ],
  "taxonomy": "BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/OPERATIONS/DELEGATION-FALLBACK/SN-0326",
  "law": "Three identical delegation failures (e.g., runtime inference timeouts) is the stop-delegating threshold: execute directly and log the hostility on the board so the pattern compounds across seats.",
  "ratification_status": "CANDIDATE — lane-observed tonight (2026-10-04); not ratified by Shawn; auto-capture is not auto-ratify.",
  "cousins": ["Evidence Law", "relayed-session-alive protocol", "delegation guidance in goal guide (bounded work with exact context)"],
  "keywords": ["delegation", "runtime inference timeout", "direct execution", "escalation ladder", "degraded runtime", "operations"]
}
```
