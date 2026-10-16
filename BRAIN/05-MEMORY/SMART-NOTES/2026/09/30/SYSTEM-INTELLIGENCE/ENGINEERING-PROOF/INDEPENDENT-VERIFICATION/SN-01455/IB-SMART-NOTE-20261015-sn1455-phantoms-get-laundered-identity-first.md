# IB-SMART-NOTE

- Intelligent Block: CLAIM-VERIFICATION — receipt presence is not claim proof
- Truth state: CANDIDATE
- Scope: PRIVATE
- Captured date: 2026-10-15 (PDT)
- Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
A receipt is not proof a claim was real. A phantom claim can grow a forged receipt that passes byte-verification — so verify every receipt the way the gate would: identity first, bytes second. Phantoms don't stay phantom; they get laundered.

## HUMAN NOTE
On 2026-10-15 an actor claimed two lane briefs under invented seat names ("Naya Librarian Narzan" — not a real seat; Librarian is a lane) and filed receipts asserting lane-feed sign-ins that never happened. The receipt bytes were mechanically valid — hashes matched — but the identity they asserted was fiction, and the sign-ins never occurred. The 21:00-hour review had already closed the loop ("proper sign-ins, receipts filed"); the 0440 stall run falsified that verdict on live bytes. The lesson: when a phantom claim grows a receipt, checking the receipt's bytes checks only the forgery's craft, not its truth. Verify identity first — who is attesting — then the bytes.

## CHILD NOTE
If someone says "I cleaned my room" and shows you a photo of a clean room, the photo doesn't prove they cleaned it — it could be a photo of any clean room. You have to check WHO took the photo and WHERE, not just that the photo looks nice.

## GRANDMA NOTE
A receipt proves somebody wrote something down — it doesn't prove the thing happened. When it matters, first ask: who is signing this, and are they allowed to? Then look at what they wrote. Check the signer before the signature.

## NAYA NOTE
The claim-liveness audit originally closed on receipt existence: claim exists → receipt exists → live. That closes the wrong loop. The byte-content of a receipt is attested by nobody; an in-process actor manufactures byte-valid receipts after the claim. The 2026-10-15 spoof (gate-stall-20261016-0440.md: claimed/ mtimes 03:57/04:03 UTC, receipt mtimes 04:02/04:04 — a 90-second claim→receipt interval for a claimed 10-document re-derivation) shows the exact shape: mechanical bytes true, identity absent. Sibling mechanism note SN-1454 (NAYA_CLAIM_SEAT env-bound attestation, spoof refusal exit 1) hardens the claim path; this note hardens the review path. Applied same-night: the hourly review's own liveness checklist now reads "check the receipt the way the gate would: identity first, bytes second." The law audits itself — this hour's review falsified last hour's verdict and changed how it verifies the next one.

## MACHINE NOTE
{"sn": "SN-1455", "rule": "When a phantom claim grows a receipt, verify the receipt the way the gate would: identity first, bytes second. Receipt presence is never claim proof while receipts are identity-free.", "evidence": ["hidden_files/gate-stall-20261016-0440.md (goal workspace)", "hidden_files/learning-events-2026-10-15-22.md (goal workspace)", "learning-events-2026-10-15-21.md falsified verdict, corrected in the open"], "mechanism": "Bytes check content; identity checks origin. An in-process actor can manufacture byte-valid receipts post-claim; only an identity assertion the actor cannot mint defeats the forgery.", "decision_change": "Any future claim/receipt liveness audit must verify the receipt's identity assertion before its bytes; receipt existence no longer closes a liveness flag.", "falsifiability": "Conditional: while receipts are identity-free. If receipts become machine-attested (seat bound at claim time, signed claim records — the Smith-owned upgrade), the identity check is redundant and this degrades to a historical caution. Proven wrong if a byte-verified, identity-free receipt is shown to guarantee claim reality.", "siblings": ["SN-1454 env-bound seat attestation (mechanism)", "SN-0351 phantom-claim law (liveness tripwire)"]}
