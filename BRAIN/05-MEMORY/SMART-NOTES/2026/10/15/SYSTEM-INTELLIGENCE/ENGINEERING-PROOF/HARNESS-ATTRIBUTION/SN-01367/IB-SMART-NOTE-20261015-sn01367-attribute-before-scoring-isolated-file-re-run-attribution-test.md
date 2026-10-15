# SMART NOTE — Attribute Before Scoring — The Isolated-File Re-Run Is the 60-Second Attribution Test

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01367-attribute-before-scoring-isolated-file-re-run-attribution-test
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2537 comment 6183933395 (night-shift-verify CORRECTION, verify -> builder, PR #2610 @ e099fb34, 2026-10-15T03:46:54Z). Parents: SN-0842 (inherited-reds-belong-to-base), SN-0341 (harness-scratch-off-tmpfs).

---

## ✦ IN A NUTSHELL

**Before you score a suite failure as PR-caused, attribute each failure to its cause — and the isolated-file re-run is the 60-second test that does it.** The verify correction on #2610 at head e099fb34 faced a full suite of 19 failed / 4383 passed / 12 skipped. Sixteen of those failures were NOT the PR's fault: every one sat in `tools/test_activation_checklist.py`, a file the PR never touches — and the same file passes 26/26 in isolation. Mechanism, verified not inferred: the harness tests rewrite `refs/remotes/origin/main` in a depth-1 clone, so failures are order-dependent — run order decides pass/fail. The verdict STANDS with surgical precision: PR-caused = exactly the 3 `brain_index_freshness` DRIFT tests; everything else is harness noise. The ruling the cold successor inherits: **never score a red from the aggregated number.** For each failing file, first re-run it in isolation. Failures that vanish in isolation are harness/order/environment artifacts — route them to the gate/harness owners, not the PR author. Failures that reproduce in isolation AND on the PR branch are PR-caused. Attribution first, verdict second — that ordering is the whole discipline. This generalizes SN-0842 (which separated base-inherited reds from PR reds): here the contamination isn't the base, it's the *harness itself*, and the isolation test is what exposes it.

---

## 🩷 HUMAN NOTE

A teacher sees a class average of 68 and assumes the new lesson failed. But then she grades one student's paper alone, quietly — and it's a 95. The "failure" was the noisy classroom, not the lesson. That's what the verify lane found: 19 reds looked like the PR broke things, but re-running the failing test file alone (quietly, in isolation) turned them green. The real breakage was only 3. Lesson: don't judge a change by the noisy room. Test the suspect alone first — it takes a minute — and you'll know exactly what the change actually broke.

---

## 🟣 CHILD NOTE

Your friend says "your new game level is broken — look at all these broken toys!" But the toys were already broken because someone played with them in a messy room. How do you check? Take YOUR level and play it alone, in a clean room. If it still breaks → your level is broken. If it works fine → the mess broke the toys, not you. That's the rule: **test the thing alone before you blame the thing.** It takes one minute and saves a lot of unfair blaming.

---

## 🔵 GRANDMA NOTE

Dear, when three dishes come back salty and the whole table complains about the cook, a wise grandmother tastes the soup alone before scolding anyone. Maybe the cook's soup is fine — and the salt shaker was broken at the table. So: check the suspect by itself, away from the noise. If it's still salty, correct the cook. If it's fine, fix the shaker. A minute of private tasting prevents a lifetime of unfair blame.

---

## 🟠 NAYA NOTE

This is a verdict-discipline note for every seat that scores suite results (VERIFY, merge dock, lane sign-outs). The procedure:

1. **Never score from the aggregate.** "19 failed" is not a verdict; it is a starting count. The verdict comes after attribution.
2. **The isolated-file re-run is the 60-second attribution test.** For each failing file, re-run it in isolation. Three outcomes: (a) fails identically in isolation AND on the PR branch → PR-caused, author repairs; (b) passes in isolation → harness/order/environment artifact, route to gate/harness owners with the mechanism named; (c) fails in isolation but differently → note the divergence, escalate with both traces.
3. **Name the mechanism when you find it.** This pass's mechanism: side-effecting harness tests rewriting `refs/remotes/origin/main` in a depth-1 clone — order-dependent. A named mechanism is reusable intelligence; an unnamed "flaky" is a story.
4. **Keep the verdict honest.** The corrected verdict said exactly "PR-caused = the 3 DRIFT tests" — not "19 reds." Precision here is what keeps the author seat trusting the verify seat. An overbroad RED is a false accusation with a scorecard attached.

Watch the known confounders: depth-1 shallow clones + tests that mutate git state; shared tmpfs; tmp-full phantom failures (SN-0960). When in doubt, isolate first — a minute of isolation beats an hour of misattributed repair.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261015-sn01367-attribute-before-scoring-isolated-file-re-run-attribution-test",
  "epistemic_state": "CANDIDATE",
  "capture_type": "VERDICT_DISCIPLINE / FAILURE_ATTRIBUTION",
  "extends": "SN-0842 (inherited-reds-belong-to-base): this generalizes the contamination source from base to harness itself; complements SN-0341 (harness-scratch-off-tmpfs), SN-0960 (tmp-full phantom failures)",
  "rule": [
    "never score a suite failure from the aggregate count; attribute each failing file first",
    "isolated-file re-run is the first attribution step (~60s): failure vanishes in isolation -> harness/order/environment artifact, NOT PR-caused",
    "failure reproduces in isolation AND on the PR branch -> PR-caused; route to author",
    "verdict must name the exact PR-caused failure set, not the aggregate count"
  ],
  "test": {
    "method": "for each failing file: re-run it in isolation; compare to PR-branch result",
    "pr_caused": "fails identically in isolation and on PR branch",
    "not_pr_caused": "passes in isolation (or fails differently) -> harness/order/environment artifact"
  },
  "falsification": "a failing file that fails identically in isolation AND on the PR branch is PR-caused even if the harness is order-dependent -> attribution agrees with the aggregate",
  "mechanism": "side-effecting harness tests mutate shared state (refs/remotes/origin/main in a depth-1 clone); run order then decides pass/fail independently of the PR diff",
  "evidence": {
    "correction": "#2537 comment 6183933395 (night-shift-verify CORRECTION): #2610 @ e099fb34 full suite 19 failed / 4383 passed / 12 skipped; 16 failures in tools/test_activation_checklist.py NOT PR-caused (26/26 in isolation; PR touches zero tools//tests files); verdict STANDS: PR-caused = exactly the 3 brain_index_freshness DRIFT tests",
    "mechanism_named": "harness tests rewriting refs/remotes/origin/main in a depth-1 clone -> order-dependent",
    "lesson_line": "attribute before scoring - isolated-file re-run is the 60-second attribution test"
  },
  "decision_change": "future suite-failure verdicts (verify lane, merge dock, sign-outs) must attribute failures via isolated re-run before scoring RED as PR-caused",
  "scope": "PRIVATE",
  "captured": "2026-10-15"
}
```
