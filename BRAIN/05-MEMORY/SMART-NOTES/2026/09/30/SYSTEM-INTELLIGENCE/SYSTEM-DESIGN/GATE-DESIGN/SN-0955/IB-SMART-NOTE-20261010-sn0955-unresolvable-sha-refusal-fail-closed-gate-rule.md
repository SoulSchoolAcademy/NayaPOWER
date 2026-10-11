# IB-SMART-NOTE — SN-0955

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/GATE-DESIGN

## IN A NUTSHELL
A gate that consumes SHAs must refuse the unresolvable. The fail-closed activation-gate prototype's design rule: claimed SHAs must resolve to real objects or the gate refuses — no default-trust, no "looks like a SHA". A missing qualification or a stale tip fails closed too. 14/14 tests including negative controls; smoke-verified against real SHAs at tip 57e935c1. The cost of a false refusal is a retry; the cost of a false pass is a forged claim riding the gate.

## HUMAN NOTE
When we designed the new activation gate, we made one rule non-negotiable: if a piece of evidence says "here's my SHA" and that SHA doesn't point to a real object, the gate says no. Not "probably fine" — no. A gate that trusts uncheckable evidence is a decoration. Being wrong by refusing costs one retry. Being wrong by trusting costs everything the gate was supposed to protect.

## CHILD NOTE
If someone shows you an ID you can't verify, you don't let them in. You say no. Saying no when you're unsure is the safe move — you can always check again later.

## GRANDMA NOTE
You don't open the door for a voice through the intercom you don't recognize. "Sounds right" is not "is right." The safe answer to "maybe" is no.

## NAYA NOTE
Future Naya: when you design or review any gate that takes SHAs, revisions, or "verified" labels as input, apply the three refusals: (1) SHA doesn't resolve to a real object → refuse; (2) qualification missing or stale → refuse; (3) tip moved since the claim was minted → refuse. Write the negative-control tests first (forged SHA, stale tip, version mismatch, wrong director — the prototype's adversarial probes). A refusal must be a clean, legible DENY (receipt written), not a crash — a crashing guard is noisier than a denying guard and teaches operators to ignore it. Prototype + 14/14 tests live at night-shift-2026-10-10/receipts/t2252-a-{design.md,gate.py}; landing (kernel/protocol/activation_gate.py + tests) is morning work per plan P2 item 7.

## MACHINE NOTE
```json
{
  "sn": "SN-0955",
  "slug": "unresolvable-sha-refusal-fail-closed-gate-rule",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "category": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/GATE-DESIGN",
  "doctrine": "refuse_the_unresolvable_fail_closed_on_unverifiable_evidence",
  "rule": {
    "sha_unresolvable": "refuse",
    "qualification_missing_or_stale": "refuse",
    "tip_moved_since_claim": "refuse",
    "refusal_form": "clean_legible_DENY_with_receipt_never_crash"
  },
  "evidence": [
    "night-shift-2026-10-10/receipts/t2252-a-design.md: fail-closed activation gate design doc — claimed SHAs must resolve to real objects or refusal; missing qualification or stale tip fails closed",
    "night-shift-2026-10-10/receipts/t2252-a-gate.py: tested prototype, 14/14 tests pass incl. negative controls; smoke-verified against real SHAs at tip 57e935c1",
    "night-shift-2026-10-10/plan.md P2 item 7: NEXT — land kernel/protocol/activation_gate.py + tests/test_activation_gate.py, register in protocol_manifest.json"
  ],
  "cousins": ["SN-0940 (built-as-code = enforced-as-code)", "SN-0953 (verification is not authorization)"],
  "distinct_from": "SN-0940 covers directive enforcement; SN-0953 covers merge authorization. This is the gate-implementation rule: what the code must do with unresolvable evidence."
}
```
