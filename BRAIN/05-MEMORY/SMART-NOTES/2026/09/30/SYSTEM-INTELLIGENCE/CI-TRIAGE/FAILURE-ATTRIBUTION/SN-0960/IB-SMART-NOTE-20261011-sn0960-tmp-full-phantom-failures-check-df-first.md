# SN-0960 — A Full /tmp Makes Mass Phantom Test Failures: Check Disk Before You Debug Code

- **Intelligent Block:** IB-SMART-NOTE-20261011-sn0960-tmp-full-phantom-failures-check-df-first
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-11
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** night-shift-2026-10-10, worker t0052-a (tick t0052, 2026-10-11 ~00:52 PDT) — scores.jsonl note: "-2 per own deduction: two wasted runs before catching /tmp 100% full (174 phantom failures) — check df first"; receipt `receipts/t0052-a.md` (score 8).

## IN A NUTSHELL

Worker t0052-a ran a local pytest repro and got **174 phantom failures** — two full wasted runs diagnosing them before discovering `/tmp` was 100% full. Freed disk, failures vanished. The rule for every cold successor: when mass test failures appear with no code change and no coherent failure pattern, `df -h /tmp` (and `/`) is the FIRST command, before any code-level debugging. Disk exhaustion makes pytest, tempdir fixtures, and build tooling fail in bizarre, numerous, patternless ways that look exactly like a broken tree. Environmental check first, code diagnosis second — this is the environment side of the SN-0894 classification discipline.

## HUMAN NOTE

It's like trying to bake and every recipe fails — not because the recipes are wrong, but because someone filled your kitchen with boxes and there's no counter space left. You can re-read every recipe twice (t0052-a did), or you can look at the kitchen first. `df` is looking at the kitchen. When hundreds of tests fail at once for no reason, the oven isn't broken — the room is full.

## CHILD NOTE

Imagine your toy box is completely stuffed and you keep trying to put more toys away — everything keeps falling out, and it looks like all the toys are broken. They're not broken; the box is full. Before you decide all 174 toys are broken, check if the box is full. That's `df` — checking if the box is full.

## GRANDMA NOTE

It's like the washing machine stopping mid-cycle and flashing every error light at once. You could call the repairman for each light — or you could check whether the drain hose is just kinked. A full disk is the kinked hose: one simple blockage, a hundred alarming symptoms. Check the simple thing first.

## NAYA NOTE

Apply this every time a test run produces mass, patternless failures (hundreds failing, nothing changed in the code): (1) run `df -h /tmp /` BEFORE opening any test file or rerunning with flags — if /tmp is at 100%, stop, free space, rerun; (2) do NOT spend a run "diagnosing" phantom failures — t0052-a's honest -2 deduction is the cost of skipping step 1; (3) when the failures vanish after freeing disk, record that the tree was never broken — a false "the tree is broken" narrative in receipts or on the board is how phantom failures compound into real wasted work for the next lane; (4) on shared/VM workers, /tmp fills silently from earlier runs' worktrees and logs — cleanup is part of the shift, not an afterthought.

## MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "environmental_phantom_failures_from_disk_exhaustion",
  "evidence": {
    "receipt": "night-shift-2026-10-10/receipts/t0052-a.md (score 8) — local pytest repro at pinned head 9a9954bc8886",
    "score_note": "scores.jsonl t0052-a: '-2 per own deduction: two wasted runs before catching /tmp 100% full (174 phantom failures) — check df first'",
    "observation": "174 failures, patternless, no code change; vanished when /tmp freed"
  },
  "rule": "mass_patternless_test_failures_with_no_code_change_means_check_disk_first",
  "procedure": [
    "on mass patternless test failures with no code change, run 'df -h /tmp /' FIRST, before any code debugging",
    "if /tmp is at 100%, free space and rerun — do not diagnose the phantom failures",
    "record that the tree was never broken when failures vanish after freeing disk — never leave a false broken-tree narrative",
    "treat /tmp cleanup as part of the shift on shared workers; earlier runs' worktrees and logs fill it silently"
  ],
  "related": ["SN-0894 (classify environment before touching product code)", "SN-0961 (duplicate-basename collection crash — the tree-side mass failure)", "SN-0962 (local repro at exact head — also catches environment confounds)"]
}
~~~
