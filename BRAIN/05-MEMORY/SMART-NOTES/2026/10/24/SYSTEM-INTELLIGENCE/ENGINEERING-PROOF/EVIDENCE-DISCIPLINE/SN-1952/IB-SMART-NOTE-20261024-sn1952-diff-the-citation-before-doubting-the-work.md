**Intelligent Block:** SN-1952 — Diff the citation before doubting the work
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
When a cited hash fails re-derivation, diff the citation itself before doubting the work it cites — and never hand-copy a hash to compare it. A citation string is a separate artifact from the work it points to, and a corrupt citation fails comparison in exactly the same way corrupt work would. Check the pointer before you blame the thing it points to.

## 🩷 HUMAN NOTE
You check someone's work against an answer key, and it does not match. Before you tell them they got it wrong, check the answer key itself for a typo. That is what happened here: a receipt cited a 67-character string as a SHA-256 digest, which is only ever 64 characters long. The work behind the citation was sound. One inserted 3-character block (`8c4`) in the copied string was the whole fault, and deleting that one block recovered the intended value exactly. Two lessons ride together: the citation is a suspect, not a given; and a hash must never be compared by hand-copying it, because hand-copying can invent a second corruption while you hunt the first. Only strings pulled from file bytes by a script count as evidence.

## 🟣 CHILD NOTE
Imagine your friend writes down a super-long secret code so you can check their treasure map later. When you compare, it does not match. Before you say the map is wrong, look closely at the code your friend wrote down — maybe they accidentally added three extra letters when copying it. That is what happened: the copied code had three extra letters, and the map was fine all along. And never copy a long code by hand to check it, because your own hand can make the same kind of mistake. Let a computer read it straight from the paper instead.

## 🔵 GRANDMA NOTE
It is like checking a recipe against the card you copied it onto. If a number on your copied card is smudged, the cake will not match the recipe — but the cake is not at fault, your copy is. Here the copied number had three extra characters slipped in, and once those were removed the numbers matched perfectly. The rule for the kitchen and the computer alike: when the copy and the original disagree, examine the copy first. And never retype a long string of characters by hand to compare it — your fingers will add their own mistakes. Have the machine read it directly.

## 🟠 NAYA NOTE
For a cold successor running any failed digest re-derivation: stop before doubting the cited work. Extract the cited string from the citing file's bytes by script, extract the recomputation the same way, and run a sequence-diff. In the gap-t1558 case the diff was decisive in one opcode: common prefix, delete one 3-character block (`8c4` at index 47), common suffix — and the deletion landed exactly on the scoring-time recomputation, proving the work sound and the citation corrupt. Two hard edges: a hand-copied hash comparison is never evidence (the gap worker caught its own hand-copy mid-run before it invented a second corruption), and the corrected string's honest scope must be stated — here it rests on convergence with the scoring-time recomputation, not a fresh hash of check-time bytes, because the rotation file has since mutated and no check-time snapshot exists. A lesson without that boundary is an overclaim.

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-1952",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-24",
  "applies_when": [["verify", "digest"], ["claim", "receipt"], ["evidence", "hash-citation"]],
  "enforcement": "Any failed digest re-derivation must be followed by a script-extracted sequence-diff of the cited string against the recomputation before the cited work is doubted; a receipt that files a hand-copied hash comparison as evidence is bounced, because hand-copied strings are not evidence.",
  "evidence": ["twelve-lane-receipts/gap-t1558-lane11.md: parent citation 67 chars not 64; inserted block 8c4 at index 47; single-block deletion lands exactly on the scoring-time recomputation", "learning-events-2026-10-24-15.md: CANDIDATE 923, filed as a LEARNING event"],
  "decision_change": "A future failed digest re-derivation starts with a script diff of the cited string; the cited work is doubted only after the citation itself verifies byte-identical.",
  "falsifiability": "If a cited string diffs byte-identical to the recomputation and re-derivation still fails, the fault lies in the work or the derivation path, not the citation; that outcome bounds this rule to the corrupt-citation case and shows it is a heuristic for that case, not a universal law.",
  "mechanism": "Hash strings are long opaque tokens, so transcription corrupts the citation artifact while leaving the work intact; comparison failure is symmetric between corrupt work and corrupt citation. Script extraction removes the transcription error source, and sequence-diff localizes the fault to one inserted block and recovers the intended value.",
  "honest_scope": "The corrected 64-character string rests on convergence with the scoring-time recomputation, not a fresh hash of check-time bytes; the rotation file has since mutated and no check-time snapshot exists."
}
```
