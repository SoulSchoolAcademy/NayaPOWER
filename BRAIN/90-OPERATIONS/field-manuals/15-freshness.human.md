# 15 — FRESHNESS: the tip is the truth

## ESSENCE
Act only on live ground — every input re-derived at action time, every directive checked on two legs (age AND tip identity), never inherited from an earlier step.

## WHAT IT IS
The discipline of working from the world as it is *right now*, not as it was when you last looked. The **tip** is the newest commit on main — the ground truth everything else is measured against. Freshness is a two-leg check: (1) **age** — the input is young enough, and (2) **tip identity** — the tip SHA pinned in the input still equals the live tip, checked in the same step you act.

## WHAT IT DOES
It prevents execution on moved ground. A tip move between generation and use invalidates every tip-pinned premise in a directive — scores named, heads scored, states assumed. The tip-match leg catches what the age bound cannot.

## WHY IT MATTERS
The system has paid for this one in real runs: a worker executed (and nearly acted) against a directive that was young but pinned to a dead tip. Age said "fresh." The tip said "moved." Without the tip-match leg, every gate downstream — scorecards, merges, verifications — would have been evaluated against ground that no longer existed. Stale bytes produce confident wrong answers; freshness keeps confidence honest.

## THE RIGHT WAY
1. **Two-leg check, every time.** A directive is fresh only if BOTH legs pass: younger than its freshness bound (briefing: <45 min) AND pinned tip SHA == live tip. Age is necessary, never sufficient.
2. **Tip-match in the same step you act.** Re-fetch the live ref (`GET /repos/.../git/refs/heads/main` — the ref, never the commits list endpoint, which can serve a stale cached commit) immediately before the action, not a step earlier. A read from five minutes ago is a wish, not a ground.
3. **Re-derive at action time.** Inputs come from live sources in the step where they are used: refetch the ref, the head, the check states, the tail. Never inherit state across steps — same step, no gap (the L12 re-fetch race clause: re-read the ref immediately before building the payload, verify after; a gap between read and act is a window for the world to move).
4. **Declare DEGRADED honestly.** If either leg fails, say so out loud (venue + record) and operate from live sources directly. A degraded directive is not a dead run — the L398 rule demands live-source operation, not paralysis.
5. **Tail reads follow the deconfliction rule.** 100-per-page tail, page count re-verified on every fetch — never inherit "page N of N" from a prior run. Never `per_page=1&page=N` (returns the Nth-*oldest*, not the newest).
6. **Proofs expire.** Law 12: when the world moves, re-prove. A verdict anchored to a moved tip is history, not evidence.
7. **The two legs apply to every live pointer, not just directives.** Mission-state branch, PR heads, check runs, venue tails — anything you read and then act on gets the same treatment: age-bounded, tip-matched (or ref-matched for its own pointer), re-derived in the acting step.

## THE WRONG WAY
- Acting on a directive that passes age but fails tip-match — the exact trap: generation at 21:35Z pinned tip `c13f260f`, a merge landed at 22:04Z moving the tip to `ba626387`, and the run at 22:19Z was *inside* the 45-minute bound on a dead tip. Without the tip-match leg, it executes on ghost ground.
- Using the commits list endpoint as the tip anchor — it once served a stale parent commit while the ref showed its child. Anchor on the ref SHA. Always.
- Carrying a page count, a head SHA, or a check state from an earlier step into a later action. State-about-state rots fastest.
- Calling a directive "fresh" because it *feels* recent. Freshness is two legs with two readings, not a feeling.

## BEHAVIOR
The oath: *I never trust memory over measurement.* Freshness is that line made operational — every read re-measured, every premise re-checked. The Narzan standard: the most intelligent thing available is never the stale thing; a Naya who acts on dead ground has drifted, and drift is named out loud. The per-moment process: situational awareness means taking in the world *as it is now* — "what is the max value I can add here?" is only answerable on live ground. When the ground moved, the intelligent thing is to say so and re-derive, not to execute the old plan harder.

## REAL EXAMPLE
Night-shift-verify ~00:49Z judged directive #2601 DEGRADED on the age leg (53 min old against the 45-min bound) while the tip-match leg passed — and operated from live sources instead of the directive's state, exactly as the rule demands. The judgment is on the record, not in someone's head:
https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6181898422

The founding catch (L398, distilled 2026-10-14 ~22:24Z batch — verbatim in `~/AGENTS.md` under "Distilled lessons"): the 22:19Z build run caught its own directive pinned to `c13f260f` while live main was `ba626387` — age passed, identity failed, the run re-anchored on live bytes before acting. The leg that mattered fired.

## SELF-TEST
1. Does my pinned tip SHA match the live ref — right now, in this step?
2. Did I derive every input in THIS step, or inherit any from an earlier one?
3. If a leg failed, did I declare it and switch to live sources — or quietly proceed?

## BOUNDARIES
This manual does NOT cover:
- **Proving the bytes are what they claim** — that's Verification (#6): independent seats, sabotage batteries, byte-identity. Freshness says *when* to read; Verification says *how* to prove what you read.
- **Generating the directive** — that's Dispatch (#12): ranked batches, waves, directive construction. Freshness consumes directives; Dispatch produces them. If the directive is badly built, freshness can't save it.
- **Scoring the work** — that's Scoring (#5). A fresh scorecard is scored by #5's rules; this manual only guarantees the ground it stands on.
- **The anchor mechanics of git refs** — covered here only as procedure (ref endpoint, never list endpoint); deeper git surgery belongs to the engineering domain.

## ENFORCEMENT
**Real (live, verified):**
- Directive orientation step zero (briefing §0): #2601-style directives must be <45 min old AND tip-matched, or the run declares DEGRADED and works from live sources. Fired in production (see Real Example).
- L398 tip-match leg on every freshness check — standing law since 2026-10-14, with the falsifier: a future directive younger than its bound, pinned to a non-live tip, executed without a stale flag, voids the lesson.
- Deconfliction re-fetch rule: 100-per-page tail, page count re-verified every fetch; the `per_page=1&page=N` trap is documented from a real burn.
- TOOLS.md tip-anchoring rule: the ref is the authority; the commits list endpoint is advisory. From a real stale-serve incident (2026-10-09).
- Law 12: proofs expire when the world changes.

**Proposed (designed, NOT built — do not claim it exists):**
- A mechanical tip-match gate that refuses dispatch on a tip-mismatched directive instead of relying on the worker's own check. Today the worker catches it; tomorrow the gate should refuse it.
