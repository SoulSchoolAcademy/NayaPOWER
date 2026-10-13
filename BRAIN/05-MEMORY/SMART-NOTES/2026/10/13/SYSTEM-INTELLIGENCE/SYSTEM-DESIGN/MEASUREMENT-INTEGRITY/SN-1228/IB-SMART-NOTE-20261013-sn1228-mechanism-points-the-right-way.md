# IB-SMART-NOTE-20261013-sn1228

**Intelligent Block:** SN-1228
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Never attribute a performance change to a commit whose diff mechanism predicts the opposite. t0671-lane11 tested the tempting story — "the smart_note_v2.py validator made cold retrieval faster (t0614 → t0660, ~25–35%)" — against the bytes: the diff ADDS hot-path work (new `_load_validated_registry()` sha256-hashes all 603 eligible pages before scoring re-reads them), entry counts were byte-identical at all three tips (631/603), and the "607→658 file growth" was a derivation-scope artifact (stdlib included vs excluded — set-diffed, not quoted). All four falsifiable checks FAILED in the attribution direction. The addendum reported **UNATTRIBUTED** with the failed checks named — and that negative is a complete deliverable: it hands the bar packet a falsifiable criterion (quote the band center 0.9682s on current bytes; never cite "the validator made retrieval faster") plus the one re-measurement that could close it (old vs new code on one tip, sealed per-trial env telemetry). Correlation is not attribution; mechanism direction is the test.

## HUMAN NOTE

It's tempting to look at a timeline — new code landed, then things got faster — and call it a cause. But the only evidence that counts is the mechanism: what does the code actually DO on the hot path? Here the diff said the new code does MORE work per query (hashing every eligible page before scoring even reads them), so it can't be the cause of a speedup. The seat said "unattributed" instead of picking the story — and wrote down exactly which checks failed and what experiment would answer it for real. An honest "I don't know, and here's what would tell us" is a finished piece of work. A confident story that points the wrong way is not.

## CHILD NOTE

Imagine your bike got faster, and you say "it must be my new shiny bell!" But the bell doesn't make bikes faster — it just sits there ringing. The lesson: before you say what made something faster, check what the thing actually does. If the thing can't make it faster, say "I don't know yet" — and write down how we could find out. That's not failing. That's the right answer.

## GRANDMA NOTE

Dear, it's like taking credit for the soup because you stirred it — when someone else turned up the heat. The stirring didn't warm the pot. Before you claim the credit, look at what actually made it hot. And if you can't see it, say so — "I don't know" is a perfectly good answer, as long as you also say how we'd find out.

## NAYA NOTE

For every Naya writing attribution claims: the diff's mechanism direction is the gate. Before attributing any measured change (latency, hit rate, score) to a byte change, state the mechanism: does the diff ADD or REMOVE work on the measured path? If the mechanism predicts neutral-to-slower and you measured faster, the claim is UNATTRIBUTED — report it so, with the four failed checks named: (1) mechanism direction, (2) entry-count identity, (3) growth-as-artifact check (set-diff, never quote counts), (4) instrument-protocol identity. Then give the bar exactly what it may cite (the band center on current bytes) and what it must never cite ("the validator made retrieval faster"). The warm-band co-movement rule: when cold AND warm bands move together with no code change explaining it, suspect host state — name it, don't claim it.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1228",
  "title": "mechanism must point the right way — an honest UNATTRIBUTED is a complete deliverable",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "category": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/MEASUREMENT-INTEGRITY",
  "evidence": [
    "#2175 comment 6155536345 (t0671-lane11 sign-out: UNATTRIBUTED, four failed checks named, 'mechanism points the wrong way')",
    "receipt twelve-lane-receipts/t0671-lane11.md (blob 92d8b2bef7… → fe6f2b4cec8…; 631/603 entries byte-identical at all three tips; addendum sha256 dcedf03f4cbe2cf6fd9d37ba807b4c3198a45c6a6b0c76b7e495f0e8b6a9d9c9)",
    "trial JSONs: t0601 1.3037/1.2760 · t0614 1.5854/1.3100 · t0660 0.9463/0.9901; warm band 0.45–0.79s → 0.32–0.35s"
  ],
  "rule": "no speedup claim is attributed to a commit without a stated mechanism on the measured path whose direction agrees with the measurement; UNATTRIBUTED with named failed checks is the complete deliverable",
  "anti_pattern": "timeline-correlation cited as cause; file-list counts quoted as repo growth without set-diff",
  "related": ["SN-01227"]
}
```
