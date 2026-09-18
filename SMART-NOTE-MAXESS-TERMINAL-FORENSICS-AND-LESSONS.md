# SMART NOTE — MAXESS TERMINAL FORENSICS, LESSONS & RECOVERY PLAN

## Purpose
Prevent repeated debugging loops, preserve every lesson, and force the MAXESS engine work to advance by evidence rather than repetition.

## Locked Objective
The immediate objective is singular:

`E00.118 Q15 Continue → next() → save() → publish() → calculate/buildResult() → validate → MAXESS_RESULT_V1`

No Name/Topic generation. No E01–E04 changes until E00 itself produces the authoritative result.

## What We Tried / What It Taught Us

### 1. Full E00→E04 integration runs
**Outcome:** Repeatedly stopped at Q15.
**Lesson:** Reproduces the symptom but has too large a debugging surface. Do not use full integration as the first diagnostic.

### 2. Parent/iframe harness work
**Outcome:** Genuine iframe integration infrastructure was established, but it still reproduced the Q15 terminal stall.
**Lesson:** The harness can observe the problem, but it cannot substitute for proving the production E00 terminal boundary.

### 3. GitHub Actions browser proof
**Outcome:** Browser automation reproduced the same Q15 stopping point.
**Lesson:** The defect is not merely Shawn's manual browser environment. Automation confirms reproducibility, but Q15 completion is not result success.

### 4. Downstream E01–E04 inspection
**Outcome:** A downstream consumer cannot display a result that E00 never publishes.
**Lesson:** Downstream debugging before authoritative-result production is premature.

### 5. Repeated reruns of substantially similar proofs
**Outcome:** More evidence of the same symptom without crossing the terminal boundary.
**Lesson:** Repeating an experiment that answers no new question is wasted motion. Change the debugging boundary.

### 6. Static inspection of the button/terminal path
**Outcome:** DOM/event lifecycle remains a plausible area, but static inspection alone has not proven the exact runtime failure.
**Lesson:** Never promote a hypothesis to fact. Instrument the exact runtime boundary.

### 7. Broad architectural/integration thinking
**Outcome:** Too much time was spent thinking about the whole system while the first authoritative result still did not exist.
**Lesson:** Shrink the problem until the failure becomes deterministic; then expand only after the rung is proven.

## Oscar Review — What Was Wrong With the Previous Reasoning

1. We optimized for coverage instead of information gain.
2. We treated reproduction as if it were diagnosis.
3. We sometimes moved downstream before proving the upstream contract.
4. We allowed the integration harness to become the debugging target instead of the production engine.
5. We did not force a strict first-failure checkpoint early enough.
6. We repeated experiments that had already produced the same information.
7. We did not sufficiently separate hypotheses from verified facts.
8. We optimized for architectural completeness before achieving the smallest executable success.
9. We allowed the ladder to advance and retreat instead of locking each proven rung.
10. We failed to change strategy quickly enough after materially similar attempts produced the same result.

## Top 10 Recovery Hypotheses — Weighted + Success Path

### 1 — 30% — Visible Continue is not executing the intended `next()` path
**Problem:** The visible button can appear enabled while the executable handler is absent, stale, detached, or otherwise not receiving the click.

**Success path:** Fetch the complete canonical E00.118; identify the actual button node, `updateContinue()`, binding code and `next()`; instrument `CLICK_RECEIVED` and `NEXT_ENTERED`; run E00 alone; if `CLICK_RECEIVED` is missing, repair the binding at the actual live DOM boundary.

**Success evidence:** `CLICK_RECEIVED → NEXT_ENTERED` on Q15.

### 2 — 20% — The live button is a replaced DOM node
**Problem:** Groove/page lifecycle may replace the button after the original listener was attached.

**Success path:** Compare the live Q15 button node identity with the node used during binding. Prefer a lifecycle-safe binding/delegation repair rather than repeatedly attaching listeners.

**Success evidence:** The current visible button receives the event and reaches `next()` after Q15.

### 3 — 12% — Event propagation/lifecycle is intercepting the click
**Problem:** Another handler, propagation order, `preventDefault`, or `stopPropagation` may block the intended path.

**Success path:** Instrument capture/bubble order and handler entry without redesigning the architecture. Identify the first interceptor, then make the smallest boundary repair.

**Success evidence:** Deterministic event path reaches `next()` exactly once.

### 4 — 10% — A JavaScript exception prevents terminal binding or execution
**Problem:** The UI can remain visible even when an exception has broken the executable path.

**Success path:** Capture page/console exceptions during Q15 and correlate them with the terminal checkpoints. Repair only the exception that blocks the first missing checkpoint.

**Success evidence:** No blocking exception and terminal checkpoints continue in order.

### 5 — 8% — `next()` is reached but the Q15 branch is not entered
**Problem:** The button is not actually the root cause; terminal control flow may branch incorrectly.

**Success path:** Instrument `NEXT_ENTERED` and `Q15_BRANCH`. If `next()` fires but Q15 branch does not, inspect the question index/state and repair that condition only.

**Success evidence:** `NEXT_ENTERED → Q15_BRANCH` with the expected Q15 state.

### 6 — 6% — Q15 save state is invalid/incomplete
**Problem:** The terminal branch may reject the final response or fail to persist the 15th answer.

**Success path:** Instrument `SAVE_COMPLETE` and assert `responses.length === 15`. Inspect the exact state entering and leaving `save()`.

**Success evidence:** Exactly 15 valid responses immediately before publish.

### 7 — 5% — `publish()` is gated or unreachable after save
**Problem:** The response is saved, but terminal control flow never crosses into publication.

**Success path:** Instrument `PUBLISH_ENTERED`; inspect guards/returns between save and publish; remove only the blocking defect.

**Success evidence:** `SAVE_COMPLETE → PUBLISH_ENTERED`.

### 8 — 4% — Calculation/buildResult produces an invalid or incomplete result
**Problem:** Publication may begin but scoring/result construction may fail.

**Success path:** Instrument `CALCULATE_COMPLETE` and `RESULT_VALID`; verify `overallScore`, exactly five dimensions, `masteryBand`, and 15 responses against `MAXESS_RESULT_V1`.

**Success evidence:** A schema-valid authoritative result exists.

### 9 — 3% — Persistence/broadcast fails after a valid result exists
**Problem:** E00 may successfully calculate but fail to expose the result to the next boundary.

**Success path:** Verify `window.MAXESS_RESULT`, persistence and broadcast separately. Repair only the first failing publication boundary.

**Success evidence:** `RESULT_PUBLISHED` plus authoritative result observable by the consumer boundary.

### 10 — 2% — Groove/iframe context changes the terminal runtime environment
**Problem:** The code may execute in a different document/window context than expected.

**Success path:** Prove E00 standalone first. Only after E00 is green reconnect the genuine parent/iframe boundary and verify the existing contract.

**Success evidence:** E00 produces the same authoritative result standalone and through the genuine iframe integration.

## Execution Protocol — One Direction Only

### STEP 1 — Establish the exact production boundary
Fetch the complete canonical E00.118. Locate:
`continueButton`, `updateContinue()`, event binding, `next()`, Q15 branch, `save()`, `publish()`, `calculate/buildResult()`, validation, persistence and broadcast.

### STEP 2 — Instrument only E00 terminal execution
Use deterministic checkpoints:
`CLICK_RECEIVED → NEXT_ENTERED → Q15_BRANCH → SAVE_COMPLETE → PUBLISH_ENTERED → CALCULATE_COMPLETE → RESULT_VALID → RESULT_PUBLISHED`

### STEP 3 — Run E00 alone from Q1
Complete all 15 questions. The first missing or throwing checkpoint is the first failure. Do not guess.

### STEP 4 — Repair the first failure only
Make the smallest surgical change. No scoring redesign. No E01–E04 changes. No Name/Topic work.

### STEP 5 — Re-fetch the exact changed canonical code
Verify the committed code, not the intended code.

### STEP 6 — Re-run E00 from Q1
Require:
- exactly 15 responses
- valid `MAXESS_RESULT_V1`
- `overallScore`
- five dimension scores
- `masteryBand`

### STEP 7 — Lock E00 GREEN
Only after the authoritative result exists is the engine considered started.

### STEP 8 — Reconnect E01–E04
Then prove the existing result contract through E01, E02, E03 and E04 sequentially. Repair downstream only if executable evidence proves a real consumer defect.

## Ground Rules

- No repeated experiment without a new question it answers.
- No static inspection declared as runtime proof.
- No downstream repair for an upstream failure.
- No architectural redesign to solve a local event defect.
- No Name/Topic work until E00→E04 is genuinely green.
- Every repair must be re-fetched and verified.
- Every successful rung becomes protected evidence.
- If two materially similar attempts produce the same failure, change the debugging boundary.
- Cause-and-effect review is mandatory before every change: intended benefit, direct effects, collateral effects, rollback path.
- Never ask Shawn to test an unverified or ambiguous version.
- When human action is required, provide the exact link and exact version to test.

## Success Definition
The engine is not considered started because the button looks enabled, Q15 appears selected, or a test runner reaches Q15.

The first true success is:

`15 responses → calculation → valid MAXESS_RESULT_V1 → overallScore + 5 dimensions + masteryBand`

Then, and only then:

`MAXESS_RESULT_V1 → E01 → E02 → E03 → E04`

## Operating Mantra
**Find the first failure. Fix the first failure. Prove the repair. Lock the rung. Move forward. Never loop backward without new evidence.**

**Optimize. Maximize. Synergize. Equalize.**
