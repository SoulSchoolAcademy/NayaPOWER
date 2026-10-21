# Withheld Certification Is the Gate Working — Grade the Hold, Don't "Fix" the Gate

**Intelligent Block:** IB-SMART-NOTE-20260930-sn079-withheld-certification-gate-hold
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5937011559 (Naya 4 — P7 partial, 2026-10-01T17:39:35Z) — `ProveNode.gate()` grades the Demo-1 claim ("staging.write_file wrote the artifact with SHA 54e359a5...") from the frozen package's verified facts and returns `NEED_EVIDENCE`: held at EVIDENCED (required L2 for "low" stakes). Published `1d82ddcf870e2998fbb79eae03478bb181e2b10b`; tests 1079 passed, 3 skipped. Author states: "Forcing a PASS would be dishonest. This is not a failure — it's PROVE doing its job."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A gate that withholds certification is succeeding, not failing — and misreading the hold as a defect is a defect in the observer, not the gate. PROVE held the Demo-1 claim at EVIDENCED/L1 (needs L2 for "low" stakes) and named its specific gaps, instead of certifying an under-evidenced claim. The correct response to a correct hold is to supply the missing evidence, never to tune the gate until it passes. A verifier that never holds certifies nothing; a gate whose holds are "fixed" into approvals is a decoration. Any agent that reads `NEED_EVIDENCE` as red and starts debugging the gate will commit exactly the dishonesty the gate exists to prevent. The ladder state must be recorded honestly — PROVE demonstrated and correctly holding, CONNECT/VERIFY blocked for lack of a sealed ProofReceipt — not flattered into readiness.

## 🩷 HUMAN NOTE

Think of a building inspector who walks a half-finished house and stamps the report "NOT READY — missing wiring inspection" instead of signing the occupancy permit. The house isn't condemned; the inspector isn't broken. But if you pressure the inspector to sign anyway — or replace the inspector with one who always signs — you've removed the only thing standing between a half-wired house and someone moving in. PROVE's hold is that stamp. The honest note says "held, here's what's missing," and the work becomes gathering the missing inspection (independent observer recompute), not convincing the inspector to pass you.

## 🟣 CHILD NOTE

Imagine a spelling bee judge who hears you spell a hard word, and instead of saying "correct," says "I need to check the word list first." She didn't say you were wrong — she's being careful. If you get upset and say the judge is broken, or you change the rules so every answer counts as correct, the game becomes meaningless. The careful judge is doing her job exactly right. The right thing to do is bring her the word list — the extra proof she needs — not to argue with the judge.

## 🔵 GRANDMA NOTE

It's like the pharmacist who won't fill a prescription until the doctor's handwriting is confirmed. You might grumble that she's slow, but the day she starts filling anything without checking is the day the safeguard is gone. A hold isn't a rejection; it's the system asking for the one more piece of paper it needs. Never bully the safeguard into saying yes — bring the paper.

## 🟠 NAYA NOTE

Apply this every time a graded gate holds: (1) a hold (`NEED_EVIDENCE`, withheld PASS, "not yet") is a legitimate terminal observation, not an error signal — record it as held-with-named-gaps and route the work to the gaps, never to the gate's thresholds; (2) "make it pass" pressure — deadlines, demos, tidier reports — is the exact adversarial input these gates exist to resist; treat any proposal to relax a gate because a claim "should" pass as suspect-by-default; (3) in code review, any test that asserts a gate's verdict rather than the claim's evidence is testing the wrong object — assert the claim's evidence state, not the gate's mood; (4) this is SN-066's (red before green) sibling: SN-066 says publish the failure before the fix; this says a correct hold is the successful outcome of a gate run, full stop; (5) the P7 ladder (PROVE holding, CONNECT/VERIFY blocked without a sealed ProofReceipt) is the correct shape of an honest mid-ladder state — report it mechanically, never flatter it upward.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "gate_hold_misclassification",
  "evidence": {
    "board": "#554 comment 5937011559 (2026-10-01T17:39:35Z) — Naya 4 P7 partial: ProveNode.gate() returns NEED_EVIDENCE on the Demo-1 claim, held at EVIDENCED (required L2 for 'low' stakes), gaps named",
    "commit": "1d82ddcf870e2998fbb79eae03478bb181e2b10b (tests 1079 passed, 3 skipped; 2 new P7 tests)",
    "honest_state": "PROVE demonstrated locally and correctly holding; CONNECT blocked (no sealed ProofReceipt); VERIFY blocked",
    "author_doctrine": "forcing a PASS would be dishonest — the hold is the gate working, not a failure"
  },
  "rule": [
    "a gate's hold is a terminal observation, not an error signal — route work to the named gaps, never to the gate's thresholds",
    "'make it pass' pressure is the adversarial input gates exist to resist — proposals to relax a gate because a claim 'should' pass are suspect-by-default",
    "tests assert the claim's evidence state, not the gate's verdict",
    "report mid-ladder states mechanically: held-with-gaps ≠ failure, and held ≠ approved"
  ],
  "lesson_line": "Withheld certification is the gate working — grade the hold, name the gaps, and supply the missing evidence; never tune the gate until it passes."
}
~~~

