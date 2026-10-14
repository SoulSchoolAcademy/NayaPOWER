# IB-SMART-NOTE-20261014-sn1290

**Intelligent Block:** SN-1290
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A seal is a claim made OUTSIDE the sealed object — a seal embedded in the file it seals is a promise to itself. t0747 (Lane 2, Arm I pre-reg amendment): the first assembly embedded the sha INSIDE the file it seals (self-referential — caught on the confirming review pass, repaired in the open: the seal now lives externally in `hidden_files/lane-2/arm-i-verdict-flip-seal-t0747.txt`, the old self-embedded seal superseded, both SHAs on the record). t0745 had already applied the detached-seal practice by construction. Lesson: the seal is recomputed over the sealed bytes by a future verifier — bytes that contain their own seal cannot be recomputed, so verification collapses into a circle. Carry the seal outside the sealed bytes, and treat any self-referential pin as a defect on sight.

## HUMAN NOTE

Think of a wax seal on a letter. The seal goes on the OUTSIDE of the envelope so anyone can check: is the envelope intact, does this seal match what the sender recorded? Now imagine someone melts the wax and drips it INTO the envelope before sealing it — the "seal" is now part of the contents. Nobody can ever verify that envelope again, because the thing being checked contains the check itself. That's what happened: a designer stamped her document with a fingerprint that lived inside the document. Caught it on review, moved the fingerprint to a separate file next to the document — now the document is checkable. The rule: the seal never lives inside the thing it seals. If you ever see a fingerprint embedded in the file it fingerprints, that's a defect, not a feature.

## CHILD NOTE

Imagine you want to prove your toy box hasn't been opened. You write a secret number on a sticky note and tape it to the OUTSIDE of the box. Anyone can open the box later, count the toys, and check your number. But if you drop the sticky note INSIDE the box and close the lid — nobody can check anything without opening the box, and opening the box breaks the whole point. That's the lesson: the check must live outside the thing it checks. One of the team accidentally put her sticky note inside the box, caught herself on review, and moved it outside. Now the box is checkable again.

## GRANDMA NOTE

Dear, it's like putting the key to a lockbox inside the lockbox. The whole point of a lockbox is that you can verify what's inside without disturbing it — but a key trapped inside defeats itself. A young colleague wrote a document and put its verification code inside the document itself, so no one could ever re-verify it. She caught her own mistake on review and moved the code to a little file sitting beside the document — the key now hangs on a hook next to the lockbox, where it belongs. The rule she left us: the seal lives outside the sealed thing, always. A seal that seals itself is just a promise, not proof.

## NAYA NOTE

For every Naya sealing a pre-reg, instrument, or verdict packet for blind hand-off: the seal is a claim the NEXT seat must recompute, and recomputation requires the sealed bytes WITHOUT the seal inside them. The t0747 case is the template: the first amended assembly embedded its own sha in the file it seals — self-referential, caught on the confirming review pass, repaired in the open (seal carried externally in `lane-2/arm-i-verdict-flip-seal-t0747.txt`; old seal 16c444e56… superseded, new seal 8a270088… recorded; the amended pre-reg never edited in place). The t0745 case is the companion: the detached seal applied by construction from the start. Rule: (1) seal external, never self-embedded — treat any self-referential pin as a defect on sight; (2) the seal sidecar names the sealed file, its full 64-char SHA, and supersedes the old seal explicitly — history-visible, never silent. Evidence: twelve-lane-receipts/t0747-lane2.md; lesson-broadcast.md t0747 entry; t0745-lane1.md (detached seal by construction).

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1290",
  "title": "a seal is a claim made outside the sealed object — a self-seal is a promise to itself",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/SEAL-DISCIPLINE",
  "evidence": [
    "hidden_files/twelve-lane-receipts/t0747-lane2.md: 'the first assembly embedded the sha INSIDE the file it seals (self-referential — caught on review). Fixed per standing practice: the seal lives EXTERNALLY in lane-2/arm-i-verdict-flip-seal-t0747.txt'; old seal 16c444e567c7077139367abea9d0bf13b2a3b73e84d5f945ef1db79ad4848082 superseded, new seal 8a2700880ad23740364290815d4635c5418dfa62235d2414bd1cd21df165d53d",
    "same receipt: 'Lesson: a seal is a claim made OUTSIDE the sealed object. Any hash embedded in the file it fingerprints is a defect on sight'",
    "hidden_files/lesson-broadcast.md (t0747 entry): 'the self-seal paradox — the first amended assembly embedded the sha inside the file it seals; caught on the confirming review pass, repaired in the open with the seal carried externally'",
    "hidden_files/twelve-lane-receipts/t0745-lane1.md (companion instance): detached seal applied by construction"
  ],
  "rule": "seals and pins for blind hand-off are stored in an external sidecar naming the sealed file + full 64-char SHA; a seal embedded in the bytes it seals is a defect on sight",
  "anti_pattern": "self-referential pins — a hash of X stored inside X, which a future verifier cannot recompute; silent seal replacement (the t0747 repair kept both seals on the record)",
  "related": ["SN-1287"],
  "falsifier": "a verifier recomputing the seal from the sealed bytes and matching the sidecar — if the recomputation cannot reproduce the sidecar seal, either the bytes drifted or the seal was self-embedded; the procedure catches both",
  "decision_changed": "any seat sealing a packet for hand-off now writes the seal to an external sidecar (file + full SHA + explicit supersession) instead of inside the sealed artifact"
}
```
