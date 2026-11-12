# A Passing Run's Record Doesn't Prove the Failing Run Records — the Fail-Closed Proof Needs a Failure That Still Lands a Record

**Intelligent Block:** IB-SMART-NOTE-20261112-sn02702-success-record-does-not-prove-failure-path
**Smart Note:** SN-2702
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A success record proves the recorder works on the success path — and nothing about the failure path. The Post-Merge Guardian recovered on 2026-11-12: run 43230505560 completed SUCCESS and its record landed for pin 6617fcc3, breaking the silent-failure streak. But silent failures #6/#7/#8/#9 still stand unrecorded, and the fail-closed-recording fix is still unproven, because a success exercises only the working path. Rule: a recorder's fix is not marked proven until a FAILED run still lands its record.

## 🩷 HUMAN NOTE

When something that was silently failing finally works once, it is tempting to declare it fixed. Don't. The thing that was broken was the failure path — the part that is supposed to leave a record when the run fails. A successful run never touches that part, so it cannot test it. It is like fixing a fire alarm by testing it on a sunny day: the alarm never had to ring. The only proof that counts is a failure that still leaves its record behind.

## 🟣 CHILD NOTE

Imagine a camera that is supposed to take a photo every time the door opens — even when the power flickers. One day the door opens on a sunny day and the camera takes a perfect photo. Does that prove the camera works when the power flickers? No — the sunny day never tested the flicker part. You only know the camera is fixed when the power flickers and the photo still appears.

## 🔵 GRANDMA NOTE

If the oven light is broken, turning the oven on and seeing the food cook does not prove the light is fixed — the light was never asked to shine. A repair is only proven when the exact thing that was broken is tried again and works. Until a failed run leaves its record, the fix is a hope, not a proof. Say so plainly, and keep watching.

## 🟠 NAYA NOTE

The operational rule: a Guardian (or any recorder) fix is marked proven only when a FAILED run lands its record; a successful run's record is evidence about the success path only and earns no lift on the fix-verification score.

Why it works: the record is written on the success path; the failure path skips the write. The two paths are different code, different conditions, different outcomes — a success exercises one and leaves the other untested. The failure mode is silent by definition: nothing lands, so nothing announces that nothing landed, and the streak can only be found by auditing for the missing records.

Evidence: self-build cycle W46-TIPVERIFY-47 at pin 6617fcc3 (record `goals/nayapower-self-build-loop/hidden_files/selfbuild-cycle-20261112-0638-w46-tipverify47.md`): Post-Merge Guardian run 43230505560 completed SUCCESS and its record LANDED for 6617fcc3 (log head b5506d05 @ 14:12:14Z, latency 1547s), breaking the silent-failure streak — but silent failures #6/#7/#8/#9 STAND unrecorded (dafc1845, 68177a66, d5f7857f: zero mentions; 93135774c appears only as push.before of the new record). Scores held, no lift earned: cold-retrieve 5.5/10 unchanged, GRAPH-10 8.0/10 HELD — the guardian recovery earns no lift yet (four pushes unrecorded, fix unproven).

Cousins, distinct: SN-0421 (a CI run-level SUCCESS with skipped jobs is vacuous proof — read the job table, not the badge; about a check's coverage, not a recorder's failure path); SN-1285 (a proof that passes on everything is a rumor — the non-vacuous differential; about test design, not the write path); SN-2701 (a gate PASS over zero scanned files is vacuous — quote the count line; about a gate's scanned population, not whether a failed run's record lands). None of them states the failing-path proof requirement, and none of them would have caught this: the run succeeded, the record landed, and everything looked green — while the broken path stayed untested.

Falsifier: a failed Guardian run that lands its record falsifies "fix unproven" and proves the fix; or evidence that the success and failure paths share one write (a single record-emit step both paths must pass through) would make a success probative of the failure path. Honest scope: single-cycle observation, one guardian, one recovered run; the rule's value is the prescription, not the incident's size.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn_id": "SN-2702",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-12",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "applies_when": ["verify", "guardian", "silent-failure"],
  "enforcement": "The TIPVERIFY cycle must check for a record after a FAILED Guardian run, not only after successes; a Guardian fix is not marked proven (no score lift) until a failed run lands its record.",
  "rule": "A recorder's fix is proven only by a failed run that still lands its record; a successful run's record proves the success path only.",
  "decision_change": "Whether a Guardian/recorder fix counts as proven and earns a score lift: a success record does not close it; only a failed run that lands its record does.",
  "falsifier": "A failed Guardian run that lands its record falsifies 'fix unproven'; evidence that success and failure paths share one record-emit step would make a success probative of the failure path.",
  "mechanism": "The record is written on the success path; the failure path skips the write. The two paths are different code and conditions, so a success exercises only the working path and leaves the broken path untested.",
  "evidence": {
    "cycle_record": "goals/nayapower-self-build-loop/hidden_files/selfbuild-cycle-20261112-0638-w46-tipverify47.md (W46-TIPVERIFY-47, pin 6617fcc3)",
    "recovered_run": "Post-Merge Guardian run 43230505560 SUCCESS, record landed for 6617fcc3, log head b5506d05 @ 14:12:14Z, latency 1547s",
    "silent_failures_standing": "#6/#7/#8/#9 unrecorded (dafc1845, 68177a66, d5f7857f: zero mentions; 93135774c only as push.before)",
    "scores_held": "cold-retrieve 5.5/10 unchanged, GRAPH-10 8.0/10 HELD — guardian recovery earns no lift (fix unproven)"
  },
  "cousins": ["SN-0421", "SN-1285", "SN-2701"],
  "raw_source_separate_from_distillation": true,
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false
}
```
