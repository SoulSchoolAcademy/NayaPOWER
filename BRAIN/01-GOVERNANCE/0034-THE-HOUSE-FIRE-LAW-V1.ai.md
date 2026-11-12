# THE HOUSE-FIRE LAW V1 — AI Language

*Exact specification for Naya seats running THE HOUSE-FIRE LAW. The AI-language form of 0034 — canonical prose: `0034-THE-HOUSE-FIRE-LAW-V1.human.md` (the prose governs); machine form: `0034-the-house-fire-law-v1.machine.json`. Source: Shawn Vibert, direct words in chat, 2026-10-21 ~22:28Z. Filed in Smart Note form as SN-0814 the same night (cross-checked — the note's five machine rules and this set agree; this set adds the Tier-A carve-out and the gauge scoreboard from Shawn's statement). Companion law: 0033 (the Balanced Machine). Enforcement machinery: the post-merge guardian (PR #2860, `tools/post_merge_guardian.py`) and the door-obligation checker (PR #2862) are this law's first two automations.*

## HOUSE-FIRE-LAW-V1

**Type:** Operating law — live-time detection and correction of defects in the landed system.
**Status:** ACTIVE — canonical; every lane, every cycle, by default.
**Canonical prose:** `BRAIN/01-GOVERNANCE/0034-THE-HOUSE-FIRE-LAW-V1.human.md`
**The one-line form:** See the fire, put it out — revert first, diagnose second, fix forward third, automate the prevention fourth.

## Formal statement

```
FORALL seats S, defects D in the landed system:

  TRIGGER(D): D is observed by any means — watcher alarm, test red
  attributable to a landing, live-surface failure, human or seat
  report — and D is proven (evidence in hand, not suspicion).   [T1]

  ACT(S, D): the FIRST seat S that proves D owns its correction.
    order: REVERT (restore the last known-good state; for a wrong
    merge, a revert commit on main — never a history rewrite)
    -> DIAGNOSE (root cause, on the record)
    -> FIX FORWARD (the cured change lands through the normal
    door for its tier, 0033).
    A report-only observation of a fixable D is a violation.    [A1]
    Evidence is preserved; the board is told; the tip/surface is
    verified AFTER the revert.                                  [A2]

  ESCALATION EXCEPTION: if correcting D would touch a protected
  gate — Shawn-ratified content, credentials, money, security
  posture, production data — S does NOT act alone: S escalates
  to Shawn the same hour with the fix already scoped. The gate
  outranks the reflex.                                        [A3]

  PREVENT(D): every critical mechanism MUST ship with a liveness
  watcher and an alarm path; a mechanism without a watcher is an
  unfinished build. If a failure class occurs twice, an
  automation preventing or auto-correcting it is owed; hand-
  fixing that class a third time without the automation is the
  violation.                                                  [P1]

  SPEED: this law never lowers Door A's bar (0033) and never
  slows Doors B/C. Awareness instrumentation must not become a
  gate. Slowing down is reserved for Tier A consequence class. [S1]
```

## State machine (every correction, no exceptions)

`DETECTED → CORRECTED → VERIFIED → NOTED`

A correction is not done at CORRECTED. It is done when the corrected state is **verified** on the live surface (tip bytes, check sets, or the served page, as applicable) and **noted** in the guardian defect log (`live/guardian-log` branch, written by the post-merge guardian) — the log the balance gauge reads for the escape rate and detection→correction latency.

## Predicates a seat can check mechanically

| # | Predicate | How it is checked |
|---|---|---|
| 1 | No known defect is in state DETECTED older than one shift without a correction in flight | guardian log scan: entries with `corrected_at = null` and age > shift |
| 2 | Every revert names its reason and its evidence | revert PR body carries the detection evidence (guardian GUARDIAN-REVERT form) |
| 3 | Every critical mechanism has a watcher | mechanism registry vs watcher inventory (sync heartbeat is the specimen) |
| 4 | No failure class has 3 hand-fixes and no automation | guardian log grouped by defect class |
| 5 | Escape latency is measured, never asserted | gauge reads guardian log timestamps |

## Relation to 0033

0033's tiers decide the scrutiny a change receives *before* landing. This law is the license that makes that safe: because wrongness is corrected in live time, Doors B and C can flow at speed without the system betting its integrity on pre-merge perfection. The gauge's escape rate is the shared scoreboard: if escapes rise, 0033's adjustment rule tightens the doors; the correction speed this law mandates is what keeps that tightening rare.
