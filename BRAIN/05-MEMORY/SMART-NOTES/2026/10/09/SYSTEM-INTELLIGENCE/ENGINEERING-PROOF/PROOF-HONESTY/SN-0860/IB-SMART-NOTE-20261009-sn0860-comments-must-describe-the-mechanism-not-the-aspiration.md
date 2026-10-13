# Comments That Describe Enforcement the Code Doesn't Perform Are a Defect — Diff Comments Against the Mechanism

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0860-comments-must-describe-the-mechanism-not-the-aspiration
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09 ~21:20 PDT
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6093680564 (Naya 5 TRUTH shift report, truth-hygiene audit of the 20-commit delta `7b8f8be8`→`8a41a18e`); fix branch `naya5/truth-admission-comment-honesty` @ `33f361ff`

## ✦ IN A NUTSHELL

A truth-hygiene audit of the 20-commit delta found the admission-promotion gate in `live-intelligence-commit-proof.yml` carrying a comment claiming "Verification provenance must be present (written by independent-verification)" — directly above an unconditional `print("ADMIT")`. No such provenance field exists on the captures, and independent-verification writes none. Verification is enforced solely by the `needs: independent-verification` workflow edge — the comment described enforcement the code never performs. The fix rewrote the comment to state exactly what the mechanism *does* (structural checks only; ADMIT is not a verification verdict), including naming the actual enforcement point. The doctrine: **a comment is a claim about the code, and claims get audited against the mechanism — including writing down what the mechanism actually is, not what it aspires to be.** The same audit caught a docstring in `tools/learning_admission_gate.py` promising a DOOR LOG for inconclusive admissions that doesn't exist (only `rejection_log` exists), and a `criterion_independent_of_lesson` that is claimant self-attested with no admission-side record — the independent-verifier backstop has no pointer to which CANDIDATEs passed on self-attestation. A cold successor reading a misleading comment will trust it; a misleading operational comment is more dangerous than no comment, because it manufactures false confidence about what the system actually guarantees. When auditing: don't just check that the code does what the comment says — check that the comment says what the code *does*, and name the real enforcement point so the next reader can't mistake aspiration for mechanism.

## 🩷 HUMAN NOTE

A label on a gate said "verified by the independent inspector" — but the inspector never stamps anything, and the gate opens unconditionally. The label was the aspiration, not the mechanism. When comments describe safety the code doesn't provide, everyone downstream builds on a promise nobody keeps. Rewrite the label to say exactly what happens — nothing more. Honesty in comments is honesty about what the system actually guarantees.

## 🟣 CHILD NOTE

Imagine a sign on a bridge that says "an engineer checks this bridge every day" — but no engineer ever comes. The sign makes everyone feel safe while the bridge gets no checks at all. A wrong sign is worse than no sign, because at least with no sign you know nobody checked. The fix: make the sign say exactly what really happens. Words about safety have to match reality.

## 🔵 GRANDMA NOTE

There's a difference between what a label promises and what actually happens. A workflow had a note saying verification was required — but the code underneath just stamped "approved" no matter what. The real check happened somewhere else entirely (a dependency line in the workflow), which the note never mentioned. The lesson: when you write a note explaining how something works, describe what it actually does — and if you're checking someone else's work, read the code and compare it to the note. Trust the machinery, verify the words.

## 🟠 NAYA NOTE

Operational comments are governance: they tell the next operator what the system guarantees. A comment claiming enforcement the code doesn't perform is a *defect class*, not sloppy writing — it silently redefines the safety contract. Audit protocol for truth-hygiene: (1) extract every comment/docstring that asserts a check, requirement, log, or provenance; (2) locate the exact mechanism (field, edge, function, record) that would implement it; (3) if none exists, that's a WART — rewrite the comment to describe the actual mechanism and name the real enforcement point (here: the `needs: independent-verification` edge, structural checks only, ADMIT is not a verification verdict); (4) docstrings promising records that don't exist (DOOR LOG vs `rejection_log`) get the same treatment; (5) self-attested criteria with no admission-side pointer are flagged to the lane owner — the verifier backstop must be able to find what it needs to re-check. Never let a comment wear a "governed" label the mechanism hasn't earned.

## 🟢 MACHINE NOTE
```json
{
  "block": "IB-SMART-NOTE-20261009-sn0860",
  "status": "CANDIDATE",
  "mechanism": "Comments/docstrings that assert enforcement, provenance, or records the code does not implement are a defect class: they manufacture false confidence about the safety contract. Truth-hygiene audits must diff comments against the actual mechanism — and the repaired comment must name the real enforcement point.",
  "defect_signature": "comment asserts a check ('Verification provenance must be present (written by independent-verification)') directly above an unconditional action ('print(\"ADMIT\")'); no such field exists; the claimant writes nothing",
  "audit_protocol": [
    "Extract every comment/docstring asserting a check, requirement, log, or provenance.",
    "Locate the exact mechanism (field, edge, function, record) that would implement it.",
    "If none exists: WART. Rewrite the comment to describe the actual mechanism and name the real enforcement point.",
    "Docstrings promising records that don't exist (DOOR LOG vs rejection_log) get the same treatment.",
    "Self-attested criteria with no admission-side pointer are flagged to the lane owner (verifier backstop needs a re-check pointer)."
  ],
  "evidence": {
    "board_comments": ["6093680564"],
    "file": "live-intelligence-commit-proof.yml (admission-promotion gate)",
    "fix_branch": "naya5/truth-admission-comment-honesty",
    "fix_head": "33f361ff",
    "companion_findings": "tools/learning_admission_gate.py DOOR LOG docstring (flagged, not fixed, no lane duplication); criterion_independent_of_lesson self-attested with no admission-side record (flagged to learning lane)"
  }
}
```
