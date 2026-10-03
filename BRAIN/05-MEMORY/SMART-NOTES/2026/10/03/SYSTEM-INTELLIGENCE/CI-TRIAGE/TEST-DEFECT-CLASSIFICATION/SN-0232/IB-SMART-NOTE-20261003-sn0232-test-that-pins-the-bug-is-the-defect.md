# The Test That Pins the Bug Verbatim Is the Defect — Re-pin the Test to the Governed Contract

**Intelligent Block:** IB-SMART-NOTE-20261003-sn0232-test-that-pins-the-bug-is-the-defect
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-03
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Naya 4 self-build sign-out #554 comment 5973067795 (2026-10-03T20:14:14Z) — H8-7R repair cycle EXECUTED and PROVEN; branch `naya4/h87-applicability-governed-registry`, commits `25c424b2` (repair) + `69ab414e` (test repair); PR #1347 open, unmerged. Extends SN-0225 (the bug) and SN-0231 (the repair design).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The H8-7 repair (SN-0231) closed the gamable string-keyed classifier at source — but the legacy test fought the repair: the old test pinned the buggy classification triplets **verbatim**, so correct repaired behavior "failed." The test wasn't a safety net; it was a fossil of the bug. The cycle classified the TEST as the defect (TEST DEFECT) and re-pinned it to the governed contract: adversarial trigger words -> UNKNOWN, declared+registered -> APPLICABLE, unregistered filtered, malformed -> UNKNOWN.

Why this is brain-grade: test suites calcify intent over time. A green suite that pins buggy behavior actively *blocks* the repair — and the repairer under time pressure is tempted to weaken a proven-correct repair to satisfy a wrong test. Naming the test the defect flips the investigation order. Test-first-suspect holds when (a) the test asserts exactly the behavior the bug report falsifies, and (b) the repair's controls are independently green (here: deno check on the full shipped edge function green, 14/14 Deno-executed behavior matrix on the shipped helper verbatim, non-vacuous negative control on pre-repair code). Rule for a cold successor: **never weaken a proven-correct repair to fit a pinned test; re-pin the test to the contract, and let the contract be the executable spec** — the 14/14 matrix pins the contract, not folklore. A test that locks buggy behavior is a bug wearing a passing CI badge.

## 🩷 HUMAN NOTE

Shawn — H8-7R repair executed and proven (PR #1347, unmerged; the merge stays yours). One sharp lesson I'm banking: the old test had the *buggy* behavior pinned in verbatim, so it "failed" the correct repair. We classified the test itself as the defect and re-pinned it to the governed contract. Rule of thumb: a green test that pins buggy behavior is a bug wearing a passing badge — suspect the test before you weaken the repair.

## 🟣 CHILD NOTE

Remember the gamable-clerk fix (SN-0231)? The repair worked — but an old test screamed "FAIL!" Not because the repair was wrong, but because the test had the *old, buggy* answers written in ink. Like a quiz whose answer key is wrong: the student who finally gets it right will "fail." So we did the brave thing: we declared the answer key the defect, and wrote a new one from the rulebook (the governed registry). Lesson: when the rules change for the better, check whether the old quiz is grading against the old rules — fix the quiz, not the student.

## 👵 GRANDMA NOTE

The bug fix for the gamable classifier was correct — but the old test called it "failed." The test wasn't protecting anyone; it had the buggy behavior baked in word for word, like an old recipe card for a cake that never rose. Instead of ruining a good new recipe to match the bad card, the team threw out the bad card and wrote a new one from the rulebook. The lesson: a passing test can itself be the defect. When a proven repair collides with an old test, question the test first.

## 🤖 NAYA NOTE

H8-7R repair cycle EXECUTED AND PROVEN (CANDIDATE note on the repair-cycle mechanics; the merge itself is Shawn's gate). Source: Naya 4 self-build sign-out #554 5973067795 (2026-10-03T20:14:14Z), branch `naya4/h87-applicability-governed-registry`, commits `25c424b2` (repair) + `69ab414e` (test repair), main pin `5b68f8dc`; PR #1347 open/non-draft/unmerged. The repair closed the adversarial seam at source per SN-0231 (closed TASK_CLASS_REGISTRY, text triggers downgraded to proposals, APPLICABLE requires a provenance-attested declaration ∈ the registry, else UNKNOWN with TEXT_TRIGGER_WITHOUT_GOVERNED_DECLARATION, fail-closed; existing relationship rows untouched). Proof shape: `deno check` green on the full shipped edge function; 14/14 Deno-executed behavior matrix on the shipped helper (verbatim); non-vacuous negative control on pre-repair code (adversarial text -> APPLICABLE); CI red = pre-existing base-pin brain-index drift, fails identically at the pin, heals when #1343 merges. The lesson captured here is orthogonal to the repair: the legacy test pinned the buggy triplets verbatim and had to be re-pinned to the governed contract (commit 69ab414e) — classified TEST DEFECT. Test-first-suspect condition: the test asserts exactly the behavior the bug report falsifies AND the repair's controls are independently green → the test is the suspect, not the repair. Remaining holes (from the sign-out): `declared_task_classes` has no writer yet (future H8-5/H15 territory); #1347 touches the same file as #1345 (H13, unmerged) — rebase-if-first-lands. Cousins: SN-0225 (the confirmed bug), SN-0231 (the repair design), SN-0072 (self-inflicted XPASS — the verifier's own artifact as the failure), SN-0118 (a crash is not a verdict — don't blame the artifact), SN-0061 (non-vacuous negatives), SN-0224 (full-scope proof doctrine the repair followed). Naya 2 relay 5973182115 live-verified PR #1347's claims (open/non-draft/mergeable true, head == branch ref, CI red = pre-existing base drift only) — folded as corroborating evidence, not a standalone note (doubt rule).

## ⚙️ MACHINE NOTE

{"sn": "SN-0232", "title": "The Test That Pins the Bug Verbatim Is the Defect — Re-pin the Test to the Governed Contract", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-03", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "TEST-DEFECT-CLASSIFICATION"], "cousins": ["SN-0225", "SN-0231", "SN-0072", "SN-0118", "SN-0061", "SN-0224"], "evidence": {"sign_out": "#554 comment 5973067795 (2026-10-03T20:14:14Z) — H8-7R repair cycle, branch naya4/h87-applicability-governed-registry, commits 25c424b2 (repair) + 69ab414e (test repair), main pin 5b68f8dc", "corroboration": "#554 comment 5973182115 (Naya 2 relay) — PR #1347 live-verified: open/non-draft/mergeable, head == branch ref, CI red = pre-existing base-pin drift only", "proof_shape": "deno check green on full shipped edge function; 14/14 Deno behavior matrix on shipped helper; non-vacuous negative control on pre-repair code"}, "rule": "when a proven-correct repair collides with an old test, suspect the test first: if the test asserts exactly the behavior the bug report falsifies and the repair's controls are independently green, classify the test as the defect and re-pin it to the governed contract — never weaken the repair to fit a pinned test"}
