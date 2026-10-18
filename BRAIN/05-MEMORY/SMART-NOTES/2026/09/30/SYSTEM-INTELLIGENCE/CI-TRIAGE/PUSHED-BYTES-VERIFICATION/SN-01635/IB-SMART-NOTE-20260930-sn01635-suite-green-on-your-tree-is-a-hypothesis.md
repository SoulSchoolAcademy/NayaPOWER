# Suite Green on Your Tree Is a Hypothesis — Run the Fresh Tree Before You Push

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01635-suite-green-on-your-tree-is-a-hypothesis
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A green suite on your dev tree is evidence about your dev tree, not about the commit. On breaker #12 (feature.naya_answers), the dev-tree pytest passed and the lane pushed — and the fresh tree then caught 3 REAL failures: tests using `naya_answers` as their "still specified" example (rotated to `feature.scheduler` per the tests' own rule). The defect reached a published head; the fix was amend + fresh-verify + force-push + re-verify (clumsier than amend-before-push). Root cause: the dev tree masked stale example tests. The standing rule, adopted by the lane itself in the receipt: fresh-tree-before-push. The suite runs on a pristine worktree at the pinned head; the push proceeds only on fresh-tree green. Your tree is the lab you cooked in — the fresh tree is the restaurant's kitchen.

## 🩷 HUMAN NOTE

A chef tastes the soup in her own pot all day and serves it confidently — but her pot has been warming on the same burner for hours, hiding a burnt spot. The first guest with a clean spoon finds it immediately. That's the breaker #12 incident: the dev tree passed every test, the lane published the commit, and a pristine checkout caught three real failures the dev tree had been masking. The lane fixed it the hard way — amend, re-verify, force-push a published head, re-verify again. The standing rule is now the easy way: cook in your pot all you want, but serve only after the dish has passed in a clean kitchen. The fresh tree is the clean spoon: a pristine worktree at the exact pinned head, full suite, green — then push. One clean-kitchen run replaces a public correction.

## 🟣 CHILD NOTE

Your homework might be right on your own paper — but copy it onto a clean sheet and read it again before you hand it in. The clean sheet shows the mistakes your own paper was hiding. Only hand in the clean copy.

## 🔵 GRANDMA NOTE

You proofread your letter three times at your own desk and it reads fine — because your eyes know what you meant to write. Read it aloud in the kitchen, where it sounds strange and new, and the errors jump out. The fresh tree is the kitchen: same letter, new room, real errors. Always do the kitchen reading before you mail it.

## 🟠 NAYA NOTE

Push-discipline incident (2026-10-18 ~06:35–07:12 PDT window, lane-executor t0840-lane12, breaker #12 feature.naya_answers, receipt 9.5/10): dev-tree pytest passed; the lane pushed; the fresh-tree suite then caught 3 REAL failures — tests using `naya_answers` as their "still specified" example, which the tests' own rule forbids once the feature is built (rotated to `feature.scheduler`). The defect reached a published head (`959ea1154…`): fix was rotate the example, amend, fresh-verify BEFORE push (adopted as the lane's standing rule), re-push, re-verify — with a force-push on a published head (own branch, harmless, but clumsier than amend-before-push). Final state clean: fresh-tree 257/257 at the pinned head, verifier PASSED ×3, consent HONEST, chain 12/14. Cousins: SN-050 (verify pushed bytes — the receiving-side twin: the pusher's bytes are what the world sees); SN-01365 (verify the final artifact, not the intermediate — the dev tree is an intermediate); SN-01632 (verification is read-only — the discipline twin). The new content is the dev-tree masking mechanism: uncommitted state and warmed fixtures make your tree a hypothesis about the commit, and the fresh tree is the check.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01635",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["push", "pre-push-verification"],
    ["suite", "full-suite"],
    ["tree", "dev-vs-pristine"],
    ["risk", "stale-fixture-masking"]
  ],
  "enforcement": "The pre-push gate is mechanical: before any push of a lane's work, the lane runs the FULL verification suite on a PRISTINE worktree checked out at the pinned head (fresh clone or clean worktree — never the dev tree), and the push proceeds only on fresh-tree green. Dev-tree green is a pre-condition, not a gate. The scorer/verifier corroboration rule mirrors it: a verifier that re-runs the suite runs it on the fresh tree at the pinned head, not on the lane's dev tree. A push that skipped the fresh-tree gate and shipped a defect is recorded as a named failure (dev-tree-masking), and the remediation is amend + fresh-verify + re-push — the force-push correction path, not a follow-up commit.",
  "decision_change": "The lane's push decision changes from 'dev-tree suite green → push' to 'dev-tree suite green (hypothesis) → fresh-tree suite at pinned head green (check) → push.' The extra run is not paranoia — the breaker-#12 incident proves the two verdicts can diverge, and the divergence lands on published heads. The ten-candidate-solutions review in the receipt adopted fresh-tree-before-push as the lane's standing rule; the general rule is: any suite verdict that can move the head outward (a push) is taken only on the pristine tree.",
  "falsifiability": "If fresh-tree and dev-tree verdicts never diverge across a sustained window, the extra run is waste and the gate is redundant — the mechanism predicts divergence only where the dev tree accumulates uncommitted state, warmed caches, or fixture drift. The falsifier is a tracked divergence rate: lanes log both verdicts; if the divergence rate stays at zero, the standing rule is demoted to advisory. One divergence (here: 3 real failures) keeps it mechanical.",
  "mechanism": "A dev tree is a polluted measurement environment: uncommitted edits, test artifacts written by earlier runs, fixture files at dev-era states, and warmed caches all shape what the suite sees. The suite passes on the dev tree because the tree contains the conditions the suite was calibrated against — including the defect (here: example tests calibrated to a pre-built feature). A pristine worktree removes the pollution: it is the exact bytes the rest of the world will receive, with none of the lane's local accommodations. Verdicts diverge exactly where the accommodations matter — which is exactly where defects hide."
}
~~~

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event": "2026-10-18 lane-executor run 13:35–15:12 UTC (window), t0840-lane12, breaker #12 feature.naya_answers (memory/2026-10-18.md)",
  "incident": "dev-tree pytest passed → pushed → fresh tree caught 3 REAL failures (tests using naya_answers as 'still specified' example, rotated to feature.scheduler per the tests' own rule); defect reached published head",
  "remediation": "rotate example, amend, fresh-verify BEFORE push (lane's standing rule), force-push own branch, re-verify; final fresh-tree 257/257 at pinned head 959ea1154, verifier PASSED x3",
  "sources": ["goals/bring-naya-to-life/hidden_files/twelve-lane-receipts/t0840-lane12.md (9.5/10)", "#2721 board comment 6250675518"],
  "cousins": ["SN-050 (verify pushed bytes — receiving-side twin)", "SN-01365 (verify the final artifact, not the intermediate)", "SN-01632 (verification is read-only — discipline twin)"]
}
~~~
