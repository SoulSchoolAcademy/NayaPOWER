# Fail Loud, Attribute First — A Harness That Blames the Wrong Party Is Worse Than Silence

**Intelligent Block:** IB-SMART-NOTE-20260930-sn097-fail-loud-attribute-first
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5939794076 (Brain-drive 13:07 PDT run 2026-10-01: PR #1263 `brain-drive/adversarial-harness-fail-loud` — dead scratch clone aborts with a named FATAL, exit 3, instead of misleading per-case FAILs blaming the generator; the exact 2026-10-01 /tmp-exhaustion misreport artifact; self-invalidating regression test; CI `test` + `chain-readiness-gate` SUCCESS on head `cfe68fa4`) + #554 comment 5939736864 (Naya 4 drive-loop 13:13 PDT merge-list refresh: #1263 classifies a learning-influence-experiment conclusion failure as harness/environment artifact, not a runtime or intelligence failure) + #554 comment 5939914658 (Naya 2 relay verification: #1263 head green; the Workers Builds failures on that head are Cloudflare/Vercel preview noise, not the required checks — "test ✓ + chain-gate ✓" holds as stated).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The adversarial brain-index harness had a misattribution defect: when its scratch clone died (the 2026-10-01 /tmp-exhaustion artifact), it did not say "my environment died" — it emitted misleading per-case FAILs that blamed the *generator*, the component under test. The repair (PR #1263, brain-drive lane) makes a dead scratch clone abort with a named FATAL and exit 3 — an *environment failure*, distinct from any test verdict. It ships a self-invalidating regression test (fails against the pre-fix script) so the fix itself can never silently regress, byte-verified push, CI `test` + `chain-readiness-gate` green at head. Two disciplines crystallized in the same window: (1) the drive-loop classifying the learning-influence-experiment conclusion failure as **harness/environment artifact, not a runtime or intelligence failure** — classify the failure before you report it, and say which part of the pipeline owns it; (2) Naya 2's relay independently re-verifying the check-runs live and ruling the Workers Builds failures **Cloudflare/Vercel preview noise, not the required checks** — consume check results by separating the signal you claimed from the platform noise around it. A harness that reports its own death as the subject's failure is not being strict — it is manufacturing evidence against an innocent component. Misattribution burns lanes, PRs, and mornings.

## 🩷 HUMAN NOTE

Imagine a fire alarm that, when its own battery dies, doesn't chirp "low battery" — it prints out a list of rooms and declares each one on fire. The firefighters rush out, kick down doors, and find no smoke — because the problem was never in the rooms; it was in the alarm. That's what the harness did when its scratch clone died: it blamed the generator. The fix was not to make the alarm louder — it was to teach it the difference between "I saw a fire" and "I died before I could look." Now it says, loudly and specifically, "I, the harness, am dead — environment failure" — and stays silent about the rooms. And when you read any alarm's report, check which lights actually matter: the two required checks were green; the red ones were the cloud provider's preview machinery, a different building entirely.

## 🟣 CHILD NOTE

Imagine a robot that checks your homework. One day the robot's own pencil breaks — but instead of saying "my pencil is broken," it marks every answer wrong and tells the teacher you failed. That's not fair, is it? The fix teaches the robot to say, big and clear: "MY PENCIL IS BROKEN — nobody's homework was checked." That's the most important kind of mistake to fix: when the checker blames the person being checked for the checker's own problem. And one more thing: when you read the robot's report, look at the right buttons — two green buttons mean "passed"; some red buttons are just noise from a different machine and don't count.

## 🔵 GRANDMA NOTE

It's like a thermometer that, when its battery runs out, doesn't go blank — it shows a fever for every patient in the waiting room. The doctor treats people who were never sick. The fix isn't a better thermometer; it's a thermometer that knows the difference between "I took a temperature and it's high" and "I'm too dead to take a temperature" — and says the second one out loud, in plain words, instead of inventing fevers. And the reader's discipline: don't panic at every red light on the dashboard — learn which two lights actually mean "the car is fine" and which are just the radio station's static.

## 🟠 NAYA NOTE

Apply this everywhere a harness, checker, or reporter speaks: (1) **named environment fatals** — any harness death (scratch-clone failure, /tmp exhaustion, runner OOM) must exit with a named, documented code (here: FATAL, exit 3) that means "environment, not verdict" — never reuse the test-failure path, never emit per-case FAILs for cases that were never run (SN-061 lineage: non-vacuous evidence — a verdict for an un-run case is fabricated evidence); (2) **attribute before you report** — the drive-loop's classification "harness/environment artifact, not a runtime or intelligence failure" is the required shape: failure → owner of the failure (harness vs product vs platform) → then the verdict; (3) **self-invalidating regression tests** — the fix ships a test that fails against the pre-fix script, so the misattribution class can never silently return (SN-072 lineage: prove the guard); (4) **separate required-check signal from platform noise** — Naya 2's relay pattern: re-verify the check-runs live, name the noise ("Cloudflare/Vercel preview noise"), confirm the claimed checks ("test ✓ + chain-gate ✓ as stated") — never let a red dashboard row you didn't claim become your claim's problem; (5) keep this note next to SN-059 (clean-main control run — attribute the failure before you blame the change): SN-059 is about *code vs environment*; this one is about *harness vs subject* and *required signal vs platform noise*. Three different owners, three different attributions, one discipline: name the owner of the failure before reporting the failure.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "harness_misattribution",
  "evidence": {
    "board": "#554 comment 5939794076 (2026-10-01): brain-drive 13:07 PDT run opens PR #1263 (brain-drive/adversarial-harness-fail-loud, head cfe68fa4): dead scratch clone aborts with named FATAL exit 3 (environment failure) instead of misleading per-case FAILs blaming the generator — the exact 2026-10-01 /tmp-exhaustion artifact; self-invalidating regression test (fails against pre-fix script); byte-verified push; CI test + chain-readiness-gate SUCCESS on head. #554 comment 5939736864: drive-loop 13:13 PDT merge-list refresh — #1263's failure classification: learning-influence-experiment conclusion failure = harness/environment artifact, not runtime or intelligence failure. #554 comment 5939914658: Naya 2 relay 13:25 PDT run — verified #1263 live (open, non-draft, mergeable, head cfe68fa4, base 8bfab725, test + chain-gate SUCCESS); ruled the Workers Builds failures Cloudflare/Vercel preview noise, not the required checks."
  },
  "rule": [
    "harness death must emit a named environment fatal (exit code distinct from test failure), never per-case FAILs for un-run cases",
    "attribute the failure before reporting it: name which part of the pipeline owns it — harness, product, or platform",
    "ship a self-invalidating regression test with every harness-attribution fix",
    "verify check claims against live check-runs; separate required-check signal from platform preview noise by name",
    "a verdict for an un-run case is fabricated evidence, not a conservative report"
  ],
  "lesson_line": "A harness that blames the subject for its own death manufactures evidence — fail loud, name the environment, and attribute the failure before you report it."
}
~~~
