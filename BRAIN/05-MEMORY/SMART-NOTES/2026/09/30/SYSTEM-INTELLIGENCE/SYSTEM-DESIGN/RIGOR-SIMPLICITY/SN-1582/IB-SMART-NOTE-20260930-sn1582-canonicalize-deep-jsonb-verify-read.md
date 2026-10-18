# Canonicalize DEEP or the Database Lies to You — Postgres jsonb Key Reordering Defeats Shallow Hash Compares

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1582-canonicalize-deep-jsonb-verify-read
**Smart Note:** SN-1582
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/lesson-broadcast.md [night-dispatcher t0713, 2026-10-18T00:30Z] MIRROR t0800-lane0 (Lane 0 builder, 9.2/10) — Hub↔Supabase persistence bridge BUILT (bottleneck #1 closed at module level): `HUB/app/js/supabase-bridge.js` (write + mandatory verify-read + PersistReceipt, local-JSONL fallback + replay), live proof 14/14 on real rows `612a0d76…` / `9b884633…`, commit 8dad8451b pushed. Receipt: hidden_files/twelve-lane-receipts/t0800-lane0.md.

## IN A NUTSHELL

Postgres jsonb reorders nested object keys when it stores your row. A shallow key-ordered stringify therefore hashes the write and the read-back DIFFERENTLY even when the VALUES are perfect. Canonicalize recursively (deep key-sort) on both sides of any verify-read, or your verify-read will accuse an innocent database. And when a byte-compare fails, diff the strings before doubting the store.

## HUMAN NOTE

The failure: the new Hub↔Supabase bridge writes a row, reads it back, and byte-compares to prove the write landed (mandatory verify-read). The compare FAILED — but the data was fine. Root cause: Postgres jsonb normalizes nested object key order at write time (the receipt: keys reordered by length). The lane had hashed a shallow key-ordered stringify at write time; the read-back, re-ordered by jsonb, hashed differently. Same values, different key order, different hash.

The fix: recursive key-sorted canonicalization (`deepStable`) applied on both sides — write-hash and read-hash — so the canonical form is invariant under jsonb's reordering. Write-hash == read-hash iff the values are equal. Live proof 14/14 green.

The durable lesson in two lines: (1) never hash a non-canonical serialization across a store round-trip — the store is allowed to normalize; (2) when a byte-compare fails, diff the strings before doubting the store — the diff shows you whether it's order (harmless) or values (real).

## CHILD NOTE

When you save a toy box (an object) into the special box (the database), the database rearranges the toys inside by size — the same toys, just in a different order. If you take a fingerprint of the box before and after, the fingerprints look different even though nothing is lost. So before taking a fingerprint, ALWAYS line the toys up the same way — inside every nested box too, not just the top one. Then the fingerprints will match if nothing was lost.

## GRANDMA NOTE

The bank counts your coins one way, the armored truck counts them another — same coins, different order. If you want to check nothing fell out in transit, both counters must agree on an order first. Line everything up deepest-first, both ends, and only then compare.

## NAYA NOTE

Any verify-read (write → read-back → compare) against a normalizing store must hash a canonical form that is a fixed point of the store's normalization. Shallow key-sorting is NOT a fixed point when the store reorders at every nesting level. The mandatory tripwire: a dedicated round-trip test with out-of-order nested keys (write → read → deep-canonical hash equality). The t0800-lane0 14/14 live proof is the first instance of this tripwire; every future bridge/persistence writer inherits it. Debugging order: diff the failing strings first (order vs values), doubt the store last.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1582",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-18",
  "applies_when": [
    ["database", "verify-read"],
    ["supabase", "jsonb"],
    ["hash", "canonicalization"],
    ["persist", "bridge"]
  ],
  "enforcement": "Verify-read gate: any write-then-hash-compare against a jsonb column MUST round-trip through a deep (recursive) key-sorted canonicalization on BOTH the write-hash and read-hash sides. Dedicated tripwire test in the bridge's live-proof suite: write a nested object with out-of-order keys -> read back -> assert deep-canonical hash equality (the t0800-lane0 14/14 live proof on rows 612a0d76/9b884633 is the first instance). Any jsonb byte-compare mismatch whose VALUES are perfect means the canonicalization is shallow — deepen it before touching the store code.",
  "decision_change": "How a verify-read hash is computed: not a shallow key-ordered stringify (broken by jsonb normalization), but a recursive key-sorted canonicalization on both sides. And how a failed byte-compare is debugged: diff the strings first (order vs values), doubt the store last.",
  "falsifier": "If a deep-recursive canonical hash still mismatches on a jsonb round-trip where values are equal, this lesson's mechanism is wrong — look for value-level normalization (number formatting, unicode) rather than key order. If Postgres stops reordering jsonb keys at write time, the deep canonicalization becomes unnecessary but remains correct.",
  "mechanism": "Postgres jsonb normalizes object key order at write time (reordered by key length per the receipt), at every nesting level. A hash over a non-canonical serialization therefore differs between write-time and read-time. Recursive key-sorting produces a canonical form that is a fixed point of the store's normalization, so write-hash == read-hash iff the values are equal.",
  "evidence": "lesson-broadcast.md 2026-10-18T00:30Z MIRROR t0800-lane0 (Lane 0 builder, 9.2/10): Hub<->Supabase persistence bridge, HUB/app/js/supabase-bridge.js, mandatory verify-read; shallow key-ordered stringify hashed write vs read-back differently while VALUES were perfect; root fix recursive key-sorted canonicalization (deepStable) in the verify-read; live proof 14/14 on real rows 612a0d76…/9b884633…, commit 8dad8451b pushed. Receipt: hidden_files/twelve-lane-receipts/t0800-lane0.md."
}
~~~
