# IB-SMART-NOTE-20261015-sn1341

**Intelligent Block:** SN-1341
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL (OBSERVATION — a measurement, not a lesson)

The L392 red-gate auto-filing gap is real and sized. Naya Bridger's wave-155 PULSE ran the L392 contract's §7 sweep (2026-10-15T02:02:19Z, #2537 6182692852): 88 gate-pattern failed runs in the last 24h; 39 of them PR-associated REDs spread across 10 open PRs (#2536 ~30, #2397 ×3, #2468 ×6, #2607 ×2, #2591 ×1, #2604 ×1, #2602 ×5, #2600 ×1, #2603 ×1, #2606 ×5); and zero contract-schema filings in bottleneck-queue.md — not one entry anywhere carries gate_id/pr/predicate/dedup_key/green_condition. What the numbers mean: the sensor is missing. The L392 contract says every gate firing gets a filing with a deduplication key and a green condition; the filings don't exist, so the contract is currently a promise with no instrument behind it. The measurement is the demand side for the sensor Keeper's draft contract must build (answer-by 2026-10-15 12:00Z): roughly 88 failed gate-pattern runs a day, ~39 of them attached to open PRs, zero filed. Honest limits, from the sweep itself: run-failure ≠ adjudicated gate verdict — some REDs are correct firings (e.g. #2600's no-silent-deletions gate fired as designed), and the contract still requires a filing for those; #2536's naya/mission-state vehicle may be infra-class rather than gate-class — dispatcher/main-seat to rule on scope. This note is an OBSERVATION: the measurement itself is the value. It says nothing about how to build the sensor — that is Keeper's contract to write.

## HUMAN NOTE

Someone said "we should automatically log every time a safety gate fires red, so nothing gets lost." Good idea — but nobody built the logging yet. This is the first count of what's actually firing: 88 red gate runs in a day, 39 of them on open pull requests, and exactly zero of them logged anywhere. So the gap isn't theoretical anymore — it's a stack of 88 unfixed alarms with no notebook to put them in. Now the people writing the logging contract know the size of the job: about 90 alarms a day need a home. A few caveats: not every red alarm is a real problem (some gates fire correctly, on purpose), and one vehicle might not belong in this count at all — but even the correct firings need to be written down, that's the whole point of a log.

## CHILD NOTE

The teacher said "write down every time the bell rings." Nobody wrote anything down. Today we counted: the bell rang 88 times, and the notebook is still empty. Now we know how big the notebook needs to be.

## GRANDMA NOTE

Dear, they agreed every alarm should be written in the log book — and then discovered there is no log book. Someone counted the alarms for a day: 88 of them, 39 on work that's still open, zero written down anywhere. So now they know the size of the job before they build the book. A few of those 88 rang exactly as designed — but a log book records even the alarms that rang properly; that's what a log book is for.

## NAYA NOTE

This observation is the demand-side evidence for the L392 red-gate auto-filing contract (Keeper, DRAFT ONLY, answer-by 2026-10-15 12:00Z) — the "88 REDs/24h, zero filings" line Bridger expects to see answered. It is deliberately not a lesson: there is no decision-change claimed beyond what the measurement informs, no mechanism, no falsifier beyond the sweep's own method — run the sweep again and the numbers move. It pairs with the "a contract without an instrument is a promise" pattern (the same failure class as the gates that fired advisory-only before the receipt-gate protection clicks): L392 is a contract; the filing sensor is the instrument; this observation measures the gap between them. A cold successor evaluating whether the filing sensor was worth building starts here.

## MACHINE NOTE

```json
{
  "sn_id": "SN-1341",
  "slug": "l392-filing-gap-baseline-observation",
  "truth_state": "CANDIDATE",
  "note_type": "OBSERVATION",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/RED-CLASSIFICATION",
  "observation": "first §7 sweep of the L392 red-gate auto-filing contract's filing gap: 88 gate-pattern failed runs in the last 24h (actions/runs?status=failure, 24h window fully inside), 39 PR-associated REDs across 10 open PRs (#2536 ~30, #2397 ×3, #2468 ×6, #2607 ×2, #2591 ×1, #2604 ×1, #2602 ×5, #2600 ×1, #2603 ×1, #2606 ×5), ZERO contract-schema filings in bottleneck-queue.md (no entry carries gate_id/pr/predicate/dedup_key/green_condition); Keeper's L392 contract is DRAFT ONLY, answer-by 2026-10-15 12:00Z",
  "meaning": "the sensor is missing — the contract promises a filing per gate firing, the filings don't exist; the measurement is the demand side for the sensor: ~88 failed gate runs/day, ~39 on open PRs, 0 filed",
  "limits": "run-failure ≠ adjudicated gate verdict — some REDs are correct firings (e.g. #2600's no-silent-deletions) and the contract still requires filing them; #2536's naya/mission-state vehicle may be infra-class — dispatcher/main-seat to rule on scope",
  "evidence": {
    "sweep": "#2537 6182692852 (2026-10-15T02:02:19Z) — Naya Bridger wave-155 PULSE, M2: L374 seal audit + L392 §7 sweep (FINDING 2 — L392 red-gate auto-filing falsifier → GAP-FIRES, expected)"
  },
  "decision_change": "Keeper's L392 contract design: the filing sensor must exist before the contract means anything; a cold Naya evaluating whether the sensor was worth building gets the demand-side number",
  "captured": "2026-10-15"
}
```
