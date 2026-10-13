# The Pin Dies When the Head Moves — Re-Pin the Receipt in the Same Motion as the Push

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1076-the-pin-dies-when-the-head-moves
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** NEXT-NAYA-HANDOFF-20261012.md, LESSONS FROM TONIGHT #2 (Naya 4): "The pin must match the head. When you update a PR branch, the receipt pin in the body must be updated too. The gate catches this — that's its job."; #2175 comment 6123008914 (Lane 9 Naya Smith t0212 sign-in, 2026-10-12T11:05:34Z): "Task: re-pin #2399 receipt-pin at action-time head"; twelve-lane-feed t952 (Lane 9) fail-closed demos: no receipt → FAIL, stale pin → FAIL, exact head → PASS; t992 (#2399): pin block added to the body matching head `4776be062822c09c9a346acb1c33c6e0705ec03a` byte-exact.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The receipt gate compares the pin in the PR body against the branch head — two independent facts. The moment you push a new head, the pin in the body refers to a dead SHA, and the gate fails closed on the stale pin: no receipt → FAIL, stale pin → FAIL, exact head → PASS (Lane 9's t952 fail-closed demos, proven locally with the exact workflow commands). The gate reads bytes, not intentions — it does not know you "meant" the new head.

The durable rule: **every push to a PR branch is incomplete until the pin is re-pinned.** Update the receipt pin in the PR body in the same motion as the push — new head SHA, same action — or make the body edit with the new pin immediately after, before any check runs. Lane 9 lived this twice in one night: t992 added the pin block to #2399's body matching the head byte-exact (4776be0628…), and t0212's sign-in task was literally "re-pin #2399 receipt-pin at action-time head." "Pushed code, pin not updated" is not a finished push — it is a red waiting to happen.

This is the mirror of SN-1037 (a body patch never moves the head — pins survive): the reverse is also true and far more common — a code push always moves the head, and pins never survive it. SN-0200's pin discipline (publish only resolvable pins) applies at publish time; this note covers every publish after the first: heads move, pins die, re-pin.

## 🩷 HUMAN NOTE

Shawn — small mechanical rule from the night shift that will save real reds. The merge gate checks the PR body's pinned commit against the branch's actual head. Push a new head and the pin in the body is instantly stale — the gate fails the check, not because the code is wrong but because the paperwork points at yesterday's code. The fix is a habit: every time you push to a PR branch, update the pin in the body in the same motion. Lane 9 ran into this twice last night and turned it into a discipline — "re-pin at action-time head" is now an explicit task line. Cheap to do, expensive to forget.

## 🟣 CHILD NOTE

Imagine your library card has the address of your old house on it. You move to a new house, but you don't update the card. The librarian checks the card, goes to the old address, finds an empty house — and says the card is wrong. Your new house is fine; the card is stale. The fix: every time you move, update the card in the same trip. Same with code: every time the branch gets a new head, the pin in the paperwork must be updated too, or the checker reads the old address and fails.

## 🔵 GRANDMA NOTE

It's like the seal on a jam jar: the date stamped on the lid has to match the batch inside. Make a new batch and pour it into the jar, but leave the old date on the lid — the inspector fails the jar, not because the jam is bad but because the label lies about what's in it. The rule the team banked last night: re-date the lid every time you refill the jar. One motion, not two.

## 🟠 NAYA NOTE

Note to future me: make re-pinning part of the push motion, not a follow-up. (1) After every `git push` to a PR branch, before anything else, edit the PR body: replace the receipt pin with the new head SHA (byte-exact, verified via ls-remote — SN-0200). (2) Never assume a check will "pick up" the new head — receipt-gate.yml's rung 1 compares the body's pin to the head; a stale pin is a designed FAIL, not a bug (t952 fail-closed demos). (3) If someone else pushed the branch (Lane 3 actively pushing on #2418), re-pin at YOUR action time too — the t0212 "re-pin at action-time head" task exists for exactly this case. (4) Cheap-check: compare the body's pin against `git ls-remote` head before declaring anything merge-ready. Related cousins: SN-0200 (publish only resolvable pins), SN-1037 (body is a third input channel — body patches preserve the head), SN-0878 (base-branch fixes don't retrigger PR checks).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1076",
  "title": "The Pin Dies When the Head Moves — Re-Pin the Receipt in the Same Motion as the Push",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-12",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "EVIDENCE-IDENTITY"],
  "extends": ["SN-0200"],
  "related": [
    "SN-0200 (a receipt pin must resolve live — this note covers every publish after the first)",
    "SN-1037 (body is a third input channel — the mirror: body patches preserve the head; code pushes never do)",
    "SN-0878 (base-branch gate fixes don't re-run PR checks — same fail-closed family)"
  ],
  "evidence": {
    "handoff_lesson": "NEXT-NAYA-HANDOFF-20261012.md LESSONS FROM TONIGHT #2: 'The pin must match the head. When you update a PR branch, the receipt pin in the body must be updated too. The gate catches this — that's its job.'",
    "live_application": "#2175 comment 6123008914 (Lane 9 Naya Smith t0212 sign-in, 2026-10-12T11:05:34Z): 'Task: re-pin #2399 receipt-pin at action-time head'",
    "fail_closed_demos": "twelve-lane-feed t952 (Lane 9): no receipt → FAIL, stale pin → FAIL, exact head → PASS, proven with exact workflow commands locally on branch naya/nine-receipt-gate-t902 @ 1184d509",
    "byte_exact_pin": "t992 (#2399): pin block added to PR body matching head 4776be062822c09c9a346acb1c33c6e0705ec03a byte-exact (ls-remote pin)"
  },
  "rule": "re-pin the receipt in the PR body in the same motion as every branch push; 'pushed code, pin not updated' is an incomplete push; the gate reads bytes, not intent"
}
```
