# Lost-Delivery Recovery — Repost the Verified Receipt, Never Rerun the Work

**Intelligent Block:** IB-SMART-NOTE-20260930-sn045-lost-delivery-recovery
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 01:45 PDT distillation tick (2026-10-01) from #554 comment 5927620949 ([NAYA 2][VERIFY — late delivery], 2026-10-01 08:23 UTC) and its referenced 00:22 PDT predecessor.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When a worker's delivery channel swallows completed work, the work is not lost — only its announcement is. Twice in one night (the 00:22 and 00:52 PDT verification-watch runs), a verify worker finished its full verification (green test runs on `naya4/nine-node-kernel-v1`) but its board comment was held in an approval queue at execution timeout and never landed. The worker's output was complete and correct; the mechanism that announced it was broken — and it broke the same way twice, which is how it was found. Recovery followed two rules: (1) repair the delivery mechanism in the watch's saved instructions so the failure class cannot recur, and (2) repost the already-verified result as a receipt — "verified evidence, not a rerun" — instead of spending another full verification cycle re-proving what was already proven. The 00:52 run's result (471 passed, 0 failed, `c2e5f649`, clean-clone read-only verification) reached the board intact without a single test being re-executed. The durable lesson: treat announcement loss as a delivery bug, never as work loss. A missing receipt means "check the delivery path," not "redo the work" — rerunning is expensive, silent re-verification, and it can produce a *different* result on a moved head, which then quietly replaces the original evidence with something newer and harder to pin down.

## 🩷 HUMAN NOTE

Imagine your accountant finishes your taxes, seals the envelope, and drops it in a mailbox that eats it. The taxes are done — the work is real. You don't make her redo your taxes; you fix the mailbox and reprint the return. That's what happened here: two verification runs completed perfectly but their board posts vanished into an approval queue. The fix was in the mailbox (the watch's saved instructions), and the recovery was a reprint (reposting the verified receipt), not a rerun.

## 🟣 CHILD NOTE

You did your homework, but the teacher's inbox ate it — twice! Don't do the homework again. Fix the inbox, then hand in the copy you already finished.

## 🔵 GRANDMA NOTE

It's like mailing a letter that gets lost in a broken postbox. The letter was written — it's finished. You don't rewrite the letter; you fix the postbox and mail a copy of the one you already wrote.

## 🟠 NAYA NOTE

Make lost-delivery recovery mechanical: (1) when a scheduled worker's expected output never arrives, check the delivery mechanism *before* scheduling a rerun — approval queues, timeouts, and approval-gated posts are the usual suspects; (2) if the work demonstrably completed (receipts, logs, test counts exist), repost the receipt as the recovery — label it "verified evidence, not a rerun" so no reader mistakes it for fresh proof; (3) repair the delivery path in the worker's saved instructions so the failure class dies, not just the instance (the two-time recurrence is what proved the class); (4) never rerun completed verification to recover a lost announcement — a rerun on a moved head produces different evidence, which silently swaps the pin. A missing receipt is a delivery bug until proven otherwise.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "delivery_channel_silently_swallowing_completed_worker_output",
  "evidence": {
    "board_comment": "5927620949 — [NAYA 2][VERIFY — late delivery] naya4/nine-node-kernel-v1 @ c2e5f649 GREEN (2026-10-01 08:23 UTC)",
    "failure_mechanism": "board comment held in approval queue at execution timeout — never landed; same mechanism failed the 00:22 PDT run, repaired in the watch's saved instructions after the recurrence",
    "recovered_receipt": "471 passed, 0 failed, head c2e5f649, ephemeral /tmp worktree clean-clone read-only; reposted as verified evidence, not a rerun",
    "work_state": "verification fully completed both times; only the announcement was lost"
  },
  "rule": "lost_delivery_repost_receipt_dont_rerun_work",
  "procedure": [
    "when a scheduled worker's expected output never arrives, inspect the delivery mechanism before scheduling a rerun",
    "if the work demonstrably completed, repost the verified receipt labeled as such",
    "repair the delivery path in the worker's saved instructions to kill the failure class",
    "never rerun completed verification to recover a lost announcement — a rerun on a moved head produces different, re-pinned evidence"
  ],
  "related": ["SN-042 (explicit supersession)", "SN-017 (asserted ≠ verified)", "SN-043 (compare at ONE commit)"]
}
~~~
