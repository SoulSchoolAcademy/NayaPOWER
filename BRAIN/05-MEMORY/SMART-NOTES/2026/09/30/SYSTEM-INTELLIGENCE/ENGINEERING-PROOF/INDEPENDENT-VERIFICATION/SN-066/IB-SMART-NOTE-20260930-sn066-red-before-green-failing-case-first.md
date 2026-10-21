# Red Before Green — Publish the Failing Case on the Frozen SHA

**Intelligent Block:** IB-SMART-NOTE-20260930-sn066-red-before-green-failing-case-first
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** PR #1216 comment 5934329483 (Naya-4 RED, 2026-10-01T15:12:10Z) — RED-1 published on the frozen candidate SHA before any fix; test at ~/workspace/kernel-red/repo/test_red1_shared_calculator_decides.py; per the Master Execution Directive (2026-10-01 ~08:07 PDT, #554 comment 5934257584).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A green test that never failed is not proof of a fix — it is proof of a green test. Under the Master Execution Directive, the first failing integration case (RED-1) was published BEFORE any fix, on the frozen SHA: EVOLVE's public `propose → evaluate` path never invokes the shared executable calculator (`kernel/value_calculus.py`) — the score is computed locally (`score = value - risk`) while the receipt binds `deciding_config_hash` and `calculusConfigHash: CALCULUS_V21_SPEC_HASH` with `calculus_spec_status: "RATIFIED"`. The spy test FAILS on the genuine red assertion at frozen SHA `42eb0e0c34bafa851d6d5bc124d5f23612240443` (PR #1216 head at publish time, setup clean). The builder's standing instruction completes the discipline: turn it green by wiring — or explicitly fence it as PROVISIONAL, in which case the test STAYS RED on the fence; never fake it green. The lesson has three parts, and all three must hold for the receipt to mean anything: (1) publish the red first, at a frozen SHA, before any fix is attempted — the later green is then provably a fix, not an assertion; (2) pin the SHA at publish time — a red that floats with the tip proves nothing about what the fix changed; (3) the fence is red, not green — a provisional fence that keeps the test red is honest; a provisional fence that flips the test green is asserted≠verified (SN-016 family). This is how the nine-node runtime work keeps its evidence chain honest: every integration fix begins as a published red.

## 🩷 HUMAN NOTE

An engineer says "I fixed the leak — the test is green." You ask one question: "Was it ever red?" If the test never failed, the green proves the test runs, not that the leak existed or is gone. The discipline that fixes this is red-before-green: write the failing test first, publish it, pin the exact version of the code it failed against, THEN fix. After the fix, the green means something — it was red ten minutes ago, on this exact code. There's a trap on the other side too: if you can't fix it properly yet and fence the feature as "provisional," the test stays red. A red test behind a provisional fence is honest work; a green test behind a provisional fence is a lie with a label. Green that was never red is a decoration.

## 🟣 CHILD NOTE

Imagine you want to prove you can fix a broken flashlight. First, you show everyone the flashlight is broken — you click it, and nothing happens. You write down "this exact flashlight, today, doesn't light up." THEN you fix it, click it again, and it lights up! Now everyone believes you fixed it, because they saw it broken first. But if you never show it broken and just say "it works now," how do they know it was ever broken? And here's the important rule: if you can't really fix it yet and you put a "TEMPORARY" sticker on it, the flashlight stays "broken" in the book. You never write "fixed!" next to a TEMPORARY sticker. Broken-first makes the fix real.

## 🔵 GRANDMA NOTE

It's like a before-and-after photo for a recipe change. If you only show the "after" photo — the beautiful cake — nobody knows the old recipe was bad or that your change did anything. You take the "before" photo first: the flat cake, dated today, with the exact recipe version written on the card. Then you bake the new one. The pair is the proof. And if you're not ready to fix it properly and you put the old recipe card in an envelope marked "needs more work," you don't then file the "after" photo as a success — the envelope means it's still not done. The before-photo comes first; the "needs work" envelope stays unsealed until the work is actually done.

## 🟠 NAYA NOTE

Apply this at the start of every integration repair under a directive: (1) reproduce the failure on the frozen head SHA and publish the failing test (path, SHA, assertion) on the relevant PR BEFORE any fix attempt — the receipt's red is the baseline; (2) pin the SHA at publish time — record the exact head (here `42eb0e0c…` on PR #1216) in the comment so a later green can be diffed against the red on identical bytes; (3) builder contract: turn it green by wiring the real fix, or explicitly fence as PROVISIONAL — on a fence the test stays red; a provisional fence with a green test is asserted≠verified and is never accepted; (4) a spy test that FAILS on a clean setup is the evidence the setup isn't the thing failing — note the setup-clean verification in the red comment, or the red proves nothing; (5) one red per defect: RED-1 covers the propose→evaluate calculator invocation path — don't let it sprawl into the other forward gaps (SN-064's ACT deliberative functions, LEARN's direct-assignment) — each gap gets its own red; (6) this is the Master Execution Directive's priority-queue mechanics made concrete: "runtime path + failing case" first, because the failing case is the acceptance criterion for everything after it.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "test_never_red_is_not_proof_of_fix",
  "evidence": {
    "board": ["PR #1216 comment 5934329483 (2026-10-01T15:12:10Z) — Naya-4 RED"],
    "directive": "Master Execution Directive 2026-10-01 ~08:07 PDT (#554 comment 5934257584) — priority 1: runtime path + failing case",
    "frozen_sha": "42eb0e0c34bafa851d6d5bc124d5f23612240443 (PR #1216 head at publish time; branch head still this SHA at publish)",
    "failing_case": "EVOLVE propose->evaluate never invokes kernel/value_calculus.py; score computed locally (score = value - risk) while receipt binds deciding_config_hash + CALCULUS_V21_SPEC_HASH (RATIFIED)",
    "test": "~/workspace/kernel-red/repo/test_red1_shared_calculator_decides.py — spy test FAILS on the genuine red assertion; setup verified clean",
    "builder_contract": "turn it green by wiring, or fence as PROVISIONAL with the test staying red — never fake it green"
  },
  "rule": "red_before_green_failing_case_first",
  "procedure": [
    "publish the failing test on the relevant PR before any fix, pinned to the frozen head SHA",
    "verify the setup is clean so the red is genuine, and state that in the red comment",
    "builder: wire the real fix to turn it green, or fence as PROVISIONAL with the test staying red — a provisional fence with a green test is asserted-not-verified and is rejected",
    "one red per defect; do not let a failing case sprawl across gaps"
  ],
  "related": ["SN-061 (post-merge verification at the pin — non-vacuous negatives; the test-family discipline)", "SN-063 (receipt provenance — the defect RED-1 captures: binding without deciding)", "SN-016 (asserted≠verified — the law the fence-is-red rule enforces)", "SN-064 (spec-outruns-kernel — the other forward gaps each get their own red)"]
}
~~~
