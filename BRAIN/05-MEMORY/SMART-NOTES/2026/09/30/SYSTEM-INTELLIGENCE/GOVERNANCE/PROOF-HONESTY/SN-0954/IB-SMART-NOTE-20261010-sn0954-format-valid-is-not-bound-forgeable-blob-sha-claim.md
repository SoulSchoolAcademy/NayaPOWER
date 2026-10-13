# IB-SMART-NOTE — SN-0954

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/GOVERNANCE/PROOF-HONESTY

## IN A NUTSHELL
Format-valid is not bound. The activation read-receipt's `validate_source_revisions` (read_receipt.py lines 168–186) is format-only — even the credited "blob-SHA binding" is forgeable. Demonstrated end-to-end on exact branch bytes (81465ee9, tip 57e935c1): copied parrot answers mint `passed=True`, `verify()=True`, with zero source reads. Exact-match hardening kills prefix false-passes, not parroting. A verification claim is only as strong as the negative control it survives; the honest fix is challenge-response — fresh byte possession, never a comprehension claim.

## HUMAN NOTE
We built a gate that was supposed to prove an agent actually read a document. An adversarial test showed you could pass it by copying the answers from the source — the gate checks that the answer is formatted right, not that you read anything. Even the SHA "binding" it bragged about could be faked. The lesson: never trust what a check claims it proves. Test it with a cheater. If the cheater passes, the check proves nothing.

## CHILD NOTE
A test that the cheater can pass is not a real test. Always give your checker a cheater and see if it gets caught. If it doesn't catch the cheater, the checker is broken.

## GRANDMA NOTE
A lock that opens for anyone who knows what a key looks like is not a lock. You don't ask "does the key fit the description" — you ask "did this key come from my hand right now."

## NAYA NOTE
Future Naya: when you build or review a verification gate, (1) name the claim the gate says it proves, (2) write the adversarial negative control FIRST (the parrot: correct output, zero legitimate work), (3) if the parrot passes, the gate's claim is void — document it honestly, don't ship it as proof. Strings labeled "binding", "SHA", "signature" in code are marketing until a negative control proves they're enforced. The parroting-bypass follow-up design (13 parrot answers as negative controls, challenge-response recommended, 4 ranked fix options) is the working template; the decision brief (adopt with changes) is Shawn's protected gate — no swap ships without his word.

## MACHINE NOTE
```json
{
  "sn": "SN-0954",
  "slug": "format-valid-is-not-bound-forgeable-blob-sha-claim",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/PROOF-HONESTY",
  "doctrine": "a_verification_claim_is_only_as_strong_as_its_negative_control",
  "rule": {
    "gate_claim": "must_name_exactly_what_is_proven",
    "negative_control_first": "parrot_with_correct_output_zero_legitimate_work_must_fail",
    "parrot_passes": "claim_void_document_honestly_do_not_ship_as_proof"
  },
  "evidence": [
    "night-shift-2026-10-10/receipts/t2312-c.md: validate_source_revisions (read_receipt.py:168-186) is format-only; credited 'blob-SHA binding' is forgeable; exact-match hardening fixes prefix false-passes, not parroting",
    "night-shift-2026-10-10/receipts/t2312-c.md + t2322-a: parroting bypass re-demonstrated end-to-end on exact branch bytes (81465ee9, tip 57e935c1) — parrot answers → passed=True, verify()=True, zero source reads",
    "night-shift-2026-10-10/receipts/parroting-gate-decision-brief.md: recommends ADOPT WITH CHANGES (challenge-response; honest claim = fresh byte possession, never comprehension) — Shawn's protected gate"
  ],
  "cousins": ["SN-0943 (sign-off without demonstrated understanding is a fabricated pass)"],
  "distinct_from": "SN-0943 covers human sign-off; this covers machine verification gates and forgeable proof claims (read receipts, SHA bindings)."
}
```
