# A "Not Yet" Gap Is a State Claim — Re-read the World Object Before Acting

**Intelligent Block:** IB-SMART-NOTE-20261016-sn1495-not-yet-gap-staleness-reread
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 13:08 PDT distillation tick (2026-10-16) from `hidden_files/twelve-lane-receipts/gap-1432-lane2.md` (filed 2026-10-16 20:01 UTC; Naya Clarity Narzan, Lane 2 Sage hat): the gap was filed as a timing residual — "CI unobserved" / run-not-yet-rerun on PR #2458 (`learn(compound-scale): pin Truth-gate receipts to repo fixtures, not seat-local paths`, branch `naya/two-compoundscale-fixture-t1432` @ `ac270833fb3a52c6be45acc730b0e5132353d5a5`). The live read (gh-api, read-only, 2026-10-16 ~20:00 UTC) showed PR #2458 **state: closed, merged: false** — the world had moved between filing and execution. The 15 check-runs on the head SHA (all completed 2026-10-12T07:11–07:12Z): 11 success / 3 failure / 1 skipped, with the `test` leg dying in the mjs step before the pytest leg — CI never exercised the compound_scale fix itself. The e2e re-run still closed the brief (11/11 lessons PROVEN, 3/3 adversarial REJECTED, 14/14 pre-registration matches, sealed_sha256 `250185b803…` MATCH), but the parent's expected merge sequence died with the closed PR — a state change, not a delay.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A gap filed as "not yet" (CI pending, run not re-run, approval awaited) is a snapshot of the world at filing time, not a promise about the world at execution time. The t1432 gap read "CI not yet observed" — the live read showed the PR closed unmerged, and its check-runs showed CI had never even exercised the code in question (the test leg died in the mjs step first). The standing discipline: for any gap whose filing says "pending" or "not yet," the first action is a live re-read of the named world object (PR state, check conclusions, branch existence) BEFORE any execution. The re-read is the cheapest byte in the run — it costs one API call and distinguishes "still pending" (genuine timing) from "the world moved" (the plan is stale). Executing on a stale plan doesn't just waste the run; it produces conclusions (like the parent's merge-sequence next action) that are already dead.

## 🩷 HUMAN NOTE

Imagine getting a note that says "the plumber hasn't arrived yet — check the pipes when he does." You arrive and spend an hour testing pipes, only to learn the plumber canceled yesterday and nobody is coming. The note wasn't wrong when written; it was a snapshot, and the world moved. That's what happened with the compound-scale gap: the filing said "CI hasn't been observed yet," but by the time someone acted, the PR was dead — closed, unmerged — and CI had never actually tested the fix. The new rule: whenever a task says "not yet" or "pending," check the current state of the thing it's waiting on BEFORE doing any work. One look at the live page is cheap; an hour of work on a dead plan is not.

## 🟣 CHILD NOTE

Imagine your friend writes you a note: "The ice cream truck hasn't come yet — listen for the music!" You wait and listen for an hour, but what you didn't know is the truck broke down that morning and isn't coming at all. The note was true when your friend wrote it, but old by the time you read it. The new rule: when a note says "not yet," first peek outside to check what's actually happening now. One peek is fast and free; waiting for a truck that's never coming wastes the whole afternoon.

## 🔵 GRANDMA NOTE

It's like getting a letter that says "the plumber will be there Tuesday" and showing up Tuesday with the tools, only to learn the job was canceled Monday. The letter was honest when it was mailed. The lesson: when instructions say "not yet," make a quick phone call to check the current situation before you drive over. A two-minute call is cheap; a wasted trip is not. Cold, hard truth: paper ages, the world doesn't wait.

## 🟠 NAYA NOTE

Cold successor: when you pick up ANY gap brief (or stale handoff) whose filing says "pending," "not yet," "unobserved," or "awaited," make the live state re-read your first action — before running anything, before reproducing anything, before trusting the brief's next action. Re-read the named world object: PR state/merged flags, check-run conclusions (not just "ran" — what they CONCLUDED and whether they exercised YOUR code), branch existence, file presence. Then classify: (a) still pending → it was genuinely timing, proceed with the plan; (b) world moved → the brief's next action may be dead — supersede it explicitly (as gap-1432 did: "the parent's merge-sequence next action is superseded by the closed PR") and route the NEW state to the right seat. Never inherit a dead next action silently. Cousin family: the stall-is-a-snapshot lesson (t0571 — a stall verdict must carry its queue-snapshot time; anything filed after it is outside the verdict) — both are "time decouples the filed claim from the world." Machine note for the executor: the re-read order is PR-state → check-conclusions → branch/tree, cheapest-first.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "not_yet_gap_staleness",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-1432-lane2.md (2026-10-16 19:55–20:05 UTC, Lane 2 Sage hat, Naya Clarity Narzan)",
    "gap_filing": "t1432 gap filed as timing residual: (a) CI unobserved, (b) run_scale.py e2e not re-run — against PR #2458, branch naya/two-compoundscale-fixture-t1432 @ ac270833fb3a52c6be45acc730b0e5132353d5a5",
    "live_reread": "PR #2458: state closed, merged false (gh-api GET, live, read-only, 2026-10-16 ~20:00 UTC); 15 check-runs on head SHA, all completed 2026-10-12T07:11–07:12Z: 11 success / 3 failure / 1 skipped; `test` leg dies in mjs step before pytest — CI never exercised the compound_scale fix",
    "superseded_plan": "parent receipt's expected merge sequence (Lane 8/9/10 fixes -> merge) died with the closed PR; receipt explicitly superseded the next action and routed the dead branch (naya/two-compoundscale-fixture-t1432) to the merge-seat/dispatcher decision",
    "e2e_still_valid": "run_scale.py exit 0: 11/11 lessons PROVEN, 3/3 adversarial REJECTED, 14/14 pre-registration matches; sealed_sha256 250185b803… MATCH; pytest 66/66"
  },
  "cousins": ["t0571 stall-is-a-snapshot lesson (a stall verdict must carry its queue-snapshot time; anything filed after it is outside the verdict)", "SN-0889 (re-anchor at verify time — stale state expires under tip velocity; different domain, same staleness class)"],
  "decision_change": "every gap brief (or stale handoff) filed as 'pending/not yet/unobserved' opens with a live re-read of the named world object (PR state, check conclusions, branch existence) before any execution; if the world moved, the inherited next action is explicitly superseded and the new state routed to the right seat — never executed as-if-alive",
  "falsifiability": "if the live re-read shows the world unchanged (PR still open, CI still genuinely pending, branch alive), the filing was correct as filed and the re-read was merely cheap insurance — the lesson's operational claim is falsified in that instance; repeated genuine-pending outcomes would demote this from standing discipline to optional hygiene",
  "mechanism": "filings snapshot state at filing time; execution happens later; the world moves between filing and execution. A 'pending' filing decays into either still-pending or changed, and only a live re-read discriminates between them. State reads cost orders of magnitude less than execution-on-stale-assumptions — so the re-read goes first, and a dead next action is never inherited silently."
}
~~~

