# Intelligent Block: "No read admission found" is not "clean" — cleanliness is a positive claim

Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-15
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
In an audit, "we found no record of you reading it" is not "you never read it" — especially when the same mind operates under many hats. Cleanliness is a positive claim that needs positive evidence. Exclusion-set audits must lead with the operator-attribution pass: who actually ran behind each identity, not just what each label admits.

## HUMAN NOTE
An audit had to certify a truly "cold" seat — someone who had never seen a sealed probe. Five lane identities were excluded by their own read admissions. But the rest couldn't be cleared: the lane labels were being operated by the very seats that were excluded. The audit's honest verdict: absence of a read admission is not evidence of coldness, because contamination rides the operator, not the label. Gate designs should say what counts as clean — not just what counts as excluded.

## CHILD NOTE
If you ask "did anyone peek?" and nobody raises their hand, that doesn't mean nobody peeked — especially if the same kid wears five different hats. To know for sure, you have to check who was actually wearing each hat, not just ask the hats.

## GRANDMA NOTE
Dear, "nobody confessed" is not the same as "nobody did it." If you want to be sure someone kept a secret, you need proof they never saw it — not just that they never mentioned seeing it. Check the hands, not the nametags.

## NAYA NOTE
Lane 6's FP-003 acceptance audit (brief-t0431-lane6) is the proof: 8 lane-executor identities enumerated; 5 excluded by cited read admissions; the remainder unattributable or operated by excluded family seats (Clarity wore Mason/Sage hats; Resolve wore Smith) — so "no direct read admissions" could not clear them. Verdict G5-NOGO, filed as the circuit-breaker finding: the exclusion set is unsatisfiable in this seat population, which is itself a finding about the probe's testability. The auditor's standing rule: distinguish absence-of-evidence from evidence-of-cleanliness in the disposition table. Future exclusion-set audits lead with the operator-attribution pass — trace lane-identity reads to the operating family seat via sign-in lines — before any cleanliness verdict.

## MACHINE NOTE
```json
{
  "sn": "SN-1414",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-15",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": {
    "name": "cleanliness_is_a_positive_claim",
    "statement": "In a shared-context population, 'no read admission found' is not 'clean'. Cleanliness is a positive claim requiring positive evidence of never-having-read. Exclusion-set audits lead with the operator-attribution pass: trace every identity's reads to the operating seat before any clean verdict.",
    "falsifier": "Repeated operator-attribution passes across exclusion-set audits keep finding zero hidden readers — then absence-of-admission was sufficient evidence in that population, and the doctrine relaxes to that population.",
    "mechanism": "Contamination rides the operator, not the label: one family seat operates many lane hats, so label-level exclusion checks miss hat-level reads. The reader is the unit of readership; the lane identity is not. An audit that gates on admissions alone samples the label, not the reader.",
    "adoption_requirements": [
      "enumerate the full identity population before auditing (no silent subset)",
      "trace each identity's reads to the operating seat via sign-in lines (contamination rides the mind)",
      "disposition table distinguishes EXCLUDED / UNRESOLVED / UNVERIFIED / positively clean — never inherits 'probably clean'",
      "gate design states what counts as clean, not just what counts as excluded"
    ],
    "decision_changed": "Future exclusion-set audits and gate designs: the audit's first pass is operator-attribution; 'clean' is never the default verdict for an identity with no admissions."
  },
  "evidence": [
    "hidden_files/twelve-lane-receipts/t0431-lane6.md (G0/G5 verdict on sealed FP-003 probe: 7/7 seal pins recomputed; 8-identity population audit; 5 excluded by cited admissions; rest unattributable or operated by excluded family seats; G5-NOGO filed as the circuit-breaker finding; auditor's rule 10: 'distinguished absence-of-evidence from evidence-of-cleanliness in the table')"
  ],
  "related": [],
  "status": "CANDIDATE — not ratified; only Shawn ratifies"
}
```
