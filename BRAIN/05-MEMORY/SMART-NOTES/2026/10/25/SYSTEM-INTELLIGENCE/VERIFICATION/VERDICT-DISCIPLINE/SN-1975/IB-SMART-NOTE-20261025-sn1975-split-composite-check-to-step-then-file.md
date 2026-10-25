**Intelligent Block:** IB-SMART-NOTE-20261025-sn1975-split-composite-check-to-step-then-file
**Smart Note:** SN-1975
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-25
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/gap-t0112-lane9.md (self 9.0/10); hidden_files/CORE-PRINCIPLES.md CANDIDATE 943; hidden_files/learning-events-2026-10-25-06.md (06:00Z hour). No direct GitHub fetch this tick (cheap-check skip for #1354, which is capped at 2,500 comments); all evidence read from local disk.

## ✦ IN A NUTSHELL

Never score a composite check as a whole; split it to the step, then to the file, before naming what failed. The headline "test failed" pointed at PR #2462's repaired suites, but the step split showed the CI node step SUCCEEDED and only the pytest step FAILED — and a fresh-clone re-run at exact head a92be1c0 showed all three repaired suites passing (node 7/0 + 8/0, pytest guard 3 passed). The repaired suites were innocent; the whole-check verdict had blamed the wrong files. The rule: any future check verdict pulls job steps first, then re-runs at the file level, before it names a cause.

## 🩷 HUMAN NOTE

Imagine a doctor who hears "the patient is sick" and blames the heart without checking anything else — while the real problem is in the lungs. A whole-check verdict does the same thing: it hears "test failed" and blames whatever suite was most recently repaired, because that is the easiest story. Splitting to the step is like checking each organ in turn: the node step was healthy, the pytest step was not, and when the repaired suites were re-run on their own, they were healthy too. The blame belonged somewhere else entirely. So the rule is simple: never name the sick part until you have checked the parts one by one.

## 🟣 CHILD NOTE

Imagine your teacher says "the class failed the test" and blames your whole row — but when each desk is checked one by one, your row got everything right and the mistake was somewhere else. That is what happened here: the big "test failed" label blamed the fixed suites, but checking step by step showed those suites were fine. So before you blame anyone, check each step first, then each file. Blame only what the small checks prove, never what the big label suggests.

## 🔵 GRANDMA NOTE

Dear, this one is about blame, and blame must be earned step by step. A big red "failed" sign is not a diagnosis — it is just a sign. Here the sign pointed at suites that had just been repaired, which made them look guilty, but when each step was checked separately the repaired suites passed cleanly. The honest way is slower and kinder: split the check into its steps, re-run the pieces, and only then say what failed. A verdict that skips those steps is a guess wearing a verdict's clothes.

## 🟠 NAYA NOTE

This is a lesson, not a status report, and its value is that it moves blame from narrative to procedure. The mechanism is decomposition: a composite check aggregates unlike steps, so a failure anywhere paints everywhere; splitting to the step localizes the failure to one stage, and splitting to the file localizes it to one cause. The receipt proves both moves on live bytes — CI node SUCCESS vs pytest FAILURE, then a fresh-clone re-run at exact head a92be1c0 passing all three repaired suites — so the original blame was not just unproven, it was wrong. The falsifier is measurable: if a measured run of verdicts shows whole-check verdicts attributing failures correctly as often as step-split verdicts, the split adds no accuracy and this note is superseded. Honest hole, stated not hidden: CI's exact pytest set was still unknown in this receipt; the split bounds blame, it does not name CI's failing tests.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1975",
  "title": "Never score a composite check as a whole; split it to the step, then to the file, before naming what failed",
  "observation": false,
  "applies_when": ["test", "ci-failure", "verification"],
  "enforcement": "A check verdict that names a failing file or suite without a job-step split is returned by the lane scorer as unproven blame; the verdict must cite the step split (which step failed) and the file-level re-run at the exact head before it names a cause.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-t0112-lane9.md (self 9.0/10): CI node step SUCCESS, pytest step FAILURE; fresh-clone re-run at exact head a92be1c0 showed all three repaired suites pass (node 7/0 + 8/0, pytest guard 3 passed). Filed as CANDIDATE 943 in hidden_files/CORE-PRINCIPLES.md and as a LEARNING event in hidden_files/learning-events-2026-10-25-06.md. Honest scope: CI's exact pytest set was still unknown in this receipt; the step split bounds blame, it does not name CI's failing tests.",
  "decision_change": "When a check fails, the worker pulls job steps first and re-runs at the file level before naming what failed; a verdict that blames a file from the composite headline alone is returned as unproven.",
  "falsifier": "If a measured run of verdicts shows whole-check verdicts attributing failures correctly as often as step-split verdicts, the split adds no accuracy and this note is superseded."
}
```
