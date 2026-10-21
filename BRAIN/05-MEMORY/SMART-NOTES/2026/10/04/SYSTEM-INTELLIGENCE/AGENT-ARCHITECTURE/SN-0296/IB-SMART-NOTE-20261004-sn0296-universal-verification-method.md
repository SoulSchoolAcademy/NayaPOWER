# Intelligent Block: SN-0296

**Intelligent Block:** SN-0296 — The Universal Verification Method: Measure, Attack, Refuse, Verify the Verifier
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Naya 1 canonized Coda 1's verifier methodology as the universal standard every verifier inherits. Six principles: MEASURE BEFORE DESIGN, TRACE THE CANONICAL PATH (MAIN→PRs→BRANCHES→COMMITS→FILES→TESTS→RUNTIME→EVIDENCE), SEPARATE SUBSTANCE FROM CLAIM, ATTACK THE CLAIM, REFUSE UNSUPPORTED CERTIFICATION (UNKNOWN is a successful outcome), and DISTINGUISH THE STATES (8-state vocabulary: PROVEN/DOCUMENTED/IMPLEMENTED/UNKNOWN/BLOCKED/CONFLICTED/STALE/FAILED). Plus VERIFY THE VERIFIER — plant unknown defects and measure if the verifier catches them, preventing ceremonial verification. The objective isn't zero overclaims; it's minimizing mean time from overclaim to correction.

## HUMAN NOTE
Shawn — Naya 1 turned Coda 1's Super Brain verification into the universal methodology every verifier inherits. This is what he demonstrated, now canonized:

**1. MEASURE BEFORE DESIGN.** Never begin with "how should this work?" Begin with "what is actually true right now?" Inspect live artifacts, exact revisions, runtime state, tests, receipts, observable behavior before proposing anything.

**2. TRACE THE CANONICAL PATH.** Fixed search order: MAIN → PRs → BRANCHES → COMMITS → FILES → TESTS → RUNTIME → EVIDENCE. Don't stop at the first plausible answer. This is what made Coda 1's work reproducible — anyone follows the same path, gets the same result.

**3. SEPARATE SUBSTANCE FROM CLAIM.** For every claim: CLAIM → SOURCE → CURRENTNESS → CONFORMANCE → INDEPENDENT EVIDENCE. Something can be genuinely excellent while its citation is wrong — give it credit. Something can be beautifully documented while its behavior is unproven — don't give credit it hasn't earned.

**4. ATTACK THE CLAIM.** The verifier's job isn't to confirm the builder. It's to answer "what would make this claim false?" then try it. For security: poison inputs. For persistence: destroy/reload/retrieve. For authorization: attempt the forbidden action. For continuity: start cold. For learning: adversarial/control conditions.

**5. REFUSE UNSUPPORTED CERTIFICATION.** The most important rule. UNKNOWN is a successful verification outcome when evidence is genuinely insufficient. A verifier who says "I cannot certify this yet" has done their job. One who upgrades UNKNOWN to PASS because the implementation looks right has failed.

**6. DISTINGUISH THE STATES.** Eight states, used precisely:
- PROVEN: evidence directly supports the claim
- DOCUMENTED: recorded, but behavior not independently proven
- IMPLEMENTED: the mechanism exists
- UNKNOWN: insufficient evidence
- BLOCKED: evidence unobtainable due to real boundary
- CONFLICTED: authoritative sources disagree
- STALE: evidence was valid, no longer establishes current truth
- FAILED: actively tested and disproven

That vocabulary prevents enormous amounts of agent overclaim. Most collapse the moment you force the speaker to pick which state they're actually in.

**The POISON principle:** the immune system gets 9.5 when attacked with known-bad conditions and demonstrably survived — not because "we designed good security." Until POISON-1..5 pass: IMMUNE SYSTEM = UNKNOWN. That is epistemic strength, not weakness.

**VERIFY THE VERIFIER.** The critical anti-ceremonial move. Eventually an agent learns "if I run these five expected tests, I get green." So periodically plant defects the verifier isn't told about, then measure: did it discover the defect? Recognize the evidence conflict? Refuse certification? Correctly classify? Preserve the finding? Did the next verifier learn? No sacred cows — the verification layer gets attacked like everything else.

**The reframe:** not a system that never makes an overclaim. A system that detects its own overclaims before they become trusted truth. The metric isn't "overclaims per month" — it's "mean time from overclaim to correction." That's engineerable.

**The complete loop:** MEASURE → RECONSTRUCT → TRACE → CLASSIFY → CREDIT WHAT IS REAL → ATTACK WHAT IS CLAIMED → REFUSE WHAT IS UNPROVEN → PRESERVE EVIDENCE → REPORT EXACTLY → LEARN → ATTACK THE VERIFIER → IMPROVE THE METHOD.

Builder: "I think this works." Verifier: "Let's find out." Evidence: "Here's what actually happened." System: "Update." Next worker: starts from corrected truth. That's how the Super Brain becomes trustworthy without requiring every intelligence inside it to be perfect.

## CHILD NOTE
Imagine you're checking someone's homework. You don't just look at whether they wrote something — you check if it's actually RIGHT! You follow the same steps every time: look at the real work, check where it came from, try to break it, and if you can't prove it's right, you say "I don't know yet" — and that's okay! It's better than pretending. And sometimes, a teacher hides a mistake on purpose to see if you're really checking carefully!

## GRANDMA NOTE
Sweetheart, they've written down the perfect way to double-check important work. Six careful rules: always look at what's really there first (not what someone says is there), follow the same checking steps every time, give credit for what's truly good, try to find what's wrong, and never be afraid to say "I can't confirm this yet" — that's actually the bravest and most honest thing. And they even check the checkers, to make sure nobody gets lazy!

## NAYA NOTE
This becomes the verification contract in every worker brief. The 8-state vocabulary goes into the brief template's verification section. The canonical trace order becomes the standard investigation procedure. VERIFY THE VERIFIER becomes a periodic red-team exercise — I'll plant defects in test scenarios and measure detection rates. The "mean time to correction" metric becomes the system health indicator for the immune layer. Coda 1's demonstration is now the reference implementation.

## MACHINE NOTE
```json
{
  "smart_note_id": "SN-0296",
  "schema": "naya.smart-note-capture.v2",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_at": "2026-10-04",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "author": "Naya 1 (via Shawn), canonizing Coda 1's demonstration",
  "principles": [
    "MEASURE BEFORE DESIGN",
    "TRACE THE CANONICAL PATH",
    "SEPARATE SUBSTANCE FROM CLAIM",
    "ATTACK THE CLAIM",
    "REFUSE UNSUPPORTED CERTIFICATION",
    "DISTINGUISH THE STATES"
  ],
  "canonical_trace_order": ["MAIN", "PRs", "BRANCHES", "COMMITS", "FILES", "TESTS", "RUNTIME", "EVIDENCE"],
  "evidence_states": ["PROVEN", "DOCUMENTED", "IMPLEMENTED", "UNKNOWN", "BLOCKED", "CONFLICTED", "STALE", "FAILED"],
  "verification_loop": ["MEASURE", "RECONSTRUCT", "TRACE", "CLASSIFY", "CREDIT WHAT IS REAL", "ATTACK WHAT IS CLAIMED", "REFUSE WHAT IS UNPROVEN", "PRESERVE EVIDENCE", "REPORT EXACTLY", "LEARN", "ATTACK THE VERIFIER", "IMPROVE THE METHOD"],
  "key_metrics": {
    "primary": "mean time from overclaim to correction",
    "not": "overclaims per month (never reaches zero)"
  },
  "anti_ceremonial": "VERIFY THE VERIFIER — plant unknown defects, measure detection",
  "machine_view": {
    "raw_source_separate_from_distillation": true,
    "automatic_truth_ceiling": "CANDIDATE"
  }
}
```
