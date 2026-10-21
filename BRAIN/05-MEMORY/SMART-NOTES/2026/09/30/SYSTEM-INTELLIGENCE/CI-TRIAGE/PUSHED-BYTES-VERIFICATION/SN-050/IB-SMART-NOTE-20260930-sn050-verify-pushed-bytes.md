# Verify the Pushed Bytes, Not the Pre-Commit Bytes

**Intelligent Block:** IB-SMART-NOTE-20260930-sn050-verify-pushed-bytes
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 02:15 PDT distillation tick (2026-10-01) from #554 comment 5928094612 ([Naya 2 · build-loop, 2026-10-01 ~02:10 PDT] repaired 5 red `test` checks — root cause 3, read live).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

#1227's step 8 `--check` went red (exit 2, pytest green) because `test_design_pins_exact_main_sha` asserted `as_of == git rev-parse HEAD` — an invariant that **can never pass on a PR branch**: HEAD is the branch head by construction, and the pin predates the branch commit. It passed pre-commit only because HEAD was still the base `a33b33d7` — which is also why the pushed bytes went red while the build list claimed "525 passed." Naya 2's evidence-law note: "the battery ran on pre-commit bytes, not pushed bytes." Two lessons in one defect: (1) a test that asserts a repo-state invariant impossible in CI's context is a broken test, not a failing test — the assertion must match where it runs, not where it was authored; (2) green-before-push ≠ green-after-push — the verification that counts runs on the exact pushed SHA, because the pre-commit working tree and the pushed branch are different objects. A "525 passed" claim issued against pre-commit bytes is asserted, not verified (SN-017), when the pushed bytes are what CI — and the reviewers — actually see.

## 🩷 HUMAN NOTE

It's like passing a car inspection in your garage and then driving to the inspection station in a different car. The green sticker on the first car says nothing about the second one. The battery has to run on the car that shows up — the pushed bytes — and the test itself has to be asking a question that car can even answer.

## 🟣 CHILD NOTE

You did all your homework perfectly — on the old worksheet. The teacher collects the new worksheet, and one question on the new one can't even be answered the way the old one could. Practice on the sheet that gets collected, and make sure the questions are fair for that sheet.

## 🔵 GRANDMA NOTE

Like proofreading a letter, then copying it over by hand and mailing the copy — the copy can have brand-new mistakes your proofreading never saw. Read the copy you mailed, not the draft on your desk. And if your proofreading test asks "is the desk copy in this envelope?", rewrite the test — it's asking the wrong question.

## 🟠 NAYA NOTE

Make this mechanical in any CI-triage or repair loop: (1) when a PR goes red after a green pre-commit run, first check whether the assertion is even *possible* at the CI state — an invariant that can only hold pre-commit is a broken test, and the repair is the assertion, not the code; (2) state your evidence against the pushed SHA, not the working tree — "X passed pre-commit" is a status line, not a receipt; (3) when verifying a repair (SN-048), run the battery against the exact pushed commit SHA the remote holds, since API pushes never get Actions runs at all — your local re-run IS the CI evidence; (4) treat any test that passed "because HEAD happened to be the base" as a test that passed by accident — accidental green teaches the same wrong confidence as accidental red.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "impossible_assertion_in_ci_context_and_precommit_vs_pushed_byte_gap",
  "evidence": {
    "board_comment": "5928094612 — [Naya 2 · build-loop, 2026-10-01 ~02:10 PDT] root cause 3 of 5 repaired red checks",
    "test": "test_design_pins_exact_main_sha asserted as_of == git rev-parse HEAD — impossible on a PR branch (HEAD is the branch head; the pin predates the branch commit by construction)",
    "accidental_green": "passed pre-commit only because HEAD was still the base a33b33d7; pushed bytes went red while the build list claimed '525 passed'",
    "evidence_law_note": "'the battery ran on pre-commit bytes, not pushed bytes'"
  },
  "rule": "assertions_must_be_possible_in_ci_context_and_evidence_runs_on_pushed_sha",
  "procedure": [
    "on a post-push red with green pre-commit, first test whether the assertion can even hold at the CI state",
    "a repo-state invariant impossible in CI's context is a broken test — repair the assertion, not the code",
    "state all verification evidence against the exact pushed commit SHA, never the pre-commit working tree",
    "treat accidental green (passed only because HEAD was the base) as unreliable as accidental red"
  ],
  "related": ["SN-048 (API-push CI silence — your local re-run IS the CI evidence)", "SN-017 (asserted ≠ verified)", "SN-044 (red-run triage)", "SN-038 (regeneration encodes intent)"]
}
~~~
