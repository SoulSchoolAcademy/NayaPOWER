# ACT Influence-Bridge Experiment — Report (Naya Gamma)

**Verdict: DELTA DEMONSTRATED** — 0 failing check(s).
Generated: 2026-10-12T00:02:24.851150+00:00
Engine: `BRAIN/12-ENGINEERING/kernel_behavior_engine.py` at live tip.
Receipts (JSONL): `experiment-receipts-20261012-000224.jsonl` in `experiments/act-influence-bridge/receipts/`

## The question
Does a REAL retrieved lesson change a REAL action plan through the ADVISE
bridge — end to end, with receipts? Not test fixtures: a real lesson from the
repo's learning store (`.naya/memory/smart-notes/index.json`), through the
real reader seam, through the real full `execute_cycle`.

## The real lesson
- **SN-0340 — The Scorecard Law** (intelligent block
  `IB-SMART-NOTE-20261005-sn0340-the-scorecard-law`)
- Source truth state: **RATIFIED** (Shawn Vibert, 2026-10-05) — the strongest
  trust signal in the store.
- Principle (quoted verbatim from the live projection): "Shawn's supreme law: you must scorecard everything. Every decision runs through a written scorecard — enumerate all options, score each on value, consequences, …"
- Translator rules T1–T4 (see `real_lesson_reader.py`): RATIFIED→VERIFIED trust
  mapping; owner scoping to the acting owner; applicability to
  `consequential_action`; advisory authored from the law's text
  ("no scorecard, no merge") into the bridge's allowlist keys.

## The five arms (identical action, identity, authority, evidence)
| Arm | Bridge | Lesson | ADVISE | Plan delta |
|-----|--------|--------|--------|-----------|
| A control | engaged | none | NO_CHANGE | none |
| B control | BYPASSED | real lesson, visible | NO_CHANGE | none |
| C treatment | engaged | real lesson (reader) | ADVISED | +2 proof reqs, +1 constraint, +1 note |
| D control | engaged | real lesson, FOREIGN owner | NO_CHANGE (unauthorized_cross_owner) | none |
| E parity | engaged | real lesson (input context) | ADVISED | identical to C |

## The delta (arm A vs arm C — before/after)
- **Before** (arm A, no lesson): proof_requirements = `['independent']`,
  constraints = `[]`, advisory_notes = `[]`
- **After** (arm C, SN-0340 via bridge): proof_requirements = `['independent', 'scorecard_receipt:options_enumerated_and_scored', 'scorecard_gate:reversibility_and_damage_checked']`,
  constraints = `['scorecard_required_before_merge']`,
  advisory_notes = `['SN-0340 The Scorecard Law: no scorecard, no merge. Every decision runs through a written scorecard.']`
- Action type untouched: `consequential_action` in both arms.
- Original requirement preserved: monotonic-additive, nothing removed.
- ADVISE receipt hashes differ (A vs C) and ACT output hashes differ —
  the delta is in the receipts, not claimed.
- Arm B proves the bridge is the causal mechanism: the same lesson, present
  and visible but unevaluated, changes nothing.
- Arm D proves the gate holds for real lessons: a foreign owner's lesson is
  excluded with reason `unauthorized_cross_owner`.
- Arm E proves reader-path parity: reader vs input-context retrieval produce
  the identical ADVISED plan.

## Why the bridge caused it
The influence receipt (arm C) records lesson_id, before/after, and the
enforced rule: "Lesson IB-SMART-NOTE-20261005-sn0340-the-scorecard-law applied
to action plan (+2 proof requirements, +1 constraints)". ACT's receipt checks
"Action plan incorporates applicable retrieved intelligence (ADVISE)" with
evidence `advise_influences:1`. No other arm's input differs except the
intelligence/bridge path — the delta has no other possible cause.

## What this does NOT claim (D32 anti-cascade)
- It does NOT prove production behavior: this runs the reference
  implementation (`kernel_behavior_engine.py` V2, whose own docstring says
  "runtime production proof remains separate"), not production operations.
- It does NOT prove the store natively carries executable advisories: the
  `advisory` and `applies_to_action_types` fields are translator-authored
  (rules T1–T4). What is real: the lesson's identity, principle text,
  RATIFIED state, and provenance. The experiment proves the BRIDGE carries a
  real lesson's influence into a real action plan — the executable encoding
  of a law into advisory form remains a separate, human-owned seam.
- It does NOT prove lessons change decisions in every pipeline: one action
  type (`consequential_action`), one lesson (SN-0340), one engine version.
  Generalization requires the four-way template at scale (Epsilon's lane).
- It does NOT certify the owner-scoping policy: T2 assigns the acting owner
  because the store carries no owner field. The cross-owner REJECTION gate is
  what is proven (arm D); owner assignment policy is not.
- Scorecard honesty: this report is generated from the run's own receipts by
  `build_report()`; failing checks would print FAIL and flip the verdict.

## Failing checks
None — all 33 checks held (see console output and receipts JSONL).
