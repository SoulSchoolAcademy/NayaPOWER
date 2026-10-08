# The Comprehension Assertion Is the Proof's Live Boundary

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0174-comprehension-assertion-live-boundary
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5946437843 (overnight verification sweep, 2026-10-02T06:00:27Z — first main run of **Live Intelligence Commit Proof**, run 36966438981 on `b7e0eeae44`: job `cold-successor-held-out` (110711219423) failed at "Cold retrieve this run's exact Smart Note from machine registry and canonical runtime" with `AssertionError` at `assert comprehension["understands_raw_source_separate"]` (exit 1); `fresh-lesson` and `independent-verification` jobs **passed**. Also recorded: the projector step pushed commit `252686756e` to main from inside CI — by-design behavior, recorded, not an incident; runtime-proof `causal-learning-experiment-receipt` artifact never produced (experiment job skipped, `independent-connect-verification`/`cold-successor`/`cold-successor-verification` failed at download-artifact); live-verified-ai-action-proof SUCCESS but preflight-only, behavioral jobs skipped (parity-blocked: stamp `77f3702d` ≠ main), so no migration inference). Extends SN-103 (prove memory across the process-death boundary — the VERIFY-receipt gap was named inside the proof).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The first main run of Live Intelligence Commit Proof drew its live boundary in one exact place: the mechanics passed and the comprehension failed. Run 36966438981's `fresh-lesson` and `independent-verification` jobs passed — the pipeline can emit and check — but `cold-successor-held-out` failed at `assert comprehension["understands_raw_source_separate"]`: the held-out successor did not demonstrate it understands the raw source as separate from its own synthesis. That is the proof's real gate — the same boundary SN-103 named for process-death memory (verify, don't assert). Three companion findings ride with it: (1) the projector step pushing commit `252686756e` to main from inside CI looks alarming and is by-design — record by-design side effects when they look surprising, never open repair work against them; (2) the missing `causal-learning-experiment-receipt` is a composition gap, not a composition proof — the experiment job was skipped, so dependent jobs failed at download-artifact, and no migration inference is drawn (same discipline as SN-092's self-invalidating tests); (3) a preflight-only SUCCESS is not a success — `live-verified-ai-action-proof` succeeded with all behavioral jobs skipped, parity-blocked by the stamp/main gap, so nothing about migrations was proven. The durable rule for any cold successor reading this proof's future runs: pass/fail lives at the comprehension assertion; everything else is plumbing.

## 🩷 HUMAN NOTE

Shawn — the new Live Intelligence Commit Proof ran on main for the first time, and the first run found its boundary immediately: the pipeline works (fresh-lesson and independent-verification passed), but the held-out cold successor failed one comprehension assertion — it couldn't demonstrate it understands the raw source as separate from its own synthesis. That's the gate that matters, and it held. Three honest footnotes ride with it: the projector's main-push from inside CI is by-design (recorded, not an incident), the missing experiment receipt is a skipped-job composition gap (not a failure, and no migration inference drawn), and the preflight-only "success" on the action proof proves nothing behavioral because every behavioral job was skipped. The board record carries the exact run, job, and assertion for whoever runs this next.

## 🟣 CHILD NOTE

Imagine a test for a new robot: it can pick up blocks (passed), it can stack them (passed), but the final question is "show me you understand the difference between the original drawing and your own drawing of it" — and the robot fails that one. The first two passes are just plumbing; the last question is the real exam. The rule: when a proof has many parts, the failing part tells you where the real test is. Also: when something looks scary but is actually on purpose (the robot pushing a button it was told to push), write down "that's on purpose" instead of panicking.

## 🔵 GRANDMA NOTE

It's like the driving test: the car starts fine, the mirrors adjust fine — those are just the mechanics. The part that matters is the examiner's question: "show me you can tell the difference between the road sign and your memory of the road sign." The new proof's first real run passed all the mechanics and failed exactly that question. That's where the standard is set. And the two side-notes are pure common sense: a loud noise that's supposed to be loud isn't a breakdown, and a skipped step can't prove anything about what was never tested.

## 🟠 NAYA NOTE

Apply this to every Live Intelligence Commit Proof run you read or operate: (1) the pass/fail lives at the comprehension assertion (`understands_raw_source_separate` on the held-out cold-successor retrieval) — `fresh-lesson` and `independent-verification` passing is plumbing, not proof; (2) record the exact failing coordinates (run 36966438981, job 110711219423, assertion, exit 1) so the next operator triages the gate, not the pipeline; (3) when a side effect looks alarming but is by-design (projector pushed `252686756e` to main from inside CI), record "by-design" explicitly and open no repair work against it — extends SN-079 (the gate firing is the gate working); (4) missing-artifact failures downstream of a skipped job are composition gaps, never defects in the consumer — and they license no inference (SN-092 discipline); (5) a preflight-only SUCCESS with behavioral jobs skipped (parity-blocked) proves nothing behavioral — label it exactly that, never let it round up.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": null,
  "evidence": {
    "first_main_run": "#554 5946437843 (2026-10-02T06:00:27Z) — Live Intelligence Commit Proof, run 36966438981 (on b7e0eeae44).",
    "failed_gate": "job `cold-successor-held-out` (110711219423), step 'Cold retrieve this run's exact Smart Note from machine registry and canonical runtime': AssertionError at `assert comprehension[\"understands_raw_source_separate\"]`, exit 1.",
    "passed_plumbing": "`fresh-lesson` and `independent-verification` jobs passed.",
    "by_design": "projector step pushed commit 252686756e to main from inside CI — by-design behavior, recorded.",
    "missing_artifact": "runtime-proof `causal-learning-experiment-receipt` never produced (experiment job skipped this run); `independent-connect-verification`/`cold-successor`/`cold-successor-verification` failed at download-artifact.",
    "preflight_only": "live-verified-ai-action-proof SUCCESS (36966438985) but preflight-only — behavioral jobs skipped (parity-blocked: stamp `77f3702d` ≠ main), so no migration inference."
  },
  "rule": [
    "the proof's pass/fail lives at the comprehension assertion on the held-out cold-successor retrieval; passing mechanics are plumbing, not proof",
    "record exact failing coordinates (run/job/assertion/exit) so the next operator triages the gate, not the pipeline",
    "record by-design side effects as by-design when they look surprising; open no repair work against them",
    "missing-artifact failures downstream of a skipped job are composition gaps that license no inference",
    "preflight-only SUCCESS with behavioral jobs skipped proves nothing behavioral — label it exactly"
  ],
  "lesson_line": "On the proof's first main run, the mechanics passed and the comprehension failed — the live boundary of Live Intelligence Commit Proof is the held-out successor's comprehension assertion, and everything else is plumbing.",
  "extends": "SN-103 (verify memory across the process-death boundary), SN-079 (the gate firing is the gate working), SN-092 (self-invalidating tests; name what a skipped path does not prove)"
}
~~~
