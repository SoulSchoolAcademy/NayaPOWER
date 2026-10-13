# Pilot the Audit Target Pre-Launch: Preregistered Gates Don't Save a Wasted Run

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0720-pilot-the-audit-target-pre-launch
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6068853907 ([NAYA 4] [LEARN-DRIVER] area completion, 2026-10-08T20:53:36Z) — SoulSchoolAcademy

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Trial-17 ran to completion: 20/20 blinded subjects, Tier-S statistics met — and then the preregistered ceiling gate fired and the whole trial was declared **INVALID_BY_CEILING**. The measurement target had been sitting near the ceiling the entire time; nothing in the data could have distinguished signal from the ceiling, so the integrity machinery did exactly what it was built to do and threw the run away. The failure wasn't dishonesty — the close-out was impeccably honest — it was waste: a full trial's worth of subjects, compute, and attention spent on a target that a ten-minute pilot would have disqualified. Lesson L17, captured with the close-out: **pilot the audit target pre-launch.**

Why this is brain-grade: the team already had the *integrity* half of the discipline — SN-0693 says pre-register the prediction before you change the data, and the ceiling gate firing honestly instead of being waived is exactly that law working (compare SN-0485: a good run that meets neither the stated n nor the blockers changes nothing). What was missing was the *investment* half: preregistered gates protect the conclusion's integrity, but they do nothing to protect the run's cost. A gate that invalidates a completed trial is correct and expensive at the same time. The pilot is the cheap gate before the expensive one: run the measurement instrument against the audit target first, verify the target has room to move (no ceiling, no floor, no degenerate baseline), verify the gates won't fire trivially — *then* spend the full run. Register the rule, then verify the target survives it, before spending the trial.

This is distinct from its cousins. SN-0693 (pre-register the prediction) governs *when* the rule is written — before touching the data. SN-0329 (reproduce in the target environment before you patch the demo) governs *where* you verify — the real environment, not a degraded harness. This note governs the *target itself*: before the full run, confirm the thing you're measuring can actually be measured by your instrument, with headroom on both sides. Two halves, one law: the prediction is registered before the data moves (SN-0693), and the audit target is piloted before the trial spends (SN-0720). A trial that is preregistered but unpiloted is honest waste.

Rule for a cold successor: **no learning trial launches without a pilot receipt** — the audit target, the instrument's baseline read on it, ceiling/floor headroom confirmed, the preregistered gates shown not to fire trivially. Ten minutes of pilot saves a twenty-subject trial.

## 🩷 HUMAN NOTE

Shawn — Trial-17 finished tonight with an honest but expensive outcome: 20 blinded subjects ran, the stats hit Tier-S, and then the preregistered ceiling gate fired and the whole trial went INVALID_BY_CEILING. The measurement target was hugging the ceiling the whole time — nothing could have been learned. The close-out was textbook-honest; the waste was avoidable. Lesson L17 is now on record: pilot the audit target before launching the trial. A ten-minute pilot read would have shown the target had no room to move and saved the full run. We already had the integrity half (preregister the gates); now we have the investment half (pilot the target before spending the trial).

## 🟣 CHILD NOTE

Imagine you spend all day building a race track for your toy cars, and when you finally race them, you discover the finish line was already at the starting line — every car "wins" before it moves. You learned nothing, and the whole day was wasted. A smart racer would walk the track first and check the finish line is far enough away. That's the lesson: before running a big test, do a tiny practice run to make sure the test can actually tell you anything. Ten minutes of checking saves a whole day of building.

## 👵 GRANDMA NOTE

The team ran a full experiment with twenty test subjects tonight and did everything right — except the thing they were measuring turned out to be stuck at the top of the scale, so no real result was possible. The honest thing happened: they threw the results out rather than pretend. But the smarter thing, now on record, is to run a tiny practice round first: check that what you're measuring actually has room to change before spending the whole effort on it. A quick check up front saves a lot of wasted work.

## 🟣 NAYA NOTE

I now treat "preregistered" as only half the job. The other half is the pilot receipt: the audit target named, a baseline instrument read taken, ceiling and floor headroom confirmed, the preregistered gates shown not to fire on sight. A trial that launches without it is honest waste — and Trial-17 proved the cost: twenty blinded subjects, Tier-S stats, all of it correctly discarded by the ceiling gate. The integrity machinery worked; the investment discipline didn't. I pilot the target, register the gates, and only then spend the run. Both halves or neither.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0720",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/MEASUREMENT-BOUNDARY",
  "doctrine": "pilot-the-audit-target-pre-launch",
  "rule": "No learning trial launches without a pilot receipt: the audit target, a baseline instrument read on it, ceiling/floor headroom confirmed, and the preregistered gates shown not to fire trivially. Register the rule before the data moves; verify the target survives the rule before the trial spends.",
  "failure_mode": "Trial-17: 20/20 blinded subjects + Tier-S stats completed, then preregistered ceiling gate fired → INVALID_BY_CEILING; full trial cost correctly discarded (honest waste)",
  "cousins": ["SN-0693", "SN-0329", "SN-0440", "SN-0485"],
  "evidence": [
    "#1354 comment 6068853907 ([NAYA 4] [LEARN-DRIVER], 2026-10-08T20:53:36Z) — 'Trial-17 closed out (14:45Z run's work, no sign-out was posted then): 20/20 blinded subjects, Tier-S stats met but preregistered ceiling gate fired → INVALID_BY_CEILING, honest. Lesson L17 captured (pilot the audit target pre-launch). PR #1879 open/unmerged.'",
    "SN-0693 (pre-register the prediction) covers the integrity half; this note covers the investment half — no existing note on piloting the audit target (staged-notes tree grep, 2026-10-08)"
  ]
}
