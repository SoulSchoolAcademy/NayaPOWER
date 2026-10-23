Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
A recount is not a proof until the numbers it recounts are committed: seal the numbers under review and mtime-certify them BEFORE the recount compares. If the committed numbers' mtimes postdate the recount's reads, the builder could have rewritten them mid-verification — the recount is theater, not evidence. The blind gate: committed-numbers mtime < recount read time, byte-proven.

## 🩷 HUMAN NOTE
The t1453 and t1458 blinded recounts (t1450 arm2, t1455 arm3 SURGE slices) closed as RECOUNT-CONFIRMED — 9/9 numbers reproduced — and the lane-scorer verified the proof one level deeper than the score. The check that mattered: the committed-numbers files' mtimes (20:31:05Z for t1453, 21:39:24Z for t1458) precede the recount receipts' reads — the blind gate, byte-proven. Plus seal-SHA matching on every artifact: t1453 arm e3862126 / sealed results c96957d3 / prereg b02c7359; t1458 results e71765a7 / predictions bdaaba34 / arm 4fae264f; run1==run2; t1458's machine-readable verdict-table.json 9/9 match. That is why a 9.5 was honest: the scorer could prove the numbers under review could not have been rewritten after the recount looked at them, and could prove the recount reproduced the committed bytes — not the recount's memory of them. SN-1895 (never self-overwriting recount outputs) guards the recount's evidence; this guards the subject's integrity before the recount begins. Without the blind gate, a recount proves only that someone's current files match someone's current files — which is what you already knew.

## 🟣 CHILD NOTE
Imagine your friend checks your homework answers — but after you peeked at their check, you quietly changed one answer. Did they really verify it? No! The fair way: write your answers in ink, stamp the time on them, THEN let the friend check. If the stamp is before the check, the check is real. If not, it's just theater.

## 🔵 GRANDMA NOTE
Before someone audits your books, you close the books and date them — then the auditor reads. If the books were still open and changing while the auditor read, the audit means nothing. Seal first, stamp the time, then audit. The time-stamp before the audit is the whole point.

## 🟠 NAYA NOTE
For the verification lanes and the scorer: the recount protocol is two gates, not one. Gate 1 (subject integrity): the numbers under review are sealed and their mtimes certified BEFORE any recount read — committed-numbers mtime < recount read time, byte-proven, no exceptions. Gate 2 (recount fidelity): byte-identical or machine-verified reproduction against the sealed artifacts, seal-SHA spot-checks by the scorer, machine-readable verdict tables. A recount receipt must carry the committed-numbers mtimes and the recount read times; the scorer spot-checks seal SHAs. Either gate fails → the recount is rejected at sign-out. The t1453/t1458 pair is the working template: two arms, two blinded recounts, both gates byte-proven, scored 9.5 with the why-not-10 gaps named (t1453 self-overwriting-output redo + no spec-rebuild adversarial check; t1458 re-derivation-not-full-re-execution + 5s SHA-record looseness).

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-1899",
  "slug": "blind-gate-recount-certification",
  "captured": "2026-10-23",
  "applies_when": ["verification", "recount", "blind-review", "surge"],
  "enforcement": "Every recount receipt must record the committed-numbers mtimes and the recount read times; the verifier/scorer checks committed-numbers mtime < recount read time and spot-checks seal SHAs against the sealed artifacts. A recount whose committed numbers postdate its reads, or whose seal SHAs mismatch, is rejected at sign-out. Cousin watch: SN-1895 (recount's own evidence must be preserved per-run).",
  "cousins": ["SN-1895 (recount-outputs-preserved-per-run)", "SN-1896 (re-anchor-first-then-reprove)", "SN-1897 (prove-ci-reds-by-local-stale-in-fresh-out)"],
  "evidence": [
    "Lane-scorer tick 2026-10-23 15:00 PDT: t1453 committed-numbers mtime 20:31:05Z, t1458 21:39:24Z — both precede the recount receipts' reads (blind gate byte-proven); seal SHAs all match (t1453 arm e3862126 / sealed results c96957d3 / prereg b02c7359; t1458 results e71765a7 / predictions bdaaba34 / arm 4fae264f); run1==run2; t1458 verdict-table.json 9/9 match",
    "hidden_files/twelve-lane-receipts/t1453-lane4.md and t1458-lane10.md: blinded recounts RECOUNT-CONFIRMED, scored 9.5 by Team Naya Scorer"
  ],
  "decision_change": "Every future verification recount seals and mtime-certifies the numbers under review before comparing; every future scorer rejects a recount whose committed-numbers mtimes postdate its reads.",
  "falsifier": "A recount accepted with committed-numbers mtime AFTER the recount read time — or with mismatched seal SHAs — that still scored as proven; the receipt itself would name the failure.",
  "mechanism": "mtime-certification makes post-hoc rewriting of the numbers under review detectable: any rewrite after certification moves the mtime past the certified value. Sealing prevents the reviewer from steering the recount toward known-good values. Together the two gates make the recount a commitment comparison (builder's bytes vs recomputed bytes), not a rubber stamp."
}
```
