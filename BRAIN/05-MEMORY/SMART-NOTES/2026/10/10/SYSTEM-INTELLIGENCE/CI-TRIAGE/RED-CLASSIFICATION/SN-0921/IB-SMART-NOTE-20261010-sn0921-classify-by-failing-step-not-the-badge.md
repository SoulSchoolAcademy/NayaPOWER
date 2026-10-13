# Classify a CI Red by the Failing Step Name from Live Job Logs — Never by the Badge

**Intelligent Block:** IB-SMART-NOTE-20261010-sn0921-classify-by-failing-step-not-the-badge
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** Smart Note distillation loop
**Provenance:** #2175 comment 6102355418 (Director pass 21:16Z — tip moved, CI red classified step-level from live job logs, 2026-10-10T21:27:17Z); CI run 38086899899; tip `cfbd81c`; independent `--check` on exact tip bytes in a fresh worktree

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

At tip `cfbd81c` (2026-10-10 21:16Z) CI showed three failures. Classified by workflow badge, the board would have read "test red, promote-and-prove red, Truth Resolver red" and routed three repair jobs. The director pass opened the live job logs instead and classified by **failing step name** — and the three reds were three different things with three different owners:

- `test` → step **"Verify generated Brain index has no drift"** = **REAL RED**, brain-index drift class, sixth occurrence. Independently verified on exact tip bytes in a fresh worktree: REAL-TREE.json + REAL-TREE.md don't match regen. Introducers: snapshot-refresh commits `0fd7d051` + `71d307e7`, PR #2186 (`drift_canary/` spec + 15-framework stack), PR #2187 (mission-state snapshot refresh) — none carried a regen (the #2173 pattern). Owner: brain-build repair lane (re-pin at `cfbd81c`, rebase-before-regen, regen, re-stamp).
- `promote-and-prove` → step **"Enforce ratified standing policy before automatic promotion"** = **GUARDRAIL FIRING AS DESIGNED**. Fail-closed on the test red; not a defect, not a lane action. Correct behavior proven by the failure itself.
- `Current Truth Resolver` → step **"Collect live GitHub evidence"** = **ENVIRONMENT RED, not a tip defect.** The log line is explicit: `gh: API rate limit exceeded for installation` at 21:15:24Z on the workflow's installation token; the director's connector token unaffected. A code-fix lane assigned to this would chase a bug that isn't in the code.

The method: **the workflow badge is not the classification unit; the failing step's name and its log line are.** SN-0240/SN-0430/SN-0557/SN-0775 classify reds by origin (PR-introduced vs base-inherited vs guardrail vs projector-commit); this note adds the missing step *before* that: open the live job log, name the failing step, and admit **environment** as a first-class red — a check whose own token, rate limit, or runner environment broke. Environment reds are documented as environmental and never routed to a repair lane as tip defects, never re-investigated as code bugs on the next pass.

Why this is brain-grade: without it, the same tip keeps generating phantom work. The Truth Resolver had been flapping all day (failures at 16:50Z / 19:19Z / 19:42Z / 19:53Z interleaved with successes) — every flap a temptation to "fix" a non-defect. One step-name read converts four investigations into one sentence: the workflow's token is rate-limited during heavy windows; the code is innocent. A correct "not a tip defect" classification is as valuable as a correct repair — it spends zero actions on phantom work, and the budget law says every action matters.

## HUMAN NOTE

Shawn — a triage-method lesson from tonight's director pass. When CI goes red, don't read the badge — "test failed" tells you almost nothing. Open the job's live log and find the exact step that failed; its name usually names the cause. Tonight one tip had three reds and all three were different: a real drift the repair lane owns, a safety guardrail working exactly as designed (the red IS the proof), and a checker whose own GitHub token hit a rate limit (nothing to fix, nothing broken in our code). Same badge, three owners, three actions — and one of the three actions is "do nothing." That's the lesson: name the step, not the badge.

## CHILD NOTE

Imagine the school's scoreboard shows three red lights. You could guess what's wrong — but if you open the little door behind each light, there's a label: one says "the art board fell off the wall" (go fix it), one says "the alarm rang because it smelled smoke — good alarm, no fire" (leave it alone), one says "this light is red because its own battery died" (change the battery, not the scoreboard). The label behind the light is the failing step name. Always read the label.

## GRANDMA NOTE

When three warnings pop up on the dashboard, they don't all mean "the engine is broken." One is the engine, one is the seatbelt light doing its job when you haven't buckled, and one is just the sensor having a bad day. The trick is reading the small print on each warning before you call the mechanic. Tonight's lesson is that small print — the name of the exact step that failed, read from the machine's own log. Read it first, and you won't spend money fixing what isn't broken.

## NAYA NOTE

Triage order for any CI red, from now on:

1. Open the live job log (not the badge, not the check-run name alone).
2. Name the failing STEP. The step name is the classification unit.
3. Classify the step: REAL RED (defect at tip bytes — verify on exact tip bytes before routing) · GUARDRAIL-AS-DESIGNED (fail-closed on another red — no repair, record the proof) · ENVIRONMENT RED (the check's own token, rate limit, or runner broke — document as environmental, never route to a repair lane as a tip defect).
4. Route only REAL RED to a repair lane, with the exact tip SHA and the step evidence. Guardrail and environment reds are recorded and closed in the same tick — a correct "not a tip defect" is a perfect triage.
5. If a check flaps intermittently (Truth Resolver all day: failures interleaved with successes), the step-name evidence is the flap's explanation — log the environmental cause once, and stop re-investigating the code.

## MACHINE NOTE

```json
{
  "intelligent_block_id": "IB-SMART-NOTE-20261010-sn0921-classify-by-failing-step-not-the-badge",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "sn_number": "SN-0921",
  "lesson": "classify CI reds by the failing step name from live job logs, never by the workflow badge; environment red (the check's own token/rate limit broke) is a first-class class — document it, never route it to a repair lane as a tip defect; the same red badge can hide REAL RED, GUARDRAIL-AS-DESIGNED, and ENVIRONMENT RED on one tip",
  "evidence": {
    "board": "#2175",
    "comment": "6102355418",
    "tip": "cfbd81c",
    "ci_run": "38086899899",
    "real_red": "test -> step 'Verify generated Brain index has no drift'; drift verified on exact tip bytes in fresh worktree; introducers 0fd7d051 + 71d307e7 + PR #2186 + PR #2187, none carried a regen (the #2173 pattern); sixth occurrence of the class",
    "guardrail": "promote-and-prove -> step 'Enforce ratified standing policy before automatic promotion'; fail-closed on the test red as designed",
    "environment_red": "Current Truth Resolver -> step 'Collect live GitHub evidence'; log line 'gh: API rate limit exceeded for installation' 21:15:24Z on the workflow's installation token; connector token unaffected; all-day flap (16:50Z/19:19Z/19:42Z/19:53Z interleaved with successes) explained by rate pressure during the heavy window, not a code defect"
  },
  "refines": ["SN-0240", "SN-0430", "SN-0557", "SN-0775"],
  "protocol": "triage: open live job log -> name failing step -> classify step (REAL_RED / GUARDRAIL_AS_DESIGNED / ENVIRONMENT_RED) -> route only REAL_RED to repair lane with exact tip SHA + step evidence; record and close the other two in the same tick"
}
```
