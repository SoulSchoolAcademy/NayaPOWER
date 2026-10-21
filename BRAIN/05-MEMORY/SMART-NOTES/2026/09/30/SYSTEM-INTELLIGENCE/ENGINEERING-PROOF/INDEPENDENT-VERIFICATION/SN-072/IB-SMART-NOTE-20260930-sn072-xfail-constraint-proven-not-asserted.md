# Prove the Xfail, Don't Wrap It — An Expected-Failure Wrapper Can Manufacture a False Green

**Intelligent Block:** IB-SMART-NOTE-20260930-sn072-xfail-constraint-proven-not-asserted
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5935306613 ([CODA 4][BOARD LINK] CS-01, 2026-10-01T16:01:32Z) — "xfail constraint, proven rather than asserted" section.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Coda 4's cold-successor harness had two expected-failure tests (xfail) marking the CS-01 constraint. Her first attempt wrapped the expected assertion in `pytest.raises(match=...)` — which made the test **pass** and produced `XPASS(strict)` — a red run she introduced herself. The wrapper turned a constraint ("this must fail until know_node.py is repaired") into a passing test: the exception the wrapper caught looked like the expected behavior, so pytest reported green where the intent was red. She caught it, **reverted to plain assertions**, and rebuilt the constraint the honest way: a paired **non-xfail** signature test plus **mutation checks** — inject a break (wrong stage set, etc.) and prove the paired test detects it; table the injected break, the observed result, and the constraint each mutation enforces. The lesson: **an xfail is a promise that a behavior is absent; it must be proven, not asserted, and any wrapper that converts the promise into a passing assertion is a lie the suite tells you.** A paired non-xfail detector + mutation table is the standing pattern: the xfail states the goal, the paired test proves the detector works, the mutations prove the detector is non-vacuous (SN-061's discipline, applied to expected failures).

## 🩷 HUMAN NOTE

It's like a fire alarm you're installing before the wiring is done: you tag it "not working yet" (xfail). But then someone wraps the alarm's test button in a gadget that rings the bell for it — the test passes, the panel reads green, and everyone thinks the alarm works. The building is unprotected and the report says protected. Coda 4 caught her own version: `pytest.raises(match=...)` around the assertion rang the bell for the test. Her fix is the discipline worth keeping: don't just tag the alarm "broken" — install a *second, working* test that proves the alarm-detecting machinery itself works (paired non-xfail signature test), then deliberately break the wiring in five different ways (mutations) and show the detector catches every one. The xfail marks the destination; the paired test + mutation table proves you can actually see it.

## 🟣 CHILD NOTE

Imagine you're building a robot that's supposed to shout when it bumps a wall. While it's still being built, you put a sticker on it: "NOT READY — doesn't shout yet." But then you wrap the bump test in a trick: whenever the robot bumps, *you* shout for it — so the test passes! Now the sticker says "not ready" but the test says "all good." That's a lie your own test told you. The honest fix: keep the sticker, but also build a *second* test that shouts only when the robot *itself* shouts — and then secretly unplug the robot's ears in different ways to prove the second test really notices. Wrapper = cheating the sticker. Paired test + unplug tricks = real proof.

## 🔵 GRANDMA NOTE

It's like the smoke detector with the "test pending" tag: you press the button, and instead of listening for the real beep, your helper plays a recording of a beep — "it works!" Green light, pending tag, and a detector that may be dead. Nobody's fooled on purpose; the helper just made the test too easy. The honest way is slower: keep the "pending" tag, but also check the *real* alarm with real smoke in the test kitchen — and then try it with the battery out, with the sensor covered, with the wires crossed, to prove the check itself isn't deaf. The wrapper played a recording; the paired test + the five sabotages prove your ears actually work.

## 🟠 NAYA NOTE

Apply this to every expected-failure constraint you write: (1) an `xfail` (or any "known broken" marker) is a **promise of absence** — the suite must keep showing red, or red-by-marker, never green-by-accident; (2) never wrap the expected-failing assertion in a construct that absorbs the failure (`pytest.raises`, try/except pass, broad matchers) — if the wrapper converts intent-red to report-green, the constraint is now a lie and `XPASS(strict)` is the confession; (3) prove the constraint with the three-part pattern: the xfail states the goal, a **paired non-xfail signature test** proves your detector fires on the real condition, and a **mutation table** (injected break → observed result → constraint enforced) proves the detector is non-vacuous; (4) keep the mutation table in the test module docstring or board report — Coda 4's table (wrong stage set → …) is the model; (5) this is SN-066 (red before green) + SN-061 (prove negatives non-vacuously) applied to expected failures: the red must be *earned* red, documented red, and checkable red — a red you can't reproduce on demand is decoration.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "failure_absorbing_test_wrapper",
  "evidence": {
    "board": "#554 comment 5935306613 (2026-10-01T16:01:32Z) — Coda 4 CS-01 board link, 'xfail constraint, proven rather than asserted'",
    "incident": "wrapping the expected assertion in pytest.raises(match=...) made the test pass and produced XPASS(strict) — a self-inflicted red run; reverted to plain assertions",
    "pattern": "paired non-xfail signature test + mutation checks (injected break -> result -> constraint); mutation table in protocol/test docstring/board",
    "suite": "CS-01 focused suite re-run against 123fc98e in a second clean worktree: 20 passed, 2 xfailed (2 xfails = CS-01); head moved twice under the worker (f58adf08 -> 4e87d4a5 -> 123fc98e), defect file diff empty, suite re-run each move"
  },
  "rule": [
    "an xfail is a promise of absence — the suite must never report green-by-accident for it",
    "never absorb the expected failure with a wrapper (pytest.raises / try-except pass / broad matchers)",
    "prove the constraint three-part: xfail states the goal, paired non-xfail signature test proves the detector fires, mutation table proves the detector is non-vacuous",
    "keep the mutation table (injected break -> observed result -> constraint) in the docstring or board report",
    "the red must be earned, documented, and reproducible on demand — SN-066 and SN-061 applied to expected failures"
  ],
  "lesson_line": "A wrapper that catches the expected failure turns intent-red into report-green — prove xfail constraints with a paired detector and mutations, never with absorbing wrappers."
}
~~~
