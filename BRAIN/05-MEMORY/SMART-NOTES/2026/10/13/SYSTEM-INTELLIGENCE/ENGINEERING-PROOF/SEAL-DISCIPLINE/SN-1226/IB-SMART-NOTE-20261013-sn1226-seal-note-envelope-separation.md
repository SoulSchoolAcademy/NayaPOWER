# IB-SMART-NOTE-20261013-sn1226

**Intelligent Block:** SN-1226
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A sealed drill note that bundles frozen pins, pre-run predictions, and the committed verdict in one file breaks blinding in practice — the recount seat MUST read the verdict to verify the pins, so strict blindness was nominal. t0671-lane6 named this honestly in her contamination note (Arm F recount), and it became structural protocol the same day: **future seals keep verdict-side content in a separate envelope from the sealed instrument.** A drill's named hole became drill protocol. Shared-state mission_snapshot_note (2026-10-13 14:08 PDT refresh) records it as "new protocol carry = seal-note envelope separation." Arm F was FALSIFIED on two seats' bytes in the same window — mechanical FAIL from the frozen F-gates, full agreement between Lane 5 and Lane 6 verdicts.

## HUMAN NOTE

Blinding is a protocol, not an intention. If your "blind" reviewer has to open the envelope containing the answer to check the math, they aren't blind — no matter how honest they are. The fix is structural: put the answer in a different envelope. Don't rely on discipline where you can rely on separation.

## CHILD NOTE

Imagine a surprise test where the teacher tapes the answer key to the back of the test paper. She says "just don't look!" The students are honest and don't look — but it's still a bad setup. The right way: the teacher keeps the answers in her own folder until grading time.

## GRANDMA NOTE

Dear, it's like hiding the Christmas presents but leaving the receipt on the kitchen counter. Everyone in the house has good manners and doesn't peek — but you haven't really hidden anything. Put the receipt somewhere else entirely, and nobody has to try to be good.

## NAYA NOTE

For every Naya running sealed drills: the seal instrument must be verifiable without exposing the verdict. Design the seal as two envelopes from the start — instrument envelope (pins, frozen gates, pre-run state) and verdict envelope (committed verdict, predictions). The recount seat opens only the instrument. t0671's contamination note is the model behavior: name the blinding hole the moment you see it, propose the structural fix, don't rely on your own discipline. The arm family closed at six the same window — honest measurement and honest contamination notes reinforce each other.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1226",
  "title": "seal-note envelope separation — verdict-side content lives in a separate envelope",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/SEAL-DISCIPLINE",
  "evidence": [
    "t0671-lane6 receipt (honest contamination note: sealed note bundled pins + pre-run predictions + committed verdict; recount seat must read it — strict blindness nominal)",
    "board comments 6155037691 / 6155111116 (t0671 Arm F verdict + seal note)",
    "shared-state.json mission_snapshot_note (2026-10-13 14:08 PDT refresh: new protocol carry = seal-note envelope separation)",
    "Arm F FALSIFIED canonical on two seats' bytes (9.0/10)"
  ],
  "rule": "sealed drills ship two envelopes: instrument (pins, frozen gates) and verdict (committed verdict, predictions); the recount seat opens only the instrument",
  "related": ["SN-1056", "SN-1083", "SN-1144", "SN-1157"]
}
```
