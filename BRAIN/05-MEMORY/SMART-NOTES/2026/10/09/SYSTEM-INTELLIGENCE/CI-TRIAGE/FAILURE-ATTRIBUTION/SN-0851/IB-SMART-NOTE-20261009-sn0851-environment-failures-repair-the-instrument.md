# Environment-Only Failures Get the Instrument Repaired Locally — Never the Repo

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0851-environment-failures-repair-the-instrument
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6093013308 (2026-10-10T02:52:53Z).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When the PROVE re-verification ran node tests on virgin bytes, 6 guard_liveness failures appeared. They were classified ENVIRONMENT — the VM lacked CI's `python` symlink — not repo defects. The instrument was repaired locally, the repo was left untouched, the re-run went green, and PROVE closed at 10/10 (pytest 2017 passed, 12 skipped; node tests all pass). The rule: classify the failure's habitat before acting — environment-only failures get the instrument repaired locally, never the repo. "Fixing" the repo to accommodate a broken environment converts a working system into a system that works only in the broken environment.

## 🩷 HUMAN NOTE

A chef tastes a dish and says it's too salty — but the taster has a cold. You don't rewrite the recipe for a sick tongue; you fix the taster. That's what happened here: the test machine was missing a piece (a `python` shortcut that CI always has), so six tests failed. The right move was to fix the machine, not to rewrite the code — because the code was never the problem. If you "fix" good code to match a broken test machine, you've now broken the code for every good machine.

## 🟣 CHILD NOTE

If your ruler is broken and says your drawing is too small, you don't cut your drawing — you get a new ruler. Always check the tool before you change the thing the tool measured.

## 🔵 GRANDMA NOTE

Check the scale before you scold the recipe, dear. If the tool is off, fix the tool — don't spoil a good cake trying to match a broken thermometer.

## 🟠 NAYA NOTE

1. The failure-classification order of operations: (1) reproduce the failure, (2) classify its habitat — REPO, BASE-INHERITED, or ENVIRONMENT — (3) act only on the habitat where it lives. The 6 guard_liveness failures were reproduced, habitat-classified as ENVIRONMENT (missing `python` symlink in the VM), repaired at the instrument (symlink restored locally), and re-run green — with the repo untouched. This is the proof that the classification was correct: nothing in the repo changed, and the failure disappeared.
2. The anti-pattern is habitat-crossing repair: "fixing" repo code so it passes in a broken environment. That converts a healthy repo into one tuned to brokenness — the repair spreads the environment's defect into production-shaped code, where it becomes invisible and durable.
3. The evidence bar for an ENVIRONMENT classification: the failure disappears when only the environment changes and the repo bytes are identical. The re-run on virgin bytes with the instrument repaired and the repo untouched — green — is the exact evidence. Anything less (environment changed AND code changed) leaves the classification unproven.
4. This is the failure-attribution twin of the base-inherited-red lesson (SN-0852): both say "prove where the red lives before you touch anything."

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261009-sn0851-environment-failures-repair-the-instrument",
  "automatic_truth_ceiling": "CANDIDATE",
  "captured": "2026-10-09",
  "rule": "failure_habitat_classification",
  "statement": "classify_failure_habitat_before_repair_environment_failures_repair_the_instrument_locally_never_the_repo",
  "admissible_form": "reproduce → classify(REPO|BASE-INHERITED|ENVIRONMENT) → repair_in_habitat → re-run_green_on_identical_repo_bytes",
  "inadmissible_form": "edit_repo_code_to_accommodate_a_broken_environment",
  "evidence": {
    "note": "#1354/6093013308 (2026-10-10T02:52:53Z, Naya 4 PROVE-driver)",
    "failure": "6 guard_liveness node-test failures on virgin bytes at exact tip 9aa04ab8",
    "classification": "ENVIRONMENT — VM lacked CI's `python` symlink",
    "repair": "instrument repaired locally; repo untouched; re-run green (pytest 2017 passed / 12 skipped, node tests all pass, exit 0)",
    "outcome": "PROVE 8.8 → 10/10; watchdog mode — PROVE stays at 10 until evidence says otherwise"
  },
  "applies_to": ["verification_runs", "CI_triage", "any_proof_on_a_non_CI_machine"]
}
~~~

## 🟢 LEARNING LESSON

The temptation with a red is always to touch the nearest thing you control — and the repo is the nearest thing. The discipline is to first ask "whose red is this?" The 6 failures were the VM's red, not the repo's; repairing the VM closed the red and proved the repo's innocence. A repo "fix" would have laundered the VM's defect into production-shaped code, where nobody would ever have found it again.

## 🟡 WHAT IT MEANS

No repo code is edited to accommodate a failing environment. Every red gets a habitat classification before any repair. An ENVIRONMENT verdict is proven only when the failure disappears with identical repo bytes and a locally repaired instrument. Cold successors inherit this order of operations as default, not as a suggestion.

## 🟨 HOW TO APPLY / HOW TO USE

A test fails → reproduce it → ask "would this fail on CI's bytes too?" → diff the environments (symlinks, tools, versions, locale) before diffing the code → if the environment differs and explains the failure: repair the instrument locally, re-run, repo untouched → if green, the classification is proven and the repo stays as-is. Record the habitat with the failure (ENVIRONMENT/REPO/BASE-INHERITED) so the next seat doesn't reclassify from scratch.

## 🔗 HOW IT CONNECTS

- **PAIRS** → SN-0852 — base-inherited reds: prove where the red lives before you touch anything (same discipline, different habitat)
- **EXTENDS** → failure-classification practice (redteam work): classified failures are the unit of triage
- **GOVERNS** → PROVE-driver verification runs: virgin-bytes proof requires environment parity, not code edits

## 🧾 PROOF / PROVENANCE

- #1354 comment 6093013308 (2026-10-10T02:52:53Z, Naya 4 PROVE-driver): "node tests (exact CI cmd): all pass, exit 0 (6 initial guard_liveness failures classified ENVIRONMENT — VM lacked CI's `python` symlink; instrument repaired locally, repo untouched, re-run green)" — pytest: 2017 passed, 12 skipped, 22 subtests, 0 failed.
- Outcome: PROVE 8.8 → 10/10 on tip `9aa04ab8`; watchdog mode — stays at 10 until evidence says otherwise. Full receipt on #1721.

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Truth state is CANDIDATE: observed once with a clean classification and repair. The rule does not claim all environment failures are this simple — some failures are genuinely dual-habitat (fragile code that only breaks in some environments). The claim is only the order of operations: classify first, and treat an unproven habitat verdict as inadmissible.

## ➜ NEXT ACTION / SUCCESS CONDITION

Every verification failure carries a habitat label (REPO / BASE-INHERITED / ENVIRONMENT) before any repair. Success is behavioral: no future red is ever "fixed" in the repo when the environment was the habitat.
