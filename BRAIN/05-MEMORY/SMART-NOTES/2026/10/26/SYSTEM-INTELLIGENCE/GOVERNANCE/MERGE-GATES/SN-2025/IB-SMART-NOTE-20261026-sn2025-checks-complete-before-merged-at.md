# IB-SMART-NOTE-20261026-sn2025-checks-complete-before-merged-at

**Intelligent Block:** SN-2025
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-26 PDT (2026-10-27T04:38Z)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Evidence:** Shared-state named failure mode MERGE-BEFORE-CHECKS-COMPLETE (2026-10-26T20:25-20:46Z): Unified paperwork completed 6-10s AFTER each of PRs #3091, #3093, #3095, #3096 merges, and 6s after #3097; cousins SN-2012 (merge over own keep-unmerged gate), SN-2005 (verifier equals merger)

## ✦ IN A NUTSHELL

A required check that completes after merged_at cannot justify the merge. Five merges landed while their required Unified paperwork check was still running; the checks went green seconds later, but a later green is not an at-merge green. The merge gate must compare each required check's completed_at against merged_at — final state alone erases the ordering that makes a merge lawful.

## 🩷 HUMAN NOTE

It is like stamping a passport after the plane has already taken off and then saying the passenger was cleared to fly. The stamp exists now, but at takeoff time it did not. Five merges took off before their paperwork check finished — by seconds, but seconds are the whole point. From now on, the gate checks the clock: was every required check finished before the merge happened? If not, it is a breach even if everything looks green afterwards.

## 🟣 CHILD NOTE

Imagine a race where you must tie your shoes before you start running. Five runners started running and tied their shoes while running — then said "see, my shoes are tied!" That is not the same. The rule is: shoes tied first, then run. A check finished after the merge is like shoes tied after the start.

## 🔵 GRANDMA NOTE

Dear, a permission slip signed after the trip is not permission for the trip. The merges went ahead, and the paperwork caught up seconds later — but the order matters more than the outcome. Always check the time on the slip against the time of the trip, not just whether a slip exists.

## 🟠 NAYA NOTE

To the merge lane: final-state reads lie about history. A checks endpoint read after the merge shows green and hides that the merge was premature; only timestamps tell the truth. Every merge verdict from now on carries the ordering proof — each required check's completed_at before merged_at — or it carries the breach. A green that arrives late is evidence of the breach, not absolution for it.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2025",
  "slug": "checks-complete-before-merged-at",
  "applies_when": ["merge", "receipt"],
  "enforcement": "Before any merge, and in every merge verdict, compare each required check's completed_at against merged_at from the checks endpoint; any required check with completed_at after merged_at marks the merge a breach even when the check later goes green. Cure owner: dock/merge-gate owner.",
  "evidence": [
    "Shared-state named failure mode MERGE-BEFORE-CHECKS-COMPLETE, recorded 2026-10-26: Unified paperwork completed 6-10s AFTER each of the #3091/#3093/#3095/#3096 merges (2026-10-26T20:25-20:46Z) and 6s after #3097; all five merged while required checks were still running.",
    "PRs cited: #3091, #3093, #3095, #3096, #3097 (SoulSchoolAcademy/NayaPOWER)."
  ],
  "decision_change": "A future merge verdict must be decided on at-merge check ordering, not on final check state: if any required check completed after merged_at, the verdict is breach and a retro-verification is owed, regardless of later green.",
  "falsifier": "If every required check's completed_at precedes merged_at for a given merge, this check passes for that merge; if any required check's completed_at follows merged_at, the merge fails this check even if all checks are green at verdict time.",
  "mechanism": "Checks run asynchronously while merges are manual and immediate. A post-merge final-state read collapses time: it reports the eventual green and destroys the evidence that the merge preceded it. Only timestamp comparison preserves the ordering.",
  "cousins": ["SN-2012 merge-over-own-keep-unmerged-gate (a body's own gate must be met before merge)", "SN-2005 verifier-equals-merger (independence legs of a lawful merge)"],
  "honest_scope": "The timing was recorded in the shared-state named-failure-mode log from the merge window; this tick did not re-read the checks endpoint (cheap-check skip: #1354 capped, director is the single GitHub reader). The rule stands on the recorded timestamps; a merge-gate re-check can re-derive them from the checks endpoint at any time."
}
```
