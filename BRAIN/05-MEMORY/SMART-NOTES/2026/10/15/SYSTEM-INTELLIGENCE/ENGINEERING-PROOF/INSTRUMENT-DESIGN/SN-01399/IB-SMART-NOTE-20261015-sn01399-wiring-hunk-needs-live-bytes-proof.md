# A Gate Tested Only at Unit Level Is a Gate Untested — Prove the Wiring Hunk on Live Bytes

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01399-wiring-hunk-needs-live-bytes-proof
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INSTRUMENT-DESIGN
**Provenance:** Captured on the 07:08 PDT smart-note-distillation tick (2026-10-15) from lesson-broadcast [t0811] (mirror, gap-scorer-20261015-1910-lane4 GAP CLOSED, 9.5/10).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The staged retrieval-auth-gate wiring was green at 25/25 module unit tests — and could never fire. An EQ1-EQ4 run falsified it on live bytes: the wiring hunk tested `not retrieval_visible(...)` on a 2-tuple that is always truthy, so the gate was dead by truthiness; the same harness with `[0]` went 4/4 green (red→green proof). The broken seam was the wiring hunk the tests never touched.

The durable rule: **unit tests exercise module interfaces with mocked boundaries; the seam — the wiring hunk joining the gate to its caller — executes only in the composed system, so truthiness-class bugs hide exactly there.** A gate the tests can't break is a gate the tests never touched. Gate acceptance requires an EQ-style red→green probe of the exact wiring hunk on live bytes.

## 🩷 HUMAN NOTE

Shawn — a security gate passed all 25 of its unit tests, but it could never actually fire: the connecting code checked "not this thing" on a value that's always true — the gate was wired dead from the start. The unit tests never touched that connecting piece, so they stayed green while the gate did nothing. Only a live end-to-end probe caught it. Lesson banked: for gates, prove the wiring — the exact piece that connects the gate to the code it guards — on live bytes, red to green. Unit tests alone don't cover the seam.

## 🟣 CHILD NOTE

Every part of the bicycle passed inspection — but the brake cable was never actually connected to the brake. All the part-tests were green because nobody pulled the brake lever. The first kid who squeezed the lever on a real hill found out the hard way. Test the squeeze, not just the parts.

## 🔵 GRANDMA NOTE

It's like testing every lightbulb in the house but never flipping the switch on the newly wired lamp. The bulbs are fine, the socket is fine — but the wire between them was never connected. You only find out when you flip the switch for real. For gates, flip the switch on live bytes.

## 🟠 NAYA NOTE

Apply to every enforcement gate you accept: (1) gate acceptance = an EQ-style red→green probe of the exact wiring hunk on live bytes — red first (prove the gate fires on the violation), green after the fix; (2) review `not` applied to composite return values as a known bug class — unpack the tuple first, then test the element; (3) if the unit suite cannot be made to break the gate, the suite does not cover the gate — add the integration probe, don't add more unit tests; (4) re-cut the hunk, re-run the probe green, THEN seek Shawn's word — the word must wire a gate that gates; (5) cross-link the family: SN-01393 (the gate must live on the claim path), SN-0987 (prose↔machine agreement).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INSTRUMENT-DESIGN",
  "sibling_notes": ["SN-01393 (prose-eligibility-is-no-eligibility — gate must live on the claim path)", "SN-0987 (dead-in-prose direction)"],
  "learning_refs": ["lesson-broadcast [t0811] (EQ1-EQ4 falsification, gap-scorer-20261015-1910-lane4, 9.5/10)"],
  "evidence": {
    "unit_tests": "25/25 module tests green while the gate could never fire",
    "falsification": "EQ1-EQ4 run on live bytes: hunk tested `not retrieval_visible(...)` on a 2-tuple that is always truthy",
    "repair_proof": "same harness with `[0]` goes 4/4 green (red→green proof)",
    "next": "wiring owner (Lane 8 / spec-0007) re-cuts the hunk with `[0]`, re-runs the probe green"
  },
  "rule": "gate acceptance requires an EQ-style red→green probe of the exact wiring hunk on live bytes — a gate the tests can't break is a gate the tests never touched",
  "decision_change": "the next seat accepting an enforcement gate ships a live-bytes red→green probe of the wiring hunk itself, not just green module unit tests",
  "falsifier": "a wiring hunk covered by an integration-level probe that breaks the gate on the violation input shows the lesson already satisfied — the acceptance criterion (red→green on the hunk) is checkable, so satisfaction is provable",
  "mechanism": "unit tests exercise module interfaces with mocked boundaries; the wiring hunk (gate joined to its caller) executes only in the composed system — truthiness bugs like `not` on an always-truthy 2-tuple are exactly the class mocks hide, which is why the seam is the place unit tests never touch"
}
~~~
