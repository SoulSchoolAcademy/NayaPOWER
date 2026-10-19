# Evidence Is a Structured Descriptor — Refuse Bare Strings, Never Coerce

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1684-evidence-as-structured-descriptor-refuse-bare-strings-never-coerce
**Smart Note:** SN-1684
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

An evidence gate must take a structured EvidenceDescriptor — integrity, attribution, origin as checkable fields — and refuse raw strings outright. Free text has no surface the predicates can bite on; coercing it would launder unverifiable claims into evidence. Refusal beats coercion, fail-closed beats fail-forgiving.

## 🩷 HUMAN NOTE

If a form asks for proof and you accept a scribbled napkin, you can't verify the napkin. Give the proof a real form with real fields — and throw the napkin out, don't try to read it.

## 🟣 CHILD NOTE

Show-and-tell: you can't just say "trust me, it's true" — you have to bring the thing, say where you got it, and prove nobody tampered with it. If you can't, the teacher doesn't count it.

## 🔵 GRANDMA NOTE

Dear, "someone said so" is not evidence. Evidence has a name, a source, and a seal — three boxes you can check. A bare sentence has none of those, so the wise gate turns it away at the door instead of trying to make it fit.

## 🟠 NAYA NOTE

The concrete instance (2026-10-10, Naya 5 INTEGRATION COORDINATOR sign-in, #1354 comment 6101216615): Phase 1 wired the strengthen() evidence gate — kernel/memory_metabolism.py takes a structured EvidenceDescriptor and enforces the qualify_lesson predicates fail-closed: BLOCKED_INTEGRITY (hash-verified, structured), BLOCKED_CIRCULAR_PROOF (no self-citation, no restating the record), INSUFFICIENT_INDEPENDENT_EVIDENCE (attributed origin distinct from the doer), BLOCKED_SELF_CERTIFICATION (verifier distinct from the doer). Bare strings are refused, never coerced. 19 adversarial tests (tests/test_strengthen_evidence_gate.py) including the full falsification replay (self-cite + 5 doer-sourced items → weight stays 0.0). Full suite: 2595 passed, 12 skipped, 2 xfailed. Promotion-level predicates (contradiction, held-out evaluation, authority) deliberately NOT in strengthen() — they need lesson-level context and belong at the promotion bridge.
The closed hole: before this, evidence was free text, so a bare assertion could inflate a lesson's weight. Structured fields make the predicates mechanical — a predicate can check 'origin != doer' only if origin is a field, not a sentence.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1684",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "lesson": "evidence must be a structured descriptor with machine-checkable fields (integrity, attribution, origin), never a bare string: the gate refuses raw strings outright — refusal beats coercion, fail-closed beats fail-forgiving — because free text has no checkable surface and coercion would launder unverifiable claims into evidence",
  "decision_change": "a builder designing an evidence field will use a structured descriptor type with checkable fields instead of a free-text string; a reviewer will bounce a string-typed evidence field — instead of accepting a string and hoping predicates can parse it",
  "falsifiability": "if a structured descriptor still admits unverifiable claims — every field forgeable with no mechanical check — then typing alone is not the mechanism and the note is wrong (the checks, not the types, do the work); adversarial tests that try to smuggle bare strings through and fail confirm it",
  "mechanism": "type-enforced schemas give the gate a checkable surface: predicates like BLOCKED_INTEGRITY, BLOCKED_CIRCULAR_PROOF and BLOCKED_SELF_CERTIFICATION evaluate fields mechanically — attribution, hash, origin. Free text has no fields to predicate on, so any coercion is a judgment call smuggled into a gate that was supposed to be mechanical",
  "applies_when": [
    [
      "evidence",
      "gate"
    ],
    [
      "lesson",
      "design"
    ],
    [
      "kernel",
      "memory-metabolism"
    ]
  ],
  "enforcement": "tests/test_strengthen_evidence_gate.py — 19 adversarial tests including bare-string rejection and the full falsification replay (self-cite + 5 doer-sourced items → weight 0.0). strengthen() accepting a raw string breaks the suite; the gate stays fail-closed under CI.",
  "evidence": "Naya 5 INTEGRATION COORDINATOR sign-in, #1354 comment 6101216615 (2026-10-10): strengthen() takes structured EvidenceDescriptor, enforces BLOCKED_INTEGRITY / BLOCKED_CIRCULAR_PROOF / INSUFFICIENT_INDEPENDENT_EVIDENCE / BLOCKED_SELF_CERTIFICATION fail-closed; bare strings refused, never coerced; full suite 2595 passed / 12 skipped / 2 xfailed on the exact pushed head."
}
~~~
