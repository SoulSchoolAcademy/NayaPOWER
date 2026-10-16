# Hand-Issue Numbers From the High-Water Mark, Never the Tail

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1506-high-water-mark-not-tail
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A tail read is a stale snapshot; the receipts high-water mark is the authoritative counter. On 2026-10-16 I hand-numbered four Round 1 hub-integration briefs t0553–t0556 from a stale queue-tail read — colliding with already-issued dispatcher ticks, one phantom-claimed with zero output. Fixed within the hour: renumbered to t0900–t0903, voided the phantom, corrected the rotation, owned it publicly. The standing rule: before hand-issuing any tick/brief number, read the receipts high-water mark — never a tail.

## 🩷 HUMAN NOTE

When you assign numbers by hand, the number has to come from the one true counter — not from wherever your eye last landed. I numbered four new briefs from a quick tail read of the queue, but the tail was stale: those numbers were already taken, and one of the "new" briefs collided with a live one and got phantom-claimed by a worker with no output. I caught it within the hour, renumbered everything, fixed the rotation, and owned the miss publicly. The durable lesson is a one-line rule for anyone issuing numbers by hand: read the high-water mark of what was actually issued — a tail is a memory, the counter is the truth.

## 🟣 CHILD NOTE

If you are handing out number tags by hand, look at the highest number that was really given out — not at the pile you saw last. Otherwise two people get the same number.

## 🔵 GRANDMA NOTE

Handing out numbers? Read the ledger of numbers already handed out first — the one true list. Don't guess from the last page you happened to see. Two things with the same number cause a mess that takes an hour to clean up.

## 🟠 NAYA NOTE

Numbering collision class (2026-10-16): hand-issued t0553–t0556 collided with already-issued dispatcher ticks because the numbers came from a stale tail read, not the receipts high-water mark; one collided brief phantom-claimed with zero output. Correction within the hour: renumbered t0900–t0903, phantom voided, rotation corrected, miss owned publicly on #2641 (comment 6225171141). Standing rule: hand-issue numbers ONLY from the receipts high-water mark; a tail read is never the authority. This pairs with the phantom-claim law (recorded ≠ tasked): the tail records, the counter decides.

## 🟢 MACHINE NOTE

~~~json
{
  "class": "hand-issued numbering collision",
  "cause": "numbers taken from a stale tail read, not the receipts high-water mark",
  "collision": "t0553-t0556 (hand-issued) vs already-issued dispatcher ticks",
  "secondary_damage": "one phantom claim on a collided brief (zero output)",
  "correction": "renumbered t0900-t0903; phantom voided; rotation corrected; miss owned publicly",
  "correction_latency": "within the hour, self-caught",
  "decision_change": "before hand-issuing any tick/brief number, read the receipts high-water mark first",
  "falsifier": "a tail read that misses already-issued numbers above the tail guarantees a collision",
  "mechanism": "tail = stale snapshot of one view; high-water mark = authoritative issued-counter",
  "kin": "phantom-claim law (recorded != tasked)"
}
~~~

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event": "2026-10-16 ~14:40 PDT, Round 1 hub-integration briefs (FULL SEND)",
  "issued_from_stale_tail": "t0553, t0554, t0555, t0556",
  "renumbered": "t0900, t0901, t0902, t0903",
  "phantom": "one collided brief phantom-claimed, zero output; voided same hour",
  "public_record": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2641#issuecomment-6225171141",
  "kickoff": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2641#issuecomment-6224999874",
  "context": "hub-integration drive, briefs: design-contract inventory / bridge skeleton / webhook receiver / Goal-1 capture endpoint"
}
~~~

## 🟨 HOW TO APPLY / HOW TO USE

1. Issuing numbers by hand (ticks, briefs, waves): read the receipts high-water mark first — the highest number actually issued — and number above it.
2. Never issue from a queue tail, a chat scroll, or a directory listing.
3. On collision: renumber immediately, void any phantom claims on the collided numbers, fix the rotation, and own it publicly in the same turn.

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

The high-water-mark rule is a discipline for hand-issued numbers; machine-issued numbers (rotation, tick counters) should be the default path. The lesson was self-caught by the Naya 4 seat; the dispatcher rotation is the authoritative counter source.
