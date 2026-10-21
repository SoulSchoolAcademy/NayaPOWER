# Intelligent Block
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04 ~16:15 PDT (Smart Note distillation tick)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-0285
**Provenance:** #1354 comments 5985291250 (CODA 3 SIGN-IN, 2026-10-04T22:43:08Z — "CONTINUING — the gate now gates, and I proved the backfill works before touching main") and 5985343389 (CODA 1 SIGN-OUT, 2026-10-04T22:54:51Z — "THE GATE NOW BLOCKS NEW DRIFT — without reddening main on legacy debt"). Branch `coda1/sn002-conformance-gate`, commits `09daad5f8`/`b378a0b66` (11/11 tests) then `e5055153e` (15/15 tests green).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

When a new conformance rule would redden `main` on legacy debt, neither obvious answer is honest: `--check`-only blocks every merge on historical captures unrelated to any current change (unacceptable); `--report`-only is advisory and would not have caught SN-020/021/022 (the exact false-pass Coda 1 was sent to eliminate). Coda 1 built the standard third answer — **the ratchet**. Legacy debt is named, dated, and attributed in `.naya/conformance-baseline.json`: reported but not blocking. Anything not in the baseline and non-conformant → **CI BLOCKS**. And a ratchet that can grow is a permanent exemption wearing a ratchet's name, so he made the structural guarantees part of the code: `test_ratchet_blocks_a_new_non_conformant_capture` (the load-bearing one — without it, `--ratchet` is `--report` with extra steps), `test_baseline_never_grows` (every currently-failing capture named, so the ratchet is actually armed, not silently empty), `test_baseline_entries_that_now_conform_are_retirable` (a fixed capture MUST be droppable — this is how debt retires). The exit ramp is written in: the baseline carries `governance_key_repair_pending` (SN-002, SN-016, SN-020, SN-021, SN-022 — the five whose repair he proved flips them green with zero residual failure); when that list reaches zero, `--check` becomes safe and the baseline retires entirely. The path from advisory to fail-closed is already built — nobody has to design it later under pressure. Two more disciplines banked in the same run: (1) the consequential flip is the Human Director's to accept, not the lane's to impose — `--check` would turn `main` red for every merge until the five captures are repaired, so the gate ships runnable and visible and the flip is a one-word change: "I would rather hand you a working gate and a decision than a red `main` I decided alone." (2) The gate is CI-live with zero workflow edits — `kernel-tests.yml` already runs `python -m pytest -q`, so the test executes on every push; and the test **asserts the known-bad captures still FAIL**, so when a repair lands the suite announces it instead of going quiet. He also proved the backfill in simulation first — added only the governance key, changed nothing else, wrote to temp files — and got WOULD-BE-FIXED: 5 captures, zero residual: the complete backfill list is FIVE captures, not three, and SN-002 the specimen is one of them.

## HUMAN NOTE

Shawn — banking Coda 1's conformance-gate run as standing enforcement doctrine: when a new rule meets legacy debt, don't choose between blocking everything and advising nothing — build a ratchet. Ten historical failures get named, dated, and grandfathered (reported, never blocking); every NEW non-conformant capture blocks CI. The ratchet is structural, not aspirational: it has a test that proves it blocks a new violation, a test that proves the grandfather list never grows, and a test that proves fixed entries can retire. The exit ramp is already written — five captures to repair, then the baseline retires and the whole gate goes fail-closed. And note the judgment call worth copying: he did NOT flip CI to blocking himself, because a red `main` is your decision to accept, not his to impose. He handed you a working gate plus a decision instead. That's the ownership pattern: prove it works in simulation, ship it runnable and visible, leave the consequential flip to the director.

## CHILD NOTE

Imagine a school making a new rule: "no running in the halls." If they suspended every kid who ever ran before the rule existed, the school would be empty — unfair. If they just put up a poster, kids would keep running. The smart answer: every NEW runner gets stopped, and the kids who ran before get their names on a list with a date, watched but not punished — and every kid on that list can earn their name off it. The gate that stops the runners is already working; the decision to also suspend everyone on the old list belongs to the principal, not the hall monitor. And the hall monitor first tried the whole thing in an empty hallway to prove it worked before touching the real school.

## GRANDMA NOTE

We've written down a new rule for enforcing new standards on old work. A seat built a check that catches new mistakes without failing the whole system for old ones: past problems are listed by name, dated, and forgiven (but tracked — the list can never secretly grow, and fixed items must be removable); any brand-new problem blocks progress. The path to full strictness is pre-built: once the five listed items are repaired, the whole system goes strict automatically. Two judgment rules captured: the check runs quietly inside the existing test routine (no workflow surgery), and it announces repairs instead of silently passing; and the seat deliberately did not turn the strict mode on by himself — that consequence belongs to the human director, not the lane. He proved the repair plan in simulation first, before touching anything real.

## NAYA NOTE

For me, months from now: the ratchet pattern is the standing answer to "new rule + legacy debt." Recipe: (1) enumerate the currently-failing items by name; (2) grandfather them — named, dated, attributed, reported-not-blocking; (3) block all NEW non-conformant items; (4) test the block itself (a ratchet without `test_ratchet_blocks_a_new_non_conformant_capture` is advisory theater); (5) test the baseline never grows; (6) test entries can retire when fixed; (7) pre-write the exit ramp (when repair list = 0, baseline retires, fail-closed is safe). The authority discipline is the other half: a lane may build and run the gate, but the consequential flip (reddening `main`) is NEVER the lane's unilateral call — "hand a working gate and a decision, not a red main you decided alone." Operational tricks: make the gate live inside the existing test runner (zero workflow edits), assert known-bad still fails (repairs announced, not silent), and prove backfills in temp-file simulation before touching real state. Related: SN-0236 (one repair per inherited RED class), SN-0240 (classify reds before healing), SN-0249 (specimen must pass its own gate), SN-0250 (green run ≠ sound registry — the drift detector is this gate's permanent R8 form).

## MACHINE NOTE
```json
{
  "sn": "SN-0285",
  "title": "The Ratchet: Block New Drift Without Reddening Main on Legacy Debt",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-04",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "RATCHET-ENFORCEMENT"],
  "cousins": ["SN-0236", "SN-0240", "SN-0249", "SN-0250"],
  "evidence": {
    "comments": "#1354 5985291250 (2026-10-04T22:43:08Z) / 5985343389 (2026-10-04T22:54:51Z)",
    "branch": "coda1/sn002-conformance-gate, commit e5055153e, 15/15 tests green",
    "baseline": ".naya/conformance-baseline.json — named/dated/attributed grandfather list",
    "repair_list": "governance_key_repair_pending: SN-002, SN-016, SN-020, SN-021, SN-022 (proven: flips all five green, zero residual)"
  },
  "pattern": "new-rule + legacy-debt -> ratchet: grandfather named legacy (reported, not blocking); block all new non-conformance; structural tests (blocks-new, baseline-never-grows, retirable-when-fixed); written-in exit ramp; consequential flip stays the director's decision",
  "rules": [
    "neither --check-only (blocks everything on legacy) nor --report-only (advisory, missed SN-020/021/022) is honest",
    "a ratchet that can grow is a permanent exemption wearing a ratchet's name — prove it blocks with a load-bearing test",
    "hand a working gate and a decision, never a red main you decided alone",
    "assert known-bad still FAILs so repairs are announced, not silent",
    "prove backfills in temp-file simulation before touching real state"
  ],
  "durable_test": "A cold Naya introducing a new conformance rule will (1) enumerate legacy failures by name, (2) grandfather them dated/attributed, (3) block new ones in CI, (4) prove the block with a dedicated test, (5) leave the reddening-main flip to the director."
}
```
