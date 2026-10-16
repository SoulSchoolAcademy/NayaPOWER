# Intelligent Block
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15 ~17:08 PDT (Smart Note distillation tick)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-1434
**Provenance:** shared-state.json mission_snapshot_note (director pass 2026-10-15 16:38 PDT): "Naya 2 heartbeat LEDGER-FORMAT-BLINDNESS (6204350017 — 7 night-shift receipts missed by parser watermark-falsification; new named failure mode, repair routed)"

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL
A parser whose format assumptions drift from what producers actually emit doesn't warn you — it silently stops seeing receipts. Seven night-shift receipts were missed because the parser's watermark-falsification checks assumed a fixed receipt shape while producers moved on. The law: any reader of receipts must fail LOUD on unrecognized format, never skip quietly — and the reader's assumptions must be re-proven against live producer bytes, not the schema in someone's head.

## HUMAN NOTE
On 2026-10-15, Naya 2's heartbeat found seven night-shift receipts that simply never made it into the ledger — not because they didn't exist, but because the parser reading them expected one format and the receipts had another. The parser didn't raise an error. It didn't flag a mismatch. It just moved on, and the seven receipts vanished from the count. This is what happens when the thing that reads and the thing that writes evolve separately: the reader's mental model of the format becomes a silent filter. The lesson: a parser that skips what it doesn't understand is a liar by omission. Build parsers that stop loudly on any format they can't recognize, and re-check them against real receipts regularly.

## CHILD NOTE
Imagine a teacher who only counts homework folded in half. If a student hands in their homework folded in thirds, the teacher doesn't say "wrong fold" — she just doesn't count it. That's what happened: the receipt-reader only counted receipts in the old shape, and seven receipts in the new shape disappeared without anyone being told.

## GRANDMA NOTE
Darling, imagine a mailman who only picks up white envelopes. When the post office starts using cream envelopes, he doesn't knock and ask — he just leaves them on the porch, and the bills pile up unpaid. The lesson is simple: when something's job is to collect everything, it must raise its hand the moment it sees a shape it doesn't recognize — never just skip it quietly.

## NAYA NOTE
Named failure mode LEDGER-FORMAT-BLINDNESS (2026-10-15, Naya 2 heartbeat 6204350017, #2641). Mechanism: parser's watermark/format regexes pinned an assumed receipt shape; producers emitted new fields; regex silently non-matched; 7 receipts dropped with no alarm, corrupting the ledger count. The class: format-parsing readers whose violation mode is silent non-match. Cure (routed): fail-loud on unrecognized format; schema-change tests against live producer bytes, not assumed shapes. This is the receipt-layer twin of the merge-commit receipt-blindness lesson (SN-1184): presence of machinery without liveness of machinery.

## MACHINE NOTE
```json
{
  "sn": "SN-1434",
  "slug": "ledger-format-blindness",
  "category": "SYSTEM-DESIGN",
  "sub": "MEASUREMENT-INTEGRITY",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "failure_mode": "LEDGER-FORMAT-BLINDNESS",
  "lesson": "A receipt parser must fail LOUD on unrecognized format, never skip quietly; the parser's format assumptions must be re-proven against live producer bytes.",
  "mechanism": "parser's watermark/format regexes assumed a fixed receipt shape; producers emitted new fields; silent non-match dropped 7 night-shift receipts with no alarm.",
  "decision_change": "Future receipt/ledger parsers must alarm on unknown formats (unknown-field alerts) and be regression-tested against live producer bytes, never against an assumed schema.",
  "falsifiability": "If the 7 missed receipts are re-run through the repaired parser and it catches them, the format-blindness attribution is confirmed; if a different cause (e.g., transport gap) explains the misses, the attribution is wrong.",
  "evidence": ["#2641 comment 6204350017 (Naya 2 heartbeat 2026-10-15)", "shared-state.json mission_snapshot_note 2026-10-15 16:38 PDT"],
  "related": ["SN-1184 (merge-commit receipt-blindness)"]
}
```
