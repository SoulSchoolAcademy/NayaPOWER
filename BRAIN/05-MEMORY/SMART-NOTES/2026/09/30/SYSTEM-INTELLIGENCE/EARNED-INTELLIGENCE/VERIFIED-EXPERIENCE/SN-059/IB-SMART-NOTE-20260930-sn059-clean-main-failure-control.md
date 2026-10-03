# The Clean-Main Control Run — Attribute the Failure Before You Blame the Change

**Intelligent Block:** IB-SMART-NOTE-20260930-sn059-clean-main-failure-control
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5930091991 (Naya-4 self-build-loop sign-out, 2026-10-01 11:08:21Z); branch `naya/p4-consent-consumer-exact-v2` @ `1352743bb3b9bc8e7c9bc27c24bc11c5ae74a179` (parent `a726a837`); draft PR #1242 (clean successor of #1139).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-01 the P4 consent-consumer re-exactification cycle ran `test_production_migration_history_baseline` against its own branch and watched one test fail on first run: `lineage_is_preserved_exactly`. The instinct is to attribute the failure to the change you just made. The control that settled it: run the same failing test on a **clean-main sparse checkout** — it failed identically there. The failure belonged to the checkout environment (missing archived paths), not to the code: with the archived paths present, the battery passed 12/12, plus 9/9 on the consent SQL tests, byte-verified and API-pushed without CI reliance. A test failure is a claim against your change only after the clean-main control run clears the environment of suspicion.

## 🩷 HUMAN NOTE

When your team ships something and a test lights up red, the room's first question is "what did we break?" — and that question wastes real hours when the answer is "the lab, not the specimen." Build the control run into the reflex: same test, clean room, before anyone rewrites a line of code. You'll catch environment failures — sparse checkouts, missing fixtures, stale caches — in minutes instead of chasing ghosts for a day. Evidence first, blame never.

## 🟣 CHILD NOTE

If your toy doesn't work in the bathtub, don't say you broke it — try it on the rug first. If it's broken on the rug too, the toy was already like that. Check the clean place before you feel bad.

## 🔵 GRANDMA NOTE

Before you throw out the whole recipe because the cake fell, bake it once in a proper tin with proper ingredients. Sometimes it's the pan, not the cook.

## 🟠 NAYA NOTE

Classify-before-code (SN-031) tells you to sort failures before changing anything. The clean-main control run is *how*: reproduce the failing test on a pristine checkout of main — no branch changes, same sparse depth. If it fails there, you are looking at an environment artifact (missing paths, checkout sparsity, fixture absence), and fixing your code would be fixing the wrong thing. Report it as such, note the reproduction, move on. Only if the control passes does the failure belong to your change.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "failing_test_reproduced_on_clean_main_is_environment_failure_not_code_failure",
  "procedure": "same_failing_test_on_pristine_main_checkout_same_sparse_depth_before_attributing_to_change",
  "evidence": "NayaPOWER#554 comment 5930091991; branch naya/p4-consent-consumer-exact-v2 @ 1352743bb3b9bc8e7c9bc27c24bc11c5ae74a179; test_production_migration_history_baseline lineage_is_preserved_exactly fails on clean-main sparse checkout, passes 12/12 with archived paths present; PR #1242",
  "refines": "SN-031 classify-before-code",
  "date": "2026-10-01"
}
~~~
