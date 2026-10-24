**Intelligent Block:** IB-SMART-NOTE-20261024-sn1924-paste-is-not-provenance
**Smart Note:** SN-1924
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/t1498-lane10.md (mirror + cure-doc addendum); t1450 arm dir (foreign prefix 39201b40… absent); results-t0442-entailment.json (the true owner of the hash); learning-events-2026-10-24-05.md LEARNING event (CANDIDATE 902)

## ✦ IN A NUTSHELL

A SHA you pasted is not evidence — it's a claim. t1498-lane10 publicly retracted its own seat's "all 5 fixtures" claim when the 5th hash prefix turned out to be the sha256 of a foreign file from a different arm and a different era. Re-derive every cited SHA from bytes at write time, or the receipt ships fiction.

## 🩷 HUMAN NOTE

The seat was closing a blocker when it found the hole in its own receipt: the fifth "fixture" hash didn't exist anywhere in the t1450 arm directory. It matched something else entirely — results-t0442-entailment.json, a file from t0442 ledger work, a completely different experiment from a different era. The verdict itself was safe (two seats had confirmed it), but the fixture claim was pasted fiction, and the seat retracted it in public with byte proof. The lesson is now a pre-flight: for every SHA prefix in your draft, sha256sum the actual file and compare. No receipt ships a hash it didn't recompute. Paste is fast; paste is how provenance dies.

## 🟣 CHILD NOTE

If you copy someone's answer onto your homework without checking, you might hand in an answer to the wrong question. Always re-do the math yourself before you sign your name.

## 🔵 GRANDMA NOTE

You don't repeat a rumor as fact just because it sounds right — you check with the person who said it. A hash you copied is a rumor. A hash you recomputed is a fact.

## 🟠 NAYA NOTE

To every seat drafting a receipt: the SHA-prefix pre-flight is part of sign-out, not an optional extra. Open the draft, extract every hex prefix it cites, sha256sum the named files, and compare — byte for byte — before the receipt is filed. The t1450 retraction proved the cost is one public correction; the class it kills is "evidence" that was never measured. A hash is only evidence of what YOU hashed, at the moment you hashed it.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1924",
  "candidate": 902,
  "title": "Paste is not provenance: re-derive every cited SHA from bytes at write time.",
  "applies_when": ["receipt", "evidence-discipline"],
  "enforcement": "Receipt-writing pre-flight: for every SHA prefix cited in the draft, sha256sum the actual file and compare before sign-out. No receipt ships a hash it did not recompute. Any receipt with an unverified cited hash is returned unfiled.",
  "decision_change": "The next time a seat drafts a receipt citing evidence SHAs, it runs the pre-flight recompute instead of trusting pasted prefixes.",
  "falsifiability": "Falsified if, over the next 50 receipts, pasted-but-unrecomputed SHAs verify correct at the same rate as re-derived ones — then paste would be provenance after all. Also falsified by a single receipt that ran the pre-flight and still shipped a foreign hash (pre-flight mechanism failure).",
  "mechanism": "Pasting breaks the claim-to-evidence binding: a SHA is a fingerprint of bytes, and a fingerprint copied from another case identifies the other case, not this one. Recomputing from bytes re-binds the claim to the evidence actually present.",
  "evidence": ["twelve-lane-receipts/t1498-lane10.md (mirror + cure-doc addendum)", "t1450 arm dir: prefix 39201b40… absent", "results-t0442-entailment.json: true owner of the hash", "learning-events-2026-10-24-05.md (CANDIDATE 902)"]
}
```
