# IB-SMART-NOTE-20261008-sn0637-local-verifier-green-proves-local-code-never-deployed-enforcement.md

Intelligent Block: SN-0637
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-08
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A local preflight verifier's green is bounded by its execution surface: it proves the local code behaves correctly, and nothing more. In the 2026-10-08 independent machine-enforcement audit of the Team Protocol integration packet, all 13/13 local falsifier tests passed — including missing/stale/mismatched read evidence, wrong repo/session, false independent claim, self-granted authority — and the auditor correctly stated what the green does NOT prove: actual reading, comprehension, repository integration, or deployed enforcement. Never cite an offline verifier's pass as proof that the gate is enforced in the live system.

## HUMAN NOTE

An independent seat audited the Team Protocol integration packet and shipped an offline, non-governing Python preflight verifier with a JSON data contract. The falsifier battery was thorough: 13/13 passing, covering adversarial cases like forged read receipts, stale digests, wrong repository or session claims, and self-granted authority (correct receipt with authority_granted=false). The green is real — but the auditor drew the exact boundary in the same breath: it validates only local code behavior; it does not prove that any agent actually reads the protocol, comprehends it, is integrated with the repository, or is enforced by a deployed gate. The artifacts were deliberately supplied in the Human Director's conversation, not committed to the repo — an offline check is a design instrument, not enforcement. Evidence: #1354 comment 6051681715, 2026-10-08T03:39:38Z. This is the family of the Deno helper-test lesson and the phantom-green doctrine: the instrument you test with is never the system you deploy to, and the verdict never travels further than the surface it ran on.

## CHILD NOTE

If you practice a fire drill in your bedroom and do everything perfectly, does that prove you'd do it perfectly in a real fire at school? No — it proves you can do the steps when everything is familiar and safe. The real test is the real building. A practice run's perfect score is real, but it only covers the practice.

## GRANDMA NOTE

A lock that works perfectly on the workbench isn't yet a locked door — you still have to install it in the door, in the house, and check it holds against a real push. Testing the mechanism in isolation is good work, but never confuse "the mechanism works on the bench" with "the house is locked."

## NAYA NOTE

Whenever you build or run an offline preflight verifier: write the boundary into the receipt in the same breath as the green. State explicitly what the run does not prove (actual reading, comprehension, repo integration, deployed enforcement). Never let a local 13/13 travel upward into a claim about the live system. The next step after a local green is always a separate, deployed-enforcement proof — and it is a different proof, not a continuation of the same one.

## MACHINE NOTE

{"sn": "SN-0637", "title": "A Local Verifier's Green Proves Local Code, Never Deployed Enforcement", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-08", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "law": "an offline verifier's verdict is bounded by its execution surface; never cite it as proof of deployed enforcement", "boundary": "proves local code behavior only; does NOT prove actual reading, comprehension, repository integration, or deployed enforcement", "evidence": {"board": "#1354 comment 6051681715 (2026-10-08T03:39:38Z)", "battery": "13/13 local falsifier tests", "artifact_disposition": "offline, non-governing; supplied in director conversation, not committed"}, "pairs_with": ["SN-0429 instrument parity", "SN-0341 the instrument lies", "phantom-green doctrine"], "receipt_rule": "write the non-proof boundary into the receipt alongside the green"}
