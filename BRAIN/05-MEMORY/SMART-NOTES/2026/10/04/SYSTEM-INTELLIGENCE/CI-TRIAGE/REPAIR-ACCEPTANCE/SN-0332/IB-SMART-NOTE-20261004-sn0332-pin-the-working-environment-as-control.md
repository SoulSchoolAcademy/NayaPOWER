# Pin the Working Environment as the No-Regression Control — Name the Acceptance Test Before Hardening

**Intelligent Block:** IB-SMART-NOTE-20261004-sn0332-pin-the-working-environment-as-control
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 5989083176 (Naya 4, fallback acceptance + hardening dispatch, 2026-10-04) / 5988980201 (Naya 2, beat-bug verdict, 2026-10-04)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 4's fallback acceptance (5989083176) is the model shape of a repair plan for an environment-specific failure. It states three things *before* the builder starts: (1) "Real-browser behavior is pinned as the no-regression control" — the environment where it works today becomes the control that must keep passing while the failing path gets hardened; (2) "headless tap-through of all 10 exchanges is the acceptance test" — the exact acceptance criterion, named on the exact environment that failed; (3) the bounded scope — "beats must form even when AudioContext can't run; voice becomes enhancement, not a gate." The lane stays coordinated ("no action needed from you" — no duplicate lanes), and the verdict that started it all (5988980201) already classified the failure as a robustness gap, not a ship-blocker.

Why this is brain-grade: hardening a failing path without pinning the working one is how you trade an environment-specific failure for a regression everyone can see. The control makes the repair testable in both directions: the old green must stay green (no-regression control), the old red must turn green (acceptance test), and both are stated before work begins — so "done" is mechanically checkable instead of vibes. This is the sequel to SN-0329 (don't patch a non-bug): when the classification says the repair *is* warranted — a genuine robustness gap — the acceptance structure is what keeps the repair from manufacturing a new problem.

Rule for a cold successor: **when hardening a failing-environment path, pin the passing environment as the no-regression control and name the acceptance test on the failing path before the repair starts. The plan must state what must not change, what must change, and how both are proven — before anyone touches code.**

## 🩷 HUMAN NOTE

Shawn — a repair-discipline note from tonight's beat-bug follow-up worth banking: when I accepted Naya 2's verdict (headless-only failure, real browser works fine), the hardening order I sent the builder had the acceptance baked in before any work started: the real browser is the control — it must keep painting beats exactly as today, no regressions allowed; the test browser is the acceptance — all 10 exchanges must tap through to speaking there. Scope bounded: beats form without audio, voice is enhancement not gate. The plan says what must not change, what must change, and how both get proven — so "done" is checkable, not vibes. New rule for repairs: pin the working side as the control, name the failing side's test, then start.

## 🟣 CHILD NOTE

After figuring out the bug only happens in the test browser (the real one is fine), the fix order was written like a proper recipe: (1) the real browser must keep working exactly as it does now — that's the control; (2) in the test browser, all 10 demo conversations must work — that's the test; (3) the fix: the animation must not need sound, sound is a bonus. Lesson: before fixing anything, write down what must stay the same AND what must get better — then "done" is something you can actually check.

## 👵 GRANDMA NOTE

When it was time to fix the browser-specific bug, the repair order spelled everything out up front: the browser that already works must keep working (that's the baseline we protect), the browser that fails must pass a specific test (all ten demo conversations), and the scope is bounded (animation without sound; sound is a bonus). The lesson: a good repair plan names what must not change and what must change before any work begins — that way, "finished" is provable, not a feeling.

## 🤖 NAYA NOTE

Source: #1354 5988980201 (Naya 2, 2026-10-04 23:00 PDT — beat-bug verdict: headless-only failure in the audio-fallback path; beat path sound; "this is a robustness gap, not a ship-blocker… should NOT hold up the v9 delivery"; recommendation: "a fallback-path hardening pass when you're in there"), 5989083176 (Naya 4, 23:11 PDT — verdict accepted; "a builder is now hardening the audio-fallback path in v9 (beats must form even when AudioContext can't run; voice becomes enhancement, not a gate). Real-browser behavior is pinned as the no-regression control; headless tap-through of all 10 exchanges is the acceptance test. Will report the fix + proof here when it lands. The lane stays coordinated — no action needed from you."). Cousins: SN-0329 (don't patch a non-bug — the classification this note's repair follows; this is its acceptance sequel), SN-0233 (the Phantom Green — controls must be virgin-state: the real-browser control pins the un-repaired passing state), SN-0061 (branch-green is not merged-true — a verdict binds exact conditions; here the acceptance binds both environments), SN-0105 (propose-then-build — the no-duplicate-lanes coordination).

## ⚙️ MACHINE NOTE

{"sn": "SN-0332", "title": "Pin the Working Environment as the No-Regression Control — Name the Acceptance Test Before Hardening", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-04", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "REPAIR-ACCEPTANCE"], "cousins": ["SN-0329", "SN-0233", "SN-0061", "SN-0105"], "evidence": {"board": "#1354 5988980201 (beat-bug verdict: headless-only, robustness gap not ship-blocker), 5989083176 (fallback acceptance + hardening dispatch)", "control": "real-browser behavior pinned as no-regression control (must keep painting beats)", "acceptance": "headless tap-through of all 10 exchanges", "scope": "beats form without AudioContext; voice = enhancement, not gate", "coordination": "lane stays with Naya 4's builder; no duplicate lanes"}, "rule": "when hardening a failing-environment path: pin the passing environment as the no-regression control and name the acceptance test on the failing path before the repair starts; the plan states what must not change, what must change, and how both are proven"}
