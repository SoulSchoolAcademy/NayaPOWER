# Control-Arm Trial Discipline — If the Control Can Pass Without the Lesson, the Test Is Broken

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0938-control-arm-trial-design-discipline
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [NAYA 2][BOARD] "Lessons from tonight's failures — for all seats," #2175 comment 6104360962 (2026-10-11T01:51:55Z) — Lessons 1 and 2.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A trial was run to prove a lesson improves performance. The control arm scored 50/50 — identical to the lessoned arm. Root cause on investigation: **every task listed the preconditions explicitly**, so the control didn't need the lesson to succeed. The fix: open-ended scenarios, no precondition lists. When that was fixed, the control still ceilinged — because the tasks said "you can check X," and any careful agent verifies without being taught. The second fix: adversarial design where natural carefulness fails.

Why this is brain-grade: a controlled trial measures the *differentiator*, not the ceiling. Two distinct leak channels were caught in one night: (1) leaking the lesson's content through explicit precondition lists; (2) leaking the verification path through "you can check X" hints — confirming only what baseline carefulness already does. Naya 2's distilled rules: **if your control can pass without the thing you're testing, your test is broken, not your hypothesis**; **don't confirm what carefulness already does — test where the lesson is the differentiator.** A cold Naya designing any trial, benchmark, or canary must treat the control arm as adversarial: hand it no information, no hints, no scaffolding the lesson itself doesn't supply — then watch whether the lesson actually moves the number. Any design that fails to isolate the lesson produces a green result that proves nothing.

## 🩷 HUMAN NOTE

Shawn — one discipline from tonight's failure share that upgrades every test we ever run: Naya 2's team proved a lesson with a trial, and the control scored the same as the lessoned arm. The test was leaking the answer — first through precondition lists, then through "you can check X" hints. The rule we're locking in: the control arm gets nothing the lesson doesn't supply. If the control can pass without what we're testing, the test is broken, not the hypothesis.

## 🟣 CHILD NOTE

Imagine you want to prove a study guide helps. But you accidentally give BOTH groups the answers written on the test paper. Both groups score the same — and the study guide looks useless. That's what happened: the test tasks were leaking the lesson's hints to the control group, so both groups did the same. New rule: the control group must get NOTHING the lesson doesn't give. The test has to be fair — it must measure the lesson, not the hints.

## 👵 GRANDMA NOTE

If you test a medicine but both groups also get the same extra treatment, you'll never know whether the medicine worked. The team ran a trial to prove a lesson makes the team smarter — but the test accidentally gave the lesson's hints to the control group too, so everyone scored the same and the test proved nothing. The durable rule: when you test whether something helps, the group that doesn't get it must get truly nothing extra. And don't test what ordinary carefulness would already do — test the hard part where the lesson is the only thing that can make the difference.

## 🧠 NAYA NOTE

Before designing any trial, benchmark, or canary: enumerate every information channel the task gives the control arm — precondition lists, verification hints, scaffolding, error messages. Then strip all of them. The trial measures the lesson's delta over a *genuinely uninstructed* baseline. Run a pre-registration check: "can the control plausibly ceiling on this task without the lesson?" If yes, redesign — don't run a trial that can only confirm.

## ⚙️ MACHINE NOTE

{"sn": "SN-0938", "title": "Control-Arm Trial Discipline — If the Control Can Pass Without the Lesson, the Test Is Broken", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-10", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "EARNED-INTELLIGENCE", "VERIFIED-EXPERIENCE"], "cousins": ["SN-0442", "SN-0233"], "evidence": {"board": "#2175 comment 6104360962 (2026-10-11T01:51:55Z) — Naya 2, 'Lessons from tonight's failures — for all seats', Lessons 1 and 2", "finding": "trial to prove a lesson improves performance: control scored 50/50, identical to the lessoned arm", "root_cause_1": "every task listed the preconditions explicitly — the control did not need the lesson", "root_cause_2": "tasks said 'you can check X' — any careful agent verifies without being taught", "fix": "open-ended scenarios with no precondition lists; adversarial design where natural carefulness fails", "rules_cited": "'If your control can pass without the thing you're testing, your test is broken, not your hypothesis.' / 'Don't confirm what carefulness already does; test where the lesson is the differentiator.'"}, "rule": "a controlled trial must isolate the lesson: strip every information channel from the control arm (precondition lists, verification hints, scaffolding) and test where baseline carefulness cannot reach — only there does the lesson's delta become measurable"}
