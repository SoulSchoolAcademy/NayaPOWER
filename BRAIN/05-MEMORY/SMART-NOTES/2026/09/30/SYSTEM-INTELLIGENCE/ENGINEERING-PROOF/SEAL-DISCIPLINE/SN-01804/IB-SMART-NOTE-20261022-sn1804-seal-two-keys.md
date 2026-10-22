# SN-1804 — The Cold-Successor Seal Needs Both Keys

Intelligent Block: SN-1804
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22 (00:08 PDT tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A cold-successor seal is a two-key check: mtime-after-seal AND sha256-of-cold-brief == sealed hash. One key is a half-check — it can pass while the seal is broken. Both keys, every time, or the seal is not proven.

## 🩷 HUMAN NOTE

On the 2026-10-22T05:53Z night-dispatcher tick (t1240), brief-t1002-lane1.md was retired as a REVERSE-PHANTOM VARIANT: rotation listed it queued but the file was absent from the entire brief-queue tree, while the canonical receipt t1002-lane1.md (cold-successor seal proof, trace adopted + labeled from t1272) existed. The verdict rested on the seal — and the broadcast states the seal rule as a two-key check: "the seal check is mtime-after-seal AND sha256-of-cold-brief == sealed — both keys, not one." Neither key alone decides: the mtime proves the brief's file state is younger than the seal (freshness, not replayed), the sha256 proves the brief's content is the sealed content (identity, not substituted). A brief could pass one and fail the other — right bytes at the wrong time, or the right time with the wrong bytes. The seal is only proven when both hold.

## 🟣 CHILD NOTE

Imagine a treasure chest with TWO locks — one that checks you came at the right time, one that checks you have the right key. If you only check the key, a thief could come at midnight with a fake key. If you only check the time, anyone could walk in at noon. A seal is proven only when BOTH locks turn. Check the time AND the key.

## 🔵 GRANDMA NOTE

It's like the pharmacist checking your prescription twice: once for the date (is it still valid?) and once for the pill bottle's seal (is it the right medicine, unopened?). Either check alone can pass on a bad prescription — an old date with good pills, or a current date with the wrong pills. The seal on a brief works the same way: the date and the contents, both, every time.

## 🟠 NAYA NOTE

Reconcile and retire seats: when a sealed brief is retired or dequeued, the seal verification must assert BOTH keys — mtime-after-seal (file state younger than the seal event) and sha256-of-cold-brief == sealed hash (content identical to what was sealed) — and fail closed on either. A single-key pass is insufficient evidence of a valid seal; a retirement on one key is a procedural breach. Named the t1240 way: "both keys, not one." Write it as two explicit assertions in the check, not one combined line you could halve by habit.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1804",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-22T07:08:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "ENGINEERING-PROOF",
  "sub": "SEAL-DISCIPLINE",
  "lesson": "A cold-successor seal proof is a two-key check: mtime-after-seal AND sha256-of-cold-brief == sealed hash. Neither key alone decides; a retirement on a single-key pass is a procedural breach. The t1240 verdict on brief-t1002-lane1.md states the rule: 'the seal check is mtime-after-seal AND sha256-of-cold-brief == sealed — both keys, not one.'",
  "decision_change": "Future seal retirements: run both assertions (freshness key + identity key) and require both to pass before a sealed brief is dequeued or retired. A one-key pass no longer clears the seal; it escalates to a named manual check.",
  "falsifiability": "If a case is found where both keys pass and the seal is nevertheless broken (both keys insufficient), the two-key rule is revised upward. If a case is found where one key provably guards nothing that the other does not also guard — i.e., the keys are not independent — the rule is revised downward to one key. Absent either, the two-key rule stands.",
  "mechanism": "The two keys guard independent failure modes. mtime-after-seal guards freshness: a stale brief replayed under a new name would carry old file state, failing the time key. sha256-of-cold-brief guards identity: a substituted or drifted file would carry different bytes, failing the content key. Because the failure modes are independent, one key cannot see the other's failure — a single-key check is blind to half the seal's attack surface.",
  "evidence": [
    "hidden_files/lesson-broadcast.md [night-dispatcher t1240, 2026-10-22T05:53Z] DEQUEUE brief-t1002-lane1.md: same REVERSE-PHANTOM VARIANT (file absent from tree, canonical receipt t1002-lane1.md (cold-successor seal proof) present). Removed as done. Lesson: 'the seal check is mtime-after-seal AND sha256-of-cold-brief == sealed — both keys, not one.'"
  ],
  "cousins": [
    "SN-1780 (verify-by-presence — the file must be observed; the seal keys verify WHICH file and WHEN)",
    "t1240 REVERSE-PHANTOM VARIANT (a queued entry with no file and a receipt is done, not pending — the verdict this seal check enabled)"
  ],
  "applies_when": [["seal", "cold-successor"], ["dispatch", "queue-retirement"], ["proof", "freshness-identity"]],
  "enforcement": "The seal verification must assert both keys as two explicit assertions and fail closed on either; a sealed brief retired on a single-key pass is a procedural breach named at reconcile review. Form: the two-key check lives as a named step in the dequeue/retire path (scripted assertions or a named manual check), not as an inline one-liner.",
  "dedupe_guard": "Not a duplicate: sealed-note sha256 mentions in lessons.md concern content-hash evidence in other batteries, not the two-key seal-check rule (grep: zero 'both keys' seal-check hits in learn/lessons.md)."
}
```
