# Aggregate Gate on an Unhealed Tip Is a Permanent Per-PR Veto

**Intelligent Block:** IB-SMART-NOTE-20261013-sn1202-aggregate-gate-on-unhealed-tip-is-a-permanent-pr-veto
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 board comment 6149794640 — 🧠 LEARNING EVENT 2026-10-13 ~15:58Z distillation (named failure mode L307, class F6, new surface); PR #2514's "Verify merge authority" gate reading the `tests_green` aggregate; base tip `34338065` with 6 pre-existing failures reproducing on base bytes alone.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

An aggregate health gate shipped onto an unhealed tip converts a tip defect into a permanent per-PR veto. PR #2514's new "Verify merge authority" gate reads the `tests_green` aggregate and exits 1 on *every* head — not because the PR is broken, but because the tip carried 6 pre-existing failures, all reproducible at base tip `34338065`. The gate is fail-closed and *correct*; its scope silently includes evidence the PR doesn't control. The PR can never go green until someone else heals the tip, and the veto reads as the PR's fault.

**The durable rule: never ship an aggregate gate without the tip green at ship time, or without PR-scoped aggregation.** If the gate must read an aggregate, the receipt must record the gate-on-base-bytes probe: run the gate against the base tip alone and prove the failure is PR-caused before attributing it to the PR. *Falsifier: a blocked PR whose gate red reproduces on base bytes alone.*

## HUMAN NOTE

This is the "is it me or the floor?" question made mechanical. When a new gate blocks a PR, the first diagnostic is never "fix the PR" — it is "does the gate fail on the base tip with no PR applied?" If yes, the gate is measuring the tip, and the attribution is wrong. A fail-closed gate with misattributed scope is worse than no gate: it burns builder time, erodes trust in gating itself, and trains lanes to distrust red. The ship-time check is cheap and permanent: green tip at ship, or scoped aggregation, or the gate doesn't ship. When inheriting an existing aggregate gate, demand the base-bytes probe in the receipt before accepting its verdict.

## CHILD NOTE

Imagine your teacher makes a new rule: "your homework must be perfectly clean to pass." But the paper she hands out is already smudged before you write a word. Every kid fails — not because of their work, but because of the smudged paper. The fair rule is: check whether the paper was already smudged *before* grading the kid. That base-paper check is the gate-on-base-bytes probe.

## GRANDMA NOTE

It's like grading a whole class's homework on a quiz that was already misprinted before anyone sat down. The teacher's rule is sound, but she's grading the printing press, not the children. Always check the paper was clean first — otherwise good work gets blamed for a bad start.

## NAYA NOTE

A gate is only as honest as its attribution. When I build a gate that reads an aggregate, I must prove the aggregate is clean at the base — otherwise I am converting someone else's defect into my PR's permanent verdict. Fail-closed is a direction, not a virtue: a gate that fails closed for the wrong reason is a machine for producing false blame. The probe against base bytes is the honesty check; it costs one run and saves every future misattribution.

## MACHINE NOTE

```json
{
  "sn": "SN-1202",
  "lesson": "aggregate-gate-unhealed-tip-permanent-pr-veto",
  "failure_mode": "L307",
  "class": "F6",
  "rule": "ship aggregate gates only on green tip, or with PR-scoped aggregation; record gate-on-base-bytes probe in receipt",
  "falsifier": "blocked PR whose gate red reproduces on base bytes alone",
  "applies_to": ["gate-design", "merge-authority", "ci-health-gates"],
  "evidence": {
    "board_comment": 6149794640,
    "pr": 2514,
    "base_tip": "34338065",
    "gate": "Verify merge authority reading tests_green aggregate"
  },
  "truth_state": "CANDIDATE",
  "supersedes": null
}
```
