# A Repair Claim Needs Two Proofs: the Gap (Non-Vacuous) and the Fix (Adversarial + Commuting)

**Intelligent Block:** IB-SMART-NOTE-20261018-sn01663-repair-claim-two-proofs
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/live-plan.md DIRECTOR TICK 2026-10-18 20:38 PDT (2026-10-19T03:38Z): "VERIFY→WIRE queue repair (completed, both honest): dispatcher 03:25Z PROMOTED TODO (review-leg post-match negation gap in `tools/check_merge_consensus.py`) — VERIFY confirmed on tip bytes with 7-case probe matrix (6259045682, fail-open CONFIRMED on three inputs, non-vacuous); WIRE REPAIRED + PROVEN (22-case battery, 5/5 adversarial probes, commute with Electrician's blockquote repair 22/22, bytes filed, no self-merge — merge lane owns; 6259109038). WIRE PROPOSED: scorecard-leg backticked-mention gap on tip bytes — observed NOT claimed, main-seat/dispatcher triage."

## ✦ IN A NUTSHELL

Patching the single input that was reported is not a repair — it's a bandage on the symptom while the class stays open. This tick's VERIFY→WIRE pair showed the two-proof pattern: first VERIFY proved the gap was real with a 7-case probe matrix (fail-open CONFIRMED on three inputs, so the gap is non-vacuous, not a misdiagnosis), and only then WIRE repaired and proved the fix — a 22-case battery, 5 adversarial probes, and a 22/22 commute check against the sibling repair, because two repairs to the same gate can each pass alone and break together. A repair claim is complete only with both proofs: the gap (non-vacuous) and the fix (adversarial + commuting).

## 🩷 HUMAN NOTE

Shawn — when the team found a hole in one of our gate checks tonight, they didn't just patch the one reported case. First the verification lane proved the hole was real with a seven-case probe — it failed open on three inputs, so it was a real class of failures, not a fluke. Then the wiring lane fixed it and proved the fix: 22 test cases, 5 adversarial attacks, and a check that the fix doesn't break the other repair made to the same gate. The rule going forward: every repair claim carries two proofs — proof the gap is real, and proof the fix holds under attack and plays well with its neighbors.

## 🟣 CHILD NOTE

Imagine you find one hole in a fence and hammer a board over it. That's the easy part. The smart part: first you walk the whole fence to prove the hole is real and find its whole shape (maybe the fence is rotten in a whole stretch, not just one hole). Then you fix it and kick the fence hard a few times to prove your fix holds — and you check that your new board doesn't block the gate your friend just fixed. Two proofs: the hole is real, and the fix is strong.

## 🔵 GRANDMA NOTE

It's the difference between patching the one flat tire you saw and inspecting all four tires, then taking the car for a hard drive to prove the repair holds. The team found a gap in a safety check tonight. They didn't just fix the one reported case — first they proved the gap was genuine with a matrix of probes (it failed in three of seven scenarios), then they fixed it and stress-tested the fix with adversarial cases and confirmed it didn't interfere with a related fix to the same check. From now on, a repair isn't done until both are proven: the gap is real, and the fix survives attack.

## 🟠 NAYA NOTE

Cold successor: a repair claim to any gate check is complete only when it carries two proofs — the gap proof (non-vacuous) and the fix proof (adversarial + commuting).

1. **Gap proof (VERIFY owns):** before any repair, run a probe matrix over the decision surface — positive and negative cases. The gap is REAL only if fail-open (or the claimed failure mode) CONFIRMS on at least one input and the matrix is non-vacuous (it discriminates: some inputs pass, some fail). A single reported input proves nothing.
2. **Fix proof (WIRE owns):** after repair, run (a) a case battery across the class the gap belonged to, (b) adversarial probes designed to break the fix, and (c) a commute check against sibling repairs to the same gate — two repairs can each pass alone and break together. Bytes filed; no self-merge — the merge lane owns the landing.
3. **Discipline on the side:** a found-but-unproven gap is PROPOSED and observed, never claimed. The scorecard-leg backticked-mention gap this tick stayed PROPOSED pending tip-byte verification — propose first, claim after the matrix.
4. A repair receipt missing any of the three (non-vacuous gap matrix, adversarial fix battery, commute check) is INCOMPLETE and the scorer bounces it.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1663",
  "title": "A Repair Claim Needs Two Proofs: the Gap (Non-Vacuous) and the Fix (Adversarial + Commuting)",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "VERIFICATION", "REPAIR-PROOF"],
  "applies_when": ["verify", "gap-repair", "gate", "repair-verification", "wire", "probe-matrix", "adversarial-proof", "sibling-repair"],
  "enforcement": "A repair claim is INCOMPLETE unless it carries (a) a probe matrix proving the gap non-vacuous — positive and negative cases, failure mode CONFIRMED on at least one input (VERIFY owns), (b) an adversarial probe battery on the repaired bytes, and (c) a commute check against sibling repairs to the same gate (WIRE owns b+c). The scorer bounces repair receipts missing any of the three; a found-but-unproven gap stays PROPOSED/observed, never claimed. Merge lane owns the landing; no self-merge.",
  "cousins": ["SN-0532 (name-the-residuals — measurement-side probe precedent; this is the repair-side two-proof discipline)", "SN-1003 (probe-tests-never-judge-live-content — probe honesty; this names what probes must prove before and after a repair)", "SN-1660 (name the gate's read surface before choosing re-fire vs fix — the read surface is where this tick's probe matrix aimed)"],
  "evidence": {
    "gap_proof": "hidden_files/live-plan.md DIRECTOR TICK 2026-10-18 20:38 PDT: dispatcher 03:25Z PROMOTED TODO (review-leg post-match negation gap in tools/check_merge_consensus.py); VERIFY confirmed on tip bytes with 7-case probe matrix (6259045682, fail-open CONFIRMED on three inputs, non-vacuous)",
    "fix_proof": "WIRE REPAIRED + PROVEN (22-case battery, 5/5 adversarial probes, commute with Electrician's blockquote repair 22/22, bytes filed, no self-merge — merge lane owns; 6259109038)",
    "discipline": "WIRE PROPOSED: scorecard-leg backticked-mention gap on tip bytes — observed NOT claimed, main-seat/dispatcher triage"
  },
  "decision_change": "the next gap-repair decision runs probe-matrix-first (prove the gap non-vacuous) and adversarial-after (prove the fix closes the class and commutes with sibling repairs) instead of patching the reported input; an unproven gap stays PROPOSED.",
  "falsifier": "if probe-matrix-verified repairs show no higher first-try success than unprobed patch repairs, or a repair passing the full two-proof bar breaks on a real input the matrix missed, the two-proof discipline's claimed value is falsified — the bar would be ritual, not discrimination.",
  "mechanism": "Probes enumerate the decision surface, so the repair must close the class, not the instance: patching the single reported input leaves the class open and the next input through the same gap fails the same way. The adversarial battery attacks the repaired surface rather than re-running the happy path. The commute check proves composition: two repairs to the same gate can each pass alone and break together, so the pair must be proved as a pair."
}
```
