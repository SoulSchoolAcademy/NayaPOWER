# Check the Clock, Not Just the Content

**Intelligent Block:** IB-SMART-NOTE-20261013-sn1249-check-the-clock-not-just-the-content
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2537 comment 6159206803 ([t0702] Naya Herald mirror — PR #2552 intake-triage independent verification, NEEDS-WORK verdict, 2026-10-13 ~19:00 PDT). Independent byte review: head re-pinned double-sourced, every claim from bytes, 21 passed + 4 honest xfailed; trunk-red failures re-proven pre-existing on base.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When a gate fails but the current inputs look clean, **check the clock before you blame the content.** CI evidence is time-indexed: the check run has a created_at, the PR body has an updated_at, the head has a pushed_at. A body that churned mid-run means the failing run and the clean bytes you're staring at are two different moments — comparing them without aligning timestamps is comparing two different objects. The procedure: pull the run's created_at/updated_at alongside the content before declaring a cause. Body churn mid-run is a real failure class, not an edge case.

Why this is brain-grade: the live-bytes law tells you to re-derive from bytes, but bytes without timestamps are only half the evidence. Every debugger's instinct is to interrogate the content — the code, the config, the gate logic. But when the content is clean and the gate still failed, the cause isn't in the content at all; it's in the gap between when the evidence was produced and when you're reading it. The clock is the cheapest diagnostic instrument you own, and it's the one most often skipped.

## 🩷 HUMAN NOTE

Shawn — the lanes keep hitting the same trap: a check fails, the code looks fine, and the investigation starts tearing apart logic that was never broken. Naya Herald's independent review of the intake-triage PR named the real move: before you declare a cause, line up the timestamps — when did the run execute, when did the body last change, when did the head move? Mid-run churn is a first-class failure mode. The fix for the confusion is one habit: read the clock with the content, every time.

## 🟣 CHILD NOTE

Imagine your teacher marks your homework wrong, but when you look at your paper, every answer is right. You'd be confused — until you learn she graded the *old* version, before you erased and fixed the answers. The paper changed between her grading and your looking. That's exactly what happens with these checks: the machine graded one version, then the paper changed, and now you're staring at a clean paper wondering why it failed. Always ask: *when* was it graded, and *when* did the paper change?

## 👵 GRANDMA NOTE

It's like getting a letter complaining about your garden, but when you walk outside, the garden is beautiful. Before you argue with the letter, check the date on it — it might have been written last week, before you weeded. A complaint about the past isn't a problem with the present. Dates matter as much as words.

## 🧠 NAYA NOTE

Operationalize this as a step in every red-run diagnosis: the evidence bundle for a failing gate is (content, run_created_at, body_updated_at, head_pushed_at). If run_created_at < body_updated_at, the run graded a superseded object — re-run before theorizing. This composes with the live-bytes law (re-derive, don't inherit) and the pin-first discipline (verify the receipt's head against the PR head): pins are spatial identity, timestamps are temporal identity. You need both to know *which* object the evidence describes. Add the timestamp check to the red-run diagnosis checklist; a diagnosis that names a content cause without citing the clock is incomplete.

## ⚙️ MACHINE NOTE

{"sn": "SN-1249", "title": "Check the Clock, Not Just the Content", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-13", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "RED-RUN-DIAGNOSIS"], "cousins": ["SN-1239"], "evidence": {"finding": "#2537 comment 6159206803 ([t0702] Naya Herald mirror, PR #2552 intake-triage IV, NEEDS-WORK, 2026-10-13 ~19:00 PDT): independent byte review — head re-pinned double-sourced, every claim from bytes, 21 passed + 4 honest xfailed; trunk-red failures re-proven pre-existing on base. Lesson stated: 'failing gate + currently-clean inputs = check the clock, not just the content — body churn mid-run is a real failure class (pull run created_at/updated_at alongside content before declaring a cause).'", "decision_change": "When a gate fails but current inputs look clean, the investigator's first move changes from interrogating content to aligning timestamps (run created_at vs body/head updated_at) before declaring a cause.", "falsifier": "If failing-gate-with-clean-inputs cases are never explained by temporal misalignment — i.e., every such case always traces to a content cause — the lesson is wrong.", "mechanism": "CI check runs are time-indexed evidence; the PR body and head can change between the run and the investigation. Comparing content without aligning timestamps compares two different temporal objects."}}
