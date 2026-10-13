# A Renumbering Migration Ships the Same Identity Gate as a Single Stage

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0673-renumbering-migration-identity-gate
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 comment 6057019483 (2026-10-08).
**Provenance:** #1354 6057019483 ([NAYA 5 — HOURLY REPORT], 2026-10-08T09:36:54Z — "#1229 frozen — 549 Smart Notes blocked by a 4-duplicate-note-number test failure (Shawn's published top-10 priority #1)"); `progress-hourly-20261008-0930-enhanced.md` (hole #5). Related: SN-0666 (the same consolidation/renumbering migration's broken-smart-links defect), SN-0420, SN-0438, the stage-script claim check (added 2026-10-06 after the SN-0449/SN-0455/SN-0457 collisions).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #1229 — the Smart Notes capture series carrying 549 notes — is frozen by a promotion-test failure: **4 duplicate note numbers**. During the consolidation/dedup renumbering era (old SN-018..SN-0525 → successors SN-0589/SN-0593/SN-0595..SN-0617), four numbers were double-assigned, and the test caught it. The lesson: a note number is an **identity invariant**, not a label. The per-note staging guard (claim check in `stage_smart_note.py`, added 2026-10-06 — refuses on collision, first claim stands) proves the invariant one note at a time; but bulk migrations bypass it unless the migration is validated by the *same* uniqueness check. The gate firing here is correct behavior — fail-closed is the design working (SN-0438), and absorbing the anomaly to silence the tripwire is canonization, not a fix (SN-0420). The legal repair is to **renumber the four collisions**, never to weaken or skip the test. A frozen promotion on duplicate identity isn't blocking progress: it's preventing 549 notes from shipping with a corrupted registry, which would poison every downstream consumer (retrieval corpus, LEARN loop, promotion writer). This is the second defect from the same migration — SN-0666 caught it leaving 21 smart links pointing at dead paths.

## 🩷 HUMAN NOTE

Shawn — the 549 notes are safe but stuck: the consolidation accidentally gave 4 notes the same number, and the safety test caught it. That's the test doing its job, not a malfunction. The fix is to give those four their own numbers — not to turn the test off. This is your priority #1, and the fix is mechanical.

## 👶 CHILD NOTE

If two kids get the same locker number, neither one can find their stuff. You don't fix it by removing the lockers — you give each kid their own number.

## 👵 GRANDMA NOTE

It's like two houses on the same street with the same address, honey — the mailman can't deliver to either. You don't burn the mail. You fix the addresses.

## 🤖 NAYA NOTE

On Smart Note identity:

1. **A note number is an identity invariant: unique across the whole corpus, forever.** Treat a duplicate as a hard stop, never a warning.
2. **Any bulk migration (renumbering, dedup, consolidation) must run the same uniqueness claim-check as single-note staging** — validate *before* landing, not after the promotion gate catches it. The migration runner is the enforcement point for bulk work; the stage script is the enforcement point for single notes. Both must exist.
3. **When the gate fires on duplicate identity, renumber the collisions; never silence, skip, or weaken the test** (SN-0420). A green gate over duplicate identity is canonization, not a fix.
4. **Read the migration's whole family before declaring it clean** (SN-0390): this migration produced two defects — 21 broken smart links (SN-0666) and 4 duplicate numbers. Check for the third before the gate moves on.

## 🧠 MACHINE NOTE

```json
{
  "sn": "SN-0673",
  "class": "SMART-NOTE-REFINEMENT",
  "subcategory": "NUMBER-UNIQUENESS",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "A note number is an identity invariant — unique across the whole corpus, forever. Bulk migrations must pass the same uniqueness claim-check as single-note staging, validated before landing; the legal repair for a duplicate-number gate failure is renumbering, never weakening the test.",
  "worked_example": {
    "frozen_pr": "#1229 (549 Smart Notes)",
    "failure": "4 duplicate note numbers, caught by promotion test",
    "era": "consolidation/dedup renumbering (SN-018..SN-0525 -> successors)",
    "sibling_defect": "SN-0666 (21 smart links left pointing at dead paths by the same migration)",
    "per_note_guard": "stage_smart_note.py claim check (2026-10-06, first claim stands)",
    "board_comment": "#1354 6057019483"
  },
  "related": ["SN-0666", "SN-0420", "SN-0438", "SN-0390"]
}
```
