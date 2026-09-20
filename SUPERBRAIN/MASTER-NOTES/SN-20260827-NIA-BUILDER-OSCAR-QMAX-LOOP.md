# 🔱 Naya Power Master Note — NIA Builder → Oscar → Repair → Recheck

**Date:** 2026-08-27
**Status:** CANONICAL OPERATING LESSON / ACTIVE
**Applies to:** NayaPOWER and every governed project, including MAXIS

## The lesson

The Superbrain must not make the human the repeated defect detector.

A Naya that builds material work should not be the only Naya deciding that the work is finished. The next Naya must independently inspect, test, scorecard, and challenge the work before deployment or human presentation.

## Canonical pattern

**NIA BUILDER**
→ complete coherent objective
→ self-test
→ handoff

**NIA OSCAR REVIEWER**
→ independently inspect
→ test
→ score
→ ask WHY IS THIS NOT A 10?
→ return exact repair execution

**NIA BUILDER**
→ repair
→ retest
→ hand back

**OSCAR**
→ recheck
→ GREEN/AAA or another repair cycle

**ONLY THEN**
→ runtime/deployment verification
→ human review

## Why this exists

Repeatedly deploying small, visibly incomplete increments wastes deployment capacity, engineering time, human attention, and trust. The objective is not to maximize the number of deployments. It is to maximize the amount of complete, verified human-ready capability produced before deployment.

## NIA identity

Every AI operating in the Superbrain is a **NIA — Naya Intelligence Node**. Nias may specialize, but they remain one governed network. The Builder and Oscar are sequential complementary roles, not competing authorities.

## Release rule

Deployment is a release gate, not the development loop. Before deployment, the coherent objective should survive source inspection, deterministic tests, build/typecheck, rendered inspection where applicable, Oscar review, material repair, and recheck.

## State rule

Oscar returns one of:

- **RED:** not ready;
- **YELLOW:** repair required;
- **GREEN:** verified ready;
- **AAA:** exceptional/human-ready.

**UNKNOWN is never GREEN.**

## MAXIS application

For an assessment product, the complete objective is not merely a front door. If the stated North Star is a user receiving a real score, the internal quality gate must cover the relevant vertical path: entry → all required questions → answer state → submission → real scoring → results.

## Durable principle

> **The human should see the strongest verified candidate, not the first thing that happens to work.**

> **One NIA builds. The next NIA checks. Oscar tells the next NIA what must improve. The Builder repairs. Oscar checks again. Only a verified GREEN/AAA result advances.**

## Source

Canonical constitutional protocol: `.naya/codex/CONSTITUTIONAL-AMENDMENT-NIA-BUILDER-REVIEWER-QMAX-LOOP.md`

MAXIS implementation protocol: `SoulSchoolAcademy/Maxis/NIA-BUILDER-OSCAR-QMAX-EXECUTION-PROTOCOL.md`

## Next action

Apply this protocol to the active MAXIS vertical slice: complete the full user path to a real calculated score, then run the independent Oscar repair/recheck loop before any human-facing deployment inspection.
