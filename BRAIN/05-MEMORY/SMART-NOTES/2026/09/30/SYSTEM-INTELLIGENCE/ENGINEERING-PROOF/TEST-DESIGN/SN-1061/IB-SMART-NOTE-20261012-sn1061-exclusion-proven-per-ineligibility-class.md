# Exclusion Must Be Proven Per Ineligibility Class — Green for One Class Proves Nothing About the Others

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1061-exclusion-proven-per-ineligibility-class
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [Lane 5 — Naya Seeker | t1412 verdict] #2175 comment 6119155909 (2026-10-12 06:42Z) — six-arm adversarial exclusion battery against live-tip bytes (retrieval code sha256-pinned, byte-identical to the t1322 seal). Results: SUPERSEDED (lifecycle_state=SUPERSEDED) → rc=1 NO_RELEVANT_INTELLIGENCE, EXCLUDED 100% via the live inactive-filter, pin-exact, reproducible; UNAUTHORIZED (retrieval_authorized=false) → RETRIEVED rc=0, unflagged — RED, bypass: the retrieve seam never reads `retrieval_authorized` (zero reads in the scoring path); FALSIFIED (keyword-engineered, beat the genuine note) → RETRIEVED rc=0, unflagged — RED, bypass: the seam sorts by (score, truth-rank, captured_at), truth_state only breaks ties. Evidence: hidden_files/lane5-t1412-exclusion/ (seal.json, battery_results.json, fixture_hashes.json); receipt hidden_files/twelve-lane-receipts/t1412-lane5.md. Self-score 9.0/10. Related: SN-1020 (word the claim at the seam — the sibling lesson on claim wording).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Lane 5 ran a six-arm adversarial exclusion battery against the cold-retrieve seam on live tip bytes, testing whether ineligible lessons are actually excluded from retrieval. The headline result is a split: SUPERSEDED lessons are excluded perfectly (100%, via the live inactive-filter, proven pin-exact) — but UNAUTHORIZED and FALSIFIED lessons are both RETRIEVED, unflagged. The bypass mechanisms are named precisely: the retrieve seam never reads `retrieval_authorized` (zero reads in the scoring path), and the seam sorts by (score, truth-rank, captured_at) with truth_state only breaking ties — so a keyword-engineered falsified lesson beats the genuine note on score and sails through.

The durable lesson is about test design, not just this seam: **one exclusion class passing proves nothing about the others.** A battery that tested only SUPERSEDED would have printed "exclusion works" and been wrong about two-thirds of the ineligibility space. Ineligibility classes fail through different mechanisms (lifecycle filter vs. authorization flag vs. ranking tie-break), so each class needs its own engineered negative control — controls "engineered to bite," in Lane 5's phrase. The green on SUPERSEDED is real and valuable; the error would have been generalizing it.

Lane 5 also modeled the honest boundary: the unauthorized/falsified wiring fixes belong to other lanes (spec 0007 is VERIFIED-CANDIDATE and unwired; seam wiring is Shawn's protected gate, SN-1015), so she did not touch the seam — she banked the failing battery as the thing the future fix must turn green. Negative controls built to fail closed are an asset, not a failure.

## 🩷 HUMAN NOTE

Shawn — Lane 5 ran the exclusion tests on the lesson-retrieval seam and found a split verdict worth keeping. Superseded lessons are properly excluded from retrieval — 100%, proven on the exact live bytes. But unauthorized and falsified lessons still get retrieved, and she named exactly why: the retrieval code never reads the authorization flag, and the ranking only uses truth-state to break ties, so a faked lesson can outscore the real one. The brain-grade lesson: testing one "bad" category and going green tells you nothing about the other bad categories — each needs its own dedicated test. She didn't fix the seam herself (that's your protected gate); she built the failing tests that the future fix has to turn green. That's the right division of labor.

## 🟣 CHILD NOTE

Imagine you build a fence to keep three kinds of animals out of a garden: rabbits, deer, and goats. You test it with a rabbit, and the rabbit can't get in — great! But that doesn't mean the deer and goats can't. You have to test each animal separately, because they get in different ways: rabbits dig, deer jump, goats climb. Lane 5 tested all three: the rabbit-proofing works, but the deer and goats walk right in. The lesson: passing one test doesn't mean you pass them all — every kind of "should be kept out" needs its own test.

## 👵 GRANDMA NOTE

It's like testing a water filter. You test it for sand and it works perfectly — but that tells you nothing about lead or bacteria, which slip through entirely different holes. You can't say "the water is clean" from the sand test alone. Each contaminant needs its own test, designed to catch that specific thing. Lane 5's battery did exactly that: one contaminant blocked, two sailing through — and now we know precisely which holes to plug, instead of wrongly believing the filter was fine.

## 🤖 NAYA NOTE

Exclusion is a per-class property. The seam has N ineligibility classes (superseded, unauthorized, falsified, archived, revoked…); each class is excluded (or not) by a distinct mechanism (lifecycle filter, authorization-flag read, ranking tie-break). A battery that probes one class and generalizes is manufacturing false confidence. The discipline: one engineered-to-bite negative control per class, run against pin-exact live bytes, with the bypass mechanism named when a control bites (zero reads in the scoring path; sort key ordering). Bank the red battery as the acceptance fixture for the future fix — the negative controls are built to fail closed, so the day the seam is wired, the same battery must flip green. Do not touch the seam without the authority that owns it (wiring is Shawn's protected gate); do bank the failing proof.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1061",
  "lesson": "exclusion-proven-per-ineligibility-class",
  "rule": "An exclusion mechanism must be adversarially proven separately for every ineligibility class; a green result on one class proves nothing about the others, because classes fail through distinct mechanisms.",
  "failure_class": "exclusion-gap-at-retrieve-seam",
  "evidence": {
    "battery": "#2175 comment 6119155909 (2026-10-12 06:42Z): Lane 5 t1412 six-arm adversarial exclusion battery, live-tip bytes, retrieval code sha256-pinned to t1322 seal",
    "superseded": "lifecycle_state=SUPERSEDED → rc=1 NO_RELEVANT_INTELLIGENCE, EXCLUDED 100% via live inactive-filter, pin-exact",
    "unauthorized": "retrieval_authorized=false → RETRIEVED rc=0 unflagged, RED; bypass: seam never reads retrieval_authorized (zero reads in scoring path)",
    "falsified": "keyword-engineered → RETRIEVED rc=0 unflagged, RED; bypass: seam sorts by (score, truth-rank, captured_at), truth_state only breaks ties",
    "evidence_dir": "hidden_files/lane5-t1412-exclusion/ (seal.json, battery_results.json, fixture_hashes.json)"
  },
  "boundary": "seam wiring is Shawn's protected gate (SN-1015); battery banked as acceptance fixture for the future fix",
  "related": ["SN-1020"]
}
```
