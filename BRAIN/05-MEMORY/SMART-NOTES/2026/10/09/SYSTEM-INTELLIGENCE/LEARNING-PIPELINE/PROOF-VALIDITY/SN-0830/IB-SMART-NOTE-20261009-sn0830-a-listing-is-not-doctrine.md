# IB-SMART-NOTE-20261009-sn0830-a-listing-is-not-doctrine

Intelligent Block: SN-0830
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

The C5 longitudinal-proof instrument's first run lied, then told the truth. C5.1 (note→doctrine integration rate) initially counted `REAL-TREE.json` as a doctrine source — but the tree file cites every Smart Note by path as an index listing. A listing is not doctrine. The citation was excluded, and the honest metric is 59/629 recent notes integrated (9.4%) — the instrument correctly FAILs at the 0.60 threshold. Anti-gaming lesson: any metric that counts index entries as integration inflates to 100% and proves nothing.

## HUMAN NOTE

On 2026-10-09 the C5 driver (Naya 4) smoke-tested `tools/longitudinal/note_integration_rate.py` (C5.1) and `tools/longitudinal/citation_graph.py` (C5.2) on the live corpus. Two honest outcomes:

- C5.1: 59 of 629 recent notes integrated into doctrine (9.4%), 0 stale → the gate honestly FAILs at the 0.60 threshold.
- First run caught registry-path inflation — `REAL-TREE.json` cites every SN by path — now excluded. A listing is not doctrine.
- C5.2: 3498 citation edges, 0 verifiable cross-seat reuse — no `seat:`/`date:` attribution exists in current artifacts, so nothing is counted. Reported, not inflated.

Same report: 19 duplicate SN-IDs in the live registry (e.g. SN-018 = two different notes) + 1 nonstandard vanity ID (`SN-NET-POWER-MAGIC-001`) — C5.7 material, flagged for repair, not silently normalized.

Provenance: NayaPOWER #1354 comment 6090349635 ([C5-DRIVER] Longitudinal proof, 2026-10-09T22:31:53Z); draft PR #2071 (`naya4/c5-longitudinal-proof-v1`).

## CHILD NOTE

If you want to know how many lessons actually got used, don't count the list of lessons — count the lessons people actually used. A list of names isn't the same as the work. Be honest with the counting, even when the number is small.

## GRANDMA NOTE

They built a tool to check whether the lessons the AI learns actually make it better. The first test was almost fooled: a master list that mentions every lesson by name made it look like all of them were being used. But being mentioned on a list isn't the same as being learned and used. They fixed the tool to count only real use — and the honest answer was that only about 9 in 100 lessons had truly stuck. An honest small number beats a lying big one.

## NAYA NOTE

Measurement-integrity doctrine for any "did learning work" instrument:

1. An index citation (a path listing, a registry mention) is NOT integration into doctrine. Exclude all index-like sources from integration numerators, or the metric pegs at 100% and proves nothing.
2. A first run that catches its own inflation is a sign the instrument works — document the exclusion, don't quietly keep the inflated number.
3. Zero-with-explanation beats an inflated positive: C5.2's "0 verifiable cross-seat reuse" is honest because attribution doesn't exist yet. Never synthesize attribution to make the number prettier.
4. Companion check from the same run: duplicate IDs (SN-018 twice) and vanity IDs (`SN-NET-POWER-MAGIC-001`) must be flagged as repair items, never silently normalized — normalization destroys the evidence the metric depends on.

## MACHINE NOTE

```json
{
  "sn": "SN-0830",
  "truth_state": "CANDIDATE",
  "director_stated": null,
  "doctrine": "index citation is not doctrine integration",
  "anti_gaming_rule": "exclude registry/tree index listings from integration-rate numerators",
  "observed_values": {"C5.1_integration_rate": "59/629 = 0.094", "C5.1_gate": "FAIL at 0.60 threshold", "C5.2_verifiable_cross_seat_reuse": 0, "duplicate_sn_ids": 19, "vanity_ids": 1},
  "repair_flags": ["19 duplicate SN-IDs (e.g. SN-018 x2)", "SN-NET-POWER-MAGIC-001 vanity ID"],
  "provenance": "NayaPOWER#1354/6090349635",
  "artifact": "draft PR #2071, tools/longitudinal/note_integration_rate.py + citation_graph.py"
}
```
