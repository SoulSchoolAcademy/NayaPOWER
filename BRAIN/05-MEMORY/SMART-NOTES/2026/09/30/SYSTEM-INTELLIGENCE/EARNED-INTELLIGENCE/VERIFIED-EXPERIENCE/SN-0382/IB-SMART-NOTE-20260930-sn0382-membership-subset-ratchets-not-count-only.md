# Count-Only Ratchets Are Gameable — Pin Membership Subsets, Never Cardinality

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0382-membership-subset-ratchets-not-count-only
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-05 the Naya 3 lane adversarially reviewed its own identity-drift ratchet repair and found the hole: the four new drift classes were pinned by **count only** (`count <= N`). A repair could remove one known defect and introduce a *different* defect in the same class — cardinality 17→17 — and CI stayed green. The stated intent ("drift may never grow silently") was silently violated. The fix: strengthen the test seam with **membership-subset ratchets** for all four identity classes — known defects may disappear without failing, but any previously unseen registry ID, unregistered capture ID, identity-less filename, or filename↔ID divergence fails. A regression now proves equal cardinality does not excuse a replacement defect.

## 🩷 HUMAN NOTE

A test that counts things without naming them only checks the shape of the problem, not the problem. If your rule is "no more than 17 issues," someone (or you, three months later, in a hurry) can swap issue #12 for a brand-new issue #43 and the count never moves. The durable rule: pin the *known* members by name. Known issues are allowed to be fixed and disappear. Anything you have never seen before must stop the line. That is what a ratchet is for.

## 🟣 CHILD NOTE

If your rule is "no more than 5 bad cookies," someone can eat a bad cookie and sneak in a different bad cookie and you still count 5. Better rule: write down the names of the 5 bad cookies. Old ones are allowed to get fixed. Any cookie you never wrote down is a red flag.

## 🔵 GRANDMA NOTE

Don't just count problems — know them by name. A problem you're allowed to fix should disappear from the list; a stranger showing up on it is the thing you're guarding against. Counts can be tricked; a roll call cannot.

## 🟠 NAYA NOTE

Whenever I write a drift or regression ratchet, the default instinct is `assert count <= baseline`. Treat that as a red flag and reach for subset membership instead: keep the count ratchet only as the floor, and assert the known-member set. My own repair passed my own tests until I asked "can I defeat this by substitution?" — the adversary was me, and I won, which is exactly the point of the review step. Run that substitution attack on every ratchet I write before calling it a repair.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "ratchets_must_pin_member_subsets_never_cardinality_alone",
  "failure_mode": "count_only_ratchet_defeated_by_same_count_substitution_repair_removes_known_defect_introduces_different_defect_ci_stays_green",
  "repair": "membership_subset_ratchets_known_defects_may_disappear_unseen_members_fail_plus_regression_proving_equal_cardinality_does_not_excuse_replacement",
  "evidence": "NayaPOWER#1354 comments 6000827491 (hole found), 6000864757 (repair landed), 6000913281 (exact-head proof re-closed), 2026-10-05",
  "self_review_protocol": "after_writing_a_ratchet_attack_it_by_substitution_before_claiming_repair"
}
~~~
