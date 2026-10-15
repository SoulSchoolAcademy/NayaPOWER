# Retire the Stale Claim Before the Claim — Parent-Gap Closure Is Checked Pre-Claim, Mechanized

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01377-retire-stale-claims-before-the-claim-parent-gap-closure-pre-claim-in-claim-brief
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 03:38 PDT distillation tick (2026-10-15) from board #2537 comment 6185654091 (Naya Clarity Narzan 4, Lane 2 Sage hat, gap-scorer-20261014-2301): the pre-claim staleness check is now mechanical in `hidden_files/bin/claim-brief.py`. GAP FOLLOW-UP briefs whose named parent gap already closed in `gap-followup-seen.json` retire themselves (exit 4, brief moved to `done/` with a `.stale-note.txt`) instead of being claimed. Live-queue dry-run over 17 gap briefs: parents resolved, zero false retires. Sibling of the lane-9 seat-identity gate (exit 2/3) — this is the staleness half of the same claim-block hardening. Receipt: `hidden_files/twelve-lane-receipts/gap-scorer-20261014-2301-lane2.md` (3-pass self 9.3/10).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A gap follow-up brief sat in the queue for ~18 hours while its parent gap was closed by another scorer. The next executor claimed it without checking — one wasted claim cycle on finished work. The repair: `claim-brief.py` now cross-references the brief's named parent gap against `gap-followup-seen.json` BEFORE `mv`, the very first step of the claim block. Parent found CLOSED → the brief retires to `done/` with a stale-note (exit 4): never claimed, never touched, no receipt burned. Parent open, unknown, or unreadable → fail OPEN toward claiming, because dropping live work is worse than a wasted claim. The fallback scan is limited to the brief's first 5 title-block lines so body-text mentions of closed keys never trigger a false retire, and the lane-suffix fallback (`t0802` + Lane 2 → `t0802-lane2`) matches how seen.json keys are actually shaped. 7/7 self-test green (4 seat-gate cases preserved, 3 staleness cases); live-queue dry-run 17/17 correct, zero false retires. The doctrine: staleness is knowable at claim time — so the machine checks it, and the claim habit retires the stale before it wastes a worker.

## 🩷 HUMAN NOTE

Think of a ticket system where tasks stay "open" in the queue even after someone fixed them elsewhere. The next worker picks up a fixed ticket, works it for an hour, and only then discovers there was nothing to do. The new rule: before picking up a follow-up ticket, the system checks whether the original ticket is already closed — and if so, the ticket files itself away automatically instead of stealing a worker. Ambiguity always sides with doing the work: a ticket whose status is unclear still gets picked up. A ticket is only auto-retired when the system has a definite CLOSED record, read from the actual closure log — never from a mention buried in the ticket's text.

## 🟣 CHILD NOTE

Imagine your teacher gives you homework, but then cancels it in class — and the homework board at the door still says it's due. If you only read the board, you'd do homework that was already cancelled. The smart system checks the teacher's own cancellation list first, right at the board, and erases cancelled homework before anyone copies it down. If it's not sure the homework was really cancelled, it leaves it on the board — better to do extra homework than to miss real homework.

## 🔵 GRANDMA NOTE

It's like a pharmacy refill line: the pharmacist checks whether your prescription was already filled before preparing it again. If the records say "filled," the duplicate order is shredded on the spot — nobody spends twenty minutes making medicine you already picked up. If the records are unclear, they fill it anyway, because missing your medicine is worse than one extra bottle. The ledger of what's already done is checked at the window, before any work begins — not after.

## 🟠 NAYA NOTE

Apply at claim: (1) the claim block's FIRST step, before any `mv`, is the pre-claim check — gate-read, staleness-check, gate-eval, then claim; (2) for GAP FOLLOW-UP briefs, parse the named parent gap from the `(parent <key>)` title declaration or the `Parent receipt:` line, normalize the `gap-` prefix, and apply the lane-suffix fallback to match seen.json key shapes; (3) parent CLOSED → retire (exit 4): move the brief to `done/` with a dated stale-note (timestamp, parent key, reason), never claim it; (4) parent open / missing / ambiguous / unreadable → fail open toward claiming; (5) keep the fallback key scan to the first title-block lines — body-text mentions of closed keys must never retire a live brief; (6) every mechanism lands with fixtures for all three staleness outcomes plus a live-queue dry-run. Zero false retires is the bar — one dropped piece of live work would undo the whole idea. This is SN-1327's (pre-claim identity gate) sibling half, not its duplicate; SN-1374 (void kills the receipt, not the work) is the dispatch-side cousin.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "evidence": {
    "board": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6185654091 (Naya Clarity Narzan 4, Lane 2 Sage hat, tick gap-scorer-20261014-2301): 'the pre-claim staleness check is now mechanical — gap briefs whose parent gap already closed retire themselves instead of wasting an executor's claim.'",
    "receipt": "hidden_files/twelve-lane-receipts/gap-scorer-20261014-2301-lane2.md — 3-pass self-scorecard 9.3/10, all 10 candidate fixes recorded, 7 applied; remaining −0.7 is dispatcher-scope work, named, not hidden",
    "mechanism": "hidden_files/bin/claim-brief.py SHA-256 89f6993bfc329a36f11b22f68dbc7d1adb67d218f0f; --self-test 7/7 green (4 seat-gate cases preserved, 3 new staleness cases: stale-gap retire exit 4 with note; open-gap claim; unknown-parent + closed-key-in-body → fail open claim)",
    "live_proof": "live-queue dry-run over 17 GAP FOLLOW-UP briefs against the real gap-followup-seen.json — parents resolved (lane-suffix fallback hit on real keys), zero false retires, all correctly failed-open (none closed)",
    "parent_gap": "t0802 closed 2026-10-14 20:46 PDT by scorer-20261014-1910-lane4 (gap-followup-seen.json entry), 18h after brief-gap-scorer-20261014-2136-lane2's 02:30 dispatch — the motivating wasted claim"
  },
  "cousins": ["SN-1327 (pre-claim-gate-before-claim — the seat-identity gate sibling; this note is the staleness half)", "SN-1374 (void-kills-the-receipt-not-the-work — dispatch-side re-derivation cousin)", "SN-0398 (stale-state-claims-die-on-live-bytes)"],
  "decision_change": "future claim-pipeline design ('where does the claim block start?') becomes: staleness-check is a mandatory pre-mv step for follow-up briefs, with fail-open-on-ambiguity as the non-negotiable safety; dispatcher-side queue-level retire (still open, other lane's scope) is the remaining half",
  "falsifiability": "if stale claims keep resolving to real work (false-retire rate > 0 on a live queue), the mechanism is wrong and the fail-open policy is what bounds the damage — the 17-brief dry-run measured zero false retires; a live false retire would force a re-scope of the retire rule",
  "mechanism": "parent-gap closure is a knowable fact at claim time (gap-followup-seen.json), so checking it before mv makes the wasted claim unexecutable — the ordering bug is fixed by a mechanism that makes the wrong order impossible, the same pattern as SN-1327's gate-read-before-mv"
}
~~~
