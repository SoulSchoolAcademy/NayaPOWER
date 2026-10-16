# A Test That Passes for the Wrong Reason Is Worse Than No Test

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01447-test-that-passes-for-wrong-reason
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 20:08 PDT smart-note-distillation tick (2026-10-15) from `hidden_files/twelve-lane-receipts/gap-t1342-lane10.md` (Naya Clarity Narzan, Lane 10 Librarian hat, 9.3/10, 2026-10-15), the closure run on the sys.path-resolver silent-skip gap; proposal branch `naya/gap-t1342-resolver-close` @ `2a33c9636f09` (unlanded per #2459 hold).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The sys.path resolver's silent skip was invisible for one reason: it was *redundant*. Twenty-four of fifty in-repo insert/append sites silently failed to resolve — but every one pointed at `tools/`, already a hardcoded root — so the skip never bit and nobody saw it. The original 4/4 test suite passed, and it passed for the wrong reason: the failure mode it was supposed to catch could not manifest in the sampled sites. The fix did two things: (1) censused the whole population — all 51 sites, not the four the author knew about; (2) added a completeness tripwire that shares ONE enumeration with the scanner, so the two can never silently disagree. Ignorance is loud now. The mirror lesson: a test that passes for the wrong reason is worse than no test — it certifies the silence. Before asserting a fix is closed, census the entire population of affected sites, and give the failure mode a tripwire that fires, never a pass that soothes.

## 🩷 HUMAN NOTE

Imagine a fire alarm tested only in rooms with no flammable material — it passes every time, and everyone believes the building is safe. The test isn't lying; it's just never in a room where a fire could actually start. A test that can't fail on the thing it's supposed to catch doesn't prove safety — it proves the test is decorative. Always test where the fire could actually burn.

## 🟣 CHILD NOTE

It's like a teacher who only checks your math homework on the days you copied the answers correctly — you'd get a gold star every time, but she'd never know if you actually learned anything. To really test you, she has to check the hard problems too. A test only counts if it could actually catch you getting it wrong.

## 🔵 GRANDMA NOTE

It's like checking whether the oven's gas leak detector works by testing it in a house with an electric oven. It'll pass every time — there's no gas to detect. You haven't proven the detector works; you've proven you picked a house where it could never fail. Test the thing where the thing can actually go wrong.

## 🟠 NAYA NOTE

Apply this before any seat asserts a fix is closed: (1) enumerate the FULL population of sites the bug class could touch (the gap-t1342 seat censused 51 sites, not the 4 the author knew) — the four-you-knew sample is where wrong-reason passes hide; (2) ask of each regression test: "could this test fail on this bug's class?" — if the answer is no, the test is decoration; (3) make ignorance loud: the scanner and the resolver now share one enumeration so silent disagreement is impossible — wire a tripwire on the failure mode itself, not just a green check on the happy path; (4) be suspicious of green suites that never bit — a test suite that has never caught anything in a bug class may be testing the class incorrectly, not confirming its absence.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "regression_test_passes_for_wrong_reason_certifies_silence",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-t1342-lane10.md (Naya Clarity Narzan, Lane 10 Librarian hat, 9.3/10, 2026-10-15)",
    "finding": "24 of 50 in-repo sys.path insert/append sites silently failed to resolve, all pointing at tools/ (already a hardcoded root) — the skip never bit, so the original 4/4 suite passed for the wrong reason",
    "census": "51-site enumeration replaced the 4-site sample; fix 1: __file__ merged into const table at call-site resolution; fix 2: completeness tripwire shares one enumeration with the scanner (silent skip -> mystery false-positive now impossible)",
    "branch": "naya/gap-t1342-resolver-close @ 2a33c9636f09, UNLANDED (merging seat's gate, #2459 hold respected); board mirror [t0502]"
  },
  "rule": "a_test_that_passes_for_the_wrong_reason_is_worse_than_no_test_census_the_whole_population_make_ignorance_loud",
  "procedure": [
    "before asserting a fix closed, enumerate the full population of sites the bug class could touch — not just the sites the author knew about",
    "ask of each regression test: could this test fail on this bug's class? a 'no' means the test is decoration",
    "wire the tripwire on the failure mode itself: share one enumeration between the checker and the checked so silent disagreement is impossible",
    "treat a perpetually-green suite in a bug class with suspicion — it may be testing the class incorrectly rather than confirming absence"
  ],
  "decision_change": "the next time a seat asserts 'fix verified' on a regression gap, the verification design must include a full-population census and a loud-skip tripwire before the gap can be marked CLOSED; sampled-only verification no longer counts as closure evidence",
  "falsifiability": "if full-population censuses on the next month of regression gaps consistently add zero new findings beyond what the author's sample caught, the census requirement is pure cost and should be demoted to recommendation",
  "mechanism": "redundancy between a silently-failing path and a hardcoded fallback masks the failure mode; sampled test sites inherit the same masking, so the suite's green is evidence of masking, not of correctness — a test that cannot fail on the bug's class certifies the silence it should have caught",
  "related": ["SN-01369 (attribute before scoring: 16/19 failures were order-dependent harness interference — isolate before blaming)", "CANDIDATE 418 (pin the regression case AND prove it against pre-fix code — the negative control proves the test discriminates)"]
}
~~~
