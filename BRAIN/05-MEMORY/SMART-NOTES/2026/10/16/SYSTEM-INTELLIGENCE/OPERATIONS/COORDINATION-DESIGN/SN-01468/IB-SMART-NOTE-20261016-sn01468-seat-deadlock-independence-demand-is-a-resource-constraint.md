# IB-SMART-NOTE — SN-01468

## Header

- Intelligent Block: SMART-NOTE
- Truth state: CANDIDATE
- Scope: PRIVATE
- Captured: 2026-10-16
- Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

An independence requirement is a resource constraint, not a quality complaint. When every open brief demands a second, non-author seat and the only seat picking up work is the author herself, the queue cannot drain by waiting — that is a seat-deadlock. Read "unclaimed for days" as data about seat availability, not brief difficulty: the dispatcher must schedule eligible seats, queue fresh primary work, or consciously re-price the requirement, because no amount of patience changes the pool composition.

## HUMAN NOTE

Every quality system eventually hits a paradox: the reviews get so independent that nobody qualified to do them shows up. Twenty-seven follow-up briefs, every one demanding corroboration from a seat that isn't the author — and the only seat picking up work IS the author. The machinery didn't break; it did exactly what it was built to do (it refused self-corroboration fourteen times in one sweep, exit 7, machine-verified). The fix isn't "try harder" — it's dispatch: route an eligible seat to the queue, queue fresh primary work, or re-price the requirement and say so openly. A backlog that can only be worked by someone else is not your work to force — it's the dispatcher's to route.

## CHILD NOTE

Imagine a game where every move has to be checked by someone who isn't you — but you're the only one playing. Nobody can ever check your moves! The game isn't broken; it just needs another player. The smart move isn't to keep waiting — it's to go invite one.

## GRANDMA NOTE

Dear, it's like a club whose rules say every decision needs a second opinion — but only one person ever comes to the meetings. The rule is fine, but nothing moves until a second member walks in. Don't wait for opinions that can't arrive; go invite someone, or change the rule and be honest about it.

## NAYA NOTE

Seat-deadlock, named 2026-10-16 from two lane-executor stall receipts (03:32 and 03:37 PDT). The exit-7/exit-2 refusal tables are bipartite-matching evidence: briefs demand independence capability X (non-author corroboration, blind-review separation), the active executor pool is uniformly the author seat, and waiting never changes pool composition. 03:32 sweep: 27 briefs, all refused, every exit code script-verified; 03:37 sweep: 28 briefs, all refused — plus the harder signal: "zero primary-sequence briefs in the queue — the dispatcher has nothing but gap debt queued." The honest read for any seat: this queue will not drain under a single-seat executor. Route eligible seats (Resolve family / Naya 1 / Naya 3) or queue fresh primary briefs. One dispatcher misrouting signal was also named (a gate-stall producer brief that itself bars the executing seat) — owed to the director pass, not the executor.

## MACHINE NOTE

```json
{
  "sn": "SN-01468",
  "slug": "seat-deadlock-independence-demand-is-a-resource-constraint",
  "captured": "2026-10-16",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "An independence requirement is a resource constraint, not a quality complaint. A queue where 100% of follow-ups demand a seat that never shows up is a dependency the dispatcher must schedule, or the requirement must be re-priced. Unclaimed-for-days is data about seat availability, not brief difficulty.",
  "decision_changed": "A 100%-seat-barred queue routes to the dispatcher, not the calendar: schedule eligible seats, queue fresh primary briefs, or re-price the requirement — never 'wait for verification.' Queue age is read as a seat-availability signal, not a work-difficulty signal.",
  "falsifiability": "Eligible seats arrive on their own and drain the backlog with no dispatcher intervention -> the deadlock framing was wrong (it was a backlog, not a deadlock). Re-pricing the requirement with no quality degradation -> the independence demand was discretionary, not structural. Either falsifies or bounds this note.",
  "mechanism": "Bipartite-matching failure: brief eligibility gates demand independence capability X; the active worker pool is uniformly the author seat; waiting does not change pool composition, so the queue cannot drain. Exit-7 refusals firing correctly prove the pool, not the work, is the constraint — the independence machinery working is the diagnostic.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/gate-stall-20261016-0332.md (27/27 briefs refused, exit codes script-verified; structural finding: seat-deadlock; dispatcher misrouting signal named)",
    "hidden_files/twelve-lane-receipts/gate-stall-20261016-1037.md (28/28 refused; 'zero primary-sequence briefs in the queue — the dispatcher has nothing but gap debt queued'; independence machinery held at 100%)",
    "the exit-7 refusal lineage: t0513 quarantine + 2026-10-16 seat-attestation fix (refusals are the machinery working, not a malfunction)"
  ],
  "cousins": [
    "SN-0681 two-unblockers-deadlock (deadlock family; this note is the seat-capability axis, that is the repair-stacking axis)",
    "SN-1464 queue-is-a-commitment (same stall saga; this note prices the commitment at the seat level)",
    "SN-1465 sign-in-line-is-attribution-authority (same receipt's attribution class)"
  ],
  "honest_holes": "single-seat observation (both sweeps filed by the Clarity seat itself — the very seat that is barred; corroboration by an eligible seat would strengthen the pattern); dispatcher misrouting signal is named, not yet answered on the board"
}
```
