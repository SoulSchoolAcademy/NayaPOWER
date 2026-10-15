# Gate-Window Mismatch — The Prose's Reference Window Must Lie Inside the Machine's Read Window

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01397-gate-window-mismatch
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/GOVERNANCE/GATE-DESIGN
**Provenance:** Captured on the 07:08 PDT smart-note-distillation tick (2026-10-15) from lesson-broadcast [t0413] (Lane 3 arm-fresh recusal receipt, mirror).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The claim gate lived in two places with two different read windows: the task-body GATE-SKIP rule said "read its first 25 lines," but the enforcement script `bin/claim-brief.py` evaluated only the first 10. Eligibility text at lines 11–25 was invisible to the machine while the rule still expected seats to read it — so the machine's verdict and the prose's verdict disagreed on the same brief, and the cost surfaced as a claim-then-recuse round-trip. This is the *window* direction of the prose↔machine agreement family (SN-0987 deprecation direction; SN-01393 constraint direction).

The durable rule: **the line window the prose references must lie inside the line window the machine evaluates.** Prose referencing a wider window than the code reads is unenforced rule masquerading as enforced rule. Until the script reads 25 lines, the standing hand workaround holds: seats hand-read the first 25 lines inside the claim block.

## 🩷 HUMAN NOTE

Shawn — a claim rule said "read the first 25 lines of the brief," but the checker tool only looked at the first 10. Any eligibility rule written on lines 11–25 was invisible to the machine — so a seat could claim a task the tool allowed, then have to recuse when a human read the full rule. Wasted round-trip. The fix is mechanical: prose and code must read the same window — the rule's referenced window must fit inside the script's evaluated window. Until the script is fixed, seats hand-read all 25 lines at claim time. Lesson banked: a rule the machine can't see isn't a rule the machine enforces.

## 🟣 CHILD NOTE

The homework instructions said "read problems 1 to 25 before answering" — but the grading computer only checked problems 1 to 10. Kids who read all 25 found a rule on problem 15 the computer never saw, so their answers were right and wrong at the same time. Fix: the computer must check all 25, or the instructions must say 10. Until then, kids read all 25 by hand.

## 🔵 GRANDMA NOTE

It's like a recipe that says "follow steps 1 through 25" but the kitchen timer only counts steps 1 through 10. A warning written at step 15 never rings the timer — the cook finds out the hard way. Make the timer count what the recipe says, or shorten the recipe. Until then, the cook reads every step herself.

## 🟠 NAYA NOTE

Apply to every gate you design or inherit: (1) state the read window in BOTH places — prose and code — and verify window(prose) ⊆ window(code), as a checkable property, not a hope; (2) test the boundary: place eligibility text at the prose window's edge and prove the machine sees it before the gate ships; (3) treat any prose reference wider than the machine's window as a prose-only rule (SN-01393) — unenforced until aligned, never "mostly enforced"; (4) the hand workaround is a bandage with an expiry: name the fix (script reads 25 lines) and its owner, and retire the workaround the same tick the script is fixed — don't let the workaround become the process; (5) cross-link the family: SN-0987 (deprecation direction), SN-01393 (constraint direction), SN-01386 (format-keyed gates).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/GATE-DESIGN",
  "sibling_notes": ["SN-01393 (prose-eligibility-is-no-eligibility — constraint direction)", "SN-0987 (dead-in-prose direction)", "SN-01386 (format-keyed gate is an open fence)"],
  "learning_refs": ["lesson-broadcast [t0413] (GATE-WINDOW MISMATCH, class-level)"],
  "evidence": {
    "prose_rule": "task-body GATE-SKIP rule: 'read its first 25 lines'",
    "machine_window": "bin/claim-brief.py evaluates only the first 10 lines",
    "observed_cost": "claim-then-recuse round-trip forced by the disagreement (Lane 3 arm-fresh recusal receipt, mirror)",
    "hand_workaround": "seats hand-read the first 25 lines inside the claim block until the script reads 25"
  },
  "rule": "window(prose reference) ⊆ window(machine evaluation) — prose referencing a wider window than the code reads is unenforced rule masquerading as enforced rule",
  "decision_change": "when writing a task-body gate rule and its enforcement script, verify the prose's referenced line window lies inside the script's evaluated window before the gate ships",
  "falsifier": "a gate whose prose references only lines inside the script's evaluated window, audited over a claim population with zero claim-then-recuse round-trips, refutes the need for this rule — which is the rule's own success condition",
  "mechanism": "the script reads lines 1–10; the rule references lines 1–25; eligibility text at lines 11–25 is invisible to the decider, so the machine's verdict and the prose's verdict disagree on the same brief — the disagreement's observable cost is the forced claim-then-recuse round-trip"
}
~~~
