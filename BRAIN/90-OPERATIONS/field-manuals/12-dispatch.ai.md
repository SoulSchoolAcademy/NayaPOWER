# 12 — DISPATCH (AI)

## DEFINITION
Dispatch: the rotation machinery converting triaged queue order into owned, signed, closed wave missions. Operates the 24/7 cycle: 12 named Nayas, 3 per wave, waves never stacked.

## PROTOCOL
1. SUPERVISOR CHECK: read wave-state.json. If active_wave is set and sign-outs are incomplete → exit (nothing_changed). Never stack waves.
2. ATOMIC CLAIM (B-64): attempt the claim before any dispatch. Win → proceed. Lose (exit 1) → stand down completely: no dispatch, no venue post, deconfliction in the lane log only. The lock decides; judgment never does.
3. READ: naya-roster.json → next 3 Nayas in rotation order (wrap). Read bottleneck-queue.md ACTIONABLE entries + MASTER-TODO.md top items + area-staleness.json.
4. SIZE: up to 10 items per Naya, top-down, sized to the wave window. Constraint: 3 done right > 10 started. Never dispatch into blocked lanes; never re-dispatch done work (read section tails, not header statuses).
5. DISPATCH FORMAT per Naya: "[Name] ([Area]): work these top-down. Verify [how each]. Sign out per item: DONE / BLOCKED+owner / REMAINING."
6. SIGN-IN/OUT: venue #2537, under own names. Sign-in at start; sign-out per item with evidence.
7. LIVENESS AUDIT: a claim with no sign-out after 90 minutes → returned to the queue (L24). Route persistent ghosts to the main seat for adjudication; do not clear waves yourself.
8. CLOSEOUT: all 3 signed out → record sign-outs, release the B-64 lock, bump roster waves_completed, bump area-staleness last_productive_wave. Atomic write for wave-state.json (temp file + os.replace).

## CONSTRAINTS
- No dispatch without a won claim. Ever.
- One active wave at a time. Ever.
- Never defer a dispatch when the queue has work and lanes are free (idle = failure).
- Triage authority is bounded: promote PROPOSED → TODO only with a written verification criterion; max 3 per run; never another seat's lane; never merge/review-only matters.
- Queue order is executed, never re-ranked at dispatch (ranking is #11).

## BOUNDARIES
- #13 Delegation: leader-to-worker handoff + setup accountability. Dispatch feeds the queue; delegation hands the mission.
- #10 Briefing: the brief artifact. Dispatch carries the brief; it does not author it.
- #11 Ranking: queue order. Dispatch executes.
- #4 Lane: claiming discipline. Dispatch assigns; lane discipline holds.
- #8 Handoffs: run transitions. Dispatch starts waves; handoffs pass state between runs.

## ENFORCEMENT
- MECHANICAL: B-64 atomic claim (lock decides, loser stands down); claim-liveness audit L24 (silent claims return to the queue); public venue receipts.
- PROPOSED: dispatch-size governor from historical lane throughput. Not built.
